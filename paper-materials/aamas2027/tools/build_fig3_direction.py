"""Build Figure 3: matching direction and structure as a leading indicator.

(A) Tie-formation events under visible rival prices, by design: programmed
    starts (Candidate A replication, LH and HL natural display) versus
    model-chosen starts (four-arm study, natural and hide-own arms).
    Downward events (the high seller cuts to the low price) are drawn left of
    zero, upward events (the low seller raises to the high price) right.
(B) Assessment-window welfare of trajectories whose round-0 state is in the
    m = 6.0 class, split by structure (tie versus capture).  Both groups start
    with welfare 311.111, so a welfare monitor cannot distinguish them.

Inputs are the outputs of `candidate_a_structural.py` and
`four_arm_leading_indicator.py`.  Offline only.

    python paper-materials/aamas2027/tools/build_fig3_direction.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
REPLICATION = MATERIALS / "analysis" / "A-confirmation-structural-20261001.json"
FOUR_ARM = MATERIALS / "analysis" / "four-arm-leading-indicator-20261001.json"
OUT = MATERIALS / "figures" / "fig3-direction-and-leading-indicator"

# Diverging pair of the validated reference palette (light mode): blue <-> red.
DOWN, UP = "#2a78d6", "#e34948"
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def style(ax) -> None:
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(axis="x", colors=MUTED, labelsize=7, length=2)
    ax.tick_params(axis="y", length=0, labelsize=7, labelcolor=INK)
    ax.set_axisbelow(True)


def main() -> None:
    rep = json.loads(REPLICATION.read_text(encoding="utf-8"))
    four = json.loads(FOUR_ARM.read_text(encoding="utf-8"))
    rows_a = [
        ("Programmed start, LH", rep["cells"]["LH-natural"]["tie_formation_events"]),
        ("Programmed start, HL", rep["cells"]["HL-natural"]["tie_formation_events"]),
        ("Model-chosen start, natural", four["arms"]["natural"]["tie_formation"]),
        ("Model-chosen start, hide-own", four["arms"]["hide_own"]["tie_formation"]),
    ]
    li = four["leading_indicator"]
    rows_b = [
        ("Programmed start, natural", li["replication_programmed_start"]["natural"]),
        ("Model-chosen start, natural", li["four_arm_model_chosen_start"]["natural"]),
        ("Model-chosen start, hide-own", li["four_arm_model_chosen_start"]["hide_own"]),
        ("Model-chosen start, hide-rival", li["four_arm_model_chosen_start"]["hide_rival"]),
    ]

    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "ps.fonttype": 42})
    fig, (ax_a, ax_b) = plt.subplots(2, 1, figsize=(3.4, 3.35), gridspec_kw={"height_ratios": [1, 1.1]})

    for i, (label, tf) in enumerate(rows_a):
        y = len(rows_a) - 1 - i
        down, up = tf["downward"], tf["upward"]
        ax_a.barh(y, -down, height=0.6, color=DOWN, edgecolor="white", linewidth=1)
        ax_a.barh(y, up, height=0.6, color=UP, edgecolor="white", linewidth=1)
        ax_a.text(-down - 1.5, y, str(down), va="center", ha="right", fontsize=6.5, color=MUTED)
        ax_a.text(up + 1.5, y, str(up), va="center", ha="left", fontsize=6.5, color=MUTED)
    ax_a.axvline(0, color=MUTED, linewidth=0.8)
    ax_a.set_yticks(range(len(rows_a)))
    ax_a.set_yticklabels([r[0] for r in reversed(rows_a)])
    ax_a.set_xlim(-68, 40)
    ax_a.set_xticks([-50, -25, 0, 25])
    ax_a.set_xticklabels(["50", "25", "0", "25"])
    ax_a.text(-3, len(rows_a) - 0.3, "\u2190 downward", ha="right", fontsize=6.3, color=DOWN)
    ax_a.text(3, len(rows_a) - 0.3, "upward \u2192", ha="left", fontsize=6.3, color=UP)
    ax_a.set_ylim(-0.6, len(rows_a) + 0.1)
    ax_a.set_title("A  Tie-formation events with rival prices visible", fontsize=7.5, loc="left", color=INK)
    style(ax_a)

    for i, (label, v) in enumerate(rows_b):
        y = len(rows_b) - 1 - i
        for group, dy, marker, face in (("tie", 0.16, "o", INK), ("capture", -0.16, "s", "white")):
            ci = v["assessment_welfare_ci95"][group]
            m = v["mean_assessment_welfare"][group]
            ax_b.plot(ci, [y + dy, y + dy], color=INK, linewidth=1.3, solid_capstyle="round")
            ax_b.plot(m, y + dy, marker=marker, markersize=4.4, markerfacecolor=face, markeredgecolor=INK,
                      markeredgewidth=0.9, linestyle="none")
        ax_b.text(316.5, y, f"n={v['n']['tie']}/{v['n']['capture']}", va="center", fontsize=6.2, color=MUTED)
    for ref, text in ((311.111, "m=6.0"), (281.944, "m=6.5 tie")):
        ax_b.axvline(ref, color=MUTED, linewidth=0.7, linestyle=(0, (3, 2)))
        ax_b.text(ref + 0.6, len(rows_b) - 0.25, text, ha="left", fontsize=6, color=MUTED)
    ax_b.set_yticks(range(len(rows_b)))
    ax_b.set_yticklabels([r[0] for r in reversed(rows_b)])
    ax_b.set_xlim(276, 322)
    ax_b.set_ylim(-0.6, len(rows_b) + 0.05)
    ax_b.set_title("B  Assessment welfare after welfare-equal starts", fontsize=7.5, loc="left", color=INK)
    style(ax_b)

    handles = [
        plt.Line2D([], [], marker="o", markersize=4.4, color=INK, linestyle="none", label="tie start (6.0, 6.0)"),
        plt.Line2D([], [], marker="s", markersize=4.4, markerfacecolor="white", markeredgecolor=INK,
                   linestyle="none", label="capture start (6.0, 6.5) / (6.5, 6.0)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=2, fontsize=6.2, frameon=False,
               bbox_to_anchor=(0.5, 0.0), handletextpad=0.3, columnspacing=1.0)
    fig.tight_layout(rect=(0, 0.05, 1, 1), h_pad=0.8)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        meta = {"CreationDate": None} if ext == "pdf" else {}
        fig.savefig(OUT.with_suffix(f".{ext}"), dpi=300 if ext == "png" else None, bbox_inches="tight", metadata=meta)
    print(f"wrote {OUT.with_suffix('.pdf').relative_to(MATERIALS)} and .png")


if __name__ == "__main__":
    main()
