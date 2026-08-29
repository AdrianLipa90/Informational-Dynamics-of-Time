import math

from idt.linearized_einstein_response import (
    C_SI,
    G_SI,
    far_zone_prefactor,
    far_zone_tt_response,
    integrated_stress_from_energy,
)
from idt.neutrino_stream_stress import normalized_stream_stress, tetrahedral_directions
from idt.qhtri_neutrino_gravity import polarization_components_z


def _max_abs_matrix(m):
    return max(abs(x) for row in m for x in row)


def test_far_zone_prefactor_matches_linearized_einstein_normalization():
    r = 3.7
    expected = 4.0 * G_SI / (C_SI ** 4 * r)
    assert math.isclose(far_zone_prefactor(r), expected, rel_tol=1e-15, abs_tol=0.0)


def test_one_joule_plus_source_at_one_meter_has_expected_dimensionless_strain():
    source = ((1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 0.0))
    response = far_zone_tt_response(source, (0.0, 0.0, 1.0), 1.0)
    plus, cross = polarization_components_z(response.strain)
    expected = 4.0 * G_SI / (C_SI ** 4)
    assert math.isclose(plus, expected, rel_tol=1e-15, abs_tol=0.0)
    assert abs(cross) < 1e-60
    assert response.strain_norm > 0.0


def test_far_zone_strain_scales_linearly_with_energy_and_inverse_distance():
    shape = ((1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 0.0))
    source_a = integrated_stress_from_energy(shape, 2.0)
    source_b = integrated_stress_from_energy(shape, 10.0)
    a = far_zone_tt_response(source_a, (0.0, 0.0, 1.0), 4.0)
    b = far_zone_tt_response(source_b, (0.0, 0.0, 1.0), 2.0)
    assert math.isclose(b.strain_norm / a.strain_norm, 10.0, rel_tol=1e-12, abs_tol=1e-12)


def test_isotropic_integrated_stress_has_zero_far_zone_tt_response():
    source = integrated_stress_from_energy(
        ((1.0 / 3.0, 0.0, 0.0), (0.0, 1.0 / 3.0, 0.0), (0.0, 0.0, 1.0 / 3.0)),
        1.0e12,
    )
    response = far_zone_tt_response(source, (0.0, 0.0, 1.0), 100.0)
    assert _max_abs_matrix(response.strain) < 1e-50


def test_tetrahedral_neutrino_streams_remain_zero_after_physical_normalization():
    shape = normalized_stream_stress(tetrahedral_directions(), [1.0, 1.0, 1.0, 1.0])
    source = integrated_stress_from_energy(shape, 1.0e18)
    response = far_zone_tt_response(source, (0.0, 0.0, 1.0), 1.0e6)
    assert response.strain_norm < 1e-40


def test_transverse_ultrarelativistic_stream_reaches_nonzero_einstein_response():
    shape = normalized_stream_stress([(1.0, 0.0, 0.0)], [1.0])
    energy = 5.0e15
    source = integrated_stress_from_energy(shape, energy)
    distance = 2.0e6
    response = far_zone_tt_response(source, (0.0, 0.0, 1.0), distance)
    plus, cross = polarization_components_z(response.strain)
    expected = 0.5 * energy * 4.0 * G_SI / (C_SI ** 4 * distance)
    assert math.isclose(plus, expected, rel_tol=1e-12, abs_tol=0.0)
    assert abs(cross) < 1e-60
    assert response.strain_norm > 0.0
