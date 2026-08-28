# 02JF — TIR Half-Fiber Temporal Normalization Bridge

Status: `FORMAL_CANDIDATE / CROSS_REPOSITORY_TYPED_BRIDGE`

This gate consumes the TIR half-fiber export while preserving repository authority boundaries. TIR owns the first-distinction theorem, the coherent `U(1)` half-fiber, the absolute phase-rate underdetermination theorem, and the common-cycle relative-rate theorem. IDT owns the activity-derived intrinsic temporal measure and its downstream clock calibration.

Pinned TIR candidate source for this bridge:

```text
repository = AdrianLipa90/The-Fundamental-Theory-of-Informational-Relations
PR         = #96
branch     = feat/tir-relational-half-seam-v0.1
head       = 46ad51b19471be509cda536365af77998996e5b7
```

## 1. TIR export packet

The TIR first-distinction chain supplies

\[
\boxed{
0_{\rm distinction}
\to 2
\to \frac12
\to \ln2
\to \mathbb C^2
\to U(1)_{1/2}.
}
\]

The coherent half-fiber is

\[
\boxed{
|\psi_{1/2}(\varphi)\rangle
=\frac{|N\rangle+e^{i\varphi}|S\rangle}{\sqrt2}.
}
\]

TIR also supplies

\[
\boxed{d\mathcal I=\kappa\,d\varphi,\qquad
\kappa=\frac{\ln2}{24\pi}.}
\]

For an arbitrary positive group parameter `lambda`, write

\[
\boxed{
\omega_\lambda:=\frac{d\varphi}{d\lambda}.
}
\]

The TIR rate no-go theorem states that the static half-fiber does not select a unique absolute numerical value of this rate because

