"""Build Figure 1: the same trajectories seen by a welfare monitor and by a joint-state monitor.

Left: the closed-loop setup (two language-model sellers, two display arms).
Centre: real replication data for the asymmetric cells (LH and HL pooled),
read through two monitor surfaces.  The welfare monitor (T1) shows both arms
at the same welfare on the full grid-welfare scale; the joint-state monitor
(T2, T3) shows the arms diverging at the first model decision.  Right: what
each target recovers for the two states that drive the contrast, with the
strategic-harm target (T4) set aside as a note because this study does not
test it.

Sources: `analysis/structure-dynamics-20261002.json` (per-round means over
completed replication trajectories; descriptive) and
`analysis/A-confirmation-structural-20261001.json` (the quoted contrasts are
the replication's registered welfare contrast D_asym and structural primary
D_tie, both block-level).

    python paper-materials/aamas2027/tools/build_fig1_framework.py
"""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

import figstyle as fs

W, H = 7.0, 1.96
DYNAMICS = fs.MATERIALS / "analysis" / "structure-dynamics-20261002.json"
REPLICATION = fs.MATERIALS / "analysis" / "A-confirmation-structural-20261001.json"
ROUNDS = np.arange(1, 30)
WINDOW = (9.5, 29.5)
WELFARE_SUPPORT = (281.9, 444.4)


def arm_series(per_round: dict, arm: str, key: str) -> np.ndarray:
    """Average of the LH and HL cell means, rounds 1-29."""
    cells = [np.array(per_round[f"{cell}-{arm}"][key][1:]) for cell in ("LH", "HL")]
    return (cells[0] + cells[1]) / 2


def box(ax, x, y, w, h, fill=fs.PANEL, edge=fs.FAINT, style="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.05", linewidth=0.6,
                                edgecolor=edge, facecolor=fill, linestyle=style, zorder=1))


def arrow(ax, x0, y0, x1, y1, color=fs.MUTED):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=7, color=color,
                                 linewidth=0.8, shrinkA=0, shrinkB=0, zorder=4))


def target(ax, x, y, w, h, title, body, mark, accent):
    box(ax, x, y, w, h)
    ax.add_patch(Rectangle((x, y), 0.055, h, facecolor=accent, edgecolor="none", zorder=2))
    ax.text(x + 0.11, y + h - 0.065, title, fontsize=fs.TEXT_PT, fontweight="bold", color=fs.INK,
            ha="left", va="top", zorder=3)
    ax.text(x + 0.11, y + h - 0.215, body, fontsize=fs.SMALL_PT, color=fs.INK, ha="left", va="top",
            linespacing=1.25, zorder=3)
    ax.text(x + w - 0.07, y + h - 0.065, mark, fontsize=fs.LABEL_PT, fontweight="bold", color=accent,
            ha="right", va="top", zorder=3)


def setup_column(ax) -> None:
    x, y, w, h = 0.02, 0.06, 1.34, 1.84
    box(ax, x, y, w, h)
    tx = x + 0.09
    ax.text(tx, y + h - 0.07, "Two LLM sellers", fontsize=fs.TEXT_PT, fontweight="bold", color=fs.INK,
            ha="left", va="top")
    ax.text(tx, y + h - 0.23, "price every round;\nno messages and no\nprofit feedback", fontsize=fs.SMALL_PT,
            color=fs.INK, ha="left", va="top", linespacing=1.25)
    ax.text(tx, y + h - 0.68, "Display arms", fontsize=fs.TEXT_PT, fontweight="bold", color=fs.INK,
            ha="left", va="top")
    for i, (color, label) in enumerate(((fs.BLUE, "natural: rival's past\nprices shown"),
                                        (fs.ORANGE, "hide-rival: rival's\nprices set to null"))):
        top = y + h - 0.84 - 0.30 * i
        ax.plot([tx + 0.04], [top - 0.045], marker="o", markersize=4, color=color, zorder=3)
        ax.text(tx + 0.12, top, label, fontsize=fs.SMALL_PT, color=fs.INK, ha="left", va="top",
                linespacing=1.2)
    ax.text(tx, y + 0.08, "start (6.0, 6.5) or (6.5, 6.0);\n30 rounds", fontsize=fs.SMALL_PT, color=fs.MUTED,
            ha="left", va="bottom", linespacing=1.2)


