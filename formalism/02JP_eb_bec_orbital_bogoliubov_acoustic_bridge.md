# 02JP — EB/BEC Nonlinear Madelung, Orbital, Bogoliubov and Acoustic-Geometry Bridge

Status: FORMAL_CANDIDATE / CONDITIONAL_SPATIAL_LIFT / NO_SPACETIME_PROMOTION

This gate is additive to 02JN. It does not modify or promote the admitted status of 02JN. It adds a density equation of state to the existing continuum Madelung–Schrödinger–Onsager system, derives its Bogoliubov-like linear sector, and states the additional hypotheses required to compare that sector with a weakly interacting Bose–Einstein condensate, circular orbital balance, holonomy-shifted circulation and analogue acoustic geometry.

Repository parents used by this gate:

- IDT 02JN: continuum Madelung Schrödinger–Onsager split;
- GREMLIN v0.6/v0.8: role-typed orbital kernel and source/coupling identifiability;
- RFC RF-L3: conditional information-scalar potential reconstruction.

The physical BEC binding, spatial-carrier binding and spacetime interpretation remain separate gates.

## 1. Parent IDT system

For constant positive M, stationary connection and

\[
\Psi=R e^{i\alpha},
\qquad
\rho=R^2,
\qquad
q=\nabla\alpha-A,
\]

the isotropic spatial lift of the 02JN current is

\[
\boxed{
\mathbf J=2M\rho\,q,
\qquad
\mathbf u_\Theta=\frac{\mathbf J}{\rho}=2Mq.
}
\]

The lift from the one-dimensional 02JN coordinate to a spatial carrier of dimension d greater than or equal to 2 is an explicit hypothesis of this gate, not a theorem of 02JN.

## 2. Nonlinear equation-of-state extension

Let the scalar phase-rate potential be

\[
\boxed{
V(\rho,\mathbf x,\Theta)
=
V_0+V_{\rm ext}+V_I+\lambda\rho,
}
\]

with constant local nonlinear coefficient \(\lambda\). The 02JN compact phase balance becomes

\[
\boxed{
\partial_\Theta\alpha+\mu\partial_\Theta\rho
=
M\frac{\nabla^2\sqrt{\rho}}{\sqrt{\rho}}
-Mq^2
-V_0-V_{\rm ext}-V_I-\lambda\rho.
}
\]

For stationary A, differentiation gives the velocity equation

\[
\boxed{
\partial_\Theta\mathbf u_\Theta
+
(\mathbf u_\Theta\cdot\nabla)\mathbf u_\Theta
=
2M^2\nabla\!\left(
\frac{\nabla^2\sqrt{\rho}}{\sqrt{\rho}}
\right)
-2M\nabla(V_{\rm ext}+V_I+\lambda\rho)
+2\mu M\nabla\!\left[\nabla\cdot(\rho\mathbf u_\Theta)\right].
}
\]

In one dimension this reduces exactly to the 02JN velocity balance with the additional term

\[
\boxed{-2M\lambda\,\partial_x\rho.}
\]

## 3. Exact nonlinear linear-mode theorem

Linearize around a uniform zero-current background

\[
\rho=\rho_0+\delta\rho,
\qquad
\mathbf u_\Theta=\delta\mathbf u,
\qquad
\rho_0>0,
\]

with constant M, \(\lambda\) and background scalar potential. For a longitudinal Fourier mode
\(\exp(s\Theta+i\mathbf k\cdot\mathbf x)\), the characteristic polynomial is

\[
\boxed{
s^2
+
2\mu M\rho_0 k^2 s
+
2M\lambda\rho_0 k^2
+
M^2 k^4
=0.
}
\]

Thus the intrinsic-coordinate sound coefficient is

\[
\boxed{
c_{\Theta}^{\,2}=2M\lambda\rho_0.
}
\]

For \(\mu=0\),

\[
\boxed{
\omega_\Theta^2
=
c_\Theta^2 k^2+M^2k^4.
}
\]

The previous 02JN mode is recovered exactly at \(\lambda=0\).

## 4. Physical BEC bridge with explicit time, space and density calibration

Introduce positive calibration factors

\[
\boxed{
\gamma:=\frac{d\Theta}{dt}>0,
\qquad
\ell_x>0,
\qquad
\rho_{\rm BEC}=Z_\rho\rho,
\quad
Z_\rho>0,
}
\]

