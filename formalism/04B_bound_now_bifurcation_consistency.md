# 04B — Bound NOW to Bifurcation Consistency

Status: `FORMAL_CANDIDATE / BOUND_NOW_BIFURCATION_CONSISTENCY_GATE`

This layer composes the realized-event/material NOW binding with the admitted hyperbolic bifurcation coordinates. The event occurrence, intrinsic temporal coordinate and material marker localize the update; the activity/current pair supplies its directional operator coordinate.

## 1. Bound NOW packet

For a serial realized history, let

\[
\mathcal N(D)=\{\nu_N\}
\]

be the unique supported maximal occurrence. The exchange-symmetric material binding supplies

\[
\boxed{
X_N:=\mathfrak B_{\rm NOW}^{(1/2)}(\nu_N)=X_{1/2}(\Theta_N)
}
\]

and the continuity law supplies its intrinsic velocity

\[
\boxed{
U_N:=D_\Theta X_N
=\frac{J}{\rho}\Big|_{X_N}
}
\]

on the zero-left-flux reference sector.

Define the localization packet

\[
\boxed{
\mathcal L_N=(\nu_N,\Theta_N,X_N,U_N).
}
\]

## 2. Realization consistency

04A uses the positive realization weight

\[
\boxed{
r_N^{(W)}=q_N\epsilon_N^{(W)}\ge0.
}
\]

The occurrence lineage stores the terminal event weight

\[
w_N^{\rm occ}>0.
\]

A bound bifurcation requires the realization identity

\[
\boxed{
w_N^{\rm occ}=r_N^{(W)}.}
\]

The material field supplied to the binding is evaluated at the same intrinsic temporal coordinate as the occurrence,

\[
\boxed{
\Theta_{\rm material}=\Theta_N.
}
\]

These equalities tie the event selected by relational precedence to the realization gate consumed by the bifurcation operator.

## 3. Directional bifurcation coordinate

At the selected occurrence carry the positive kinetic pair

\[
\mathfrak a_N>0,
\qquad
|\mathfrak j_N|<\mathfrak a_N.
\]

04A gives

\[
\boxed{
M_N=\frac12\sqrt{\mathfrak a_N^2-\mathfrak j_N^2},
}
\]

and

\[
\boxed{
\beta_N
=\frac{1}{12\pi}
\operatorname{artanh}\!\left(\frac{\mathfrak j_N}{\mathfrak a_N}\right).
}
\]

For a declared Hermitian generator \(G\),

\[
\boxed{
B_N=e^{-i\beta_NG}.
}
\]

The bound update is therefore represented by

\[
\boxed{
\mathfrak C_N
=\left(\mathcal L_N,r_N^{(W)},M_N,\beta_N,B_N\right).
}
\]

## 4. Localization–orientation factorization

The construction factorizes exactly as

\[
\boxed{
\begin{aligned}
(D,\prec_T,q_e;\rho,J)
&\longrightarrow
(\nu_N,\Theta_N,X_N,U_N),\\
(\mathfrak a_N,\mathfrak j_N)
&\longrightarrow
(M_N,\beta_N),\\
(q_N,\epsilon_N^{(W)})
&\longrightarrow
r_N^{(W)},\\
(\beta_N,G)
&\longrightarrow
B_N.
\end{aligned}
}
\]

The first line supplies occurrence and material localization. The second supplies wave magnitude and directional rapidity. The third verifies realization. The fourth constructs the event operator.

Consequently a translation of the material density at fixed occurrence and fixed kinetic pair changes \(X_N\) while preserving \(B_N\). A current reversal at fixed material density preserves \(X_N\) and \(M_N\), while

\[
\boxed{
\mathfrak j_N\mapsto-\mathfrak j_N
\Rightarrow
\beta_N\mapsto-\beta_N
\Rightarrow
B_N\mapsto B_N^\dagger.
}
\]

This is the localization/orientation independence control.

## 5. Event action

For the admitted realized occurrence,

\[
\boxed{
\Psi_T(\nu_N^+)=B_N\Psi_T(\nu_N^-).
}
\]

The material support coordinate carried with the event is

\[
\boxed{x_N=X_N.}
\]

Hence the update receipt records both occurrence identity and material localization,

```text
occurrence_prefix
terminal_edge_id
Theta_N
X_1/2(Theta_N)
U_1/2(Theta_N)
realization_weight
M_N
beta_N
operator_hash / operator payload
```

The occurrence prefix remains the lineage identity when state labels recur.

## 6. Concurrent frontier

For a concurrent NOW antichain

\[
\mathcal N(D)=\{\nu_b\}_{b\in\mathcal B},
\]

the binding is branchwise. Each branch carries

\[
\boxed{
\mathfrak C_b
=\left(
\nu_b,\Theta_b,X_{1/2}^{(b)},U_{1/2}^{(b)},
 r_b^{(W)},M_b,\beta_b,B_b
\right).
}
\]

This preserves all maximal occurrence identities and their branch-local material coordinates. Ordered composition of multiple branch operators is handled by the downstream transport/composition gate.

## 7. Immediate falsification gates

Reference tests require:

- the bound occurrence has positive terminal event weight;
- `terminal_event_weight == q_e * epsilon_e^(W)` within declared tolerance;
- material `Theta` equals occurrence `Theta` within declared tolerance;
- the stored material marker is the selected quantile front;
- `beta` equals the 04A hyperbolic coordinate from the supplied activity/current pair;
- the returned operator matches the existing `wave_active_bifurcation_operator`;
- translating the material density changes material position while preserving the operator for fixed event/kinetics;
- current reversal preserves material position and mobility while returning the adjoint operator;
- state-label recurrence preserves occurrence-prefix targeting;
- inconsistent realization or temporal coordinates fail closed.

Reference implementation: `src/idt/bound_now_bifurcation.py`.
Reference tests: `tests/reference/test_bound_now_bifurcation.py`.
Validation receipt: `validation/BOUND_NOW_BIFURCATION_CONSISTENCY_V0_1.json`.
