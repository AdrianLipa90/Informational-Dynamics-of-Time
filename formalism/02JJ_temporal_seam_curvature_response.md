# 02JJ — Temporal Seam Curvature and Positive Connection Response

Status: `FORMAL_CANDIDATE / GAUGE_INVARIANT_CONNECTION_RESPONSE_GATE`

02JI derives the exact moving-connection work for an admitted seam phase `varphi_e(Theta)` and leaves the connection rate unselected. This layer introduces the temporal vertex connection required by time-dependent gauge covariance, constructs the gauge-invariant temporal seam curvature, and uses a positive response tensor to select the moving seam rate.

## 1. Temporal vertex connection

Let the full instantaneous Hamiltonian be decomposed as

\[
\boxed{
H=\bar H+\operatorname{diag}(A_{\Theta,1},\ldots,A_{\Theta,N}),
}
\]

where `A_Theta` is the vertex temporal connection and `bar H` is the covariant Hamiltonian sector.

For a time-dependent local rephasing

\[
U_\chi(\Theta)=\operatorname{diag}(e^{i\chi_1},\ldots,e^{i\chi_N}),
\]

02JI gives

\[
\psi'=U_\chi\psi,
\qquad
\varphi'_e=\varphi_e+\chi_{e+1}-\chi_e,
\]

\[
H'=U_\chi H U_\chi^\dagger-\operatorname{diag}(D_\Theta\chi_n).
\]

Therefore choose

\[
\boxed{
A'_{\Theta,n}=A_{\Theta,n}-D_\Theta\chi_n,
}
\]

so that

\[
\boxed{
\bar H'=U_\chi\bar H U_\chi^\dagger.
}
\]

## 2. Temporal seam curvature

Let `B` be the oriented edge-difference operator,

\[
(BA_\Theta)_e=A_{\Theta,e+1}-A_{\Theta,e}.
\]

The seam rate transforms as

\[
D_\Theta\varphi'_e
=D_\Theta\varphi_e
+D_\Theta\chi_{e+1}-D_\Theta\chi_e.
\]

Define

\[
\boxed{
F_{\Theta e}
:=D_\Theta\varphi_e+(BA_\Theta)_e.
}
\]

Then exactly

