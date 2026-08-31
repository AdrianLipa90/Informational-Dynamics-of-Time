"""IDT 05I regular smooth clock-extension witness certifier.

The certifier validates a supplied finite 4D affine-chart witness for a smooth
regular scalar clock extending a discrete 05H event clock.  It certifies the
witness; it does not infer existence of such a witness from graph exactness.

On patch p:
    t_p(x) = a_p . x + b_p,      a_p != 0.

On overlap p -> q:
    x_q = A_{q<-p} x_p + s_{q<-p}.

Scalar compatibility is the coefficient identity
    a_q A_{q<-p} = a_p,
    a_q . s_{q<-p} + b_q = b_p.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from typing import Iterable, Mapping, Sequence


class SmoothClockExtensionError(ValueError):
    """Raised when a declared 05I smooth-clock witness fails closed."""


Vector4 = tuple[float, float, float, float]
Matrix4 = tuple[Vector4, Vector4, Vector4, Vector4]


def _finite(value: float, label: str) -> float:
    out = float(value)
    if not isfinite(out):
        raise SmoothClockExtensionError(f"{label} must be finite")
    return out


def _vector4(values: Sequence[float], label: str) -> Vector4:
    if len(values) != 4:
        raise SmoothClockExtensionError(f"{label} must have length 4")
    out = tuple(_finite(value, f"{label}[{i}]") for i, value in enumerate(values))
    return out  # type: ignore[return-value]


def _matrix4(values: Sequence[Sequence[float]], label: str) -> Matrix4:
    if len(values) != 4:
        raise SmoothClockExtensionError(f"{label} must be 4x4")
    rows = tuple(_vector4(row, f"{label}[{i}]") for i, row in enumerate(values))
    return rows  # type: ignore[return-value]


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise SmoothClockExtensionError("vector dimensions do not match")
    return sum(float(x) * float(y) for x, y in zip(a, b))


def norm(a: Sequence[float]) -> float:
    return sqrt(dot(a, a))


def matvec(a: Matrix4, x: Sequence[float]) -> Vector4:
    vec = _vector4(x, "vector")
    return tuple(dot(row, vec) for row in a)  # type: ignore[return-value]


def row_times_matrix(row: Sequence[float], a: Matrix4) -> Vector4:
    r = _vector4(row, "row")
    return tuple(sum(r[k] * a[k][j] for k in range(4)) for j in range(4))  # type: ignore[return-value]


def matmul(a: Matrix4, b: Matrix4) -> Matrix4:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4))
        for i in range(4)
    )  # type: ignore[return-value]


def add_vectors(a: Sequence[float], b: Sequence[float]) -> Vector4:
    av = _vector4(a, "a")
    bv = _vector4(b, "b")
    return tuple(x + y for x, y in zip(av, bv))  # type: ignore[return-value]


def det4(a: Matrix4) -> float:
    """4x4 determinant by elimination with partial pivoting."""

    m = [list(row) for row in a]
    sign = 1.0
    determinant = 1.0
    for col in range(4):
        pivot = max(range(col, 4), key=lambda row: abs(m[row][col]))
        if abs(m[pivot][col]) <= 1.0e-15:
            return 0.0
        if pivot != col:
            m[col], m[pivot] = m[pivot], m[col]
            sign *= -1.0
        pivot_value = m[col][col]
        determinant *= pivot_value
        for row in range(col + 1, 4):
            factor = m[row][col] / pivot_value
            for j in range(col + 1, 4):
                m[row][j] -= factor * m[col][j]
    return sign * determinant


def _close(a: float, b: float, atol: float) -> bool:
    scale = 1.0 + max(abs(a), abs(b))
    return abs(a - b) <= atol * scale


def _vector_residual(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != len(b):
        raise SmoothClockExtensionError("vector dimensions do not match")
    return max((abs(float(x) - float(y)) for x, y in zip(a, b)), default=0.0)


def _matrix_residual(a: Matrix4, b: Matrix4) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(4) for j in range(4))


@dataclass(frozen=True)
class RegularClockPatch:
    name: str
    gradient: Sequence[float]
    intercept: float

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise SmoothClockExtensionError("patch name must be a non-empty string")
        gradient = _vector4(self.gradient, f"{self.name}.gradient")
        if norm(gradient) <= 1.0e-14:
            raise SmoothClockExtensionError("clock gradient must be nonzero on every regular patch")
        object.__setattr__(self, "gradient", gradient)
        object.__setattr__(self, "intercept", _finite(self.intercept, f"{self.name}.intercept"))

    def value(self, coordinates: Sequence[float]) -> float:
        return dot(self.gradient, _vector4(coordinates, f"{self.name}.coordinates")) + self.intercept

    @property
    def dt_norm(self) -> float:
        return norm(self.gradient)


@dataclass(frozen=True)
class ClockOverlap:
    source: str
    target: str
    linear: Sequence[Sequence[float]]
    translation: Sequence[float]

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source:
            raise SmoothClockExtensionError("overlap source must be a non-empty string")
        if not isinstance(self.target, str) or not self.target:
            raise SmoothClockExtensionError("overlap target must be a non-empty string")
        if self.source == self.target:
            raise SmoothClockExtensionError("self overlap is not a chart transition")
        linear = _matrix4(self.linear, "overlap.linear")
        if abs(det4(linear)) <= 1.0e-14:
            raise SmoothClockExtensionError("overlap linear map must be invertible")
        object.__setattr__(self, "linear", linear)
        object.__setattr__(self, "translation", _vector4(self.translation, "overlap.translation"))

    def map_point(self, coordinates: Sequence[float]) -> Vector4:
        return add_vectors(matvec(self.linear, coordinates), self.translation)


@dataclass(frozen=True)
class EventEmbedding:
    event: str
    patch: str
    coordinates: Sequence[float]

    def __post_init__(self) -> None:
        if not isinstance(self.event, str) or not self.event:
            raise SmoothClockExtensionError("event name must be a non-empty string")
        if not isinstance(self.patch, str) or not self.patch:
            raise SmoothClockExtensionError("embedding patch must be a non-empty string")
        object.__setattr__(self, "coordinates", _vector4(self.coordinates, "event.coordinates"))


@dataclass(frozen=True)
class RegularClockExtensionCertificate:
    compatible: bool
    smoothness_class: str
    regular_clock: bool
    min_dt_norm: float
    event_count: int
    embedding_count: int
    patch_count: int
    overlap_count: int
    triangle_count: int
    alignment_offset: float
    max_event_alignment_residual: float
    max_overlap_scalar_residual: float
    max_embedding_overlap_residual: float
    max_linear_cocycle_residual: float
    max_translation_cocycle_residual: float
    domain_coverage_witness_supplied: bool
    global_regular_extension: bool
    production_input_status: str = "OPEN_INPUT"


def _connected(names: set[str], overlaps: Sequence[ClockOverlap]) -> bool:
    if len(names) <= 1:
        return True
    adjacency = {name: set() for name in names}
    for overlap in overlaps:
        if overlap.source in names and overlap.target in names:
            adjacency[overlap.source].add(overlap.target)
            adjacency[overlap.target].add(overlap.source)
    root = next(iter(names))
    seen = {root}
    stack = [root]
    while stack:
        current = stack.pop()
        for nxt in adjacency[current] - seen:
            seen.add(nxt)
            stack.append(nxt)
    return seen == names


def certify_regular_smooth_clock_extension(
    patches: Sequence[RegularClockPatch],
    overlaps: Sequence[ClockOverlap],
    event_clock: Mapping[str, float],
    embeddings: Sequence[EventEmbedding],
    *,
    triangles: Iterable[tuple[str, str, str]] = (),
    domain_coverage_witness_supplied: bool = False,
    atol: float = 1.0e-10,
) -> RegularClockExtensionCertificate:
    """Certify a supplied finite affine-chart witness for the 05H -> 05G bridge.

    The discrete 05H scalar is defined only up to one additive constant.  The
    continuum witness is therefore required to agree with every embedded event
    up to one common additive offset.
    """

    atol = _finite(atol, "atol")
    if atol < 0.0:
        raise SmoothClockExtensionError("atol must be non-negative")
    if not patches:
        raise SmoothClockExtensionError("at least one regular clock patch is required")

    patch_map: dict[str, RegularClockPatch] = {}
    for patch in patches:
        if not isinstance(patch, RegularClockPatch):
            raise SmoothClockExtensionError("all patches must be RegularClockPatch instances")
        if patch.name in patch_map:
            raise SmoothClockExtensionError(f"duplicate patch name {patch.name!r}")
        patch_map[patch.name] = patch

    clocks: dict[str, float] = {}
    for event, value in event_clock.items():
        if not isinstance(event, str) or not event:
            raise SmoothClockExtensionError("event-clock keys must be non-empty strings")
        clocks[event] = _finite(value, f"event_clock[{event!r}]")
    if not clocks:
        raise SmoothClockExtensionError("05I requires a non-empty 05H event-clock potential")

    overlap_map: dict[tuple[str, str], ClockOverlap] = {}
    max_overlap_scalar = 0.0
    for overlap in overlaps:
        if not isinstance(overlap, ClockOverlap):
            raise SmoothClockExtensionError("all overlaps must be ClockOverlap instances")
        if overlap.source not in patch_map or overlap.target not in patch_map:
            raise SmoothClockExtensionError("overlap references an unknown patch")
        key = (overlap.source, overlap.target)
        if key in overlap_map:
            raise SmoothClockExtensionError(f"duplicate overlap {key!r}")
        overlap_map[key] = overlap

        source = patch_map[overlap.source]
        target = patch_map[overlap.target]
        pulled_gradient = row_times_matrix(target.gradient, overlap.linear)
        gradient_residual = _vector_residual(pulled_gradient, source.gradient)
        intercept_target = target.intercept + dot(target.gradient, overlap.translation)
        intercept_residual = abs(intercept_target - source.intercept)
        residual = max(gradient_residual, intercept_residual)
        scale = 1.0 + max(norm(source.gradient), norm(target.gradient), abs(source.intercept), abs(target.intercept))
        if residual > atol * scale:
            raise SmoothClockExtensionError(
                f"clock scalar mismatch on overlap {key!r}; residual={residual:.17g}"
            )
        max_overlap_scalar = max(max_overlap_scalar, residual)

    if not _connected(set(patch_map), tuple(overlaps)):
        raise SmoothClockExtensionError("declared clock-atlas overlap graph must be connected")

    embedding_map: dict[str, dict[str, EventEmbedding]] = {event: {} for event in clocks}
    alignment_residuals: list[float] = []
    raw_offsets: list[float] = []
    for embedding in embeddings:
        if not isinstance(embedding, EventEmbedding):
            raise SmoothClockExtensionError("all embeddings must be EventEmbedding instances")
        if embedding.event not in clocks:
            raise SmoothClockExtensionError(f"embedding references unknown event {embedding.event!r}")
        if embedding.patch not in patch_map:
            raise SmoothClockExtensionError(f"embedding references unknown patch {embedding.patch!r}")
        if embedding.patch in embedding_map[embedding.event]:
            raise SmoothClockExtensionError(
                f"duplicate embedding for event {embedding.event!r} in patch {embedding.patch!r}"
            )
        embedding_map[embedding.event][embedding.patch] = embedding
        witness_value = patch_map[embedding.patch].value(embedding.coordinates)
        raw_offsets.append(witness_value - clocks[embedding.event])

    missing = sorted(event for event, by_patch in embedding_map.items() if not by_patch)
    if missing:
        raise SmoothClockExtensionError(f"every 05H event must be embedded; missing={missing!r}")
    if not raw_offsets:
        raise SmoothClockExtensionError("at least one event embedding is required")

    alignment_offset = raw_offsets[0]
    max_event_alignment = 0.0
    for offset in raw_offsets:
        residual = abs(offset - alignment_offset)
        max_event_alignment = max(max_event_alignment, residual)
        if not _close(offset, alignment_offset, atol):
            raise SmoothClockExtensionError(
                "embedded continuum clock does not extend the 05H scalar up to one global additive constant"
            )
        alignment_residuals.append(residual)

    max_embedding_overlap = 0.0
    for (source_name, target_name), overlap in overlap_map.items():
        for event, by_patch in embedding_map.items():
            if source_name not in by_patch or target_name not in by_patch:
                continue
            mapped = overlap.map_point(by_patch[source_name].coordinates)
            target_coords = by_patch[target_name].coordinates
            residual = _vector_residual(mapped, target_coords)
            scale = 1.0 + max(norm(mapped), norm(target_coords))
            if residual > atol * scale:
                raise SmoothClockExtensionError(
                    f"event {event!r} has incompatible overlap coordinates; residual={residual:.17g}"
                )
            max_embedding_overlap = max(max_embedding_overlap, residual)

    max_linear_cocycle = 0.0
    max_translation_cocycle = 0.0
    triangle_count = 0
    for p, q, r in triangles:
        triangle_count += 1
        try:
            pq = overlap_map[(p, q)]
            qr = overlap_map[(q, r)]
            pr = overlap_map[(p, r)]
        except KeyError as exc:
            raise SmoothClockExtensionError(
                f"triangle {(p, q, r)!r} requires direct p->q, q->r and p->r overlaps"
            ) from exc

        composed_linear = matmul(qr.linear, pq.linear)
        linear_residual = _matrix_residual(pr.linear, composed_linear)
        if linear_residual > atol * (1.0 + max(abs(det4(pr.linear)), abs(det4(composed_linear)))):
            raise SmoothClockExtensionError(
                f"linear chart cocycle failed on triangle {(p, q, r)!r}"
            )

        composed_translation = add_vectors(matvec(qr.linear, pq.translation), qr.translation)
        translation_residual = _vector_residual(pr.translation, composed_translation)
        if translation_residual > atol * (1.0 + max(norm(pr.translation), norm(composed_translation))):
            raise SmoothClockExtensionError(
                f"translation chart cocycle failed on triangle {(p, q, r)!r}"
            )

        max_linear_cocycle = max(max_linear_cocycle, linear_residual)
        max_translation_cocycle = max(max_translation_cocycle, translation_residual)

    min_dt_norm = min(patch.dt_norm for patch in patch_map.values())
    coverage = bool(domain_coverage_witness_supplied)
    return RegularClockExtensionCertificate(
        compatible=True,
        smoothness_class="C_INFINITY_AFFINE_CHART_WITNESS",
        regular_clock=True,
        min_dt_norm=min_dt_norm,
        event_count=len(clocks),
        embedding_count=len(embeddings),
        patch_count=len(patch_map),
        overlap_count=len(overlap_map),
        triangle_count=triangle_count,
        alignment_offset=alignment_offset,
        max_event_alignment_residual=max_event_alignment,
        max_overlap_scalar_residual=max_overlap_scalar,
        max_embedding_overlap_residual=max_embedding_overlap,
        max_linear_cocycle_residual=max_linear_cocycle,
        max_translation_cocycle_residual=max_translation_cocycle,
        domain_coverage_witness_supplied=coverage,
        global_regular_extension=coverage,
    )
