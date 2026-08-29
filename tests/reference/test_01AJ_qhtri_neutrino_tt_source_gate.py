import math

from idt.qhtri_neutrino_gravity import (
    frobenius_norm,
    phase_encoded_quadrupole,
    polarization_components_z,
    project_tt,
    trace3,
    transverse_residual,
    tt_source_gate,
)


def _max_abs_matrix(m):
    return max(abs(x) for row in m for x in row)


def test_isotropic_source_has_zero_tt_projection():
    stress = ((2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0))
    tt = project_tt(stress, (0.0, 0.0, 1.0))
    assert _max_abs_matrix(tt) < 1e-12
    assert not tt_source_gate(stress, (0.0, 0.0, 1.0)).admitted


def test_longitudinal_source_has_zero_tt_projection():
    stress = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 3.0))
    tt = project_tt(stress, (0.0, 0.0, 1.0))
    assert _max_abs_matrix(tt) < 1e-12
    assert not tt_source_gate(stress, (0.0, 0.0, 1.0)).admitted


def test_plus_quadrupole_survives_tt_gate_with_sqrt2_norm():
    stress = ((1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 0.0))
    result = tt_source_gate(stress, (0.0, 0.0, 1.0))
    assert result.admitted
    assert math.isclose(result.norm, math.sqrt(2.0), rel_tol=1e-12, abs_tol=1e-12)
    assert abs(result.trace_residual) < 1e-12
    assert max(abs(x) for x in result.transverse_residual) < 1e-12


def test_cross_quadrupole_survives_tt_gate_with_sqrt2_norm():
    stress = ((0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 0.0))
    result = tt_source_gate(stress, (0.0, 0.0, 1.0))
    assert result.admitted
    assert math.isclose(result.norm, math.sqrt(2.0), rel_tol=1e-12, abs_tol=1e-12)


def test_phase_encoded_quadrupole_maps_exactly_to_spin2_polarizations():
    for phase in (0.0, 0.17, 0.41, 0.93, 1.37):
        stress = phase_encoded_quadrupole(phase)
        tt = project_tt(stress, (0.0, 0.0, 1.0))
        plus, cross = polarization_components_z(tt)
        assert math.isclose(plus, math.cos(2.0 * phase), rel_tol=1e-12, abs_tol=1e-12)
        assert math.isclose(cross, math.sin(2.0 * phase), rel_tol=1e-12, abs_tol=1e-12)


def test_tt_projection_is_traceless_and_transverse_for_generic_symmetric_source():
    stress = ((1.3, -0.4, 0.8), (-0.4, 2.1, 0.2), (0.8, 0.2, -0.7))
    direction = (1.0, 2.0, 3.0)
    tt = project_tt(stress, direction)
    assert abs(trace3(tt)) < 1e-12
    assert max(abs(x) for x in transverse_residual(tt, direction)) < 1e-12


def test_tt_projection_is_idempotent():
    stress = ((1.3, -0.4, 0.8), (-0.4, 2.1, 0.2), (0.8, 0.2, -0.7))
    direction = (1.0, -2.0, 0.5)
    once = project_tt(stress, direction)
    twice = project_tt(once, direction)
    diff = tuple(tuple(twice[i][j] - once[i][j] for j in range(3)) for i in range(3))
    assert frobenius_norm(diff) < 1e-12


def test_zero_direction_fails_closed():
    stress = phase_encoded_quadrupole(0.2)
    try:
        project_tt(stress, (0.0, 0.0, 0.0))
    except ValueError:
        pass
    else:
        raise AssertionError("zero propagation direction must fail closed")
