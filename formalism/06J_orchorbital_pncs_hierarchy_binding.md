# 06J — PNCS-Bound ORCHORBITAL Hierarchy

Status: `PNCS_V0_29_SOURCE_PINNED / HIERARCHY_BINDING_REFERENCE_PASS / HOSTED_FULL_SUITE_PASS`

## 1. Source contract

The temporal ORCHORBITAL hierarchy consumes the established PNCS sphere/entity identity contract from the exact upstream snapshot

```text
repository = AdrianLipa90/PhaseNav-Natural-Coding-System
commit     = 7a54596c1794be29e0b85f5c363213cc81eb87d7
contract   = PNCS_ORCHORBITAL_HARVEST_HARDENING_V0_29
```

The upstream entity projection supplies the typed coordinates

\[
\boxed{
(\mathrm{canonical\_id},\mathrm{hierarchy\_path\_id},
\mathrm{sphere\_id},\mathrm{parent\_sphere\_id},
\mathrm{orbit\_index},\varphi_{orb})
}
\]

with optional paired semantic-mass coordinates

\[
\boxed{(m_{sem},\mathrm{mass\_binding\_id}).}
\]

IDT binds each dynamic attractor leaf to one such upstream entity projection.

## 2. Temporal attractor/entity binding

For temporal attractor \(\mathfrak A_i\), define the source binding

\[
\boxed{
\mathcal B_i=
\left(
 a_i,
 p_i,
 c_i,
 h_i,
 s_i,
 s_i^{parent},
 o_i,
 \varphi_i,
 m_i^{sem},
 b_i^{mass}
\right),
}
\]

where

- \(a_i\) is the IDT dynamic attractor name;
- \(p_i\) is the PNCS `entity-projection` ID;
- \(c_i\) is the PNCS typed canonical entity ID;
- \(h_i\) is the PNCS `hierarchy-lineage` ID;
- \(s_i\) and \(s_i^{parent}\) are the sphere and parent-sphere IDs;
- \(o_i\in\mathbb N_0\) is the orbit index inside the sphere;
- \(\varphi_i\in[0,2\pi)\) is the upstream orbital phase;
- semantic mass and its mass-binding ID form one optional typed pair.

The binding set must exactly cover the dynamic ORCHORBITAL leaf set:

\[
\boxed{
\{a_i\}_{\rm IDT}
=
\{a_i\}_{\rm PNCS\ binding}.
}
\]

## 3. Sphere graph

Let the upstream sphere graph be

\[
\mathcal S=\{(s,parent(s))\}.
\]

Every non-root parent must resolve inside \(\mathcal S\), and every ancestry chain terminates at a root. The entity binding satisfies

\[
\boxed{
parent(s_i)=s_i^{parent}.
}
\]

For a leaf attractor \(a_i\), the temporal hierarchy path is therefore

\[
\boxed{
\Pi_i=
(root,\ldots,s_i,a_i).
}
\]

The existing IDT `HierarchyNode` operator is generated directly from the source-bound sphere graph plus the attractor leaves. The Shannon hierarchy operator, residence aggregation and transition coarse-graining therefore consume the same hierarchy already implemented in IDT while entity identity and orbital placement come from PNCS.

## 4. Replay-stable orbital ordering

Inside one source sphere, entity bindings are ordered by

\[
\boxed{
(o_i,\varphi_i,c_i)
}
\]

with unique \((s_i,o_i)\) slots. This gives a deterministic local orbital ordering independent of input record order.

## 5. Typed identity domains

The source binding preserves the upstream ID domains:

```text
source projection  = pncs:entity-projection:sha256:<64 hex>
hierarchy lineage  = pncs:hierarchy-lineage:sha256:<64 hex>
mass binding       = pncs:mass-binding:sha256:<64 hex>
canonical entity   = pncs:<typed-domain>:sha256:<64 hex>
```

Semantic mass is finite and non-negative whenever present and is admitted together with its typed mass-binding ID.

## 6. Integration with IDT hierarchy

For attractor field weights \(w_i\), the source binding changes the provenance and hierarchy identity layer while the existing IDT aggregation remains

\[
W_s=\sum_{i\in\mathrm{desc}(s)}w_i.
\]

The active temporal path is

\[
\boxed{
\Pi_{active}
=(root,\ldots,s_{active},a_{active}).
}
\]

The existing Shannon chain-rule audit, hierarchical residence summary and coarse-grained transition graph therefore operate on nodes generated from the PNCS-bound sphere/entity structure.

## 7. Reference implementation

Implementation:

`src/idt/orchorbital_pncs_hierarchy_binding.py`

Existing hierarchy engine:

`src/idt/orchorbital_hierarchy.py`

Reference controls:

`tests/reference/test_orchorbital_hierarchy.py`

`tests/reference/test_orchorbital_pncs_hierarchy_binding.py`

The controls verify:

- exact upstream repository/commit/contract pin;
- PNCS sphere/entity binding generates the existing IDT hierarchy path;
- exact dynamic-attractor leaf coverage;
- parent-sphere consistency;
- typed projection, hierarchy and mass-binding ID domains;
- paired semantic-mass provenance;
- unique orbit slots and replay-stable ordering;
- source-pin integrity.

## 8. Hosted evidence

GitHub Actions `Reference suite` run `33195337839`, run number `553`, job `98930915664`, executed

```text
python -m pytest -q tests/reference
```

under Python 3.12.14 on Ubuntu 24.04. The complete result was

```text
457 passed in 13.90s
```

The tested PR merge commit is

`39bf430426bb70e1b4b9946d437833b12258dc78`

with tree

`908512a33f37a0ba41f90c5778aacf1f3d2861f9`.

## 9. Dependency state

The ORCHORBITAL temporal-memory chain now includes

\[
\boxed{
\mathrm{Memory}
\rightarrow
\mathrm{attractor\ field}
\rightarrow
\mathrm{residence/switch\ ledger}
\rightarrow
\mathrm{PNCS\ sphere/entity\ hierarchy}
\rightarrow
\mathrm{hierarchical\ temporal\ observables}.
}
\]

The active ORCHORBITAL frontier proceeds to typed binding of the retained truth scalar, semantic mass and reduction-readiness observables. Retrodiction remains the next sequential node after ORCHORBITAL admission.
