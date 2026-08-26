from __future__ import annotations

import math
from typing import Iterable, Sequence

import numpy as np


def kappa() -> float:
    return float(math.log(2.0) / (24.0 * math.pi))


def info_potential(z: np.ndarray, alpha: float = 1.0, beta: float = 0.18) -> np.ndarray:
    """Information functional on C≈R^2.

    I(x,y)=κ[ α/2 (x^2+y^2) + β/4 (x^4+y^4) ].
    """
    z = np.asarray(z, dtype=float)
    x = z[..., 0]
    y = z[..., 1]
    κ = kappa()
    return κ * (0.5 * alpha * (x * x + y * y) + 0.25 * beta * (x**4 + y**4))


def grad_info(z: np.ndarray, alpha: float = 1.0, beta: float = 0.18) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    x = z[..., 0]
    y = z[..., 1]
    κ = kappa()
    gx = κ * (alpha * x + beta * x**3)
    gy = κ * (alpha * y + beta * y**3)
    return np.stack([gx, gy], axis=-1)


def phase_hamiltonian(z: np.ndarray, eta: float = 0.75, gamma: float = 0.04) -> np.ndarray:
    """Independent phase Hamiltonian.

    H(x,y)=η xy + γ/3 (x^3 - 3 x y^2)
    """
    z = np.asarray(z, dtype=float)
    x = z[..., 0]
    y = z[..., 1]
    return eta * x * y + (gamma / 3.0) * (x**3 - 3.0 * x * y**2)


def grad_H(z: np.ndarray, eta: float = 0.75, gamma: float = 0.04) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    x = z[..., 0]
    y = z[..., 1]
    gx = eta * y + gamma * (x**2 - y**2)
    gy = eta * x - 2.0 * gamma * x * y
    return np.stack([gx, gy], axis=-1)


def J_apply(v: np.ndarray) -> np.ndarray:
    v = np.asarray(v, dtype=float)
    return np.stack([-v[..., 1], v[..., 0]], axis=-1)


def kahler_bracket(z: np.ndarray, alpha: float = 1.0, beta: float = 0.18, eta: float = 0.75, gamma: float = 0.04) -> np.ndarray:
    gI = grad_info(z, alpha=alpha, beta=beta)
    gH = grad_H(z, eta=eta, gamma=gamma)
    return np.sum(gI * J_apply(gH), axis=-1)


def kahler_flow(z: np.ndarray, alpha: float = 1.0, beta: float = 0.18, eta: float = 0.75, gamma: float = 0.04) -> np.ndarray:
    gI = grad_info(z, alpha=alpha, beta=beta)
    gH = grad_H(z, eta=eta, gamma=gamma)
    return -gI + J_apply(gH)


def integrate_flow(z0: Sequence[float], *, n_steps: int = 2500, dt: float = 0.05, alpha: float = 1.0, beta: float = 0.18, eta: float = 0.75, gamma: float = 0.04) -> np.ndarray:
    z = np.zeros((n_steps + 1, 2), dtype=float)
    z[0] = np.asarray(z0, dtype=float)
    for n in range(n_steps):
        k1 = kahler_flow(z[n], alpha=alpha, beta=beta, eta=eta, gamma=gamma)
        k2 = kahler_flow(z[n] + 0.5 * dt * k1, alpha=alpha, beta=beta, eta=eta, gamma=gamma)
        k3 = kahler_flow(z[n] + 0.5 * dt * k2, alpha=alpha, beta=beta, eta=eta, gamma=gamma)
        k4 = kahler_flow(z[n] + dt * k3, alpha=alpha, beta=beta, eta=eta, gamma=gamma)
        z[n + 1] = z[n] + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return z


def chirality_from_holonomy(path: np.ndarray) -> int:
    x = np.asarray(path[:, 0], dtype=float)
    y = np.asarray(path[:, 1], dtype=float)
    area = 0.5 * np.sum(x[:-1] * y[1:] - y[:-1] * x[1:])
    return int(np.sign(area)) if area != 0 else 0


def event_measure(values: Sequence[float], threshold: float = 1e-4) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    d = np.diff(values)
    return np.where(np.abs(d) >= threshold, d, 0.0)


def box_count_dimension(points: np.ndarray, epsilons: Iterable[float]) -> float:
    pts = np.asarray(points, dtype=float)
    mins = pts.min(axis=0)
    spans = pts.max(axis=0) - mins
    spans[spans == 0.0] = 1.0
    ptsn = (pts - mins) / spans
    xs, ys = [], []
    for eps in epsilons:
        if eps <= 0:
            continue
        bins = np.floor(ptsn / eps).astype(int)
        n_boxes = len({tuple(b) for b in bins})
        if n_boxes > 0:
            xs.append(math.log(1.0 / eps))
            ys.append(math.log(float(n_boxes)))
    if len(xs) < 2:
        return float('nan')
    A = np.vstack([xs, np.ones(len(xs))]).T
    m, _b = np.linalg.lstsq(A, np.asarray(ys), rcond=None)[0]
    return float(m)
