# 05B — Temporal Wave Smooth Transport from the Energy Metric

Status: `CANDIDATE / TEMPORAL_WAVE_TO_TRANSPORT_GATE_PASS`

The Temporal Wave layer supplies the stiffness and damping operators
\[
K=K_M\succeq0,
\qquad
C=C_\eta\succeq0.
\]
Using the phase-space state
\[
x=\begin{pmatrix}q\\p\end{pmatrix},
\]
and the sign convention already used by the wave reference implementation,
\[
\dot q=-p,
\qquad
\dot p=Kq-Cp,
\]
the smooth generator is
\[
\boxed{
A_W=
\begin{pmatrix}
0&-I\\
K&-C
\end{pmatrix}.
}
\]

## Energy metric and generator identity

Define
\[
\boxed{
Q_W=
\begin{pmatrix}
K&0\\
0&I
\end{pmatrix},
}
\]
so that
\[
\mathcal H_T(x)=\frac12x^\dagger Q_Wx
=\frac12q^\dagger Kq+\frac12p^\dagger p.
\]
A direct block calculation gives
\[
\boxed{
A_W^\dagger Q_W+Q_WA_W
=
\begin{pmatrix}
0&0\\
0&-2C
\end{pmatrix}
\preceq0.
}
\]
Thus the continuous Temporal Wave generator is dissipative with respect to its own energy form.  For a gapped wave operator $K\succ0$, $Q_W$ is a positive-definite metric.

## Cayley / implicit-midpoint segment

For an ordered increment $h>0$, define
\[
\boxed{
U_h^{(W)}
=\left(I-\frac h2A_W\right)^{-1}
 \left(I+\frac h2A_W\right).
}
\]
Let
\[
z=\frac{x_{n+1}+x_n}{2}.
\]
The Cayley update satisfies
\[
x_{n+1}-x_n=hA_Wz.
\]
Therefore
\[
\mathcal H_T(x_{n+1})-\mathcal H_T(x_n)
=\frac h2
z^\dagger(A_W^\dagger Q_W+Q_WA_W)z
\le0.
\]
Equivalently,
\[
\boxed{
(U_h^{(W)})^\dagger Q_WU_h^{(W)}\preceq Q_W.
}
\]
For $C=0$ this becomes the exact discrete conservation law
\[
\boxed{
(U_h^{(W)})^\dagger Q_WU_h^{(W)}=Q_W.
}
\]
The algebraic inverse of a finite Cayley segment is the opposite-step transform,
\[
(U_h^{(W)})^{-1}=U_{-h}^{(W)},
\]
whenever the declared linear solves are invertible.

## Energy-compatible bifurcation subclass

For a Hermitian bifurcation generator $G$, the sufficient compatibility condition
\[
\boxed{[G,Q_W]=0}
\]
gives
\[
B(\beta)=e^{-i\beta G},
\]
and
\[
\boxed{B(\beta)^\dagger Q_WB(\beta)=Q_W.}
\]
This supplies a tested event subclass that preserves the same wave-energy metric used by the smooth segment.

For one shared pair $(K,C)$ and a sequence of energy-compatible realized events,
\[
\mathcal U
=U_N^{(W)}B_N\cdots U_1^{(W)}B_1U_0^{(W)}
\]
therefore obeys
\[
\boxed{
\mathcal U^\dagger Q_W\mathcal U\preceq Q_W.
}
\]
The generic Temporal Transport operator contract remains available for events that exchange energy with the wave sector; the $Q_W$-compatible subclass provides the reference contraction closure inherited directly from Temporal Wave.

## Validation

A deterministic 1,000-case complex Hermitian stress probe returned:

- generator Lyapunov-identity maximum absolute defect: `9.036560719766055e-16`;
- maximum positive Cayley energy-growth eigenvalue: `2.788252038584075e-15`;
- conservative $Q_W$-unitarity maximum defect: `2.664535267923636e-15`;
- $Q_W$-compatible bifurcation maximum defect: `1.4210957137042335e-14`;
- composed smooth/event maximum positive energy-growth eigenvalue: `1.8887140887886513e-14`.

GREMLIN v0.5 remained `CANDIDATE_ONLY`.  The Temporal-Wave and Temporal-Transport typed graphs matched under

`LOCAL_DISSIPATIVE_GENERATOR -> POSITIVE_ENERGY_METRIC`

and

`LOCAL_DISSIPATIVE_GENERATOR -> CONTRACTIVE_EVOLUTION_SEGMENT`.

The comparison returned `structurally_isomorphic=true`, SHA-256 `ca5aba794968eec6b8d81a5e8a94cc066bf728ba70cf1d2caece06b90e478d93`.

Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `2/2`, `1/1`, and `3/3`.

Reference implementation: `src/idt/temporal_transport_wave.py`.
Reference tests: `tests/reference/test_temporal_transport_wave.py`.
