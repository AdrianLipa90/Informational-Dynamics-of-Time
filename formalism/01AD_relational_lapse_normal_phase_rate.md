# 01AD — Relational-Lapse Normal Phase-Rate Bridge

Status: `ZERO_SHIFT_LAPSE_NORMAL_RATE_EXACT_CONDITIONAL / PHYSICAL_CLOCK_CALIBRATION_GATE_INHERITED / RFC_CURRENT_PROMOTION_OPEN`

01AD follows 01AC. It binds the gauge-covariant field↔rotor bridge to the activity-derived relational lapse and the RFC zero-shift temporal coframe.

## 1. Activity-derived elapsed-clock relation

00E and 05C supply

\[
\boxed{
d\Theta_x=\mathfrak a_xd\lambda,
\qquad
d\Theta_r=\mathfrak a_rd\lambda,
}
\]

and therefore

\[
\boxed{
N_R(x|r)=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}>0.
}
\]

After reference-clock calibration

\[
\boxed{dt=T_r\,d\Theta_r,}
\]

the local calibrated elapsed interval is

\[
\boxed{d\hat\tau=N_Rdt.}
\]

The clock ratio is reparameterization invariant and the conversion scale \(T_r\) supplies physical clock units.

## 2. Zero-shift temporal coframe

RFC RF-N0 exports the zero-shift temporal coframe candidate

\[
\boxed{
\mathcal E^0=N_Rc\,dt.
}
\]

Its dual unit-time frame vector is

\[
\boxed{
e_{\hat0}=\frac{1}{N_Rc}\partial_t.
}
\]

For the dimensionless phase one-form \(\mathscr D\vartheta\), define

\[
\boxed{
r_n^{(\tau)}:=c\,e_{\hat0}\lrcorner\mathscr D\vartheta.
}
\]

Hence on the zero-shift coframe,

\[
\boxed{
r_n^{(\tau)}=\frac{1}{N_R}\mathscr D_t\vartheta.
}
\]

## 3. Coordinate-time pullback

01AC supplies the common-\(U(1)\) pullback. Parameterizing the relational trajectory by calibrated coordinate time \(t\), define

\[
\boxed{
r_t:=q^*(\mathscr D\vartheta)(\partial_t).}
\]

On an admitted local patch,

\[
r_t
=\partial_t\vartheta
+\mathcal A^{ABE}_a\frac{dq^a}{dt}.
\]

The rotor pullback in coordinate time is

\[
\boxed{D_t\chi=r_t.}
\]

## 4. Proper-time rotor rate

From

\[
d\hat\tau=N_Rdt,
\]

the chain rule gives

\[
\boxed{
D_{\hat\tau}\chi
=\frac{1}{N_R}D_t\chi
=\frac{1}{N_R}r_t.
}
\]

Combining this with the coframe expression gives

\[
\boxed{
D_{\hat\tau}\chi
=r_n^{(\tau)}
=c\,e_{\hat0}\lrcorner\mathscr D\vartheta.
}
\]

Equivalently,

\[
\boxed{r_t=N_Rr_n^{(\tau)}.}
\]

## 5. Executable defects

The lapse-rate defect is

\[
\boxed{
\Delta_{N\!r}
:=\frac{|r_t-N_Rr_n^{(\tau)}|}{|r_t|}.
}
\]

The proper-rate comparison defect is

\[
\boxed{
\Delta_{\tau n}
:=\frac{|D_{\hat\tau}\chi-r_n^{(\tau)}|}
{|D_{\hat\tau}\chi|}.
}
\]

Both vanish on the admitted zero-shift calibrated-clock bridge.

## 6. Noether generator consequence

01AB supplies

\[
I_A=I_\phi.
\]

Therefore

\[
Q_\vartheta=I_A r_n^{(\tau)},
\qquad
P_\Phi=I_\phi D_{\hat\tau}\chi,
\]

and the proper-rate identity gives

\[
\boxed{Q_\vartheta=P_\Phi.}
\]

After Euler/Berry closure,

\[
\boxed{Q_\vartheta^{EB}=P_\Phi^{EB}=J-J_I^{EB}.}
\]

## 7. Energy-per-carrier coordinate

On the positive carrier sector,

\[
\epsilon_N^{EB}
=\frac{H_\Phi^{EB}}{Q_\vartheta^{EB}}
=\frac12D_{\hat\tau}\chi.
\]

Using the lapse relation,

\[
\boxed{
\epsilon_N^{EB}
=\frac{1}{2N_R}D_t\chi
=\frac{r_t}{2N_R}.
}
\]

Thus the phase energy-per-carrier coordinate inherits the activity-derived relative clock normalization through \(N_R\).

## 8. Admission surface

The theorem uses the common \(U(1)\) bundle/patch/ABE connection from 01AC, the 00E/05C activity-derived clock ratio, reference-clock calibration into coordinate \(t\), the RF-N0 zero-shift temporal coframe, the 01AB scalar-field/rotor reduction and common measure/support for the finite generator. The physical RFC current identity retains its downstream measured gate.

## 9. PNCS contract

Proposed contract:

`PNCS_PNV_RELATIONAL_LAPSE_NORMAL_PHASE_RATE_V0_1`

Proposed semantic loop:

`SOURCE.PHASE.NOETHER.RELATIONAL_LAPSE_NORMAL_RATE.ROUNDTRIP`

The executable state receives `N_R`, coordinate-time pullback rate, independently evaluated normal proper-time rate, independently evaluated rotor proper-time rate, clock/coframe IDs and finite inertia/generator coordinates. It audits the lapse-rate identity and generator consequence by independent comparison.
