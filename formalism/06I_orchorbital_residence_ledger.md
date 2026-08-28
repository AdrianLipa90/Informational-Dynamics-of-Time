# 06I — ORCHORBITAL Residence Ledger and Dwell-Time Gate

Status: `TARGETED_REFERENCE_PASS / APPEND_ONLY_HASH_CHAIN_PASS / LONG_TRAJECTORY_PROFILE_PASS / HOSTED_FULL_SUITE_PASS`

## 1. Purpose

This gate promotes the existing ORCHORBITAL residence summary from an in-memory diagnostic to a replayable temporal lineage. The input is the ordered sequence of admitted ORCHORBITAL smooth segments

\[
S_k=(X_k^-,X_k^+,a_k,F_k^-,F_k^+,\Delta W_k),
\]

with positive internal elapsed increment

\[
\boxed{\Delta\tau_k=\tau(X_k^+)-\tau(X_k^-)>0.}
\]

The ledger preserves the completed segment label, the post-segment attractor candidate, the state lineage and the exact elapsed/winding increments used by residence statistics.

## 2. Content-addressed segment receipt

For each completed segment define

\[
\boxed{
\mathcal R_k=
\left(
 k,
 a_k,
 a_k^+,
 \ell_k,
 \Delta\tau_k,
 \Delta W_k,
 H(X_k^-),
 H(X_k^+),
 h_{k-1}
\right),
}
\]

where

- \(a_k\) is the attractor used by the completed segment;
- \(a_k^+\) is the next bound attractor selected by the post-segment field;
- \(\ell_k\) is the post-segment `LEAK_MODE` flag;
- \(H(X)\) is SHA-256 of the exact finite little-endian float64 memory state carrier;
- \(h_{k-1}\) is the previous receipt hash.

The state carrier hashed by this gate is

\[
\boxed{
X_M^{\rm hash}=(m_x,m_y,v_x,v_y,\tau_{\rm int},\mathcal A_M)
\in\mathbb R^6.
}
\]

`delta_tau` and `winding_increment` are serialized through the exact hexadecimal representation of their finite binary64 values. The receipt hash is

\[
\boxed{
h_k=\operatorname{SHA256}\!\left(\operatorname{CanonicalJSON}(\mathcal R_k)\right).}
\]

The genesis receipt has \(h_{-1}=\varnothing\); every later receipt carries the preceding hash.

## 3. Temporal and state continuity

For adjacent receipts the ledger requires

\[
\boxed{H(X_k^+)=H(X_{k+1}^-)}
\]

and

\[
\boxed{\operatorname{prev}(\mathcal R_{k+1})=h_k.}
\]

Receipt indices form the exact sequence

\[
0,1,\ldots,N-1.
\]

Existing ledger bytes are parsed and verified before an append. A new append is admitted only after the complete candidate chain passes hash, index, state-continuity and attractor-lineage validation. The persisted JSONL is then re-read and compared with the validated candidate.

This defines the append-only trajectory relation

\[
\boxed{
\mathcal L_N
\xrightarrow{\operatorname{append}(S_N,\ldots,S_{N+r})}
\mathcal L_{N+r+1}.
}
\]

## 4. Residence episodes

A residence episode for attractor \(i\) is a maximal contiguous interval of receipt indices

\[
I_{i,r}=\{k_0,\ldots,k_1\}
\]

such that

\[
a_k=i\qquad\forall k\in I_{i,r}.
\]

Its internal dwell time and winding are

\[
\boxed{
T_{i,r}=\sum_{k\in I_{i,r}}\Delta\tau_k,
}
\]

\[
\boxed{
W_{i,r}=\sum_{k\in I_{i,r}}\Delta W_k.
}
\]

Per-attractor dwell statistics are evaluated over the episode set \(\{T_{i,r}\}\):

\[
\boxed{
T_i^{\rm tot}=\sum_rT_{i,r},
\qquad
\bar T_i=\frac{1}{n_i}\sum_rT_{i,r},
}
\]

with median, minimum, maximum and population variance retained as separately typed observables.

The exact global accounting identity is

\[
\boxed{
\sum_i\sum_rT_{i,r}
=\sum_k\Delta\tau_k.
}
\]

## 5. Directed switch lineage

Adjacent active-attractor labels produce the directed transition count

\[
\boxed{
N_{i\to j}
=\#\{k:a_k=i,\ a_{k+1}=j,\ i\neq j\}.
}
\]

A post-segment bound switch is represented by \(a_k^+\neq a_k\). A post-segment leak is represented by

\[
\ell_k=1,
\qquad
a_k^+=\varnothing.
\]

The following orbital segment therefore consumes either a bound next-attractor state or the existing typed `LEAK_MODE` boundary.

## 6. Reference implementation

Implementation:

`src/idt/orchorbital_residence_ledger.py`

Reference controls:

`tests/reference/test_orchorbital_residence_ledger.py`

`tests/reference/test_orchorbital_long_residence_profile.py`

The ledger reference controls cover deterministic receipt hashing, hash-chain linkage, state continuity, append preservation, malformed/empty persistent-state rejection, residence episodes, dwell statistics, directed transition counts and post-segment leak receipts.

The long dynamic profile consumes the real `propagate_orchorbital` operator with two attractors and 101 consecutive segments. It records the expected first `A -> B` promotion, builds and verifies all 101 receipts, derives residence episodes and dwell statistics, and satisfies the global elapsed-time accounting identity to the declared floating-point tolerance.

## 7. Hosted evidence

GitHub Actions `Reference suite` run `33194693525`, job `98928738642`, executed

```text
python -m pytest -q tests/reference
```

under Python 3.12.14 on Ubuntu 24.04. The complete result was

```text
440 passed in 14.50s
```

The tested PR merge commit is

`6aa59bfa4fd8acfc5675de608d29f6aaa6f5a835`

with tested tree

`73f3d31020863b402a04f16b5a2ef562ed1b4e2a`.

## 8. Dependency state

The completed temporal path at this gate is

\[
\boxed{
\mathrm{Memory}
\rightarrow
\mathrm{ORCHORBITAL\ field}
\rightarrow
\mathrm{active\ segment}
\rightarrow
\mathrm{content\mbox{-}addressed\ residence\ ledger}
\rightarrow
\mathrm{dwell/switch\ observables}.
}
\]

The active ORCHORBITAL frontier now proceeds to hierarchical attractor-family typing and the typed binding of retained ORCHORBITAL truth, semantic-mass and reduction-readiness observables. Retrodiction remains the following dependency node.
