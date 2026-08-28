# 07P — Quotient/Fiber Finite-Domain Injectivity Gate

Status: `PROVISIONAL_DOWNSTREAM / GREMLIN_QUOTIENT_FIBER_CANDIDATE / LOCAL_REFERENCE_9_OF_9_PASS / FINITE_DOMAIN_GATE_IMPLEMENTED / HOSTED_FULL_SUITE_REQUIRED_FOR_PROMOTION / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## 1. Dependency position

The current Retrodiction frontier contains pair-scoped collision witnesses, continuous ORCHORBITAL separators, spatial-offset/divergence channels, adaptive SOD selection, and event-aware residence conditioning. The active global question is whether a declared observation family separates every collision in a candidate history domain.

Reference implementation:

`src/idt/retrodiction_quotient_fiber_injectivity.py`.

Reference tests:

`tests/reference/test_retrodiction_quotient_fiber_injectivity.py`.

This layer converts the existing pair-level evidence into a finite-domain collision audit.

## 2. Exact finite-set lemma

Let

\[
\mathcal C=\{z_1,\ldots,z_n\}
\]

be a finite candidate history set, let

\[
Y:\mathcal C\to\mathcal Y
\]

be the retained base projection, and let

\[
F_c:\mathcal C\to\mathcal F_c,
\qquad c=1,\ldots,m,
\]

be declared fiber channels. Define the augmented observation

\[
\widetilde Y(z)
=\bigl(Y(z),F_1(z),\ldots,F_m(z)\bigr).
\]

For exact equality on the finite set,

\[
\boxed{
\widetilde Y\text{ is injective on }\mathcal C
\iff
\forall i\ne j:\
Y(z_i)=Y(z_j)
\Longrightarrow
\exists c:\ F_c(z_i)\ne F_c(z_j).
}
\]

The proof is the pair partition of \(\mathcal C\times\mathcal C\): every distinct pair is separated either by the base projection or, when it lies in one base fiber, by at least one retained fiber channel.

The numerical reference gate uses explicit tolerances

\[
\varepsilon_B>0,
\qquad
\varepsilon_Z>0,
\qquad
\varepsilon_F>0.
\]

A pair enters the collision set when

\[
\|z_i-z_j\|_2>\varepsilon_Z
\]

and

\[
\|Y(z_i)-Y(z_j)\|_2\le\varepsilon_B.
\]

It is separated by the declared fiber when

\[
\exists c:\
\|F_c(z_i)-F_c(z_j)\|_2>\varepsilon_F.
\]

The finite-domain status `FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER` is emitted only when every collision pair passes that condition.

## 3. GREMLIN relational-isomorphism candidate

GREMLIN identified the invariant

```text
non-injective base projection
  -> collision fiber
  -> retained lift coordinate
  -> pair separation inside the fiber
  -> inverse recovery on the declared finite domain
