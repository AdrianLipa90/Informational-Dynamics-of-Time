# CURRENT EVIDENCE STATE

Status: `TEMPORAL_ACTIVITY_NOW_V0_1_PASS`

Current targeted reference suite:

- Shannon/phase + relational kinetics + memory-orbit + temporal activity + harmonic scheduler: `31 passed in 0.07s`;
- activity/current hyperbolic decomposition: PASS;
- drive reversal preserves positive activity and flips directed current: PASS;
- edge drive and affinity recovered from activity/current ratio: PASS;
- coincident positive activity atoms aggregate without cancellation: PASS;
- non-injective pushforward preserves positive atomic support as the image support: PASS;
- memory-orbit antisymmetry and signed-area circulation controls remain PASS.

Fail-loud note: the first run produced `30 passed, 1 failed` because one test compared the floating sum `0.6000000000000001` to `0.6` by exact equality. The assertion was corrected to a numerical tolerance; the implementation itself was unchanged. The final targeted suite is `31 passed`.

The evidence establishes structural properties of the declared mathematical construction. Physical memory, subjective elapsed time, and metric time remain separate downstream evidence targets.

Local monograph verification: two-pass `pdflatex` PASS, 46 pages, no Overfull/Undefined/LaTeX warnings after shortening the appendix running header. PDF remains local only.
