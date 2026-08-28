# Nature of the Temporal State — Activity-Derived IDT Synthesis

Status: `SYNTHESIS_OF_ADMITTED_STRUCTURAL_LAYERS / ACTIVITY_DERIVATION_CANDIDATE`

This document collects the temporal layers into a single typed architecture. The new upstream coordinate is the activity-derived temporal measure of 00E; clock ratios, calibrated elapsed time, phase transport, NOW, Memory and Retrodiction are placed downstream of that measure.

## 1. Relational order

Let

\[
(S,\prec)
\]

be an ordered relational domain and

\[
\boxed{\Psi:S\to\mathcal H}
\]

the state assignment. The order relation supplies admissible event precedence. A strictly increasing label \(\lambda\) may parameterize an ordered path,

\[
\Gamma:\lambda\mapsto s(\lambda).
\]

The physical temporal measure will be constructed from the relational dynamics carried along this order.

## 2. Directed relational kinetics

For an admitted active pair \(a\leftrightarrow b\),

\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2},
\qquad
M_{ab}>0.
\]

Define activity and directed current,

\[
\boxed{
\mathfrak a_{ab}
=W_{a\to b}+W_{b\to a}
=2M_{ab}\cosh(A_{ab}/2)>0,
}
\]

\[
\boxed{
\mathfrak j_{ab}
=W_{a\to b}-W_{b\to a}
=2M_{ab}\sinh(A_{ab}/2).
}
\]

The normalized directed coordinate is

\[
\boxed{
\chi_{ab}
=\frac{\mathfrak j_{ab}}{\mathfrak a_{ab}}
=\tanh(A_{ab}/2),
\qquad -1<\chi_{ab}<1.
}
\]

The transition affinity in bits is

\[
\boxed{
\sigma_{ab}=\log_2\frac{W_{a\to b}}{W_{b\to a}},
\qquad
A_{ab}=(\ln2)\sigma_{ab}.
}
\]

Thus the same transition structure provides a positive symmetric channel \(\mathfrak a\) and an orientation channel \(\chi\).

## 3. Derivation of the temporal measure

Treat the transition weights as one-densities with respect to the ordering label. Under an increasing reparameterization

\[
\lambda'=f(\lambda),
\]

they transform as

\[
W'_\pm=W_\pm\frac{d\lambda}{d\lambda'}.
\]

Therefore