\[
\lambda'=f(\lambda)
\quad\Longrightarrow\quad
\omega_{\lambda'}
=\omega_\lambda\frac{d\lambda}{d\lambda'}.
\]

The geometric orbit remains the same.

## 2. IDT intrinsic temporal measure

00E supplies the activity-derived invariant measure

\[
\boxed{
d\Theta=\mathfrak a\,d\lambda,
\qquad
\mathfrak a=W_++W_->0.
}
\]

Under the same increasing reparameterization,

\[
\boxed{
\mathfrak a'
=\mathfrak a\frac{d\lambda}{d\lambda'}.
}
\]

Hence `dTheta` is invariant.

## 3. Intrinsic phase rate

Define the phase rate per unit intrinsic temporal measure by

\[
\boxed{
\Omega_\Theta
:=\frac{d\varphi}{d\Theta}
=\frac{d\varphi/d\lambda}{d\Theta/d\lambda}
=\frac{\omega_\lambda}{\mathfrak a}.
}
\]

Under `lambda -> lambda'`,

\[
\Omega_\Theta'
=\frac{
\omega_\lambda(d\lambda/d\lambda')
}{
\mathfrak a(d\lambda/d\lambda')
}
=\Omega_\Theta.
\]

Therefore

\[
\boxed{
\Omega_\Theta
\text{ is invariant under every admitted increasing reparameterization.}
}
\]

This is the precise IDT normalization of the free TIR group-rate coordinate.

## 4. Intrinsic information rate

Since

\[
d\mathcal I=\kappa d\varphi,
\]

the information rate per intrinsic temporal measure is

\[
\boxed{
\Gamma_{\mathcal I}^{(\Theta)}
:=\frac{d\mathcal I}{d\Theta}
=\kappa\Omega_\Theta.
}
\]

Thus the TIR phase-information identity survives the temporal normalization exactly.

## 5. Relative clocks and the existing lapse bridge

For local subsystem `x` and reference subsystem `r`,

\[
d\Theta_x=\mathfrak a_xd\lambda,
\qquad
d\Theta_r=\mathfrak a_rd\lambda,
\]

so

\[
\boxed{
N_R(x|r)=\frac{d\Theta_x}{d\Theta_r}
=\frac{\mathfrak a_x}{\mathfrak a_r}.
}
\]

Let the reference clock calibration be

\[
\boxed{dt=T_r d\Theta_r,\qquad T_r>0.}
\]

Then the calibrated local interval is

\[
\boxed{d\hat\tau_x=N_Rdt=T_r d\Theta_x.}
\]

For a phase coordinate carried by subsystem `x`,

\[
\boxed{
\frac{d\varphi}{d\hat\tau_x}
=\frac{1}{T_r}\Omega_{\Theta,x}.
}
\]

and

\[
\boxed{
\frac{d\varphi}{dt}
=N_R\frac{d\varphi}{d\hat\tau_x}.
}
\]

This reproduces the structural form of the existing 01AD lapse/normal-rate bridge,

\[
\boxed{r_t=N_Rr_n^{(\tau)}}.
\]

The new result identifies the upstream origin of the normalized phase-rate coordinate as the TIR half-fiber rate divided by the IDT activity density.

## 6. Common-cycle winding ratios before clock calibration

TIR A5–A6 allow two phase fibers closing on the same oriented relational cycle `C` to carry integer windings

\[
\oint_Cd\varphi_i=2\pi m_i,
\qquad
\oint_Cd\varphi_j=2\pi m_j.
\]

Therefore, for `m_j != 0`,

\[
\boxed{
R_{ij}[C]
=\frac{\oint_Cd\varphi_i}{\oint_Cd\varphi_j}
=\frac{m_i}{m_j}.
}
\]

Using the common intrinsic temporal interval

\[
\Delta\Theta_C=\int_Cd\Theta,
\]

define cycle-averaged intrinsic rates

\[
\bar\Omega_{\Theta,i}
=\frac{2\pi m_i}{\Delta\Theta_C},
\qquad
\bar\Omega_{\Theta,j}
=\frac{2\pi m_j}{\Delta\Theta_C}.
\]

Then exactly

\[
\boxed{
\frac{\bar\Omega_{\Theta,i}}
{\bar\Omega_{\Theta,j}}
=\frac{m_i}{m_j}.
}
\]

Thus the winding arithmetic fixes relative average intrinsic phase rates while the common physical unit scale remains downstream of clock calibration.

## 7. Connection to half-frame modular support

02J/02JE use the finite frame-budget coordinate

\[
\boxed{\Phi_N=2\pi N.}
\]

The TIR first distinction supplies the symmetric share `1/2`; IDT 02J represents each full frame by two equal half-supports. The typed crosslink is

\[
\boxed{
\text{TIR symmetric first distinction }\frac12
\dashrightarrow
\text{IDT equal half-support split}.
}
\]

For `N` frame closures,

\[
\Phi_N=2\pi N
\]

and the half-frame quotient gives

\[
\boxed{2N-(N-1)=N+1}
\]

glued supports,

\[
|1|\,|12|\,|23|\cdots|N|.
\]

This crosslink explains why the equal half split is the natural TIR-fed candidate in the IDT modular realization while leaving its physical spinorial identification to the separately declared gate.

## 8. Local seam phase versus global frame budget

02JD carries an edge-native seam phase

\[
L_n=e^{i\varphi_n}
\]

and the gauge-invariant mismatch

\[
\delta_n=\alpha_{n+1}-\alpha_n-\varphi_n.
\]

The TIR half-fiber phase `varphi` and the IDT seam phase `varphi_n` share the same `U(1)` carrier type. A physical identification of a particular TIR fiber with a particular temporal seam requires an explicit binding map.

The global frame-count phase budget

\[
\Phi_N=2\pi N
\]

remains separately typed from each local seam phase.

## 9. Four-pi double-cover boundary

02JE proves algebraically that the half-link representation

\[
e^{\pm i\varphi/2}
\]

changes sign after `2pi` and returns after `4pi`, while quadratic seam observables return after `2pi`.

The TIR quantum half-fiber supplies a two-state complex carrier `C^2` and Bloch-equator `U(1)` phase family. The exact common algebraic signature is therefore available for comparison, but a physical spin-1/2 identification remains downstream of an explicit state/transformation-law binding.

## 10. Authority and evidence boundary

The bridge preserves the following authority split:

```text
TIR:
  first distinction -> 2 -> 1/2 -> ln2
  C^2 quantum carrier
  U(1) half-fiber
  absolute phase-rate no-go
  common-cycle winding-ratio theorem

IDT:
  dTheta = activity d_lambda
  Omega_Theta = dphi/dTheta
  relational lapse N_R
  clock calibration T_r
  half-frame support quotient
  phase-aware temporal seams
```

The current bridge claims an exact algebraic normalization identity conditional on the declared TIR and IDT inputs. Physical clock units, spinorial identification and microscopic seam-source identification retain their downstream gates.

## 11. Next gate

The next derivational question is whether the phase-aware half-seam dynamics supplies a synchronization law that turns the TIR common-cycle average ratio

\[
m_i/m_j
\]

into a local phase-locking relation while preserving gauge covariance and the absolute-rate scale boundary.

Reference implementation: `src/idt/tir_half_fiber_temporal_normalization.py`.
Reference tests: `tests/reference/test_tir_half_fiber_temporal_normalization.py`.
Validation receipt: `validation/TIR_HALF_FIBER_TEMPORAL_NORMALIZATION_V0_1.json`.
