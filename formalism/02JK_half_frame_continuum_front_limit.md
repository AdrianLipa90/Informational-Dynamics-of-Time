# 02JK — Half-Frame Continuum Front Limit

Status: `FORMAL_CANDIDATE / CONTINUUM_BRIDGE_GATE`

02JJ derives the finite-path fuzzy-interface front. This layer derives the half-frame overlap/defect continuum limit while retaining the heterogeneous continuum operator already established in 02C.

## 1. Smooth continuum sampling

Let

\[
\Psi(x,\Theta)=R(x,\Theta)e^{i\alpha(x,\Theta)}
\]

be a smooth complex temporal-wave carrier on a one-dimensional patch, and let the frame mesh be

\[
x_n=x_0+nh,
\qquad h>0.
\]

Use the norm-consistent sampling

\[
\boxed{
a_n^{(h)}=\sqrt h\,\Psi(x_n,\Theta).
}
\]

Let a smooth edge connection \(A(x,\Theta)\) define the seam phase

\[
\boxed{
\varphi_n^{(h)}
=\int_{x_n}^{x_{n+1}}A(x,\Theta)\,dx.
}
\]

The gauge-invariant seam mismatch is

\[
\boxed{
\delta_n^{(h)}
=\alpha(x_{n+1})-\alpha(x_n)-\varphi_n^{(h)}.
}
\]

For smooth \(\alpha\) and \(A\),

\[
\delta_n^{(h)}=O(h).
\]

## 2. Glued channel becomes continuum density

02JI--02JJ give the occupancy-sensitive fuzzy-interface mass

\[
J_n
=2|a_n||a_{n+1}|\cos^2\!\frac{\delta_n}{2}.
\]

Define its edge density by

\[
\boxed{
\rho_{F,n}^{(h)}
:=\frac{J_n}{2h}.
}
\]

Then exactly

\[
\rho_{F,n}^{(h)}
=R(x_n)R(x_{n+1})
\cos^2\!\frac{\delta_n^{(h)}}2.
\]

At the edge midpoint

\[
x_{n+1/2}=\frac{x_n+x_{n+1}}2,
\]

smoothness gives

\[
\boxed{
\rho_{F,n}^{(h)}
\longrightarrow
|\Psi(x_{n+1/2},\Theta)|^2
\qquad(h\to0).
}
\]

Under sufficient smoothness, the midpoint expansion is

\[
\boxed{
\rho_{F,n}^{(h)}
=R^2
+\frac{h^2}{4}
\left[
RR''-(R')^2-R^2(\alpha'-A)^2
\right]_{x_{n+1/2}}
+O(h^4).
}
\]

Hence the genuine interface-quality coordinate satisfies

\[
F_n\to1
\]

in a smooth occupied bulk, while the rescaled interface mass \(J_n/(2h)\) carries the continuum density.

## 3. Seam defect becomes the covariant gradient

The phase-aware seam-defect amplitude is

\[
\boxed{
d_n^{(h)}
=\frac12\left(
 e^{+i\varphi_n/2}a_n
-e^{-i\varphi_n/2}a_{n+1}
\right).
}
\]

Define the continuum defect density

\[
\boxed{
\varepsilon_{D,n}^{(h)}
:=\frac{4|d_n^{(h)}|^2}{h^3}.
}
\]

With the covariant derivative

\[
\boxed{
D_A:=\partial_x-iA,
}
\]

the symmetric edge expansion gives

\[
\boxed{
d_n^{(h)}
=-\frac{h^{3/2}}2
\,D_A\Psi(x_{n+1/2},\Theta)
+O(h^{7/2}),
}
\]

and therefore

\[
\boxed{
\varepsilon_{D,n}^{(h)}
\longrightarrow
|D_A\Psi(x_{n+1/2},\Theta)|^2.
}
\]

The two half-seam channels therefore carry complementary continuum data:

