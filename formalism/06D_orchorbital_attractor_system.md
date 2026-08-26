# 06D — ORCHORBITAL Attractor System on Temporal Memory

Status: `PROVISIONAL_MEMORY_EXTENSION_REFERENCE_CLASS`

Dependency position:

\[
\mathrm{Temporal\ Transport}
\rightarrow
\mathrm{Memory}
\rightarrow
\mathrm{ORCHORBITAL\ Attractor\ System}
\rightarrow
\mathrm{Retrodiction}.
\]

This layer maps the established ORCHORBITAL vocabulary of `Attractor`, `Orbit`, attractor weights, winding, leak mode and closure defect onto the event-driven temporal-memory state already present in this repository. The admitted reference substrate is the Kepler--Newton memory state

\[
X_M=(m,v_M,\tau_{\rm int},\mathcal A_M),
\qquad m\in\mathbb R^2\simeq\mathbb C.
\]

The first typed integration keeps each smooth admitted segment single-centred and allows the active centre to change only at a segment boundary after the attractor field is re-evaluated. This preserves the previously tested single-centre Kepler reference dynamics inside each orbital segment.

## 1. Attractor specification

An ORCHORBITAL memory attractor is represented by

\[
\boxed{\mathfrak A_i=(c_i,\mu_i)},
\qquad
c_i\in\mathbb R^2,
\quad
\mu_i>0.
\]

For memory state \((m,v_M)\), define the relative radius and the specific Kepler energy with respect to attractor \(i\):

\[
r_i=\|m-c_i\|,
\qquad
\boxed{
E_i=\frac12\|v_M\|^2-\frac{\mu_i}{r_i}.
}
\]

The positive binding margin is

\[
\boxed{b_i=[-E_i]_+=\max(0,-E_i).}
\]

This turns the existing bound/unbound Kepler classification into a multi-attractor admission observable.

## 2. Attractor weights and active basin

Let

\[
B=\sum_i b_i.
\]

For \(B>0\), define the normalized attractor weights

\[
\boxed{w_i=\frac{b_i}{B}},
\qquad
\sum_i w_i=1.
\]

The active attractor is the maximum-binding reference basin,

\[
\boxed{a=\arg\max_i w_i.}
\]

The implementation resolves an exact numerical tie deterministically by attractor name so replay remains reproducible.

For \(B=0\), the ORCHORBITAL field state is

`LEAK_MODE`.

In the v0.1 reference operator, `LEAK_MODE` terminates orbital-step admission for that state and is returned as an explicit fail-closed branch status. A leak-transport law may be introduced later as its own typed contract.

## 3. Shannon organization of attractor occupancy

The attractor weights supply a relational probability distribution over the currently bound basins. Define

\[
\boxed{
H_A=-\sum_{i:w_i>0}w_i\log_2w_i.
}
\]

For \(N>1\) declared attractors, define the normalized attractor coherence

\[
\boxed{
C_A=1-\frac{H_A}{\log_2N}.
}
\]

For a single declared attractor, \(C_A=1\). Thus the ORCHORBITAL basin state has a direct Shannon observable inherited from the same informational foundation used by the temporal branch.

## 4. Active-attractor orbital segment

During one admitted smooth segment with active attractor \(a\), the memory coordinate evolves relative to its selected centre:

\[
\boxed{
\frac{d^2m}{d\tau_{\rm int}^2}
=-\mu_a\frac{m-c_a}{\|m-c_a\|^3}.
}
\]

Equivalently, with \(r_a=m-c_a\),

\[
\ddot r_a=-\mu_a\frac{r_a}{\|r_a\|^3}.
\]

The reference implementation obtains this exactly by translating the already tested `kepler_memory_step` into the active attractor frame and translating the resulting position back. The internal elapsed activity \(\tau_{\rm int}\) remains the independent parameter of the memory orbit.

After the segment, the attractor field is evaluated again. If its maximizing basin differs from the centre used for the completed segment, the step records an attractor-switch candidate. The next segment therefore begins from the newly evaluated field state.

## 5. Winding

For an admitted segment around centre \(c_a\), let

\[
\theta_n=\arg(m_n-c_a).
\]

The branch-safe winding increment is

\[
\boxed{
\Delta W_a
=\frac{1}{2\pi}
\operatorname{wrap}_{(-\pi,\pi]}
(\theta_{n+1}-\theta_n).
}
\]

A trajectory winding observable is the ordered sum of these increments over consecutive segments assigned to the same attractor.

## 6. Closure defect

For an explicitly declared position scale \(r_* > 0\) and velocity scale \(v_* > 0\), the dimensionless phase-space closure defect is

\[
\boxed{
D_{\rm cl}
=
\sqrt{
\left(\frac{\|m_f-m_i\|}{r_*}\right)^2
+
\left(\frac{\|v_f-v_i\|}{v_*}\right)^2
}.
}
\]

The scales are inputs to the observable rather than hidden normalization choices.

## 7. Event and attractor ordering

The existing memory event law remains

\[
\Delta v_{M,n}=q_n\delta m_n.
\]

The ORCHORBITAL integration consumes the resulting memory phase state. The causal ordering is therefore

\[
\boxed{
NOW
\rightarrow
\Delta M_n
\rightarrow
q_n\delta m_n
\rightarrow
X_M^+
\rightarrow
\{E_i,b_i,w_i\}
\rightarrow
a_n
\rightarrow
\text{orbital segment in }\tau_{\rm int}.
}
\]

Attractor organization is downstream of the already registered event imprint and memory kick. It does not redefine NOW or the temporal-transport operator.

## 8. ORCHORBITAL scope retained for later typed mapping

The existing ORCHORBITAL foundation also carries hierarchical sphere/entity structure, truth scalar, global coherence, semantic mass and reduction-readiness observables. This repository first admits the temporal-memory mapping of attractors, orbit, winding, leak mode, basin weights and closure defect. The remaining ORCHORBITAL observables retain their upstream definitions until a dependency-compatible typed map is derived here.

## 9. Evidence boundary

Reference implementation:

`src/idt/orchorbital.py`

Targeted controls:

`tests/reference/test_orchorbital.py`

Native declaration:

`operators/orchorbital_attractor_v01.pnv`

Validation receipt:

`validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json`

This layer is a formal/reference candidate inside the Memory extension path. Physical interpretation and later attractor-to-retrodiction performance claims require their own evidence and admission receipts.
