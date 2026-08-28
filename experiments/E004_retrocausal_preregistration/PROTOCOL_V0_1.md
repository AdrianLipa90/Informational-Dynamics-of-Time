# E004 — Retrocausal Test Preregistration V0.1

Status: `PREREGISTRATION_READY / EXECUTION_GATED_BY_RETRODICTION_ADMISSION`

## 1. Purpose

This protocol fixes the analysis contract for a future retrocausal test before experimental data are inspected. The experiment asks whether an observation record sealed at an earlier ordered event contains reproducible information about a later independently generated condition after the declared Retrodiction and classical-channel controls are applied.

The evidential pipeline is fixed as

```text
RAW_OBSERVATION
-> STATISTICAL_EFFECT
-> CLASSICAL_CHANNEL_AUDIT
-> PHYSICAL_CLAIM_STATUS
```

Every transition is separately recorded.

## 2. Ordered event contract

For trial `i`, define four ordered events

\[
t_{0,i}<t_{S,i}<t_{F,i}<t_{R,i}.
\]

- `t0`: trial initialization;
- `tS`: early observation record is sealed and content-hashed;
- `tF`: future condition is generated independently after the seal;
- `tR`: condition is revealed to the analysis layer after all trial data are immutable.

The raw early record is denoted `X_i`. Its commitment is

\[
C_i=H(\mathrm{canonical}(X_i)).
\]

The future condition is denoted

\[
F_i\in\{0,1\}
\]

for the binary reference protocol. The same analysis can later be generalized through a separately versioned preregistration.

## 3. Future-condition generation

`F_i` is generated only after `C_i` has been persisted. The condition generator uses a declared independent random source whose raw output, conversion rule and timestamp are logged.

The assignment record stores:

```text
trial_id
sealed_observation_sha256
seal_timestamp
future_rng_source_id
future_rng_raw_record_sha256
future_condition
future_condition_timestamp
reveal_timestamp
```

The temporal-order gate requires

\[
\boxed{t_S<t_F<t_R.}
\]

Trials failing this inequality are excluded by the preregistered integrity rule and remain present in the audit ledger with an exclusion code.

## 4. Frozen early-data statistic

Before execution, define a deterministic feature map

\[
Z_i=g(X_i),
\]

where `g` is code-hashed and frozen by this preregistration. A deterministic scoring map

\[
s_i=h(Z_i)
\]

produces one scalar score per trial using only the sealed early record.

For the binary reference protocol, the primary statistic is the standardized difference

\[
\boxed{
T_{\rm obs}
=
\frac{\bar s_{F=1}-\bar s_{F=0}}
{\sqrt{s_1^2/n_1+s_0^2/n_0}}.
}
\]

If a declared estimator directly outputs a probability `p_i=P(F_i=1|X_i)`, the preregistered secondary statistic is balanced log loss relative to the assignment labels. Secondary statistics do not replace the primary statistic.

## 5. Null ensemble

The confirmatory p-value is produced by a permutation ensemble that shuffles `F_i` only within preregistered exchangeability blocks. Blocks are defined before execution by experimental session and any declared hardware/configuration stratum.

Let `B` be the number of random permutations and let `T_b` be the statistic under permutation `b`. The two-sided finite-sample permutation p-value is

