# 00D — Memory-Orbit Drive

Status: `FORMAL_CANDIDATE_WITH_PROVED_STRUCTURAL_IDENTITIES`

The density/viscosity layer separates scalar mobility from directional affinity. This layer introduces the first explicit candidate for a non-exact antisymmetric edge drive using an oriented memory-orbit coordinate.

Let each admitted relational state carry a complex memory coordinate
\[
m(s)=x_M(s)+i y_M(s)=r_M(s)e^{i\theta_M(s)}.
\]
For an edge \(a\to b\), define
\[
\boxed{
A^{(M)}_{ab}
=\lambda_M\operatorname{Im}\!\left[m(a)^*m(b)\right]
=\lambda_M r_a r_b\sin(\theta_b-\theta_a),
}
\]
where \(\lambda_M\) is a declared dimensionless coupling.

## Theorem T009B — antisymmetry

\[
A^{(M)}_{ba}=-A^{(M)}_{ab}.
\]
Thus the construction is immediately admissible as the antisymmetric drive in the relational kinetic pair
\[
W_{a\to b}=M_{ab}e^{A^{(M)}_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A^{(M)}_{ab}/2}.
\]

## Theorem T009C — closed memory-orbit circulation equals oriented polygon area

For a closed sequence of memory coordinates \(m_0,\ldots,m_{N-1}\),
\[
\sum_{n=0}^{N-1}A^{(M)}_{n,n+1}
=\lambda_M\sum_{n=0}^{N-1}(x_n y_{n+1}-y_n x_{n+1}),
\]
with cyclic indexing. By the shoelace identity,
\[
\boxed{
\sum_C A^{(M)}_e
=2\lambda_M\,\mathcal A_M(C),
}
\]
where \(\mathcal A_M(C)\) is the signed area enclosed by the polygonal memory orbit in the \((x_M,y_M)\) plane.

Therefore the memory-orbit drive is generally non-exact: a loop enclosing non-zero oriented memory area retains a non-zero cycle drive. Reversing the loop orientation reverses its sign.

## Degenerate control

If all memory coordinates lie on one ray through the origin, then every pair has zero imaginary cross term and
\[
A^{(M)}_{ab}=0.
\]
The drive therefore requires oriented memory geometry rather than memory magnitude alone.

## Candidate implication for temporal affinity

Using the directed-transition affinity layer,
\[
\sigma^{(M)}_{ab}
=\frac{A^{(M)}_{ab}}{\ln2},
\]
and hence
\[
\mathcal A_C^{(M)}
=\frac{2\lambda_M}{\ln2}\,\mathcal A_M(C).
\]
This gives a concrete candidate mechanism by which an oriented memory orbit can contribute a non-zero path affinity while scalar relational density and viscosity continue to control transition mobility.

This result is a mathematical construction within the model. Its identification with physical memory or a physical arrow of time requires an independent evidence path.
