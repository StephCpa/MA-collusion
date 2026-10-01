"""Candidate A: reproduce the registered welfare contrasts and add the structural primary.

The Candidate A protocol (`protocols/confirmation-A-protocol.md`) names the
natural-minus-hide-rival contrast in equal-price persistence (LH, HL and their
average D_tie) as the structural primary, but the frozen analysis
(`data/A-confirmation-analysis.json`) reports only the welfare contrasts.  This
script:

1. reproduces D_asym and J (complete blocks, Bonferroni block-t intervals and
   the full-welfare-support completion ranges) and asserts agreement with the
   frozen analysis file, which it never modifies;
2. computes D_tie with the protocol's block-level two-sided 95% interval, a
   seeded block bootstrap, sign counts and a completion range;
3. records the descriptive tables used by the manuscript (round-1 states,
   assessment-window states, first-change rates, tie-formation direction, and
   choices after a previous rival price of 6.5 split by the seller's own
   previous price).

Assessment window: rounds 10--29 of each trajectory.  Equal-price persistence
is operationalised, as in the controlled-initial study, as the fraction of
assessment rounds with p_A == p_B.  Offline only: no provider calls.

    python paper-materials/aamas2027/tools/candidate_a_structural.py --check --write
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter
from itertools import product
from pathlib import Path
from statistics import mean, stdev

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
LEDGER = MATERIALS / "data" / "A-confirmation-cells.json"
FROZEN = MATERIALS / "data" / "A-confirmation-analysis.json"
OUT_JSON = MATERIALS / "analysis" / "A-confirmation-structural-20261001.json"
OUT_MD = MATERIALS / "analysis" / "A-confirmation-structural-20261001.md"

INITIALS = ("LL", "LH", "HL", "HH")
ARMS = ("natural", "hide_rival")
BLOCKS = range(1, 49)
WINDOW = range(10, 30)
GRID = [2.0 + 0.5 * i for i in range(10)]
DELTA_W = 5.0  # protocol candidate margin; 3 and 10 are descriptive only
BOOT_DRAWS = 20000
BOOT_SEED = 20261001


def welfare(m: float) -> float:
    q = 100 * (10 - m) / 9
    return 0.5 * (10 - m) * q + (m - 1) * q


W_SUPPORT = (min(map(welfare, GRID)), max(map(welfare, GRID)))


# ---------------------------------------------------------------- statistics
def _betainc(a: float, b: float, x: float) -> float:
    """Regularised incomplete beta via Lentz continued fraction."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)

    def cf(a: float, b: float, x: float) -> float:
        tiny = 1e-300
        c, d = 1.0, 1.0 - (a + b) * x / (a + 1)
        d = 1.0 / (d if abs(d) > tiny else tiny)
        h = d
        for m in range(1, 400):
            m2 = 2 * m
            for num in (m * (b - m) * x / ((a - 1 + m2) * (a + m2)),
                        -(a + m) * (a + b + m) * x / ((a + m2) * (a + 1 + m2))):
                d = 1.0 + num * d
                d = 1.0 / (d if abs(d) > tiny else tiny)
                c = 1.0 + num / c
                c = c if abs(c) > tiny else tiny
                h *= d * c
            if abs(d * c - 1.0) < 1e-16:
                break
        return h

    if x < (a + 1) / (a + b + 2):
        return math.exp(lbeta) * cf(a, b, x) / a
    return 1.0 - math.exp(lbeta) * cf(b, a, 1 - x) / b


def t_cdf(t: float, df: int) -> float:
    tail = 0.5 * _betainc(df / 2, 0.5, df / (df + t * t))
    return 1 - tail if t > 0 else tail


def t_quantile(p: float, df: int) -> float:
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if t_cdf(mid, df) < p else (lo, mid)
    return (lo + hi) / 2


def t_interval(xs: list[float], alpha: float) -> list[float]:
    n, m = len(xs), mean(xs)
    half = t_quantile(1 - alpha / 2, n - 1) * stdev(xs) / math.sqrt(n)
    return [m - half, m + half]


