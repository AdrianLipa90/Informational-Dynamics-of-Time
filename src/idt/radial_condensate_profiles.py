"""Radial condensate / orbital inverse identities for IDT 02JQ.

These functions implement algebraic consequences of a differentiable stationary
central scalar potential. They do not assert a physical BEC, GREMLIN-source,
RFC-coupling, or spacetime binding.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


class RadialCondensateError(ValueError):
    """Raised when a declared 02JQ domain condition is violated."""


def _positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0.0:
        raise RadialCondensateError(f"{name} must be finite and > 0")
    return value


def _finite(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise RadialCondensateError(f"{name} must be finite")
    return value


@dataclass(frozen=True)
class RadialObservables:
    radius: float
    omega_sq: float
    kappa_sq: float

    @property
    def k_obs(self) -> float:
        r = _positive("radius", self.radius)
        return r**3 * _finite("omega_sq", self.omega_sq)

    @property
    def hessian_radial(self) -> float:
        return _finite("kappa_sq", self.kappa_sq) - 3.0 * _finite(
            "omega_sq", self.omega_sq
        )

    @property
    def hessian_tangential(self) -> float:
        return _finite("omega_sq", self.omega_sq)


def epicyclic_sq(radius: float, omega_sq: float, d_omega_sq_dr: float) -> float:
    """Return kappa^2 = 4 Omega^2 + r d(Omega^2)/dr."""

    r = _positive("radius", radius)
    w2 = _finite("omega_sq", omega_sq)
    dw2 = _finite("d_omega_sq_dr", d_omega_sq_dr)
    return 4.0 * w2 + r * dw2


def central_consistency_residual(
    radius: float,
    omega_sq: float,
    d_omega_sq_dr: float,
    measured_kappa_sq: float,
) -> float:
    """BELZEBUB-style fail-closed residual for a stationary central scalar."""

    return _finite("measured_kappa_sq", measured_kappa_sq) - epicyclic_sq(
        radius, omega_sq, d_omega_sq_dr
    )


def k_obs(radius: float, omega_sq: float) -> float:
    r = _positive("radius", radius)
    return r**3 * _finite("omega_sq", omega_sq)


def k_obs_gradient_from_epicycle(
    radius: float, omega_sq: float, kappa_sq: float
) -> float:
    """Exact identity d(r^3 Omega^2)/dr = r^2 (kappa^2 - Omega^2)."""

    r = _positive("radius", radius)
    return r**2 * (
        _finite("kappa_sq", kappa_sq) - _finite("omega_sq", omega_sq)
    )


def power_law_epicyclic_sq(omega_sq: float, exponent_q: float) -> float:
    return (4.0 - _finite("exponent_q", exponent_q)) * _finite(
        "omega_sq", omega_sq
    )


def power_law_potential(
    radius: float,
    amplitude: float,
    exponent_q: float,
    *,
    reference_radius: float = 1.0,
    additive_constant: float = 0.0,
) -> float:
    """Potential whose circular law is Omega^2 = A r^{-q}."""

    r = _positive("radius", radius)
    a = _finite("amplitude", amplitude)
    q = _finite("exponent_q", exponent_q)
    c = _finite("additive_constant", additive_constant)
    if math.isclose(q, 2.0, rel_tol=0.0, abs_tol=1e-15):
        r0 = _positive("reference_radius", reference_radius)
        return c + a * math.log(r / r0)
    return c + a * r ** (2.0 - q) / (2.0 - q)


def mean_field_inverse_density(
    radius: float,
    *,
    rho0: float,
    amplitude: float,
    exponent_q: float,
    mobility: float,
    coupling_g: float,
    reference_radius: float = 1.0,
) -> float:
    """Density generating Delta Omega_g^2 = A r^{-q} via Phi_g=2 M g rho."""

    r = _positive("radius", radius)
    m = _positive("mobility", mobility)
    g = _finite("coupling_g", coupling_g)
    if g == 0.0:
        raise RadialCondensateError("coupling_g must be non-zero")
    a = _finite("amplitude", amplitude)
    q = _finite("exponent_q", exponent_q)
    base = _finite("rho0", rho0)

    if math.isclose(q, 2.0, rel_tol=0.0, abs_tol=1e-15):
        r0 = _positive("reference_radius", reference_radius)
        return base + a * math.log(r / r0) / (2.0 * m * g)

    return base + a * r ** (2.0 - q) / (2.0 * m * g * (2.0 - q))


def quantum_pressure_inverse_ode_coefficient(
    phi_q: float, mobility: float
) -> float:
    """Coefficient c(r) in f''+(d-1)f'/r+c(r)f=0 for f=sqrt(rho)."""

    m = _positive("mobility", mobility)
    return _finite("phi_q", phi_q) / (2.0 * m * m)


def holonomy_shell_susceptibility_nu(
    radius: float,
    *,
    circulation_scale: float,
    effective_winding: float,
    kappa_sq: float,
) -> float:
    """dr/dnu for r^2 Omega = Lambda nu."""

    r = _positive("radius", radius)
    lam = _positive("circulation_scale", circulation_scale)
    nu = _finite("effective_winding", effective_winding)
    k2 = _finite("kappa_sq", kappa_sq)
    if k2 == 0.0:
        raise RadialCondensateError("kappa_sq must be non-zero")
    return 2.0 * lam * lam * nu / (r**3 * k2)


def holonomy_shell_susceptibility_tau(
    radius: float,
    *,
    circulation_scale: float,
    effective_winding: float,
    kappa_sq: float,
) -> float:
    """dr/dtau with nu = ell - tau/(2 pi)."""

    return -holonomy_shell_susceptibility_nu(
        radius,
        circulation_scale=circulation_scale,
        effective_winding=effective_winding,
        kappa_sq=kappa_sq,
    ) / (2.0 * math.pi)


def transverse_phase_gradient(
    radius: float, impact_parameter: float, omega_sq: float
) -> float:
    """d Phi/db = b Omega^2 for a spherical scalar."""

    r = _positive("radius", radius)
    b = _finite("impact_parameter", impact_parameter)
    if abs(b) > r:
        raise RadialCondensateError("|impact_parameter| must be <= radius")
    return b * _finite("omega_sq", omega_sq)


def transverse_phase_curvature(
    radius: float,
    impact_parameter: float,
    omega_sq: float,
    kappa_sq: float,
) -> float:
    """d^2 Phi/db^2 expressed through orbital and epicyclic observables."""

    r = _positive("radius", radius)
    b = _finite("impact_parameter", impact_parameter)
    if abs(b) > r:
        raise RadialCondensateError("|impact_parameter| must be <= radius")
    w2 = _finite("omega_sq", omega_sq)
    k2 = _finite("kappa_sq", kappa_sq)
    beta2 = (b / r) ** 2
    return beta2 * k2 + (1.0 - 4.0 * beta2) * w2


def condensate_subtracted_residual(
    radius: float,
    omega_sq: float,
    *,
    k_orb: float,
    mobility: float,
    coupling_g: float,
    density_gradient: float,
    q_density_gradient: float,
) -> float:
    """Return G_res after removing central, mean-field and quantum-pressure terms."""

    r = _positive("radius", radius)
    w2 = _finite("omega_sq", omega_sq)
    k = _finite("k_orb", k_orb)
    m = _positive("mobility", mobility)
    g = _finite("coupling_g", coupling_g)
    rho_p = _finite("density_gradient", density_gradient)
    q_p = _finite("q_density_gradient", q_density_gradient)
    return r * w2 - k / (r * r) - 2.0 * m * g * rho_p + 2.0 * m * m * q_p
