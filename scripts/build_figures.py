from __future__ import annotations

from pathlib import Path
import json
import math
import base64
import io
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from src.idt.kahler_time import (
    info_potential,
    phase_hamiltonian,
    kahler_flow,
    integrate_flow,
    chirality_from_holonomy,
    box_count_dimension,
    event_measure,
)

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'monograph' / 'figures'
RAW = ROOT / 'evidence' / 'raw' / 'visuals_v050'
REV = ROOT / 'evidence' / 'reviewed'
FIG.mkdir(parents=True, exist_ok=True)
RAW.mkdir(parents=True, exist_ok=True)
REV.mkdir(parents=True, exist_ok=True)


def write_svg_preview(png_path: Path, svg_path: Path, *, max_width: int = 900, jpeg_quality: int = 72) -> None:
    """Create a compact repository SVG preview from a generated raster figure."""
    with Image.open(png_path) as im:
        im = im.convert('RGB')
        if im.width > max_width:
            h = int(round(im.height * (max_width / im.width)))
            im = im.resize((max_width, h), Image.Resampling.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, format='JPEG', quality=jpeg_quality, optimize=True)
        payload = base64.b64encode(buf.getvalue()).decode('ascii')
        svg = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{im.width}" height="{im.height}" '
            f'viewBox="0 0 {im.width} {im.height}">'
            f'<image width="{im.width}" height="{im.height}" href="data:image/jpeg;base64,{payload}"/>'
            '</svg>\n'
        )
        svg_path.write_text(svg, encoding='utf-8')


def write_nd_slice_contour_svg(path: Path, u: np.ndarray, v: np.ndarray, fields: list[np.ndarray], params: list[tuple[float, float]], levels: np.ndarray) -> None:
    """Write a compact contour preview derived from the same sampled fields as Figure 4.1."""
    panel_w, panel_h, gap = 220, 220, 35
    margin_x, margin_y = 30, 48
    width = margin_x * 2 + panel_w * 2 + gap
    height = margin_y * 2 + panel_h * 2 + gap
    chunks = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="50%" y="22" text-anchor="middle" font-family="sans-serif" font-size="15">Figure 4.1 - tensor-scalar slices</text>',
    ]
    compact_levels = np.asarray([levels[1], levels[-2]]) if len(levels) >= 4 else levels
    for idx, ((a, b), F) in enumerate(zip(params, fields)):
        col, row = idx % 2, idx // 2
        x0 = margin_x + col * (panel_w + gap)
        y0 = margin_y + row * (panel_h + gap)
        chunks.append(f'<rect x="{x0}" y="{y0}" width="{panel_w}" height="{panel_h}" fill="#fafafa" stroke="#222"/>')
        chunks.append(f'<text x="{x0 + panel_w/2:.1f}" y="{y0 - 8}" text-anchor="middle" font-family="sans-serif" font-size="10">Theta=({a:.1f},{b:.1f})</text>')
        tmpfig, tmpax = plt.subplots()
        cs = tmpax.contour(u, v, F, levels=compact_levels)
        for li, segs in enumerate(cs.allsegs):
            for seg in segs:
                if len(seg) < 2:
                    continue
                take = np.linspace(0, len(seg)-1, min(24, len(seg))).astype(int)
                pts = []
                for xv, yv in seg[take]:
                    sx = x0 + (xv - u.min()) / (u.max() - u.min()) * panel_w
                    sy = y0 + panel_h - (yv - v.min()) / (v.max() - v.min()) * panel_h
                    pts.append(f'{sx:.1f},{sy:.1f}')
                chunks.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#2b6f9f" stroke-opacity="{0.55 + 0.3*li:.2f}" stroke-width="1.6"/>')
        plt.close(tmpfig)
        k = np.unravel_index(np.argmin(F), F.shape)
        mx = x0 + (u[k[1]] - u.min()) / (u.max() - u.min()) * panel_w
        my = y0 + panel_h - (v[k[0]] - v.min()) / (v.max() - v.min()) * panel_h
        chunks.append(f'<path d="M {mx-4:.1f} {my-4:.1f} L {mx+4:.1f} {my+4:.1f} M {mx+4:.1f} {my-4:.1f} L {mx-4:.1f} {my+4:.1f}" stroke="#b11" stroke-width="2"/>')
    chunks.append('</svg>')
    path.write_text('\n'.join(chunks) + '\n', encoding='utf-8')

# Figure 1: 2D vector field + trajectories
xs = np.linspace(-2.0, 2.0, 17)
ys = np.linspace(-2.0, 2.0, 17)
X, Y = np.meshgrid(xs, ys)
Z = np.stack([X, Y], axis=-1)
V = kahler_flow(Z)
U = V[..., 0]
W = V[..., 1]
I = info_potential(Z)

fig, ax = plt.subplots(figsize=(7, 6))
ax.contour(X, Y, I, levels=12)
ax.quiver(X, Y, U, W, angles='xy', scale_units='xy', scale=0.12, width=0.002)
for z0 in ([1.7, 0.3], [1.4, -1.2], [-1.2, 1.5], [-1.7, -0.8]):
    path = integrate_flow(z0, n_steps=300, dt=0.02)
    ax.plot(path[:, 0], path[:, 1], linewidth=1.5)
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_title('2D Kähler time flow and informational descent')
ax.set_aspect('equal', adjustable='box')
fig.tight_layout()
fig.savefig(FIG / 'kahler_flow_2d.png', dpi=170, bbox_inches='tight')
fig.savefig(RAW / 'kahler_flow_2d.png', dpi=170, bbox_inches='tight')
write_svg_preview(FIG / 'kahler_flow_2d.png', FIG / 'kahler_flow_2d.svg')
plt.close(fig)

