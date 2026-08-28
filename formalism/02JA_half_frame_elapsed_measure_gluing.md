# 02JA — Half-Frame Elapsed-Measure Gluing

Status: `FORMAL_CANDIDATE / EXACT_MEASURE_CONSERVATION_GATE`

02J supplies the half-frame Hilbert quotient. This companion gate applies the same topology to the already-derived positive intrinsic temporal measure.

## 1. Framewise temporal measure

Let a finite temporal history contain `N` positive activity-derived frame intervals

\[
\boxed{\theta_n>0,\qquad n=1,\ldots,N,}
\]

with total intrinsic elapsed measure

\[
\boxed{\Theta_N=\sum_{n=1}^{N}\theta_n.}
\]

Each frame interval is split into equal left/right half-measures,

\[
\boxed{\theta_n=\frac{\theta_n}{2}+\frac{\theta_n}{2}.}
\]

## 2. Neighboring half-measure gluing

Using the same support topology as 02J, define

\[
\boxed{\ell_0=\frac{\theta_1}{2},}
\]

\[
\boxed{\ell_n=\frac{\theta_n+\theta_{n+1}}{2},\qquad 1\le n\le N-1,}
\]

\[
\boxed{\ell_N=\frac{\theta_N}{2}.}
\]

The supports are

```text
ell_0      -> |1|
ell_1      -> |12|
ell_2      -> |23|
...
ell_(N-1) -> |N-1,N|
ell_N      -> |N|
```

For `N=1`, the two supports are the two halves of the same frame,

\[
\boxed{(\ell_0,\ell_1)=(\theta_1/2,\theta_1/2).}
\]

## 3. Exact elapsed-measure conservation

Summing the glued support measures gives

\[
\begin{aligned}
\sum_{j=0}^{N}\ell_j
&=\frac{\theta_1}{2}
+\sum_{n=1}^{N-1}\frac{\theta_n+\theta_{n+1}}2
+\frac{\theta_N}{2}\\
&=\sum_{n=1}^{N}\theta_n.
\end{aligned}
\]

Therefore

\[
\boxed{\sum_{j=0}^{N}\ell_j=\Theta_N.}
\]

The half-frame overlap changes the support decomposition while preserving the total intrinsic elapsed measure exactly.

## 4. Uniform frames

For

\[
\theta_n=\theta,
\]

the glued support measures are

\[
\boxed{
\left(\frac\theta2,\theta,\theta,\ldots,\theta,\frac\theta2\right).
}
\]

Thus an extended uniform chain has half-width boundary supports and full-width neighboring overlap supports in its interior.

For the modular sectors:

```text
2pi  -> (theta/2, theta/2)                         -> |1|1|
4pi  -> (theta/2, theta, theta/2)                  -> |1|12|2|
6pi  -> (theta/2, theta, theta, theta/2)           -> |1|12|23|3|
8pi  -> (theta/2, theta, theta, theta, theta/2)    -> |1|12|23|34|4|
```

## 5. Relation to activity-derived time

00E derives each frame interval from positive relational activity,

\[
\boxed{\theta_n=\int_{\Gamma_n}\mathfrak a\,d\lambda>0.}
\]

02JA therefore acts after the intrinsic temporal measure has been derived. It reorganizes that measure over the half-frame quotient supports.

The composed map is

\[
\boxed{
\{\mathfrak a_n\}
\to
\{\theta_n\}
\to
\{\theta_n/2\}_{L,R}
\to
\{\ell_0,\ell_1,\ldots,\ell_N\},
}
\]

with exact total-measure closure at every finite `N`.

## 6. Joint amplitude/measure picture

02J supplies the glued amplitude interface

\[
b_n=\frac{a_n+a_{n+1}}2,
\]

while 02JA supplies its positive temporal support size

\[
\ell_n=\frac{\theta_n+\theta_{n+1}}2.
\]

Hence an internal fuzzy temporal interface carries the typed pair

\[
\boxed{\mathfrak F_{n,n+1}=(b_n,\ell_n).}
\]

The amplitude sector records coherent overlap; the measure sector records how much intrinsic elapsed support belongs to that interface.

## 7. Falsification gate

Reference tests require:

- all positive frame intervals produce positive glued support measures;
- output count is `N+1`;
- total elapsed measure is conserved exactly within floating tolerance;
- the declared `N=1..4` uniform patterns hold;
- nonuniform frame intervals preserve the same total measure.

Reference implementation: `glued_temporal_measures` in `src/idt/half_frame_temporal_gluing.py`.