def bootstrap(xs: list[float], seed: int = BOOT_SEED, draws: int = BOOT_DRAWS) -> list[float]:
    rng = random.Random(seed)
    means = sorted(mean(rng.choices(xs, k=len(xs))) for _ in range(draws))
    return [means[int(0.025 * draws)], means[int(0.975 * draws) - 1]]


def signs(xs: list[float]) -> dict[str, int]:
    return {"positive": sum(x > 0 for x in xs), "zero": sum(x == 0 for x in xs), "negative": sum(x < 0 for x in xs)}


# ---------------------------------------------------------------- ledger
def load() -> dict[tuple[str, str, int], dict]:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    out = {}
    for traj in data:
        init, arm = traj["cell"].split("-", 1)
        out[(init, arm, int(traj["block"]))] = traj
    assert len(out) == 384, len(out)
    return out


def prices(event: dict) -> tuple[float, float]:
    return event["prices"]["seller_a"]["price"], event["prices"]["seller_b"]["price"]


def window_mean(traj: dict, value, fill: float | None = None) -> float | None:
    """Assessment-window mean; partial rounds are kept and missing rounds filled."""
    by_round = {e["round"]: e for e in traj["events"]}
    vals = []
    for r in WINDOW:
        if r in by_round:
            vals.append(value(by_round[r]))
        elif fill is None:
            return None
        else:
            vals.append(fill)
    return mean(vals)


def eq(event: dict) -> float:
    pa, pb = prices(event)
    return float(pa == pb)


def wel(event: dict) -> float:
    return event["total_welfare"]


def min_price(event: dict) -> float:
    return min(prices(event))


def completed(traj: dict) -> bool:
    return traj["status"] == "completed"


# ---------------------------------------------------------------- estimands
def registered_welfare(T: dict) -> dict:
    def Y(init, arm, b, fills=None):
        t = T[(init, arm, b)]
        if completed(t):
            return window_mean(t, wel)
        if fills is None:
            return None
        return window_mean(t, wel, fills[(init, arm, b)])

    def d_asym(b, fills=None):
        v = [Y(i, a, b, fills) for i in ("LH", "HL") for a in ("hide_rival", "natural")]
        return None if None in v else 0.5 * ((v[0] - v[1]) + (v[2] - v[3]))

    def j(b, fills=None):
        da = d_asym(b, fills)
        v = [Y(i, a, b, fills) for i in ("LL", "HH") for a in ("hide_rival", "natural")]
        return None if da is None or None in v else da - 0.5 * ((v[0] - v[1]) + (v[2] - v[3]))

    failed = sorted(k for k, t in T.items() if not completed(t))
    out = {}
    for name, fn in (("D_asym", d_asym), ("J", j)):
        xs = [x for x in (fn(b) for b in BLOCKS) if x is not None]
        ranges = {}
        for label, support in (("full_grid_welfare_support", W_SUPPORT),
                               ("observed_run_welfare_support", observed_welfare_support(T))):
            ests = [mean(fn(b, dict(zip(failed, combo))) for b in BLOCKS)
                    for combo in product(support, repeat=len(failed))]
            ranges[label] = [min(ests), max(ests)]
        ci = t_interval(xs, 0.05 / 2)
        out[name] = {
            "estimand": "hide_rival minus natural (registered sign convention)",
            "complete_blocks": len(xs),
            "mean": mean(xs),
            "bonferroni_block_t_95": ci,
            "completion_range": ranges,
            "equivalence": {
                str(d): {
                    "observed_ci_within_margin": -d <= ci[0] and ci[1] <= d,
                    "registered_completion_range_within_margin": -d <= ranges["full_grid_welfare_support"][0]
                    and ranges["full_grid_welfare_support"][1] <= d,
                }
                for d in (3.0, DELTA_W, 10.0)
            },
        }
    return out


def observed_welfare_support(T: dict) -> tuple[float, float]:
    vals = {e["total_welfare"] for t in T.values() for e in t["events"]}
    return min(vals), max(vals)


