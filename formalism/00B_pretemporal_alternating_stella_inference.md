# 00B — Pretemporal Alternating Stella Inference

Status: EXACT_DECORATED_HALFSTEP / TIR_RELABELING_INVARIANT_SIGNATURE_INTERFACE / NO_BACKGROUND_TIME

Date: 2026-09-28

## 1. Position in IDT

00A established the abstract two-sector carrier and

\[
H^2=S.
\]

00B decorates each sector with an internal tetrahedral orientation state supplied by the TIR Stella interface.

No temporal coordinate is introduced. The word alternating means ordered composition of transformations.

## 2. Decorated state

Use

\[
\widetilde X=(n,\sigma,A,B),
\]

where

\[
(n,\sigma)\in\mathbb N_0\times\mathbb Z_2
\]

is the 00A carrier and \(A,B\) are internal orientation lifts for the two Stella sectors.

For admitted transformations \(R_+,R_-\), define

\[
\widetilde H(n,0,A,B)
=
(n,1,R_+A,B),
\]

\[
\widetilde H(n,1,A,B)
=
(n+1,0,A,R_-B).
\]

Define

\[
\widetilde S(n,\sigma,A,B)
=
(n+1,\sigma,R_+A,R_-B).
\]

Then

\[
\boxed{\widetilde H^2=\widetilde S.}
\]

Projection onto the first two coordinates yields exactly the 00A identity

\[
\boxed{H^2=S.}
\]

## 3. TIR inference payload

TIR supplies the label-free cross-sector signature

\[
\mathcal I(A,B)
=
\{\!\{-n_i^TA^TBn_j\}\!\}_{i,j=1}^{4},
\]

with the tetrahedral vectors normalized so that \(n_i\cdot n_i=1\).

For independent tetrahedral relabelings \(a,b\in A_4\),

\[
\boxed{
\mathcal I(Aa,Bb)=\mathcal I(A,B).
}
\]

Therefore the payload passed into IDT does not depend on the arbitrary names assigned to the four vertices.

IDT consumes the ordered sequence

\[
\boxed{
\mathcal I_0\to\mathcal I_1\to\mathcal I_2\to\cdots
}
\]

as a pretemporal inference orbit.

## 4. Relation to the half grading

The existing grade

\[
g(n,\sigma)=n+\frac{\sigma}{2}
\]

is unchanged:

\[
g(Hx)-g(x)=\frac12.
\]

The new orientation/inference payload does not create this half. It decorates each half-step with relational content.

Hence

\[
\boxed{
\text{half-grade}
=
\text{sector alternation},
}
\]

while

\[
\boxed{
\text{inference content}
=
\text{change of the label-free Stella signature}.
}
\]

These are coupled but separately typed statements.

## 5. Hilbert chain

The coarse projection remains

\[
1\,|\,12\,|\,23\,|\,34\,|\,45\,|\cdots
\]

and the unilateral shift remains

\[
S_{\mathbb N}:n\mapsto n+1.
\]

Thus the decorated construction has the hierarchy

\[
\boxed{
\text{Stella relation}
\to
\text{alternating orientation transform}
\to
\text{label-free inference signature orbit}
\to
H^2=S
\to
\text{serial order}
\to
\text{00E duration}
\to
\text{00F temporal precedence}.
}
\]

No physical clock is needed upstream of this chain.

## 6. Pre-spacetime firewall

At 00B:

- the sphere is an internal state/symmetry representation;
- the tetrahedra are relational frames, not objects moving in physical three-space;
- \(R_+\) and \(R_-\) are abstract composable transformations, not angular velocities;
- the index \(n\) is a successor label, not time;
- the value \(1/2\) is a normalized grading, not half of an assumed duration.

Physical space and calibrated time remain downstream bindings.

## 7. Status

| Statement | Status |
|---|---|
| decorated half-step definition | EXACT |
| \(\widetilde H^2=\widetilde S\) | EXACT |
| projection to 00A \(H^2=S\) | EXACT |
| TIR overlap signature label invariance | IMPORTED EXACT TIR RESULT |
| inference orbit is pretemporal | TYPE FIREWALL |
| physical spacetime derived completely here | NOT CLAIMED |

TIR source:

The-Fundamental-Theory-of-Informational-Relations/TIR/foundations/TIR_STELLA_ALTERNATING_ROTATION_INFERENCE_V0_1.md
