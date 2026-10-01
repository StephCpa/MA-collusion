"""Build descriptive figures from the public controlled-initial ledger."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Tuple

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/original-controlled-initial/ledger.json"
OUT = ROOT / "figures"
SELLERS = ("seller_a", "seller_b")


def state(event: Dict[str, Any]) -> Tuple[float, float]:
    return tuple(float(event["prices"][s]["price"]) for s in SELLERS)  # type: ignore[return-value]


def transition_direction(events: list[Dict[str, Any]]) -> Counter[str]:
    result: Counter[str] = Counter()
    for before, after in zip(events, events[1:]):
        a, b = state(before), state(after)
        if a[0] != a[1] and b[0] == b[1]:
            if b[0] == max(a):
                result["upward"] += 1
            elif b[0] == min(a):
                result["downward"] += 1
    return result


def cell_rows(rows: list[Dict[str, Any]], cell: str) -> list[Dict[str, Any]]:
    return [r for r in rows if r["cell"] == cell and r["status"] == "completed"]


def draw(rows: list[Dict[str, Any]], out: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(9.0, 6.8))
    for ax, cell in zip(axes[0], ("LH-natural", "LH-hide_rival")):
        counts = Counter()
        for row in cell_rows(rows, cell):
            counts.update(
                f"{state(e)[0]:g},{state(e)[1]:g}"
                for e in row["events"]
                if 10 <= e["round"] <= 29
            )
        labels = [(6.0, 6.0), (6.0, 6.5), (6.5, 6.0), (6.5, 6.5)]
        values = [counts[f"{a:g},{b:g}"] for a, b in labels]
        mat = np.array([[values[0], values[2]], [values[1], values[3]]])
        im = ax.imshow(mat, cmap="Blues", vmin=0, vmax=max(1, int(mat.max())))
        ax.set_xticks([0, 1], ["A=6.0", "A=6.5"])
        ax.set_yticks([0, 1], ["B=6.0", "B=6.5"])
        ax.set_title(cell.replace("_", " "))
        for i in range(2):
            for j in range(2):
                ax.text(j, i, int(mat[i, j]), ha="center", va="center")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    cells = ["LH-natural", "LH-hide_rival", "HL-natural", "HL-hide_rival"]
    directions = []
    for cell in cells:
        c: Counter[str] = Counter()
        for row in cell_rows(rows, cell):
            c.update(transition_direction(row["events"]))
        directions.append(c)
    x = np.arange(len(cells))
    downward = [c["downward"] for c in directions]
    upward = [c["upward"] for c in directions]
    axes[1, 0].bar(x, downward, label="downward", color="#4C78A8")
    axes[1, 0].bar(x, upward, bottom=downward, label="upward", color="#E45756")
    axes[1, 0].set_xticks(x, ["LH\nnatural", "LH\nhide rival", "HL\nnatural", "HL\nhide rival"])
    axes[1, 0].set_ylabel("tie-formation events")
    axes[1, 0].set_title("Matching direction")
    axes[1, 0].legend(frameon=False, fontsize=8)

    assessment_ties = []
    for cell in cells:
        events = [e for r in cell_rows(rows, cell) for e in r["events"] if 10 <= e["round"] <= 29]
        assessment_ties.append(sum(state(e)[0] == state(e)[1] for e in events) / max(1, len(events)))
    axes[1, 1].bar(x, assessment_ties, color="#72B7B2")
    axes[1, 1].set_xticks(x, ["LH\nnatural", "LH\nhide rival", "HL\nnatural", "HL\nhide rival"])
    axes[1, 1].set_ylim(0, 1)
    axes[1, 1].set_ylabel("equal-price round fraction")
    axes[1, 1].set_title("Assessment-window structure")
    fig.suptitle("Controlled-initial descriptive evidence", fontsize=13, y=0.98)
    fig.text(0.5, 0.012, "Descriptive counts; repeated rounds are not independent observations.", ha="center", fontsize=8)
    fig.subplots_adjust(left=0.08, right=0.94, bottom=0.16, top=0.90, wspace=0.42, hspace=0.38)
    fig.savefig(out.with_suffix(".png"), dpi=300, facecolor="white")
    fig.savefig(out.with_suffix(".pdf"), facecolor="white")
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--output", type=Path, default=OUT / "original-controlled-initial-descriptives")
    args = parser.parse_args()
    rows = json.loads(args.ledger.read_text(encoding="utf-8"))["cells"]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    draw(rows, args.output)
    print(json.dumps({"png": str(args.output.with_suffix('.png')), "pdf": str(args.output.with_suffix('.pdf'))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
