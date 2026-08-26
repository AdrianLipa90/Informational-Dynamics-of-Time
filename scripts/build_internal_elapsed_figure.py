from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / 'monograph' / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

lam = np.linspace(0.0, 1.0, 240)
a_slow = 0.8 + 0.15 * np.sin(2*np.pi*lam)**2
a_fast = 2.0 + 0.45 * np.sin(2*np.pi*lam + 0.3)**2

dlam = np.diff(lam)
tau_slow = np.concatenate(([0.0], np.cumsum(0.5*(a_slow[:-1]+a_slow[1:])*dlam)))
tau_fast = np.concatenate(([0.0], np.cumsum(0.5*(a_fast[:-1]+a_fast[1:])*dlam)))

fig, ax = plt.subplots(figsize=(7.2, 4.5))
ax.plot(lam, tau_slow, label='lower internal activity')
ax.plot(lam, tau_fast, label='higher internal activity')
ax.plot([0,1],[0,1], linestyle='--', linewidth=0.9, label='ordering parameter reference')
ax.set_xlabel(r'ordering parameter $\lambda$')
ax.set_ylabel(r'internal elapsed activity $\tau_{\rm int}$')
ax.set_title('Same ordering interval, different internal elapsed activity')
ax.legend()
fig.tight_layout()
fig.savefig(FIG / 'internal_elapsed_activity.png', dpi=180, bbox_inches='tight')
plt.close(fig)

W,H=760,460; margin=56
xmin,xmax=0.0,1.0; ymin=0.0; ymax=float(max(tau_fast.max(),1.0))*1.04
def sx(x): return margin+(x-xmin)/(xmax-xmin)*(W-2*margin)
def sy(y): return H-margin-(y-ymin)/(ymax-ymin)*(H-2*margin)
def pts(xs,ys): return ' '.join(f'{sx(float(x)):.2f},{sy(float(y)):.2f}' for x,y in zip(xs,ys))
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="100%" height="100%" fill="white"/>
<polyline points="{pts(lam,tau_slow)}" fill="none" stroke="#1f77b4" stroke-width="3"/>
<polyline points="{pts(lam,tau_fast)}" fill="none" stroke="#ff7f0e" stroke-width="3"/>
<polyline points="{pts([0,1],[0,1])}" fill="none" stroke="#777" stroke-width="1.5" stroke-dasharray="6 5"/>
<text x="{W/2}" y="28" text-anchor="middle" font-family="sans-serif" font-size="18">Internal elapsed activity</text>
<text x="{W/2}" y="{H-12}" text-anchor="middle" font-family="sans-serif" font-size="14">ordering parameter lambda</text>
<text x="{W-250}" y="60" font-family="sans-serif" font-size="13" fill="#1f77b4">lower activity</text>
<text x="{W-250}" y="80" font-family="sans-serif" font-size="13" fill="#ff7f0e">higher activity</text>
</svg>'''
(FIG/'internal_elapsed_activity.svg').write_text(svg, encoding='utf-8')
