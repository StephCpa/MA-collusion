"""Shared style and export helpers for the manuscript figures.

All manuscript figures use one restrained palette (validated with the dataviz
palette validator: light-mode lightness band, chroma floor, CVD separation and
contrast), 6-8 pt text at final column or page width, editable TrueType text
in the PDF and timestamp-free PDF metadata so that rebuilds are byte-stable.

When the environment variable ``NATURE_FIGURE_QA`` points to a directory that
contains ``audit_panel_alignment.py`` (from the nature-figure skill), every
multi-panel figure passes the render-time panel-alignment gate before export
and the measurement is written to ``analysis/figure-qa-20261002/`` as
``<figure>.alignment.json``.
The builders run unchanged without it.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

MATERIALS = Path(__file__).resolve().parent.parent
FIGURES = MATERIALS / "figures"
FIGURE_QA = MATERIALS / "analysis" / "figure-qa-20261002"

# Categorical slots of the validated reference palette (light mode).
BLUE, ORANGE, AQUA, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#4a3aa7", "#e34948"
BLUE_RAMP = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5",
             "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
INK, MUTED, FAINT, GRID, PANEL = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#f4f3f0"

TEXT_PT, SMALL_PT, LABEL_PT = 7.0, 6.2, 8.0
SINGLE_COLUMN_IN, DOUBLE_COLUMN_IN = 3.33, 7.0


def apply() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": TEXT_PT,
        "axes.titlesize": TEXT_PT,
        "axes.labelsize": TEXT_PT,
        "xtick.labelsize": SMALL_PT,
        "ytick.labelsize": SMALL_PT,
        "legend.fontsize": SMALL_PT,
        "axes.linewidth": 0.6,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.0,
        "ytick.major.size": 2.0,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "mathtext.default": "regular",
    })


def panel_label(ax, letter: str, x: float = -0.02, y: float = 1.02) -> None:
    """Bold panel letter at the top-left of the axes, outside the plot area."""
    ax.text(x, y, letter, transform=ax.transAxes, fontsize=LABEL_PT, fontweight="bold",
            color=INK, ha="right", va="bottom")


def _alignment_gate(fig, name: str) -> None:
    qa = os.environ.get("NATURE_FIGURE_QA")
    if not qa:
        return
    sys.path.insert(0, qa)
    from audit_panel_alignment import require_matplotlib_panel_alignment  # type: ignore

    fig.canvas.draw()
    FIGURE_QA.mkdir(parents=True, exist_ok=True)
    require_matplotlib_panel_alignment(
        fig, json_out=FIGURE_QA / f"{name}.alignment.json", tolerance_pt=1.5, gutter_tolerance_pt=1.5,
        strict=False,
    )


def save(fig, name: str, run_alignment: bool = True) -> Path:
    stem = FIGURES / name
    stem.parent.mkdir(parents=True, exist_ok=True)
    if run_alignment:
        _alignment_gate(fig, name)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.02, metadata={"CreationDate": None})
    fig.savefig(stem.with_suffix(".png"), dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"wrote figures/{name}.pdf and .png")
    return stem