def structural_primary(T: dict) -> dict:
    def E(init, arm, b, fill=None):
        t = T[(init, arm, b)]
        if completed(t):
            return window_mean(t, eq)
        return None if fill is None else window_mean(t, eq, fill)

    out = {}
    for init in ("LH", "HL"):
        xs, blocks = [], []
        for b in BLOCKS:
            n, h = E(init, "natural", b), E(init, "hide_rival", b)
            if n is not None and h is not None:
                xs.append(n - h)
                blocks.append(b)
        mins = [window_mean(T[(init, "natural", b)], min_price) - window_mean(T[(init, "hide_rival", b)], min_price)
                for b in blocks]
        out[init] = {
            "complete_pairs": len(xs),
            "mean": mean(xs),
            "block_t_95": t_interval(xs, 0.05),
            "bootstrap_95": bootstrap(xs),
            "signs": signs(xs),
            "minimum_price_natural_minus_hide": {
                "mean": mean(mins),
                "block_t_95": t_interval(mins, 0.05) if len(set(mins)) > 1 else [mean(mins), mean(mins)],
                "signs": signs(mins),
            },
        }

    def dtie(b, fill_nat=None, fill_hide=None):
        v = []
        for init in ("LH", "HL"):
            n, h = E(init, "natural", b, fill_nat), E(init, "hide_rival", b, fill_hide)
            if n is None or h is None:
                return None
            v.append(n - h)
        return mean(v)

    xs = [x for x in (dtie(b) for b in BLOCKS) if x is not None]
    # D_tie is increasing in the natural-arm fill and decreasing in the hide-arm
    # fill, so the planned-estimand completion range is attained at the corners.
    lo = mean(dtie(b, 0.0, 1.0) for b in BLOCKS)
    hi = mean(dtie(b, 1.0, 0.0) for b in BLOCKS)
    ci = t_interval(xs, 0.05)
    out["D_tie"] = {
        "estimand": "natural minus hide_rival equal-price fraction, rounds 10-29, averaged over LH and HL",
        "complete_blocks": len(xs),
        "mean": mean(xs),
        "block_t_95": ci,
        "bootstrap_95": bootstrap(xs),
        "signs": signs(xs),
        "completion_range": [lo, hi],
        "structural_confirmation": ci[0] > 0 and lo > 0,
    }
    return out


# ---------------------------------------------------------------- descriptives
def descriptives(T: dict) -> dict:
    cells = {}
    for init, arm in product(INITIALS, ARMS):
        trajs = [T[(init, arm, b)] for b in BLOCKS]
        done = [t for t in trajs if completed(t)]
        r0 = Counter(prices(e) for t in done for e in t["events"] if e["round"] == 0)
        r1 = Counter(prices(e) for t in done for e in t["events"] if e["round"] == 1)
        assess = Counter(prices(e) for t in done for e in t["events"] if e["round"] in WINDOW)
        a0, b0 = next(iter(r0))
        low, high = ("seller_a", "seller_b") if a0 < b0 else ("seller_b", "seller_a")

        def changed(t, seller, first_only):
            start = t["events"][0]["prices"][seller]["price"]
            rounds = [e for e in t["events"] if (e["round"] == 1 if first_only else e["round"] >= 1)]
            return any(e["prices"][seller]["price"] != start for e in rounds)

        n_done = len(done)
        eq_rounds = sum(c for (pa, pb), c in assess.items() if pa == pb)
        cells[f"{init}-{arm}"] = {
            "completed": n_done,
            "failed": len(trajs) - n_done,
            "failed_blocks": sorted(int(t["block"]) for t in trajs if not completed(t)),
            "round1_states": {f"({pa:g},{pb:g})": c for (pa, pb), c in sorted(r1.items())},
            "assessment_states": {f"({pa:g},{pb:g})": c for (pa, pb), c in sorted(assess.items())},
            "assessment_equal_rounds": [eq_rounds, sum(assess.values())],
            "mean_assessment_equal_fraction": mean(window_mean(t, eq) for t in done),
            "mean_assessment_welfare": mean(window_mean(t, wel) for t in done),
            "first_change_rate": None if a0 == b0 else {
                "initially_high_seller": sum(changed(t, high, True) for t in done) / n_done,
                "initially_low_seller": sum(changed(t, low, True) for t in done) / n_done,
            },
            "ever_change_rate": None if a0 == b0 else {
                "initially_high_seller": sum(changed(t, high, False) for t in done) / n_done,
                "initially_low_seller": sum(changed(t, low, False) for t in done) / n_done,
            },
            "tie_formation_events": tie_formation(done),
            "after_previous_rival_6_5": after_rival_high(done),
        }
    return cells


