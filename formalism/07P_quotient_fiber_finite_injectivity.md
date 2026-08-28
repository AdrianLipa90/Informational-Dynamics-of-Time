# 07P — Quotient/Fiber Finite-Domain Injectivity Gate

Status: `PROVISIONAL_DOWNSTREAM / GREMLIN_QUOTIENT_FIBER_CANDIDATE / LOCAL_REFERENCE_9_OF_9_PASS / FINITE_DOMAIN_GATE_IMPLEMENTED / HOSTED_FULL_SUITE_PASS / GENERAL_GLOBAL_INJECTIVITY_OPEN`.

## 1. Dependency position

The Retrodiction stack already contains pair-scoped collision witnesses, continuous ORCHORBITAL separators, spatial-offset/divergence channels, adaptive SOD selection, and event-aware residence conditioning. 07P adds the missing finite-domain admission rule: a declared observation bundle must separate every collision pair in a declared finite candidate-history domain.

Reference implementation:

`src/idt/retrodiction_quotient_fiber_injectivity.py`.

Reference tests:

`tests/reference/test_retrodiction_quotient_fiber_injectivity.py`.

Evidence receipt:

`validation/RETRODICTION_QUOTIENT_FIBER_FINITE_INJECTIVITY_V0_1.json`.

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

be declared fiber channels. Define

\[
\widetilde Y(z)=\bigl(Y(z),F_1(z),\ldots,F_m(z)\bigr).
\]

Then

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

The proof partitions all distinct candidate pairs into those already separated by the base projection and those lying in one base fiber. Injectivity of the augmented map is equivalent to separation of every pair in the second class by at least one retained fiber channel.

The numerical gate uses explicit tolerances

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

It is fiber-separated when

\[
\exists c:\
\|F_c(z_i)-F_c(z_j)\|_2>\varepsilon_F.
\]

The implementation emits `FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER` only when every collision pair in the declared finite domain is separated.

## 3. GREMLIN relational-isomorphism candidate

GREMLIN identified the common typed structure

```text
non-injective base projection
  -> collision fiber
  -> retained lift coordinate
  -> separation inside the fiber
  -> inverse recovery on the declared finite domain
```

The candidate is grounded in three independently versioned source structures.

### 3.1 RFC normalized shape and extensive scale

Pinned source:

```text
AdrianLipa90/Relational-Field-Closure
e7817ce07a989ae95246f21e5e632da4b9d04493
formalism/RFN1B2H_NORMALIZED_SHAPE_HOLONOMY.md
```

RFC defines

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

The extensive coordinate \(Q_\Sigma\) is retained separately and the lift

\[
\mathcal L_{Q_\Sigma}(p)=Q_\Sigma p
\]

closes the round trip. In the 07P dictionary, normalized shape is a quotient/base coordinate and positive extensive scale is a separating fiber coordinate.

### 3.2 Secret of a Half exact two-sheeted quotient

Pinned source:

