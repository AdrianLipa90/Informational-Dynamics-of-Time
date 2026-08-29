"""Physical ultrarelativistic neutrino stress-energy source helpers.

Conventions
-----------
Coordinates use ``x^0 = c t``.  The local stress-energy components therefore
share units of energy density (J m^-3):

    T^00 = u,
    T^0i = u n_i,
    T^ij = u n_i n_j

for a massless/ultrarelativistic stream of energy density ``u`` moving in the
unit direction ``n``.  After integrating over source volume, all components of
``mathcal_T^{mu nu} = integral T^{mu nu} d^3x`` have units of joule.

This module establishes source normalization and kinematic identities only.  It
does not assume any particular microscopic QHTRI-to-neutrino interaction.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

from .qhtri_neutrino_gravity import normalize_direction


FourTensor = tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
]


@dataclass(frozen=True)
class IntegratedNeutrinoStress:
    """Volume-integrated contravariant stress tensor in the x^0=ct convention."""

    tensor_joule: FourTensor
    total_energy_joule: float
    energy_flux_vector_joule: tuple[float, float, float]

    @property
    def spatial_stress_joule(self) -> tuple[tuple[float, float, float], ...]:
        return tuple(
            tuple(self.tensor_joule[i + 1][j + 1] for j in range(3))
            for i in range(3)
        )


def _finite_nonnegative(values: Sequence[float], name: str) -> tuple[float, ...]:
    out = tuple(float(x) for x in values)
    if not out:
        raise ValueError(f"{name} must be non-empty")
    if not all(math.isfinite(x) and x >= 0.0 for x in out):
        raise ValueError(f"{name} must be finite and non-negative")
    if sum(out) <= 0.0:
        raise ValueError(f"{name} must contain positive total energy")
    return out


def integrated_massless_stress(
    directions: Sequence[Sequence[float]],
    energies_joule: Sequence[float],
) -> IntegratedNeutrinoStress:
    """Construct ``integral T^{mu nu} d^3x`` for discrete massless streams.

    Each entry represents the total energy carried by one directional packet.
    The construction is the discrete kinetic-theory moment

        mathcal_T^{mu nu} = sum_a E_a k_a^mu k_a^nu,
        k_a^mu = (1, n_a),

    in the ``x^0=ct`` convention.
    """

    if len(directions) == 0 or len(directions) != len(energies_joule):
        raise ValueError("directions and energies_joule must have equal non-zero length")
    energies = _finite_nonnegative(energies_joule, "energies_joule")
    ns = tuple(normalize_direction(d) for d in directions)

    t = [[0.0 for _ in range(4)] for _ in range(4)]
    for energy, n in zip(energies, ns):
        k = (1.0, n[0], n[1], n[2])
        for mu in range(4):
            for nu in range(4):
                t[mu][nu] += energy * k[mu] * k[nu]

    tensor: FourTensor = tuple(tuple(row) for row in t)  # type: ignore[assignment]
    flux = (tensor[0][1], tensor[0][2], tensor[0][3])
    return IntegratedNeutrinoStress(
        tensor_joule=tensor,
        total_energy_joule=tensor[0][0],
        energy_flux_vector_joule=flux,
    )


def flavour_resolved_integrated_stress(
    directions: Sequence[Sequence[float]],
    flavour_energies_joule: Sequence[Sequence[float]],
) -> IntegratedNeutrinoStress:
    """Collapse flavour energies within each momentum direction before T^{mu nu}.

    Pure unitary flavour redistribution at fixed total energy in every momentum
    direction is therefore exactly stress-energy invariant.
    """

    if len(directions) == 0 or len(directions) != len(flavour_energies_joule):
        raise ValueError(
            "directions and flavour_energies_joule must have equal non-zero length"
        )
    width = len(flavour_energies_joule[0])
    if width == 0 or any(len(row) != width for row in flavour_energies_joule):
        raise ValueError("flavour rows must have one common non-zero width")

    totals = []
    for row in flavour_energies_joule:
        values = tuple(float(x) for x in row)
        if not all(math.isfinite(x) and x >= 0.0 for x in values):
            raise ValueError("flavour energies must be finite and non-negative")
        totals.append(sum(values))
    return integrated_massless_stress(directions, totals)


def local_stress_from_integrated(
    integrated: IntegratedNeutrinoStress,
    source_volume_m3: float,
) -> FourTensor:
    """Convert an integrated source tensor [J] to a uniform local tensor [J/m^3]."""

    volume = float(source_volume_m3)
    if not math.isfinite(volume) or volume <= 0.0:
        raise ValueError("source_volume_m3 must be finite and positive")
    return tuple(
        tuple(x / volume for x in row) for row in integrated.tensor_joule
    )  # type: ignore[return-value]


def minkowski_trace_plus_minus_minus_minus(tensor: Sequence[Sequence[float]]) -> float:
    """Return ``T^00 - T^11 - T^22 - T^33``."""

    if len(tensor) != 4 or any(len(row) != 4 for row in tensor):
        raise ValueError("expected a 4x4 tensor")
    return float(tensor[0][0] - tensor[1][1] - tensor[2][2] - tensor[3][3])


def integrated_four_momentum_si(
    source: IntegratedNeutrinoStress,
    c_si: float = 299_792_458.0,
) -> tuple[float, float, float, float]:
    """Return ``P^mu=(E/c,p_x,p_y,p_z)`` in SI momentum units [kg m/s]."""

    c = float(c_si)
    if not math.isfinite(c) or c <= 0.0:
        raise ValueError("c_si must be finite and positive")
    return (
        source.tensor_joule[0][0] / c,
        source.tensor_joule[0][1] / c,
        source.tensor_joule[0][2] / c,
        source.tensor_joule[0][3] / c,
    )
