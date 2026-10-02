"""Build the dynamics figure: structure diverges at the first decision; welfare does not.

(A) Per-round pooled asymmetric contrast in the equal-price rate
    (natural - hide-rival, average of LH and HL) with 95% block-bootstrap
    bands, original run and replication.  Round 0 is programmed and identical.
(B) The same contrast for welfare, on a scale where the protocol's candidate
    margin (5 welfare units) is visible.
(C) Block-level window means (rounds 10--29): structural contrast against
    welfare contrast; each point is one complete block.

Source: `analysis/structure-dynamics-20261002.json` (written by
`structure_dynamics.py`).  Descriptive; rounds repeat within trajectories.

    python paper-materials/aamas2027/tools/build_fig_dynamics.py
"""
from __future__ import annotations

import json

import matplotlib.pyplot as plt
import numpy as np

import figstyle as fs

DYNAMICS = fs.MATERIALS / "analysis" / "structure-dynamics-20261002.json"
RUNS = (("original", fs.BLUE, "o", "Original run"), ("replication", fs.ORANGE, "s", "Replication"))


def window_shade(ax) -> None:
    ax.axvspan(9.5, 29.5, color=fs.PANEL, zorder=0, linewidth=0)


def main() -> None:
    fs.apply()
    dyn = json.loads(DYNAMICS.read_text(encoding="utf-8"))
    fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(fs.DOUBLE_COLUMN_IN, 1.85),
                                           gridspec_kw={"wspace": 0.45})
    rounds = np.arange(30)
    for run, color, marker, label in RUNS:
        a = dyn["runs"][run]["asymmetric_pooled"]
        tie, band = np.array(a["tie"]), np.array(a["tie_band"])
        ax_a.fill_between(rounds, band[:, 0], band[:, 1], color=color, alpha=0.18, linewidth=0)
        ax_a.plot(rounds, tie, color=color, linewidth=1.3, label=f"{label} ({a['blocks']} blocks)")
        w, wb = np.array(a["welfare"]), np.array(a["welfare_band"])
        ax_b.fill_between(rounds, wb[:, 0], wb[:, 1], color=color, alpha=0.18, linewidth=0)
        ax_b.plot(rounds, w, color=color, linewidth=1.3)
        # Dot strip: one dot per block along the structural contrast; vertical
        # offsets only separate overlapping dots and carry no value.
        x, y = np.array(a["block_tie_window"]), np.array(a["block_welfare_window"])
        base = 1.0 if run == "original" else 0.0
        order = np.argsort(x, kind="stable")
        offsets = np.zeros(len(x))
        for rank, idx in enumerate(order):
            offsets[idx] = ((rank % 5) - 2) * 0.085
        zero = np.abs(y) < 1e-9
        ax_c.scatter(x[zero], base + offsets[zero], s=9, marker=marker, facecolor=color, edgecolor=color,
                     linewidth=0.5, zorder=3)
        ax_c.scatter(x[~zero], base + offsets[~zero], s=9, marker=marker, facecolor="white", edgecolor=color,
                     linewidth=0.8, zorder=4)

    for ax in (ax_a, ax_b):
        window_shade(ax)
        ax.axhline(0, color=fs.MUTED, linewidth=0.6, zorder=1)
        ax.set_xlim(0, 29)
        ax.set_xticks([1, 10, 20, 29])
        ax.set_xlabel("round")
    ax_a.set_ylim(-0.05, 1.0)
    ax_a.set_ylabel("equal-price rate,\nnatural − hide-rival")
    ax_a.text(19.5, 0.52, "assessment window", ha="center", va="center", fontsize=fs.SMALL_PT, color=fs.MUTED)
    handles, labels = ax_a.get_legend_handles_labels()
    ax_b.legend(handles, labels, loc="lower left", bbox_to_anchor=(0.0, 0.02), fontsize=fs.SMALL_PT,
                handlelength=1.4, borderaxespad=0.2)
    ax_b.set_ylim(-6, 6)
    ax_b.set_yticks([-5, 0, 5])
    ax_b.set_ylabel("welfare,\nnatural − hide-rival")

    ax_c.set_xlim(-0.05, 1.05)
    ax_c.set_ylim(-0.45, 1.75)
    ax_c.set_xticks([0, 0.5, 1.0])
    o, r = dyn["runs"]["original"]["asymmetric_pooled"], dyn["runs"]["replication"]["asymmetric_pooled"]
    ax_c.set_yticks([1.0, 0.0], ["Original", "Replication"])
    ax_c.tick_params(axis="y", length=0)
    ax_c.spines["left"].set_visible(False)
    ax_c.set_xlabel("equal-price contrast per block")
    ax_c.text(-0.03, 1.58, f"filled: welfare contrast exactly 0 ({o['blocks_welfare_exactly_zero']}/{o['blocks']}, "
              f"{r['blocks_welfare_exactly_zero']}/{r['blocks']})", ha="left", va="center", fontsize=fs.SMALL_PT,
              color=fs.INK)

    for ax, letter, title in ((ax_a, "A", "Structure diverges at round 1"),
                              (ax_b, "B", "Welfare barely moves"),
                              (ax_c, "C", "Per-block structural contrasts")):
        ax.set_title(title, loc="left", fontsize=fs.TEXT_PT, pad=4)
        fs.panel_label(ax, letter, x=-0.30, y=1.04)
    fig.subplots_adjust(left=0.085, right=0.99, bottom=0.25, top=0.87)
    fs.save(fig, "fig-dynamics-structure-welfare")


if __name__ == "__main__":
    main()