def tie_formation(trajs: list[dict]) -> dict[str, int]:
    """Rounds where an unequal state becomes a tie, split by direction."""
    out = Counter()
    for t in trajs:
        ev = sorted(t["events"], key=lambda e: e["round"])
        for prev, cur in zip(ev, ev[1:]):
            (pa0, pb0), (pa1, pb1) = prices(prev), prices(cur)
            if pa0 != pb0 and pa1 == pb1:
                if pa1 == min(pa0, pb0):
                    out["downward"] += 1
                elif pa1 == max(pa0, pb0):
                    out["upward"] += 1
                else:
                    out["other"] += 1
    return {k: out.get(k, 0) for k in ("downward", "upward", "other")}


def after_rival_high(trajs: list[dict]) -> dict[str, dict[str, int]]:
    """Seller choices when the previous-round rival price was 6.5.

    Split by the seller's own previous price so that continuing an existing
    (6.5, 6.5) tie is not counted as an upward move.  In hide_rival arms the
    conditioning price is not displayed to the seller.
    """
    out: dict[str, Counter] = {}
    for t in trajs:
        ev = sorted(t["events"], key=lambda e: e["round"])
        for prev, cur in zip(ev, ev[1:]):
            for me, rival in (("seller_a", "seller_b"), ("seller_b", "seller_a")):
                if prev["prices"][rival]["price"] != 6.5:
                    continue
                own_prev = prev["prices"][me]["price"]
                choice = cur["prices"][me]["price"]
                key = f"{me}|own_prev={own_prev:g}"
                out.setdefault(key, Counter())[f"{choice:g}"] += 1
    return {k: dict(sorted(v.items())) for k, v in sorted(out.items())}


# ---------------------------------------------------------------- driver
def build() -> dict:
    T = load()
    return {
        "scope": "offline re-analysis of the sealed Candidate A ledger; no provider calls; "
                 "frozen data/A-confirmation-analysis.json is read, never written",
        "source_ledger": str(LEDGER.relative_to(MATERIALS)),
        "assessment_window": "rounds 10-29",
        "completion_range_note": "missing-outcome bounds on the planned 48-block estimand; observed partial "
                                 "rounds retained; not confidence intervals and not imputations",
        "registered_welfare": registered_welfare(T),
        "structural_primary": structural_primary(T),
        "descriptive_welfare_deltas_hide_minus_natural": welfare_deltas(T),
        "cells": descriptives(T),
        "correction_note": "The 2026-10-01 result record labelled descriptive_deltas as equal-price "
                           "persistence. They are hide_rival-minus-natural assessment-window welfare deltas "
                           "over complete pairs (reproduced in descriptive_welfare_deltas_hide_minus_natural).",
    }


def welfare_deltas(T: dict) -> dict:
    out = {}
    for init in INITIALS:
        xs = []
        for b in BLOCKS:
            n, h = T[(init, "natural", b)], T[(init, "hide_rival", b)]
            if completed(n) and completed(h):
                xs.append(window_mean(h, wel) - window_mean(n, wel))
        out[init] = {"complete_pairs": len(xs), "delta_mean": mean(xs)}
    return out


