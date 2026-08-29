"""01AQ: two-rotor -> Lambda-board -> neutrino-metronome source binding.

This module formalizes the mechanical correspondence used by the QHTRI source
construction:

    two rotor phases -> Minkowski-form common/differential coordinates
    -> Lambda coupling -> relative neutrino phase carrier
    -> conserved 01AO quadrupole -> 01AP collision/transport rates.

The gate is an exact model binding to the already-tested 01AO/01AP source family.
It keeps the neutrino phase drive relative (traceless across flavour channels),
so a pure global U(1) phase is not promoted to a stress-energy modulation.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

from .neutrino_conserved_quadrupole import (
    PhaseQuadrupoleSource,
    phase_quadrupole_source,
)
from .neutrino_phase_transport import (
    phase_quadrupole_collision_four_moment_power,
    phase_quadrupole_stream_power_rates,
)


@dataclass(frozen=True)
class MinkowskiRotorState:
    """Two rotor phases decomposed into common and differential coordinates.

    For rotor phases theta_+ and theta_-, define

        tau = (theta_+ + theta_-)/2
        chi = (theta_+ - theta_-)/2

    and likewise for angular rates.  The algebraic Minkowski-form identity is

        tau^2 - chi^2 = theta_+ theta_-.

    ``chi`` is the spin/relative coordinate used by the Lambda board.
    """

    theta_plus_rad: float
    theta_minus_rad: float
    omega_plus_rad_s: float
    omega_minus_rad_s: float
    tau_rad: float
    chi_rad: float
    tau_rate_rad_s: float
    chi_rate_rad_s: float
    interval_like_rad2: float


def minkowski_rotor_state(
    theta_plus_rad: float,
    theta_minus_rad: float,
    omega_plus_rad_s: float,
    omega_minus_rad_s: float,
) -> MinkowskiRotorState:
    values = tuple(
        float(x)
        for x in (
            theta_plus_rad,
            theta_minus_rad,
            omega_plus_rad_s,
            omega_minus_rad_s,
        )
    )
    if not all(math.isfinite(x) for x in values):
        raise ValueError("rotor phases and rates must be finite")
    theta_p, theta_m, omega_p, omega_m = values
    tau = 0.5 * (theta_p + theta_m)
    chi = 0.5 * (theta_p - theta_m)
    tau_dot = 0.5 * (omega_p + omega_m)
    chi_dot = 0.5 * (omega_p - omega_m)
    return MinkowskiRotorState(
        theta_plus_rad=theta_p,
        theta_minus_rad=theta_m,
        omega_plus_rad_s=omega_p,
        omega_minus_rad_s=omega_m,
        tau_rad=tau,
        chi_rad=chi,
        tau_rate_rad_s=tau_dot,
        chi_rate_rad_s=chi_dot,
        interval_like_rad2=tau * tau - chi * chi,
    )


@dataclass(frozen=True)
class LambdaBoard:
    """Minimal Lambda coupling from rotor coordinates to the phase carrier.

    ``coupling_fraction`` fixes the conserved quadrupole amplitude through

        A = coupling_fraction * E / 4,

    so positivity of all 01AO stream energies is automatic for 0 <= Lambda <= 1.

    The phase carrier is

        phi = phase_bias + common_gain * tau + spin_gain * chi.

    Default gains select the differential/spin coordinate only.

    ``flavour_gains`` maps this carrier to relative neutrino-metronome phase
    shifts.  Their sum must vanish, removing a common/global U(1) component.
    """

    coupling_fraction: float = 1.0
    common_gain: float = 0.0
    spin_gain: float = 1.0
    phase_bias_rad: float = 0.0
    flavour_gains: tuple[float, float, float] = (1.0, -1.0, 0.0)

    def __post_init__(self) -> None:
        scalars = (
            float(self.coupling_fraction),
            float(self.common_gain),
            float(self.spin_gain),
            float(self.phase_bias_rad),
        )
        if not all(math.isfinite(x) for x in scalars):
            raise ValueError("Lambda board parameters must be finite")
        if not 0.0 <= self.coupling_fraction <= 1.0:
            raise ValueError("coupling_fraction must satisfy 0 <= Lambda <= 1")
        gains = tuple(float(x) for x in self.flavour_gains)
        if len(gains) != 3 or not all(math.isfinite(x) for x in gains):
            raise ValueError("flavour_gains must contain three finite values")
        if abs(sum(gains)) > 1e-12:
            raise ValueError("flavour_gains must be traceless: sum(gains)=0")


@dataclass(frozen=True)
class RotorLambdaNeutrinoDrive:
    rotor: MinkowskiRotorState
    total_energy_joule: float
    modulation_joule: float
    carrier_phase_rad: float
    carrier_phase_rate_rad_s: float
    flavour_phase_shifts_rad: tuple[float, float, float]
    flavour_phase_rates_rad_s: tuple[float, float, float]
    quadrupole: PhaseQuadrupoleSource
    stream_power_rates_watt: tuple[float, ...]
    collision_four_moment_power_watt: tuple[float, float, float, float]


def relative_neutrino_metronome_drive(
    carrier_phase_rad: float,
    carrier_phase_rate_rad_s: float,
    flavour_gains: Sequence[float] = (1.0, -1.0, 0.0),
) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
    """Return traceless relative phase shifts/rates for three flavour metronomes."""

    phi = float(carrier_phase_rad)
    phidot = float(carrier_phase_rate_rad_s)
    gains = tuple(float(x) for x in flavour_gains)
    if not math.isfinite(phi) or not math.isfinite(phidot):
        raise ValueError("carrier phase and rate must be finite")
    if len(gains) != 3 or not all(math.isfinite(x) for x in gains):
        raise ValueError("flavour_gains must contain three finite values")
    if abs(sum(gains)) > 1e-12:
        raise ValueError("flavour_gains must be traceless: sum(gains)=0")
    phase = tuple(g * phi for g in gains)
    rate = tuple(g * phidot for g in gains)
    return phase, rate


def rotor_lambda_neutrino_drive(
    theta_plus_rad: float,
    theta_minus_rad: float,
    omega_plus_rad_s: float,
    omega_minus_rad_s: float,
    total_energy_joule: float,
    board: LambdaBoard = LambdaBoard(),
) -> RotorLambdaNeutrinoDrive:
    """Bind the two-rotor/Lambda model exactly to the 01AO/01AP source chain."""

    energy = float(total_energy_joule)
    if not math.isfinite(energy) or energy <= 0.0:
        raise ValueError("total_energy_joule must be finite and positive")

    rotor = minkowski_rotor_state(
        theta_plus_rad,
        theta_minus_rad,
        omega_plus_rad_s,
        omega_minus_rad_s,
    )
    amp = board.coupling_fraction * energy / 4.0
    phi = (
        board.phase_bias_rad
        + board.common_gain * rotor.tau_rad
        + board.spin_gain * rotor.chi_rad
    )
    phidot = (
        board.common_gain * rotor.tau_rate_rad_s
        + board.spin_gain * rotor.chi_rate_rad_s
    )
    flavour_phase, flavour_rate = relative_neutrino_metronome_drive(
        phi, phidot, board.flavour_gains
    )
    quadrupole = phase_quadrupole_source(energy, amp, phi)
    stream_power = phase_quadrupole_stream_power_rates(amp, phi, phidot)
    residual = phase_quadrupole_collision_four_moment_power(amp, phi, phidot)

    return RotorLambdaNeutrinoDrive(
        rotor=rotor,
        total_energy_joule=energy,
        modulation_joule=amp,
        carrier_phase_rad=phi,
        carrier_phase_rate_rad_s=phidot,
        flavour_phase_shifts_rad=flavour_phase,
        flavour_phase_rates_rad_s=flavour_rate,
        quadrupole=quadrupole,
        stream_power_rates_watt=stream_power,
        collision_four_moment_power_watt=residual,
    )
