from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class RelationalTemporalForcingError(ValueError):
    pass


@dataclass(frozen=True)
class ResponseGeometryAudit:
    dimension: int
    scalar_pace: float
    dissipation_rate: float
    reversible_rate: float
    covariance_defect: float
    complex_structure_defect: float
    antisymmetry_defect: float


def _positive(value: float, name: str) -> float:
    x=float(value)
    if not math.isfinite(x) or x <= 0.0:
        raise RelationalTemporalForcingError(f"{name} must be finite and strictly positive")
    return x


def contextual_temporal_pace(activity: float, reference_activity: float) -> float:
    return _positive(activity, "activity") / _positive(reference_activity, "reference_activity")


def internal_elapsed_increment(activity: float, reference_activity: float, delta_lambda: float) -> float:
    return contextual_temporal_pace(activity, reference_activity) * _positive(delta_lambda, "delta_lambda")


def reparameterized_activity(activity: float, d_lambda_d_lambda_prime: float) -> float:
    return _positive(activity, "activity") * _positive(d_lambda_d_lambda_prime, "d_lambda_d_lambda_prime")


def canonical_complex_structure(dimension: int) -> np.ndarray:
    n=int(dimension)
    if n <= 0 or n % 2:
        raise RelationalTemporalForcingError("dimension must be a positive even integer")
    J=np.zeros((n,n), dtype=float)
    for i in range(0,n,2):
        J[i,i+1] = -1.0
        J[i+1,i] = 1.0
    return J


def _matrix(value: Sequence[Sequence[float]], name: str) -> np.ndarray:
    arr=np.asarray(value,dtype=float)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1] or not np.all(np.isfinite(arr)):
        raise RelationalTemporalForcingError(f"{name} must be a finite square matrix")
    return arr


def _covector(value: Sequence[float], dimension: int, name: str) -> np.ndarray:
    arr=np.asarray(value,dtype=float)
    if arr.shape != (dimension,) or not np.all(np.isfinite(arr)):
        raise RelationalTemporalForcingError(f"{name} must be a finite covector of length {dimension}")
    return arr


def response_flow(info_covector: Sequence[float], phase_covector: Sequence[float], mobility: Sequence[Sequence[float]], complex_structure: Sequence[Sequence[float]]) -> np.ndarray:
    G=_matrix(mobility, "mobility")
    J=_matrix(complex_structure, "complex_structure")
    if G.shape != J.shape:
        raise RelationalTemporalForcingError("mobility and complex_structure must have equal shape")
    n=G.shape[0]
    p=_covector(info_covector,n,"info_covector")
    h=_covector(phase_covector,n,"phase_covector")
    return -(G @ p) + J @ (G @ h)


def transformed_response_geometry(mobility: np.ndarray, complex_structure: np.ndarray, coordinate_map: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    G=_matrix(mobility,"mobility")
    J=_matrix(complex_structure,"complex_structure")
    A=_matrix(coordinate_map,"coordinate_map")
    if G.shape != J.shape or G.shape != A.shape:
        raise RelationalTemporalForcingError("all matrices must have equal shape")
    invA=np.linalg.inv(A)
    return A @ G @ A.T, A @ J @ invA


def audit_response_geometry(activity: float, reference_activity: float, info_covector: Sequence[float], phase_covector: Sequence[float], mobility: Sequence[Sequence[float]], complex_structure: Sequence[Sequence[float]], coordinate_map: Sequence[Sequence[float]]) -> ResponseGeometryAudit:
    alpha=contextual_temporal_pace(activity, reference_activity)
    G=_matrix(mobility,"mobility")
    J=_matrix(complex_structure,"complex_structure")
    A=_matrix(coordinate_map,"coordinate_map")
    if G.shape != J.shape or G.shape != A.shape:
        raise RelationalTemporalForcingError("all matrices must have equal shape")
    n=G.shape[0]
    p=_covector(info_covector,n,"info_covector")
    h=_covector(phase_covector,n,"phase_covector")
    if not np.allclose(G,G.T,rtol=0.0,atol=1e-12):
        raise RelationalTemporalForcingError("mobility must be symmetric")
    eig=np.linalg.eigvalsh(G)
    if float(np.min(eig)) <= 0.0:
        raise RelationalTemporalForcingError("mobility must be positive definite")
    omega_contra=J @ G
    antisym=float(np.linalg.norm(omega_contra + omega_contra.T,ord=np.inf))
    complex_def=float(np.linalg.norm(J@J + np.eye(n),ord=np.inf))
    v=response_flow(p,h,G,J)
    diss=float(p @ (-(G@p)))
    rev=float(h @ (J @ (G@h)))
    Gp,Jp=transformed_response_geometry(G,J,A)
    pp=np.linalg.solve(A.T,p)
    hp=np.linalg.solve(A.T,h)
    vp=response_flow(pp,hp,Gp,Jp)
    covariance=float(np.linalg.norm(vp - A@v))
    return ResponseGeometryAudit(n,alpha,diss,rev,covariance,complex_def,antisym)
