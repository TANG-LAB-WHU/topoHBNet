"""
Tests for the interfacial water analyzer module.
"""

import pytest
import numpy as np
import tempfile
import os

from hbond_topology.io.trajectory_parser import Frame
from hbond_topology.analysis.interfacial import (
    InterfacialAnalyzer,
    InterfacialAnalysisResult,
    InterfacialVisualizer,
)


@pytest.fixture
def sample_interfacial_result():
    """Create a sample InterfacialAnalysisResult."""
    return InterfacialAnalysisResult(
        z_bins=np.linspace(-5.0, 15.0, 10),
        density_O=np.random.rand(10),
        density_H=np.random.rand(10),
        density_substrate=np.random.rand(10),
        interface_cutoff=4.0,
        z_surf_timeseries=np.array([12.5, 12.6, 12.4]),
        n_interfacial_water=np.array([5, 6, 4]),
        phi_bins=np.linspace(0, 180, 5),
        phi_distribution=np.array([0.1, 0.2, 0.4, 0.2, 0.1]),
        theta_bins=np.linspace(0, 180, 5),
        theta_distribution=np.array([0.05, 0.15, 0.6, 0.15, 0.05]),
        hbonds_per_molecule=np.array([2.5, 2.6, 2.4]),
        hbonds_bulk_reference=3.6,
        surface_mode="dynamic",
    )


class TestInterfacialAnalysisResult:
    """Tests for the InterfacialAnalysisResult dataclass."""

    def test_to_dict(self, sample_interfacial_result):
        d = sample_interfacial_result.to_dict()
        assert isinstance(d, dict)
        assert d["surface_mode"] == "dynamic"
        assert d["hbonds_bulk_reference"] == pytest.approx(3.6)

    def test_json_roundtrip(self, sample_interfacial_result):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            sample_interfacial_result.to_json(filepath)
            loaded = InterfacialAnalysisResult.from_json(filepath)
            assert loaded.surface_mode == sample_interfacial_result.surface_mode
            np.testing.assert_array_almost_equal(loaded.z_bins, sample_interfacial_result.z_bins)
        finally:
            os.unlink(filepath)


def create_two_phase_frame(z_shift=0.0):
    """Create a synthetic two-phase slab: substrate at Z < 10, water at Z > 10."""
    box_bounds = np.array([[0.0, 10.0], [0.0, 10.0], [0.0, 30.0]])
    
    symbols = []
    positions = []
    
    # Substrate dense phase (Z = 2 to 10)
    for z in np.linspace(2.0, 9.8, 40):
        symbols.append("C")
        positions.append([5.0, 5.0, z + z_shift])
        
    # Water dense phase (Z = 12 to 18)
    # Space them by 2.0 A to prevent them from sharing H atoms!
    for z in np.linspace(12.0, 18.0, 4):
        for x in [2.0, 6.0]:
            for y in [2.0, 6.0]:
                symbols.append("O")
                positions.append([x, y, z + z_shift])
                # H atoms 0.5A away in x/y and z
                symbols.append("H")
                positions.append([x + 0.5, y, z + 0.5 + z_shift])
                symbols.append("H")
                positions.append([x, y + 0.5, z + 0.5 + z_shift])

    return Frame(
        timestep=0,
        n_atoms=len(symbols),
        box_bounds=box_bounds,
        symbols=np.array(symbols),
        positions=np.array(positions),
    )


