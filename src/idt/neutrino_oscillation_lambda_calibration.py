"""01AR: calibrate the Lambda board against standard neutrino oscillation phase.

The calibration keeps two independent Lambda channels explicit:

    Lambda_phi -- phase/rate gain between the QHTRI differential rotor chi
                  and the standard neutrino oscillation probability phase;
    Lambda_A   -- source-amplitude fraction A = Lambda_A E / 4.

For a mass-squared splitting Delta m^2 quoted in eV^2 and neutrino energy E in
eV, the standard vacuum probability phase is

    delta_prob = Delta m^2 L / (4 E)

in natural units.  In SI time units this gives

    omega_prob = Delta m^2 / (4 E hbar),

while the relative propagation eigenphase advances twice as fast:

    omega_state = Delta m^2 / (2 E hbar) = 2 omega_prob.

This factor of two is deliberately matched to the 01AO/01AQ spin-2 carrier,
whose TT coordinates depend on cos(2 phi), sin(2 phi).  Setting the QHTRI
carrier phi equal to delta_prob therefore makes 2 phi track the relative
neutrino state phase without inserting an extra factor by hand.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .qhtri_rotor_lambda_neutrino import LambdaBoard


HBAR_EV_S = 6.582_119_569e-16
C_SI = 299_792_458.0


def _positive_finite(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out) or out <= 0.0:
        raise ValueError(f"{name} must be finite and positive")
    return out


def neutrino_probability_phase_rate_rad_s(
    delta_m2_ev2: float,
    energy_ev: float,
    hbar_ev_s: float = HBAR_EV_S,
) -> float:
    """Return d(delta_prob)/dt = Delta m^2/(4 E hbar) in rad/s."""

    dm2 = _positive_finite(abs(float(delta_m2_ev2)), "abs(delta_m2_ev2)")
    energy = _positive_finite(energy_ev, "energy_ev")
    hbar = _positive_finite(hbar_ev_s, "hbar_ev_s")
    return dm2 / (4.0 * energy * hbar)


def neutrino_relative_state_phase_rate_rad_s(
    delta_m2_ev2: float,
    energy_ev: float,
    hbar_ev_s: float = HBAR_EV_S,
) -> float:
    """Return the relative propagation eigenphase rate Delta m^2/(2 E hbar)."""

    return 2.0 * neutrino_probability_phase_rate_rad_s(
        delta_m2_ev2, energy_ev, hbar_ev_s
    )


def neutrino_probability_phase_rad(
    delta_m2_ev2: float,
    energy_ev: float,
    baseline_m: float,
    hbar_ev_s: float = HBAR_EV_S,
    c_si: float = C_SI,
) -> float:
    """Return the vacuum probability phase after a baseline L."""

    length = float(baseline_m)
    if not math.isfinite(length) or length < 0.0:
        raise ValueError("baseline_m must be finite and non-negative")
    c = _positive_finite(c_si, "c_si")
    return neutrino_probability_phase_rate_rad_s(
        delta_m2_ev2, energy_ev, hbar_ev_s
    ) * length / c


def neutrino_oscillation_length_m(
    delta_m2_ev2: float,
    energy_ev: float,
    hbar_ev_s: float = HBAR_EV_S,
    c_si: float = C_SI,
) -> float:
    """Return the full vacuum probability oscillation length.

    Since sin^2(delta_prob) has period pi in delta_prob,

        L_osc = pi c / omega_prob = 4 pi hbar c E / Delta m^2.
    """

    omega = neutrino_probability_phase_rate_rad_s(
        delta_m2_ev2, energy_ev, hbar_ev_s
    )
    c = _positive_finite(c_si, "c_si")
    return math.pi * c / omega


def lambda_phase_gain_from_rotor_rate(
    delta_m2_ev2: float,
    energy_ev: float,
    chi_rate_rad_s: float,
) -> float:
    """Calibrate Lambda_phi so phi_dot = Lambda_phi chi_dot = omega_prob."""

    chi_dot = float(chi_rate_rad_s)
    if not math.isfinite(chi_dot) or chi_dot == 0.0:
        raise ValueError("chi_rate_rad_s must be finite and non-zero")
    return neutrino_probability_phase_rate_rad_s(delta_m2_ev2, energy_ev) / chi_dot


def lambda_amplitude_fraction(total_energy_joule: float, modulation_joule: float) -> float:
    """Calibrate Lambda_A from the already-normalized 01AO source amplitude."""

    energy = _positive_finite(total_energy_joule, "total_energy_joule")
    amp = float(modulation_joule)
    if not math.isfinite(amp) or amp < 0.0 or amp > energy / 4.0:
        raise ValueError("modulation_joule must satisfy 0 <= A <= E/4")
    return 4.0 * amp / energy


@dataclass(frozen=True)
class LambdaOscillationCalibration:
    delta_m2_ev2: float
    energy_ev: float
    chi_rate_rad_s: float
    lambda_phase_gain: float
    lambda_amplitude_fraction: float
    probability_phase_rate_rad_s: float
    relative_state_phase_rate_rad_s: float
    board: LambdaBoard


def calibrated_lambda_board(
    delta_m2_ev2: float,
    energy_ev: float,
    chi_rate_rad_s: float,
    total_energy_joule: float,
    modulation_joule: float,
    *,
    common_gain: float = 0.0,
    phase_bias_rad: float = 0.0,
    flavour_gains: tuple[float, float, float] = (1.0, -1.0, 0.0),
) -> LambdaOscillationCalibration:
    """Return a LambdaBoard calibrated to an oscillation phase and source amplitude."""

    phase_gain = lambda_phase_gain_from_rotor_rate(
        delta_m2_ev2, energy_ev, chi_rate_rad_s
    )
    amp_fraction = lambda_amplitude_fraction(total_energy_joule, modulation_joule)
    omega_prob = neutrino_probability_phase_rate_rad_s(delta_m2_ev2, energy_ev)
    omega_state = neutrino_relative_state_phase_rate_rad_s(delta_m2_ev2, energy_ev)
    board = LambdaBoard(
        coupling_fraction=amp_fraction,
        common_gain=float(common_gain),
        spin_gain=phase_gain,
        phase_bias_rad=float(phase_bias_rad),
        flavour_gains=flavour_gains,
    )
    return LambdaOscillationCalibration(
        delta_m2_ev2=float(delta_m2_ev2),
        energy_ev=float(energy_ev),
        chi_rate_rad_s=float(chi_rate_rad_s),
        lambda_phase_gain=phase_gain,
        lambda_amplitude_fraction=amp_fraction,
        probability_phase_rate_rad_s=omega_prob,
        relative_state_phase_rate_rad_s=omega_state,
        board=board,
    )
