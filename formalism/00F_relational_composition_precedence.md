# 00F — Relational Composition, Derived Precedence, and NOW Frontier

Status: `FORMAL_CANDIDATE / ALGEBRAIC_REFERENCE_GATE`

This layer removes a global temporal order from the primitive input. It starts from directed relational composability, unfolds realized relation occurrences into history prefixes, and then uses the positive activity measure of 00E to derive temporal precedence on those occurrences.

## 1. Pretime relational structure

Let

\[
\mathcal G=(S,E,s,t)
\]

be a directed relational multigraph. Each edge \(e\in E\) has source \(s(e)\in S\) and target \(t(e)\in S\).

The primitive operation is composability:

\[
\boxed{
e_{k+1}\circ e_k\ \text{is admitted when}\ t(e_k)=s(e_{k+1}).}
\]

This is an algebraic typing rule for relations. It supplies source/target compatibility without introducing a metric clock coordinate.

A finite realized relational word is

\[
\boxed{
P_n=e_n\circ e_{n-1}\circ\cdots\circ e_1.
}
\]

Define its prefixes

\[
P_0=\mathrm{id}_{s(e_1)},
\qquad
P_k=e_k\circ\cdots\circ e_1.
\]

The terminal state label of the prefix is

\[
x_k=t(P_k).
\]

State labels may recur: \(x_i=x_j\) is allowed for \(i\ne j\).

## 2. Occurrences rather than state labels

A realized occurrence is identified by its full prefix,

\[
\boxed{\nu_k:=(P_k,x_k).}
\]

Two occurrences can carry the same state label while remaining distinct because their prefixes differ.

Define the prefix relation

\[
\boxed{
\nu_i\sqsubseteq\nu_j
\iff
\exists Q:\ P_j=Q\circ P_i.
}
\]

For the prefixes of one realized word,

\[
\boxed{
\nu_0\sqsubset\nu_1\sqsubset\cdots\sqsubset\nu_n.
}
\]

The relation is reflexive, transitive and antisymmetric on prefix-labelled occurrences. Antisymmetry follows because two finite prefixes that extend one another have the same word length and therefore the same prefix.

Thus the unfolded occurrence space carries a partial order generated solely by relational composition. On one serial realized word it is a total order.

## 3. Cycles in state space do not create cycles in occurrence order

Consider

\[
A\xrightarrow{e_1}B\xrightarrow{e_2}A.
\]

The state label returns to \(A\), but the occurrence sequence is

\[
(A,P_0)\sqsubset(B,P_1)\sqsubset(A,P_2).
\]

Hence

\[
\boxed{x_0=x_2\quad\text{while}\quad \nu_0\ne\nu_2.}
\]

State recurrence is retained as recurrence in the relational carrier while the history occurrence remains advanced in the prefix order.

## 4. Positive activity turns prefix order into temporal precedence

00E supplies for each realized edge an intrinsic positive activity measure

\[
\boxed{
\theta(e)
:=\int_e\mathfrak a\,d\lambda>0,
}
\]

where \(\lambda\) is only a local increasing edge parameter and \(\theta(e)\) is invariant under its admitted reparameterization.

Define the cumulative activity coordinate on a prefix,

\[
\boxed{
\Theta(P_k)
:=\sum_{r=1}^{k}\theta(e_r),
\qquad
\Theta(P_0)=0.
}
\]

If \(\nu_i\sqsubset\nu_j\), then

\[
P_j=(e_j\circ\cdots\circ e_{i+1})\circ P_i
\]

and therefore

\[
\Theta(P_j)-\Theta(P_i)
=\sum_{r=i+1}^{j}\theta(e_r)>0.
\]

Hence

\[
\boxed{
\nu_i\sqsubset\nu_j
\Longrightarrow
\Theta(P_i)<\Theta(P_j).
}
\]

On the prefixes of one realized word the converse also holds, so

\[
\boxed{
\nu_i\sqsubset\nu_j
\iff
\Theta(P_i)<\Theta(P_j).
}
\]

