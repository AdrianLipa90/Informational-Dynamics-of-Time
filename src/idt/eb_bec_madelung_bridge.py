from __future__ import annotations

import cmath
import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


class EBBECBridgeError(ValueError):
    pass


def _finite(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise EBBECBridgeError(f"{name} must be finite")
    return out


def _positive(value: float, name: str) -> float:
    out = _finite(value, name)
    if out <= 0.0:
        raise EBBECBridgeError(f"{name} must be positive")
    return out


def _nonnegative(value: float, name: str) -> float:
    out = _finite(value, name)
    if out < 0.0:
        raise EBBECBridgeError(f"{name} must be non-negative")
    return out


def _finite_vector(values: Sequence[float], name: str) -> np.ndarray:
    out = np.asarray(values, dtype=float)
    if out.ndim != 1 or out.size == 0 or not np.all(np.isfinite(out)):
        raise EBBECBridgeError(
            f"{name} must be a finite non-empty one-dimensional vector"
        )
    return out


@dataclass(frozen=True)
class BECPhysicalBridge:
    """Typed local calibration between intrinsic IDT and a physical BEC branch.

    Conventions:
      theta = dtheta_dt * t locally;
      x_phys = spatial_scale * x_idt;
      rho_bec = density_scale * rho_idt.

    The bridge is algebraic only.  It does not assert that the IDT continuum
    coordinate is physically realized by a condensate.
    """

    mass: float
    hbar: float
    dtheta_dt: float
    spatial_scale: float = 1.0
    density_scale: float = 1.0

    def __post_init__(self) -> None:
        for name in (
            "mass",
            "hbar",
            "dtheta_dt",
            "spatial_scale",
            "density_scale",
        ):
            object.__setattr__(self, name, _positive(getattr(self, name), name))

    @property
    def idt_mobility(self) -> float:
        return self.hbar / (
            2.0 * self.mass * self.dtheta_dt * self.spatial_scale**2
        )

    def idt_potential(self, physical_potential: float) -> float:
        return _finite(physical_potential, "physical_potential") / (
            self.hbar * self.dtheta_dt
        )

    def idt_nonlinear_coupling(self, contact_coupling: float) -> float:
        return (
            _finite(contact_coupling, "contact_coupling")
            * self.density_scale
            / (self.hbar * self.dtheta_dt)
        )

    def physical_density(self, idt_density: float) -> float:
        return self.density_scale * _positive(idt_density, "idt_density")

    def intrinsic_wave_number(self, physical_wave_number: float) -> float:
        return self.spatial_scale * _finite(
            physical_wave_number, "physical_wave_number"
        )

    def physical_frequency(self, intrinsic_frequency: float) -> float:
        return self.dtheta_dt * _finite(
            intrinsic_frequency, "intrinsic_frequency"
        )

    def physical_velocity(self, intrinsic_velocity: float) -> float:
        return (
            self.spatial_scale
            * self.dtheta_dt
            * _finite(intrinsic_velocity, "intrinsic_velocity")
        )

    def physical_connection(self, idt_connection: float) -> float:
        return (
            self.hbar
            / self.spatial_scale
            * _finite(idt_connection, "idt_connection")
        )

    def intrinsic_sound_speed_sq(
        self,
        contact_coupling: float,
        idt_background_density: float,
    ) -> float:
        rho0 = _positive(idt_background_density, "idt_background_density")
        lam = self.idt_nonlinear_coupling(contact_coupling)
        return 2.0 * self.idt_mobility * lam * rho0

    def physical_sound_speed_sq(
        self,
        contact_coupling: float,
        idt_background_density: float,
    ) -> float:
        return (
            self.spatial_scale * self.dtheta_dt
        ) ** 2 * self.intrinsic_sound_speed_sq(
            contact_coupling,
            idt_background_density,
        )


def nonlinear_characteristic_coefficients(
    wave_number: float,
    mobility: float,
    background_density: float,
    onsager_mobility: float,
    nonlinear_coupling: float,
) -> tuple[float, float, float]:
    k = _finite(wave_number, "wave_number")
    m = _positive(mobility, "mobility")
    rho0 = _positive(background_density, "background_density")
    mu = _nonnegative(onsager_mobility, "onsager_mobility")
    lam = _finite(nonlinear_coupling, "nonlinear_coupling")
    return (
        1.0,
        2.0 * mu * m * rho0 * k * k,
        2.0 * m * lam * rho0 * k * k + m * m * k**4,
    )


def nonlinear_mode_roots(
    wave_number: float,
    mobility: float,
    background_density: float,
    onsager_mobility: float,
    nonlinear_coupling: float,
) -> tuple[complex, complex]:
    a, b, c = nonlinear_characteristic_coefficients(
        wave_number,
        mobility,
        background_density,
        onsager_mobility,
        nonlinear_coupling,
    )
    root = cmath.sqrt(complex(b * b - 4.0 * a * c, 0.0))
    return ((-b + root) / (2.0 * a), (-b - root) / (2.0 * a))


def intrinsic_bogoliubov_omega_sq(
    wave_number: float,
    mobility: float,
    background_density: float,
    nonlinear_coupling: float,
) -> float:
    k = _finite(wave_number, "wave_number")
    m = _positive(mobility, "mobility")
    rho0 = _positive(background_density, "background_density")
    lam = _finite(nonlinear_coupling, "nonlinear_coupling")
    return 2.0 * m * lam * rho0 * k * k + m * m * k**4


def physical_bogoliubov_omega_sq(
    wave_number: float,
    mass: float,
    hbar: float,
    contact_coupling: float,
    physical_density: float,
) -> float:
    k = _finite(wave_number, "wave_number")
    m = _positive(mass, "mass")
    hb = _positive(hbar, "hbar")
    g = _finite(contact_coupling, "contact_coupling")
    rho = _positive(physical_density, "physical_density")
    return (g * rho / m) * k * k + (hb * hb / (4.0 * m * m)) * k**4


def dilute_3d_contact_coupling(
    hbar: float,
    mass: float,
    scattering_length: float,
) -> float:
    hb = _positive(hbar, "hbar")
    m = _positive(mass, "mass")
    a_s = _finite(scattering_length, "scattering_length")
    return 4.0 * math.pi * hb * hb * a_s / m


@dataclass(frozen=True)
class OrbitalKDecomposition:
    central: float
    information: float
    mean_field: float
    quantum_pressure: float

    @property
    def total(self) -> float:
        return (
            self.central
            + self.information
            + self.mean_field
            + self.quantum_pressure
        )


def orbital_k_decomposition(
    radius: float,
    mass: float,
    source_strength: float,
    source_coupling: float,
    information_coupling: float,
    information_gradient: float,
    contact_coupling: float,
    density_gradient: float,
    quantum_pressure_gradient: float,
) -> OrbitalKDecomposition:
    r = _positive(radius, "radius")
    m = _positive(mass, "mass")
    mu_s = _positive(source_strength, "source_strength")
    q_g = _positive(source_coupling, "source_coupling")
    c_i = _finite(information_coupling, "information_coupling")
    xi_r = _finite(information_gradient, "information_gradient")
    g = _finite(contact_coupling, "contact_coupling")
    rho_r = _finite(density_gradient, "density_gradient")
    q_b_r = _finite(quantum_pressure_gradient, "quantum_pressure_gradient")

    factor = r * r / m
    return OrbitalKDecomposition(
        central=mu_s * q_g / m,
        information=factor * c_i * xi_r,
        mean_field=factor * g * rho_r,
        quantum_pressure=factor * q_b_r,
    )


def effective_winding(integer_winding: int, total_holonomy: float) -> float:
    if not isinstance(integer_winding, int) or isinstance(integer_winding, bool):
        raise EBBECBridgeError("integer_winding must be an integer")
    tau = _finite(total_holonomy, "total_holonomy")
    return float(integer_winding) - tau / (2.0 * math.pi)


def holonomy_radius_one_over_r(
    hbar: float,
    mass: float,
    source_coupling: float,
    source_strength: float,
    integer_winding: int,
    total_holonomy: float,
) -> float:
    hb = _positive(hbar, "hbar")
    m = _positive(mass, "mass")
    q_g = _positive(source_coupling, "source_coupling")
    mu_s = _positive(source_strength, "source_strength")
    nu = effective_winding(integer_winding, total_holonomy)
    if nu == 0.0:
        raise EBBECBridgeError(
            "effective winding must be non-zero for a positive circular shell"
        )
    return hb * hb * nu * nu / (m * q_g * mu_s)


def holonomy_radial_balance_residual(
    hbar: float,
    mass: float,
    radius: float,
    integer_winding: int,
    total_holonomy: float,
    total_potential_gradient: float,
) -> float:
    hb = _positive(hbar, "hbar")
    m = _positive(mass, "mass")
    r = _positive(radius, "radius")
    nu = effective_winding(integer_winding, total_holonomy)
    d_u = _finite(total_potential_gradient, "total_potential_gradient")
    return hb * hb * nu * nu - m * r**3 * d_u


def thomas_fermi_density(
    chemical_potential: float,
    external_potential: float,
    information_potential: float,
    contact_coupling: float,
) -> float:
    mu_c = _finite(chemical_potential, "chemical_potential")
    u_ext = _finite(external_potential, "external_potential")
    u_i = _finite(information_potential, "information_potential")
    g = _positive(contact_coupling, "contact_coupling")
    numerator = mu_c - u_ext - u_i
    if numerator <= 0.0:
        raise EBBECBridgeError(
            "Thomas-Fermi density requires positive local chemical-potential excess"
        )
    return numerator / g


def thomas_fermi_sound_speed_sq(
    chemical_potential: float,
    external_potential: float,
    information_potential: float,
    mass: float,
) -> float:
    m = _positive(mass, "mass")
    numerator = (
        _finite(chemical_potential, "chemical_potential")
        - _finite(external_potential, "external_potential")
        - _finite(information_potential, "information_potential")
    )
    if numerator <= 0.0:
        raise EBBECBridgeError(
            "Thomas-Fermi sound speed requires positive local chemical-potential excess"
        )
    return numerator / m


def information_sound_speed_shift(
    delta_information_potential: float,
    mass: float,
) -> float:
    return -_finite(
        delta_information_potential, "delta_information_potential"
    ) / _positive(mass, "mass")


def acoustic_metric(
    density: float,
    sound_speed: float,
    velocity: Sequence[float],
) -> np.ndarray:
    rho = _positive(density, "density")
    c_s = _positive(sound_speed, "sound_speed")
    v = _finite_vector(velocity, "velocity")
    dimension = v.size
    metric = np.zeros((dimension + 1, dimension + 1), dtype=float)
    v_sq = float(v @ v)
    metric[0, 0] = -(c_s * c_s - v_sq)
    metric[0, 1:] = -v
    metric[1:, 0] = -v
    metric[1:, 1:] = np.eye(dimension)
    return (rho / c_s) * metric
