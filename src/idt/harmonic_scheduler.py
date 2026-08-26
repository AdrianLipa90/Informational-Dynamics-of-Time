from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

BASE_FREQUENCY_HZ = 7.83
DEFAULT_MAX_BAND = 7


@dataclass(frozen=True)
class HarmonicBand:
    index: int
    frequency_hz: float
    period_s: float
    role: str


_BAND_ROLES = {
    0: "heartbeat_observation",
    1: "queue_and_admission",
    2: "candidate_microsteps",
    3: "critic_and_graph_audit",
    4: "numerics_and_small_slices",
    5: "serialization_and_repository_io",
    6: "visualization",
    7: "latex_and_heavy_build",
}


def band(index: int, base_frequency_hz: float = BASE_FREQUENCY_HZ) -> HarmonicBand:
    if index < 0:
        raise ValueError("band index must be non-negative")
    if base_frequency_hz <= 0.0:
        raise ValueError("base frequency must be positive")
    frequency = base_frequency_hz / (2**index)
    return HarmonicBand(
        index=index,
        frequency_hz=frequency,
        period_s=1.0 / frequency,
        role=_BAND_ROLES.get(index, "reserved"),
    )


def eligible_tick(tick: int, band_index: int) -> bool:
    """Return whether an integer base tick belongs to a workload band.

    B0 is an observation/heartbeat band sampled at every base tick.
    Workload bands B1+ form disjoint phase classes:
        tick == 2**(k-1) mod 2**k.
    """
    if tick < 0:
        raise ValueError("tick must be non-negative")
    if band_index < 0:
        raise ValueError("band index must be non-negative")
    if band_index == 0:
        return True
    modulus = 2**band_index
    phase = 2 ** (band_index - 1)
    return tick % modulus == phase


def admission_band(tick: int, max_band: int = DEFAULT_MAX_BAND) -> Optional[int]:
    """Return the unique workload band B1..Bmax for this tick.

    Ticks on deeper dyadic boundaries are intentionally left unassigned,
    creating quiet maintenance slots instead of catch-up bursts.
    """
    if tick <= 0:
        return None
    if max_band < 1:
        return None
    for k in range(1, max_band + 1):
        if eligible_tick(tick, k):
            return k
    return None


def next_eligible_tick(after_tick: int, band_index: int) -> int:
    if after_tick < 0:
        raise ValueError("after_tick must be non-negative")
    if band_index < 1:
        raise ValueError("workload band must be B1 or higher")
    modulus = 2**band_index
    phase = 2 ** (band_index - 1)
    candidate = after_tick + 1
    offset = (phase - candidate) % modulus
    return candidate + offset


def jitter_adjusted_band(
    band_index: int,
    *,
    observed_jitter_s: float,
    jitter_limit_s: float,
    max_band: int = DEFAULT_MAX_BAND,
) -> int:
    """Demote a workload by one band when measured jitter exceeds its limit."""
    if band_index < 1:
        raise ValueError("workload band must be B1 or higher")
    if observed_jitter_s < 0.0 or jitter_limit_s < 0.0:
        raise ValueError("jitter values must be non-negative")
    if observed_jitter_s > jitter_limit_s:
        return min(band_index + 1, max_band)
    return min(band_index, max_band)
