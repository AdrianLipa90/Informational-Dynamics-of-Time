from __future__ import annotations

from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from src.idt.kahler_time import (
    info_potential,
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

# Figure 3.1: 2D Kähler flow
xs = np.linspace(-2.0, 2.0, 17)
ys = np.linspace(-2.0, 2.0, 17)
X, Y = np.meshgrid(xs, ys)
Z = np.stack([X, Y], axis=-1)
V = kahler_flow(Z)
U, W = V[..., 0], V[..., 1]
I = info_potential(Z)
fig, ax = plt.subplots(figsize=(7, 6))
ax.contour(X, Y, I, levels=12)
ax.quiver(X, Y, U, W, angles='xy', scale_units='xy', scale=0.12, width=0.002)
for z0 in ([1.7, 0.3], [1.4, -1.2], [-1.2, 1.5], [-1.7, -0.8]):
    path = integrate_flow(z0, n_steps=300, dt=0.02)
    ax.plot(path[:, 0], path[:, 1], linewidth=1.5)
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.2, 2.2)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$')
ax.set_title('2D Kähler time flow and informational descent')
ax.set_aspect('equal', adjustable='box')
fig.tight_layout()
fig.savefig(FIG / 'kahler_flow_2d.png', dpi=170, bbox_inches='tight')
fig.savefig(RAW / 'kahler_flow_2d.png', dpi=170, bbox_inches='tight')
fig.savefig(FIG / 'kahler_flow_2d.svg', format='svg', bbox_inches='tight')
plt.close(fig)

# Figure 5.1: 3D trajectory over informational level
path = integrate_flow([1.7, 0.3], n_steps=1400, dt=0.025)
It = info_potential(path)
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')
ax.plot(path[:, 0], path[:, 1], It, linewidth=1.4)
sel = np.linspace(0, len(path)-1, 80).astype(int)
ax.scatter(path[sel, 0], path[sel, 1], It[sel], s=8)
ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); ax.set_zlabel(r'$\mathcal{I}$')
ax.set_title('3D slice: trajectory of time on Kähler informational landscape')
fig.tight_layout()
fig.savefig(FIG / 'temporal_ribbon_3d.png', dpi=200)
fig.savefig(RAW / 'temporal_ribbon_3d.png', dpi=200)
fig.savefig(FIG / 'temporal_ribbon_3d.svg', format='svg', bbox_inches='tight')
plt.close(fig)

# Figure 4.1: four common-scale 2D slices through a higher-dimensional surrogate
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
    last = ax.contourf(U2, V2, surrogate, levels=levels)
    ax.contour(U2, V2, surrogate, levels=levels[::3], linewidths=0.45, alpha=0.65)
    k = np.unravel_index(np.argmin(surrogate), surrogate.shape)
    ax.scatter([U2[k]], [V2[k]], marker='x', s=42, linewidths=1.6)
    ax.axhline(0.0, linewidth=0.45, alpha=0.5)
    ax.axvline(0.0, linewidth=0.45, alpha=0.5)
    ax.set_title(rf'$(\Theta_1,\Theta_2)=({a:.1f},{b:.1f})$')
    ax.set_xlabel(r'$\phi_1$'); ax.set_ylabel(r'$\phi_2$')
    ax.set_aspect('equal', adjustable='box')
cbar = fig.colorbar(last, ax=axes, location='right', shrink=0.92, pad=0.025)
cbar.set_label(r'surrogate informational level $\mathcal{I}_{\rm slice}$')
fig.suptitle('Four 2D slices through one higher-dimensional tensor–scalar field', fontsize=16)
fig.savefig(FIG / 'nd_slices.png', dpi=220, bbox_inches='tight')
fig.savefig(RAW / 'nd_slices.png', dpi=220, bbox_inches='tight')
fig.savefig(FIG / 'nd_slices.svg', format='svg', bbox_inches='tight')
plt.close(fig)

# Figure 5.2: discrete event measure
path2 = integrate_flow([1.4, -1.2], n_steps=1200, dt=0.03)
I2 = info_potential(path2)
q = event_measure(I2, threshold=2e-5)
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(np.arange(len(I2)), I2, linewidth=1.2, label=r'$\mathcal{I}_n$')
ax2 = ax.twinx()
ax2.plot(np.arange(1, len(I2)), q, linewidth=1.0, label=r'$\mathcal{K}_n$')
ax.set_xlabel('step $n$'); ax.set_ylabel(r'$\mathcal{I}_n$'); ax2.set_ylabel(r'$\mathcal{K}_n$')
ax.set_title('Discrete event measure extracted from informational evolution')
fig.tight_layout()
fig.savefig(FIG / 'event_measure.png', dpi=200)
fig.savefig(RAW / 'event_measure.png', dpi=200)
fig.savefig(FIG / 'event_measure.svg', format='svg', bbox_inches='tight')
plt.close(fig)

closed = np.vstack([path, path[0]])
summary = {
    'chirality_main_path': chirality_from_holonomy(closed),
    'box_dimension_main_path': box_count_dimension(path[::3], [0.5, 0.25, 0.125, 0.0625]),
    'mean_information_drop_per_step': float(np.mean(np.diff(It))),
    'event_measure_nonzero_count': int(np.count_nonzero(q)),
}
(REV / 'VISUAL_SUMMARY_V0_5.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
