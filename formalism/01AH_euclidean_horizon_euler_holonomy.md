# 01AH — Euclidean-Horizon Euler Holonomy

Status: `EXACT_EUCLIDEAN_REGULARITY_THEOREM / EXACT_EULER_WINDING_CLOSURE / AB_HOLONOMY_ISOMORPHISM_CANDIDATE / MICROSCOPIC_HAWKING_CHANNEL_BINDING_OPEN`

01AH develops the horizon-side relational isomorphism suggested by the Aharonov–Bohm route. The exact theorem is geometric: regularity of a non-extremal Euclidean horizon fixes a `2π` winding. The comparison with the electromagnetic Aharonov–Bohm loop is an isomorphism of `U(1)` holonomy structure, not an identification of the electromagnetic potential with the gravitational horizon connection.

## 1. Near-horizon Euclidean geometry

For a non-extremal stationary horizon with surface-gravity parameter `kappa_H > 0`, the Euclidean near-horizon two-plane can be written locally as

\[
\boxed{
 ds_E^2=d\rho^2+\rho^2\,d\Theta_H^2+\cdots,
 \qquad
 \Theta_H:=\kappa_H\tau_E
}
\]

in natural units. Here `tau_E` is Euclidean time and `rho=0` is the horizon cap.

Smooth polar geometry requires

\[
\boxed{\Theta_H\sim\Theta_H+2\pi.}
\]

Therefore the fundamental Euclidean period is

\[
\boxed{\beta_H=\frac{2\pi}{\kappa_H}.}
\]

## 2. Euler winding closure

Define the horizon Euler phase

\[
\boxed{
\Phi_H:=\int_0^{\beta_H}\kappa_H\,d\tau_E.
}
\]

Then exactly

\[
\boxed{\Phi_H=\kappa_H\beta_H=2\pi.}
\]

The corresponding holonomy is

\[
\boxed{
W_H:=e^{i\Phi_H}=1.
}
\]

More generally, an `n`-fold cover obeys

\[
\Phi_H^{(n)}=2\pi n,
\qquad
W_H^{(n)}=1,
\]

while the primitive smooth thermal circle is the `n=1` sector.

## 3. Conical-defect coordinate

For an independently supplied Euclidean period `beta`, define

\[
\boxed{
\delta_{cone}:=2\pi-\kappa_H\beta.
}
\]

The regularity gate is

\[
\boxed{\delta_{cone}=0.}
\]

Thus the Euler closure defect is literally the Euclidean conical defect in the near-horizon plane.

## 4. Hawking temperature from the primitive winding

Thermal Euclidean periodicity gives

\[
\boxed{T_H=\beta_H^{-1}=\frac{\kappa_H}{2\pi}}
\]

in units `hbar=c=k_B=1`. Restoring constants when `kappa_H` is a physical acceleration gives

\[
\boxed{
T_H=\frac{\hbar\kappa_H}{2\pi c k_B}.
}
\]

Therefore the horizon temperature is fixed by the primitive Euler winding closure of the Euclidean thermal circle.

## 5. Aharonov–Bohm holonomy isomorphism

For the electromagnetic Aharonov–Bohm connection,

\[
\boxed{
\Phi_{AB}[C]=\frac q\hbar\oint_C A,
\qquad
W_{AB}[C]=e^{i\Phi_{AB}[C]}.
}
\]

The horizon thermal circle has

\[
\boxed{
\Phi_H[C_H]=\oint_{C_H}\omega_H,
\qquad
\omega_H:=\kappa_H d\tau_E,
\qquad
W_H[C_H]=e^{i\Phi_H[C_H]}.
}
\]

The structural map is therefore

\[
\boxed{
\frac q\hbar A
\;\longleftrightarrow\;
\omega_H=\kappa_H d\tau_E,
\qquad
\oint_C\;\longleftrightarrow\;\oint_{C_H},
\qquad
U(1)\text{ phase}\;\longleftrightarrow\;U(1)\text{ phase}.
}
\]

Both sides are closed-loop phase holonomies and both admit an Euler winding description. Their physical connections remain separately typed.

## 6. Relation to the existing Euler–Berry horizon programme

The project already uses global Euler phase closure and winding sectors to organize multiple phase contributions. 01AH supplies a standard geometric horizon anchor for that language: the Euclidean thermal circle itself has a primitive `2π` winding.

A later microscopic Hawking-channel theorem may compare the project’s internal phase-information transport to this exact horizon winding and thermal period. Such a comparison must preserve the distinction between the exact Euclidean regularity theorem and any proposed microscopic emission mechanism.

## 7. Executable defects

A reference gate should audit

\[
\Delta_{period}=|\kappa_H\beta-2\pi|,
\]

\[
\Delta_{hol}=|e^{i\kappa_H\beta}-1|,
\]

\[
\Delta_T=\left|T_H-\frac{\kappa_H}{2\pi}\right|,
\]

and an adversarial detuned period `beta != 2π/kappa_H` must produce nonzero conical and holonomy defects.

## 8. Frontier

Exact at 01AH:

- Euclidean near-horizon polar regularity;
- primitive `2π` Euler winding;
- `beta_H=2π/kappa_H`;
- `T_H=kappa_H/(2π)` in natural units;
- trivial primitive horizon holonomy `W_H=1`.

Candidate bridge:

- Aharonov–Bohm and Euclidean-horizon loops are isomorphic at the level of closed `U(1)` holonomy and Euler winding.

Open downstream binding:

- a microscopic map from project phase-information channels to Hawking quanta;
- greybody factors and mode occupation;
- rotating/charged horizon chemical potentials;
- backreaction and evaporation dynamics.