The positive activity measure is therefore an order embedding of the nontrivial prefix order into \(\mathbb R\).

Define temporal precedence on realized occurrences by

\[
\boxed{
\nu_i\prec_T\nu_j
\iff
\nu_i\sqsubset\nu_j.
}
\]

Its metric-free origin is relational composition; its intrinsic scalar realization is the strictly increasing coordinate \(\Theta\).

## 5. Local orientation and realized precedence are typed separately

00E supplies

\[
\chi_e=\frac{\mathfrak j_e}{\mathfrak a_e}
=\tanh(A_e/2).
\]

The sign of \(\chi_e\) describes the statistical/dynamical orientation of the admitted pair. The realized morphism occurrence carries its own source-to-target composition type.

At the symmetric point \(A_e=0\),

\[
\chi_e=0,
\qquad
\theta(e)>0.
\]

A realized composable event can therefore advance the occurrence order and accumulate positive duration even when the pairwise directional affinity is at its symmetry value.

## 6. NOW as the maximal realized event frontier

03 supplies a positive gauge-invariant event signature

\[
q_e\ge0.
\]

For a finite realized down-set \(D\) of occurrence prefixes, define the supported event occurrences

\[
D_q
:=\{\nu_k\in D:\ q_{e_k}>0\}.
\]

Define the NOW frontier by maximality in the derived occurrence order,

\[
\boxed{
\mathcal N(D)
:=\operatorname{Max}_{\prec_T}(D_q).
}
\]

For a serial finite realized word with at least one supported event, \(\mathcal N(D)\) contains exactly the latest supported occurrence.

For a partially ordered realized structure with independent concurrent branches, the same definition yields the maximal antichain of currently realized supported events.

Thus NOW is a boundary/frontier of realized relational history rather than an externally supplied coordinate value.

## 7. Prefix extension theorem

Let a realized history be extended by one composable supported edge \(e_{n+1}\):

\[
P_{n+1}=e_{n+1}\circ P_n,
\qquad
q_{e_{n+1}}>0.
\]

Then

\[
\boxed{
\Theta(P_{n+1})
=\Theta(P_n)+\theta(e_{n+1})
>\Theta(P_n),
}
\]

and

\[
\boxed{
\mathcal N(D_{n+1})=\{\nu_{n+1}\}
}
\]

for the serial history. The realized frontier therefore advances exactly when a new supported relation occurrence is appended.

## 8. Derived temporal architecture

The upstream chain is now

\[
\boxed{
\begin{aligned}
&\text{RELATIONAL STATES + DIRECTED COMPOSABILITY}\\
&\downarrow\\
&\text{REALIZED RELATION WORD / PREFIX OCCURRENCES}\\
&\downarrow\\
&\text{PREFIX PARTIAL ORDER }\sqsubseteq\\
&\downarrow\quad +\quad \theta(e)>0\\
&\text{TEMPORAL PRECEDENCE }\prec_T\text{ AND }\Theta\\
&\downarrow\quad +\quad q_e>0\\
&\text{NOW}=\operatorname{Max}(\text{REALIZED SUPPORTED EVENTS}).
\end{aligned}
}
\]

The primitive input has therefore been reduced from an assumed temporal poset \((S,\prec)\) to directed relational composability plus positive transition/event data.

## 9. GREMLIN candidate audit contract

GREMLIN remains candidate-only. The relational-isomorphism candidate is

```text
relation composition      -> prefix extension
prefix extension          -> occurrence partial order
positive extensive weight -> strict scalar order embedding
repeated state label      -> distinct history occurrence
maximal supported prefix  -> NOW frontier
independent maxima        -> concurrent NOW antichain
```

Promotion requires explicit tests for composability, prefix antisymmetry/transitivity, strict activity monotonicity, recurrence without order cycles, unique serial frontier, concurrent maximal-antichain behavior and fail-closed invalid histories.

Reference implementation: `src/idt/relational_precedence.py`.
Reference tests: `tests/reference/test_relational_precedence.py`.
Validation receipt: `validation/RELATIONAL_PRECEDENCE_NOW_V0_1.json`.
