"""Build Figure 1: study framework and evidence map.

A display intervention changes what each language-model seller sees; the
joint trajectory is then read through three monitor surfaces (T1 market
outcome, T2 joint structure, T3 allocation) before a gated strategic claim
(T4).  A dashed outline marks the differences that a T1-only monitor cannot
see, and the bottom row maps each layer to the evidence that supports it.
Drawn with matplotlib so that the figure is reproducible from source.

    python paper-materials/aamas2027/tools/build_fig1_framework.py
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

import figstyle as fs

W, H = 7.0, 1.96


def box(ax, x, y, w, h, title, lines, accent=None, fill=fs.PANEL, body_offset=0.26):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05",
                                linewidth=0.6, edgecolor=fs.FAINT, facecolor=fill, zorder=1))
    if accent:
        ax.add_patch(Rectangle((x, y), 0.055, h, facecolor=accent, edgecolor="none", zorder=2))
    ax.text(x + 0.11, y + h - 0.07, title, fontsize=fs.TEXT_PT, fontweight="bold", color=fs.INK,
            ha="left", va="top", zorder=3)
    ax.text(x + 0.11, y + h - body_offset, "\n".join(lines), fontsize=fs.SMALL_PT, color=fs.INK, ha="left", va="top",
            linespacing=1.28, zorder=3)


def arrow(ax, x0, y0, x1, y1, color=fs.MUTED):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7, color=color,
                                 linewidth=0.8, shrinkA=0, shrinkB=0, zorder=4))


def tag(ax, x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.04", linewidth=0.6,
                                edgecolor=color, facecolor="white", zorder=1))
    ax.text(x + 0.07, y + h / 2, text, fontsize=fs.SMALL_PT, color=fs.INK, ha="left", va="center",
            linespacing=1.2, zorder=3)


def main() -> None:
    fs.apply()
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    top, h, bw = 0.66, 1.27, 1.17
    xs = [0.02, 1.33, 2.64]
    box(ax, xs[0], top, bw, h, "Display policy",
        ["What each seller sees:", "natural: own + rival", "hide-rival: rival = null",
         "(four-arm study also", " hides own or both)", "No message channel"])
    box(ax, xs[1], top, bw, h, "Two LLM sellers",
        ["Simultaneous prices", "on {2.0, 2.5, ..., 6.5}", "No sales, profit or", "welfare is shown",
         "Lowest price serves", "demand; ties split"])
    box(ax, xs[2], top, bw, h, "Joint trajectory",
        ["State (p_A, p_B)", "Round 0: programmed", "  or model-chosen", "Rounds 1-29: model",
         "Assessed: 10-29", "Block: arms matched"])
    mid = top + h / 2
    arrow(ax, xs[0] + bw, mid, xs[1], mid)
    arrow(ax, xs[1] + bw, mid, xs[2], mid)

    sx, sw, sh, gap = 4.04, 1.38, 0.375, 0.07
    ys = [top + h - sh, top + h - 2 * sh - gap, top + h - 3 * sh - 2 * gap]
    box(ax, sx, ys[0], sw, sh, "T1  Market outcome", ["m, W, CS, industry profit"], accent=fs.BLUE, body_offset=0.225)
    box(ax, sx, ys[1], sw, sh, "T2  Joint structure", ["ties, transitions, persistence"], accent=fs.AQUA, body_offset=0.225)
    box(ax, sx, ys[2], sw, sh, "T3  Allocation", ["T3a capture | T3b division"], accent=fs.ORANGE, body_offset=0.225)
    for y in ys:
        arrow(ax, xs[2] + bw, mid, sx, y + sh / 2)

    # Differences inside a welfare class are visible to T2/T3 but not to T1.
    ax.add_patch(FancyBboxPatch((sx - 0.05, ys[2] - 0.05), sw + 0.10, ys[1] + sh - ys[2] + 0.10,
                                boxstyle="round,pad=0,rounding_size=0.06", linewidth=0.9, edgecolor=fs.RED,
                                facecolor="none", linestyle=(0, (3, 2)), zorder=5))
    ax.text(sx + sw / 2, ys[2] - 0.17, "Blind spot of a T1-only monitor, e.g.\n(6.0, 6.0) vs (6.0, 6.5): both W = 311.1",
            fontsize=fs.SMALL_PT, color=fs.RED, ha="center", va="center", linespacing=1.15, zorder=5)

    tx, tw = 5.64, 1.34
    box(ax, tx, top, tw, h, "T4  Strategic harm",
        ["Gate on target tie (p, p):", "(i) profit > grid Nash", "(ii) profitable deviation",
         "(iii) p ≤ 5.5 (joint profit)", "+ deviation, response", "   rule, counterfactual",
         "Observed 6.0 / 6.5 ties", "fail (iii): not identified"],
        fill="#fbf1ee")
    arrow(ax, sx + sw + 0.05, mid, tx, mid, color=fs.FAINT)

    ey, eh = 0.02, 0.32
    tag(ax, 0.02, ey, 3.77, eh, "Closed loop: controlled-initial run (380/384 trajectories), replication (376/384),\n"
        "four-arm study (44/48 blocks).  Single shot: fixed-history diagnostic (1,458 units).", fs.MUTED)
    tag(ax, sx - 0.05, ey, sw + 0.10, eh, "Certificate; D_tie = 0.83;\ncapture start: -27.9 W", fs.AQUA)
    tag(ax, tx, ey, tw, eh, "X1 / X2 null at 6.0 tie;\nQ-learning positive control", fs.MUTED)
    fs.save(fig, "fig1-framework-evidence-map", run_alignment=False)


if __name__ == "__main__":
    main()
