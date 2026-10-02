"""Build Figure 2: the settlement-induced observability boundary and where trajectories sit inside it.

(A) All 100 ordered price states, coloured by welfare W(min(p_A, p_B)).  Each
    welfare class is an L-shaped set of states; the m = 6.0 class used in the
    experiments is outlined.  Values come from the exact settlement arithmetic
    in `observability_certificate.py`.
(B) The three states of the m = 6.0 class have identical welfare but different
    seller-profit vectors: an equal split (tie, T3b) or capture by one seller
    (T3a).
(C) Assessment-window composition (rounds 10--29) of the asymmetric cells in
    the original run and the replication: display policy moves trajectories
    between ties and capture inside the m = 6.0 class; only the small share of
    6.5 ties changes welfare.  From `analysis/structure-dynamics-20261002.json`.

    python paper-materials/aamas2027/tools/build_fig2_observability.py
"""
from __future__ import annotations

import json
from fractions import Fraction

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Rectangle

import figstyle as fs
import observability_certificate as oc

DYNAMICS = fs.MATERIALS / "analysis" / "structure-dynamics-20261002.json"


def grid_panel(ax, cax) -> None:
    grid = oc.GRID
    n = len(grid)
    welfare = np.array([[float(oc.settle(pa, pb)["welfare"]) for pa in grid] for pb in grid])
    levels = sorted({float(oc.settle(p, p)["welfare"]) for p in grid})
    # Ten classes on ten steps of the blue ramp: higher welfare is darker.
    colors = [fs.BLUE_RAMP[i] for i in (0, 1, 2, 3, 4, 5, 6, 8, 10, 12)]
    edges = [levels[0] - 1] + [(a + b) / 2 for a, b in zip(levels, levels[1:])] + [levels[-1] + 1]
    cmap, norm = ListedColormap(colors), BoundaryNorm(edges, len(colors))
    ax.imshow(welfare, origin="lower", cmap=cmap, norm=norm, extent=(-0.5, n - 0.5, -0.5, n - 0.5))
    for k in range(n + 1):
        ax.axhline(k - 0.5, color="white", linewidth=0.4)
        ax.axvline(k - 0.5, color="white", linewidth=0.4)
    for i, p in enumerate(grid):
        w = float(oc.settle(p, p)["welfare"])
        ax.text(i, i, f"{w:.0f}", ha="center", va="center", fontsize=5.4,
                color="white" if w > 380 else fs.INK)
    i6, i65 = grid.index(Fraction(6)), grid.index(Fraction(13, 2))
    for (x, y) in ((i6, i6), (i65, i6), (i6, i65)):
        ax.add_patch(Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, edgecolor=fs.RED, linewidth=1.1, zorder=5))
    ticks = list(range(0, n, 2))
    ax.set_xticks(ticks, [f"{float(grid[t]):.1f}" for t in ticks])
    ax.set_yticks(ticks, [f"{float(grid[t]):.1f}" for t in ticks])
    ax.set_xlabel("seller A price")
    ax.set_ylabel("seller B price")
    for side in ("top", "right"):
        ax.spines[side].set_visible(True)
    cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=cax)
    cb.set_ticks(levels[::3] if len(levels) > 4 else levels)
    cb.set_ticklabels([f"{v:.0f}" for v in (levels[::3] if len(levels) > 4 else levels)])
    cb.outline.set_linewidth(0.5)
    cb.ax.tick_params(labelsize=fs.SMALL_PT, length=1.5)
    cb.set_label("welfare W", fontsize=fs.SMALL_PT, labelpad=1)


def class_panel(ax) -> None:
    states = [(Fraction(6), Fraction(6), "(6.0, 6.0)  tie, T3b"),
              (Fraction(6), Fraction(13, 2), "(6.0, 6.5)  A captures, T3a"),
              (Fraction(13, 2), Fraction(6), "(6.5, 6.0)  B captures, T3a")]
    for row, (pa, pb, label) in enumerate(states):
        y = len(states) - 1 - row
        s = oc.settle(pa, pb)
        a, b = float(s["seller_a_profit"]), float(s["seller_b_profit"])
        ax.barh(y, a, height=0.56, color=fs.BLUE_RAMP[9], edgecolor="white", linewidth=0.8)
        ax.barh(y, b, left=a, height=0.56, color=fs.BLUE_RAMP[3], edgecolor="white", linewidth=0.8)
        for x0, val, name, col in ((0, a, "A", "white"), (a, b, "B", fs.INK)):
            if val > 0:
                ax.text(x0 + val / 2, y, f"{name} {val:.0f}", ha="center", va="center", fontsize=fs.SMALL_PT, color=col)
        ax.text(-6, y + 0.43, label, ha="left", va="bottom", fontsize=fs.SMALL_PT, color=fs.INK)
        ax.text(229, y, f"W = {float(s['welfare']):.1f}", ha="left", va="center", fontsize=fs.SMALL_PT,
                color=fs.MUTED)
    ax.set_xlim(-6, 300)
    ax.set_ylim(-0.5, len(states) - 0.05)
    ax.set_yticks([])
    ax.set_xticks([0, 111.1, 222.2], ["0", "111", "222"])
    ax.set_xlabel("industry profit split between sellers")
    ax.spines["left"].set_visible(False)


