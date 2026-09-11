from __future__ import annotations

from dataclasses import dataclass
import math

SCHEMA = "IDT_ORCHORBITAL_600CELL_CANDIDATE_V0_1"
STATUS = "CANDIDATE"
ACTIVE_WORKING_VERSION = True
CANONICAL = False
TEMPORAL_CORE_MUTATED = False
PHYSICAL_TIME_BINDING = "OPEN"
SOURCE_CARRIER = "PNCS_600CELL_S3_ANGULAR_CANDIDATE_V0_1"
SUPPORTED_L = tuple(range(6))
PHI = (1.0 + math.sqrt(5.0)) / 2.0

_ADJ = {
    0: 12.0,
    1: 6.0 * PHI,
    2: 4.0 * PHI,
    3: 3.0,
    4: 0.0,
    5: -2.0,
}


class IDTOrchorbital600CellCandidateError(ValueError):
    pass


@dataclass(frozen=True)
class Orchorbital600CellSector:
    ell: int
    multiplicity: int
    adjacency_eigenvalue: float
    angular_eigenvalue: int
    status: str
    active_working_version: bool
    canonical: bool
    temporal_core_mutated: bool
    physical_time_binding: str
    source_carrier: str


def bind_orchorbital_sector(ell: int) -> Orchorbital600CellSector:
    if isinstance(ell, bool) or not isinstance(ell, int) or ell not in SUPPORTED_L:
        raise IDTOrchorbital600CellCandidateError("ell must be an integer in [0,5]")
    return Orchorbital600CellSector(
        ell=ell,
        multiplicity=(ell + 1) ** 2,
        adjacency_eigenvalue=_ADJ[ell],
        angular_eigenvalue=ell * (ell + 2),
        status=STATUS,
        active_working_version=ACTIVE_WORKING_VERSION,
        canonical=CANONICAL,
        temporal_core_mutated=TEMPORAL_CORE_MUTATED,
        physical_time_binding=PHYSICAL_TIME_BINDING,
        source_carrier=SOURCE_CARRIER,
    )


def working_orchorbital_table() -> tuple[Orchorbital600CellSector, ...]:
    return tuple(bind_orchorbital_sector(ell) for ell in SUPPORTED_L)


def supported_dimension() -> int:
    return sum(row.multiplicity for row in working_orchorbital_table())
