"""Build Figure 2: welfare versus structural contrasts, original run and Candidate A.

Inputs are the frozen controlled-initial follow-up analysis and the Candidate A
structural analysis written by `candidate_a_structural.py`.  Offline only.

    python paper-materials/aamas2027/tools/build_fig2_replication.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
ORIGINAL = MATERIALS / "analysis" / "controlled-initial-followup-analysis.json"
REPLICATION = MATERIALS / "analysis" / "A-confirmation-structural-20261001.json"
OUT = MATERIALS / "figures" / "fig2-welfare-versus-structure"

# Categorical slots 1-2 of the validated reference palette (light mode), with
# marker shape as a secondary encoding for grayscale print.
SERIES = {
    "original": {"color": "#2a78d6", "marker": "o", "label": "Original run (380/384)"},
    "replication": {"color": "#eb6834", "marker": "s", "label": "Candidate A replication (376/384)"},
}
INK, MUTED, GRID, MARGIN_FILL = "#0b0b0b", "#52514e", "#e4e3df", "#efeeea"
DELTA_W = 5.0


def load() -> tuple[dict, dict]:
    orig = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    rep = json.loads(REPLICATION.read_text(encoding="utf-8"))
    welfare = {
        "original": {k: {"mean": orig["registered_context"][k]["mean"],
                         "ci": orig["registered_context"][k]["ci"],
                         "range": orig["registered_context"][k]["planned_completion_range"],
                         "n": orig["registered_context"][k]["complete_blocks"]} for k in ("D_asym", "J")},
        "replication": {k: {"mean": rep["registered_welfare"][k]["mean"],
                            "ci": rep["registered_welfare"][k]["bonferroni_block_t_95"],
                            "range": rep["registered_welfare"][k]["completion_range"]["full_grid_welfare_support"],
                            "n": rep["registered_welfare"][k]["complete_blocks"]} for k in ("D_asym", "J")},
    }
    sens = orig["paired_block_sensitivity_natural_minus_hide_rival"]
    structure = {
        "original": {k: {"mean": sens[k]["tie"]["mean_natural_minus_hide_rival"],
                         "ci": sens[k]["tie"]["t_interval_95"], "n": sens[k]["pairs"]} for k in ("LH", "HL")},
        "replication": {k: {"mean": rep["structural_primary"][k]["mean"],
                            "ci": rep["structural_primary"][k]["block_t_95"],
                            "n": rep["structural_primary"][k]["complete_pairs"]} for k in ("LH", "HL")},
    }
    d = rep["structural_primary"]["D_tie"]
    structure["replication"]["D_tie"] = {"mean": d["mean"], "ci": d["block_t_95"],
                                         "range": d["completion_range"], "n": d["complete_blocks"]}
    return welfare, structure


def style_axis(ax) -> None:
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(axis="x", colors=MUTED, labelsize=7, length=2)
    ax.tick_params(axis="y", length=0, labelsize=7.5, labelcolor=INK)
    ax.set_axisbelow(True)


def draw_rows(ax, data: dict, rows: list[str], labels: list[str], fmt: str) -> None:
    offsets = {"original": 0.17, "replication": -0.17}
    for i, row in enumerate(rows):
        y0 = len(rows) - 1 - i
        for series, spec in SERIES.items():
            point = data[series].get(row)
            if point is None:
                continue
            y = y0 + offsets[series]
            if "range" in point:
                ax.plot(point["range"], [y, y], color=spec["color"], alpha=0.35, linewidth=5,
                        solid_capstyle="butt", zorder=2)
            ax.plot(point["ci"], [y, y], color=spec["color"], linewidth=1.6, solid_capstyle="round", zorder=3)
            ax.plot(point["mean"], y, marker=spec["marker"], markersize=4.6, color=spec["color"],
                    markeredgecolor="white", markeredgewidth=0.8, zorder=4, linestyle="none")
            right = max(point["ci"][1], point.get("range", point["ci"])[1])
            ax.annotate(f"{point['mean']:{fmt}} (n={point['n']})", xy=(right, y), xytext=(4, 0),
                        textcoords="offset points", va="center", fontsize=6.3, color=MUTED)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(list(reversed(labels)))
    ax.set_ylim(-0.6, len(rows) - 0.4)


def main() -> None:
    welfare, structure = load()
    plt.rcParams.update({"font.family": "DejaVu Sans", "pdf.fonttype": 42, "ps.fonttype": 42})
    fig, (ax_w, ax_s) = plt.subplots(2, 1, figsize=(3.4, 3.0), gridspec_kw={"height_ratios": [2, 3]})

    ax_w.axvspan(-DELTA_W, DELTA_W, color=MARGIN_FILL, zorder=0, linewidth=0)
    ax_w.axvline(0, color=MUTED, linewidth=0.8, zorder=1)
    draw_rows(ax_w, welfare, ["D_asym", "J"], [r"$D_{\mathrm{asym}}$", r"$J$"], ".2f")
    ax_w.set_xlim(-7.5, 10.5)
    ax_w.set_xticks([-5, 0, 5])
    ax_w.set_title("A  Registered welfare contrasts (hide-rival − natural)", fontsize=7.5, loc="left", color=INK)
    style_axis(ax_w)

    ax_s.axvline(0, color=MUTED, linewidth=0.8, zorder=1)
    draw_rows(ax_s, structure, ["LH", "HL", "D_tie"], ["LH", "HL", r"$D_{\mathrm{tie}}$"], ".3f")
    ax_s.set_xlim(-0.05, 1.3)
    ax_s.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax_s.set_title("B  Equal-price fraction (natural − hide-rival)", fontsize=7.5, loc="left", color=INK)
    style_axis(ax_s)

    handles = [plt.Line2D([], [], color=s["color"], marker=s["marker"], markersize=4.6, linewidth=1.6,
                          markeredgecolor="white", label=s["label"]) for s in SERIES.values()]
    handles.append(plt.Line2D([], [], color=MUTED, alpha=0.35, linewidth=5, label="Missing-outcome completion range"))
    fig.legend(handles=handles, loc="lower center", ncol=1, fontsize=6.3, frameon=False,
               bbox_to_anchor=(0.5, 0.0), handlelength=1.8)
    fig.tight_layout(rect=(0, 0.13, 1, 1), h_pad=0.6)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png"):
        # Drop the creation timestamp so rebuilds are byte-reproducible.
        meta = {"CreationDate": None} if ext == "pdf" else {}
        fig.savefig(OUT.with_suffix(f".{ext}"), dpi=300 if ext == "png" else None, bbox_inches="tight", metadata=meta)
    print(f"wrote {OUT.with_suffix('.pdf').relative_to(MATERIALS)} and .png")


if __name__ == "__main__":
    main()
