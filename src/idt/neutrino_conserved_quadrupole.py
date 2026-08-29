"""Momentum-conserving transverse quadrupole family for ultrarelativistic streams.

This module supplies an explicit *kinematically admissible* source family whose
integrated four-momentum stays fixed while the spatial TT stress rotates with a
phase.  It is a conservation/control construction, not a microscopic interaction
law.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from .neutrino_physical_stress import (
    IntegratedNeutrinoStress,
    integrated_four_momentum_si,
    integrated_massless_stress,
)


SQRT2_INV = 1.0 / math.sqrt(2.0)
TRANSVERSE_OCTET_DIRECTIONS = (
    (1.0, 0.0, 0.0),
    (-1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, -1.0, 0.0),
    (SQRT2_INV, SQRT2_INV, 0.0),
    (-SQRT2_INV, -SQRT2_INV, 0.0),
    (SQRT2_INV, -SQRT2_INV, 0.0),
    (-SQRT2_INV, SQRT2_INV, 0.0),
)


@dataclass(frozen=True)
class PhaseQuadrupoleSource:
    phase_rad: float
    modulation_joule: float
    source: IntegratedNeutrinoStress
    pair_energies_joule: tuple[float, float, float, float]


def phase_quadrupole_source(
    total_energy_joule: float,
    modulation_joule: float,
    phase_rad: float,
) -> PhaseQuadrupoleSource:
    """Return an eight-stream source with exact spin-2 phase dependence.

    Four opposite stream pairs carry pair energies

        W_x  = E/4 + A cos(2 phi)
        W_y  = E/4 - A cos(2 phi)
        W_d+ = E/4 + A sin(2 phi)
        W_d- = E/4 - A sin(2 phi)

    and every pair is split equally between opposite directions.  Hence total
    energy is E and net three-momentum is exactly zero for every phase.  The TT
    coordinates for propagation along z are

        (T_xx - T_yy)/2 = A cos(2 phi)
        T_xy             = A sin(2 phi).
    """

    energy = float(total_energy_joule)
    amp = float(modulation_joule)
    phase = float(phase_rad)
    if not all(math.isfinite(x) for x in (energy, amp, phase)):
        raise ValueError("energy, modulation and phase must be finite")
    if energy <= 0.0:
        raise ValueError("total_energy_joule must be positive")
    if amp < 0.0 or amp > energy / 4.0:
        raise ValueError("modulation_joule must satisfy 0 <= A <= E/4")

    c2 = math.cos(2.0 * phase)
    s2 = math.sin(2.0 * phase)
    pair = (
        energy / 4.0 + amp * c2,
        energy / 4.0 - amp * c2,
        energy / 4.0 + amp * s2,
        energy / 4.0 - amp * s2,
    )
    stream_energies = tuple(w / 2.0 for w in pair for _ in range(2))
    source = integrated_massless_stress(TRANSVERSE_OCTET_DIRECTIONS, stream_energies)
    return PhaseQuadrupoleSource(
        phase_rad=phase,
        modulation_joule=amp,
        source=source,
        pair_energies_joule=pair,
    )


def integrated_four_momentum_exchange_rate(
    before: IntegratedNeutrinoStress,
    after: IntegratedNeutrinoStress,
    dt_seconds: float,
) -> tuple[float, float, float, float]:
    """Finite-difference external four-force required by a source update.

    Returns ``dP^mu/dt`` in SI force units.  Zero means the update preserves the
    source's integrated four-momentum; it does not by itself prove local
    ``partial_mu T^{mu nu}=0`` inside the source volume.
    """

    dt = float(dt_seconds)
    if not math.isfinite(dt) or dt <= 0.0:
        raise ValueError("dt_seconds must be finite and positive")
    p0 = integrated_four_momentum_si(before)
    p1 = integrated_four_momentum_si(after)
    return tuple((b - a) / dt for a, b in zip(p0, p1))
