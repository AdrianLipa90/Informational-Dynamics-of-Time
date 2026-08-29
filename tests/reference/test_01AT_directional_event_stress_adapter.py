import math

import pytest

from idt.neutrino_conserved_quadrupole import TRANSVERSE_OCTET_DIRECTIONS
from idt.neutrino_directional_event_stress import (
    estimate_directional_stress,
    estimate_icetracks_rows,
    estimate_radec_events,
    exposure_corrected_weights,
    radec_unit_vector,
    relative_energy_proxy_weights,
)


def _angle_mod_pi_distance(a: float, b: float) -> float:
    d = (a - b) % math.pi
    return min(d, math.pi - d)


def _radec_from_vector(v):
    x, y, z = v
    ra = math.degrees(math.atan2(y, x)) % 360.0
    dec = math.degrees(math.asin(z / math.sqrt(x * x + y * y + z * z)))
    return ra, dec


def test_radec_cardinal_axes_are_exact():
    assert radec_unit_vector(0.0, 0.0) == pytest.approx((1.0, 0.0, 0.0), abs=1e-15)
    assert radec_unit_vector(90.0, 0.0) == pytest.approx((0.0, 1.0, 0.0), abs=1e-15)
    assert radec_unit_vector(0.0, 90.0) == pytest.approx((0.0, 0.0, 1.0), abs=1e-15)


def test_equal_six_axis_events_are_isotropic_null():
    ra = (0.0, 180.0, 90.0, 270.0, 0.0, 0.0)
    dec = (0.0, 0.0, 0.0, 0.0, 90.0, -90.0)
    est = estimate_radec_events(ra, dec)
    for i in range(3):
        for j in range(3):
            assert est.stress_shape[i][j] == pytest.approx(1.0 / 3.0 if i == j else 0.0, abs=1e-15)
    assert est.lambda_amplitude < 1e-14
    assert est.amplitude_fraction < 1e-14


def test_01ao_event_weights_recover_lambda_and_spin2_phase():
    energy = 80.0
    lam = 0.6
    amp = lam * energy / 4.0
    phi = 0.37
    pair = (
        energy / 4.0 + amp * math.cos(2.0 * phi),
        energy / 4.0 - amp * math.cos(2.0 * phi),
        energy / 4.0 + amp * math.sin(2.0 * phi),
        energy / 4.0 - amp * math.sin(2.0 * phi),
    )
    weights = tuple(w / 2.0 for w in pair for _ in range(2))
    est = estimate_directional_stress(TRANSVERSE_OCTET_DIRECTIONS, weights)
    assert est.lambda_amplitude == pytest.approx(lam, abs=1e-12)
    assert _angle_mod_pi_distance(est.phase_rad_mod_pi, phi) < 1e-12
    assert est.canonical_lambda_family


def test_inverse_acceptance_recovers_hidden_source_shape_exactly():
    energy = 40.0
    lam = 0.4
    phi = 0.71
    amp = lam * energy / 4.0
    pair = (
        energy / 4.0 + amp * math.cos(2.0 * phi),
        energy / 4.0 - amp * math.cos(2.0 * phi),
        energy / 4.0 + amp * math.sin(2.0 * phi),
        energy / 4.0 - amp * math.sin(2.0 * phi),
    )
    true_weights = tuple(w / 2.0 for w in pair for _ in range(2))
    acceptance = (0.4, 0.4, 1.2, 1.2, 0.7, 0.7, 1.6, 1.6)
    observed = tuple(w * a for w, a in zip(true_weights, acceptance))
    corrected = exposure_corrected_weights(observed, acceptance)
    assert corrected == pytest.approx(true_weights, abs=1e-12)
    est = estimate_directional_stress(TRANSVERSE_OCTET_DIRECTIONS, corrected)
    assert est.lambda_amplitude == pytest.approx(lam, abs=1e-12)
    assert _angle_mod_pi_distance(est.phase_rad_mod_pi, phi) < 1e-12


def test_radec_adapter_matches_direct_cartesian_estimator():
    ra_dec = tuple(_radec_from_vector(v) for v in TRANSVERSE_OCTET_DIRECTIONS)
    ra = tuple(x[0] for x in ra_dec)
    dec = tuple(x[1] for x in ra_dec)
    weights = (1.0, 1.0, 2.0, 2.0, 1.5, 1.5, 0.5, 0.5)
    direct = estimate_directional_stress(TRANSVERSE_OCTET_DIRECTIONS, weights)
    sky = estimate_radec_events(ra, dec, weights)
    assert sky.lambda_amplitude == pytest.approx(direct.lambda_amplitude, abs=1e-12)
    assert _angle_mod_pi_distance(sky.phase_rad_mod_pi, direct.phase_rad_mod_pi) < 1e-12


def test_log_energy_proxy_weights_are_scale_free_and_icetracks_adapter_is_typed():
    rows = [
        {"ra": 0.0, "dec": 0.0, "log_energy": 2.0},
        {"ra": 180.0, "dec": 0.0, "log_energy": 2.0},
        {"ra": 90.0, "dec": 0.0, "log_energy": 3.0},
        {"ra": 270.0, "dec": 0.0, "log_energy": 3.0},
    ]
    w0 = relative_energy_proxy_weights([2.0, 2.0, 3.0, 3.0])
    w1 = relative_energy_proxy_weights([7.0, 7.0, 8.0, 8.0])
    assert w0 == pytest.approx(w1, abs=1e-15)
    est = estimate_icetracks_rows(rows, energy_proxy_weighted=True)
    assert math.isfinite(est.lambda_amplitude)
    assert math.isfinite(est.phase_rad_mod_pi)


def test_acceptance_and_input_validation_fail_closed():
    with pytest.raises(ValueError):
        exposure_corrected_weights([1.0], [0.0])
    with pytest.raises(ValueError):
        radec_unit_vector(0.0, 91.0)
    with pytest.raises(ValueError):
        estimate_icetracks_rows([{"ra": 0.0, "dec": 0.0}], energy_proxy_weighted=True)
