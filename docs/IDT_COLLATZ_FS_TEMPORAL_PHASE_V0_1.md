# IDT Collatz–Fubini–Study Temporal Phase Interface v0.1

**Date:** 2026-09-04  
**Status:** `EXACT_DISCRETE_PHASE_MAP / PHYSICAL_TIME_BINDING_OPEN`  
**Scope:** temporal formalism only; no spectroscopic or gravitational claim is promoted here.

## 1. Purpose

This note adds a discrete phase coordinate to the temporal layer without identifying that coordinate with physical clock time by assumption.

Let the unreduced Collatz map be

\[
C(n)=\begin{cases}
n/2,&n\equiv0\pmod2,\\
3n+1,&n\equiv1\pmod2.
\end{cases}
\]

For an orbit define the parity itinerary

\[
b_k(n)=C^k(n)\bmod2\in\{0,1\}.
\]

For every orbit that reaches the terminal cycle \(1\to4\to2\to1\), define

\[
q(n)=\sum_{k=0}^{\infty}\frac{b_k(n)}{2^{k+1}},
\qquad
\zeta_C(n)=e^{2\pi i q(n)}.
\]

The parity shift gives exactly

\[
q(Cn)=2q(n)\pmod1,
\qquad
\boxed{\zeta_C(Cn)=\zeta_C(n)^2}.
\]

Thus the admitted mathematical phase dynamics is the doubling map

\[
\boxed{\phi_{k+1}=2\phi_k\pmod{2\pi}},
\qquad
\zeta_C=e^{i\phi}.
\]

No physical identification of one Collatz iteration with a fixed elapsed duration is made.

## 2. Terminal-cycle quantization

The repeating parity words of the terminal cycle are

\[
1:\;100100100\ldots,
\qquad
2:\;010010010\ldots,
\qquad
4:\;001001001\ldots
\]

and therefore

\[
\boxed{q(1)=4/7},\qquad
\boxed{q(2)=2/7},\qquad
\boxed{q(4)=1/7}.
\]

The cycle is represented on \(S^1\) as

\[
\frac17\to\frac27\to\frac47\to\frac17\pmod1.
\]

For an orbit whose first arrival at 1 occurs after \(L_n\) steps,

\[
q(n)=\sum_{k=0}^{L_n-1}\frac{b_k}{2^{k+1}}
+\frac{4}{7\,2^{L_n}},
\]

hence

\[
\boxed{q(n)\in\frac{1}{7\,2^{L_n}}\mathbb Z},
\qquad
\boxed{\zeta_C(n)^{7\,2^{L_n}}=1}.
\]

This is conditional on the orbit reaching the terminal cycle; it is not a proof of the Collatz conjecture.

## 3. Projective placement

Place the phase on the equator of a two-state projective carrier,

\[
|\psi_n\rangle=
\frac{|0\rangle+\zeta_C(n)|1\rangle}{\sqrt2}.
\]

Then

\[
|\zeta_C|=1,
\qquad
\theta=\pi/2,
\]

and the Fubini–Study line element restricted to the equator is

\[
\boxed{ds_{FS}^2=\frac14\,d\phi^2}
\]

for the standard radius-1/2 normalization.

The symbol \(\zeta\) is therefore a projective phase coordinate. It is **not** the complex number zero. A temporal reset may instead be written

\[
\tau_\zeta=0\pmod{2\pi}.
\]

## 4. 2π / 4π split

The projective phase closes on \(S^1\) modulo \(2\pi\). A spin-1/2 lift may be carried on the double cover,

\[
\widetilde\phi\in\mathbb R/4\pi\mathbb Z,
\]

with projection

\[
\widetilde\phi\mapsto\phi=\widetilde\phi\pmod{2\pi}.
\]

This establishes a typed distinction between projective phase closure and spinor closure. It does not by itself establish a new physical time law.

## 5. IDT state extension

The minimal compatible temporal state is

\[
\boxed{\mathcal T=(t,\phi,\widetilde\phi)}
\]

with the discrete phase operator

\[
\mathcal C_\phi:\phi\mapsto2\phi\pmod{2\pi}.
\]

Continuous elapsed activity and the discrete phase itinerary remain separate coordinates until a physical binding is derived.

## 6. Validation receipt

The companion validator checks integers \(1\le n\le10000\):

- every tested orbit reaches 1;
- \(q(Cn)=2q(n)\pmod1\);
- `denominator(q(n))` divides \(7\,2^{L_n}\);
- exact anchors \(q(1)=4/7\), \(q(2)=2/7\), \(q(4)=1/7\), \(q(3)=141/224\).

Reference result on 2026-09-04: `10000/10000 PASS`, zero arithmetic exceptions.

## 7. Claim firewall

**EXACT / CONDITIONAL MATHEMATICS**

- parity-itinerary definition;
- doubling-map identity;
- terminal-cycle fractions;
- root-of-unity quantization for trajectories reaching 1;
- equatorial CP1 placement.

**OPEN PHYSICAL BINDINGS**

- conversion from iteration count or phase increment to elapsed SI time;
- coupling to energy, mass, frequency or gravity;
- observable role in atomic selection rules or spectra.