with local isotropic spatial map

\[
\boxed{
\mathbf x_{\rm phys}=\ell_x\mathbf x.
}
\]

Let \(m_B\) be the condensate inertial mass and let the physical Gross–Pitaevskii branch be

\[
i\hbar\partial_t\Psi
=
\left[
\frac{(-i\hbar\nabla_{\rm phys}-\mathbf A_{\rm phys})^2}{2m_B}
+
U_{\rm ext}+U_I+g\rho_{\rm BEC}
\right]\Psi.
\]

Exact coefficient matching to the intrinsic IDT equation requires

\[
\boxed{
M=\frac{\hbar}{2m_B\gamma\ell_x^2},
}
\]

\[
\boxed{
V_{\rm ext}+V_I
=
\frac{U_{\rm ext}+U_I}{\hbar\gamma},
}
\]

\[
\boxed{
\lambda
=
\frac{gZ_\rho}{\hbar\gamma},
}
\]

and the connection normalization

\[
\boxed{
\mathbf A_{\rm phys}
=
\frac{\hbar}{\ell_x}\mathbf A.
}
\]

The velocity and wave-number maps are

\[
\boxed{
\mathbf v_{\rm phys}
=
\ell_x\gamma\,\mathbf u_\Theta,
\qquad
\mathbf k_{\rm IDT}
=
\ell_x\mathbf k_{\rm phys}.
}
\]

The special branch \(\Theta=t\), \(\ell_x=1\), \(Z_\rho=1\) gives

\[
M=\frac{\hbar}{2m_B},
\qquad
\lambda=\frac{g}{\hbar},
\]

but those equalities are not assumed by the general bridge.

## 5. Exact Bogoliubov coefficient roundtrip

For the conservative branch \(\mu=0\), use
\(\omega_{\rm phys}=\gamma\omega_\Theta\) and
\(k_{\rm IDT}=\ell_x k_{\rm phys}\). Then

\[
\boxed{
\gamma^2
\left[
2M\lambda\rho_0(\ell_x k_{\rm phys})^2
+
M^2(\ell_x k_{\rm phys})^4
\right]
=
\frac{g\rho_{\rm BEC,0}}{m_B}k_{\rm phys}^2
+
\frac{\hbar^2}{4m_B^2}k_{\rm phys}^4.
}
\]

Hence

\[
\boxed{
\omega_{\rm Bog}^2
=
c_s^2k_{\rm phys}^2
+
\frac{\hbar^2k_{\rm phys}^4}{4m_B^2},
\qquad
c_s^2=\frac{g\rho_{\rm BEC,0}}{m_B}.
}
\]

This equality does not require \(\Theta=t\). It requires the declared calibration map.

The nonzero IDT Onsager coefficient \(\mu\) supplies an additional damping channel. It is not identified here with a specific measured BEC damping mechanism.

## 6. Conditional chemistry corollary

For a weak dilute three-dimensional contact-interaction gas,

\[
\boxed{
g=\frac{4\pi\hbar^2a_s}{m_B}.
}
\]

This is a conditional 3D dilute-gas relation, not a universal interaction law. On the stable repulsive branch \(a_s>0\),

\[
a_s
\longrightarrow
g
\longrightarrow
c_s
\longrightarrow
\omega_{\rm Bog}
\]

provides an explicit chemistry-to-hydrodynamics channel.

## 7. Information-potential cross-reference

RFC RF-L3 supplies the conditional reconstruction

\[
\boxed{
U_I=c_I\Xi_I,
\qquad
c_I:=\frac{\alpha_I}{\kappa_E}.
}
\]

In the BEC bridge this enters IDT as

\[
\boxed{
V_I
=
\frac{c_I\Xi_I}{\hbar\gamma}.
}
\]

Therefore a spatial information-curvature gradient contributes to the same condensate force balance as the external and mean-field potentials. The physical calibration of \(c_I\) remains inherited from RFC and is not promoted by this gate.

## 8. Physical Madelung force balance

Under the physical bridge, the conservative Gross–Pitaevskii sector gives

\[
\boxed{
m_B
(\partial_t+\mathbf v\cdot\nabla_{\rm phys})\mathbf v
=
-\nabla_{\rm phys}
\left(
U_{\rm ext}+U_I+g\rho_{\rm BEC}+Q_B
\right)
+
\mathbf F_A,
}
\]

