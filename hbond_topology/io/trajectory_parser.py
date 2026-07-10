"""
Parses molecular dynamics trajectory files from various sources
(LAMMPS, CP2K, XYZ, VASP, etc.) using ASE as the unified backend.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Generator, Union
from pathlib import Path
import re

# ASE imports
from ase.io import read, iread
from ase import Atoms
from ase.data import atomic_numbers, atomic_masses_iupac2016, chemical_symbols


# Use atomic numbers from periodic table for element-to-type mapping
# H=1, He=2, Li=3, ... O=8, ... (all 118 elements supported)
DEFAULT_ELEMENT_TO_TYPE = atomic_numbers


@dataclass
class Frame:
    """
    A single trajectory frame containing atomic data.
    
    This is a unified frame structure that can be created from either:
    - ASE Atoms objects (recommended)
    - Legacy LAMMPS-style numeric data (backward compatible)
    
    Attributes
    ----------
    timestep : int
        Frame index or timestep number
    n_atoms : int
        Number of atoms in the frame
    box_bounds : np.ndarray
        Box boundaries, shape (3, 2) - [[xlo, xhi], [ylo, yhi], [zlo, zhi]]
    symbols : np.ndarray
        Element symbols for each atom (e.g., ['O', 'H', 'H', ...])
    positions : np.ndarray
        Atomic positions, shape (n_atoms, 3)
    atom_types : np.ndarray, optional
        Numeric atom types (for backward compatibility)
    atom_ids : np.ndarray, optional
        Atom IDs (for backward compatibility)
    """
    
    timestep: int
    n_atoms: int
    box_bounds: np.ndarray
    symbols: np.ndarray
    positions: np.ndarray
    atom_types: Optional[np.ndarray] = None
    atom_ids: Optional[np.ndarray] = None
    
    def __post_init__(self):
        """Ensure atom_types and atom_ids are set for backward compatibility."""
        if self.atom_ids is None:
            self.atom_ids = np.arange(1, self.n_atoms + 1)
        if self.atom_types is None:
            self.atom_types = np.array([
                DEFAULT_ELEMENT_TO_TYPE.get(s, 999) for s in self.symbols
            ])
    
    @property
    def box_lengths(self) -> np.ndarray:
        """Return box lengths in x, y, z directions."""
        return self.box_bounds[:, 1] - self.box_bounds[:, 0]
    
    def get_atoms_by_type(self, atom_type: int) -> np.ndarray:
        """Get indices of atoms with specified numeric type."""
        return np.where(self.atom_types == atom_type)[0]
    
    def get_atoms_by_symbol(self, symbol: str) -> np.ndarray:
        """Get indices of atoms with specified element symbol."""
        return np.where(self.symbols == symbol)[0]
    
    def get_positions_by_type(self, atom_type: int) -> np.ndarray:
        """Get positions of atoms with specified numeric type."""
        mask = self.atom_types == atom_type
        return self.positions[mask]
    
    def get_positions_by_symbol(self, symbol: str) -> np.ndarray:
        """Get positions of atoms with specified element symbol."""
        mask = self.symbols == symbol
        return self.positions[mask]
    
    @classmethod
    def from_ase_atoms(
        cls, 
        atoms: Atoms, 
        timestep: int = 0,
        element_to_type: Optional[Dict[str, int]] = None
    ) -> "Frame":
        """
        Create Frame from ASE Atoms object.
        
        Parameters
        ----------
        atoms : ase.Atoms
            ASE Atoms object
        timestep : int
            Frame index/timestep
        element_to_type : dict, optional
            Mapping from element symbols to numeric types
        
        Returns
        -------
        Frame
            Unified frame object
        """
        element_map = element_to_type or DEFAULT_ELEMENT_TO_TYPE
        
        # Extract cell/box information
        cell = atoms.get_cell()
        if cell.any():
            # Use cell diagonal as box bounds (works for orthorhombic cells)
            box_bounds = np.array([
                [0.0, cell[0, 0]],
                [0.0, cell[1, 1]],
                [0.0, cell[2, 2]]
            ])
        else:
            # No cell defined, use atom extent
            positions = atoms.get_positions()
            min_pos = positions.min(axis=0) - 1.0
            max_pos = positions.max(axis=0) + 1.0
            box_bounds = np.column_stack([min_pos, max_pos])
        
        symbols = np.array(atoms.get_chemical_symbols())
        atom_types = np.array([element_map.get(s, 999) for s in symbols])
        
        return cls(
            timestep=timestep,
            n_atoms=len(atoms),
            box_bounds=box_bounds,
            symbols=symbols,
            positions=atoms.get_positions(),
            atom_types=atom_types,
            atom_ids=np.arange(1, len(atoms) + 1)
        )


def parse_lammps_data_masses(data_filepath: Union[str, Path]) -> List[str]:
    """
    Parse a LAMMPS data file (.data, .lmpdat) to extract the atom type → element
    mapping from the Masses section, returned as a specorder list for ASE.

    The Masses section may have inline comments with element symbols, e.g.:
        1 12.0107  # C
        2 1.0079   # H

    If a comment contains an element symbol, it is used directly.
    Otherwise, the mass is matched to the nearest element in the periodic table.

    Parameters
    ----------
    data_filepath : str or Path
        Path to the LAMMPS data file

    Returns
    -------
    list of str
        Ordered element symbols for ASE's ``specorder`` parameter.
        E.g. ['C', 'H', 'O', 'Si'] means type 1=C, type 2=H, type 3=O, type 4=Si.
    """
    data_filepath = Path(data_filepath)
    if not data_filepath.exists():
        raise FileNotFoundError(f"LAMMPS data file not found: {data_filepath}")

    masses_section = False
    type_to_symbol: Dict[int, str] = {}

    with open(data_filepath, 'r') as f:
        for line in f:
            stripped = line.strip()
            # Detect Masses section header
            if stripped == 'Masses':
                masses_section = True
                continue
            # End of Masses section: blank line after data, or another section
            if masses_section:
                if stripped == '':
                    if type_to_symbol:
                        break  # Finished reading masses
                    continue  # Skip blank line right after "Masses"
                # Check for next section header (e.g., "Atoms", "Bonds")
                if stripped.split()[0].isalpha() and not stripped[0].isdigit():
                    break

                # Parse: type_id  mass  [# comment]
                parts = line.split('#')
                data_part = parts[0].strip().split()
                if len(data_part) < 2:
                    continue
                try:
                    type_id = int(data_part[0])
                    mass = float(data_part[1])
                except (ValueError, IndexError):
                    continue

                # Try to get element from inline comment first
                symbol = None
                if len(parts) > 1:
                    comment = parts[1].strip()
                    # Match element symbol (1 or 2 letters, first uppercase)
                    match = re.match(r'^([A-Z][a-z]?)\b', comment)
                    if match:
                        candidate = match.group(1)
                        if candidate in atomic_numbers:
                            symbol = candidate

                # Fall back to mass matching
                if symbol is None:
                    best_z = 1
                    best_diff = abs(atomic_masses_iupac2016[1] - mass)
                    for z in range(1, len(atomic_masses_iupac2016)):
                        ref_mass = atomic_masses_iupac2016[z]
                        if np.isnan(ref_mass):
                            continue
                        diff = abs(ref_mass - mass)
                        if diff < best_diff:
                            best_diff = diff
                            best_z = z
                    symbol = chemical_symbols[best_z]

                type_to_symbol[type_id] = symbol

    if not type_to_symbol:
        raise ValueError(
            f"No Masses section found in {data_filepath}. "
            "Use --type-map to specify the mapping manually."
        )

    # Build ordered specorder list: type 1 → index 0, type 2 → index 1, ...
    max_type = max(type_to_symbol.keys())
    specorder = []
    for tid in range(1, max_type + 1):
        sym = type_to_symbol.get(tid, 'X')
        specorder.append(sym)

    # Print resolved mapping for user verification
    print(f"    Atom type mapping from {data_filepath.name}:")
    for tid in range(1, max_type + 1):
        sym = type_to_symbol.get(tid, 'X')
        print(f"      Type {tid} \u2192 {sym}")

    return specorder


class TrajectoryParser:
    """
    Unified parser for molecular dynamics trajectories.
    
    Uses ASE as backend to support multiple trajectory formats:
    - LAMMPS dump (.lammpstrj, .dump)
    - CP2K (.xyz, .dcd)
    - XYZ (.xyz)
    - Extended XYZ (.extxyz)
    - VASP (POSCAR, CONTCAR, XDATCAR)
    - And 80+ other formats supported by ASE
    
    Parameters
    ----------
    filepath : str or Path
        Path to trajectory file
    format : str, optional
        File format (auto-detected if not specified).
        See https://wiki.fysik.dtu.dk/ase/ase/io/io.html for options.
    element_to_type : dict, optional
        Mapping from element symbols to numeric atom types.
        Default: {'O': 1, 'H': 2, ...}
    
    Examples
    --------
    # Auto-detect format
    >>> parser = TrajectoryParser("trajectory.lammpstrj")
    >>> frames = parser.parse()
    
    # Specify format explicitly
    >>> parser = TrajectoryParser("pos.xyz", format="xyz")
    >>> frames = parser.parse()
    
    # Iterate without loading all frames
    >>> for frame in TrajectoryParser("large_traj.xyz"):
    ...     process(frame)
    """
    
    def __init__(
        self, 
        filepath: Union[str, Path], 
        format: Optional[str] = None,
        element_to_type: Optional[Dict[str, int]] = None,
        cell_filepath: Optional[Union[str, Path]] = None,
        atom_type_to_atomic_number: Optional[Dict[int, int]] = None,
        lammps_data_file: Optional[Union[str, Path]] = None,
        specorder: Optional[List[str]] = None
    ):
        """
        Initialize the TrajectoryParser.
        
        Parameters
        ----------
        filepath : str or Path
            Path to the trajectory file
        format : str, optional
            Format of the trajectory file (e.g., 'xyz', 'pdb').
            If None, ASE will attempt to guess.
        element_to_type : dict, optional
            Mapping from element symbols to numeric types.
            If None, defaults will be used.
        cell_filepath : str or Path, optional
            Path to separate CP2K cell file (.cell) containing box information.
        atom_type_to_atomic_number : dict, optional
            DEPRECATED. Use specorder or lammps_data_file instead.
            If provided, will be converted to specorder automatically.
        lammps_data_file : str or Path, optional
            Path to LAMMPS data file (.data, .lmpdat) to auto-extract
            the atom type→element mapping from the Masses section.
        specorder : list of str, optional
            Ordered element symbols for LAMMPS atom types.
            E.g. ['C', 'H', 'O', 'Si'] means type 1=C, 2=H, 3=O, 4=Si.
            This is passed directly to ASE's LAMMPS dump reader.
        """
        self.filepath = Path(filepath)
        self.format = format
        # ASE sometimes needs explicit format for LAMMPS dump files
        if self.format is None:
            if self.filepath.suffix in ['.lammpstrj', '.dump']:
                self.format = 'lammps-dump-text'
        
        self.element_to_type = element_to_type or DEFAULT_ELEMENT_TO_TYPE
        self.cell_filepath = Path(cell_filepath) if cell_filepath else None
        
        # Resolve specorder for LAMMPS dump files
        # Priority: specorder > lammps_data_file > atom_type_to_atomic_number
        if specorder is not None:
            self.specorder = specorder
        elif lammps_data_file is not None:
            self.specorder = parse_lammps_data_masses(Path(lammps_data_file))
        elif atom_type_to_atomic_number is not None:
            # Convert deprecated dict format to specorder list
            max_type = max(atom_type_to_atomic_number.keys())
            self.specorder = [
                chemical_symbols[atom_type_to_atomic_number.get(t, 0)]
                for t in range(1, max_type + 1)
            ]
        else:
            self.specorder = None
        
        self._frames: List[Frame] = []
        self._parsed = False

    def _parse_cp2k_cell_file(self) -> Optional[np.ndarray]:
        """
        Parse CP2K .cell file to extract box dimensions.
        
        Returns
        -------
        np.ndarray
            Array of shape (n_steps, 3) containing box lengths [Lx, Ly, Lz] for each step.
            Currently assumes orthorhombic boxes aligned with axes for simplicity in integration.
        """
        if not self.cell_filepath or not self.cell_filepath.exists():
            return None
            
        try:
            # Skip header line (starts with #)
            data = np.loadtxt(self.cell_filepath)
            
            # CP2K cell file columns:
            # Step Time Ax Ay Az Bx By Bz Cx Cy Cz Vol
            # 0    1    2  3  4  5  6  7  8  9  10 11
            
            # Extract diagonal elements for box lengths (Ax, By, Cz)
            # This assumes orthorhombic cell aligned with axes, which is standard for most CP2K AIMD
            # TODO: Support full triclinic cells if needed by upgrading Frame class
            box_lengths = data[:, [2, 6, 10]]
            
            return box_lengths
            
        except Exception as e:
            print(f"Warning: Failed to parse cell file {self.cell_filepath}: {e}")
            return None

    def parse(self) -> List[Frame]:
        """
        Parse the entire trajectory file.
        
        Returns
        -------
        List[Frame]
            List of Frame objects, one for each timestep
        """
        if self._parsed:
            return self._frames
        
        # Read frames lazily using iread generator to prevent massive memory overhead (OOM)
        # ase.io.read(..., index=':') loads all frames into heavy Atoms objects simultaneously.
        # list(self._parse_generator()) uses iread to parse one at a time and converts them to
        # lightweight numpy-backed Frame objects immediately, allowing Atoms to be GC'd.
        self._frames = list(self._parse_generator())
        self._parsed = True
        return self._frames
    
    def _parse_generator(self) -> Generator[Frame, None, None]:
        """Generator that yields frames one at a time (memory efficient)."""
        cell_data = self._parse_cp2k_cell_file()
        read_kwargs = {}
        if self.specorder and self.format == 'lammps-dump-text':
            read_kwargs['specorder'] = self.specorder
        for i, atoms in enumerate(iread(str(self.filepath), format=self.format, **read_kwargs)):
            timestep = atoms.info.get('timestep', atoms.info.get('time', i))
            frame = Frame.from_ase_atoms(atoms, timestep, self.element_to_type)
            
            # Override box information if cell data is available
            if cell_data is not None and i < len(cell_data):
                lengths = cell_data[i]
                frame.box_bounds = np.array([
                    [0.0, lengths[0]],
                    [0.0, lengths[1]],
                    [0.0, lengths[2]]
                ])
            
            yield frame
    
    def __len__(self) -> int:
        """Return number of frames in trajectory."""
        if not self._parsed:
            self.parse()
        return len(self._frames)
    
    def __getitem__(self, idx: int) -> Frame:
        """Get frame by index."""
        if not self._parsed:
            self.parse()
        return self._frames[idx]
    
    def __iter__(self):
        """Iterate over frames (uses generator for memory efficiency if not parsed)."""
        if self._parsed:
            return iter(self._frames)
        return self._parse_generator()
    
    def get_element_symbol(self, atom_type: int) -> str:
        """Get element symbol for numeric atom type (reverse lookup)."""
        type_to_element = {v: k for k, v in self.element_to_type.items()}
        return type_to_element.get(atom_type, 'X')
