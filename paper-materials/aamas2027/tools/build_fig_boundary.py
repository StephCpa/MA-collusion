"""Build the boundary-conditions figure: when is a display effect invisible to welfare?

(A) Agent class.  Display effect on structure (equal-price fraction,
    natural - hide-rival) against its effect on welfare (natural -
    hide-rival).  LLM runs: pooled asymmetric contrast per complete block
    (block-t 95% intervals).  Q-learning baseline: LH and HL programmed starts,
    200 independent sessions per arm (normal 95% intervals).
(B) Market rule: captive consumers.  Share of the 90 tie-versus-capture pairs
    at equal minimum price that a welfare monitor with relative resolution eps
    cannot separate, as the captive share theta per seller grows (theta = 0 is
    the study's settlement).  Exact arithmetic.
(C) Market rule: number of sellers.  Share of allocation-distinct state pairs
    that welfare cannot separate in homogeneous Bertrand.

Sources: `analysis/structure-dynamics-20261002.json`,
`analysis/qlearning-baseline-20261001.json`, `settlement_generalization.py`.

    python paper-materials/aamas2027/tools/build_fig_boundary.py
"""
from __future__ import annotations

import json
import math
from statistics import mean, stdev

import matplotlib.pyplot as plt
import numpy as np

import figstyle as fs
import settlement_generalization as sg

DYNAMICS = fs.MATERIALS / "analysis" / "structure-dynamics-20261002.json"
QLEARN = fs.MATERIALS / "analysis" / "qlearning-baseline-20261001.json"
T975 = {41: 2.0195, 46: 2.0129}


def tci(xs: list[float]) -> tuple[float, float]:
    half = T975.get(len(xs) - 1, 2.0) * stdev(xs) / math.sqrt(len(xs))
    return mean(xs) - half, mean(xs) + half


def agent_panel(ax) -> None:
    dyn = json.loads(DYNAMICS.read_text(encoding="utf-8"))
    for run, color, marker, label in (("original", fs.BLUE, "o", "LLM, original run"),
                                      ("replication", fs.ORANGE, "s", "LLM, replication")):
        a = dyn["runs"][run]["asymmetric_pooled"]
        x, y = a["block_tie_window"], a["block_welfare_window"]
        (xl, xh), (yl, yh) = tci(x), tci(y)
        ax.errorbar(mean(x), mean(y), xerr=[[mean(x) - xl], [xh - mean(x)]], yerr=[[mean(y) - yl], [yh - mean(y)]],
                    fmt=marker, color=color, markersize=4, elinewidth=0.9, capsize=0, label=label, zorder=3)
    q = json.loads(QLEARN.read_text(encoding="utf-8"))["contrasts_natural_vs_hide_rival"]
    for i, start in enumerate(("LH", "HL")):
        c = q[start]
        x, (xl, xh) = c["equal_fraction_natural_minus_hide"], c["equal_fraction_95"]
        y = -c["welfare_hide_minus_natural"]
        yl, yh = -c["welfare_95"][1], -c["welfare_95"][0]
        ax.errorbar(x, y, xerr=[[x - xl], [xh - x]], yerr=[[y - yl], [yh - y]], fmt="D", color=fs.VIOLET,
                    markersize=3.6, elinewidth=0.9, capsize=0, label="Q-learning (LH, HL)" if i == 0 else None,
                    zorder=3)
    ax.axhline(0, color=fs.MUTED, linewidth=0.6, zorder=1)
    ax.axvline(0, color=fs.MUTED, linewidth=0.6, zorder=1)
    ax.set_xlim(-0.55, 1.05)
    ax.set_ylim(-50, 8)
    ax.set_xticks([-0.5, 0, 0.5, 1.0])
    ax.set_xlabel("structural effect (equal-price fraction)")
    ax.set_ylabel("welfare effect")
    ax.text(0.85, -8, "structure moves,\nwelfare flat", ha="center", va="top", fontsize=fs.SMALL_PT, color=fs.INK)
    ax.legend(loc="lower right", bbox_to_anchor=(1.02, 0.0), fontsize=fs.SMALL_PT, handlelength=1.0,
              borderaxespad=0.2)


def captive_panel(ax) -> None:
    thetas = np.round(np.arange(0.0, 0.501, 0.01), 3)
    rows = [sg.captive_blindness(float(t)) for t in thetas]
    for eps, color, style, label in (("0.05", fs.BLUE_RAMP[11], "-", "ε = 5%"),
                                     ("0.01", fs.BLUE_RAMP[8], "-", "ε = 1%"),
                                     ("0.001", fs.BLUE_RAMP[5], "-", "ε = 0.1%")):
        ax.plot(thetas, [r["by_epsilon"][eps] for r in rows], color=color, linestyle=style, linewidth=1.3, label=label)
    ax.plot(thetas, [r["by_epsilon"]["0.0"] for r in rows], color=fs.MUTED, linestyle=(0, (2, 1.5)), linewidth=0.9,
            label="_exact welfare")
    ax.set_xlim(0, 0.5)
    ax.set_ylim(-0.03, 1.05)
    ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
    ax.set_xlabel("captive share per seller θ")
    ax.set_ylabel("tie vs capture pairs\nwelfare cannot separate")
    ax.legend(loc="upper right", bbox_to_anchor=(1.02, 1.02), fontsize=fs.SMALL_PT, handlelength=1.4,
              borderaxespad=0.2, labelspacing=0.3)


def seller_panel(ax) -> None:
    rows = sg.build()["n_sellers_homogeneous_bertrand"]
    xs = [r["sellers"] for r in rows]
    ys = [r["blind_share"] for r in rows]
    ax.bar(xs, ys, width=0.55, color=fs.BLUE, edgecolor="white", linewidth=0.6)
    for x, y, r in zip(xs, ys, rows):
        ax.text(x, y + 0.008, f"{y:.3f}", ha="center", va="bottom", fontsize=fs.SMALL_PT, color=fs.INK)
    ax.set_xticks(xs, [f"N = {r['sellers']}\n({r['ordered_states']:,})" for r in rows])
    ax.set_xlabel("sellers (ordered states)")
    ax.tick_params(axis="x", length=0, pad=3)
    ax.set_ylim(0, 0.24)
    ax.set_yticks([0, 0.1, 0.2])
    ax.set_ylabel("allocation-distinct pairs\nwelfare cannot separate")


def main() -> None:
    fs.apply()
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(fs.DOUBLE_COLUMN_IN, 1.85), gridspec_kw={"wspace": 0.55})
    agent_panel(ax_a)
    captive_panel(ax_b)
    seller_panel(ax_c)
    for ax, letter, title in ((ax_a, "A", "Agent class"), (ax_b, "B", "Captive consumers"),
                              (ax_c, "C", "Number of sellers")):
        ax.set_title(title, loc="left", fontsize=fs.TEXT_PT, pad=4)
        fs.panel_label(ax, letter, x=-0.30, y=1.04)
    fig.subplots_adjust(left=0.085, right=0.99, bottom=0.25, top=0.87)
    fs.save(fig, "fig-boundary-conditions")


if __name__ == "__main__":
    main()
