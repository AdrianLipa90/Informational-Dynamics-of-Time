# 06E — ORCHORBITAL Residence and Attractor-Transition Graph

Status: `PROVISIONAL_MEMORY_EXTENSION_REFERENCE_CLASS`

This layer extends the per-segment attractor field of `06D_orchorbital_attractor_system.md` into an ordered multi-segment system observable.

For ORCHORBITAL steps indexed by \(n\), let \(a_n\) be the attractor used on the completed segment and \(\Delta\tau_n>0\) its internal elapsed duration.

## 1. Residence time

For attractor \(i\), define the segment set

\[
\mathcal S_i=\{n:a_n=i\}.
\]

The ORCHORBITAL residence time is

\[
\boxed{
T_i^{\rm res}
=\sum_{n\in\mathcal S_i}\Delta\tau_n.
}
\]

This observable is measured in the already derived internal elapsed activity \(\tau_{\rm int}\).

The corresponding segment count is

\[
\boxed{
N_i^{\rm seg}=|\mathcal S_i|.
}
\]

## 2. Attractor-resolved winding

With segment winding increment \(\Delta W_{i,n}\), define

\[
\boxed{
W_i^{\rm tot}
=\sum_{n\in\mathcal S_i}\Delta W_{i,n}.
}
\]

This retains the orientation of the memory orbit separately for each attractor basin.

## 3. Directed transition graph

Adjacent completed segment labels generate the directed count

\[
\boxed{
N_{i\to j}
=\#\{n:a_n=i,\ a_{n+1}=j,\ i\neq j\}.
}
\]

The node set is the set of visited attractors and the directed weighted edge set is

\[
\boxed{
\mathcal G_A=(\mathcal V_A,\mathcal E_A),
\qquad
\mathcal E_A=\{(i,j,N_{i\to j}):N_{i\to j}>0\}.
}
\]

The reference implementation omits self-edges from the transition count while retaining same-attractor residence through \(N_i^{\rm seg}\) and \(T_i^{\rm res}\).

## 4. Boundary promotion rule

A completed segment records the post-segment attractor field. If its maximizing basin differs from the basin used on that segment, the next `orchorbital_step` re-evaluates the current memory state and promotes the newly maximizing basin as the active attractor of the following segment.

Thus the ordered reference chain is

\[
\boxed{
a_n
\rightarrow
X_{n+1}
\rightarrow
\mathrm{field}(X_{n+1})
\rightarrow
a_{n+1}
\rightarrow
N_{a_n\to a_{n+1}}.
}
\]

## 5. Reference controls

`tests/reference/test_orchorbital.py` verifies a constructed two-attractor trajectory in which the completed first segment uses attractor `A`, the boundary field changes to `B`, and the following segment uses `B`. The resulting directed transition graph contains exactly one `A -> B` edge.

The same suite verifies accumulation of three same-attractor segments into one residence record with total dwell time equal to the sum of their \(\Delta\tau\) values and positive accumulated winding.

The combined ORCHORBITAL reference result is recorded in `validation/ORCHORBITAL_ATTRACTOR_SYSTEM_V0_1.json` as `11 passed in 0.07s`.