where

\[
\boxed{
Q_B
=
-\frac{\hbar^2}{2m_B}
\frac{\nabla_{\rm phys}^2\sqrt{\rho_{\rm BEC}}}
{\sqrt{\rho_{\rm BEC}}}.
}
\]

The connection-force term \(\mathbf F_A\) vanishes only in the declared local force-free/topological sector. A connection with local curvature or explicit time dependence generally contributes additional force terms.

## 9. Circular orbital decomposition

Assume a stationary axisymmetric circular flow with

\[
v_r=0,
\qquad
v_\theta=r\omega,
\]

and assume the local connection-force contribution to the radial equation vanishes on the orbit. Then

\[
\boxed{
m_Br\omega^2
=
\partial_r
\left(
U_{\rm ext}+U_I+g\rho_{\rm BEC}+Q_B
\right).
}
\]

Define

\[
\boxed{
K_{\rm orb}:=\omega^2r^3.
}
\]

If the central source sector is

\[
\boxed{
U_{\rm ext}
=
-\frac{q_G\mu_S}{r},
}
\]

and the GREMLIN inertial role is conditionally bound to the condensate mass,
\(m_{\rm inertial}=m_B\), then

\[
\boxed{
K_{\rm orb}
=
\mu_S\eta_G
+
\frac{c_Ir^2}{m_B}\partial_r\Xi_I
+
\frac{gr^2}{m_B}\partial_r\rho_{\rm BEC}
+
\frac{r^2}{m_B}\partial_rQ_B,
}
\]

with

\[
\boxed{
\eta_G=\frac{q_G}{m_B}.
}
\]

Thus the GREMLIN invariant \(\mu_S\eta_G\) is the central \(1/r\) sector of a wider condensate radial balance. Orbital data alone identify only the total radial combination unless the other terms are independently constrained.

## 10. Holonomy-shifted circulation

Single-valued condensate phase gives

\[
\boxed{
\oint
(m_B\mathbf v+\mathbf A_{\rm phys})\cdot d\mathbf l
=
2\pi n\hbar,
\qquad
n\in\mathbb Z.
}
\]

Define

\[
\boxed{
\tau
=
\frac1\hbar
\oint\mathbf A_{\rm phys}\cdot d\mathbf l,
\qquad
\nu
=
n-\frac{\tau}{2\pi}.
}
\]

For a circular orbit,

\[
\boxed{
m_Br^2\omega=\hbar\nu.
}
\]

If the GREMLIN phase transports are source-bound on the same oriented loop and in a compatible convention, one may use the conditional composition

\[
\boxed{
\tau_{\rm total}
=
\tau_{\rm rot}+\tau_{\rm GR}+\tau_{\rm AB}.
}
\]

This composition does not itself prove the physical source assignments of the three terms.

## 11. Radial-shell theorem

Combining circulation with the force-free radial balance yields

\[
\boxed{
\hbar^2\nu^2
=
m_Br^3
\partial_r
\left(
U_{\rm ext}+U_I+g\rho_{\rm BEC}+Q_B
\right).
}
\]

For the pure \(1/r\) sector,

\[
\boxed{
r_\nu
=
\frac{\hbar^2}
{m_Bq_G\mu_S}
\left(
n-\frac{\tau}{2\pi}
\right)^2.
}
\]

The GREMLIN equivalence branch \(q_G=m_B\), when separately admitted, gives

\[
\boxed{
r_\nu
=
\frac{\hbar^2}
{m_B^2\mu_S}
\left(
n-\frac{\tau}{2\pi}
\right)^2.
}
\]

This is a Bohr-like shell law derived from condensate circulation plus a central \(1/r\) potential. It is not an independent proof of gravitational equivalence.

## 12. Thomas–Fermi cross-modal theorem

In the Thomas–Fermi regime, neglecting quantum pressure,

\[
\boxed{
\mu_c
=
U_{\rm ext}+U_I+g\rho_{\rm BEC},
}
\]

so

\[
\boxed{
\rho_{\rm BEC}
=
\frac{\mu_c-U_{\rm ext}-U_I}{g},
}
\]

and

\[
\boxed{
c_s^2
=
\frac{\mu_c-U_{\rm ext}-U_I}{m_B}.
}
\]

