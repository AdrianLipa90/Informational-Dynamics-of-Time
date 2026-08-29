"""Local conservative transport identities for phase-driven neutrino anisotropy.

For fixed massless stream directions ``k_a^mu=(1,n_a)`` and local energy
 densities ``u_a``, the kinetic transport equation is

    (d_t + c n_a.grad) u_a = C_a.

With ``x^0=ct`` this gives

    partial_mu T^{mu nu} = (1/c) sum_a k_a^nu C_a.

Hence a collision/redistribution operator is locally energy-momentum conserving
when its zeroth and first directional moments vanish.
"""

from __future__ import annotations

import math
from typing import Sequence

from .neutrino_conserved_quadrupole import TRANSVERSE_OCTET_DIRECTIONS
from .qhtri_neutrino_gravity import normalize_direction


C_SI = 299_792_458.0


def phase_quadrupole_pair_power_rates(
    modulation_joule: float,
    phase_rad: float,
    phase_rate_rad_s: float,
) -> tuple[float, float, float, float]:
    """Analytic dW/dt for the 01AO four opposite-pair energies [W]."""

    amp = float(modulation_joule)
    phase = float(phase_rad)
    rate = float(phase_rate_rad_s)
    if not all(math.isfinite(x) for x in (amp, phase, rate)):
        raise ValueError("modulation, phase and phase rate must be finite")
    if amp < 0.0:
        raise ValueError("modulation_joule must be non-negative")
    s2 = math.sin(2.0 * phase)
    c2 = math.cos(2.0 * phase)
    return (
        -2.0 * amp * s2 * rate,
        +2.0 * amp * s2 * rate,
        +2.0 * amp * c2 * rate,
        -2.0 * amp * c2 * rate,
    )


def phase_quadrupole_stream_power_rates(
    modulation_joule: float,
    phase_rad: float,
    phase_rate_rad_s: float,
) -> tuple[float, ...]:
    """Split each opposite-pair power rate equally into its two streams."""

    pair_rates = phase_quadrupole_pair_power_rates(
        modulation_joule, phase_rad, phase_rate_rad_s
    )
    return tuple(rate / 2.0 for rate in pair_rates for _ in range(2))


def collision_four_moment_power(
    directions: Sequence[Sequence[float]],
    stream_power_rates_watt: Sequence[float],
) -> tuple[float, float, float, float]:
    """Return sum_a k_a^nu C_a for integrated stream powers [W]."""

    if len(directions) == 0 or len(directions) != len(stream_power_rates_watt):
        raise ValueError("directions and stream powers must have equal non-zero length")
    ns = tuple(normalize_direction(d) for d in directions)
    rates = tuple(float(x) for x in stream_power_rates_watt)
    if not all(math.isfinite(x) for x in rates):
        raise ValueError("stream power rates must be finite")
    return (
        sum(rates),
        sum(r * n[0] for r, n in zip(rates, ns)),
        sum(r * n[1] for r, n in zip(rates, ns)),
        sum(r * n[2] for r, n in zip(rates, ns)),
    )


def phase_quadrupole_collision_four_moment_power(
    modulation_joule: float,
    phase_rad: float,
    phase_rate_rad_s: float,
) -> tuple[float, float, float, float]:
    return collision_four_moment_power(
        TRANSVERSE_OCTET_DIRECTIONS,
        phase_quadrupole_stream_power_rates(
            modulation_joule, phase_rad, phase_rate_rad_s
        ),
    )


def local_stress_divergence_from_transport(
    directions: Sequence[Sequence[float]],
    density_time_derivatives_j_m3_s: Sequence[float],
    density_gradients_j_m4: Sequence[Sequence[float]],
    c_si: float = C_SI,
) -> tuple[float, float, float, float]:
    """Compute partial_mu T^{mu nu} from stream density derivatives/gradients.

    For stream a,

        D_a = (1/c) partial_t u_a + n_a . grad u_a,

    and the returned four-vector is ``sum_a k_a^nu D_a``.
    """

    if (
        len(directions) == 0
        or len(directions) != len(density_time_derivatives_j_m3_s)
        or len(directions) != len(density_gradients_j_m4)
    ):
        raise ValueError("all stream arrays must have equal non-zero length")
    c = float(c_si)
    if not math.isfinite(c) or c <= 0.0:
        raise ValueError("c_si must be finite and positive")
    ns = tuple(normalize_direction(d) for d in directions)
    du = tuple(float(x) for x in density_time_derivatives_j_m3_s)
    grads = tuple(tuple(float(x) for x in g) for g in density_gradients_j_m4)
    if any(len(g) != 3 for g in grads):
        raise ValueError("each density gradient must have three components")
    if not all(math.isfinite(x) for x in du):
        raise ValueError("density time derivatives must be finite")
    if not all(math.isfinite(x) for g in grads for x in g):
        raise ValueError("density gradients must be finite")

    directional = tuple(
        du_a / c + sum(n[i] * grad[i] for i in range(3))
        for du_a, grad, n in zip(du, grads, ns)
    )
    return (
        sum(directional),
        sum(d * n[0] for d, n in zip(directional, ns)),
        sum(d * n[1] for d, n in zip(directional, ns)),
        sum(d * n[2] for d, n in zip(directional, ns)),
    )
