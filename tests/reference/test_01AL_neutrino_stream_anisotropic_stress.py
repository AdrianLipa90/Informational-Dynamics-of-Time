import math

from idt.neutrino_stream_stress import (
    flavour_resolved_stream_stress,
    normalized_stream_stress,
    tetrahedral_directions,
)
from idt.qhtri_neutrino_gravity import polarization_components_z, tt_source_gate


def _max_abs_diff(a, b):
    return max(abs(a[i][j] - b[i][j]) for i in range(3) for j in range(3))


def test_equal_tetrahedral_streams_are_exactly_isotropic():
    stress = normalized_stream_stress(tetrahedral_directions(), [1.0, 1.0, 1.0, 1.0])
    target = ((1.0 / 3.0, 0.0, 0.0), (0.0, 1.0 / 3.0, 0.0), (0.0, 0.0, 1.0 / 3.0))
    assert _max_abs_diff(stress, target) < 1e-12
    assert not tt_source_gate(stress, (0.0, 0.0, 1.0)).admitted


def test_collinear_neutrino_stream_is_longitudinal_for_same_wave_direction():
    stress = normalized_stream_stress([(0.0, 0.0, 1.0)], [1.0])
    result = tt_source_gate(stress, (0.0, 0.0, 1.0))
    assert not result.admitted
    assert result.norm < 1e-12


def test_transverse_neutrino_stream_has_nonzero_tt_anisotropy():
    stress = normalized_stream_stress([(1.0, 0.0, 0.0)], [1.0])
    result = tt_source_gate(stress, (0.0, 0.0, 1.0))
    plus, cross = polarization_components_z(result.tt)
    assert result.admitted
    assert math.isclose(plus, 0.5, rel_tol=1e-12, abs_tol=1e-12)
    assert abs(cross) < 1e-12


def test_internal_flavour_redistribution_at_fixed_direction_totals_leaves_stress_invariant():
    directions = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    before = [[0.7, 0.2, 0.1], [0.1, 0.3, 0.6]]
    after = [[0.1, 0.5, 0.4], [0.55, 0.25, 0.20]]
    s0 = flavour_resolved_stream_stress(directions, before)
    s1 = flavour_resolved_stream_stress(directions, after)
    assert _max_abs_diff(s0, s1) < 1e-12


def test_direction_correlated_weight_transfer_changes_tt_source():
    directions = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    balanced = flavour_resolved_stream_stress(directions, [[0.5, 0.5], [0.5, 0.5]])
    biased = flavour_resolved_stream_stress(directions, [[0.9, 0.9], [0.1, 0.1]])

    g0 = tt_source_gate(balanced, (0.0, 0.0, 1.0))
    g1 = tt_source_gate(biased, (0.0, 0.0, 1.0))
    plus0, _ = polarization_components_z(g0.tt)
    plus1, _ = polarization_components_z(g1.tt)

    assert abs(plus0) < 1e-12
    assert g1.admitted
    assert math.isclose(plus1, 0.4, rel_tol=1e-12, abs_tol=1e-12)
