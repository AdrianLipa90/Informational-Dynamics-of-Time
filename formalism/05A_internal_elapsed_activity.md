# 05A — System-Internal Elapsed Activity

Status: `FORMAL_CANDIDATE_WITH_PROVED_STRUCTURAL_IDENTITIES`

The positive temporal activity field supplies a system-internal elapsed coordinate before metric clock calibration is introduced.

Let \(\lambda\) be an admissible increasing ordering parameter, let \(\mathfrak a(\lambda)>0\) be realized temporal activity, and choose a strictly positive system-internal reference activity \(\mathfrak a_\star\). Define
\[
\boxed{
d\tau_{\rm int}
=\frac{\mathfrak a(\lambda)}{\mathfrak a_\star}\,d\lambda.
}
\]
For a discrete ordered path,
\[
\boxed{
\tau_{{\rm int},N}
=\sum_{n=0}^{N-1}
\frac{\mathfrak a_n}{\mathfrak a_\star}\,\Delta\lambda_n,
\qquad
\Delta\lambda_n>0.
}
\]
Because every admitted activity and ordering increment is positive, \(\tau_{\rm int}\) is strictly monotone along an admitted realized path.

## Reparameterization covariance

For an increasing relabeling \(\lambda'=f(\lambda)\), require activity to transform as a one-density,
\[
\mathfrak a'(\lambda')
=\mathfrak a(\lambda)\frac{d\lambda}{d\lambda'}.
\]
Then
\[
\boxed{
\mathfrak a'(\lambda')\,d\lambda'
=\mathfrak a(\lambda)\,d\lambda,
}
\]
and therefore \(d\tau_{\rm int}\) is invariant under the admitted relabeling.

## Density, viscosity and directional drive

Using the relational kinetic closure,
\[
\frac{d\tau_{\rm int}}{d\lambda}
=\frac{2M}{\mathfrak a_\star}\cosh(A/2),
\qquad
M=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12(\eta_R(a)+\eta_R(b))}.
\]
Thus relational density raises the internal activity pace, relational viscosity lowers it, and the magnitude of the antisymmetric drive raises activity through an even function. Edge reversal \(A\mapsto -A\) leaves elapsed activity unchanged while reversing the directed current.

Formalism 01A identifies
\[
\boxed{\phi=\mathfrak a/\mathfrak a_\star}
\]
as the forced positive scalar pace for a context-sensitive internal elapsed measure. Calibration against biological, cognitive and physical clock observables is a downstream validation program.
