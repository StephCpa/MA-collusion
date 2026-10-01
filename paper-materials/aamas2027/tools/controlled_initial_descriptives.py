"""Reproduce descriptive summaries from the public controlled-initial ledger."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/original-controlled-initial/ledger.json"
OUT = ROOT / "analysis"
SELLERS = ("seller_a", "seller_b")


def state(event: Dict[str, Any]) -> Tuple[float, float]:
    return tuple(float(event["prices"][s]["price"]) for s in SELLERS)  # type: ignore[return-value]


def state_label(pair: Tuple[float, float]) -> str:
    return "(" + ",".join(f"{x:g}" for x in pair) + ")"


def transition_counts(events: list[Dict[str, Any]]) -> Dict[str, int]:
    out: Counter[str] = Counter()
    for before, after in zip(events, events[1:]):
        a, b = state(before), state(after)
        if a[0] != a[1] and b[0] == b[1]:
            kind = "upward_matching" if b[0] == max(a) else "downward_matching" if b[0] == min(a) else "other_tie_formation"
            out[kind] += 1
    return dict(out)


def summarize(rows: list[Dict[str, Any]]) -> Dict[str, Any]:
    table: Dict[str, Any] = {}
    transitions: Dict[str, Any] = {}
    for cell in sorted({r["cell"] for r in rows}):
        complete = [r for r in rows if r["cell"] == cell and r["status"] == "completed"]
        assessment = [e for r in complete for e in r["events"] if 10 <= e["round"] <= 29]
        round1 = [e for r in complete for e in r["events"] if e["round"] == 1]
        table[cell] = {
            "complete_trajectories": len(complete),
            "assessment_rounds": len(assessment),
            "round1_tie_count": sum(state(e)[0] == state(e)[1] for e in round1),
            "assessment_tie_rounds": sum(state(e)[0] == state(e)[1] for e in assessment),
            "assessment_state_counts": dict(Counter(state_label(state(e)) for e in assessment)),
        }
        transitions[cell] = {
            "tie_formation_counts": dict(sum((Counter(transition_counts(r["events"])) for r in complete), Counter()))
        }
    return {
        "schema": "controlled-initial-descriptives-v1",
        "scope": "descriptive summaries only; assessment rounds 10--29; transitions include observed prefixes",
        "cells": table,
        "transitions": transitions,
    }


def render(result: Dict[str, Any]) -> str:
    lines = [
        "# Original controlled-initial descriptive summaries",
        "",
        "Derived from `data/original-controlled-initial/ledger.json`; no provider calls. Counts are descriptive and repeated rounds are not independent observations.",
        "",
        "| cell | complete trajectories | round-1 ties | assessment ties / rounds | assessment states |",
        "|---|---:|---:|---:|---|",
    ]
    for cell, row in result["cells"].items():
        lines.append(
            f"| {cell} | {row['complete_trajectories']} | {row['round1_tie_count']} | "
            f"{row['assessment_tie_rounds']} / {row['assessment_rounds']} | "
            f"`{row['assessment_state_counts']}` |"
        )
    lines += ["", "## Tie-formation directions", ""]
    for cell, row in result["transitions"].items():
        lines.append(f"- `{cell}`: `{row['tie_formation_counts']}`")
    lines += ["", "The ledger intentionally excludes provider request IDs and model-call metadata."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = summarize(json.loads(args.ledger.read_text(encoding="utf-8"))["cells"])
    if args.write:
        (OUT / "original-controlled-initial-descriptives-20261002.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        (OUT / "original-controlled-initial-descriptives-20261002.md").write_text(render(result), encoding="utf-8")
    print(json.dumps({"cells": len(result["cells"]), "written": args.write}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
