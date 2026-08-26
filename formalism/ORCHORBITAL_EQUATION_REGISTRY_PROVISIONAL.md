# Provisional ORCHORBITAL Equation Registry

Status: `MEMORY_EXTENSION_STAGING_ONLY`

These equation IDs are reserved for the ORCHORBITAL temporal-memory extension. Promotion into the canonical `EQUATION_REGISTRY.md` requires explicit parent/extension admission and preserves the identifiers.

**EQ-T019O — attractor-relative Kepler energy and binding margin**
\[
\boxed{
E_i=\frac12\|v_M\|^2-\frac{\mu_i}{\|m-c_i\|},
\qquad
b_i=[-E_i]_+.
}
\]

**EQ-T019P — normalized ORCHORBITAL attractor weights**
For \(B=\sum_i b_i>0\),
\[
\boxed{
w_i=\frac{b_i}{B},
\qquad
\sum_iw_i=1,
\qquad
a=\arg\max_iw_i.
}
\]
For \(B=0\), the field state is `LEAK_MODE`.

**EQ-T019Q — Shannon basin entropy and normalized coherence**
\[
\boxed{
H_A=-\sum_{i:w_i>0}w_i\log_2w_i.
}
\]
For \(N>1\),
\[
\boxed{
C_A=1-\frac{H_A}{\log_2N}.
}
\]

**EQ-T019R — active-centre ORCHORBITAL memory dynamics**
\[
\boxed{
\frac{d^2m}{d\tau_{\rm int}^2}
=-\mu_a\frac{m-c_a}{\|m-c_a\|^3}.
}
\]

**EQ-T019S — active-attractor winding increment**
\[
\boxed{
\Delta W_a
=\frac{1}{2\pi}
\operatorname{wrap}_{(-\pi,\pi]}
\left[
\arg(m_{n+1}-c_a)-\arg(m_n-c_a)
\right].
}
\]

**EQ-T019T — phase-space closure defect**
For declared \(r_*>0\) and \(v_*>0\),
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

**EQ-T019U — event-to-attractor causal ordering**
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

**EQ-T019V — attractor residence time and accumulated winding**
For \(\mathcal S_i=\{n:a_n=i\}\),
\[
\boxed{
T_i^{\rm res}=\sum_{n\in\mathcal S_i}\Delta\tau_n,
\qquad
W_i^{\rm tot}=\sum_{n\in\mathcal S_i}\Delta W_{i,n}.
}
\]

**EQ-T019W — directed attractor transition count**
\[
\boxed{
N_{i\to j}
=\#\{n:a_n=i,\ a_{n+1}=j,\ i\neq j\}.
}
\]