def monitor_panels(fig, ax, dyn: dict, rep: dict) -> tuple[float, float]:
    per_round = dyn["runs"]["replication"]["per_round"]
    d_asym = rep["registered_welfare"]["D_asym"]["mean"]
    d_tie = rep["structural_primary"]["D_tie"]["mean"]
    left, width, height = 2.02, 2.06, 0.50
    rows = {"welfare": 1.13, "structure": 0.30}
    centres = {k: v + height / 2 for k, v in rows.items()}
    for key, bottom in rows.items():
        a = fig.add_axes([left / W, bottom / H, width / W, height / H])
        a.axvspan(*WINDOW, color=fs.PANEL, linewidth=0, zorder=0)
        if key == "welfare":
            nat, hide = arm_series(per_round, "natural", "mean_welfare"), arm_series(per_round, "hide_rival",
                                                                                   "mean_welfare")
            a.plot(ROUNDS, nat, color=fs.BLUE, linewidth=1.4, zorder=3)
            a.plot(ROUNDS, hide, color=fs.ORANGE, linewidth=1.2, linestyle=(0, (2.2, 1.6)), zorder=4)
            a.set_ylim(*WELFARE_SUPPORT)
            a.set_yticks([300, 400])
            a.set_ylabel("welfare", labelpad=2)
            a.tick_params(axis="x", labelbottom=False)
            a.text(19.5, 392, f"both arms at W ≈ 311\nwelfare contrast {d_asym:.2f}", fontsize=fs.SMALL_PT,
                   color=fs.INK, ha="center", va="center", linespacing=1.2)
            title = "Welfare monitor (T1): arms look the same"
        else:
            nat, hide = arm_series(per_round, "natural", "tie_rate"), arm_series(per_round, "hide_rival", "tie_rate")
            a.plot(ROUNDS, nat, color=fs.BLUE, linewidth=1.4, zorder=3)
            a.plot(ROUNDS, hide, color=fs.ORANGE, linewidth=1.2, linestyle=(0, (2.2, 1.6)), zorder=4)
            a.set_ylim(-0.06, 1.0)
            a.set_yticks([0, 0.5, 1.0], ["0", "0.5", "1"])
            a.set_ylabel("equal-price\nrate", labelpad=2)
            a.set_xticks([1, 10, 20, 29])
            a.set_xlabel("round", labelpad=1)
            a.text(10.6, 0.63, "natural", fontsize=fs.SMALL_PT, color=fs.BLUE, ha="left", va="center")
            a.text(3.0, 0.14, "hide-rival", fontsize=fs.SMALL_PT, color=fs.ORANGE, ha="left", va="center")
            a.text(20.0, 0.30, f"structural contrast {d_tie:.2f}", fontsize=fs.SMALL_PT, color=fs.INK, ha="center",
                   va="center")
            title = "Joint-state monitor (T2, T3): arms diverge"
        a.set_xlim(0.5, 29.5)
        a.tick_params(length=2, pad=1.5)
        ax.text(left - 0.30, bottom + height + 0.07, title, fontsize=fs.TEXT_PT, fontweight="bold", color=fs.INK,
                ha="left", va="bottom")
    return centres["welfare"], centres["structure"]


def main() -> None:
    fs.apply()
    dyn = json.loads(DYNAMICS.read_text(encoding="utf-8"))
    rep = json.loads(REPLICATION.read_text(encoding="utf-8"))
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    setup_column(ax)
    y_top, y_bottom = monitor_panels(fig, ax, dyn, rep)

    # The same trajectories feed both monitors.
    fork_x = 1.47
    arrow(ax, 1.36, (y_top + y_bottom) / 2, fork_x, (y_top + y_bottom) / 2)
    ax.plot([fork_x, fork_x], [y_bottom, y_top], color=fs.MUTED, linewidth=0.8, zorder=4)
    arrow(ax, fork_x, y_top, 1.56, y_top)
    arrow(ax, fork_x, y_bottom, 1.56, y_bottom)

    tx, tw = 4.40, 1.52
    t1 = (1.10, 0.62)
    t2 = (0.58, 0.44)
    t3 = (0.06, 0.44)
    target(ax, tx, t1[0], tw, t1[1], "T1  Market outcome", "minimum price, welfare:\n(6.0, 6.0), (6.0, 6.5) same W",
           "✗", fs.RED)
    target(ax, tx, t2[0], tw, t2[1], "T2  Joint structure", "ties, transitions:\ntie vs capture visible",
           "✓", fs.AQUA)
    target(ax, tx, t3[0], tw, t3[1], "T3  Allocation", "seller rewards:\n(111, 111) vs (222, 0)", "✓", fs.AQUA)
    arrow(ax, 4.14, y_top, tx, t1[0] + t1[1] / 2)
    arrow(ax, 4.14, y_bottom, tx, t2[0] + t2[1] / 2)
    arrow(ax, 4.14, y_bottom, tx, t3[0] + t3[1] / 2)

    # Strategic harm is outside this study's identified targets: a side note, not a next step.
    sx, sw = 6.04, 0.94
    box(ax, sx, 0.06, sw, 1.66, fill="#fbf1ee", edge=fs.FAINT, style=(0, (3, 2)))
    ax.text(sx + 0.08, 1.65, "T4  Strategic\nharm", fontsize=fs.TEXT_PT, fontweight="bold", color=fs.INK,
            ha="left", va="top", linespacing=1.15)
    ax.text(sx + 0.08, 1.30, "Not tested here.\nNeeds additional\ncounterfactual\ndeviation evidence\n(Section 3.3).",
            fontsize=fs.SMALL_PT, color=fs.MUTED, ha="left", va="top", linespacing=1.25)
    fs.save(fig, "fig1-framework-evidence-map", run_alignment=False)


if __name__ == "__main__":
    main()
