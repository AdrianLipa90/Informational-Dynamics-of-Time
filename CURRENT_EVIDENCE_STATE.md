# CURRENT EVIDENCE STATE

Status: `TRANSPORT_V0_1_RECORDED / KEPLER_MEMORY_V0_1_TARGETED_PASS / EVENT_MEMORY_KICK_V0_1_TARGETED_PASS / MEMORY_MU_IDENTIFIABILITY_V0_1_TARGETED_PASS`

Previously recorded full reference suite at the admitted Temporal Transport frontier: `83 passed in 0.12s`.

Recorded targeted controls:

- Kepler--Newton memory suite: `11 passed in 0.46s`;
- event-imprint memory-kick suite: `7 passed in 0.08s`;
- memory central-parameter identifiability: `6 targeted checks PASS`.

The latest identifiability checks cover:

- ellipse apses recovering \(a_M,e_M,p_M\): PASS;
- \(\mu_M=h_M^2/p_M\): PASS;
- \(\mu_M=4\pi^2a_M^3/T_M^2\): PASS;
- circulation estimator \(\mu_M=p_M^{-1}[(d\Gamma_M/d\tau_{\rm int})/\lambda_M]^2\): PASS;
- orientation reversal preserving identified \(\mu_M\): PASS;
- invalid geometry, period and coupling inputs failing closed: PASS.

Validation receipts:

- `validation/KEPLER_MEMORY_DYNAMICS_V0_1.json`;
- `validation/EVENT_MEMORY_KICK_V0_1.json`;
- `validation/MEMORY_MU_IDENTIFIABILITY_V0_1.json`.

Full repository suite status for the latest execution: `NOT_RERUN_IN_THIS_EXECUTION`.

The current evidence supports the declared structural reference implementations and conditional identifiability identities. Memory-node admission continues to follow the dependency graph; Kähler-derived memory-observable selection, persistence/recall, deeper upstream prediction of \(\mu_M\), and physical-unit calibration remain later derivation/evidence targets.