\[
\boxed{
p_{perm}
=
\frac{1+\#\{b:|T_b|\ge|T_{obs}|\}}
{B+1}.
}
\]

Reference defaults:

```text
permutations: 100000
alpha_confirmatory: 0.005
alternative: two-sided
```

These values are part of the preregistration and require a new protocol version to change.

## 6. Sample-size and stopping rule

The confirmatory sample size is fixed before execution. The reference V0.1 target is

```text
valid_trials_target: 4096
```

Acquisition ends when 4096 valid trials have been collected or the preregistered operational ceiling is reached. Statistical results are not inspected for stopping decisions.

The operational ceiling is

```text
attempted_trials_ceiling: 4608
```

Excluded trials do not count toward the valid-trial target. Every exclusion is append-only and receives a preregistered reason code.

## 7. Exclusion rules

A trial is excluded from the confirmatory statistic when any of the following machine-checkable conditions occur:

1. early-record serialization or content hash fails;
2. `tS < tF < tR` fails;
3. future RNG raw record is absent or malformed;
4. duplicated trial identifier;
5. declared hardware acquisition error;
6. non-finite frozen feature or score;
7. classical-channel audit finds trial-specific future-label availability before `tF`.

Excluded trials remain in the raw ledger.

## 8. Classical-channel audit

A statistical effect advances to physical-claim review only after the classical-channel audit passes. The audit checks at minimum:

- process and thread memory accessible to the early-data pipeline;
- environment variables and configuration files;
- filesystem paths, caches and temporary files;
- database/shared-memory state;
- network sockets and external requests;
- RNG state sharing;
- clock synchronization and timestamp source;
- future-condition precomputation;
- filename, directory, metadata and ordering leakage;
- post-seal mutation of `X_i`;
- analysis access to `F_i` before the reveal stage;
- preprocessing choices conditioned on future labels.

The audit output is append-only and trial-addressable.

## 9. Retrodiction control

The experiment inherits the IDT Retrodiction gate. For every retained temporal record used by the scoring layer, the declared observation representation must pass its applicable collision/fiber audit. Residence-bound winding/radius coordinates are authenticated by the 07V lineage when that architecture is used.

Execution of the physical retrocausal experiment remains gated until the repository dependency authority admits the required Retrodiction domain coverage.

## 10. Negative and positive controls

The preregistered controls are:

### Negative control A — permuted future labels

The complete pipeline is evaluated against block-permuted labels. Results must agree with the declared null ensemble.

### Negative control B — synthetic timing reversal audit

The analysis intentionally supplies labels generated before `tS` in a separate engineering control dataset. The leakage audit must identify this ordering as classically available information.

### Positive control — explicit allowed channel

A separate engineering dataset injects a known low-amplitude classical marker into the early record. The frozen statistic/audit stack must detect the channel. This validates sensitivity without entering the confirmatory dataset.

Controls are stored separately from confirmatory trials.

## 11. Multiple testing

The primary statistic is singular and confirmatory. Any additional feature families, frequency bands, lags, subsets or model variants are exploratory unless separately preregistered before acquisition.

Exploratory results receive their own label and do not modify the V0.1 confirmatory threshold.

## 12. Evidence-state transitions

The protocol uses four explicit states:

```text
RAW_OBSERVATION_RECORDED
STATISTICAL_EFFECT_PASS | STATISTICAL_EFFECT_NULL
CLASSICAL_CHANNEL_AUDIT_PASS | CLASSICAL_CHANNEL_FOUND
PHYSICAL_CLAIM_REVIEW_ELIGIBLE | PHYSICAL_CLAIM_GATE_CLOSED
```

A statistically significant result with a discovered classical channel terminates at `CLASSICAL_CHANNEL_FOUND`.

A statistically significant result with a passed classical-channel audit becomes `PHYSICAL_CLAIM_REVIEW_ELIGIBLE` only when the Retrodiction dependency gate is admitted.

## 13. Replication rule

The first confirmatory dataset is a discovery dataset. A physical claim review requires at least one separately acquired replication using the frozen V0.1 protocol or a strictly predeclared successor protocol, with the same primary direction-independent statistic and classical-channel audit.

## 14. Immutable preregistration boundary

Before acquisition, archive:

- this protocol;
- `preregistration_v0_1.json`;
- hashes of feature/scoring code;
- acquisition code hash;
- RNG adapter code hash;
- classical-channel audit code hash;
- dependency-graph commit SHA;
- hardware/configuration manifest.

Any later change produces a new preregistration version and preserves V0.1 unchanged.
