# CURRENT THEORY STATE

Status: `RELATIONAL_KINETICS_V0_1`

The upstream temporal chain is now

\[
(H_S,\psi)
\to (\Delta H_e,G_e)
\to \sigma_e
\to (\rho_R,\eta_R,A_e)
\to W_e
\to L_e
\to q_e
\to \mathcal K_T.
\]

The path affinity remains
\[
\sigma_{a\to b}=\log_2\frac{P(b\mid a)}{P(a\mid b)}.
\]
The first density/viscosity closure separates pair mobility from directional drive:
\[
M_{ab}=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]},
\]
\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2}.
\]
Hence \(\sigma_{a\to b}=A_{ab}/\ln2\): symmetric scalar mobility affects pace but cancels from directional affinity.

If \(A_{ab}\) is an exact scalar state-potential difference, closed-cycle affinity vanishes. Immediate derivational target: test whether memory-orbit state or phase geometry supplies a non-exact edge drive.