\[
\mathfrak a'
=\mathfrak a\frac{d\lambda}{d\lambda'}.
\]

Define

\[
\boxed{
d\Theta:=\mathfrak a\,d\lambda.}
\]

Then exactly

\[
\boxed{d\Theta'=d\Theta.}
\]

For an ordered interval \(\Gamma_{12}\),

\[
\boxed{
\Theta[\Gamma_{12}]
=\int_{\Gamma_{12}}\mathfrak a\,d\lambda.
}
\]

Positive activity makes this accumulated measure increase on active realized intervals. Concatenation gives

\[
\boxed{
\Theta[\Gamma_{13}]
=\Theta[\Gamma_{12}]+\Theta[\Gamma_{23}].
}
\]

This is the intrinsic duration coordinate of the present derivation.

Under reversal of transition orientation,

\[
A\mapsto-A,
\]

we have

\[
\boxed{d\Theta\mapsto d\Theta,}
\qquad
\boxed{\chi\mapsto-\chi.}
\]

The formalism therefore carries duration and orientation as distinct temporal coordinates.

## 4. Information, density and viscosity representation

The relational mobility is

\[
\boxed{
M_{ab}
=\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}.
}
\]

Using \(A=(\ln2)\sigma\),

\[
\boxed{
\frac{d\Theta}{d\lambda}
=
2\frac{\sqrt{\rho_R(a)\rho_R(b)}}{\tfrac12[\eta_R(a)+\eta_R(b)]}
\cosh\!\left(\frac{\ln2}{2}\sigma_{ab}\right),
}
\]

\[
\boxed{
\chi_{ab}
=\tanh\!\left(\frac{\ln2}{2}\sigma_{ab}\right).
}
\]

Hence the upstream temporal map is

\[
\boxed{
(\rho_R,\eta_R,\sigma)
\longmapsto
(d\Theta,\chi).
}
\]

The canonical information-phase normalization

\[
\boxed{
\kappa=\frac{\ln2}{24\pi}
}
\]

weights the Shannon/geometric phase-link sector, while the transition traffic supplies the duration measure.

## 5. Relational clocks and lapse

For two active subsystems \(x\) and \(r\) referred to the same ordering label,

\[
d\Theta_x=\mathfrak a_xd\lambda,
\qquad
d\Theta_r=\mathfrak a_rd\lambda.
\]

The intrinsic relative clock rate is

\[
\boxed{
N_R(x|r)
=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
}
\]

Reference changes compose multiplicatively,

\[
\boxed{
N_{x|s}=N_{x|r}N_{r|s}.
}
\]

A reference clock calibration introduces physical units,

\[
\boxed{
dt=T_r\,d\Theta_r,
\qquad T_r>0,
}
\]

and the local calibrated elapsed interval becomes

\[
\boxed{
d\hat\tau_x=N_R(x|r)\,dt.}
\]

The sequence is therefore

\[
\boxed{
\text{transition traffic}
\to d\Theta
\to N_R
\to d\hat\tau.
}
\]

## 6. Phase topology and temporal orientation

For the complex-state carrier, an admitted transition carries the composite link

\[
L_e
=G_e\exp\!\left[i\kappa(\Delta H_e+\sigma_e)\right].
\]

Exact Shannon state differences telescope on a closed cycle, while geometric holonomy and non-exact transition affinity survive as cycle data,

\[
\boxed{
\operatorname{Arg}\prod_{e\in C}L_e
=\gamma_B(C)+\kappa\sum_{e\in C}\sigma_e
\pmod{2\pi}.
}
\]

Thus the temporal architecture has two complementary orientation carriers:

\[
\chi=\tanh(A/2)
\]

locally on a directed active pair, and the connection/holonomy class on an extended relational cycle.

## 7. Tensor–scalar response

The state manifold response is

\[
\boxed{
\frac{dx}{d\lambda}
=-\operatorname{grad}_{g}\mathcal I
+J\operatorname{grad}_{g}\mathcal H_\alpha.
}
\]

The positive metric sector carries Shannon/Onsager informational descent; the compatible antisymmetric sector carries reversible phase response. The temporal response object is

\[
\boxed{
\mathcal T=(\mathfrak a,G+\Omega),
\qquad
\Omega=JG.
}
\]

The scalar entry \(\mathfrak a\) is now inherited from the activity-derived temporal primitive.

## 8. NOW as localized realized activity

The NOW layer localizes admitted temporal activity on event support. For an admitted event \(s_n\),

\[
\boxed{
\Psi_T(s_n^+)=B_n\Psi_T(s_n^-).
}
\]

The event support identifies where a realized update occurs. Its positive activity contributes to elapsed accumulation, while its directed coordinate and bifurcation operator carry the oriented state change.

For the reversible representation,

\[
B(q)=e^{qG},
\]

with the declared unitary subclass

\[
B_\phi(\beta)=e^{-i\beta G}.
\]

## 9. Transport between realized events

Between event surfaces,

\[
\boxed{
\Psi_{n+1}=U_n\Psi_n.
}
\]

An ordered history is the alternating composition

\[
\boxed{
\Psi_N
=U_{N-1}B_{N-1}\cdots U_2B_2U_1B_1\Psi_0.
}
\]

Each active segment carries an accumulated \(\Theta\)-interval. The transport layer therefore propagates state and phase across an intrinsically measured relational duration.

## 10. Memory as retained temporal lineage

Memory carries the consequences of admitted events forward through the ordered activity measure. ORCHORBITAL organizes the retained history by active attractor, elapsed segment, switch/leak state, winding and radial carrier.

For a retained event sequence,

\[
\boxed{
\alpha=(a_1,\ldots,a_N),
\qquad
\mathcal W=(\Delta W_1,\ldots,\Delta W_N),
}
\]

and 07V adds

\[
\boxed{
\mathcal R=(\rho_1,\ldots,\rho_N),
\qquad
\rho_k=\|r_k-c_{a_k}\|>0.
}
\]

The resulting lineage carries both ordered state history and the temporal activity accumulated across its segments.

## 11. Retrodiction

Retrodiction operates on retained temporal records. In the winding–radius architecture,

\[
(\alpha,\mathcal W,\rho_1,\ldots,\rho_{N-1},r_N)
\longmapsto
(r_1,\ldots,r_N)
\]

followed by the exact position-lineage inverse

\[
(r_1,\ldots,r_N)
\longmapsto
(u_1,\ldots,u_N).
\]

Spatial Offset Divergence audits collision fibers of compressed observation maps by comparing full hidden position histories. The activity-derived temporal coordinate supplies the corresponding elapsed lineage on the same ordered history.

## 12. Current derivational architecture

The current chain is

\[
\boxed{
\begin{aligned}
&\text{RELATIONAL ORDER + TRANSITION WEIGHTS}\\
&\downarrow\\
&\mathfrak a=W_++W_-,\qquad \mathfrak j=W_+-W_-\\
&\downarrow\\
&d\Theta=\mathfrak a\,d\lambda,\qquad
\chi=\mathfrak j/\mathfrak a\\
&\downarrow\\
&N_R=d\Theta_x/d\Theta_r\\
&\downarrow\\
&\text{CALIBRATED ELAPSED TIME + PHASE RATE}\\
&\downarrow\\
&\text{NOW}\to\text{BIFURCATION}\to\text{TRANSPORT}\\
&\downarrow\\
&\text{MEMORY}\to\text{RETRODICTION}.
\end{aligned}
}
\]

The typed temporal coordinates are

```text
precedence            : (S, prec)
transition traffic    : W_plus, W_minus
activity              : a = W_plus + W_minus > 0
directed current      : j = W_plus - W_minus
intrinsic duration    : dTheta = a d_lambda
orientation           : chi = j/a
relative clock rate   : N_R = dTheta_x / dTheta_ref
physical clock scale  : dt = T_ref dTheta_ref
calibrated elapsed    : d tau_hat = N_R dt
phase topology        : U(1) connection + Berry/affinity holonomy
realized event support: NOW
state update          : bifurcation B_n
inter-event evolution : transport U_n
retained history      : Memory / ORCHORBITAL lineage
inverse history map   : Retrodiction
```

This is the current mathematical candidate for deriving the temporal measure and its orientation from relational dynamics. Each physical identification retains the evidence status of its corresponding dependency gate.
