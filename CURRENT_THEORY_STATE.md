# CURRENT THEORY STATE

Status: `TEMPORAL_TRANSPORT_STRUCTURAL_PASS / MEMORY_ACTIVE / ORCHORBITAL_ATTRACTOR_REFERENCE_CANDIDATE / RETRODICTION_PROVISIONAL_DOWNSTREAM`

The canonical admitted frontier remains

\[
\boxed{\text{Temporal Primitive}\rightarrow\text{Temporal Wave}\rightarrow\text{NOW}\rightarrow\text{Bifurcation}\rightarrow\text{Temporal Transport}\rightarrow\mathbf{Memory}}
\]

The dependency path being developed downstream of the active Memory node is

\[
\boxed{
\mathrm{Memory}
\rightarrow
\mathrm{ORCHORBITAL\ Attractors}
\rightarrow
\mathrm{Retrodiction}.
}
\]

## Temporal-memory substrate

The active Memory reference branch uses internal elapsed activity and event-driven Kepler dynamics,

\[
\Delta\tau_{\rm int}=\frac{\mathfrak a}{\mathfrak a_\star}\Delta\lambda,
\qquad
\ddot m=-\mu_M\frac{m}{|m|^3},
\qquad
\Delta v_{M,n}=q_n\delta m_n.
\]

For the pure-state \(\mathbb{CP}^1\) reference subclass,

\[
|\delta m|=d_{FS}.
\]

Memory persistence uses the append-only receipt

\[
\mathcal E_n=(\Delta\tau_n,q_n,\delta m_n)
\]

and the reversible reference cell

\[
\mathcal C_n=\Phi_K(\Delta\tau_n;\mu_M)\circ K_{\mathcal E_n},
\qquad
\mathcal C_n^{-1}=K_{\mathcal E_n}^{-1}\circ\Phi_K^{-1}(\Delta\tau_n;\mu_M).
\]

## ORCHORBITAL attractor extension

For attractor

\[
\mathfrak A_i=(c_i,\mu_i),
\qquad \mu_i>0,
\]

the temporal-memory state is evaluated relative to every candidate centre by

\[
\boxed{
E_i=\frac12\|v_M\|^2-\frac{\mu_i}{\|m-c_i\|}
}
\]

and positive binding margin

\[
\boxed{b_i=[-E_i]_+.}
\]

When \(B=\sum_i b_i>0\), the ORCHORBITAL attractor weights are

\[
\boxed{w_i=\frac{b_i}{B}},
\qquad
\boxed{a=\arg\max_i w_i}.
\]

For \(B=0\), the field state is `LEAK_MODE`.

The attractor-weight distribution carries Shannon organization,

\[
\boxed{H_A=-\sum_{i:w_i>0}w_i\log_2w_i},
\]

with normalized coherence for \(N>1\),

\[
\boxed{C_A=1-\frac{H_A}{\log_2N}}.
\]

During one admitted smooth segment the selected attractor defines the translated Kepler law

\[
\boxed{
\frac{d^2m}{d\tau_{\rm int}^2}
=-\mu_a\frac{m-c_a}{\|m-c_a\|^3}.
}
\]

The orbital winding increment is

\[
\boxed{
\Delta W_a
=\frac{1}{2\pi}\operatorname{wrap}(\theta_{n+1}-\theta_n),
\qquad
\theta_n=\arg(m_n-c_a).
}
\]

After every segment the attractor field is re-evaluated. A changed maximizing basin is recorded as the next attractor-switch candidate. Thus the first ORCHORBITAL temporal-memory chain is

\[
\boxed{
NOW
\rightarrow
\Delta M
\rightarrow
q\delta m
\rightarrow
X_M
\rightarrow
\{E_i,b_i,w_i\}
\rightarrow
\text{attractor}
\rightarrow
\text{orbit / winding}
\rightarrow
\text{re-evaluation}.
}
\]

## Retrodiction downstream staging

The tested Retrodiction stack remains provisional downstream and includes withheld-lineage inversion, observability/rank admission, checkpoint selection, estimation, covariance/Fisher uncertainty geometry and covariance-preserving permutation nulls. It consumes the admitted Memory/ORCHORBITAL path and does not redefine the upstream temporal primitives.

Parent Memory admission still requires a real full repository reference-suite result. The presence of tested ORCHORBITAL and Retrodiction implementations therefore does not by itself move the canonical admitted frontier beyond Memory.
