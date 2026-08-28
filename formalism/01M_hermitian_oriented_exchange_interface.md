# 01M — Hermitian Oriented Exchange Interface

Status: `TARGETED_HERMITIAN_OPERATOR_INTERFACE_CANDIDATE / TARGET_SYSTEM_BINDING_OPEN`

Pinned upstreams and implementation witness:

- IDT 01L branch `feat/relational-lambda-oriented-holonomy-v0.1`: `305e8602620b552052471fadfe798cad44a2d182`
- GREMLIN branch `feat/gremlin-hermitian-oriented-exchange-v1.4`: `1cfeb2df52f3b98318bf207c6a12cd3e6a913f24`
- GREMLIN CI run `33125674008`: `209 passed`

## 1. Purpose

01M receives the oriented relational coupling exported by 01L,

\[
\mathcal J_R=E_Re^{i\tau_R},
\]

and defines a Hermitian two-state exchange interface that preserves both the source-energy magnitude and the signed holonomy phase.

The typed chain is

\[
\boxed{
\Lambda_R
\rightarrow E_R
\rightarrow \tau_R
\rightarrow \mathcal J_R
\rightarrow H_{\rm ex}
\rightarrow U_{\rm ex}(t)
\rightarrow \text{phase-sensitive observable}
}
\]

## 2. Hermitian exchange embedding

For a target two-state subspace with basis states `|01>` and `|10>`, define

\[
\boxed{
H_{\rm ex}
=\mathcal J_R|01\rangle\langle10|
+\mathcal J_R^*|10\rangle\langle01|.
}
\]

The corresponding matrix on

\[
(|00\rangle,|01\rangle,|10\rangle,|11\rangle)
\]

is

\[
\boxed{
H_{\rm ex}
=
\begin{pmatrix}
0&0&0&0\\
0&0&\mathcal J_R&0\\
0&\mathcal J_R^*&0&0\\
0&0&0&0
\end{pmatrix}.
}
\]

The conjugate pair gives

\[
\boxed{H_{\rm ex}=H_{\rm ex}^{\dagger}.}
\]

## 3. Pauli decomposition

Writing

\[
\mathcal J_R=J_x+iJ_y,
\qquad
J_x=E_R\cos\tau_R,
\qquad
J_y=E_R\sin\tau_R,
\]

gives

\[
\boxed{
H_{\rm ex}
=\frac{J_x}{2}(X\otimes X+Y\otimes Y)
+\frac{J_y}{2}(X\otimes Y-Y\otimes X).
}
\]

The real projection is the v1.1 channel-energy imbalance,

\[
J_x=J_C-J_D,
\]

while the second operator component carries the signed rotational quadrature `E_R sin(tau_R)`.

## 4. Spectrum

In the single-excitation subspace,

\[
H_{\rm ex}^{(1)}
=
\begin{pmatrix}
0&\mathcal J_R\\
\mathcal J_R^*&0
\end{pmatrix}.
\]

Therefore

\[
\boxed{
\lambda_{\pm}=\pm|\mathcal J_R|=\pm|E_R|.
}
\]

The remaining two basis states carry zero eigenvalue in this reference embedding.

## 5. Exact unitary exchange

Let

\[
\phi_R
=\frac{|\mathcal J_R|\Delta t}{\hbar}.
\]

Then

\[
\boxed{
\begin{aligned}
a'_{01}
&=\cos\phi_R\,a_{01}
-i\sin\phi_R\frac{\mathcal J_R}{|\mathcal J_R|}a_{10},\\
a'_{10}
&=\cos\phi_R\,a_{10}
-i\sin\phi_R\frac{\mathcal J_R^*}{|\mathcal J_R|}a_{01}.
\end{aligned}
}
\]

The reference implementation receipts norm closure and excitation-number conservation.

## 6. Quarter- and half-exchange diagnostics

For initial state `|10>`, define

\[
\Delta t_{1/4}
=\frac{\pi\hbar}{4|E_R|}.
\]

At this diagnostic time the reference two-qubit model reaches equal single-excitation populations and concurrence

\[
\boxed{C=1.}
\]

At

\[
\Delta t_{1/2}
=\frac{\pi\hbar}{2|E_R|},
\]

the population is fully transferred into the other exchange basis state.

These are reference-conformance consequences of the declared Hermitian exchange model.

## 7. Orientation-reversal observable

Under

\[
\tau_R\mapsto-\tau_R,
\]

we have

\[
J_x\mapsto J_x,
\qquad
J_y\mapsto-J_y.
\]

Thus population-transfer probabilities are invariant under orientation reversal while the transfer phase changes.

For positive `E_R`, the reference exchange amplitude gives

\[
\boxed{
\Delta\varphi_{\rm transfer}
=2\tau_R\pmod{2\pi}.
}
\]

This phase-sensitive quantity is the preferred observable for testing the orientation sector.

## 8. Target-system adapter contract

A physical target adapter must provide:

```text
target_state_basis             = explicit physical state map
target_free_hamiltonian        = independently specified
target_matter_hamiltonian      = independently specified when applicable
relational_exchange_embedding  = H_ex or a derived multi-level extension
holonomy_lineage               = tau_R from admitted IDT connection
source_lineage                 = E_R from admitted RFC Lambda_R binding
observable                     = phase/probability residual with uncertainty
```

For the neutrino test target, the adapter must preserve the standard vacuum/matter terms and expose the relational holonomy contribution as a separately falsifiable residual.

## 9. Promotion gates

01M advances through separate receipts for:

1. a physical state-space map for the target system;
2. compatibility with the target free Hamiltonian;
3. compatibility with matter terms where relevant;
4. unitary multi-level closure when the target exceeds two states;
5. an orientation-sensitive observable;
6. comparison with baseline oscillation data;
7. joint-state witness when entanglement attribution is tested.

The author/formalism may suggest that internal geometric rotation can become an observable interaction phase through this Hermitian embedding, yet does not state that target-system realization as an established result before these gates are receipted.
