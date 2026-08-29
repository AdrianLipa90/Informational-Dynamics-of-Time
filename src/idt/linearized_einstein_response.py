"""Far-zone linearized Einstein response for a supplied integrated stress tensor.

At one retarded source time, the leading far-zone TT solution is represented as

    h_ij^TT = (4 G / (c^4 r)) * [integral T_ij d^3x]^TT.

This module binds SI normalization and the Einstein response only.  Construction
of the underlying QHTRI/neutrino source remains a separate source-dynamics gate.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

from .qhtri_neutrino_gravity import Matrix3, frobenius_norm, project_tt


G_SI = 6.67430e-11
C_SI = 299_792_458.0


def _matrix3_finite(m: Sequence[Sequence[float]]) -> Matrix3:
    if len(m) != 3 or any(len(row) != 3 for row in m):
        raise ValueError("expected a 3x3 matrix")
    out = tuple(tuple(float(x) for x in row) for row in m)
    if not all(math.isfinite(x) for row in out for x in row):
        raise ValueError("matrix entries must be finite")
    return out  # type: ignore[return-value]


def integrated_stress_from_energy(
    stress_shape: Sequence[Sequence[float]],
    total_energy_joule: float,
) -> Matrix3:
    """Scale a dimensionless ultrarelativistic spatial stress shape by total energy."""

    shape = _matrix3_finite(stress_shape)
    energy = float(total_energy_joule)
    if not math.isfinite(energy) or energy < 0.0:
        raise ValueError("total_energy_joule must be finite and non-negative")
    return tuple(tuple(energy * shape[i][j] for j in range(3)) for i in range(3))  # type: ignore[return-value]


def far_zone_prefactor(distance_m: float) -> float:
    r = float(distance_m)
    if not math.isfinite(r) or r <= 0.0:
        raise ValueError("distance_m must be finite and positive")
    return 4.0 * G_SI / (C_SI ** 4 * r)


@dataclass(frozen=True)
class FarZoneTTResponse:
    source_tt_joule: Matrix3
    strain: Matrix3
    strain_norm: float
    prefactor_per_joule: float


def far_zone_tt_response(
    integrated_spatial_stress_joule: Sequence[Sequence[float]],
    wave_direction: Sequence[float],
    distance_m: float,
) -> FarZoneTTResponse:
    """Apply TT projection and leading far-zone linearized Einstein normalization."""

    source = _matrix3_finite(integrated_spatial_stress_joule)
    source_tt = project_tt(source, wave_direction)
    prefactor = far_zone_prefactor(distance_m)
    strain = tuple(
        tuple(prefactor * source_tt[i][j] for j in range(3))
        for i in range(3)
    )  # type: ignore[assignment]
    return FarZoneTTResponse(
        source_tt_joule=source_tt,
        strain=strain,  # type: ignore[arg-type]
        strain_norm=frobenius_norm(strain),
        prefactor_per_joule=prefactor,
    )
