from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Sequence
import numpy as np

class ShannonOnsagerError(ValueError):
    pass

@dataclass(frozen=True)
class OnsagerAudit:
    factorization_defect: float
    symmetry_defect: float
    min_eigenvalue: float
    mass_null_defect: float
    dissipation_rate_bits: float
    detailed_balance_defect: float


def logarithmic_mean(x: float, y: float) -> float:
    a=float(x); b=float(y)
    if not (math.isfinite(a) and math.isfinite(b) and a>0 and b>0):
        raise ShannonOnsagerError('logarithmic mean inputs must be finite and positive')
    if abs(a-b) <= 1e-12*max(a,b):
        return 0.5*(a+b)
    return (a-b)/(math.log(a)-math.log(b))


def _prob(v: Sequence[float], name: str, positive: bool=True) -> np.ndarray:
    a=np.asarray(v,dtype=float)
    if a.ndim!=1 or a.size<2 or not np.all(np.isfinite(a)):
        raise ShannonOnsagerError(f'{name} must be a finite vector')
    if positive and np.any(a<=0): raise ShannonOnsagerError(f'{name} must be strictly positive')
    if not positive and np.any(a<0): raise ShannonOnsagerError(f'{name} must be nonnegative')
    if abs(float(a.sum())-1.0)>1e-12: raise ShannonOnsagerError(f'{name} must sum to one')
    return a


def _generator(Q: Sequence[Sequence[float]]) -> np.ndarray:
    A=np.asarray(Q,dtype=float)
    if A.ndim!=2 or A.shape[0]!=A.shape[1] or A.shape[0]<2 or not np.all(np.isfinite(A)):
        raise ShannonOnsagerError('generator must be a finite square matrix')
    row_def=np.abs(A.sum(axis=1))
    row_scale=np.maximum(1.0,np.sum(np.abs(A),axis=1))
    if np.any(row_def > 1e-12*row_scale):
        raise ShannonOnsagerError('generator rows must sum to zero')
    off=A.copy(); np.fill_diagonal(off,0.0)
    if np.any(off < -1e-14): raise ShannonOnsagerError('generator off-diagonal rates must be nonnegative')
    return A


def detailed_balance_conductance(pi: Sequence[float], Q: Sequence[Sequence[float]], *, atol: float=1e-11) -> np.ndarray:
    r=_prob(pi,'pi'); A=_generator(Q); n=r.size
    if A.shape!=(n,n): raise ShannonOnsagerError('dimension mismatch')
    C=np.zeros_like(A)
    for i in range(n):
        for j in range(i+1,n):
            cij=r[i]*A[i,j]; cji=r[j]*A[j,i]
            if abs(cij-cji)>atol:
                raise ShannonOnsagerError('generator must satisfy detailed balance with pi')
            c=0.5*(cij+cji)
            C[i,j]=C[j,i]=c
    return C


def incidence_from_conductance(C: np.ndarray) -> tuple[np.ndarray,np.ndarray]:
    C=np.asarray(C,dtype=float); n=C.shape[0]
    rows=[]; weights=[]
    for i in range(n):
        for j in range(i+1,n):
            if C[i,j] > 0:
                row=np.zeros(n); row[i]=-1.0; row[j]=1.0
                rows.append(row); weights.append(C[i,j])
    if not rows: raise ShannonOnsagerError('connected response requires at least one positive edge')
    return np.vstack(rows), np.asarray(weights)


def kl_gradient_bits(p: Sequence[float], pi: Sequence[float]) -> np.ndarray:
    q=_prob(p,'p'); r=_prob(pi,'pi')
    if q.shape!=r.shape: raise ShannonOnsagerError('dimension mismatch')
    return (np.log(q/r)+1.0)/math.log(2.0)


def shannon_onsager_tensor_bits(p: Sequence[float], pi: Sequence[float], Q: Sequence[Sequence[float]]) -> np.ndarray:
    q=_prob(p,'p'); r=_prob(pi,'pi'); A=_generator(Q)
    C=detailed_balance_conductance(r,A)
    D,c=incidence_from_conductance(C)
    ratio=q/r
    lm=np.empty(len(c))
    for e,row in enumerate(D):
        i=int(np.where(row<0)[0][0]); j=int(np.where(row>0)[0][0])
        lm[e]=logarithmic_mean(ratio[i],ratio[j])
    return math.log(2.0) * (D.T @ np.diag(c*lm) @ D)


def master_velocity(p: Sequence[float], Q: Sequence[Sequence[float]]) -> np.ndarray:
    q=_prob(p,'p'); A=_generator(Q)
    if A.shape[0]!=q.size: raise ShannonOnsagerError('dimension mismatch')
    return q@A


def audit_onsager_factorization(p: Sequence[float], pi: Sequence[float], Q: Sequence[Sequence[float]]) -> OnsagerAudit:
    q=_prob(p,'p'); r=_prob(pi,'pi'); A=_generator(Q)
    G=shannon_onsager_tensor_bits(q,r,A); grad=kl_gradient_bits(q,r); v=master_velocity(q,A)
    pred=-(G@grad)
    db=float(np.max(np.abs(r[:,None]*A - r[None,:]*A.T)))
    eig=np.linalg.eigvalsh(0.5*(G+G.T))
    return OnsagerAudit(
        factorization_defect=float(np.linalg.norm(v-pred)),
        symmetry_defect=float(np.linalg.norm(G-G.T,ord=np.inf)),
        min_eigenvalue=float(np.min(eig)),
        mass_null_defect=float(np.linalg.norm(G@np.ones(q.size))),
        dissipation_rate_bits=float(grad@v),
        detailed_balance_defect=db,
    )


def symmetric_generator_from_mobility(M: Sequence[Sequence[float]]) -> np.ndarray:
    W=np.asarray(M,dtype=float)
    if W.ndim!=2 or W.shape[0]!=W.shape[1] or W.shape[0]<2 or not np.all(np.isfinite(W)):
        raise ShannonOnsagerError('mobility matrix must be finite square')
    if not np.allclose(W,W.T,rtol=0.0,atol=1e-12): raise ShannonOnsagerError('mobility must be symmetric')
    if np.any(W<0): raise ShannonOnsagerError('mobility must be nonnegative')
    W=W.copy(); np.fill_diagonal(W,0.0)
    Q=W.copy(); np.fill_diagonal(Q,-W.sum(axis=1))
    return Q


def graph_stiffness(M: Sequence[Sequence[float]]) -> np.ndarray:
    W=np.asarray(M,dtype=float).copy(); np.fill_diagonal(W,0.0)
    return np.diag(W.sum(axis=1))-W
