from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np

from .shannon_onsager_response import (
    audit_onsager_factorization,
    master_velocity,
    symmetric_generator_from_mobility,
)


class TetraSICPacketFlowError(ValueError):
    pass


_TETRA = np.asarray(
    (
        (1.0, 1.0, 1.0),
        (1.0, -1.0, -1.0),
        (-1.0, 1.0, -1.0),
        (-1.0, -1.0, 1.0),
    ),
    dtype=float,
) / math.sqrt(3.0)

_UNIFORM = np.full(4, 0.25, dtype=float)


def _bloch3(value: Sequence[float]) -> np.ndarray:
    r = np.asarray(value, dtype=float)
    if r.shape != (3,) or not np.all(np.isfinite(r)):
        raise TetraSICPacketFlowError("bloch3 must be a finite length-3 vector")
    if float(np.dot(r, r)) > 1.0 + 1e-12:
        raise TetraSICPacketFlowError("Bloch vector lies outside the unit ball")
    return r


def tetra_sic_probabilities(bloch3: Sequence[float]) -> np.ndarray:
    r = _bloch3(bloch3)
    p = 0.25 * (1.0 + _TETRA @ r)
    if np.any(p <= 0.0):
        # For admitted Bloch-ball states and tetra SIC this should not occur;
        # fail closed because 01D requires strictly positive probabilities.
        raise TetraSICPacketFlowError("tetra SIC probabilities must be strictly positive")
    return p


def bloch_from_tetra_sic(probabilities: Sequence[float]) -> np.ndarray:
    p = np.asarray(probabilities, dtype=float)
    if p.shape != (4,) or not np.all(np.isfinite(p)):
        raise TetraSICPacketFlowError("probabilities must be finite length-4")
    if np.any(p < 0.0) or abs(float(p.sum()) - 1.0) > 1e-12:
        raise TetraSICPacketFlowError("probabilities must be nonnegative and sum to one")
    return 3.0 * (_TETRA.T @ p)


def tetra_symmetric_generator(rate: float) -> np.ndarray:
    m = float(rate)
    if not math.isfinite(m) or m <= 0.0:
        raise TetraSICPacketFlowError("rate must be positive finite")
    mobility = np.full((4, 4), m, dtype=float)
    np.fill_diagonal(mobility, 0.0)
    return symmetric_generator_from_mobility(mobility)


def tetra_probability_velocity(
    bloch3: Sequence[float],
    rate: float,
) -> np.ndarray:
    p = tetra_sic_probabilities(bloch3)
    q = tetra_symmetric_generator(rate)
    return master_velocity(p, q)


def tetra_bloch_velocity(
    bloch3: Sequence[float],
    rate: float,
) -> np.ndarray:
    dp = tetra_probability_velocity(bloch3, rate)
    return 3.0 * (_TETRA.T @ dp)


def elapsed_bloch_packet_velocity(
    ell: float,
    bloch3: Sequence[float],
    ell_velocity: float,
    bloch_velocity: Sequence[float],
) -> np.ndarray:
    l = float(ell)
    dl = float(ell_velocity)
    r = _bloch3(bloch3)
    dr = np.asarray(bloch_velocity, dtype=float)
    if not math.isfinite(l) or l <= 0.0:
        raise TetraSICPacketFlowError("ell must be positive finite")
    if not math.isfinite(dl) or dr.shape != (3,) or not np.all(np.isfinite(dr)):
        raise TetraSICPacketFlowError("packet velocity inputs must be finite")
    return np.concatenate(
        (
            np.asarray((0.5 * dl,)),
            0.5 * (dl * r + l * dr),
        )
    )


@dataclass(frozen=True)
class TetraSICOnsagerAudit:
    reconstruction_defect: float
    isotropic_velocity_defect: float
    onsager_factorization_defect: float
    onsager_dissipation_rate_bits: float


def audit_tetra_sic_onsager(
    bloch3: Sequence[float],
    rate: float,
) -> TetraSICOnsagerAudit:
    r = _bloch3(bloch3)
    p = tetra_sic_probabilities(r)
    reconstructed = bloch_from_tetra_sic(p)
    dp = tetra_probability_velocity(r, rate)
    dr = 3.0 * (_TETRA.T @ dp)
    expected = -4.0 * float(rate) * r
    q = tetra_symmetric_generator(rate)
    onsager = audit_onsager_factorization(p, _UNIFORM, q)
    return TetraSICOnsagerAudit(
        reconstruction_defect=float(np.linalg.norm(reconstructed - r)),
        isotropic_velocity_defect=float(np.linalg.norm(dr - expected)),
        onsager_factorization_defect=onsager.factorization_defect,
        onsager_dissipation_rate_bits=onsager.dissipation_rate_bits,
    )


def tetra_relational_mobility_generator(
    rho_relational: Sequence[float],
    eta_relational: Sequence[float],
) -> np.ndarray:
    """Use the existing 00C/02B zero-drive pair mobility on the tetra K4 graph."""
    from .temporal_wave_dissipation import zero_drive_rate_generator

    rho = np.asarray(rho_relational, dtype=float)
    eta = np.asarray(eta_relational, dtype=float)
    if rho.shape != (4,) or eta.shape != (4,):
        raise TetraSICPacketFlowError("rho_relational and eta_relational must have four entries")
    if not np.all(np.isfinite(rho)) or not np.all(np.isfinite(eta)):
        raise TetraSICPacketFlowError("relational fields must be finite")
    if np.any(rho <= 0.0) or np.any(eta <= 0.0):
        raise TetraSICPacketFlowError("relational density and viscosity must be positive")

    edges=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
    return zero_drive_rate_generator(4,edges,rho,eta)


def tetra_relational_probability_velocity(
    bloch3: Sequence[float],
    rho_relational: Sequence[float],
    eta_relational: Sequence[float],
) -> np.ndarray:
    p=tetra_sic_probabilities(bloch3)
    q=tetra_relational_mobility_generator(rho_relational,eta_relational)
    return master_velocity(p,q)


def tetra_relational_bloch_velocity(
    bloch3: Sequence[float],
    rho_relational: Sequence[float],
    eta_relational: Sequence[float],
) -> np.ndarray:
    dp=tetra_relational_probability_velocity(
        bloch3,
        rho_relational,
        eta_relational,
    )
    return 3.0*(_TETRA.T@dp)
