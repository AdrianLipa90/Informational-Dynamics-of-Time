# 06G — Temporal Transport to Memory Admission Bridge

Status: `CANDIDATE / TRANSPORT_TO_MEMORY_TARGETED_PASS`

This layer closes the declared parent boundary

\[
\mathrm{Temporal\ Transport}\rightarrow\mathrm{Memory}
\]

using only quantities already available upstream.

## 1. Internal elapsed increment inherited from transport

Let one smooth Temporal Transport segment carry an ordered increment
\[
h_n=\Delta\lambda_n>0
\]
and let the positive kinetic activity on the realized path be \(\mathfrak a_n>0\).  With the existing system-internal reference activity \(\mathfrak a_\star>0\), define
\[
\boxed{
\Delta\tau_n
=\frac{\mathfrak a_n}{\mathfrak a_\star}\Delta\lambda_n.
}
\]
Under an increasing relabeling \(\lambda'=f(\lambda)\),
\[
\mathfrak a'_n=\frac{\mathfrak a_n}{f'(\lambda_n)},
\qquad
\Delta\lambda'_n=f'(\lambda_n)\Delta\lambda_n,
\]
so
\[
\boxed{\Delta\tau'_n=\Delta\tau_n.}
\]
The Memory smooth-segment duration is therefore inherited from the same ordered segment already used by Temporal Transport.

## 2. Wave-active realization gate

The preceding NOW bridge supplies
\[
q_n\ge0,
\qquad
\epsilon_n^{(W)}\ge0,
\qquad
r_n^{(W)}=q_n\epsilon_n^{(W)}.
\]
Define the exact realization indicator
\[
\boxed{
g_n=\mathbf 1\!\left[r_n^{(W)}>0\right].
}
\]
The Memory event receipt is then
\[
\boxed{
\mathcal E_n^{T\to M}
=\left(
\Delta\tau_n,
 g_nq_n,
 \delta m_n
\right).
}
\]
The resulting normalized kick is
\[
\boxed{
\Delta v_{M,n}
=g_nq_n\delta m_n.
}
\]
Thus Temporal Wave activation controls event realization, while the previously derived structural event signature \(q_n\) remains the event amplitude.  No second gain parameter is introduced.

If \(q_n=0\) or \(\epsilon_n^{(W)}=0\), then
\[
g_n=0,
\qquad
\Delta v_{M,n}=0,
\]
while \(\Delta\tau_n>0\) can still advance the smooth Memory segment.  This matches the existing zero-weight Memory receipt control.

## 3. Normalization negative gate

Under a nonzero global rescaling of the Temporal Wave amplitude,
\[
\Phi\mapsto c\Phi,
\]
the edge activation transforms as
\[
\epsilon_n^{(W)}\mapsto |c|^2\epsilon_n^{(W)}.
\]
For \(c\neq0\), its positive support is unchanged, hence
\[
g_n\mapsto g_n.
\]
Consequently the admitted Memory kick above is unchanged.

By contrast, using
\[
q_n\epsilon_n^{(W)}
\]
as the Memory kick amplitude would give
\[
\Delta v_{M,n}\mapsto |c|^2\Delta v_{M,n}
\]
under the same wave-amplitude rescaling.  The current upstream stack has no canonical physical normalization that would justify this extra amplitude dependence.  Therefore the candidate assignment

\[
\boxed{
\text{Memory gain}=q_n\epsilon_n^{(W)}
}
\]
receives the scoped verdict

`BLOCKED_NORMALIZATION_DEPENDENT`.

The product \(q_n\epsilon_n^{(W)}\) remains retained as the positive NOW realization weight and provenance field.

## 4. Compatibility with the existing Memory cell

The existing Memory receipt type is
\[
\mathcal E_n=(\Delta\tau_n,q_n,\delta m_n).
\]
The transport-derived receipt has the same typed structure, with the event amplitude replaced only by the admitted gated value \(g_nq_n\).  It can therefore be consumed directly by the existing lineage cell
\[
\mathcal C_n
=\Phi_K(\Delta\tau_n;\mu_M)\circ K_{\mathcal E_n}
\]
and by the declared reverse cell in reverse chronology.

A deterministic 5,000-case probe returned:

- maximum reparameterized \(\Delta\tau\) defect: `1.7763568394002505e-15`;
- maximum kick-identity defect: `0.0`;
- wave-rescaling gate failures: `0`;
- zero-gate failures: `0`;
- active cases: `4277`;
- product-amplitude normalization-sensitive cases: `4277/4277`;
- maximum forward/reverse lineage reconstruction defect: `4.868520327566372e-13`.

GREMLIN v0.5 remained `CANDIDATE_ONLY`.  The transport-derived receipt and existing Memory receipt matched under the typed relation structure

`POSITIVE_DURATION + NONNEGATIVE_EVENT_AMPLITUDE + IMPRINT_DIRECTION -> TYPED_MEMORY_RECEIPT`.

The comparison returned `structurally_isomorphic=true`, SHA-256 `6ecebd1f89e4aeb37cf701a348f42c326275c663ab18c49918d44dca4c236fe8`.

Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `3/3`, `2/2`, and `1/1`.

Reference implementation: `src/idt/memory_transport_bridge.py`.
Reference tests: `tests/reference/test_memory_transport_bridge.py`.
