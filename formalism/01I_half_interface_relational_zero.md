# 01I — Half Interface / Relational Zero Principle

Status: `TARGETED_DERIVATION_PASS_CANDIDATE`

Base provenance: `AdrianLipa90/Informational-Dynamics-of-Time@79898fc1584a5dc238f517359ae19f1d31521db0` (`feat/shannon-onsager-response-v0.1`).

## 1. Binary relational coordinate

For a complementary pair with probability coordinate \(p\in[0,1]\), define the signed relational imbalance

\[
\boxed{X=2p-1.}
\]

Then

\[
\boxed{X=0\iff p=\frac12.}
\]

The point \(X=0\) is therefore the balanced interface of the two complementary channels.

For binary Shannon entropy

\[
H(p)=-p\ln p-(1-p)\ln(1-p),
\]

one has

\[
H\!\left(\frac12\right)=\ln2,\qquad
H'\!\left(\frac12\right)=0,\qquad
H''\!\left(\frac12\right)=-4.
\]

In the centred coordinate \(X\),

\[
\boxed{H(X)=\ln2-\frac12X^2+O(X^4).}
\]

Thus the balanced interface is simultaneously the zero of signed local imbalance and the stationary maximum of binary Shannon uncertainty.

## 2. Spinorial half-turn

Use the 01H spinorial phase carrier

\[
z_{1/2}(\tau)=e^{i\tau/2}.
\]

A \(2\pi\) displacement in the \(4\pi\)-periodic lift gives

\[
\Delta\tau=2\pi
\quad\Longrightarrow\quad
z_{1/2}(\tau+\Delta\tau)=-z_{1/2}(\tau),
\]

while the full return occurs after \(4\pi\). Hence

\[
\boxed{\frac{2\pi}{4\pi}=\frac12}
\]

is the normalized half-turn of the spinorial cover.

## 3. Exact relational-zero kernel

For a two-channel normalized state, introduce

\[
\mathcal D_{1/2}(p,\Delta\tau)
=
\left|\sqrt p+e^{i\Delta\tau/2}\sqrt{1-p}\right|^2.
\]

Expanding,

\[
\boxed{\mathcal D_{1/2}=1+2\sqrt{p(1-p)}\cos\!\left(\frac{\Delta\tau}{2}\right).}
\]

For \(p\in[0,1]\),

\[
\boxed{\mathcal D_{1/2}=0
\iff
p=\frac12
\ \land\ 
\Delta\tau\equiv2\pi\pmod{4\pi}.}
\]

At that point the measured symmetric channel cancels while the underlying normalized two-channel state remains finite. The exact zero is therefore a zero of a relational projection.

## 4. Typed role in Informational Dynamics of Time

01I introduces the typed relation

\[
\boxed{0_{\rm relational}\leftrightarrow\left(X=0,\ H=\ln2,\ \text{spinorial half-turn}\right).}
\]

The same kernel can be instantiated by any admitted complementary pair, provided the pair weights and phase carrier are explicitly identified. Candidate application domains include past/future branches, local/nonlocal channels, and chemical transition amplitudes. Each physical binding requires its own admission and falsification gate.

## 5. Cross-repository contract

This gate is prepared for:

- `AdrianLipa90/secret-of-a-half` — balanced two-channel cancellation and spinorial \(2\pi\) sign change;
- `AdrianLipa90/The-Fundamental-Theory-of-Informational-Relations` — Shannon/Kähler/phase geometry;
- `AdrianLipa90/Resonant-Chemistry` — chemical state, orbital, transition and spectral observables.

Cross-repository contract ID:

`RCE_CHEM_PHOTO_EM_BRIDGE_V0_1`

GREMLIN may propose relational isomorphisms across these domains. Promotion remains controlled by the repository dependency graph and reproducible tests.
