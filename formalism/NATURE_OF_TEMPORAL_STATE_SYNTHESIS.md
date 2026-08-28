# Nature of the Temporal State — IDT Synthesis

Status: `SYNTHESIS_OF_ADMITTED_STRUCTURAL_LAYERS`

This document collects the already developed temporal layers into one typed description of the temporal state architecture used by IDT. It is a synthesis layer: every displayed component is inherited from an existing formalism node and keeps that node's evidential status.

## 1. Ordered relational support

Let

\[
(S,\prec)
\]

be an ordered relational domain. A temporal state is represented by

\[
\boxed{\Psi:S\to\mathcal H.}
\]

The order relation supplies event precedence. State values live in the declared state space; precedence lives in the relational support.

## 2. Relational transition and phase

For an admitted relation \(a\to b\), Shannon-relative information and the phase-link construction supply a transition coordinate. The kinetic representation carries positive directed rates

\[
W_{a\to b}=M_{ab}e^{A_{ab}/2},
\qquad
W_{b\to a}=M_{ab}e^{-A_{ab}/2}.
\]

Define activity and directed current

\[
\boxed{\mathfrak a_{ab}=2M_{ab}\cosh(A_{ab}/2)>0,}
\]

\[
\boxed{\mathfrak j_{ab}=2M_{ab}\sinh(A_{ab}/2).}
\]

The pair separates two temporal roles:

- \(\mathfrak a\): positive transition activity and elapsed pace;
- \(\mathfrak j\): orientation of the directed transition.

Their ratio recovers the directed drive,

\[
\boxed{
A_{ab}=2\operatorname{artanh}\!\left(\frac{\mathfrak j_{ab}}{\mathfrak a_{ab}}\right).
}
\]

Thus pace and orientation are retained as separate typed coordinates.

## 3. NOW as localized event support

The NOW layer localizes admitted temporal activity on event support. For an admitted event \(s_n\), the pre-event and post-event states are related by a bifurcation operator

\[
\boxed{
\Psi_T(s_n^+)=B_n\Psi_T(s_n^-).
}
\]

Event localization and event orientation remain distinct: the event-support rule identifies where an update occurs, while the activity/current and bifurcation layers encode its directed action.

For the reference reversible representation,

\[
B(q)=e^{qG},
\]

and the declared unitary subclass is

\[
B_\phi(\beta)=e^{-i\beta G}.
\]

## 4. Transport between admitted events

Between event surfaces the temporal state is transported by the admitted temporal transport operator,

\[
\boxed{
\Psi_{n+1}=U_n\Psi_n.
}
\]

The ordered temporal history is therefore an alternating composition of continuous/inter-event transport and event-local bifurcation,

\[
\boxed{
\Psi_N
=
U_{N-1}B_{N-1}\cdots U_2B_2U_1B_1\Psi_0,
}
\]

with ordering inherited from \((S,\prec)\).

## 5. Internal elapsed time

IDT carries a positive internal elapsed one-form

\[
\boxed{
d\tau_{\rm int}=\phi\,d\lambda,
\qquad
\phi=\frac{\mathfrak a}{\mathfrak a_\star}>0.
}
\]

The ordering coordinate \(\lambda\) labels the relational path; \(d\tau_{\rm int}\) measures accumulated internal elapsed activity along that ordered path.

For a local subsystem and an admitted reference clock,

\[
d\tau_x=\phi_xd\lambda,
\qquad
d\tau_{\rm ref}=\phi_{\rm ref}d\lambda,
\]

the exact relational lapse ratio is

\[
\boxed{
N_R(x)=\frac{d\tau_x}{d\tau_{\rm ref}}
=\frac{\phi_x}{\phi_{\rm ref}}>0.
}
\]

It is invariant under the admitted increasing reparameterization of \(\lambda\), and clock changes compose multiplicatively,

\[
N_{x|s}=N_{x|r}N_{r|s}.
\]

After an explicit reference-clock calibration,

\[
dt=T_{\rm ref}d\tau_{\rm ref},
\]

the local calibrated elapsed interval is

\[
\boxed{d\hat\tau_x=N_Rdt.}
\]

## 6. Temporal phase rate and local clock rate

On the admitted zero-shift lapse/coframe bridge, the coordinate-time phase pullback and normal proper-time phase rate satisfy

\[
\boxed{r_t=N_Rr_n^{(\tau)}.}
\]

Equivalently,

\[
D_{\hat\tau}\chi=r_n^{(\tau)}.
\]

This binds phase evolution to the same relational lapse that compares local elapsed clocks.

## 7. Memory as retained temporal lineage

The Memory layer carries the state consequences of admitted events forward in internal elapsed activity. The ORCHORBITAL layer organizes that retained history by active attractor, elapsed segment, switch/leak state and signed winding.

For a retained event sequence, the residence lineage supplies

\[
\boxed{
\alpha=(a_1,\ldots,a_N),
\qquad
\mathcal W=(\Delta W_1,\ldots,\Delta W_N).
}
\]

07V adds the residence-bound radial lineage

\[
\boxed{
\mathcal R=(\rho_1,\ldots,\rho_N),
\qquad
\rho_k=\|r_k-c_{a_k}\|>0,
}
\]

with each radial coordinate content-bound to its event-residence cell and committed post-segment state.

The temporal state architecture therefore carries both current state and an authenticated ordered lineage sufficient for declared reconstruction gates.

## 8. Retrodiction as inverse history reconstruction

Retrodiction operates on retained temporal records. In the admitted winding–radius architecture, the fixed-stratum lift is

\[
(\alpha,\mathcal W,\rho_1,\ldots,\rho_{N-1},r_N)
\longmapsto
(r_1,\ldots,r_N),
\]

followed by the exact 07K inverse

\[
(r_1,\ldots,r_N)
\longmapsto
(u_1,\ldots,u_N).
\]

Spatial Offset Divergence audits collision fibers of compressed observation maps by comparing their full position histories. It therefore provides a direct diagnostic of history hidden by a chosen projection.

## 9. Typed temporal architecture

The synthesis can be summarized as

\[
\boxed{
\text{ORDER}
\to
\text{EVENT SUPPORT}
\to
\text{BIFURCATION}
\to
\text{TRANSPORT}
\to
\text{ELAPSED ACTIVITY}
\to
\text{MEMORY LINEAGE}
\to
\text{RETRODICTION}.
}
\]

The corresponding typed coordinates are:

```text
precedence          : (S, prec)
state               : Psi
activity / pace     : a > 0
directed current    : j
bifurcation         : B_n
transport           : U_n
internal elapsed    : d tau_int = phi d lambda
relational lapse    : N_R = d tau_x / d tau_ref
memory lineage      : event + residence commitments
history geometry    : alpha, winding, radial/position carrier
inverse history map : Retrodiction
```

This is the current IDT mathematical architecture for the nature of a temporal state. Physical calibration and downstream spacetime closure retain their own declared dependency gates.
