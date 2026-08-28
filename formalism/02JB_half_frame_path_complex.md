# 02JB — Half-Frame Temporal Path Complex

Status: `FORMAL_CANDIDATE / TOPOLOGICAL_REFERENCE_GATE`

02J identifies neighboring half-frame supports. The quotient has an immediate one-dimensional simplicial realization that supplies the local path topology used by the discrete Temporal Wave continuum sector.

## 1. Frames become oriented edges

For `N` full temporal frames define `N+1` glued support vertices

\[
\boxed{V_N=\{v_0,v_1,\ldots,v_N\}.}
\]

Their display labels are

\[
\boxed{
v_0\leftrightarrow|1|,
\qquad
v_n\leftrightarrow|n,n+1|\ (1\le n<N),
\qquad
v_N\leftrightarrow|N|.
}
\]

Each full frame becomes one oriented temporal edge

\[
\boxed{e_n=[v_{n-1},v_n],\qquad n=1,\ldots,N.}
\]

Thus

\[
\boxed{\#E=N,\qquad \#V=N+1.}
\]

The topology is exactly the path complex `P_(N+1)`.

## 2. Boundary/incidence operator

Define

\[
\boxed{\partial_1 e_n=v_n-v_{n-1}.}
\]

In the vertex/edge bases the incidence matrix `D_N` has entries

\[
\boxed{
(D_N)_{j,n}
=\begin{cases}
-1,&j=n-1,\\
+1,&j=n,\\
0,&\text{otherwise}.
\end{cases}
}
\]

Every column sums to zero,

\[
\boxed{\mathbf 1^T D_N=0,}
\]

and

\[
\boxed{\operatorname{rank}D_N=N.}
\]

The constant support mode is therefore the unique zero mode of the connected unweighted vertex Laplacian.

## 3. Weighted temporal support Laplacian

Let each full frame/edge carry a positive weight

\[
\boxed{w_n>0.}
\]

The vertex-support Laplacian is

\[
\boxed{
L_V=D_N\operatorname{diag}(w_n)D_N^T.
}
\]

Hence

\[
\boxed{L_V=L_V^T,\qquad L_V\succeq0,\qquad L_V\mathbf1=0.}
\]

For a support scalar `f`,

\[
\boxed{
f^T L_V f
=\sum_{n=1}^{N}w_n(f_n-f_{n-1})^2\ge0.
}
\]

This is the local operator induced by the half-frame quotient topology.

## 4. Uniform spectral law

For uniform edge weight `w`, the exact spectrum of the path-support Laplacian is

\[
\boxed{
\lambda_k
=2w\left[1-\cos\left(\frac{k\pi}{N+1}\right)\right],
\qquad
k=0,\ldots,N.
}
\]

At low mode number with large `N`,

\[
\boxed{
\lambda_k
=w\left(\frac{k\pi}{N+1}\right)^2
+O\!\left(\frac{k^4}{(N+1)^4}\right).
}
\]

Thus the one-dimensional long-wave quadratic spectrum follows directly from the half-frame path topology.

## 5. Relation to 02F

02F introduced a Zeta-ordered nearest-frame stiffness

\[
K_{\rm path}=D^\dagger\operatorname{diag}(M_e)D.
\]

02JB supplies the topological source of that incidence structure:

```text
full frame n
  -> left/right half-supports
  -> R_n glued to L_(n+1)
  -> shared vertex v_n
  -> path incidence D_N
  -> weighted path Laplacian
```

The ordering and weights remain separately typed:

- Zeta/prime order supplies the declared frame sequence in the current candidate;
- Collatz first-merge geometry may supply positive edge mobility weights;
- half-frame gluing supplies local adjacency itself.

## 6. Joint architecture

The resulting candidate chain is

\[
\boxed{
\text{FRAME ORDER}
\to
\text{HALF SPLIT}
\to
\text{NEIGHBOR GLUING}
\to
P_{N+1}
\to
D_N
\to
L_V.
}
\]

With the amplitude layer included,

\[
\boxed{
i\partial_\Theta a=H_{\zeta C}a
\quad\to\quad
\text{half-frame interface readout on }V_N.
}
\]

With the elapsed-measure layer included,

\[
\boxed{
\{\theta_n\}_{E}
\to
\{\ell_j\}_{V},
\qquad
\sum_j\ell_j=\sum_n\theta_n.
}
\]

This separates temporal topology, amplitude propagation and elapsed measure while placing them on the same finite path complex.

## 7. Falsification gate

Reference tests require:

- exactly `N+1` vertices for `N` frames;
- incidence shape `(N+1,N)`;
- one `-1` and one `+1` per edge column;
- incidence rank `N`;
- weighted Laplacian symmetry and positive semidefiniteness;
- constant zero mode;
- exact uniform path spectrum;
- low-mode quadratic convergence.

Reference implementation: `temporal_path_incidence` and `temporal_support_laplacian` in `src/idt/half_frame_temporal_gluing.py`.