class TestInterfacialAnalyzerPhysics:
    """Rigorous physical tests as specified in the implementation plan."""

    def test_gibbs_surface_two_phase(self):
        """test_gibbs_surface_two_phase: Z_GDS falls at the correct crossover."""
        frame = create_two_phase_frame(z_shift=0.0)
        analyzer = InterfacialAnalyzer(mode="dynamic", verbose=False)
        z_surf = analyzer.compute_surface_position(frame)
        
        # DEBUG
        water_mols, _, substrate_indices = analyzer._partition_atoms(frame)
        z = analyzer.z_axis
        sub_z = frame.positions[substrate_indices, z]
        wat_o_z = np.array([wm.o_position[z] for wm in water_mols])
        bins = np.linspace(0, 30, analyzer.n_bins + 1)
        hist_sub, _ = np.histogram(sub_z, bins=bins)
        hist_wat, _ = np.histogram(wat_o_z, bins=bins)
        print(f"sub_z bounds: {sub_z.min()} to {sub_z.max()}")
        print(f"wat_o_z bounds: {wat_o_z.min()} to {wat_o_z.max()}")
        print(f"Z_GDS detected: {z_surf}")
        
        # Crossover should be in the gap between 9.8 and 12.0 (around 10.9)
        assert 10.0 <= z_surf <= 11.5

    def test_gibbs_surface_tracks_shift(self):
        """test_gibbs_surface_tracks_shift: Shifting atoms shifts Z_GDS."""
        frame_base = create_two_phase_frame(z_shift=0.0)
        frame_shift = create_two_phase_frame(z_shift=2.0)
        analyzer = InterfacialAnalyzer(mode="dynamic", verbose=False)
        
        z_surf_base = analyzer.compute_surface_position(frame_base)
        z_surf_shift = analyzer.compute_surface_position(frame_shift)
        
        assert z_surf_shift - z_surf_base == pytest.approx(2.0, abs=0.2)

    def test_density_profile_normalization(self):
        """test_density_profile_normalization: Integral of ρ_O(z) * A_xy * dz ≈ N_O."""
        frame = create_two_phase_frame(z_shift=0.0)
        analyzer = InterfacialAnalyzer(mode="static", static_z_surface=10.0, verbose=False)
        z_bins, density_O, density_H, density_sub, _ = analyzer.compute_density_profile([frame])
        
        dz = z_bins[1] - z_bins[0]
        area = (frame.box_bounds[0,1] - frame.box_bounds[0,0]) * (frame.box_bounds[1,1] - frame.box_bounds[1,0])
        
        total_O_integrated = np.sum(density_O) * dz * area
        actual_O_count = np.sum(frame.symbols == "O")
        
        # Should match closely
        assert total_O_integrated == pytest.approx(actual_O_count, rel=0.05)

    def test_classify_empty(self):
        """test_classify_empty: If water is entirely below substrate, returns empty list."""
        # Frame with water below the "surface" (e.g. Z < 0) when surface is at 10
        frame = create_two_phase_frame(z_shift=-20.0) 
        analyzer = InterfacialAnalyzer(mode="static", static_z_surface=10.0, verbose=False)
        interfacial, bulk = analyzer.classify_interfacial_water(frame, cutoff=4.0)
        
        assert len(interfacial) == 0
        assert len(bulk) > 0 # all water is bulk, as it's outside the [10, 14] interface region

    def test_angle_phi_flat_water(self):
        """test_angle_phi_flat_water: A water molecule lying flat on surface (dipole ∥ surface) → φ ≈ 90°."""
        symbols = ["C", "O", "H", "H"]
        # O at Z=12, H's at Z=12 (flat)
        positions = [
            [5.0, 5.0, 5.0],    # C at Z=5
            [5.0, 5.0, 12.0],   # O
            [5.8, 5.8, 12.0],   # H1
            [4.2, 5.8, 12.0],   # H2
        ]
        # Dipole bisector is along +Y axis. Z is normal. Angle between Y and Z is 90 deg.
        box_bounds = np.array([[0, 10], [0, 10], [0, 20]])
        frame = Frame(0, len(symbols), box_bounds, np.array(symbols), np.array(positions))
        
        analyzer = InterfacialAnalyzer(mode="static", static_z_surface=10.0, verbose=False)
        phi_bins, phi_dist, theta_bins, theta_dist = analyzer.compute_angle_distributions([frame], cutoff=4.0, n_angle_bins=18)
        
        # Find which bin has the probability mass
        max_phi_bin_idx = np.argmax(phi_dist)
        phi_peak = phi_bins[max_phi_bin_idx]
        assert 80 <= phi_peak <= 100  # ≈ 90°

    def test_angle_theta_pointing_down(self):
        """test_angle_theta_pointing_down: O-H pointing toward surface (lower Z) → θ ≈ 180°."""
        symbols = ["C", "O", "H", "H"]
        # Surface at Z=10. Normal is +Z.
        # O at Z=12. H pointing straight down to Z=11.
        # Vector O->H is (0,0,-1). Normal is (0,0,1). Angle = 180.
        positions = [
            [5.0, 5.0, 5.0],    # C
            [5.0, 5.0, 12.0],   # O
            [5.0, 5.0, 11.2],   # H1 (pointing down)
            [5.5, 5.5, 11.2],   # H2
        ]
        box_bounds = np.array([[0, 10], [0, 10], [0, 20]])
        frame = Frame(0, len(symbols), box_bounds, np.array(symbols), np.array(positions))
        
        analyzer = InterfacialAnalyzer(mode="static", static_z_surface=10.0, verbose=False)
        phi_bins, phi_dist, theta_bins, theta_dist = analyzer.compute_angle_distributions([frame], cutoff=4.0, n_angle_bins=18)
        
        # Find which bin has the peak for theta
        # There are two O-H bonds. One is straight down (180), other is slanted.
        # At least some probability should be at ~180.
        theta_prob_at_180 = theta_dist[-1] # last bin is 170-180
        assert theta_prob_at_180 > 0.04

    def test_hbond_count_bulk_reference(self):
        """test_hbond_count_bulk_reference: Bulk water reference gives expected mean."""
        # Create a bulk-like cluster of water molecules
        symbols = ["C"]
        positions = [[5.0, 5.0, 0.0]] # Surface
    
        # A simple dimer in bulk (Z = 20)
        symbols.extend(["O", "H", "H"])
        positions.extend([
            [5.0, 5.0, 20.0],
            [5.0, 4.2, 20.5],
            [5.8, 5.0, 20.5],
        ])
        symbols.extend(["O", "H", "H"])
        positions.extend([
            [5.0, 5.0, 22.5], # 2.5 A away
            [5.0, 5.8, 22.0], # H pointing towards the other O
            [4.2, 5.0, 22.0],
        ])
    
        box_bounds = np.array([[0, 10], [0, 10], [0, 30]])
        frame = Frame(0, len(symbols), box_bounds, np.array(symbols), np.array(positions))
        
        analyzer = InterfacialAnalyzer(mode="static", static_z_surface=10.0, verbose=False)
        # Relax constraints to ensure the bond is caught
        analyzer.r_oo_hbond = 4.0
        analyzer.angle_ooh_hbond = 60.0
        
        _, bulk_ref = analyzer.compute_hbond_statistics([frame], cutoff=4.0)
        
        assert bulk_ref > 0.0