```text
glued/fuzzy channel : J_n/(2h)       -> |Psi|^2
seam-defect channel : 4|d_n|^2/h^3   -> |D_A Psi|^2
```

## 4. Gauge covariance

For a smooth local phase re-expression

\[
\Psi\mapsto e^{i\chi}\Psi,
\qquad
A\mapsto A+\partial_x\chi,
\]

the edge phase transforms as

\[
\varphi_n\mapsto
\varphi_n+\chi(x_{n+1})-\chi(x_n).
\]

Hence \(\delta_n\), \(\rho_{F,n}^{(h)}\), \(|d_n|^2\), and \(\varepsilon_{D,n}^{(h)}\) are gauge invariant. In the continuum,

\[
D_A\Psi\mapsto e^{i\chi}D_A\Psi,
\]

so the limiting defect density is gauge invariant as well.

## 5. Integrated measure limit

For a finite interval with vanishing mesh size,

\[
\boxed{
\sum_n h\rho_{F,n}^{(h)}
\longrightarrow
\int |\Psi(x,\Theta)|^2\,dx.
}
\]

Equivalently,

\[
\boxed{
\frac12\sum_n J_n
\longrightarrow
\int |\Psi|^2dx.
}
\]

Thus the finite half-frame overlap mass becomes the continuum temporal-wave density measure.

## 6. Direct bridge to the 02C heterogeneous stiffness operator

02C derives the discrete heterogeneous stiffness

\[
K=D^\dagger\operatorname{diag}(M_e)D,
\qquad M_e>0,
\]

and its long-wave effective coefficient

\[
\boxed{
M_{\rm eff}
=\left(\frac1N\sum_e\frac1{M_e}\right)^{-1}.
}
\]

The half-seam defect supplies the corresponding local covariant-gradient density. For smooth edge mobility \(M(x)>0\),

\[
\boxed{
\sum_n hM_n\varepsilon_{D,n}^{(h)}
=
\sum_n\frac{4M_n}{h^2}|d_n|^2
\longrightarrow
\int M(x)|D_A\Psi|^2dx.
}
\]

Therefore the half-frame quotient supplies a microscopic overlap/gradient decomposition whose gradient channel enters the same mobility-weighted quadratic form used by the 02C stiffness sector. The 02C homogenization result retains coefficient authority:

\[
\boxed{c_{\rm eff}^2=M_{\rm eff}.}
\]

The propagation coefficients of this continuum bridge are inherited from 02C as \(M_{\rm eff}\) and \(\beta_{\rm eff}\).

## 7. Continuum reading of the slice picture

For finite spacing, the pattern

\[
|1|\,|12|\,|23|\cdots|N|
\]

contains individually resolvable fuzzy seams. Under mesh refinement, adjacent seam masses scale as \(O(h)\), while their number scales as \(O(h^{-1})\). Their rescaled density remains finite and converges to \(|\Psi|^2\).

Thus the continuum is obtained as the density limit of overlapping half-frame supports while the complementary seam mismatch becomes the covariant spatial derivative of the temporal-wave carrier.

## 8. Falsification gates

Reference tests require:

- exact constant covariantly locked field reduction \(\rho_F=|\Psi|^2\), \(\varepsilon_D=0\);
- second-order midpoint convergence of \(\rho_F\) to \(|\Psi|^2\) for a smooth nonuniform field;
- second-order midpoint convergence of \(\varepsilon_D\) to \(|D_A\Psi|^2\);
- gauge invariance under a nontrivial smooth local rephasing;
- convergence of the integrated glued measure to \(\int|\Psi|^2dx\);
- convergence of the mobility-weighted seam-defect form to \(\int M|D_A\Psi|^2dx\);
- inheritance of the 02C coefficient authority through \(M_{\rm eff}\) and \(\beta_{\rm eff}\).

Reference implementation: `src/idt/half_frame_continuum.py`.
Reference tests: `tests/reference/test_half_frame_continuum.py`.
Validation receipt: `validation/HALF_FRAME_CONTINUUM_V0_1.json`.
