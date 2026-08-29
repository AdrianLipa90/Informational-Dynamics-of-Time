from __future__ import annotations

import math
from dataclasses import dataclass


class TemporalMaterialFrontError(ValueError):
    pass


@dataclass(frozen=True)
class MaterialFrontKinematics:
    current_transport_velocity: float
    boundary_flux_correction: float
    selector_drift_velocity: float
    total_velocity: float


def _finite(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise TemporalMaterialFrontError(f"{name} must be finite")
    return out


def _positive(value: float, name: str) -> float:
    out = _finite(value, name)
    if out <= 0.0:
        raise TemporalMaterialFrontError(f"{name} must be positive")
    return out


def _probability(value: float, name: str = "p") -> float:
    out = _finite(value, name)
    if not 0.0 < out < 1.0:
        raise TemporalMaterialFrontError(f"{name} must lie strictly between 0 and 1")
    return out


def total_mass_rate(left_flux: float, right_flux: float) -> float:
    return _finite(left_flux, "left_flux") - _finite(right_flux, "right_flux")


def material_front_velocity(
    *,
    p: float,
    density_at_front: float,
    current_at_front: float,
    total_mass: float,
    selector_rate: float = 0.0,
    left_flux: float = 0.0,
    right_flux: float = 0.0,
) -> MaterialFrontKinematics:
    probability = _probability(p)
    rho = _positive(density_at_front, "density_at_front")
    mass = _positive(total_mass, "total_mass")
    current = _finite(current_at_front, "current_at_front")
    p_dot = _finite(selector_rate, "selector_rate")
    j_left = _finite(left_flux, "left_flux")
    j_right = _finite(right_flux, "right_flux")

    transport = current / rho
    boundary = (-(1.0 - probability) * j_left - probability * j_right) / rho
    selector = mass * p_dot / rho
    return MaterialFrontKinematics(
        current_transport_velocity=transport,
        boundary_flux_correction=boundary,
        selector_drift_velocity=selector,
        total_velocity=transport + boundary + selector,
    )


def no_flux_material_front_velocity(
    *,
    density_at_front: float,
    current_at_front: float,
    total_mass: float,
    selector_rate: float = 0.0,
    p: float = 0.5,
) -> MaterialFrontKinematics:
    return material_front_velocity(
        p=p,
        density_at_front=density_at_front,
        current_at_front=current_at_front,
        total_mass=total_mass,
        selector_rate=selector_rate,
        left_flux=0.0,
        right_flux=0.0,
    )


def logistic_quantile(
    p: float,
    theta: float,
    *,
    velocity: float,
    scale: float,
    origin: float = 0.0,
) -> float:
    probability = _probability(p)
    th = _finite(theta, "theta")
    v = _finite(velocity, "velocity")
    s = _positive(scale, "scale")
    x0 = _finite(origin, "origin")
    return x0 + v * th + s * math.log(probability / (1.0 - probability))


def logistic_density_at_quantile(p: float, *, scale: float) -> float:
    probability = _probability(p)
    s = _positive(scale, "scale")
    return probability * (1.0 - probability) / s


def logistic_quantile_velocity(
    p: float,
    *,
    velocity: float,
    scale: float,
    selector_rate: float = 0.0,
) -> float:
    probability = _probability(p)
    v = _finite(velocity, "velocity")
    s = _positive(scale, "scale")
    p_dot = _finite(selector_rate, "selector_rate")
    return v + s * p_dot / (probability * (1.0 - probability))


def phase_diffusion_coefficient(onsager_mobility: float, coefficient: float) -> float:
    mu = _positive(onsager_mobility, "onsager_mobility")
    c = _positive(coefficient, "coefficient")
    return 2.0 * mu * c


def phase_diffusion_variance(
    delta_theta: float,
    *,
    onsager_mobility: float,
    coefficient: float,
) -> float:
    dt = _positive(delta_theta, "delta_theta")
    diffusion = phase_diffusion_coefficient(onsager_mobility, coefficient)
    return 2.0 * diffusion * dt


def phase_diffusion_sigma(
    delta_theta: float,
    *,
    onsager_mobility: float,
    coefficient: float,
) -> float:
    return math.sqrt(
        phase_diffusion_variance(
            delta_theta,
            onsager_mobility=onsager_mobility,
            coefficient=coefficient,
        )
    )


def phase_diffusion_green(
    x: float,
    delta_theta: float,
    *,
    onsager_mobility: float,
    coefficient: float,
) -> float:
    position = _finite(x, "x")
    dt = _positive(delta_theta, "delta_theta")
    diffusion = phase_diffusion_coefficient(onsager_mobility, coefficient)
    denominator = math.sqrt(4.0 * math.pi * diffusion * dt)
    return math.exp(-(position * position) / (4.0 * diffusion * dt)) / denominator