For fixed \(m_B\), \(g\), \(\mu_c\) and \(U_{\rm ext}\),

\[
\boxed{
\delta c_s^2
=
-\frac{\delta U_I}{m_B}.
}
\]

More generally,

\[
\boxed{
\delta c_s^2
=
\frac{
\delta\mu_c-\delta U_{\rm ext}-\delta U_I
}{m_B}.
}
\]

Thus phase-optical, spectral, density and orbital channels can be required to reconstruct one common \(U_I\) rather than being fitted independently.

## 13. Acoustic-geometry corollary

In the barotropic long-wavelength hydrodynamic regime, away from vortex cores and after neglecting quantum pressure at leading eikonal order, linear perturbations propagate on the analogue acoustic metric

\[
\boxed{
g_{\mu\nu}^{\rm ac}
\propto
\frac{\rho_{\rm BEC}}{c_s}
\begin{pmatrix}
-(c_s^2-v^2) & -v_j\\
-v_i & \delta_{ij}
\end{pmatrix}.
}
\]

The same background fields \((\rho_{\rm BEC},\mathbf v,c_s)\) therefore control both orbital-flow observables and analogue propagation/lensing of condensate excitations.

Firewall:

\[
\boxed{
g_{\mu\nu}^{\rm ac}
\neq
g_{\mu\nu}^{\rm spacetime}
}
\]

unless an additional independent spacetime-binding gate \(H_g\) is supplied.

## 14. Typed hypothesis ledger

The theorem chain depends on the following explicit hypotheses.

H_time:
\[
\Theta=\Theta(t),
\qquad
\gamma=d\Theta/dt>0
\]
is locally regular and treated as constant over the comparison window.

H_space:
an isotropic local spatial carrier exists with
\[
\mathbf x_{\rm phys}=\ell_x\mathbf x.
\]

H_density:
\[
\rho_{\rm BEC}=Z_\rho\rho
\]
with fixed positive \(Z_\rho\) over the comparison window.

H_mass:
the GREMLIN inertial role is bound to the condensate inertial mass only on the declared comparison branch.

H_forcefree:
the connection may carry global holonomy while contributing no additional local radial force on the selected orbit.

H_hydro:
the acoustic metric is used only in the long-wavelength barotropic hydrodynamic regime.

H_g:
spacetime interpretation remains OPEN.

## 15. Falsification gates

Reference validation must test:

1. exact recovery of the 02JN characteristic polynomial at \(\lambda=0\);
2. exact nonlinear polynomial
   \[
   s^2+2\mu M\rho_0k^2s+2M\lambda\rho_0k^2+M^2k^4=0;
   \]
3. exact coefficient roundtrip between the intrinsic conservative dispersion and the physical Bogoliubov dispersion for arbitrary positive \(\gamma,\ell_x,Z_\rho\);
4. exact current/velocity scaling
   \[
   \mathbf v_{\rm phys}=\ell_x\gamma\mathbf u_\Theta;
   \]
5. exact GREMLIN central-orbit recovery when information, mean-field and quantum-pressure gradients vanish;
6. exact decomposition of \(K_{\rm orb}\) into central, information, mean-field and quantum-pressure terms;
7. exact holonomy-shifted shell law in the \(1/r\) sector;
8. Thomas–Fermi sound-shift identity under its declared fixed-background conditions;
9. symmetric acoustic metric construction with Lorentzian sign pattern when \(c_s>0\);
10. fail-closed handling of non-positive masses, calibration scales, densities, radii and malformed vectors.

## 16. Status boundary

Exact within this gate:

- nonlinear extension of the 02JN phase potential;
- characteristic polynomial and conservative intrinsic dispersion;
- algebraic calibration map to the standard weak-contact BEC coefficients;
- conditional circular-force and circulation identities;
- algebraic Thomas–Fermi cross-modal relations.

Still conditional/open:

- the physical spatial realization of the IDT continuum coordinate;
- density normalization \(Z_\rho\);
- physical calibration of the information-potential coupling;
- identification of GREMLIN mass/source roles with a particular condensate experiment;
- physical source binding of rotation/GR/AB holonomies;
- identification of analogue acoustic geometry with spacetime geometry.

Reference implementation:
src/idt/eb_bec_madelung_bridge.py

Reference tests:
tests/reference/test_eb_bec_madelung_bridge.py
