# 02JI — Fuzzy Temporal Interface Order Parameter

Status: `FORMAL_CANDIDATE / JOINT_OCCUPANCY_PHASE_COHERENCE_GATE`

This gate gives an exact criterion for when the half-frame pattern

\[
|1|\,|12|\,|23|\cdots|N|
\]

contains a genuine neighboring-frame fuzzy interface rather than only the baseline half-support produced by the quotient map.

It combines the phase-aware seam of 02JD, the local Onsager locking of 02JG and the full Schrödinger–Onsager balance of 02JH.

## 1. One seam

For neighboring frame amplitudes

\[
a_n=r_ne^{i\alpha_n},\qquad
a_{n+1}=r_{n+1}e^{i\alpha_{n+1}},
\]

with edge-native seam phase \(\varphi_n\), define

\[
\boxed{
\delta_n=\alpha_{n+1}-\alpha_n-\varphi_n
\pmod{2\pi}.
}
\]

The phase-aware overlap and defect amplitudes are

\[
\boxed{
b_n=\frac{e^{+i\varphi_n/2}a_n+e^{-i\varphi_n/2}a_{n+1}}2,}
\]

\[
\boxed{d_n=\frac{e^{+i\varphi_n/2}a_n-e^{-i\varphi_n/2}a_{n+1}}2.}
\]

Their exact probabilities are

\[
|b_n|^2
=\frac14\left(r_n^2+r_{n+1}^2+2r_nr_{n+1}\cos\delta_n\right),
\]

\[
|d_n|^2
=\frac14\left(r_n^2+r_{n+1}^2-2r_nr_{n+1}\cos\delta_n\right).
\]

## 2. Exact defect decomposition

Using \(1-\cos\delta=2\sin^2(\delta/2)\),

\[
\boxed{
|d_n|^2
=\frac14(r_{n+1}-r_n)^2
+r_nr_{n+1}\sin^2\!\left(\frac{\delta_n}{2}\right).
}
\]

The seam defect therefore decomposes into

\[
\boxed{V_n^{\rm amp}=\frac14(r_{n+1}-r_n)^2}
\]

and

\[
\boxed{V_n^{\rm phase}=r_nr_{n+1}\sin^2(\delta_n/2).}
\]

A seamless neighboring interface requires both amplitude co-occupancy/smoothness and phase coherence.

## 3. Pair-normalized overlap and defect fractions

For nonzero pair weight

\[
S_n:=r_n^2+r_{n+1}^2>0,
\]

define

\[
\boxed{
o_n:=\frac{2|b_n|^2}{S_n},
\qquad
f_n:=\frac{2|d_n|^2}{S_n}.
}
\]

Then exactly

\[
\boxed{o_n+f_n=1.}
\]

Define the amplitude-balance coordinate

\[
\boxed{
g_n:=\frac{2r_nr_{n+1}}{r_n^2+r_{n+1}^2}\in[0,1].}
\]

Hence

\[
\boxed{o_n=\frac12(1+g_n\cos\delta_n),}
\]

\[
\boxed{f_n=\frac12(1-g_n\cos\delta_n).}
\]

The value \(g_n=1\) occurs exactly for equal positive neighboring magnitudes. The value \(g_n=0\) occurs when at least one neighboring magnitude vanishes.

## 4. Genuine fuzzy-interface strength

The half-frame quotient assigns an overlap support even when only one neighboring frame is occupied. To isolate genuine two-frame participation define

\[
\boxed{
\mathfrak F_n
:=g_n\cos^2\!\left(\frac{\delta_n}{2}\right)
\in[0,1].
}
\]

This factorizes into

```text
amplitude co-occupancy  = g_n
phase coherence         = cos^2(delta_n/2)
genuine fuzzy interface = product
```

It obeys the exact relation

\[
\boxed{
\mathfrak F_n
=o_n-\frac{1-g_n}{2}.
}
\]

Therefore the baseline half-support contribution caused by amplitude imbalance is removed explicitly.

The sharp conditions are:

\[
\boxed{\mathfrak F_n=1}
\]