\[
\boxed{F'_{\Theta e}=F_{\Theta e}.}
\]

Thus `F_Theta` is the gauge-invariant temporal curvature carried by the half-seam connection.

## 3. Gauge-native decomposition of moving seam power

Let

\[
V_{\rm seam}=\psi^\dagger K_\varphi\psi
\]

and

\[
\boxed{
q_e^{\rm conn}=\frac{\partial V_{\rm seam}}{\partial\varphi_e}.
}
\]

02JI gives

\[
P_{\rm geom}
=i\psi^\dagger[H,K_\varphi]\psi
+(\mathbf q^{\rm conn})^T D_\Theta\boldsymbol\varphi.
\]

Using `H=bar H+diag(A_Theta)`, the diagonal temporal-connection sector satisfies

\[
\boxed{
i\psi^\dagger[\operatorname{diag}(A_\Theta),K_\varphi]\psi
=(\mathbf q^{\rm conn})^TBA_\Theta.
}
\]

Therefore

\[
\boxed{
P_{\rm geom}
=P_{\rm cov}
+(\mathbf q^{\rm conn})^T\mathbf F_\Theta,
}
\]

with

\[
\boxed{
P_{\rm cov}
:=i\psi^\dagger[\bar H,K_\varphi]\psi.
}
\]

Both terms are gauge invariant.

## 4. Positive curvature response

Let `G_phi` be a real symmetric positive-semidefinite response tensor on the edge sector. Define the constitutive response

\[
\boxed{
\mathbf F_\Theta
=-G_\varphi\mathbf q^{\rm conn}.
}
\]

This selects the seam rate covariantly:

\[
\boxed{
D_\Theta\boldsymbol\varphi
=-BA_\Theta-G_\varphi\mathbf q^{\rm conn}.
}
\]

In the temporal gauge `A_Theta=0`, this reduces to

\[
\boxed{
D_\Theta\boldsymbol\varphi
=-G_\varphi\mathbf q^{\rm conn}.
}
\]

The curvature-sector dissipation is

\[
\boxed{
\mathcal D_\varphi
=(\mathbf q^{\rm conn})^T
G_\varphi
\mathbf q^{\rm conn}
\ge0.
}
\]

Since

\[
(\mathbf q^{\rm conn})^T\mathbf F_\Theta
=-\mathcal D_\varphi,
\]

the response contributes a non-positive term to the seam-energy balance.

## 5. Full gauge-native seam balance

Let the already admitted vertex-phase Onsager dissipation be

\[
\mathcal D_\alpha
=\mathbf g_\alpha^TG_\alpha\mathbf g_\alpha\ge0.
\]

Then the moving-connection balance becomes

\[
\boxed{
\frac{dV_{\rm seam}}{d\Theta}
=P_{\rm cov}
-\mathcal D_\varphi
-\mathcal D_\alpha.
}
\]

This is the gauge-native form of the PR #54 balance after the seam rate has been selected by the positive curvature response.

The exact decomposition is

\[
\boxed{
P_{\rm Sch}+P_{\rm conn}
=P_{\rm cov}+\mathbf q^{\rm conn}\!\cdot\mathbf F_\Theta.
}
\]

Hence the original moving-connection expression and the curvature-native expression are algebraically identical.

## 6. Gauge-invariant temporal seam offset

The raw accumulated seam phase

\[
\Delta\varphi_e
=\int D_\Theta\varphi_e\,d\Theta
\]

depends on a time-dependent gauge choice unless endpoint gauge data are fixed.

The gauge-invariant accumulated temporal seam offset is instead

\[
\boxed{
\Delta\Phi^{\rm curv}_e
=\int_{\Theta_1}^{\Theta_2}
F_{\Theta e}\,d\Theta.
}
\]

Equivalently,

\[
\boxed{
\Delta\Phi^{\rm curv}_e
=\varphi_e(\Theta_2)-\varphi_e(\Theta_1)
+\int_{\Theta_1}^{\Theta_2}
\bigl(A_{\Theta,e+1}-A_{\Theta,e}\bigr)d\Theta.
}
\]

This quantity is additive under interval concatenation and invariant under the declared time-dependent local rephasing.

In temporal gauge it reduces to the accumulated seam phase.

## 7. Relation to the derived temporal normalization

All rates in this gate are derivatives with respect to the already-derived intrinsic temporal measure `Theta`. No second temporal coordinate is introduced.

The TIR/IDT bridge supplies the intrinsic phase-rate coordinate

\[
\Omega_\Theta=\frac{d\phi}{d\Theta}.
\]

Conversion of `Delta Phi_curv` into an intrinsic or calibrated clock-duration offset requires an admitted local phase-rate map and remains a separate downstream gate.

## 8. Falsification gates

Reference tests require:

- exact time-dependent gauge invariance of `F_Theta`;
- similarity-only transformation of `bar H`;
- exact identity between the original moving geometric power and the curvature-native decomposition;
- exact diagonal temporal-connection commutator identity;
- gauge-covariant seam-rate selection from the response law;
- non-negative curvature dissipation;
- exact `q dot F = -D_phi` identity;
- equality of the curvature-native and original moving-connection balance rates;
- time-dependent gauge invariance of the full response balance;
- additive accumulated curvature offset;
- fail-closed validation of dimensions, Hermiticity and positive-semidefinite response tensors.

Reference implementation: `src/idt/temporal_seam_curvature_response.py`.

Reference tests: `tests/reference/test_temporal_seam_curvature_response.py`.

Validation receipt: `validation/TEMPORAL_SEAM_CURVATURE_RESPONSE_V0_1.json`.
