# 05 — Temporal Transport Closure

Status: `STRUCTURAL_REFERENCE_GATE_PASS_CANDIDATE`

The ordered interrupted propagator is
\[
\boxed{\mathcal U_{f\leftarrow i}=U_NB_NU_{N-1}B_{N-1}\cdots U_1B_1U_0.}
\]
Chronological multiplication order is part of the operator contract.

## Norm bound

For the spectral norm,
\[
\|\mathcal U_{f\leftarrow i}\|_2
\le \prod_{k=0}^{N}\|U_k\|_2\prod_{n=1}^{N}\|B_n\|_2.
\]
For unitary smooth segments and the reference polar event class
\(B_n=e^{-q_nD_n}e^{-i\beta_nG_n}\) with \(D_n\succeq0\) and \(q_n\ge0\),
\[
\boxed{\|\mathcal U_{f\leftarrow i}\|_2\le1.}
\]

## Algebraic invertibility and conditioning

For finite \(q_n\) and finite Hermitian generators, both exponential factors are invertible, hence every finite ordered product is algebraically invertible. Numerical reconstruction is tracked separately by the condition number
\[
\kappa_2(\mathcal U)=\|\mathcal U\|_2\|\mathcal U^{-1}\|_2.
\]
The reference tests include an invertible propagator with large \(\kappa_2\), establishing the distinction between existence of an inverse and stable reconstruction.

## Exact cut identity

For any cut after the first \(c\) events,
\[
\boxed{\mathcal U_{f\leftarrow i}=\mathcal U_{f\leftarrow c}\,\mathcal U_{c\leftarrow i}.}
\]
The two factors preserve the same chronological order as the uncut propagator. Cuts at \(c=0\) and \(c=N\) are included in the reference test.

## Gate

The Transport gate is structurally closed when the existing order/noncommutation controls and the three controls above pass together. The next dependency node is Memory.