iff \(r_n=r_{n+1}>0\) and \(\delta_n=0\pmod{2\pi}\);

\[
\boxed{\mathfrak F_n=0}
\]

if either one neighboring amplitude vanishes or \(\delta_n=\pi\pmod{2\pi}\).

Thus `|n,n+1|` as a maximally coherent fuzzy interface has a precise algebraic criterion.

## 5. Onsager locking increases interface coherence at fixed magnitudes

On the one-seam 02JG flow,

\[
D_\Theta\delta_n=-K_n\sin\delta_n,
\qquad
K_n=\frac{\mu_nr_nr_{n+1}}2>0.
\]

At fixed magnitudes \(g_n\) is constant. Therefore

\[
\boxed{
D_\Theta\mathfrak F_n
=\frac{g_nK_n}{2}\sin^2\delta_n
\ge0.
}
\]

Explicitly,

\[
\boxed{
D_\Theta\mathfrak F_n
=\frac{\mu_n(r_nr_{n+1})^2}
{2(r_n^2+r_{n+1}^2)}\sin^2\delta_n
\ge0.
}
\]

So phase-only Onsager locking monotonically increases the genuine fuzzy-interface strength wherever both adjacent frames are occupied.

Its asymptotic ceiling is

\[
\boxed{\mathfrak F_n\to g_n.}
\]

Perfect value \(1\) additionally requires amplitude balance.

## 6. Role of Schrödinger spreading

02E/02JH permits the frame magnitudes \(r_n(\Theta)\) to evolve under unitary transport. This changes \(g_n\), so the full-system derivative of \(\mathfrak F_n\) has both amplitude-transport and phase-locking contributions.

The structural division is therefore

\[
\boxed{
\text{Schrödinger transport}
\to
\text{neighboring amplitude co-occupancy }g_n,
}
\]

\[
\boxed{
\text{Onsager seam descent}
\to
\text{phase coherence }\cos^2(\delta_n/2).
}
\]

and their joint observable is \(\mathfrak F_n\).

No monotonicity is asserted for \(\mathfrak F_n\) under arbitrary combined Schrödinger–Onsager evolution; the exact global balance of 02JH remains the governing full-system statement.

## 7. Chain profile

For \(N\) frames define the fuzzy-interface profile

\[
\boxed{
\boldsymbol{\mathfrak F}
=(\mathfrak F_1,\ldots,\mathfrak F_{N-1}).
}
\]

The serial half-frame pattern

\[
|1|\,|12|\,|23|\cdots|N|
\]

is therefore represented by boundary half-supports plus the internal profile \(\boldsymbol{\mathfrak F}\).

A useful aggregate is the pair-weighted chain coherence

\[
\boxed{
\mathfrak F_{\rm chain}
=\frac{\sum_{n=1}^{N-1}(r_n^2+r_{n+1}^2)\mathfrak F_n}
{\sum_{n=1}^{N-1}(r_n^2+r_{n+1}^2)}
\in[0,1].
}
\]

This scalar summarizes the internal fuzzy-interface sector while retaining the per-seam profile for local audits.

## 8. Reference controls

The reference gate requires:

- exact defect decomposition into amplitude roughness plus phase mismatch;
- exact pair identity \(o_n+f_n=1\);
- \(0\le g_n,\mathfrak F_n,o_n,f_n\le1\);
- a sharp isolated frame gives \(\mathfrak F=0\) on every adjacent seam;
- equal occupied in-phase neighbors give \(\mathfrak F=1\);
- equal occupied anti-phase neighbors give \(\mathfrak F=0\);
- pure one-seam Onsager locking increases \(\mathfrak F\) at the exact analytic rate;
- a finite Schrödinger spreading witness creates nonzero neighboring co-occupancy from a sharp frame, after which phase locking raises the joint interface strength;
- fail-closed behavior for invalid dimensions or non-finite inputs.

Reference implementation: `src/idt/fuzzy_temporal_interface.py`.
Reference tests: `tests/reference/test_fuzzy_temporal_interface.py`.
Validation receipt: `validation/FUZZY_TEMPORAL_INTERFACE_V0_1.json`.
