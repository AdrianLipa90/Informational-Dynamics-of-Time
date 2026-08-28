# 07V — Radial Packet Residence-Lineage Binding

## Scope

07U supplies an exact winding–radius decoder once the pre-final active-attractor radii

\[
\rho_k=\|r_k-c_{a_k}\|>0,
\qquad 1\le k<N,
\]

are retained together with the ordered signed winding and final position. This layer binds those radial coordinates directly to the append-only Memory/ORCHORBITAL event-residence lineage.

The historical residence receipt schema remains unchanged. 07V adds a companion content-addressed radial lineage whose coordinates are authenticated by the residence cells that generated them.

## Residence-bound radial coordinate

Let the event-residence cell at checkpoint \(k\) carry content hash \(C_k\), active attractor \(a_k\), and committed post-segment state hash \(H_k^+\). Let

\[
\rho_k=\|r_k-c_{a_k}\|.
\]

For each checkpoint define the radial-coordinate commitment

\[
\boxed{
R_k=
H\!\left(
\mathrm{schema},k,a_k,\operatorname{floathex}(\rho_k),C_k,H_k^+,R_{k-1}
\right),
}
\]

with \(R_0\) represented by the null previous-hash field.

Thus every radial coordinate is bound simultaneously to:

1. its checkpoint index;
2. the active attractor used for the segment;
3. the exact binary64 radial value;
4. the source event-residence cell;
5. the committed post-segment state;
6. the preceding radial-coordinate commitment.

The chain head is therefore a content commitment to the ordered radial packet and its exact residence provenance.

## Construction

The reference implementation replays the same persisted Memory event sequence used to build the event-residence cells. For each post-segment state it verifies

\[
H(\mathrm{state}_{k}^{+})=H_k^+
\]

and the replayed active attractor equals \(a_k\). Only then is

\[
\rho_k=\|r_k-c_{a_k}\|
\]

admitted into the radial companion lineage.

The pre-final coordinates

\[
(\rho_1,\ldots,\rho_{N-1})
\]

are exported directly as the 07U `ActiveRadiusCoordinate` packet. The final radial coordinate remains in the authenticated lineage as an audit coordinate while 07U obtains the final position directly from the declared base observation.

## Composition with 07U and 07K

The persistence path is

\[
\boxed{
\mathrm{event\ residence\ lineage}
\longrightarrow
(\alpha,\mathcal W,\rho_1,\ldots,\rho_{N-1})
\xrightarrow{07U}
(r_1,\ldots,r_N)
\xrightarrow{07K^{-1}}
(u_1,\ldots,u_N).
}
\]

Residence hashes authenticate the retained coordinates and are excluded from semantic observability. Separation remains carried by the declared physical/model coordinates: active sequence, winding, radii and retained base observation.

## Fail-closed conditions

The verifier rejects malformed or non-positive radii, broken coordinate hash chains, source-cell mismatches, post-state commitment mismatches, active-attractor mismatches, non-contiguous checkpoint indices and unequal residence/radial lineage lengths.

An explicit A→B active-attractor switch reference verifies that the radial coordinate is computed relative to the active center of each segment rather than one fixed center.

## Evidence

Hosted Reference-suite authority:

```text
run: 33209552154 (#692)
job: 98979116624
tested head: 2047bd585ca91c58bb106547a2ea4cb296a19bfc
tested PR merge: cf59dc9e69f26fa5b566d6b54e26294ef7478efb
result: 557 passed in 14.11s
Python: 3.12.14
Ubuntu: 24.04.4
```

The six new reference tests cover exact residence binding, exact export into the 07U packet, composition through 07U and 07K to the original kicks, content-hash tamper rejection, residence-lineage mismatch rejection and active-attractor switching.

## Status

```text
RADIAL_PACKET_RESIDENCE_BINDING_PASS
RESIDENCE_BOUND_WINDING_RADIUS_CARRIER_PASS
HOSTED_FULL_SUITE_PASS
GENERAL_GLOBAL_INJECTIVITY_OPEN
```

07V closes the declared radial-persistence gate. The broader global-domain coverage coordinate remains active before Retrocausal Tests can be admitted.
