# 07G — Local ORCHORBITAL-Augmented Retrodiction Estimator

Status: `PROVISIONAL_DOWNSTREAM_CANDIDATE / LOCAL_ESTIMATION_TARGETED_PASS / GLOBAL_NULL_EXPLICIT`

This layer consumes the 07F observability gate and turns the locally full-rank partial-checkpoint problem into an explicit estimator. Canonical Retrodiction admission remains downstream of the Memory -> ORCHORBITAL parent gate.

## 1. Measurement map

For latent two-component event kicks collected in
\[
z\in\mathbb R^{2N},
\]
let the retained partial Memory checkpoint and ORCHORBITAL basin weights define
\[
\boxed{Y(z)=Y_{P,O}(z).}
\]
Inside one fixed active-attractor/support regime the sensitivity matrix is
\[
\boxed{J(z)=\frac{\partial Y}{\partial z}.}
\]
The estimator admits a local update only after
\[
\boxed{\operatorname{rank}J(z)=2N.}
\]
A rank-deficient declaration receives the fail-closed status `LOCAL_OBSERVABILITY_RANK_DEFICIENT`.

## 2. Same-regime Gauss--Newton step

Given a target checkpoint vector \(Y_\star\), define the residual
\[
r_k=Y_\star-Y(z_k).
\]
The local step is the least-squares solution
\[
\boxed{
\delta z_k
=\arg\min_{\delta z}
\|J(z_k)\delta z-r_k\|_2.
}
\]
A backtracking line search selects \(\alpha_k\in(0,1]\) and updates
\[
\boxed{z_{k+1}=z_k+\alpha_k\delta z_k}
\]
while preserving the initial active-attractor sequence and bound-support pattern and requiring a strictly smaller residual norm. Boundary crossings are routed back to the 07F non-smooth boundary gate.

## 3. Local recovery probe

The deterministic 200-case probe used two latent kicks, one final checkpoint retaining
\[
(r_x,r_y,v_x)
\]
and the three ORCHORBITAL basin weights. The augmented Jacobian had local rank four in the tested regime.

Starting from the common nominal seed, all 200 nearby targets converged to their generating latent coordinates:

- successful local recoveries: `200/200`;
- maximum latent-coordinate error: `4.6949912690116956e-09`;
- maximum observation residual: `8.996117987372108e-11`.

This supports the scoped claim
\[
\boxed{\text{same-regime local retrodiction: PASS}_{\rm targeted}.}
\]

## 4. Residual-only negative control

The same targets were fitted using only
\[
(r_x,r_y,v_x),
\]
whose local Jacobian has rank three for four latent coordinates. A minimum-norm least-squares procedure reached residual below \(10^{-8}\) in 200/200 cases while the inferred latent vector remained separated from the generating vector by more than \(10^{-4}\) in 200/200 cases.

The median latent error was
\[
5.511556235292925\times10^{-3},
\]
and the maximum was
\[
2.618850346837075\times10^{-2}.
\]
Accordingly a low residual with a rank-deficient measurement receives the typed status

`AMBIGUOUS_FIT / RETRODICTION_UNRESOLVED`.

## 5. Explicit global reflection null

Local full rank and global injectivity are separate gates. The tested augmented checkpoint admits two distinct latent histories with the same retained observation.

Reference latent pair:
\[
\begin{aligned}
u_1&=(0.034,-0.023),\\
u_2&=(-0.008,0.028),
\end{aligned}
\]
while a second solution is
\[
\begin{aligned}
\tilde u_1&=(0.03399999999998063,\ 0.34071654937113033),\\
\tilde u_2&=(-0.00802729491823317,\ -0.8206629500579328).
\end{aligned}
\]
Their latent separation is
\[
\boxed{\|\tilde z-z\|_2=0.9233193011263697.}
\]
Yet the final retained vector
\[
(r_x,r_y,v_x,w_1,w_2,w_3)
\]
agrees to residual
\[
1.936720866602264\times10^{-14}.
\]
The hidden final component changes sign,
\[
v_y=+0.24247769958074852
\quad\longleftrightarrow\quad
v_y=-0.24247769958074855.
\]
Both histories remain in the same tested active-attractor sequence. This establishes an explicit global reflection-null branch for the declared partial measurement.

The repository/formalism may suggest global uniqueness from a locally full-rank augmented Jacobian, yet does not state global uniqueness as an established result. A later global-injectivity or additional-checkpoint gate decides that claim.

## 6. GREMLIN gate

GREMLIN v0.5 remained `CANDIDATE_ONLY`. Three explicit hypotheses returned `SUPPORTED_BY_DECLARED_TESTS` with counts `3/3`, `3/3`, and `3/3`:

1. same-regime augmented local recovery succeeds in the 200-case probe;
2. residual-only fitting on the rank-deficient partial checkpoint is classified as ambiguous;
3. the explicit velocity-reflection global null survives the augmented partial observation.

GREMLIN artifact:

`/dev/shm/ciel_noema/gremlin/IDT_ORCHORBITAL_RETRODICTION_ESTIMATION_PROBE_20260827.json`

SHA-256:

`db97c9ddf6ffbd53ecf9b809ea39f162489df1926a218de32fb9a7d5a1d017df`

Reference implementation: `src/idt/retrodiction_orchorbital_estimation.py`.
Reference tests: `tests/reference/test_retrodiction_orchorbital_estimation.py`.
