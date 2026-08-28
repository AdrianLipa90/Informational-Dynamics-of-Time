# 02JC — Half-Frame NOW Frontier Update

Status: `FORMAL_CANDIDATE / FRONTIER_REALIZATION_GATE`

02J–02JB produce a finite path of glued temporal supports. This gate identifies the serial maximal support with the existing NOW frontier and derives its update under one realized frame extension.

## 1. Finite support chain

For `N` realized frames define

\[
\boxed{
\mathcal T_N
=
\bigl(
|1|,
|12|,
|23|,
\ldots,
|N-1,N|,
|N|
\bigr).
}
\]

The final pure support is

\[
\boxed{\mathcal N_N:=|N|_\partial.}
\]

On the path complex of 02JB this is the terminal vertex `v_N`, hence the maximal serial support.

## 2. One-frame extension

Append one realized frame `N+1`. Its left half-support is glued to the previous terminal right half-support,

\[
\boxed{|N,R\rangle\sim|N+1,L\rangle.}
\]

Therefore the support sequence updates by

\[
\boxed{
\mathcal T_N
\longmapsto
\mathcal T_{N+1}
=
\bigl(
|1|,
|12|,
\ldots,
|N,N+1|,
|N+1|
\bigr).
}
\]

Equivalently, the terminal update rule is

\[
\boxed{
|N|_\partial
\longmapsto
|N,N+1|,
\qquad
\text{append }|N+1|_\partial.
}
\]

Thus the former pure frontier becomes an internal neighboring-overlap support and the new right boundary becomes the serial maximal support.

## 3. NOW realization

The independently derived relational NOW gate defines NOW as the maximal supported realized occurrence frontier. On the serial half-frame path this has the realization

\[
\boxed{
\mathrm{NOW}_N
\leftrightarrow
|N|_\partial.
}
\]

After one admitted extension,

\[
\boxed{
\mathrm{NOW}_{N+1}
\leftrightarrow
|N+1|_\partial.
}
\]

The support geometry therefore carries an explicit moving-frontier representation of the same maximality rule.

## 4. Elapsed-measure update

Let the old final frame carry positive measure `theta_N` and the new frame carry `theta_(N+1)>0`. Before extension, the final pure support has measure

\[
\boxed{\ell_N^{(N)}=\frac{\theta_N}{2}.}
\]

After extension, it is replaced by

\[
\boxed{
\ell_N^{(N+1)}
=\frac{\theta_N+\theta_{N+1}}2
}
\]

and the new frontier carries

\[
\boxed{
\ell_{N+1}^{(N+1)}
=\frac{\theta_{N+1}}2.
}
\]

The added total support is exactly

\[
\boxed{
\left[
\ell_N^{(N+1)}+\ell_{N+1}^{(N+1)}
\right]
-\ell_N^{(N)}
=\theta_{N+1}.
}
\]

Thus each realized frame extension increases the total intrinsic elapsed measure by precisely the positive measure of the new frame.

## 5. Prefix compatibility

Let the realized temporal history after `N` transitions be represented by prefix occurrence `P_N`. The next admitted relation gives

\[
P_N\sqsubset P_{N+1}.
\]

The activity-derived measure satisfies

\[
\Theta(P_{N+1})
=\Theta(P_N)+\theta_{N+1}
>\Theta(P_N).
\]

The half-frame frontier update and the prefix-order temporal update therefore share the same one-step extension index.

## 6. Support-history interpretation

At every finite serial stage:

```text
internal glued supports : retained neighboring history interfaces
right pure boundary     : current maximal support / NOW realization
next admitted frame     : converts old boundary into an internal interface
new right boundary      : new maximal support
```

This provides a concrete finite-support realization of the already admitted NOW maximal-frontier rule.

## 7. Evidence boundary

This gate promotes only the exact combinatorial and measure identities of the half-frame realization. Retrocausal experimental classification, physical spinor binding and microscopic frame identification retain their declared downstream gates.

Reference tests are included in `tests/reference/test_half_frame_now_frontier.py`.
