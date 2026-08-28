# 02J — Half-Frame Temporal Gluing

Status: `FORMAL_CANDIDATE / ALGEBRAIC_REFERENCE_GATE`

This gate formalizes the modular temporal-slice picture in which each discrete temporal frame carries two half-supports and neighboring frames are glued through one shared interface. The construction is placed downstream of the already-derived intrinsic coordinate `Theta` and the Zeta–Collatz frame carrier.

## 1. Modular frame sector

For a positive integer frame count `N`, define the corresponding phase-budget sector

\[
\boxed{\Phi_N=2\pi N.}
\]

The first four sectors are

```text
2pi  -> |1|1|
4pi  -> |1|12|2|
6pi  -> |1|12|23|3|
8pi  -> |1|12|23|34|4|
```

The notation records support topology rather than amplitudes.

## 2. Two half-supports per frame

Let the discrete frame Hilbert space be

\[
\mathcal H_F=\operatorname{span}\{|1\rangle,\ldots,|N\rangle\}.
\]

Introduce the doubled half-frame carrier

\[
\boxed{\mathcal H_{1/2}=\operatorname{span}\{|n,L\rangle,|n,R\rangle\}_{n=1}^N.}
\]

Define the equal half-splitting isometry

\[
\boxed{
S_N|n\rangle
=\frac{|n,L\rangle+|n,R\rangle}{\sqrt2}.
}
\]

Hence

\[
\boxed{S_N^\dagger S_N=I_N.}
\]

Each whole-frame amplitude is therefore represented by two half-frame amplitudes with equal probability weight `1/2` before neighboring gluing is applied.

## 3. Neighboring half-frame identification

For every neighboring pair impose the interface identification

\[
\boxed{|n,R\rangle\sim|n+1,L\rangle,\qquad n=1,\ldots,N-1.}
\]

The glued support space has basis

\[
\boxed{
\mathcal H_G=
\operatorname{span}
\bigl\{
|1\rangle_\partial,
|12\rangle,
|23\rangle,\ldots,
|N-1,N\rangle,
|N\rangle_\partial
\bigr\}.
}
\]

Starting from `2N` half-supports and applying `N-1` independent neighboring identifications gives

\[
\boxed{\dim\mathcal H_G=2N-(N-1)=N+1.}
\]

This is the exact counting rule behind the modular patterns above.

## 4. Co-isometric gluing operator

Define `Q_N : H_{1/2} -> H_G` by

\[
Q_N|1,L\rangle=|1\rangle_\partial,
\qquad
Q_N|N,R\rangle=|N\rangle_\partial,
\]

and for every internal seam

\[
\boxed{
Q_N|n,R\rangle
=\frac{|n,n+1\rangle}{\sqrt2},
\qquad
Q_N|n+1,L\rangle
=\frac{|n,n+1\rangle}{\sqrt2}.
}
\]

Then

\[
\boxed{Q_NQ_N^\dagger=I_{N+1}.}
\]

The adjoint embeds each interface support as the symmetric half-frame combination

\[
\boxed{
Q_N^\dagger|n,n+1\rangle
=\frac{|n,R\rangle+|n+1,L\rangle}{\sqrt2}.
}
\]

The orthogonal antisymmetric seam mode is

\[
\boxed{
|A_n\rangle
=\frac{|n,R\rangle-|n+1,L\rangle}{\sqrt2},
\qquad
Q_N|A_n\rangle=0.
}
\]

Thus the gluing operation has a resolved symmetric interface sector and an explicitly retained mismatch sector.

## 5. Whole-frame to glued-support map

Define

\[
\boxed{G_N:=Q_NS_N.}
\]

For a normalized frame amplitude vector

\[
|a\rangle=\sum_{n=1}^Na_n|n\rangle,
\qquad
\sum_n|a_n|^2=1,
\]

the raw glued-support amplitudes are

\[
\boxed{
\begin{aligned}
b_0&=\frac{a_1}{\sqrt2},\\
b_n&=\frac{a_n+a_{n+1}}{2},\qquad 1\le n\le N-1,\\
b_N&=\frac{a_N}{\sqrt2}.
\end{aligned}
}
\]

The antisymmetric seam-defect amplitudes are