```text
AdrianLipa90/secret-of-a-half
4cf36453ee2b6d33a1f9177ca324b9ef491270be
monograph/chapters/41_paired_spectrum_quotient_correspondence.tex
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
=\left\{
\frac12+\sqrt w,
\frac12-\sqrt w
\right\}.
\]

The quotient therefore has an exact two-element fiber. A sheet coordinate separates the two lifted states at one quotient value. The same source proves

\[
\boxed{q\circ N_s=J\circ q},
\]

so the quotient dynamics commutes exactly while the lifted sheet information remains separately typed.

### 3.3 TIR projection, orientation and open holonomy

Pinned source:

```text
AdrianLipa90/The-Fundamental-Theory-of-Informational-Relations
26bd867c10b6f6e21b54f2a4dc7b2f49df62907a
archive/v7.9/full/33_debt10_white_thread_open_holonomy_preckm_v3_5/METATIME_SM_WHITE_THREAD_OPEN_HOLONOMY_PRECKM_v3_5.md
```

The source carries an open-path White-Thread holonomy between non-identical oriented sector bases and verifies nonzero off-diagonal structure. For the 07P candidate dictionary, projected/base information and orientation/transport information occupy distinct roles. GREMLIN keeps this mapping at candidate status until an explicit commuting map into the Retrodiction state space is supplied.

## 4. Exact IDT reflection-null binding

07H supplies two latent histories with

\[
\|\widetilde z-z\|_2=0.9233193011263697
\]

and final retained base observation

\[
Y_B=(r_x,r_y,v_x,w_A,w_B,w_C)_2
\]

with

\[
\delta_B=5.594315114139762\times10^{-17}.
\]

The earlier continuous basin weight is

\[
w_{A,1}(z)=0.5838364569736161,
\qquad
w_{A,1}(\widetilde z)=0.6030256253846112,
\]

hence

\[
\boxed{|\Delta w_{A,1}|=0.01918916841099516.}
\]

The two-history finite domain therefore receives

`FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER`

when `w_A_1` is supplied as the fiber channel.

The 07H negative-control coordinate satisfies

\[
|\Delta r_{x,1}|=1.1102230246251565\times10^{-16},
\]

which remains within the declared fiber tolerance and preserves the collision. This directly tests the distinction between coordinate count and separating information.

## 5. Typed Retrodiction fiber bundle

07O establishes an event-aware residence signature containing active/next-attractor labels, switch/leak indices and winding increments. For the declared reflection pair the discrete residence/switch class is shared, while the earlier continuous basin weight separates the histories.

The current Retrodiction observation architecture is therefore represented as

\[
\boxed{
Y_{\rm aug}
=
Y_B
\oplus F_{\rm ORCH}^{\rm cont}
\oplus F_{\rm SOD}
\oplus F_{\rm residence}
\oplus F_{\rm holonomy},
}
\]

where each channel remains separately typed and is admitted as a separator only by the finite-domain pair audit. Content-addressed provenance commitments remain integrity coordinates unless a later observation contract explicitly promotes one into the semantic observation bundle.

## 6. Reference controls

The 07P reference suite contains nine tests:

1. exact two-sheet quotient collision separated by a sheet coordinate;
2. normalized-shape collision separated by scale;
3. identical declared fiber preserving a collision;
4. every base-collision pair required for finite-domain PASS;
5. finite domain with no base collisions;
6. deterministic channel attribution;
7. malformed shape, tolerance and non-finite inputs fail closed;
8. exact 07H reflection-null values separated by `w_A_1`;
9. exact 07H `r_x_1` negative control preserving the collision.

Local pre-write result:

```text
9 passed in 0.04s
```

Hosted repository gate:

- workflow: `Reference suite`;
- run: `33200684482` / run number `592`;
- job: `98949092398`;
- tested branch head: `17d3ba854e83f930194b8dd4c4b7089382578a35`;
- tested PR merge commit: `ee1985c96df734d32a8232c03ca078c993ef7318`;
- command: `python -m pytest -q tests/reference`;
- result: `495 passed in 10.14s`;
- Python: `3.12.14`;
- runner: Ubuntu `24.04.4`.

## 7. Frontier result

07P advances Retrodiction from isolated pair-separation witnesses to a reusable finite-domain injectivity gate:

\[
\boxed{
\forall (z_i,z_j)\in\mathcal K_{\rm base}:\
\exists c\quad F_c(z_i)\ne F_c(z_j)
}
\]

for the declared finite collision set \(\mathcal K_{\rm base}\).

The governing repository frontier remains `GENERAL_GLOBAL_INJECTIVITY_OPEN`. The next admission target is a domain-covering separation argument, constructive inverse, or equivalent global theorem over the retained continuous ORCHORBITAL, SOD and holonomy channels.

## 8. GREMLIN evidence

Live candidate artifact:

```text
/dev/shm/ciel_noema/gremlin/IDT_GREMLIN_RETRODICTION_QUOTIENT_FIBER_20260828.json
```

SHA-256:

```text
2c0caeca231bc135ceec972a6df6cec99db517455564b55f66c5f4314773c1fc
```

GREMLIN remains `CHYBA / CANDIDATE_ONLY`; the exact finite-set lemma, executable gate and hosted reference suite provide the independent IDT evidence path.