```

The candidate is supported by three independently versioned structures.

### 3.1 RFC normalized-shape / extensive-scale fiber

Pinned source:

```text
repo: AdrianLipa90/Relational-Field-Closure
commit: e7817ce07a989ae95246f21e5e632da4b9d04493
file: formalism/RFN1B2H_NORMALIZED_SHAPE_HOLONOMY.md
```

For a positive carrier vector \(Q\), RFC defines

\[
\mathcal N(Q)=p,
\qquad
p_a=\frac{Q_a}{Q_\Sigma},
\]

with

\[
\mathcal N(\lambda Q)=\mathcal N(Q),
\qquad \lambda>0.
\]

The extensive coordinate \(Q_\Sigma\) is carried separately, and the exact lift

\[
\mathcal L_{Q_\Sigma}(p)=Q_\Sigma p
\]

closes the round trip. In 07P terminology, normalized shape is the base projection and the positive extensive scale is a fiber separator.

### 3.2 Secret of a Half exact two-sheeted quotient

Pinned source:

```text
repo: AdrianLipa90/secret-of-a-half
commit: 4cf36453ee2b6d33a1f9177ca324b9ef491270be
file: monograph/chapters/41_paired_spectrum_quotient_correspondence.tex
```

The exact quotient

\[
q(s)=\left(s-\frac12\right)^2
\]

satisfies

\[
q(1-s)=q(s),
\]

and for \(w\ne0\),

\[
q^{-1}(w)
=
\left\{
\frac12+\sqrt w,
\frac12-\sqrt w
\right\}.
\]

The quotient therefore has an exact two-element fiber. A sheet coordinate separates the two lifted states while the quotient value remains identical.

The same source proves the commuting diagram

\[
q\circ N_s=J\circ q,
\]

showing that a dynamics can descend through the quotient while the lifted two-sheet structure remains recoverable only with fiber information.

### 3.3 TIR projection/orientation/open-holonomy structure

Pinned source:

```text
repo: AdrianLipa90/The-Fundamental-Theory-of-Informational-Relations
commit: 26bd867c10b6f6e21b54f2a4dc7b2f49df62907a
file: archive/v7.9/full/33_debt10_white_thread_open_holonomy_preckm_v3_5/METATIME_SM_WHITE_THREAD_OPEN_HOLONOMY_PRECKM_v3_5.md
```

The source carries an open-path White-Thread holonomy between non-identical oriented sector bases and verifies nonzero off-diagonal structure. For the 07P candidate dictionary, the projected/base description and its orientation/transport data occupy distinct information roles. GREMLIN classifies this as a structural candidate for a fiber-transport channel; domain-specific promotion requires an explicit commuting map into the Retrodiction state space.

## 4. IDT reflection-null binding

07H supplies a concrete two-history collision for the final retained base checkpoint

\[
Y_B=(r_x,r_y,v_x,w_A,w_B,w_C)_2.
\]

The two latent histories have

\[
\|\widetilde z-z\|_2
=0.9233193011263697,
\]

while

\[
\delta_B
=5.594315114139762\times10^{-17}.
\]

The earlier continuous basin weight gives

\[
w_{A,1}(z)=0.5838364569736161,
\]

\[
w_{A,1}(\widetilde z)=0.6030256253846112,
\]

and therefore

\[
\boxed{
|\Delta w_{A,1}|
=0.01918916841099516.
}
\]

The 07P finite-domain gate classifies this two-history domain as

`FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER`

when `w_A_1` is the declared fiber channel.

The 07H negative control

\[
|\Delta r_{x,1}|
=1.1102230246251565\times10^{-16}
\]

remains within the declared fiber tolerance and therefore leaves that collision unresolved. This preserves the distinction between adding a coordinate and adding a separating coordinate.

## 5. Residence labels, continuous channels and provenance

07O establishes an event-aware residence signature containing active/next attractor labels, switch/leak indices and winding increments. For the declared reflection pair, the discrete residence and switch lineage remains equivalent, while the earlier continuous basin weight separates the histories.

07P therefore treats all retained channels uniformly at the gate interface while preserving their typed origin:

\[
\boxed{
\text{base projection}
\;\oplus\;
\text{continuous ORCH observables}
\;\oplus\;
\text{spatial/SOD coordinates}
\;\oplus\;
\text{residence/transport channels}.
}
\]

Content-addressed provenance commitments remain audit coordinates and stay outside semantic pair separation unless a later gate explicitly admits a provenance field as an observation.

## 6. Reference controls

The initial 07P reference suite contains nine tests:

1. exact two-sheet quotient collision separated by a sheet coordinate;
2. normalized-shape collision separated by scale;
3. identical declared fiber preserving a collision;
4. all base-collision pairs required for finite-domain PASS;
5. no-collision finite domain returning the vacuous base-injective status;
6. deterministic sorted channel attribution;
7. malformed shape/tolerance/non-finite inputs fail closed;
8. exact 07H reflection-null values separated by `w_A_1`;
9. exact 07H `r_x_1` negative control preserving the collision.

Local exact result before repository write:

```text
9 passed in 0.04s
```

Hosted full-suite authority is the next promotion requirement for this branch head.

## 7. Scope of the new status

07P introduces a strict finite-domain claim:

\[
\boxed{
\text{every base collision in the declared finite candidate set}
\text{ is separated by the declared fiber bundle}
}
\]

when the implementation emits `FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER`.

The current repository-wide frontier remains `GENERAL_GLOBAL_INJECTIVITY_OPEN`. Advancement from a finite candidate set to a global history domain requires a domain-covering argument, constructive inverse, or equivalent global separation theorem using the retained continuous ORCHORBITAL and spatial/holonomy channels.

## 8. GREMLIN evidence

Live candidate artifact:

```text
/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_QUOTIENT_FIBER_20260828.json
```

Candidate artifact SHA-256:

```text
2c0caeca231bc135ceec972a6df6cec99db517455564b55f66c5f4314773c1fc
```

GREMLIN status remains `CHYBA / CANDIDATE_ONLY`. The formal lemma and reference tests are the independent admission path for IDT.
