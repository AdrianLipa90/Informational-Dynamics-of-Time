import math

import numpy as np
import pytest

from idt.neutrino_conserved_quadrupole import (
    TRANSVERSE_OCTET_DIRECTIONS,
    phase_quadrupole_source,
)
from idt.neutrino_phase_transport import (
    collision_four_moment_power,
    local_stress_divergence_from_transport,
    phase_quadrupole_collision_four_moment_power,
    phase_quadrupole_pair_power_rates,
    phase_quadrupole_stream_power_rates,
)


def test_analytic_pair_power_rates_match_centered_finite_difference():
    energy = 40.0
    amp = 3.0
    phi = 0.73
    phidot = 2.4
    dt = 1e-7
    before = phase_quadrupole_source(energy, amp, phi - phidot * dt).pair_energies_joule
    after = phase_quadrupole_source(energy, amp, phi + phidot * dt).pair_energies_joule
    numerical = tuple((b - a) / (2.0 * dt) for a, b in zip(before, after))
    analytic = phase_quadrupole_pair_power_rates(amp, phi, phidot)
    assert max(abs(a - b) for a, b in zip(analytic, numerical)) < 1e-6


def test_phase_collision_has_exact_zero_energy_momentum_moments():
    for phi in np.linspace(-math.pi, math.pi, 17):
        residual = phase_quadrupole_collision_four_moment_power(4.0, float(phi), 7.0)
        assert max(abs(x) for x in residual) < 1e-12


def test_stream_power_rates_sum_to_zero_and_preserve_opposite_pair_balance():
    rates = phase_quadrupole_stream_power_rates(2.0, 0.37, 5.0)
    assert len(rates) == 8
    assert abs(sum(rates)) < 1e-12
    for i in range(0, 8, 2):
        assert rates[i] == rates[i + 1]


def test_generic_nonconserving_collision_exposes_exchange_four_moment():
    residual = collision_four_moment_power(
        [(1.0, 0.0, 0.0), (-1.0, 0.0, 0.0)],
        [3.0, 0.0],
    )
    assert residual[0] == 3.0
    assert residual[1] == 3.0


def test_local_homogeneous_phase_collision_closes_divergence_when_inserted_as_transport():
    volume = 2.0
    stream_power = phase_quadrupole_stream_power_rates(3.0, 0.2, 4.0)
    du_dt = tuple(power / volume for power in stream_power)
    # Homogeneous cell: transport derivative itself carries the collision update.
    # Since the collision has zero zeroth/first moment, the summed stress divergence closes.
    gradients = [(0.0, 0.0, 0.0)] * 8
    divergence = local_stress_divergence_from_transport(
        TRANSVERSE_OCTET_DIRECTIONS,
        du_dt,
        gradients,
        c_si=1.0,
    )
    assert max(abs(x) for x in divergence) < 1e-12


def test_free_streaming_profile_closes_local_divergence_stream_by_stream():
    directions = [(1.0, 0.0, 0.0), (0.0, -1.0, 0.0)]
    c = 5.0
    gradients = [(2.0, 0.0, 0.0), (0.0, -3.0, 0.0)]
    # Choose du/dt = -c n.grad(u), so each convective derivative vanishes.
    du_dt = [-c * 2.0, -c * 3.0]
    divergence = local_stress_divergence_from_transport(
        directions, du_dt, gradients, c_si=c
    )
    assert max(abs(x) for x in divergence) < 1e-12


def test_transport_validation_fails_closed():
    with pytest.raises(ValueError):
        phase_quadrupole_pair_power_rates(-1.0, 0.0, 1.0)
    with pytest.raises(ValueError):
        collision_four_moment_power([], [])
    with pytest.raises(ValueError):
        local_stress_divergence_from_transport(
            [(1.0, 0.0, 0.0)], [0.0], [(0.0, 0.0)], c_si=1.0
        )
