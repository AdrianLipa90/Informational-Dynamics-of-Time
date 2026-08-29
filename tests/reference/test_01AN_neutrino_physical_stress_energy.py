import math

import numpy as np
import pytest

from idt.neutrino_physical_stress import (
    flavour_resolved_integrated_stress,
    integrated_four_momentum_si,
    integrated_massless_stress,
    local_stress_from_integrated,
    minkowski_trace_plus_minus_minus_minus,
)
from idt.qhtri_neutrino_gravity import project_tt
from idt.neutrino_stream_stress import tetrahedral_directions


def test_single_ultrarelativistic_stream_has_exact_null_stress_trace():
    source = integrated_massless_stress([(1.0, 0.0, 0.0)], [7.0])
    assert source.tensor_joule == (
        (7.0, 7.0, 0.0, 0.0),
        (7.0, 7.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    )
    assert minkowski_trace_plus_minus_minus_minus(source.tensor_joule) == 0.0


def test_equal_tetrahedral_packets_are_zero_flux_and_spatially_isotropic():
    directions = tetrahedral_directions()
    source = integrated_massless_stress(directions, [2.0, 2.0, 2.0, 2.0])
    assert np.linalg.norm(source.energy_flux_vector_joule) < 1e-12
    spatial = np.asarray(source.spatial_stress_joule)
    assert np.max(np.abs(spatial - (8.0 / 3.0) * np.eye(3))) < 1e-12
    tt = np.asarray(project_tt(source.spatial_stress_joule, (0.0, 0.0, 1.0)))
    assert np.linalg.norm(tt) < 1e-12


def test_pure_flavour_redistribution_at_fixed_directional_energy_is_exactly_invariant():
    directions = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    before = flavour_resolved_integrated_stress(
        directions,
        [[2.0, 3.0, 5.0], [7.0, 11.0, 13.0]],
    )
    after = flavour_resolved_integrated_stress(
        directions,
        [[8.0, 1.0, 1.0], [10.0, 10.0, 11.0]],
    )
    assert before.tensor_joule == after.tensor_joule


def test_direction_correlated_energy_change_changes_tt_source():
    directions = [
        (1.0, 0.0, 0.0),
        (-1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, -1.0, 0.0),
    ]
    isotropic_xy = integrated_massless_stress(directions, [1.0, 1.0, 1.0, 1.0])
    quadrupole = integrated_massless_stress(directions, [1.4, 1.4, 0.6, 0.6])
    tt0 = np.asarray(project_tt(isotropic_xy.spatial_stress_joule, (0.0, 0.0, 1.0)))
    tt1 = np.asarray(project_tt(quadrupole.spatial_stress_joule, (0.0, 0.0, 1.0)))
    assert np.linalg.norm(tt0) < 1e-12
    assert np.linalg.norm(tt1) > 1.0


def test_local_source_has_energy_density_units_by_volume_scaling():
    source = integrated_massless_stress([(0.0, 0.0, 1.0)], [12.0])
    local = local_stress_from_integrated(source, 3.0)
    assert local[0][0] == 4.0
    assert local[3][3] == 4.0


def test_integrated_four_momentum_obeys_massless_single_packet_relation():
    source = integrated_massless_stress([(0.0, 0.6, 0.8)], [9.0])
    p = integrated_four_momentum_si(source)
    spatial_norm = math.sqrt(sum(x * x for x in p[1:]))
    assert math.isclose(spatial_norm, p[0], rel_tol=1e-12, abs_tol=0.0)


def test_multistream_total_momentum_is_future_nonspacelike():
    source = integrated_massless_stress(
        [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0), (0.0, 1.0, 0.0)],
        [3.0, 2.0, 4.0],
    )
    p = integrated_four_momentum_si(source)
    assert p[0] >= math.sqrt(sum(x * x for x in p[1:])) - 1e-20


def test_source_validation_fails_closed():
    with pytest.raises(ValueError):
        integrated_massless_stress([], [])
    with pytest.raises(ValueError):
        integrated_massless_stress([(1.0, 0.0, 0.0)], [-1.0])
    with pytest.raises(ValueError):
        integrated_massless_stress([(0.0, 0.0, 0.0)], [1.0])
    source = integrated_massless_stress([(1.0, 0.0, 0.0)], [1.0])
    with pytest.raises(ValueError):
        local_stress_from_integrated(source, 0.0)
