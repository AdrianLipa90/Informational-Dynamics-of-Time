from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence
import numpy as np

class ShannonRelativeInformationError(ValueError):
    pass

@dataclass(frozen=True)
class RelativeInformationStep:
    before_bits: float
    after_bits: float
    delta_bits: float
    stationary_defect: float


def _prob(v: Sequence[float], name: str, *, strictly_positive: bool=False) -> np.ndarray:
    p=np.asarray(v,dtype=float)
    if p.ndim!=1 or p.size<2 or not np.all(np.isfinite(p)):
        raise ShannonRelativeInformationError(f'{name} must be a finite probability vector')
    if strictly_positive:
        if np.any(p<=0): raise ShannonRelativeInformationError(f'{name} must be strictly positive')
    elif np.any(p<0):
        raise ShannonRelativeInformationError(f'{name} must be nonnegative')
    s=float(np.sum(p))
    if not math.isfinite(s) or abs(s-1.0)>1e-12:
        raise ShannonRelativeInformationError(f'{name} must sum to one')
    return p


def _kernel(P: Sequence[Sequence[float]]) -> np.ndarray:
    K=np.asarray(P,dtype=float)
    if K.ndim!=2 or K.shape[0]!=K.shape[1] or K.shape[0]<2 or not np.all(np.isfinite(K)):
        raise ShannonRelativeInformationError('kernel must be a finite square matrix')
    if np.any(K<0): raise ShannonRelativeInformationError('kernel must be nonnegative')
    if not np.allclose(K.sum(axis=1),1.0,rtol=0.0,atol=1e-12):
        raise ShannonRelativeInformationError('kernel rows must sum to one')
    return K


def shannon_bits(p: Sequence[float]) -> float:
    q=_prob(p,'p')
    nz=q>0
    return float(-np.sum(q[nz]*np.log2(q[nz])))


def kl_bits(p: Sequence[float], reference: Sequence[float]) -> float:
    q=_prob(p,'p'); r=_prob(reference,'reference',strictly_positive=True)
    if q.shape!=r.shape: raise ShannonRelativeInformationError('p and reference must have equal shape')
    nz=q>0
    return float(np.sum(q[nz]*np.log2(q[nz]/r[nz])))


def uniform_information_deficit_bits(p: Sequence[float]) -> float:
    q=_prob(p,'p')
    return float(math.log2(q.size)-shannon_bits(q))


def apply_kernel(p: Sequence[float], kernel: Sequence[Sequence[float]]) -> np.ndarray:
    q=_prob(p,'p'); K=_kernel(kernel)
    if K.shape[0]!=q.size: raise ShannonRelativeInformationError('kernel dimension must match p')
    out=q@K
    out=np.where(abs(out)<1e-15,0.0,out)
    return _prob(out,'updated_p')


def stationary_defect(reference: Sequence[float], kernel: Sequence[Sequence[float]]) -> float:
    r=_prob(reference,'reference',strictly_positive=True); K=_kernel(kernel)
    if K.shape[0]!=r.size: raise ShannonRelativeInformationError('kernel dimension must match reference')
    return float(np.linalg.norm(r@K-r,ord=1))


def relative_information_step(p: Sequence[float], reference: Sequence[float], kernel: Sequence[Sequence[float]], *, stationary_atol: float=1e-11) -> RelativeInformationStep:
    r=_prob(reference,'reference',strictly_positive=True); K=_kernel(kernel)
    defect=stationary_defect(r,K)
    if defect>float(stationary_atol):
        raise ShannonRelativeInformationError('reference must be stationary under kernel')
    before=kl_bits(p,r); after=kl_bits(apply_kernel(p,K),r)
    return RelativeInformationStep(before,after,after-before,defect)
