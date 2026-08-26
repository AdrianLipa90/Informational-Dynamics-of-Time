# 06F — CPn Kähler Memory Frame

Status: `MEMORY_FRONTIER_CANDIDATE / HIGHER_DIMENSIONAL_KÄHLER_FRAME_REFERENCE_SUBCLASS`

This layer extends the geometry-derived memory frame from \(\mathbb{CP}^1\) to finite-dimensional pure-state projective Hilbert spaces \(\mathbb{CP}^{d-1}\). It preserves the previously admitted two-real-dimensional memory plane as one selected complex tangent line while exposing the orthogonal tangent residual explicitly.

## T019O — Fubini–Study logarithm in \(\mathbb{CP}^{d-1}\)

Let \(|\psi\rangle,|\phi\rangle\) be normalized non-orthogonal pure-state representatives and define
\[
z=\langle\psi|\phi\rangle,
\qquad
c=|z|,
\qquad
\theta=\arccos c.
\]
Phase-align the target ray to the anchor,
\[
|\widetilde\phi\rangle=e^{-i\arg z}|\phi\rangle,
\qquad
\langle\psi|\widetilde\phi\rangle=c.
\]
For \(0<\theta<\pi/2\), define the horizontal unit tangent
\[
|u\rangle
=\frac{|\widetilde\phi\rangle-c|\psi\rangle}{\sin\theta}
\]
and the Fubini--Study logarithm
\[
\boxed{|\xi^{FS}_{\psi\to\phi}\rangle=\theta|u\rangle.}
\]
Then
\[
\langle\psi|u\rangle=0,
\qquad
\boxed{\|\xi^{FS}_{\psi\to\phi}\|=d_{FS}(\psi,\phi)=\arccos|\langle\psi|\phi\rangle|.}
\]
Orthogonal rays are the reference cut locus and fail closed because the shortest projective geodesic phase is ambiguous there.

## T019P — selected Kähler memory line and residual

Choose the first admitted nonzero tangent direction as
\[
|e_Q\rangle=|u_{\rm ref}\rangle,
\qquad
\boxed{|e_P\rangle=J|e_Q\rangle=i|e_Q\rangle.}
\]
Using the real Fubini--Study tangent metric
\[
g(v,w)=\operatorname{Re}\langle v|w\rangle,
\]
project a later logarithmic displacement \(|\xi\rangle\) to the selected memory plane by
\[
\boxed{
\delta m
=g(e_Q,\xi)+i\,g(e_P,\xi).
}
\]
The orthogonal tangent residual is
\[
\boxed{
r_\perp
=\sqrt{d_{FS}^2-|\delta m|^2},
}
\]
so the exact reference decomposition is
\[
\boxed{
d_{FS}^2=|\delta m|^2+r_\perp^2.
}
\]
For \(\mathbb{CP}^1\), the tangent space has one complex dimension and \(r_\perp=0\), recovering the earlier identity \(|\delta m|=d_{FS}\). In higher dimensions, \(r_\perp\) records event displacement outside the selected complex memory line rather than discarding that norm silently.

## T019Q — finite-dimensional geodesic frame transport

Along the selected shortest geodesic, let
\[
s=\sin\theta,
\qquad
|\widetilde\phi\rangle=c|\psi\rangle+s|u\rangle.
\]
Define the complex-linear isometry \(U_{\phi\leftarrow\psi}\) by
\[
U|\psi\rangle=|\widetilde\phi\rangle,
\qquad
U|u\rangle=-s|\psi\rangle+c|u\rangle,
\]
and let \(U\) act as the identity on the orthogonal complement of \(\operatorname{span}_{\mathbb C}\{\psi,u\}\).

The transported memory dyad is
\[
\boxed{
|e_Q'\rangle=U|e_Q\rangle,
\qquad
|e_P'\rangle=U|e_P\rangle.
}
\]
Because \(U\) is complex-linear and unitary on the declared decomposition,
\[
\langle\widetilde\phi|e_Q'\rangle
=\langle\widetilde\phi|e_P'\rangle=0,
\]
\[
\|e_Q'\|=\|e_P'\|=1,
\qquad
\boxed{e_P'=i e_Q'.}
\]
The reference implementation also verifies the forward/backward transport round trip up to the common phase of the endpoint ray.

## Relation to the Memory admission gate

The existing Memory admission path uses the \(\mathbb{CP}^1\) subclass, where the entire tangent displacement lies in the selected complex memory line. The \(\mathbb{CP}^{d-1}\) extension provides the higher-dimensional continuation and a typed residual channel \(r_\perp\). Promotion of additional residual channels into the orbital memory state requires a later explicit model contract.

Reference controls are recorded in `validation/KAHLER_MEMORY_FRAME_CPN_V0_1.json`.
