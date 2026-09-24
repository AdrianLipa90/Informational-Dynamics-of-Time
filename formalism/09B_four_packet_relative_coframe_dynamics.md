# 09B — Four-Packet Relative Coframe Dynamics

Status: `FORMAL_CANDIDATE / EXACT_RELATIVE_FRAME_DYNAMICS / PHYSICAL_RESPONSE_FUNCTIONALS_OPEN`

Date: 2026-09-24

## 1. Input from 01A

01A supplies the local relational response law

\[
\boxed{
\frac{dY^A}{d\lambda}
=
-G^{AB}\partial_B\mathcal I
+
J^A{}_C G^{CB}\partial_B\mathcal H.
}
\]

For four elapsed/Bloch packets, collect the sixteen real packet coordinates into

\[
Y\in\mathbb R^{16}.
\]

Reshape the corresponding four lifted packet vectors into a 4x4 frame

\[
E=[x_0\;x_1\;x_2\;x_3].
\]

Because reshaping is linear,

\[
\dot E
=
\operatorname{reshape}_{4\times4}(\dot Y).
\]

Thus the response law supplies a candidate frame velocity once \(G,J,\mathcal I,\mathcal H\) are admitted on the sixteen-dimensional packet manifold.

This gate does not select those physical response objects; it derives the relative geometry once their packet velocity is supplied.

## 2. Relative layer dynamics

Let two packet layers be

\[
E_A(\lambda),
\qquad
E_B(\lambda),
\]

with both frames invertible. Define

\[
\boxed{
e=E_BE_A^{-1}.
}
\]

Define the left-trivialized frame generators

\[
\boxed{
L_A=\dot E_AE_A^{-1},
\qquad
L_B=\dot E_BE_B^{-1}.
}
\]

Direct differentiation gives

\[
\boxed{
\dot e
=
L_Be-eL_A.
}
\]

This is an exact two-sided relative-frame flow.

It is the natural dynamic version of the TIR moire/coframe variable.

## 3. Common-frame covariance

If both layers receive the same left frame transformation

\[
E_s\mapsto S(\lambda)E_s,
\]

then

\[
e\mapsto SeS^{-1}.
\]

Thus a common change of external frame acts by conjugation. The matrix entries of \(e\) are not themselves gauge invariants; conjugacy- or metric/curvature-based downstream observables are required.

For identical infinitesimal left generator \(L\),

\[
\dot e=[L,e].
\]

In particular, if \(e=I\), common motion leaves the relative state fixed.

## 4. 36D exterior-square dynamics

Let

\[
B=C_2(e)=\Lambda^2e.
\]

The differential exterior-square representation

\[
\rho=d(\Lambda^2):
\mathfrak{gl}(4)\to\mathfrak{co}(3,3)
\]

then gives

\[
\boxed{
\dot B
=
\rho(L_B)B
-
B\rho(L_A).
}
\]

Equivalently,

\[
C_2(E_BE_A^{-1})
=
C_2(E_B)C_2(E_A)^{-1}.
\]

Therefore the 36-coefficient hyperlayer dynamics is generated functorially from the four-packet frame dynamics. No anonymous T36 coordinate assignment is required.

## 5. Path-ordered solution and memory crosswalk

If

\[
\dot E_s=L_sE_s,
\]

write the path-ordered propagator

\[
U_s(\lambda,\lambda_0)
=
\mathcal T
\exp\int_{\lambda_0}^{\lambda}L_s(\tau)d\tau.
\]

Then

\[
E_s(\lambda)=U_sE_s(\lambda_0),
\]

and the relative operator is

\[
\boxed{
e(\lambda)
=
U_B(\lambda,\lambda_0)
e(\lambda_0)
U_A(\lambda,\lambda_0)^{-1}.
}
\]

When generators at different parameter values do not commute, path ordering is essential. This provides an exact mathematical history dependence compatible with the TIR holonomy-memory definition.

It is not by itself evidence that physical spacetime stores memory.

## 6. Gravity firewall

The exact relative dynamics closes a kinematic/dynamical representation gate, not Einstein dynamics.

Still required:

1. an admitted physical \(16\)-dimensional packet response geometry \(G\);
2. physical informational/phase functionals \(\mathcal I,\mathcal H\);
3. proof that packet evolution preserves the admitted future-cone/frame domain;
4. spatial dependence and gluing of the local packet frames;
5. construction of the Levi-Civita/spin connection from the resulting coframe;
6. nonzero gauge-invariant curvature;
7. source normalization and gravitational phenomenology.

Using the Einstein-Hilbert action to choose these objects would be a downstream cross-check, not a pre-geometric derivation.

## 7. Exact validation

The reference implementation checks:

- direct differentiation of \(E_BE_A^{-1}\) against \(L_Be-eL_A\);
- direct differentiation of \(C_2(e)\) against \(\rho(L_B)B-B\rho(L_A)\);
- multiplicativity of the exterior-square representation;
- common-left-flow conjugation;
- numerical residuals at machine precision.

Reference implementation:

`src/idt/relative_coframe_dynamics.py`

Reference tests:

`tests/reference/test_relative_coframe_dynamics.py`
