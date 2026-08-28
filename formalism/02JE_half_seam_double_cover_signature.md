# 02JE — Half-Seam Double-Cover Signature

Status: `FORMAL_CANDIDATE / FOUR_PI_AMPLITUDE_RETURN_GATE`

02JD introduces the half-link factors `exp(± i varphi/2)` on each internal temporal seam. This layer records the exact periodicity consequences of that half-phase representation.

## 1. Two modular coordinates

The finite half-frame architecture carries two distinct phase coordinates.

The frame-count budget is

\[
\boxed{\Phi_N=2\pi N,}
\]

which labels the finite sector with `N` full frames and `N+1` glued supports.

Separately, every internal seam carries a local connection phase

\[
\boxed{\varphi_n\in\mathbb R/2\pi\mathbb Z}
\]

at the link level, represented on half-support amplitudes by

\[
\boxed{e^{\pm i\varphi_n/2}.}
\]

The frame-budget coordinate and the local seam phase remain separately typed.

## 2. Two-pi sign reversal on seam amplitudes

For the internal overlap amplitude

\[
b_n(\varphi)
=\frac{e^{+i\varphi/2}a_n+e^{-i\varphi/2}a_{n+1}}2,
\]

we have

\[
e^{\pm i(\varphi+2\pi)/2}
=-e^{\pm i\varphi/2}.
\]

Therefore

\[
\boxed{b_n(\varphi+2\pi)=-b_n(\varphi).}
\]

The same relation holds for the seam-defect amplitude,

\[
\boxed{d_n(\varphi+2\pi)=-d_n(\varphi).}
\]

Thus a `2pi` shift returns seam probabilities but reverses the seam amplitude sign.

## 3. Four-pi amplitude return

Applying the shift twice gives

\[
\boxed{b_n(\varphi+4\pi)=b_n(\varphi),}
\]

\[
\boxed{d_n(\varphi+4\pi)=d_n(\varphi).}
\]

At the phase-aware gluing-operator level, if every internal seam phase is shifted by `2pi`,

\[
\boxed{
Q_{\varphi+2\pi}=J_G Q_{\varphi},
}
\]

where `J_G` acts as `+1` on the two boundary supports and `-1` on every internal glued support. Hence

\[
\boxed{J_G^2=I,}
\]

and

\[
\boxed{Q_{\varphi+4\pi}=Q_{\varphi}.}
\]

This is the exact double-cover signature of the half-seam amplitude representation.

## 4. Two-pi observable return

Because the `2pi` transformation is only a sign reversal in the internal seam amplitude,

\[
\boxed{|b_n(\varphi+2\pi)|^2=|b_n(\varphi)|^2,}
\]

\[
\boxed{|d_n(\varphi+2\pi)|^2=|d_n(\varphi)|^2.}
\]

The amplitude carrier is therefore `4pi` periodic while the quadratic seam observables are `2pi` periodic.

## 5. Relation to the modular slice picture

The finite support pattern remains

\[
\boxed{
\mathcal T_N
=|1|\,|12|\,|23|\cdots|N|,
}
\]

with frame budget `Phi_N=2pi N`. The half-seam phase acts inside each overlap support and supplies the local amplitude sign structure.

Hence the architecture distinguishes

```text
2pi per added frame  -> finite support-count extension
4pi half-seam return -> local amplitude double-cover signature
2pi seam observable  -> probability/occupancy return
```

## 6. Spin-half comparison boundary

The `4pi` amplitude return is an exact algebraic property of the half-phase seam representation. A physical spin-1/2 identification requires an independent map from this seam carrier to an admitted physical spinorial state, transformation law and observable comparison.

## 7. Falsification gates

Reference tests require:

- internal overlap amplitudes reverse sign under `varphi -> varphi+2pi`;
- seam-defect amplitudes reverse sign under the same shift;
- both amplitudes return exactly under `varphi -> varphi+4pi`;
- seam probabilities are invariant under `2pi`;
- the full phase-aware gluing coisometry obeys `Q_(varphi+2pi)=J_G Q_varphi`;
- `J_G^2=I` and `Q_(varphi+4pi)=Q_varphi`.

Reference tests: `tests/reference/test_half_seam_double_cover.py`.
