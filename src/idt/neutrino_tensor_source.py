"""Flavour-Hilbert -> candidate spatial tensor expectation gate.

Natural units with hbar=1 are used for the commutator-rate identity.  The module
keeps physical stress-energy normalization as a separate downstream binding.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np


def _state(state: Sequence[complex]) -> np.ndarray:
    psi = np.asarray(state, dtype=np.complex128)
    if psi.ndim != 1 or psi.size == 0:
        raise ValueError("state must be a non-empty vector")
    if not np.all(np.isfinite(psi)):
        raise ValueError("state entries must be finite")
    norm = float(np.vdot(psi, psi).real)
    if not math.isclose(norm, 1.0, rel_tol=1e-10, abs_tol=1e-12):
        raise ValueError("state must be normalized")
    return psi


def _hermitian(operator: Sequence[Sequence[complex]], dim: int) -> np.ndarray:
    op = np.asarray(operator, dtype=np.complex128)
    if op.shape != (dim, dim):
        raise ValueError("operator dimension does not match state")
    if not np.all(np.isfinite(op)):
        raise ValueError("operator entries must be finite")
    if np.max(np.abs(op - op.conj().T)) > 1e-12:
        raise ValueError("operator must be Hermitian")
    return op


def expectation(state: Sequence[complex], operator: Sequence[Sequence[complex]]) -> float:
    psi = _state(state)
    op = _hermitian(operator, psi.size)
    value = np.vdot(psi, op @ psi)
    if abs(value.imag) > 1e-10:
        raise ValueError("Hermitian expectation developed an imaginary residual")
    return float(value.real)


def commutator_norm(
    hamiltonian: Sequence[Sequence[complex]],
    operator: Sequence[Sequence[complex]],
) -> float:
    h = np.asarray(hamiltonian, dtype=np.complex128)
    if h.ndim != 2 or h.shape[0] != h.shape[1]:
        raise ValueError("hamiltonian must be square")
    h = _hermitian(h, h.shape[0])
    op = _hermitian(operator, h.shape[0])
    return float(np.linalg.norm(h @ op - op @ h))


def expectation_rate(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    operator: Sequence[Sequence[complex]],
) -> float:
    """Return d<O>/dt = i <[H,O]> for time-independent O and hbar=1."""

    psi = _state(state)
    h = _hermitian(hamiltonian, psi.size)
    op = _hermitian(operator, psi.size)
    value = 1j * np.vdot(psi, (h @ op - op @ h) @ psi)
    if abs(value.imag) > 1e-10:
        raise ValueError("expectation-rate identity developed an imaginary residual")
    return float(value.real)


def tensor_expectation(
    state: Sequence[complex],
    tensor_operators: Sequence[Sequence[Sequence[Sequence[complex]]]],
) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
    """Evaluate a symmetric 3x3 spatial tensor of Hermitian flavour operators."""

    psi = _state(state)
    if len(tensor_operators) != 3 or any(len(row) != 3 for row in tensor_operators):
        raise ValueError("tensor_operators must be a 3x3 operator array")

    ops = [[_hermitian(tensor_operators[i][j], psi.size) for j in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            if np.max(np.abs(ops[i][j] - ops[j][i])) > 1e-12:
                raise ValueError("spatial tensor operator must be symmetric in i,j")

    return tuple(
        tuple(float(np.vdot(psi, ops[i][j] @ psi).real) for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def tensor_expectation_rate(
    state: Sequence[complex],
    hamiltonian: Sequence[Sequence[complex]],
    tensor_operators: Sequence[Sequence[Sequence[Sequence[complex]]]],
) -> tuple[tuple[float, float, float], tuple[float, float, float], tuple[float, float, float]]:
    psi = _state(state)
    h = _hermitian(hamiltonian, psi.size)
    if len(tensor_operators) != 3 or any(len(row) != 3 for row in tensor_operators):
        raise ValueError("tensor_operators must be a 3x3 operator array")
    return tuple(
        tuple(expectation_rate(psi, h, tensor_operators[i][j]) for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]
