"""
Implements Nature Protocols Steps 63-65 for characterizing interfacial water
at solid-liquid interfaces from AIMD trajectories.

Supports two surface detection modes:
  - Dynamic (default): Density-crossover-based Gibbs dividing surface tracking
    for soft-matter (polymer) interfaces.
  - Static: Fixed Z-coordinate cutoff for rigid surfaces (metals, crystals).

References
----------
- Wang, Y.-H., Li, S., et al., "In situ electrochemical Raman spectroscopy and ab initio molecular dynamics study of interfacial water on a single-crystal surface", Nature Protocols 18, 1421–1446 (2023). (Protocol Steps 63-65)
- Willard, A. P. & Chandler, D., "Instantaneous Liquid Interfaces", J. Phys. Chem. B 114, 1954–1958 (2010).
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Union
from pathlib import Path
import json

from ..io.trajectory_parser import Frame
from ..detection.hbond_detector import HBondDetector, WaterMolecule


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class InterfacialAnalysisResult:
    """
    Complete results from interfacial water analysis (Protocol Steps 63-65).

    Attributes
    ----------
    z_bins : np.ndarray
        Bin centres for the relative-Z density profile (Å).
    density_O : np.ndarray
        Water oxygen number-density profile (atoms/ų).
    density_H : np.ndarray
        Water hydrogen number-density profile (atoms/ų).
    density_substrate : np.ndarray
        Substrate (non-water) atom number-density profile (atoms/ų).
    interface_cutoff : float
        Final cutoff δ used to define the interfacial layer (Å).
    z_surf_timeseries : np.ndarray
        Z_GDS(t) or Z_static for each analysed frame.
    n_interfacial_water : np.ndarray
        Number of interfacial water molecules per frame.
    phi_bins : np.ndarray
        Bin centres for dipole-angle φ distribution (degrees).
    phi_distribution : np.ndarray
        Normalised probability P(φ).
    theta_bins : np.ndarray
        Bin centres for O-H bond angle θ distribution (degrees).
    theta_distribution : np.ndarray
        Normalised probability P(θ).
    hbonds_per_molecule : np.ndarray
        Mean H-bonds per interfacial water molecule per frame.
    hbonds_bulk_reference : float
        Mean H-bonds per bulk water molecule (for comparison).
    surface_mode : str
        Surface detection mode used: 'dynamic' or 'static'.
    """

    # Step 63
    z_bins: np.ndarray
    density_O: np.ndarray
    density_H: np.ndarray
    density_substrate: np.ndarray
    interface_cutoff: float
    z_surf_timeseries: np.ndarray
    n_interfacial_water: np.ndarray

    # Step 64
    phi_bins: np.ndarray
    phi_distribution: np.ndarray
    theta_bins: np.ndarray
    theta_distribution: np.ndarray

    # Step 65
    hbonds_per_molecule: np.ndarray
    hbonds_bulk_reference: float

    # Metadata
    surface_mode: str = "dynamic"

    def to_dict(self) -> Dict[str, Any]:
        """Serialise to a JSON-safe dictionary."""
        d: Dict[str, Any] = {}
        for k, v in self.__dict__.items():
            if isinstance(v, np.ndarray):
                d[k] = v.tolist()
            else:
                d[k] = v
        return d

    def to_json(self, filepath: Union[str, Path]) -> None:
        """Save results to a JSON file."""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_json(cls, filepath: Union[str, Path]) -> "InterfacialAnalysisResult":
        """Load results from a JSON file."""
        with open(filepath, "r") as f:
            data = json.load(f)
        # Convert lists back to numpy arrays
        array_fields = [
            "z_bins", "density_O", "density_H", "density_substrate",
            "z_surf_timeseries", "n_interfacial_water",
            "phi_bins", "phi_distribution", "theta_bins", "theta_distribution",
            "hbonds_per_molecule",
        ]
        for k in array_fields:
            if k in data and isinstance(data[k], list):
                data[k] = np.array(data[k])
        return cls(**data)


# ---------------------------------------------------------------------------
# Core analyser
# ---------------------------------------------------------------------------

class InterfacialAnalyzer:
    """
    Dynamic interfacial water analyser for solid-liquid interfaces.

    Supports two surface-detection modes:

    **Dynamic mode** (default, for soft matter / polymer surfaces):
      Computes per-frame density profiles of substrate vs. water along the
      interface normal, and locates the Gibbs dividing surface (GDS) at the
      density crossover point.

    **Static mode** (for rigid metal / crystal surfaces):
      Uses a fixed Z coordinate as the surface reference.  The user must
      supply ``static_z_surface``.

    Parameters
    ----------
    mode : str
        ``'dynamic'`` or ``'static'``.  Default: ``'dynamic'``.
    interface_cutoff : float or None
        Distance (Å) from the surface defining the interfacial layer.
        If *None*, auto-detected from the first valley of the O-density
        profile.  Default: ``None``.
    z_axis : int
        Cartesian axis perpendicular to the interface (0=x, 1=y, 2=z).
        Default: ``2``.
    n_bins : int
        Number of bins for density histograms.  Default: ``200``.
    density_sigma : float
        Gaussian smoothing σ (Å) applied to density profiles.
        Default: ``0.5``.
    static_z_surface : float or None
        Fixed Z coordinate of the surface (Å).  Required when
        ``mode='static'``.  Default: ``None``.
    r_oh_max : float
        Maximum O-H bond length for water identification (Å).
        Default: ``1.2``.
    r_oo_hbond : float
        Maximum O···O distance for H-bond detection (Å).
        Default: ``3.5``.
    angle_ooh_hbond : float
        Maximum O···O-H angle for H-bond detection (degrees).
        Default: ``35.0``.
    verbose : bool
        Print progress messages.  Default: ``True``.
    """

    def __init__(
        self,
        mode: str = "dynamic",
        interface_cutoff: Optional[float] = None,
        z_axis: int = 2,
        n_bins: int = 200,
        density_sigma: float = 0.5,
        static_z_surface: Optional[float] = None,
        r_oh_max: float = 1.2,
        r_oo_hbond: float = 3.5,
        angle_ooh_hbond: float = 35.0,
        verbose: bool = True,
    ):
        if mode not in ("dynamic", "static"):
            raise ValueError(f"mode must be 'dynamic' or 'static', got '{mode}'")
        if mode == "static" and static_z_surface is None:
            raise ValueError("static_z_surface is required when mode='static'")

        self.mode = mode
        self.interface_cutoff = interface_cutoff
        self.z_axis = z_axis
        self.n_bins = n_bins
        self.density_sigma = density_sigma
        self.static_z_surface = static_z_surface
        self.r_oh_max = r_oh_max
        self.r_oo_hbond = r_oo_hbond
        self.angle_ooh_hbond = angle_ooh_hbond
        self.verbose = verbose

        # Internal H-bond detector (reuse existing logic for water ID)
        self._detector = HBondDetector(r_oh_max=r_oh_max)

    # ------------------------------------------------------------------
    # Water / substrate partitioning
    # ------------------------------------------------------------------

    def _partition_atoms(
        self, frame: Frame
    ) -> Tuple[List[WaterMolecule], np.ndarray, np.ndarray]:
        """
        Partition atoms into water molecules and substrate atoms.

        Returns
        -------
        water_molecules : list of WaterMolecule
        water_all_indices : np.ndarray
            Flat array of all atom indices belonging to water.
        substrate_indices : np.ndarray
            Atom indices not belonging to any water molecule.
        """
        water_mols = self._detector.identify_water_molecules(frame)

        water_idx_set: set = set()
        for wm in water_mols:
            water_idx_set.update([wm.o_idx, wm.h1_idx, wm.h2_idx])

        all_indices = np.arange(frame.n_atoms)
        substrate_mask = np.ones(frame.n_atoms, dtype=bool)
        for idx in water_idx_set:
            substrate_mask[idx] = False

        return water_mols, np.array(sorted(water_idx_set)), all_indices[substrate_mask]

    # ------------------------------------------------------------------
    # Surface position
    # ------------------------------------------------------------------

    def compute_surface_position(self, frame: Frame) -> float:
        """
        Compute the instantaneous surface Z coordinate for one frame.

        In **dynamic** mode, returns the density-crossover Gibbs dividing
        surface.  In **static** mode, returns the fixed user value.

        Parameters
        ----------
        frame : Frame

        Returns
        -------
        float
            Z_GDS(t) or Z_static.
        """
        if self.mode == "static":
            return float(self.static_z_surface)  # type: ignore[arg-type]

        # --- Dynamic mode: density crossover ---
        water_mols, _, substrate_indices = self._partition_atoms(frame)
        z = self.z_axis
        box_lo = frame.box_bounds[z, 0]
        box_hi = frame.box_bounds[z, 1]

        # Z coordinates
        sub_z = frame.positions[substrate_indices, z] if len(substrate_indices) > 0 else np.array([])
        wat_o_z = np.array([wm.o_position[z] for wm in water_mols]) if water_mols else np.array([])

        if len(sub_z) == 0 or len(wat_o_z) == 0:
            # Fallback: midpoint of box
            return (box_lo + box_hi) / 2.0

        bins = np.linspace(box_lo, box_hi, self.n_bins + 1)
        bin_centres = 0.5 * (bins[:-1] + bins[1:])

        hist_sub, _ = np.histogram(sub_z, bins=bins)
        hist_wat, _ = np.histogram(wat_o_z, bins=bins)

        # Smooth
        if self.density_sigma > 0:
            hist_sub = self._gaussian_smooth(hist_sub.astype(float), bins, self.density_sigma)
            hist_wat = self._gaussian_smooth(hist_wat.astype(float), bins, self.density_sigma)

        # Find crossover: where |hist_sub - hist_wat| is minimised in
        # a region where both are non-negligible
        threshold = 0.05 * max(hist_sub.max(), hist_wat.max(), 1e-30)
        valid = (hist_sub > threshold) | (hist_wat > threshold)
        if not np.any(valid):
            return (box_lo + box_hi) / 2.0

        diff = np.abs(hist_sub - hist_wat)
        diff[~valid] = np.inf

        # Among potentially multiple crossovers, pick the one closest to the
        # transition from substrate-dominated to water-dominated region
        idx_cross = int(np.argmin(diff))
        return float(bin_centres[idx_cross])

    # ------------------------------------------------------------------
    # Density profile
    # ------------------------------------------------------------------

    def compute_density_profile(
        self, frames: List[Frame]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, float]:
        """
        Compute the averaged density profiles in relative coordinates.

        Parameters
        ----------
        frames : list of Frame

        Returns
        -------
        z_bins : np.ndarray  — bin centres (Å, relative to surface)
        density_O : np.ndarray
        density_H : np.ndarray
        density_sub : np.ndarray
        auto_cutoff : float  — auto-detected interfacial cutoff (Å)
        """
        # Use a generous range for relative Z
        z_range = (-15.0, 30.0)
        bins = np.linspace(z_range[0], z_range[1], self.n_bins + 1)
        bin_centres = 0.5 * (bins[:-1] + bins[1:])
        dz = bins[1] - bins[0]

        acc_O = np.zeros(self.n_bins, dtype=float)
        acc_H = np.zeros(self.n_bins, dtype=float)
        acc_sub = np.zeros(self.n_bins, dtype=float)

        z = self.z_axis
        n_frames = len(frames)

        for i, frame in enumerate(frames):
            if self.verbose and (i % max(1, n_frames // 10) == 0):
                print(f"  Density profile: frame {i + 1}/{n_frames}")

            z_surf = self.compute_surface_position(frame)
            water_mols, water_indices, substrate_indices = self._partition_atoms(frame)

            # Substrate
            if len(substrate_indices) > 0:
                dz_sub = frame.positions[substrate_indices, z] - z_surf
                h, _ = np.histogram(dz_sub, bins=bins)
                acc_sub += h.astype(float)

            # Water O and H
            for wm in water_mols:
                dz_o = wm.o_position[z] - z_surf
                h, _ = np.histogram([dz_o], bins=bins)
                acc_O += h.astype(float)

                dz_h1 = wm.h1_position[z] - z_surf
                dz_h2 = wm.h2_position[z] - z_surf
                h, _ = np.histogram([dz_h1, dz_h2], bins=bins)
                acc_H += h.astype(float)

        # Normalise: average over frames, convert to number density
        A_xy = frames[0].box_lengths[0] * frames[0].box_lengths[1]  # cross-sectional area
        vol_bin = A_xy * dz  # volume of each bin slab

        density_O = acc_O / (n_frames * vol_bin) if vol_bin > 0 else acc_O
        density_H = acc_H / (n_frames * vol_bin) if vol_bin > 0 else acc_H
        density_sub = acc_sub / (n_frames * vol_bin) if vol_bin > 0 else acc_sub

        # Auto-detect interfacial cutoff from O-density first valley
        auto_cutoff = self._detect_cutoff_from_density(bin_centres, density_O)

        return bin_centres, density_O, density_H, density_sub, auto_cutoff

    def _detect_cutoff_from_density(
        self, z_bins: np.ndarray, density_O: np.ndarray
    ) -> float:
        """
        Find the first valley in the O-density profile for ΔZ > 0.

        Falls back to 4.0 Å if no clear valley is found.
        """
        # Focus on the water side (ΔZ > 0)
        mask = z_bins > 0.5  # skip the immediate crossover region
        if not np.any(mask):
            return 4.0

        z_pos = z_bins[mask]
        rho = density_O[mask]

        if len(rho) < 5:
            return 4.0

        # Smooth for peak/valley detection
        from scipy.ndimage import gaussian_filter1d
        rho_smooth = gaussian_filter1d(rho, sigma=2.0)

        # Find first peak
        peak_idx = None
        for j in range(1, len(rho_smooth) - 1):
            if rho_smooth[j] > rho_smooth[j - 1] and rho_smooth[j] > rho_smooth[j + 1]:
                if rho_smooth[j] > 0.1 * rho_smooth.max():
                    peak_idx = j
                    break

        if peak_idx is None:
            return 4.0

        # Find first valley after peak
        for j in range(peak_idx + 1, len(rho_smooth) - 1):
            if rho_smooth[j] < rho_smooth[j - 1] and rho_smooth[j] < rho_smooth[j + 1]:
                return float(z_pos[j])

        return 4.0

    # ------------------------------------------------------------------
    # Classify interfacial water
    # ------------------------------------------------------------------

    def classify_interfacial_water(
        self, frame: Frame, cutoff: float
    ) -> Tuple[List[WaterMolecule], List[WaterMolecule]]:
        """
        Classify water molecules into interfacial and bulk.

        Parameters
        ----------
        frame : Frame
        cutoff : float
            Interface cutoff δ (Å).

        Returns
        -------
        interfacial : list of WaterMolecule
        bulk : list of WaterMolecule
        """
        z = self.z_axis
        z_surf = self.compute_surface_position(frame)
        water_mols, _, _ = self._partition_atoms(frame)

        interfacial: List[WaterMolecule] = []
        bulk: List[WaterMolecule] = []

        for wm in water_mols:
            dz = wm.o_position[z] - z_surf
            if 0 < dz < cutoff:
                interfacial.append(wm)
            else:
                bulk.append(wm)

        return interfacial, bulk

    # ------------------------------------------------------------------
    # Angle distributions
    # ------------------------------------------------------------------

    def compute_angle_distributions(
        self, frames: List[Frame], cutoff: float, n_angle_bins: int = 90
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute dipole angle φ and O-H bond angle θ distributions for
        interfacial water.

        φ = angle between surface normal (z-axis) and the water dipole
            bisector vector.
        θ = angle between surface normal and each O-H bond direction.

        Parameters
        ----------
        frames : list of Frame
        cutoff : float
        n_angle_bins : int

        Returns
        -------
        phi_bins, phi_dist, theta_bins, theta_dist
        """
        phi_edges = np.linspace(0, 180, n_angle_bins + 1)
        theta_edges = np.linspace(0, 180, n_angle_bins + 1)
        phi_centres = 0.5 * (phi_edges[:-1] + phi_edges[1:])
        theta_centres = 0.5 * (theta_edges[:-1] + theta_edges[1:])

        phi_counts = np.zeros(n_angle_bins, dtype=float)
        theta_counts = np.zeros(n_angle_bins, dtype=float)

        z_hat = np.zeros(3)
        z_hat[self.z_axis] = 1.0  # surface normal

        n_frames = len(frames)
        for i, frame in enumerate(frames):
            if self.verbose and (i % max(1, n_frames // 10) == 0):
                print(f"  Angle distributions: frame {i + 1}/{n_frames}")

            interfacial, _ = self.classify_interfacial_water(frame, cutoff)
            box_lengths = frame.box_lengths

            for wm in interfacial:
                # Minimum-image vectors from O to H
                oh1 = wm.h1_position - wm.o_position
                oh1 -= box_lengths * np.round(oh1 / box_lengths)
                oh2 = wm.h2_position - wm.o_position
                oh2 -= box_lengths * np.round(oh2 / box_lengths)

                # Dipole bisector (points from O towards the midpoint of H1-H2)
                bisector = oh1 + oh2
                bisector_norm = np.linalg.norm(bisector)
                if bisector_norm < 1e-10:
                    continue
                bisector /= bisector_norm

                # φ: angle between bisector and surface normal
                cos_phi = np.clip(np.dot(bisector, z_hat), -1.0, 1.0)
                phi_deg = np.degrees(np.arccos(cos_phi))
                idx_phi = np.searchsorted(phi_edges, phi_deg, side="right") - 1
                idx_phi = min(idx_phi, n_angle_bins - 1)
                if 0 <= idx_phi < n_angle_bins:
                    phi_counts[idx_phi] += 1

                # θ: angle between each O-H bond and surface normal
                for oh in [oh1, oh2]:
                    oh_len = np.linalg.norm(oh)
                    if oh_len < 1e-10:
                        continue
                    cos_theta = np.clip(np.dot(oh / oh_len, z_hat), -1.0, 1.0)
                    theta_deg = np.degrees(np.arccos(cos_theta))
                    idx_theta = np.searchsorted(theta_edges, theta_deg, side="right") - 1
                    idx_theta = min(idx_theta, n_angle_bins - 1)
                    if 0 <= idx_theta < n_angle_bins:
                        theta_counts[idx_theta] += 1

        # Normalise to probability density (integrate to 1)
        dphi = phi_edges[1] - phi_edges[0]
        dtheta = theta_edges[1] - theta_edges[0]
        phi_sum = phi_counts.sum() * dphi
        theta_sum = theta_counts.sum() * dtheta
        phi_dist = phi_counts / phi_sum if phi_sum > 0 else phi_counts
        theta_dist = theta_counts / theta_sum if theta_sum > 0 else theta_counts

        return phi_centres, phi_dist, theta_centres, theta_dist

    # ------------------------------------------------------------------
    # H-bond statistics
    # ------------------------------------------------------------------

    def compute_hbond_statistics(
        self, frames: List[Frame], cutoff: float
    ) -> Tuple[np.ndarray, float]:
        """
        Compute per-frame mean H-bond count for interfacial water,
        and a bulk reference value.

        H-bond criterion: O···O < r_oo_hbond AND O···O-H angle < angle_ooh_hbond.

        Parameters
        ----------
        frames : list of Frame
        cutoff : float

        Returns
        -------
        hbonds_per_mol : np.ndarray
            Mean H-bonds per interfacial water molecule for each frame.
        bulk_ref : float
            Mean H-bonds per bulk water molecule (averaged over all frames).
        """
        hbonds_per_mol = []
        bulk_hbonds_list = []

        n_frames = len(frames)
        for i, frame in enumerate(frames):
            if self.verbose and (i % max(1, n_frames // 10) == 0):
                print(f"  H-bond statistics: frame {i + 1}/{n_frames}")

            interfacial, bulk = self.classify_interfacial_water(frame, cutoff)
            all_water = interfacial + bulk
            box_lengths = frame.box_lengths

            # Build a set of O indices for quick lookup
            interface_o_set = {wm.o_idx for wm in interfacial}
            bulk_o_set = {wm.o_idx for wm in bulk}

            # Count H-bonds for each water molecule among ALL water
            hb_count_interface: Dict[int, int] = {wm.o_idx: 0 for wm in interfacial}
            hb_count_bulk: Dict[int, int] = {wm.o_idx: 0 for wm in bulk}

            for donor in all_water:
                for acceptor in all_water:
                    if donor.o_idx == acceptor.o_idx:
                        continue

                    # O···O distance
                    delta = acceptor.o_position - donor.o_position
                    delta -= box_lengths * np.round(delta / box_lengths)
                    r_oo = np.linalg.norm(delta)
                    if r_oo > self.r_oo_hbond:
                        continue

                    # Check each H of donor
                    for h_pos in [donor.h1_position, donor.h2_position]:
                        oh = h_pos - donor.o_position
                        oh -= box_lengths * np.round(oh / box_lengths)
                        oa = acceptor.o_position - donor.o_position
                        oa -= box_lengths * np.round(oa / box_lengths)

                        # O···O-H angle
                        cos_angle = np.dot(oh, oa) / (np.linalg.norm(oh) * np.linalg.norm(oa) + 1e-30)
                        cos_angle = np.clip(cos_angle, -1.0, 1.0)
                        angle_deg = np.degrees(np.arccos(cos_angle))

                        if angle_deg < self.angle_ooh_hbond:
                            if donor.o_idx in hb_count_interface:
                                hb_count_interface[donor.o_idx] += 1
                            if donor.o_idx in hb_count_bulk:
                                hb_count_bulk[donor.o_idx] += 1
                            break  # count only one H-bond per donor-acceptor pair

            # Mean H-bonds per interfacial water
            if len(hb_count_interface) > 0:
                mean_hb = np.mean(list(hb_count_interface.values()))
            else:
                mean_hb = 0.0
            hbonds_per_mol.append(mean_hb)

            # Bulk reference
            if len(hb_count_bulk) > 0:
                bulk_hbonds_list.append(np.mean(list(hb_count_bulk.values())))

        bulk_ref = float(np.mean(bulk_hbonds_list)) if bulk_hbonds_list else 3.5

        return np.array(hbonds_per_mol), bulk_ref

    # ------------------------------------------------------------------
    # Full analysis pipeline
    # ------------------------------------------------------------------

    def run_full_analysis(
        self,
        frames: List[Frame],
        start: int = 0,
        stop: Optional[int] = None,
        step: int = 1,
    ) -> InterfacialAnalysisResult:
        """
        Run the complete analysis.

        Parameters
        ----------
        frames : list of Frame
        start, stop, step : int
            Frame range selection.

        Returns
        -------
        InterfacialAnalysisResult
        """
        selected = frames[start:stop:step]
        n = len(selected)
        if self.verbose:
            print(f"InterfacialAnalyzer: analysing {n} frames (mode={self.mode})")

        # --- Density profile ---
        if self.verbose:
            print("\nComputing density profiles...")
        z_bins, density_O, density_H, density_sub, auto_cutoff = (
            self.compute_density_profile(selected)
        )

        cutoff = self.interface_cutoff if self.interface_cutoff is not None else auto_cutoff
        if self.verbose:
            print(f"  Interface cutoff: {cutoff:.2f} Å "
                  f"({'user-specified' if self.interface_cutoff else 'auto-detected'})")

        # Surface position time series
        z_surf_ts = np.array([self.compute_surface_position(f) for f in selected])

        # Interfacial water count per frame
        n_iw = np.array([
            len(self.classify_interfacial_water(f, cutoff)[0]) for f in selected
        ])

        # --- Angle distributions ---
        if self.verbose:
            print("\nComputing angle distributions...")
        phi_bins, phi_dist, theta_bins, theta_dist = (
            self.compute_angle_distributions(selected, cutoff)
        )

        # --- H-bond statistics ---
        if self.verbose:
            print("\nComputing H-bond statistics...")
        hbonds_per_mol, bulk_ref = self.compute_hbond_statistics(selected, cutoff)

        if self.verbose:
            print(f"\n  Mean interfacial H-bonds/molecule: "
                  f"{np.mean(hbonds_per_mol):.2f}")
            print(f"  Bulk reference H-bonds/molecule:   {bulk_ref:.2f}")
            print("  Analysis complete.")

        return InterfacialAnalysisResult(
            z_bins=z_bins,
            density_O=density_O,
            density_H=density_H,
            density_substrate=density_sub,
            interface_cutoff=cutoff,
            z_surf_timeseries=z_surf_ts,
            n_interfacial_water=n_iw,
            phi_bins=phi_bins,
            phi_distribution=phi_dist,
            theta_bins=theta_bins,
            theta_distribution=theta_dist,
            hbonds_per_molecule=hbonds_per_mol,
            hbonds_bulk_reference=bulk_ref,
            surface_mode=self.mode,
        )

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _gaussian_smooth(
        data: np.ndarray, bins: np.ndarray, sigma: float
    ) -> np.ndarray:
        """Apply Gaussian smoothing to a histogram."""
        try:
            from scipy.ndimage import gaussian_filter1d
            dz = bins[1] - bins[0]
            sigma_bins = sigma / dz
            return gaussian_filter1d(data, sigma=sigma_bins)
        except ImportError:
            # Fallback: simple moving average
            w = max(1, int(sigma / (bins[1] - bins[0])))
            kernel = np.ones(2 * w + 1) / (2 * w + 1)
            return np.convolve(data, kernel, mode="same")


# ---------------------------------------------------------------------------
# Visualiser
# ---------------------------------------------------------------------------

class InterfacialVisualizer:
    """
    Publication-quality plots for interfacial water analysis results.
    """

    def __init__(self, dpi: int = 150, figsize: Tuple[float, float] = (8, 5)):
        self.dpi = dpi
        self.figsize = figsize

    def plot_all(
        self,
        result: InterfacialAnalysisResult,
        save_dir: Union[str, Path] = "interfacial_analysis_results",
        timestep_fs: float = 0.5,
    ) -> None:
        """Generate all four figures and save to *save_dir*."""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)

        self.plot_density_profile(result, save_dir / "density_profile.png")
        self.plot_angle_distributions(result, save_dir / "angle_distributions.png")
        self.plot_hbond_evolution(result, save_dir / "hbond_evolution.png", timestep_fs)
        self.plot_surface_fluctuation(result, save_dir / "surface_fluctuation.png", timestep_fs)

        print(f"All figures saved to {save_dir}/")

        # Save raw data to CSV files
        self.save_csvs(result, save_dir, timestep_fs)

    def save_csvs(
        self,
        result: InterfacialAnalysisResult,
        save_dir: Union[str, Path],
        timestep_fs: float = 0.5,
    ) -> None:
        """Save the raw data of each plot as separate CSV files in *save_dir*."""
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        import csv

        # 1. density_profile.csv
        density_path = save_dir / "density_profile.csv"
        with open(density_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Delta_Z_A", "Density_Substrate_atoms_per_A3", "Density_O_atoms_per_A3", "Density_H_atoms_per_A3"])
            for z, sub, o, h in zip(result.z_bins, result.density_substrate, result.density_O, result.density_H):
                writer.writerow([z, sub, o, h])

        # 2. angle_distributions.csv
        angle_path = save_dir / "angle_distributions.csv"
        with open(angle_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Angle_deg", "Phi_probability_density", "Theta_probability_density"])
            for phi_val, phi_prob, theta_prob in zip(result.phi_bins, result.phi_distribution, result.theta_distribution):
                writer.writerow([phi_val, phi_prob, theta_prob])

        # 3. hbond_evolution.csv
        hbond_path = save_dir / "hbond_evolution.csv"
        n_frames_hb = len(result.hbonds_per_molecule)
        time_ps_hb = np.arange(n_frames_hb) * timestep_fs / 1000.0
        with open(hbond_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Time_ps", "HBonds_per_interfacial_water", "N_interfacial_water"])
            for t, hb, n_w in zip(time_ps_hb, result.hbonds_per_molecule, result.n_interfacial_water):
                writer.writerow([t, hb, n_w])

        # 4. surface_fluctuation.csv
        fluct_path = save_dir / "surface_fluctuation.csv"
        n_frames_fl = len(result.z_surf_timeseries)
        time_ps_fl = np.arange(n_frames_fl) * timestep_fs / 1000.0
        with open(fluct_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Time_ps", "Z_surface_A"])
            for t, z in zip(time_ps_fl, result.z_surf_timeseries):
                writer.writerow([t, z])

        print(f"All raw data CSVs saved to {save_dir}/")

    def plot_density_profile(
        self, result: InterfacialAnalysisResult, filepath: Union[str, Path]
    ) -> None:
        """Density profiles of substrate, O, H vs ΔZ."""
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        ax.plot(result.z_bins, result.density_substrate, "grey", lw=1.5, label="Substrate")
        ax.plot(result.z_bins, result.density_O, "r", lw=2, label="Water O")
        ax.plot(result.z_bins, result.density_H, "b", lw=1.2, alpha=0.7, label="Water H")

        # Shade interfacial region
        ax.axvspan(0, result.interface_cutoff, alpha=0.12, color="gold",
                   label=f"Interface (δ={result.interface_cutoff:.1f} Å)")
        ax.axvline(0, color="k", ls="--", lw=0.8, label="GDS")

        ax.set_xlabel("ΔZ relative to surface (Å)", fontsize=12)
        ax.set_ylabel("Number density (atoms/ų)", fontsize=12)
        ax.set_title("Interfacial Density Profile", fontsize=13)
        ax.legend(fontsize=9)
        ax.set_xlim(-5, 15)
        fig.tight_layout()
        fig.savefig(filepath)
        plt.close(fig)

    def plot_angle_distributions(
        self, result: InterfacialAnalysisResult, filepath: Union[str, Path]
    ) -> None:
        """Side-by-side φ and θ distributions."""
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=self.dpi)

        ax1.bar(result.phi_bins, result.phi_distribution,
                width=result.phi_bins[1] - result.phi_bins[0],
                color="steelblue", alpha=0.8, edgecolor="navy", linewidth=0.3)
        ax1.set_xlabel("φ (dipole bisector angle, °)", fontsize=12)
        ax1.set_ylabel("Probability density", fontsize=12)
        ax1.set_title("Dipole Orientation", fontsize=13)
        ax1.set_xlim(0, 180)

        ax2.bar(result.theta_bins, result.theta_distribution,
                width=result.theta_bins[1] - result.theta_bins[0],
                color="coral", alpha=0.8, edgecolor="darkred", linewidth=0.3)
        ax2.set_xlabel("θ (O-H bond angle, °)", fontsize=12)
        ax2.set_ylabel("Probability density", fontsize=12)
        ax2.set_title("O-H Bond Orientation", fontsize=13)
        ax2.set_xlim(0, 180)

        fig.tight_layout()
        fig.savefig(filepath)
        plt.close(fig)

    def plot_hbond_evolution(
        self,
        result: InterfacialAnalysisResult,
        filepath: Union[str, Path],
        timestep_fs: float = 0.5,
    ) -> None:
        """H-bond count and interfacial water count vs time."""
        import matplotlib.pyplot as plt

        n = len(result.hbonds_per_molecule)
        time_ps = np.arange(n) * timestep_fs / 1000.0

        fig, ax1 = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        color1 = "tab:blue"
        ax1.plot(time_ps, result.hbonds_per_molecule, color=color1, lw=1.2)
        ax1.axhline(result.hbonds_bulk_reference, color=color1, ls="--", lw=0.8,
                     alpha=0.6, label=f"Bulk ref = {result.hbonds_bulk_reference:.2f}")
        ax1.set_xlabel("Time (ps)", fontsize=12)
        ax1.set_ylabel("H-bonds / interfacial water molecule", fontsize=12, color=color1)
        ax1.tick_params(axis="y", labelcolor=color1)
        ax1.legend(loc="upper left", fontsize=9)

        ax2 = ax1.twinx()
        color2 = "tab:orange"
        ax2.plot(time_ps, result.n_interfacial_water, color=color2, lw=1.0, alpha=0.7)
        ax2.set_ylabel("N interfacial water", fontsize=12, color=color2)
        ax2.tick_params(axis="y", labelcolor=color2)

        ax1.set_title("H-bond Evolution at Interface", fontsize=13)
        fig.tight_layout()
        fig.savefig(filepath)
        plt.close(fig)

    def plot_surface_fluctuation(
        self,
        result: InterfacialAnalysisResult,
        filepath: Union[str, Path],
        timestep_fs: float = 0.5,
    ) -> None:
        """Z_GDS(t) time series and fluctuation histogram."""
        import matplotlib.pyplot as plt

        n = len(result.z_surf_timeseries)
        time_ps = np.arange(n) * timestep_fs / 1000.0

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=self.dpi,
                                        gridspec_kw={"width_ratios": [3, 1]})

        ax1.plot(time_ps, result.z_surf_timeseries, "k", lw=0.8)
        mean_z = result.z_surf_timeseries.mean()
        std_z = result.z_surf_timeseries.std()
        ax1.axhline(mean_z, color="r", ls="--", lw=0.8,
                     label=f"Mean = {mean_z:.2f} Å")
        ax1.fill_between(time_ps, mean_z - std_z, mean_z + std_z,
                          alpha=0.15, color="red", label=f"±σ = {std_z:.2f} Å")
        ax1.set_xlabel("Time (ps)", fontsize=12)
        ax1.set_ylabel(f"Z_surface (Å) [{result.surface_mode} mode]", fontsize=12)
        ax1.set_title("Surface Position Fluctuation", fontsize=13)
        ax1.legend(fontsize=9)

        ax2.hist(result.z_surf_timeseries, bins=30, orientation="horizontal",
                 color="steelblue", alpha=0.7, edgecolor="navy", linewidth=0.5)
        ax2.set_xlabel("Count", fontsize=12)
        ax2.set_ylim(ax1.get_ylim())
        ax2.set_yticklabels([])

        fig.tight_layout()
        fig.savefig(filepath)
        plt.close(fig)
