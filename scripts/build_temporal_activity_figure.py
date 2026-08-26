from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'monograph' / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

A = np.linspace(-3.0, 3.0, 401)
M = 1.0
activity = 2.0 * M * np.cosh(A / 2.0)
current = 2.0 * M * np.sinh(A / 2.0)

fig, ax = plt.subplots(figsize=(7.2, 4.4))
ax.plot(A, activity, label=r'$\mathfrak{a}=2M\cosh(A/2)$')
ax.plot(A, current, label=r'$\mathfrak{j}=2M\sinh(A/2)$')
ax.axhline(0.0, linewidth=0.6)
ax.axvline(0.0, linewidth=0.6)
ax.set_xlabel(r'antisymmetric edge drive $A$')
ax.set_ylabel('relative transition scale')
ax.set_title('Temporal activity and directed current from one kinetic pair')
ax.legend()
fig.tight_layout()
fig.savefig(FIG / 'temporal_activity_decomposition.png', dpi=180, bbox_inches='tight')
plt.close(fig)

# Compact repository SVG generated from the same sampled arrays.
W, H = 760, 460
margin = 54
xmin, xmax = float(A.min()), float(A.max())
ymin = float(min(current.min(), activity.min()))
ymax = float(max(current.max(), activity.max()))
def sx(x): return margin + (x-xmin)/(xmax-xmin)*(W-2*margin)
def sy(y): return H-margin - (y-ymin)/(ymax-ymin)*(H-2*margin)
def pts(xs, ys): return ' '.join(f'{sx(float(x)):.2f},{sy(float(y)):.2f}' for x,y in zip(xs,ys))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" fill="white"/>
<line x1="{sx(0):.2f}" y1="{margin}" x2="{sx(0):.2f}" y2="{H-margin}" stroke="#777" stroke-width="1"/>
<line x1="{margin}" y1="{sy(0):.2f}" x2="{W-margin}" y2="{sy(0):.2f}" stroke="#777" stroke-width="1"/>
<polyline points="{pts(A,activity)}" fill="none" stroke="#1f77b4" stroke-width="3"/>
<polyline points="{pts(A,current)}" fill="none" stroke="#ff7f0e" stroke-width="3"/>
<text x="{W/2}" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">Temporal activity and directed current</text>
<text x="{W/2}" y="{H-10}" text-anchor="middle" font-family="sans-serif" font-size="14">antisymmetric edge drive A</text>
<text x="{W-250}" y="58" font-family="sans-serif" font-size="13" fill="#1f77b4">activity = 2M cosh(A/2)</text>
<text x="{W-250}" y="78" font-family="sans-serif" font-size="13" fill="#ff7f0e">current = 2M sinh(A/2)</text>
</svg>'''
(FIG / 'temporal_activity_decomposition.svg').write_text(svg, encoding='utf-8')