def check(result: dict) -> None:
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    for name in ("D_asym", "J"):
        ours, theirs = result["registered_welfare"][name], frozen["primary"][name]
        assert ours["complete_blocks"] == theirs["complete_blocks"], name
        assert abs(ours["mean"] - theirs["mean"]) < 1e-9, name
        assert all(abs(a - b) < 1e-9 for a, b in zip(ours["bonferroni_block_t_95"], theirs["ci"])), name
        rng = ours["completion_range"]["full_grid_welfare_support"]
        assert all(abs(a - b) < 1e-9 for a, b in zip(rng, theirs["planned_completion_range"])), name
    for init, row in frozen["descriptive_deltas"].items():
        ours = result["descriptive_welfare_deltas_hide_minus_natural"][init]
        assert ours["complete_pairs"] == row["complete_pairs"] and abs(ours["delta_mean"] - row["delta_mean"]) < 1e-9, init
    sp = result["structural_primary"]
    assert sp["D_tie"]["complete_blocks"] == result["registered_welfare"]["D_asym"]["complete_blocks"]
    assert 0 <= sp["D_tie"]["completion_range"][0] <= sp["D_tie"]["mean"] <= sp["D_tie"]["completion_range"][1] <= 1
    counts = Counter()
    for cell in result["cells"].values():
        counts["completed"] += cell["completed"]
        counts["failed"] += cell["failed"]
    assert counts == {"completed": 376, "failed": 8}, counts
    # Hide-rival asymmetric cells never reach a tie in the assessment window.
    for cell in ("LH-hide_rival", "HL-hide_rival"):
        assert result["cells"][cell]["assessment_equal_rounds"][0] == 0, cell
    assert abs(t_quantile(0.975, 10) - 2.228138851986) < 1e-9


def fmt_ci(ci: list[float], nd: int = 3) -> str:
    return f"[{ci[0]:.{nd}f}, {ci[1]:.{nd}f}]"


