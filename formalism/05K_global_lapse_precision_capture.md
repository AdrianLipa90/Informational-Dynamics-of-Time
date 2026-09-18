# 05K — Precision-Safe Global-Lapse Production Capture

Status: `SOURCE_CONTRACT / PRECISION_SAFE_REFERENCE_GATE / PHYSICAL_PRODUCTION_CLAIM_FALSE / CANON_ALLOWED_FALSE`

## Purpose

05K preserves lapse information below binary64 unit-resolution by storing the multiplicative clock ratio in an additive logarithmic coordinate. For a fractional offset `delta` with `delta>-1`,

\[
\ell_{x|y}=\ln N_{x|y}=\ln(1+\delta_{x|y}).
\]

The reference implementation uses decimal arithmetic with an explicit precision budget rather than forming `1+delta` in binary64.

## Global-potential certificate

For every oriented clock edge `y -> x`, the supplied logarithmic ratio must admit one patch potential `L`,

\[
\boxed{L_x-L_y=\ell_{x|y}.}
\]

Equivalent cycle closure is

\[
\boxed{\sum_{e\in C}\operatorname{sgn}_C(e)\,\ell_e=0}
\]

within the declared decimal tolerance. A disconnected graph, inconsistent cycle, digest mismatch, invalid provenance class, or non-finite value fails closed.

Recovered patch ratios are

\[
N_x=e^{L_x},\qquad \delta_x=e^{L_x}-1.
\]

## Evidence boundary

A structurally valid production-shaped dataset is only `promotion_review_eligible`. The source contract sets `canon_allowed=false` and the evidence wrapper sets `physical_production_claim=false`. Physical realization, calibration, and canon promotion require separate evidence and authority.

Reference implementation:

- `src/idt/global_lapse_precision_production_capture.py`;
- `src/idt/global_lapse_precision_evidence_v0_2.py`;
- `src/idt/global_lapse_precision_receipt_v0_2.py`.

Reference tests:

- `tests/reference/test_05K_global_lapse_precision_production_capture_v0_2.py`.
