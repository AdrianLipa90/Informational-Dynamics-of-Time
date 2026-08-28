# 01AC — Gauge-Covariant Phase Pullback and Noether Generator

Status: `GAUGE_COVARIANT_PULLBACK_EXACT_PASS_CONDITIONAL / SAME_U1_BUNDLE_ADMISSION_OPEN / RFC_CURRENT_PROMOTION_OPEN`

01AC follows 01AB and resolves the sign/convention layer required to compare the Euler–Noether scalar-field phase with the canonical rotor phase coordinate.

The construction uses the same `U(1)` bundle and the same Aharonov–Bohm–Berry–Euler connection already present in the phase Hamiltonian scaffold.

## 1. Connection convention from the admitted Berry definition

The admitted Berry connection is

\[
\mathcal A_B=i\langle u|du\rangle.
\]

Under a local section change

\[
|u\rangle\mapsto |u'\rangle=e^{i\lambda}|u\rangle,
\]

direct substitution gives

\[
\boxed{\mathcal A_B' = \mathcal A_B-d\lambda.}
\]

The same local `U(1)` convention is used for the total admitted phase connection

\[
\mathcal A^{ABE}=\mathcal A_{AB}+\mathcal A_B+\mathcal A_E,
\]

so on a common local trivialization

\[
\boxed{\mathcal A^{ABE}\mapsto \mathcal A^{ABE}-d\lambda.}
\]

For a local scalar-field phase coordinate

\[
\psi=Ae^{i\vartheta},
\qquad
\vartheta\mapsto\vartheta+\lambda,
\]

the gauge-invariant phase one-form is therefore

\[
\boxed{
\mathscr D\vartheta:=d\vartheta+\mathcal A^{ABE}.}
\]

Indeed,

\[
\mathscr D\vartheta'
=d(\vartheta+\lambda)+\mathcal A^{ABE}-d\lambda
=\mathscr D\vartheta.
\]

This fixes the `+` sign from the admitted connection convention.

## 2. Covariant scalar-field phase sector

Define the covariant derivative on the charged local section by

\[
\boxed{
\mathcal D_\mu\psi
=(\partial_\mu+i\mathcal A^{ABE}_\mu)\psi.}
\]

Then

\[
\mathcal D_\mu\psi
=e^{i\vartheta}
\left[
\partial_\mu A
+iA\bigl(\partial_\mu\vartheta+\mathcal A^{ABE}_\mu\bigr)
\right].
\]

Hence the covariant phase kinetic term is

\[
(\mathcal D_\mu\psi)^*\mathcal D^\mu\psi
=(\partial_\mu A)(\partial^\mu A)
+A^2\mathscr D_\mu\vartheta\,\mathscr D^\mu\vartheta.
\]

The phase current associated with the common `U(1)` action is

\[
\boxed{
J_\vartheta^\mu
=i\left(
\psi\,(\mathcal D^\mu\psi)^*
-\psi^*\mathcal D^\mu\psi
\right)
=2A^2\mathscr D^\mu\vartheta.}
\]

## 3. Pullback to the canonical rotor trajectory

Let

\[
q:\tau\mapsto q(\tau)
\]

be the relational trajectory and let the canonical rotor coordinate \(\chi(\tau)\) be the pullback of the same local `U(1)` fiber coordinate used by \(\vartheta\), up to one constant phase offset on the chosen patch:

\[
\boxed{
\chi(\tau)=\vartheta(q(\tau))+\chi_0.}
\]

Then

\[
\dot\chi
=\partial_a\vartheta\,\dot q^a,
\]

and the pullback of the gauge-invariant phase one-form is

\[
q^*(\mathscr D\vartheta)
=
\left(\partial_a\vartheta+\mathcal A^{ABE}_a\right)\dot q^a\,d\tau.
\]

Therefore

\[
\boxed{
q^*(\mathscr D\vartheta)
=D_\tau\chi\,d\tau,}
\]

with

\[
\boxed{
D_\tau\chi
=\dot\chi+\mathcal A^{ABE}_a\dot q^a.}
\]

The rate equality is thus a pullback identity after the same-bundle/same-coordinate admission.

## 4. Full collective reduction of the field action

On a collective phase mode with one common positive pullback rate

\[
r:=D_\tau\chi=q^*(\mathscr D\vartheta)(\partial_\tau),
\]

the pure phase contribution reduces to

\[
L_{\rm phase}^{field}
=\int_\Sigma A^2r^2\,dV_h.
\]

Define

\[
C_A:=\int_\Sigma A^2dV_h,
\qquad
I_A:=2C_A.
\]

Then

\[
\boxed{
L_{\rm phase}^{field}
=\frac{I_A}{2}r^2.}
\]

Comparing with the independently supplied canonical rotor coefficient

\[
L_{\rm phase}^{rotor}
=\frac{I_\phi}{2}r^2
\]

gives the 01AB result

\[
\boxed{I_\phi=I_A}
\]

inside the admitted common reduction.

## 5. Noether generator equals rotor kinetic generator

For a slice whose unit normal follows the collective phase evolution,

\[
n_\mu\mathscr D^\mu\vartheta=r,
\]

the finite Noether charge is

\[
Q_\vartheta
=\int_\Sigma n_\mu J_\vartheta^\mu\,dV_h
=\int_\Sigma 2A^2r\,dV_h
=I_A r.
\]

The canonical rotor kinetic generator is

\[
P_\Phi:=J-J_I=I_\phi r.
\]

Using \(I_\phi=I_A\),

\[
\boxed{
Q_\vartheta=P_\Phi=J-J_I.}
\]

Thus the field and rotor moment maps for the admitted common `U(1)` action coincide on the collective reduction.

After Euler/Berry closure,

\[
\boxed{
Q_\vartheta^{EB}=P_\Phi^{EB}=J-J_I^{EB}.}
\]

## 6. Energy-per-carrier consequence

The rotor phase energy is

\[
H_\Phi^{EB}
=\frac{(P_\Phi^{EB})^2}{2I_\phi}.
\]

On the positive carrier sector,

\[
\epsilon_N^{EB}
:=\frac{H_\Phi^{EB}}{Q_\vartheta^{EB}},
\]

so the common-generator theorem gives

\[
\boxed{
\epsilon_N^{EB}
=\frac{P_\Phi^{EB}}{2I_\phi}
=\frac12D_\tau\chi.}
\]

This reproduces the 01AB normalization through an independent gauge-covariant route.

## 7. Admission and falsification coordinates

The executable interface should keep the following gates separate:

\[
\Delta_{bundle},\qquad
\Delta_{phase},\qquad
\Delta_{conn},\qquad
\Delta_{rate},\qquad
\Delta_{normal},\qquad
\Delta_Q.
\]

A finite-cell implementation may use

\[
\Delta_{rate}
:=
\frac{|r_{field}-r_{rotor}|}{|r_{rotor}|},
\]

\[
\Delta_Q
:=
\frac{|Q_\vartheta-P_\Phi|}{|P_\Phi|},
\]

with explicit identity checks for bundle ID, local phase patch, connection ID, slice normal, measure ID and ordered support.

The exact theorem is admitted on the common zero-defect surface

\[
\boxed{
\Delta_{bundle}=\Delta_{phase}=\Delta_{conn}
=\Delta_{rate}=\Delta_{normal}=\Delta_Q=0.}
\]

## 8. Downstream RFC promotion

01AC supplies a gauge-covariant field↔rotor generator bridge. 01AA remains the measured RFC current/measure gate.

After the 01AC common-`U(1)` admission and the downstream RFC current promotion,

\[
Q_\Sigma=Q_\vartheta=P_\Phi^{EB}
\]

and the RFC normalization candidate is

\[
\boxed{
\epsilon_Q
=\epsilon_N^{EB}
=\frac12D_\tau\chi.}
\]

The physical `J_Q^\mu <-> J_\vartheta^\mu` promotion remains a measured gate.

## 9. Proposed PNCS executable contract

Proposed contract:

`PNCS_PNV_GAUGE_COVARIANT_PHASE_PULLBACK_V0_1`

Proposed semantic loop:

`SOURCE.PHASE.NOETHER.GAUGE_COVARIANT_PULLBACK.ROUNDTRIP`

The loop should receive field phase, gauge transformation, connection, trajectory/rate, field amplitudes/measure, independent rotor inertia and rotor momentum as separate inputs, then audit gauge invariance, pullback equality, reduced-action coefficient matching and generator equality without constructing any of those equalities by assignment.