def render_md(r: dict) -> str:
    sp, rw, cells = r["structural_primary"], r["registered_welfare"], r["cells"]
    d = sp["D_tie"]
    lines = [
        "# Candidate A: structural primary and corrected descriptive record (2026-10-01)",
        "",
        "Generated by `tools/candidate_a_structural.py` from the sealed ledger "
        f"`{r['source_ledger']}`. Offline; no provider calls. The frozen "
        "`data/A-confirmation-analysis.json` is read and reproduced, never modified.",
        "",
        "## Structural primary (protocol estimand 1)",
        "",
        "Natural minus hide-rival equal-price fraction over assessment rounds 10--29, "
        "aggregated within trajectory and paired by block.",
        "",
        "| contrast | complete blocks | mean | block-t 95% | bootstrap 95% | + / 0 / − blocks | completion range "
        "| minimum price, natural − hide (block-t 95%) |",
        "|---|---:|---:|---|---|---|---|---|",
    ]
    for init in ("LH", "HL"):
        row = sp[init]
        s = row["signs"]
        mp = row["minimum_price_natural_minus_hide"]
        lines.append(f"| {init} | {row['complete_pairs']} | {row['mean']:.3f} | {fmt_ci(row['block_t_95'])} "
                     f"| {fmt_ci(row['bootstrap_95'])} | {s['positive']} / {s['zero']} / {s['negative']} | — "
                     f"| {mp['mean']:.3f} {fmt_ci(mp['block_t_95'])} |")
    s = d["signs"]
    lines.append(f"| **D_tie** | {d['complete_blocks']} | **{d['mean']:.3f}** | {fmt_ci(d['block_t_95'])} "
                 f"| {fmt_ci(d['bootstrap_95'])} | {s['positive']} / {s['zero']} / {s['negative']} "
                 f"| {fmt_ci(d['completion_range'])} | — |")
    lines += [
        "",
        f"Decision rule (protocol): the 95% interval for D_tie excludes zero in the registered direction, "
        f"subject to the completion-range report. **Structural confirmation: "
        f"{'met' if d['structural_confirmation'] else 'not met'}** — the interval and the full completion "
        "range both lie above zero.",
        "",
        "## Registered welfare contrasts (reproduced exactly)",
        "",
        "| estimand | complete blocks | mean | Bonferroni 95% | completion range, full grid support | completion range, observed run support |",
        "|---|---:|---:|---|---|---|",
    ]
    for name in ("D_asym", "J"):
        row = rw[name]
        cr = row["completion_range"]
        lines.append(f"| {name} | {row['complete_blocks']} | {row['mean']:.4f} | {fmt_ci(row['bonferroni_block_t_95'], 4)} "
                     f"| {fmt_ci(cr['full_grid_welfare_support'], 4)} | {fmt_ci(cr['observed_run_welfare_support'], 4)} |")
    eq5 = {n: rw[n]["equivalence"][str(DELTA_W)] for n in ("D_asym", "J")}
    lines += [
        "",
        f"At the protocol's candidate margin δ_W = {DELTA_W:g}, both observed-complete intervals lie inside "
        f"the margin ({eq5['D_asym']['observed_ci_within_margin']} / {eq5['J']['observed_ci_within_margin']}); "
        "the registered full-support completion range for J does not "
        f"({eq5['J']['registered_completion_range_within_margin']}). The welfare-equivalence decision therefore "
        "remains **inconclusive under the registered missingness sensitivity**. The observed-run-support "
        "column is a post-hoc, non-registered sensitivity that restricts unresolved rounds to the welfare "
        "values observed anywhere in the run; it is reported for transparency and does not change the decision.",
        "",
        "## Correction to the 2026-10-01 result record",
        "",
        r["correction_note"],
        "",
        "| initial | complete pairs | hide − natural welfare delta |",
        "|---|---:|---:|",
    ]
    for init, row in r["descriptive_welfare_deltas_hide_minus_natural"].items():
        lines.append(f"| {init} | {row['complete_pairs']} | {row['delta_mean']:.4f} |")
    lines += [
        "",
        "## Descriptive cell summaries (completed trajectories)",
        "",
        "| cell | completed / failed | round-1 states | assessment equal rounds | first change: high / low seller | tie formation down / up |",
        "|---|---|---|---|---|---|",
    ]
    for name, c in cells.items():
        fc = c["first_change_rate"]
        fc_s = "—" if fc is None else f"{fc['initially_high_seller']:.3f} / {fc['initially_low_seller']:.3f}"
        tf = c["tie_formation_events"]
        r1 = "; ".join(f"{k}: {v}" for k, v in c["round1_states"].items())
        er = c["assessment_equal_rounds"]
        lines.append(f"| {name} | {c['completed']} / {c['failed']} | {r1} | {er[0]}/{er[1]} | {fc_s} | "
                     f"{tf['downward']} / {tf['upward']} |")
    lines += [
        "",
        "Choices after a previous-round rival price of 6.5 are tabulated in the JSON companion by the "
        "seller's own previous price, so continuations of an existing (6.5, 6.5) tie are not counted as "
        "upward moves. In hide-rival arms the conditioning price is not displayed to the seller.",
        "",
        "## Boundary",
        "",
        "Round and seller-round counts are nested within trajectories and are descriptive. The replication "
        "uses the same model alias and returned fingerprint as the original study; it is a within-deployment "
        "replication, not a cross-model test. Nothing here identifies collusion, punishment or T4 strategic "
        "harmful coordination.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="assert reproduction of the frozen analysis")
    parser.add_argument("--write", action="store_true", help="write the analysis/A-confirmation-structural-* files")
    args = parser.parse_args()
    result = build()
    if args.check:
        try:
            check(result)
        except AssertionError as exc:
            print(f"CHECK FAILED: {exc!r}", file=sys.stderr)
            return 1
    if args.write:
        OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        OUT_MD.write_text(render_md(result), encoding="utf-8")
    d = result["structural_primary"]["D_tie"]
    print(json.dumps({"passed": True, "D_tie": d["mean"], "D_tie_ci": d["block_t_95"],
                      "D_tie_completion_range": d["completion_range"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
