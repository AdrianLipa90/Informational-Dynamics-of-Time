# Monograph status

Repository policy: LaTeX source is canonical; compiled PDF is a local QA artifact and is not committed.

Current included downstream reference chapters:

- `08A_memory_admission.tex` — integrated Memory reference gate;
- `08B_retrodiction_contract.tex` — withheld-lineage inverse problem;
- `08C_retrodiction_uncertainty.tex` — covariance and local Fisher geometry;
- `08D_partial_checkpoint_selection.tex` — partial-retention observability and conditioning;
- `08E_weighted_retrodiction_nulls.tex` — covariance-weighted estimator and permutation-null ensemble.

Retrodiction chapters remain `PROVISIONAL_DOWNSTREAM` while the canonical admitted dependency frontier remains at Memory. Their presence in the monograph source records the tested reference branch; it does not promote physical or canonical claim status.

Latest weighted-null targeted test file: `5 passed in 0.19s`. Final pre-merge combined checkpoint-selection plus weighted-null targeted rerun: `10 passed in 0.25s` in the isolated local reconstruction of the exact implementation dependencies.

GitHub Actions full-suite status remains `CI_RESULT_NOT_OBTAINED` because hosted jobs terminate before executing steps.