# Figure 2: 3D temporal ribbon/helix with information as height
path = integrate_flow([1.7, 0.3], n_steps=1400, dt=0.025)
It = info_potential(path)
t = np.arange(len(path)) * 0.025
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(path[:, 0], path[:, 1], It, linewidth=1.4)
sel = np.linspace(0, len(path)-1, 80).astype(int)
ax.scatter(path[sel, 0], path[sel, 1], It[sel], s=8)
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_zlabel(r'$\mathcal{I}$')
ax.set_title('3D slice: trajectory of time on Kähler informational landscape')
fig.tight_layout()
fig.savefig(FIG / 'temporal_ribbon_3d.png', dpi=200)
fig.savefig(RAW / 'temporal_ribbon_3d.png', dpi=200)
write_svg_preview(FIG / 'temporal_ribbon_3d.png', FIG / 'temporal_ribbon_3d.svg')
plt.close(fig)

# Figure 3: 2D slices through a 4D tensor-scalar surrogate
u = np.linspace(-2.0, 2.0, 260)
v = np.linspace(-2.0, 2.0, 260)
U2, V2 = np.meshgrid(u, v)
params = [(-0.8, -0.3), (-0.8, 0.6), (0.9, -0.3), (0.9, 0.6)]
fields = []
for a, b in params:
    fields.append(
        0.5 * (U2**2 + V2**2)
        + 0.08 * (U2**4 + V2**4)
        + 0.25 * a * U2 * V2
        + 0.18 * b * (U2**3 - 3 * U2 * V2**2)
    )
common_min = min(float(F.min()) for F in fields)
common_max = max(float(F.max()) for F in fields)
levels = np.linspace(common_min, common_max, 15)

fig, axes = plt.subplots(2, 2, figsize=(9.2, 8.4), constrained_layout=True)
last = None
for ax, (a, b), surrogate in zip(axes.flat, params, fields):
    last = ax.imshow(surrogate, extent=[u.min(), u.max(), v.min(), v.max()], origin='lower', aspect='equal', vmin=common_min, vmax=common_max)
    ax.contour(U2, V2, surrogate, levels=levels[::2], linewidths=0.45, alpha=0.65)
    k = np.unravel_index(np.argmin(surrogate), surrogate.shape)
    ax.scatter([U2[k]], [V2[k]], marker='x', s=42, linewidths=1.6)
    ax.axhline(0.0, linewidth=0.45, alpha=0.5)
    ax.axvline(0.0, linewidth=0.45, alpha=0.5)
    ax.set_title(rf'$(\Theta_1,\Theta_2)=({a:.1f},{b:.1f})$')
    ax.set_xlabel(r'$\phi_1$')
    ax.set_ylabel(r'$\phi_2$')
    ax.set_aspect('equal', adjustable='box')

cbar = fig.colorbar(last, ax=axes, location='right', shrink=0.92, pad=0.025)
cbar.set_label(r'surrogate informational level $\mathcal{I}_{\rm slice}$')
fig.suptitle('Four 2D slices through one higher-dimensional tensor–scalar field', fontsize=16)
fig.savefig(FIG / 'nd_slices.png', dpi=220, bbox_inches='tight')
fig.savefig(RAW / 'nd_slices.png', dpi=220, bbox_inches='tight')
write_nd_slice_contour_svg(FIG / 'nd_slices.svg', u, v, fields, params, levels[::2])
plt.close(fig)

# Figure 4: event measure from information slope and thresholding
path2 = integrate_flow([1.4, -1.2], n_steps=1200, dt=0.03)
I2 = info_potential(path2)
q = event_measure(I2, threshold=2e-5)
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(np.arange(len(I2)), I2, linewidth=1.2, label=r'$\mathcal{I}_n$')
ax2 = ax.twinx()
ax2.plot(np.arange(1, len(I2)), q, linewidth=1.0, label=r'$\mathcal{K}_n$')
ax.set_xlabel('step $n$')
ax.set_ylabel(r'$\mathcal{I}_n$')
ax2.set_ylabel(r'$\mathcal{K}_n$')
ax.set_title('Discrete event measure extracted from informational evolution')
fig.tight_layout()
fig.savefig(FIG / 'event_measure.png', dpi=200)
fig.savefig(RAW / 'event_measure.png', dpi=200)
write_svg_preview(FIG / 'event_measure.png', FIG / 'event_measure.svg')
plt.close(fig)

# Small evidence summary
closed = np.vstack([path, path[0]])
summary = {
    'chirality_main_path': chirality_from_holonomy(closed),
    'box_dimension_main_path': box_count_dimension(path[::3], [0.5, 0.25, 0.125, 0.0625]),
    'mean_information_drop_per_step': float(np.mean(np.diff(It))),
    'event_measure_nonzero_count': int(np.count_nonzero(q)),
}
(REV / 'VISUAL_SUMMARY_V0_5.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