def composition_panel(ax) -> None:
    dyn = json.loads(DYNAMICS.read_text(encoding="utf-8"))
    segs = (("tie_6.0", fs.BLUE), ("capture_m6.0", fs.ORANGE), ("tie_6.5", fs.VIOLET))
    rows, ys, y = [], [], 0.0
    for g, run in enumerate(("original", "replication")):
        if g:
            y -= 0.9
        for cell in ("LH", "HL"):
            for arm, short in (("natural", "natural"), ("hide_rival", "hide-rival")):
                rows.append((run, f"{cell} {short}", dyn["runs"][run]["assessment_composition"][f"{cell}-{arm}"]))
                ys.append(y)
                y -= 1.0
    for yy, (run, label, comp) in zip(ys, rows):
        left = 0.0
        for key, color in segs:
            ax.barh(yy, comp[key], left=left, height=0.74, color=color, edgecolor="white", linewidth=0.6)
            left += comp[key]
        if comp["tie_6.5"] > 0:
            ax.text(1.02, yy, f"{100 * comp['tie_6.5']:.1f}%", ha="left", va="center", fontsize=fs.SMALL_PT,
                    color=fs.VIOLET)
    # Direct labels on the first natural and first hide-rival bars.
    first_nat, first_hide = rows[0][2], rows[1][2]
    ax.text(first_nat["tie_6.0"] / 2, ys[0], "tie at 6.0", ha="center", va="center", fontsize=fs.SMALL_PT,
            color="white")
    ax.text(0.5, ys[1], "capture, m = 6.0", ha="center", va="center", fontsize=fs.SMALL_PT, color="white")
    ax.text(1.02, ys[0] + 0.62, "6.5 tie", ha="left", va="center", fontsize=fs.SMALL_PT, color=fs.VIOLET)
    ax.set_yticks(ys, [r[1] for r in rows])
    ax.tick_params(axis="y", length=0, labelsize=fs.SMALL_PT, labelcolor=fs.INK)
    for g, label in ((0, "Original run"), (4, "Replication")):
        ax.text(-0.02, ys[g] + 0.72, label, transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=fs.SMALL_PT, color=fs.MUTED, fontweight="bold")
    ax.set_ylim(ys[-1] - 0.6, ys[0] + 1.1)
    ax.set_xlim(0, 1.25)
    ax.set_xticks([0, 0.5, 1.0], ["0", "0.5", "1"])
    ax.set_xlabel("share of assessment rounds")
    ax.spines["left"].set_visible(False)


def main() -> None:
    fs.apply()
    fig = plt.figure(figsize=(fs.DOUBLE_COLUMN_IN, 2.30))
    ax_a = fig.add_axes([0.062, 0.16, 0.235, 0.74])
    cax = fig.add_axes([0.302, 0.16, 0.010, 0.74])
    ax_b = fig.add_axes([0.385, 0.16, 0.235, 0.74])
    ax_c = fig.add_axes([0.785, 0.16, 0.185, 0.74])
    grid_panel(ax_a, cax)
    class_panel(ax_b)
    composition_panel(ax_c)
    for ax, letter, x in ((ax_a, "A", -0.20), (ax_b, "B", -0.04), (ax_c, "C", -0.66)):
        fs.panel_label(ax, letter, x=x, y=1.03)
        ax.set_title({"A": "100 states, 10 welfare classes", "B": "One welfare class, three allocations",
                      "C": "Where trajectories sit (m = 6.0)"}[letter], loc="left", fontsize=fs.TEXT_PT, pad=4,
                     x=0.0 if letter != "C" else -0.62)
    fs.save(fig, "fig2-observability-boundary", run_alignment=False)


if __name__ == "__main__":
    main()
