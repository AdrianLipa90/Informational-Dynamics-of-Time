from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from idt.half_frame_temporal_gluing import (
    glued_support_labels,
    modular_phase_budget,
    temporal_path_incidence,
)


TOL = 1.0e-12


@dataclass(frozen=True)
class ModularC3PauliAudit:
    quotient_incidence: np.ndarray
    cyclic_shift: np.ndarray
    character_basis: np.ndarray
    character_diagonal: np.ndarray
    pauli_gram: np.ndarray
    su2_lift: np.ndarray
    checks: dict[str, bool]

    @property
    def passed(self) -> bool:
        return all(self.checks.values())


def path3_incidence() -> np.ndarray:
    """Incidence of the 3-edge open temporal path P4 from IDT 02J/02JB."""
    return temporal_path_incidence(3)


def periodic_endpoint_quotient() -> np.ndarray:
    """Map v0,v1,v2,v3 to the three classes [v0=v3], [v1], [v2]."""
    return np.array(
        [
            [1.0, 0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ],
        dtype=float,
    )


def cyclic_incidence() -> np.ndarray:
    """Incidence of P4/(v0~v3), i.e. the oriented triangle C3."""
    return periodic_endpoint_quotient() @ path3_incidence()


def cyclic_shift() -> np.ndarray:
    """Regular C3 shift e1->e2->e3->e1 on the frame-edge basis."""
    return np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
        ],
        dtype=complex,
    )


def character_basis_f3() -> np.ndarray:
    omega = np.exp(2j * math.pi / 3.0)
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega**2],
            [1.0, omega**2, omega],
        ],
        dtype=complex,
    ) / math.sqrt(3.0)


def pauli_basis() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sy = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    return sx, sy, sz


def hs(a: np.ndarray, b: np.ndarray) -> float:
    value = 0.5 * np.trace(a @ b)
    if abs(value.imag) > TOL:
        raise ValueError("Hilbert-Schmidt product expected real")
    return float(value.real)


def su2_cyclic_lift() -> np.ndarray:
    """SU(2) lift of the 120-degree SO(3) rotation around (1,1,1)/sqrt(3)."""
    sx, sy, sz = pauli_basis()
    n_sigma = (sx + sy + sz) / math.sqrt(3.0)
    half_angle = math.pi / 3.0
    return (
        math.cos(half_angle) * np.eye(2, dtype=complex)
        - 1j * math.sin(half_angle) * n_sigma
    )


def audit_mod6pi_c3_pauli_bridge() -> ModularC3PauliAudit:
    b = cyclic_incidence()
    p = cyclic_shift()
    f3 = character_basis_f3()
    omega = np.exp(2j * math.pi / 3.0)
    diagonal = f3.conj().T @ p @ f3
    target_diagonal = np.diag([1.0, omega**2, omega])

    pauli = pauli_basis()
    gram = np.array([[hs(a, c) for c in pauli] for a in pauli], dtype=float)
    u = su2_cyclic_lift()

    conjugated = tuple(u @ s @ u.conj().T for s in pauli)
    equivariance_residual = max(
        float(np.max(np.abs(conjugated[j] - pauli[(j + 1) % 3])))
        for j in range(3)
    )

    checks = {
        "parent_02j_modular_sector_is_exact_6pi": (
            abs(modular_phase_budget(3) - 6.0 * math.pi) < TOL
            and glued_support_labels(3) == ("1", "12", "23", "3")
        ),
        "periodic_P4_quotient_is_three_vertex_cycle": (
            b.shape == (3, 3)
            and np.linalg.matrix_rank(b, TOL) == 2
            and np.allclose(np.sum(b, axis=0), 0.0, atol=TOL)
            and np.all(np.sum(np.abs(b), axis=1) == 2.0)
        ),
        "c3_shift_has_order_three": np.allclose(
            np.linalg.matrix_power(p, 3), np.eye(3), atol=TOL
        ),
        "f3_is_unitary": np.allclose(f3.conj().T @ f3, np.eye(3), atol=TOL),
        "f3_diagonalizes_same_c3_shift": np.allclose(
            diagonal, target_diagonal, atol=TOL
        ),
        "pauli_triplet_is_real_orthonormal_herm0_basis": (
            np.allclose(gram, np.eye(3), atol=TOL)
            and all(abs(np.trace(s)) < TOL for s in pauli)
            and all(np.allclose(s, s.conj().T, atol=TOL) for s in pauli)
        ),
        "su2_lift_is_special_unitary": (
            np.allclose(u.conj().T @ u, np.eye(2), atol=TOL)
            and abs(np.linalg.det(u) - 1.0) < TOL
        ),
        "adjoint_action_cycles_pauli_axes": equivariance_residual < TOL,
        "spinorial_cube_is_minus_identity": np.allclose(
            np.linalg.matrix_power(u, 3), -np.eye(2), atol=TOL
        ),
        "adjoint_c3_action_has_order_three": all(
            np.allclose(
                np.linalg.matrix_power(u, 3)
                @ s
                @ np.linalg.matrix_power(u.conj().T, 3),
                s,
                atol=TOL,
            )
            for s in pauli
        ),
    }

    return ModularC3PauliAudit(
        quotient_incidence=b,
        cyclic_shift=p,
        character_basis=f3,
        character_diagonal=diagonal,
        pauli_gram=gram,
        su2_lift=u,
        checks=checks,
    )