\[
\boxed{
d_n=\frac{a_n-a_{n+1}}{2}.}
\]

The construction obeys the exact norm decomposition

\[
\boxed{
\sum_{j=0}^{N}|b_j|^2
+
\sum_{n=1}^{N-1}|d_n|^2
=
\sum_{n=1}^{N}|a_n|^2.
}
\]

Therefore compatible overlap and seam mismatch form complementary sectors of the same conserved frame norm.

## 6. Constructive and destructive half-frame overlap

At interface `n,n+1`,

\[
\boxed{b_n=\frac{a_n+a_{n+1}}{2}.}
\]

Equal neighboring phase gives constructive gluing,

\[
a_{n+1}=a_n
\quad\Longrightarrow\quad
b_n=a_n,
\qquad d_n=0.
\]

Opposite neighboring phase gives an interface null,

\[
a_{n+1}=-a_n
\quad\Longrightarrow\quad
b_n=0,
\qquad d_n=a_n.
\]

Thus the half-frame construction converts relative phase directly into interface occupancy versus seam mismatch.

## 7. Uniform coherent chain

For the equal coherent frame state

\[
\boxed{a_n=\frac1{\sqrt N}},
\]

all seam defects vanish. The glued probabilities are

\[
\boxed{
P_{\partial,1}=P_{\partial,N}=\frac1{2N},
\qquad
P_{n,n+1}=\frac1N.
}
\]

They sum exactly to unity. The interior of the chain is therefore carried entirely by neighboring overlap supports,

\[
\boxed{|1|\,|12|\,|23|\cdots|N-1,N|\,|N|.}
\]

## 8. Schrödinger fuzziness on the half-frame quotient

Let the already declared Hermitian frame Hamiltonian generate

\[
\boxed{
i\partial_\Theta|a(\Theta)\rangle=H_{\zeta C}|a(\Theta)\rangle.}
\]

The half-frame temporal observable is evaluated downstream by

\[
\boxed{|b(\Theta)\rangle=G_N|a(\Theta)\rangle.}
\]

Define raw interface occupancy

\[
\boxed{
F_{1/2}(\Theta)
=\sum_{n=1}^{N-1}|b_n(\Theta)|^2,
}
\]

and seam-defect weight

\[
\boxed{
D_{1/2}(\Theta)
=\sum_{n=1}^{N-1}|d_n(\Theta)|^2.
}
\]

Together with the two endpoint weights they satisfy the exact conserved decomposition inherited from the unitary frame state.

This replaces an arbitrary smooth kernel by a topology-driven neighboring half-frame overlap. Continuous coarse-graining may subsequently act on the `N+1` glued supports.

## 9. Relation to modular phase count

For integer `N`, the declared phase-budget sector

\[
\Phi_N=2\pi N
\]

contains `N` full frames, `2N` half-frame carriers and `N+1` glued supports. Hence

\[
\boxed{
\#\text{glued supports}
=\frac{\Phi_N}{2\pi}+1.
}
\]

Explicitly,

\[
\begin{aligned}
\Phi_1=2\pi &: \quad |1|1|,\\
\Phi_2=4\pi &: \quad |1|12|2|,\\
\Phi_3=6\pi &: \quad |1|12|23|3|,\\
\Phi_4=8\pi &: \quad |1|12|23|34|4|.
\end{aligned}
\]

The spin-1/2 / `4pi` physical binding remains a separately typed downstream gate; this algebraic gate establishes the half-support quotient and modular counting rule used by that future comparison.

## 10. Immediate falsification gates

The reference candidate fails if any declared test violates:

- `S_N^dagger S_N = I`;
- `Q_N Q_N^dagger = I`;
- quotient dimension `N+1`;
- exact modular support labels for `N=1,2,3,4`;
- seam antisymmetric modes lie in `ker Q_N`;
- norm decomposition between glued and seam-defect sectors;
- constructive equal-phase seam closure;
- destructive opposite-phase interface null;
- consistent downstream action on a unitary Schrödinger-evolved frame state.

Reference implementation: `src/idt/half_frame_temporal_gluing.py`.
Reference tests: `tests/reference/test_half_frame_temporal_gluing.py`.
Validation receipt: `validation/HALF_FRAME_TEMPORAL_GLUING_V0_1.json`.
