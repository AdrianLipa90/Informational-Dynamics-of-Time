# Memory admission CI retry — 2026-08-28

Status: `FRESH_FULL_REFERENCE_SUITE_REQUESTED`

Base commit: `3ac1f53af5223d16f8818dba99a63a6af2ba9498`

Base tree: `62f036df6b09e873659566c425c074af507aa081`

Workflow: `.github/workflows/reference-suite.yml`

Required command:

```text
python -m pytest -q tests/reference
```

## Purpose

Obtain a fresh full repository reference-suite result for the integrated Memory tree before issuing any combined Memory admission receipt or moving the canonical admitted frontier beyond Memory.

## Evidence policy

- Hosted GitHub Actions evidence and targeted/local reference receipts remain distinct evidence classes.
- Memory admission requires the full reference suite to execute and pass on the integrated tree.
- A workflow or infrastructure termination before the test step remains `CI_RESULT_NOT_OBTAINED`; it is neither a test PASS nor a test FAIL.
- This retry record does not itself promote Memory, ORCHORBITAL, Retrodiction, or any downstream claim.
- The exact source commit/tree and resulting workflow execution must be bound into any later combined Memory admission receipt.
