# 04A — Hyperbolic Coordinates from NOW to Bifurcation

Status: `CANDIDATE / NOW_TO_BIFURCATION_GATE_PASS`

This layer uses the same positive directed kinetic pair already present at the NOW boundary and rewrites it in coordinates adapted to the two adjacent dynamical layers.

For
\[
\mathfrak a=2M\cosh(A/2),
\qquad
\mathfrak j=2M\sinh(A/2),
\]
the exact invariant is
\[
\boxed{\mathfrak a^2-\mathfrak j^2=4M^2.}
\]
Hence
\[
\boxed{
M=\frac12\sqrt{\mathfrak a^2-\mathfrak j^2}.
}
\]
The same pair supplies the directed edge drive
\[
A=2\operatorname{artanh}\left(\frac{\mathfrak j}{\mathfrak a}\right).
\]
With
\[
\kappa=\frac{\ln2}{24\pi},
\qquad
\beta=\frac{\kappa A}{\ln2},
\]
we obtain
\[
\boxed{
\beta=\frac{1}{12\pi}
\operatorname{artanh}\left(\frac{\mathfrak j}{\mathfrak a}\right),
\qquad
A=24\pi\beta.
}
\]
Therefore the kinetic pair has the exact inverse parameterization
\[
\boxed{
\mathfrak a=2M\cosh(12\pi\beta),
\qquad
\mathfrak j=2M\sinh(12\pi\beta).
}
\]

## Typed decomposition

The invariant coordinate \(M\) is the edge coefficient entering the Temporal Wave stiffness
\[
K_M=D_L^\dagger\operatorname{diag}(M_e)D_L.
\]
The oriented coordinate \(\beta\) is the phase entering the unitary bifurcation family
\[
B_\phi(\beta)=e^{-i\beta G}.
\]
Thus the same observable pair \((\mathfrak a,\mathfrak j)\) separates into
\[
\boxed{
(\mathfrak a,\mathfrak j)
\longleftrightarrow
(M,\beta),
}
\]
where \(M\) carries the wave-magnitude channel and \(\beta\) carries the bifurcation-orientation channel.

Under current reversal
\[
\mathfrak j\mapsto-\mathfrak j,
\]
the two coordinates transform as
\[
M\mapsto M,
\qquad
\beta\mapsto-\beta.
\]
Consequently the Temporal Wave stiffness is preserved while the realized unitary bifurcation is inverted,
\[
B_\phi(-\beta)=B_\phi(\beta)^\dagger.
\]

## Wave-active bifurcation gate

The preceding NOW layer supplies the positive realization weight
\[
r_e^{(W)}=q_e\epsilon_e^{(W)}\ge0.
\]
The bifurcation gate uses the typed assignment
\[
\boxed{
r_e^{(W)}>0\Rightarrow B_e=B_\phi(\beta_e),}
\]
\[
\boxed{
r_e^{(W)}=0\Rightarrow B_e=I.}
\]
The realization weight therefore controls event admission, while \(\beta_e\) controls its directional unitary orientation. The magnitude channel \(M_e\) simultaneously remains available to the Temporal Wave operator.

For a general Hermitian generator \(G\),
\[
B_e=e^{-i\beta_e G}
\]
is unitary on every realized event. Current reversal maps the realized operator to its inverse.

## Numerical gate

A deterministic 10,000-case hyperbolic-coordinate probe over
\[
10^{-4}\le M\le50,
\qquad
-8\le A\le8
\]
returned maximum relative round-trip defects below \(2.3\times10^{-13}\) for the invariant mobility channel and below \(7\times10^{-14}\) for the drive/phase channel. Current reversal preserved \(M\) and reversed \(\beta\) exactly at machine representation in the declared probe.

Reference unitary checks returned inversion error below \(8\times10^{-18}\) and unitarity defect below \(6\times10^{-16}\).

GREMLIN v0.5 remained `CANDIDATE_ONLY`. It matched the typed decomposition

`TWO_COMPONENT_PAIR -> INVARIANT_MAGNITUDE_CHANNEL`

and

`TWO_COMPONENT_PAIR -> ORIENTATION_CHANNEL`

between the kinetic and Temporal-Wave/Bifurcation domains. The comparison returned `structurally_isomorphic=true`, SHA-256 `6c2987f83b4bc3e3379d2c71691753f60f5095fa23f026909baac85ee9aa6e72`.

Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `3/3`, `2/2`, and `1/1`.

Reference implementation: `src/idt/now_bifurcation_bridge.py`.
Reference tests: `tests/reference/test_now_bifurcation_bridge.py`.
