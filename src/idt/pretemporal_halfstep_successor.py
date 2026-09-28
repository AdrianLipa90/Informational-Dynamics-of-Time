from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True, order=True)
class PretemporalState:
    coarse: int
    sector: int

    def __post_init__(self) -> None:
        if self.coarse < 0:
            raise ValueError("coarse must be >= 0")
        if self.sector not in (0, 1):
            raise ValueError("sector must be 0 or 1")


def half_step(state: PretemporalState) -> PretemporalState:
    if state.sector == 0:
        return PretemporalState(state.coarse, 1)
    return PretemporalState(state.coarse + 1, 0)


def successor(state: PretemporalState) -> PretemporalState:
    return PretemporalState(state.coarse + 1, state.sector)


def normalized_grade(state: PretemporalState) -> Fraction:
    return Fraction(state.coarse, 1) + Fraction(state.sector, 2)


def relational_edge(n: int) -> frozenset[int]:
    if n < 1:
        raise ValueError("n must be >= 1")
    return frozenset((n, n + 1))


def hilbert_shift(n: int) -> int:
    if n < 1:
        raise ValueError("room label must be >= 1")
    return n + 1


def shifted_edge(n: int) -> frozenset[int]:
    return frozenset(hilbert_shift(v) for v in relational_edge(n))


def post_transition_click_label(step_index: int) -> tuple[Fraction, str]:
    if step_index < 1:
        raise ValueError("step_index must be >= 1")
    state = PretemporalState(0, 0)
    for _ in range(step_index):
        state = half_step(state)
    sign = "-" if state.sector == 1 else "+"
    return normalized_grade(state), sign
