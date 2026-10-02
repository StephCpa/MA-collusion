"""Per-round dynamics, block-paired contrasts and state composition for both runs.

Reads the public original controlled-initial ledger and the Candidate A
replication ledger and writes the descriptive inputs of the redesigned
Figure 2 and the dynamics figure:

1. per-round (rounds 0--29) equal-price rate and mean welfare for each
   initial cell and display arm, with 95% block-bootstrap bands for the
   natural-minus-hide-rival difference in the asymmetric cells;
2. block-level paired contrasts in the assessment window (rounds 10--29):
   equal-price fraction (natural - hide-rival) and welfare (natural -
   hide-rival), the independent-unit view of "structure moves, welfare does
   not";
3. assessment-window state composition by welfare class (tie at 6.0, capture
   at minimum price 6.0, tie at 6.5, other).

It asserts that the original ledger reproduces the frozen paired sensitivities
in `analysis/controlled-initial-followup-analysis.json`.  Offline; no provider
calls.  Post hoc and descriptive except where a frozen estimand is reproduced.

    python paper-materials/aamas2027/tools/structure_dynamics.py --check --write
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path
from statistics import mean, stdev

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
RUNS = {
    "original": MATERIALS / "data" / "original-controlled-initial" / "ledger.json",
    "replication": MATERIALS / "data" / "A-confirmation-cells.json",
}
FROZEN = MATERIALS / "analysis" / "controlled-initial-followup-analysis.json"
OUT_JSON = MATERIALS / "analysis" / "structure-dynamics-20261002.json"
OUT_MD = MATERIALS / "analysis" / "structure-dynamics-20261002.md"

INITIALS = ("LL", "LH", "HL", "HH")
ARMS = ("natural", "hide_rival")
ROUNDS = range(30)
WINDOW = range(10, 30)
SEED = 20261002
DRAWS = 5000


def load(path: Path) -> dict[tuple[str, str, int], dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data["cells"] if isinstance(data, dict) else data
    out = {}
    for row in rows:
        init, arm = row["cell"].split("-", 1)
        out[(init, arm, int(row["block"]))] = row
    return out


def prices(e: dict) -> tuple[float, float]:
    return float(e["prices"]["seller_a"]["price"]), float(e["prices"]["seller_b"]["price"])


def by_round(row: dict) -> dict[int, dict]:
    return {int(e["round"]): e for e in row["events"]}


def completed(row: dict | None) -> bool:
    return row is not None and row["status"] == "completed"


def window_mean(row: dict, fn) -> float:
    ev = by_round(row)
    return mean(fn(ev[r]) for r in WINDOW)


def is_tie(e: dict) -> float:
    a, b = prices(e)
    return float(a == b)


def welfare(e: dict) -> float:
    return float(e["total_welfare"])


def t_ci(xs: list[float]) -> list[float]:
    """95% t interval with a tabulated quantile (n - 1 >= 30 uses the normal limit)."""
    n = len(xs)
    table = {44: 2.0154, 45: 2.0141, 46: 2.0129, 47: 2.0117, 41: 2.0195, 42: 2.0181}
    q = table.get(n - 1, 1.96 if n > 120 else 2.0)
    half = q * (stdev(xs) / math.sqrt(n) if n > 1 else 0.0)
    return [mean(xs) - half, mean(xs) + half]


def boot_band(pairs: list[tuple[float, float]], rng: random.Random) -> list[float]:
    diffs = [a - b for a, b in pairs]
    means = sorted(mean(rng.choices(diffs, k=len(diffs))) for _ in range(DRAWS))
    return [means[int(0.025 * DRAWS)], means[int(0.975 * DRAWS) - 1]]


def analyse(T: dict) -> dict:
    rng = random.Random(SEED)
    per_round: dict = {}
    for init in INITIALS:
        for arm in ARMS:
            rows = [T[(init, arm, b)] for b in range(1, 49) if completed(T.get((init, arm, b)))]
            per_round[f"{init}-{arm}"] = {
                "n": len(rows),
                "tie_rate": [mean(is_tie(by_round(r)[k]) for r in rows) for k in ROUNDS],
                "mean_welfare": [mean(welfare(by_round(r)[k]) for r in rows) for k in ROUNDS],
            }
    diff_bands: dict = {}
    paired: dict = {}
    for init in ("LH", "HL"):
        blocks = [b for b in range(1, 49)
                  if completed(T.get((init, "natural", b))) and completed(T.get((init, "hide_rival", b)))]
        nat = {b: by_round(T[(init, "natural", b)]) for b in blocks}
        hid = {b: by_round(T[(init, "hide_rival", b)]) for b in blocks}
        diff_bands[init] = {
            "blocks": len(blocks),
            "tie_diff": [mean(is_tie(nat[b][k]) - is_tie(hid[b][k]) for b in blocks) for k in ROUNDS],
            "tie_diff_band": [boot_band([(is_tie(nat[b][k]), is_tie(hid[b][k])) for b in blocks], rng) for k in ROUNDS],
            "welfare_diff": [mean(welfare(nat[b][k]) - welfare(hid[b][k]) for b in blocks) for k in ROUNDS],
            "welfare_diff_band": [boot_band([(welfare(nat[b][k]), welfare(hid[b][k])) for b in blocks], rng)
                                  for k in ROUNDS],
        }
        d_eq = [window_mean(T[(init, "natural", b)], is_tie) - window_mean(T[(init, "hide_rival", b)], is_tie)
                for b in blocks]
        d_w = [window_mean(T[(init, "natural", b)], welfare) - window_mean(T[(init, "hide_rival", b)], welfare)
               for b in blocks]
        paired[init] = {
            "blocks": blocks,
            "equal_fraction_natural_minus_hide": d_eq,
            "welfare_natural_minus_hide": d_w,
            "equal_fraction_mean": mean(d_eq),
            "equal_fraction_t95": t_ci(d_eq),
            "welfare_mean": mean(d_w),
            "welfare_t95": t_ci(d_w),
            "blocks_structure_positive": sum(x > 0 for x in d_eq),
            "blocks_welfare_exactly_zero": sum(abs(x) < 1e-9 for x in d_w),
        }
    # Pooled asymmetric contrast per round: the per-round analogue of D_tie, on
    # blocks where all four asymmetric trajectories are complete.
    full = [b for b in range(1, 49) if all(completed(T.get((i, a, b))) for i in ("LH", "HL") for a in ARMS)]
    ev = {(i, a, b): by_round(T[(i, a, b)]) for i in ("LH", "HL") for a in ARMS for b in full}

    def pooled(fn, k, b):
        return 0.5 * sum(fn(ev[(i, "natural", b)][k]) - fn(ev[(i, "hide_rival", b)][k]) for i in ("LH", "HL"))

    def band(vals):
        means = sorted(mean(rng.choices(vals, k=len(vals))) for _ in range(DRAWS))
        return [means[int(0.025 * DRAWS)], means[int(0.975 * DRAWS) - 1]]

    asym = {"blocks": len(full), "tie": [], "tie_band": [], "welfare": [], "welfare_band": []}
    for k in ROUNDS:
        t = [pooled(is_tie, k, b) for b in full]
        w = [pooled(welfare, k, b) for b in full]
        asym["tie"].append(mean(t))
        asym["tie_band"].append(band(t))
        asym["welfare"].append(mean(w))
        asym["welfare_band"].append(band(w))
    block_tie = [0.5 * sum(window_mean(T[(i, "natural", b)], is_tie) - window_mean(T[(i, "hide_rival", b)], is_tie)
                           for i in ("LH", "HL")) for b in full]
    block_w = [0.5 * sum(window_mean(T[(i, "natural", b)], welfare) - window_mean(T[(i, "hide_rival", b)], welfare)
                         for i in ("LH", "HL")) for b in full]
    asym["block_tie_window"] = block_tie
    asym["block_welfare_window"] = block_w
    asym["blocks_welfare_exactly_zero"] = sum(abs(x) < 1e-9 for x in block_w)
    asym["blocks_tie_positive"] = sum(x > 0 for x in block_tie)
    composition: dict = {}
    for init in ("LH", "HL"):
        for arm in ARMS:
            counts = {"tie_6.0": 0, "capture_m6.0": 0, "tie_6.5": 0, "other": 0}
            for b in range(1, 49):
                row = T.get((init, arm, b))
                if not completed(row):
                    continue
                for k, e in by_round(row).items():
                    if k not in WINDOW:
                        continue
                    a, c = prices(e)
                    if a == c == 6.0:
                        counts["tie_6.0"] += 1
                    elif a == c == 6.5:
                        counts["tie_6.5"] += 1
                    elif min(a, c) == 6.0:
                        counts["capture_m6.0"] += 1
                    else:
                        counts["other"] += 1
            total = sum(counts.values())
            composition[f"{init}-{arm}"] = {"rounds": total, **{k: v / total for k, v in counts.items()}}
    return {"per_round": per_round, "paired_difference_by_round": diff_bands,
            "paired_assessment": paired, "asymmetric_pooled": asym, "assessment_composition": composition}


def build() -> dict:
    return {
        "scope": "offline descriptive analysis of the public original and replication ledgers; no provider calls",
        "sources": {k: str(v.relative_to(MATERIALS)) for k, v in RUNS.items()},
        "window": "assessment rounds 10-29; per-round series cover rounds 0-29 (round 0 programmed)",
        "bootstrap": {"unit": "block", "draws": DRAWS, "seed": SEED},
        "runs": {name: analyse(load(path)) for name, path in RUNS.items()},
    }


def check(r: dict) -> None:
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))["paired_block_sensitivity_natural_minus_hide_rival"]
    orig = r["runs"]["original"]["paired_assessment"]
    for init in ("LH", "HL"):
        f = frozen[init]["tie"]
        assert len(orig[init]["blocks"]) == frozen[init]["pairs"], init
        assert abs(orig[init]["equal_fraction_mean"] - f["mean_natural_minus_hide_rival"]) < 1e-9, init
        lo, hi = orig[init]["equal_fraction_t95"]
        assert abs(lo - f["t_interval_95"][0]) < 1e-3 and abs(hi - f["t_interval_95"][1]) < 1e-3, init
    rep = r["runs"]["replication"]["paired_assessment"]
    assert abs(rep["LH"]["equal_fraction_mean"] - 0.8188888888888889) < 1e-9
    pooled = r["runs"]["replication"]["asymmetric_pooled"]
    assert pooled["blocks"] == 42 and abs(mean(pooled["block_tie_window"]) - 0.8303571428571429) < 1e-9
    for run in r["runs"].values():
        for init in ("LH", "HL"):
            assert run["paired_difference_by_round"][init]["tie_diff"][0] == 0.0, "round 0 is programmed"


def render_md(r: dict) -> str:
    lines = [
        "# Structure dynamics and block-paired contrasts (2026-10-02)",
        "",
        "Generated by `tools/structure_dynamics.py` from the public ledgers; descriptive, no provider calls.",
        "",
        "| run | cell | blocks | equal-price fraction, natural − hide [95% t] | welfare, natural − hide [95% t] | "
        "blocks with structure > 0 | blocks with welfare difference exactly 0 |",
        "|---|---|---:|---|---|---:|---:|",
    ]
    for run, v in r["runs"].items():
        for init in ("LH", "HL"):
            p = v["paired_assessment"][init]
            lines.append(
                f"| {run} | {init} | {len(p['blocks'])} | {p['equal_fraction_mean']:.3f} "
                f"[{p['equal_fraction_t95'][0]:.3f}, {p['equal_fraction_t95'][1]:.3f}] | {p['welfare_mean']:.2f} "
                f"[{p['welfare_t95'][0]:.2f}, {p['welfare_t95'][1]:.2f}] | {p['blocks_structure_positive']} | "
                f"{p['blocks_welfare_exactly_zero']} |")
    lines += ["", "Round-1 and assessment-window paired differences in the equal-price rate:", "",
              "| run | cell | round 1 | rounds 10–29 mean |", "|---|---|---:|---:|"]
    for run, v in r["runs"].items():
        for init in ("LH", "HL"):
            d = v["paired_difference_by_round"][init]["tie_diff"]
            lines.append(f"| {run} | {init} | {d[1]:.3f} | {mean(d[10:30]):.3f} |")
    lines += ["", "Assessment-window composition (share of rounds):", "",
              "| run | cell-arm | tie at 6.0 | capture, m = 6.0 | tie at 6.5 | other |", "|---|---|---:|---:|---:|---:|"]
    for run, v in r["runs"].items():
        for key, c in v["assessment_composition"].items():
            lines.append(f"| {run} | {key} | {c['tie_6.0']:.3f} | {c['capture_m6.0']:.3f} | {c['tie_6.5']:.3f} | "
                         f"{c['other']:.3f} |")
    lines += ["", "Pooled asymmetric contrast (average of LH and HL, natural − hide-rival), blocks complete in both cells:", "",
              "| run | blocks | round 1 equal-price | window mean equal-price | blocks with structure > 0 | "
              "blocks with welfare difference exactly 0 |", "|---|---:|---:|---:|---:|---:|"]
    for run, v in r["runs"].items():
        a = v["asymmetric_pooled"]
        lines.append(f"| {run} | {a['blocks']} | {a['tie'][1]:.3f} | {mean(a['block_tie_window']):.3f} | "
                     f"{a['blocks_tie_positive']} | {a['blocks_welfare_exactly_zero']} |")
    lines += ["", "Rounds repeat within trajectories; per-round bands use block resampling and are descriptive.", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    r = build()
    if args.check:
        try:
            check(r)
        except AssertionError as exc:
            print(f"CHECK FAILED: {exc!r}", file=sys.stderr)
            return 1
    if args.write:
        OUT_JSON.write_text(json.dumps(r, indent=1) + "\n", encoding="utf-8")
        OUT_MD.write_text(render_md(r), encoding="utf-8")
    print(render_md(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
