import math

import numpy as np
import pytest

from idt.temporal_wave_homogenization import TemporalWaveError, effective_long_wave_coefficients
from idt.temporal_wave_holonomy_homogenization import (
    acoustic_holonomy_exponent,
    gauge_redistribute_link_phases,
    holonomy_bloch_operators,
    shifted_cell_phase,
    total_holonomy_phase,
)


def test_uniform_shifted_ring_spectrum():
    n = 11
    mobility = 2.3
    viscosity = 0.7
    h = 1.0 / n
    phi = 0.63
    theta = phi + 0.08
    phases = np.full(n, phi / n)
    K, _ = holonomy_bloch_operators(
        [mobility] * n,
        [viscosity] * n,
        phases,
        theta,
        edge_spacing=h,
    )
    got = float(np.linalg.eigvalsh(K)[0])
    delta = theta - phi
    expected = 4.0 * mobility / (h * h) * math.sin(delta / (2.0 * n)) ** 2
    assert abs(got - expected) < 1e-10


def test_phase_redistribution_preserves_spectra_and_holonomy():
    rng = np.random.default_rng(11)
    n = 8
    mobility = rng.uniform(0.2, 3.0, n)
    viscosity = rng.uniform(0.1, 2.0, n)
    phases = rng.uniform(-1.0, 1.0, n)
    theta = 0.4
    chi = rng.uniform(-2.0, 2.0, n)
    shifted = gauge_redistribute_link_phases(phases, chi)
    K1, C1 = holonomy_bloch_operators(mobility, viscosity, phases, theta, edge_spacing=1.0 / n)
    K2, C2 = holonomy_bloch_operators(mobility, viscosity, shifted, theta, edge_spacing=1.0 / n)
    assert abs(total_holonomy_phase(phases) - total_holonomy_phase(shifted)) < 1e-12
    assert np.max(np.abs(np.linalg.eigvalsh(K1) - np.linalg.eigvalsh(K2))) < 1e-10
    assert np.max(np.abs(np.linalg.eigvalsh(C1) - np.linalg.eigvalsh(C2))) < 1e-10


def test_heterogeneous_holonomy_long_wave_coefficients():
    rng = np.random.default_rng(12)
    n = 9
    mobility = rng.uniform(0.3, 2.5, n)
    viscosity = rng.uniform(0.15, 1.7, n)
    phi = 1.1
    phases = rng.uniform(-1.0, 1.0, n)
    phases = phases - phases.mean() + phi / n
    coeff = effective_long_wave_coefficients(mobility, viscosity)
    errors = []
    for delta in [0.02, 0.01, 0.005]:
        s, k = acoustic_holonomy_exponent(
            mobility,
            viscosity,
            phases,
            phi + delta,
            edge_spacing=1.0 / n,
        )
        errors.append((
            abs(s.imag / abs(k) - coeff.wave_speed) / coeff.wave_speed,
            abs((-2.0 * s.real / (k * k)) - coeff.damping_eff) / coeff.damping_eff,
        ))
    assert errors[-1][0] < 5e-4
    assert errors[-1][1] < 5e-4
    assert math.log(errors[-2][0] / errors[-1][0], 2.0) > 1.7
    assert math.log(errors[-2][1] / errors[-1][1], 2.0) > 1.5


def test_fixed_shift_is_independent_of_absolute_holonomy():
    rng = np.random.default_rng(13)
    n = 7
    mobility = rng.uniform(0.4, 2.0, n)
    viscosity = rng.uniform(0.2, 1.5, n)
    delta = 0.01
    values = []
    for phi in [-1.7, -0.4, 0.8, 1.9]:
        phases = np.full(n, phi / n)
        s, _ = acoustic_holonomy_exponent(
            mobility,
            viscosity,
            phases,
            phi + delta,
            edge_spacing=1.0 / n,
        )
        values.append(s)
    assert max(abs(z - values[0]) for z in values) < 1e-9


def test_no_shift_candidate_is_rejected():
    rng = np.random.default_rng(14)
    n = 8
    mobility = rng.uniform(0.4, 2.0, n)
    viscosity = rng.uniform(0.2, 1.5, n)
    phi = 1.2
    delta = 0.005
    phases = np.full(n, phi / n)
    K, _ = holonomy_bloch_operators(
        mobility,
        viscosity,
        phases,
        phi + delta,
        edge_spacing=1.0 / n,
    )
    mobility_eff = effective_long_wave_coefficients(mobility, viscosity).mobility_eff
    lam = float(np.linalg.eigvalsh(K)[0])
    correct = mobility_eff * delta * delta
    wrong = mobility_eff * (phi + delta) ** 2
    assert abs(lam - correct) / correct < 1e-3
    assert abs(lam - wrong) / wrong > 0.9


def test_fail_closed_invalid_inputs():
    with pytest.raises(TemporalWaveError):
        holonomy_bloch_operators([1.0, 2.0], [1.0, 2.0], [0.0, float("nan")], 0.1)
    with pytest.raises(TemporalWaveError):
        holonomy_bloch_operators([1.0, 2.0, 3.0], [1.0, 2.0], [0.0, 0.0, 0.0], 0.1)
    with pytest.raises(TemporalWaveError):
        acoustic_holonomy_exponent([1.0, 2.0], [1.0, 2.0], [0.0, 0.0], 0.0)
