# 02JP — NOW Material Quantile Realization Binding

Status: `FORMAL_CANDIDATE / REALIZED_EVENT_TO_MATERIAL_FRONT_BINDING_GATE`

02JO supplies a continuum family of material Temporal Wave markers \(X_q(\Theta)\). The relational-precedence layer supplies the realized-event NOW frontier \(\mathcal N(D)=\operatorname{Max}_{\prec_T}(D_q)\). This gate gives the exact typed bridge between those two structures.

## 1. Material quantile family

For conserved temporal-wave mass

\[
M_T=\int\rho\,dx>0,
\]

define

\[
C(x,\Theta)=\frac1{M_T}\int_{x_L}^{x}\rho(y,\Theta)\,dy.
\]

For every

\[
q\in(0,1),
\]

the resolved positive-density sector carries a material marker

\[
\boxed{C(X_q(\Theta),\Theta)=q.}
\]

Under zero left-boundary flux,

\[
\boxed{
D_\Theta X_q
=\frac{J}{\rho}\Big|_{X_q}
=u(X_q,\Theta).
}
\]

Thus the wave sector supplies the entire equivariant family

\[
\boxed{\mathfrak X_\rho=\{X_q:q\in(0,1)\}.}
\]

## 2. Exchange involution and the symmetric selector

The first-distinction exchange acts on mass fractions by

\[
\boxed{\mathscr R(q)=1-q.}
\]

A selector invariant under this exchange satisfies

\[
q_*=\mathscr R(q_*)=1-q_*.
\]

Hence uniquely

\[
\boxed{q_*=\frac12.}
\]

The corresponding material marker is

\[
\boxed{X_{1/2}:\ C(X_{1/2},\Theta)=\frac12.}
\]

For a density symmetric about \(x=c\),

\[
\rho(c+\xi)=\rho(c-\xi),
\]

the quantile family obeys

\[
\boxed{X_{1-q}=2c-X_q,}
\]

and therefore

\[
\boxed{X_{1/2}=c.}
\]

This is the exact material realization of the TIR exchange-symmetric half selector.

## 3. Realized-event selector

For a finite realized history down-set \(D\), define

\[
D_q=\{\nu\in D:q_{e(\nu)}>0\}
\]

and

\[
\boxed{\mathcal N(D)=\operatorname{Max}_{\prec_T}(D_q).}
\]

The wave sector supplies material position candidates through \(\mathfrak X_\rho\). The realized-event sector supplies event identity through \(\mathcal N(D)\).

The two outputs therefore have distinct types:

```text
Temporal Wave        -> X_q(Theta), q in (0,1)
Realization/order    -> N(D), maximal supported occurrences
Binding selector     -> q_*(nu)
Material NOW image   -> B_NOW(nu)=X_{q_*(nu)}
```

## 4. Serial realization binding

For a serial history with a supported realized frontier,

\[
\mathcal N(D)=\{\nu_N\},
\]

define a material binding by a selector

\[
q_*:\mathcal N(D)\to(0,1).
\]

Then

\[
\boxed{
\mathfrak B_{\rm NOW}(\nu_N;\rho,J)
:=X_{q_*(\nu_N)}(\Theta_N).
}
\]

The exchange-symmetric binding uses

\[
\boxed{q_*(\nu_N)=\frac12}
\]

and therefore

\[
\boxed{
\mathfrak B_{\rm NOW}^{(1/2)}(\nu_N)=X_{1/2}(\Theta_N).
}
\]

Its material velocity is inherited directly from continuity,

\[
\boxed{
D_\Theta\mathfrak B_{\rm NOW}^{(1/2)}
=u(X_{1/2},\Theta).
}
\]

The realized occurrence identity is inherited from the prefix-order frontier.

## 5. Concurrent realization binding

For a concurrent realized frontier

\[
\mathcal N(D)=\{\nu_{b_1},\ldots,\nu_{b_m}\},
\]

use a branch-indexed family of material densities and selectors,

\[
(\rho_b,J_b,q_{*,b}).
\]

The material image is

\[
\boxed{
\mathfrak B_{\rm NOW}(\mathcal N)
=\left\{
(\nu_b,X_{q_{*,b}}^{(b)})
:\nu_b\in\mathcal N
\right\}.
}
\]

With exchange-symmetric branch selectors,

\[
\boxed{q_{*,b}=\frac12\quad\forall b.}
\]

Hence the antichain structure is retained while each branch receives its own material half-mass marker.

## 6. Selector factorization theorem

The full NOW material coordinate factors as

\[
\boxed{
(D,\prec_T,q_e;\rho,J)
\longmapsto
\left(
\mathcal N(D),
\mathfrak X_\rho
\right)
\longmapsto
\mathfrak B_{\rm NOW}.
}
\]

The first component selects realized occurrence identity. The second component supplies material kinematics. The binding selector pairs the two.

For the exchange-symmetric selector,

\[
\boxed{
\mathfrak B_{\rm NOW}^{(1/2)}
=
X_{1/2}\circ\mathcal N
}
\]

with the understanding that \(X_{1/2}\) is evaluated on the material branch associated with each maximal occurrence.

This produces a direct architecture

\[
\boxed{
\text{RELATIONAL REALIZATION}
\to
\text{NOW EVENT IDENTITY}
\quad\times\quad
\text{TEMPORAL WAVE CONTINUITY}
\to
\text{MATERIAL FRONT}
\to
\text{BOUND NOW COORDINATE}.
}
\]

## 7. Falsification gates

Reference tests require:

- \(q\mapsto1-q\) has the unique fixed point \(1/2\);
- mirror-symmetric densities satisfy \(X_{1-q}=2c-X_q\);
- the symmetric material marker is \(X_{1/2}=c\);
- a serial realized history binds its unique supported NOW occurrence to exactly one selected material marker;
- state-label recurrence preserves unique occurrence identity through prefix lineage;
- concurrent maximal frontiers bind branchwise and retain all maximal occurrence IDs;
- changing wave density changes material coordinates while preserving the supplied realized-event identity;
- changing event realization changes the selected occurrence while preserving the supplied material quantile family;
- invalid selectors and unresolved material quantiles fail closed.

Reference implementation: `src/idt/now_material_quantile_binding.py`.
Reference tests: `tests/reference/test_now_material_quantile_binding.py`.
Validation receipt: `validation/NOW_MATERIAL_QUANTILE_BINDING_V0_1.json`.
