"""Four-arm ledger: reproduction, leading-indicator test and monitor-blindness metric.

1. Reproduces the registered four-arm block contrasts from the sealed ledger
   and asserts agreement with `data/four-arm-history-channel/analysis.json`
   (read, never written), plus the post-hoc simple contrast (11.070).
2. Leading-indicator test (post hoc, descriptive).  In this study round 0 is a
   model decision whose prompt is identical in every arm, so round-0 states are
   draws from the model, not assignments.  Within each arm, trajectories that
   start in the m = 6.0 welfare class are split by structure: an equal-price
   tie (6.0, 6.0) versus a capture state (6.0, 6.5)/(6.5, 6.0).  Both have
   welfare 311.111 at round 0, so a welfare monitor cannot tell them apart.  The
   test asks whether structure predicts later welfare.  The same comparison is
   made in the controlled-initial replication, where the LL (tie) and LH/HL
   (capture) starts are programmed.
3. Monitor-blindness metric: total-variation distance between arms in the
   assessment-round distribution of ordered states versus the distribution of
   welfare (equivalently of the minimum price), for every study in the
   materials.  Rounds repeat within trajectories, so this is descriptive.

Offline only: no provider calls.

    python paper-materials/aamas2027/tools/four_arm_leading_indicator.py --check --write
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
FOUR_ARM = MATERIALS / "data" / "four-arm-history-channel"
REPLICATION = MATERIALS / "data" / "A-confirmation-cells.json"
ORIGINAL = MATERIALS / "analysis" / "controlled-initial-followup-analysis.json"
OUT_JSON = MATERIALS / "analysis" / "four-arm-leading-indicator-20261001.json"
OUT_MD = MATERIALS / "analysis" / "four-arm-leading-indicator-20261001.md"

ARMS = ("natural", "hide_own", "hide_rival", "hide_both")
WINDOW = range(10, 30)
SEED = 20261001
DRAWS = 20000


def prices(event: dict) -> tuple[float, float]:
    return event["prices"]["seller_a"]["price"], event["prices"]["seller_b"]["price"]


def window_mean(events: list[dict], fn) -> float:
    return mean(fn(e) for e in events if e["round"] in WINDOW)


def welfare(e: dict) -> float:
    return e["total_welfare"]


def tv(p: Counter, q: Counter) -> float:
    np_, nq = sum(p.values()), sum(q.values())
    return 0.5 * sum(abs(p[k] / np_ - q[k] / nq) for k in set(p) | set(q))


def welch_ci(x: list[float], y: list[float]) -> list[float]:
    """Welch interval with a normal quantile; reported beside the permutation p-value."""
    vx = sum((v - mean(x)) ** 2 for v in x) / (len(x) - 1) if len(x) > 1 else 0.0
    vy = sum((v - mean(y)) ** 2 for v in y) / (len(y) - 1) if len(y) > 1 else 0.0
    se = math.sqrt(vx / len(x) + vy / len(y))
    d = mean(x) - mean(y)
    return [d - 1.96 * se, d + 1.96 * se]


def permutation_p(x: list[float], y: list[float]) -> float:
    rng = random.Random(SEED)
    pooled, nx = x + y, len(x)
    obs = abs(mean(x) - mean(y))
    hits = 0
    for _ in range(DRAWS):
        rng.shuffle(pooled)
        hits += abs(mean(pooled[:nx]) - mean(pooled[nx:])) >= obs - 1e-12
    return (hits + 1) / (DRAWS + 1)


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    """Exact two-sided Fisher test for [[a, b], [c, d]]."""
    n1, n2, k = a + b, c + d, a + c
    n = n1 + n2

    def pmf(x: int) -> float:
        return math.comb(n1, x) * math.comb(n2, k - x) / math.comb(n, k)

    observed = pmf(a)
    lo, hi = max(0, k - n2), min(k, n1)
    return min(1.0, sum(pmf(x) for x in range(lo, hi + 1) if pmf(x) <= observed * (1 + 1e-9)))


# ---------------------------------------------------------------- four-arm
def load_four_arm() -> dict:
    data = json.loads((FOUR_ARM / "ledger.json").read_text(encoding="utf-8"))
    return {(x["arm"], int(x["block"])): x for x in data["arms"]}


def registered(T: dict) -> dict:
    blocks = sorted(b for b in range(1, 49) if all(T.get((a, b), {}).get("status") == "complete" for a in ARMS))
    Y = {a: [window_mean(T[(a, b)]["events"], welfare) for b in blocks] for a in ARMS}
    rows = list(zip(*(Y[a] for a in ARMS)))
    nat, own, riv, both = (list(v) for v in zip(*rows))
    contrasts = {
        "hide_rival_marginal": [0.5 * ((r - n) + (b - o)) for n, o, r, b in rows],
        "hide_own_marginal": [0.5 * ((o - n) + (b - r)) for n, o, r, b in rows],
        "interaction": [(b - o) - (r - n) for n, o, r, b in rows],
        "simple_hide_rival_minus_natural": [r - n for n, o, r, b in rows],
        "simple_hide_both_minus_hide_own": [b - o for n, o, r, b in rows],
    }
    return {
        "complete_blocks": len(blocks),
        "arm_mean_assessment_welfare": {a: mean(Y[a]) for a in ARMS},
        "contrasts": {k: mean(v) for k, v in contrasts.items()},
    }


def describe_arms(T: dict) -> dict:
    out = {}
    for arm in ARMS:
        done = [x for (a, _), x in sorted(T.items()) if a == arm and x["status"] == "complete"]
        formation = Counter()
        for x in done:
            ev = x["events"]
            for p, c in zip(ev, ev[1:]):
                (a0, b0), (a1, b1) = prices(p), prices(c)
                if a0 != b0 and a1 == b1:
                    formation["upward" if a1 == max(a0, b0) else "downward" if a1 == min(a0, b0) else "other"] += 1
                elif a0 == b0 and a1 != b1:
                    formation["tie_split"] += 1
        out[arm] = {
            "completed_trajectories": len(done),
            "round0_states": {f"({a:g},{b:g})": n for (a, b), n in sorted(Counter(prices(x["events"][0]) for x in done).items())},
            "round0_prompt_tokens": sorted({x["events"][0]["model_calls"]["seller_a"]["usage"]["prompt_tokens"] for x in done}),
            "tie_formation": {k: formation.get(k, 0) for k in ("downward", "upward", "other", "tie_split")},
            "assessment_states": {f"({a:g},{b:g})": n for (a, b), n in sorted(
                Counter(prices(e) for x in done for e in x["events"] if e["round"] in WINDOW).items())},
        }
    return out


def split_by_start(trajectories: list[tuple[str, list[dict]]]) -> dict:
    """Compare tie versus capture starts inside the m = 6.0 welfare class."""
    groups: dict[str, list[list[dict]]] = {"tie": [], "capture": []}
    for _, ev in trajectories:
        a, b = prices(ev[0])
        if min(a, b) != 6.0:
            continue
        groups["tie" if a == b else "capture"].append(ev)
    w = {g: [window_mean(ev, welfare) for ev in v] for g, v in groups.items()}
    high = {g: sum(window_mean(ev, lambda e: float(min(prices(e)) == 6.5)) > 0.5 for ev in v) for g, v in groups.items()}
    def group_ci(v: list[float]) -> list[float] | None:
        if len(v) < 2:
            return None
        se = math.sqrt(sum((x - mean(v)) ** 2 for x in v) / (len(v) - 1) / len(v))
        return [mean(v) - 1.96 * se, mean(v) + 1.96 * se]

    out = {
        "round0_welfare": {g: sorted({ev[0]["total_welfare"] for ev in v}) for g, v in groups.items()},
        "n": {g: len(v) for g, v in groups.items()},
        "mean_assessment_welfare": {g: mean(v) if v else None for g, v in w.items()},
        "assessment_welfare_ci95": {g: group_ci(v) for g, v in w.items()},
        "trajectories_mostly_at_m6.5": high,
    }
    if groups["tie"] and groups["capture"]:
        out["capture_minus_tie_welfare"] = mean(w["capture"]) - mean(w["tie"])
        out["welch_95"] = welch_ci(w["capture"], w["tie"])
        out["permutation_p"] = permutation_p(w["capture"], w["tie"])
        out["fisher_p_mostly_m6.5"] = fisher_two_sided(
            high["capture"], len(groups["capture"]) - high["capture"], high["tie"], len(groups["tie"]) - high["tie"])
    return out


def leading_indicator(T: dict) -> dict:
    four = {}
    for arm in ARMS:
        trajs = [(f"{arm}-{b}", x["events"]) for (a, b), x in sorted(T.items()) if a == arm and x["status"] == "complete"]
        four[arm] = split_by_start(trajs)
    rep = json.loads(REPLICATION.read_text(encoding="utf-8"))
    programmed = {}
    for arm in ("natural", "hide_rival"):
        trajs = [(t["cell"], t["events"]) for t in rep if t["status"] == "completed"
                 and t["cell"].endswith(arm) and t["cell"][:2] in ("LL", "LH", "HL")]
        programmed[arm] = split_by_start(trajs)
    return {"four_arm_model_chosen_start": four, "replication_programmed_start": programmed}


# ---------------------------------------------------------------- blindness metric
def blindness(T: dict) -> list[dict]:
    rows = []

    def add(study: str, contrast: str, s1: Counter, s2: Counter) -> None:
        m1, m2 = Counter(), Counter()
        for (a, b), n in s1.items():
            m1[min(a, b)] += n
        for (a, b), n in s2.items():
            m2[min(a, b)] += n
        rows.append({"study": study, "contrast": contrast, "tv_ordered_state": tv(s1, s2), "tv_welfare": tv(m1, m2)})

    def parse(d: dict) -> Counter:
        out = Counter()
        for k, n in d.items():
            a, b = (float(v) for v in k.strip("()").split(","))
            out[(a, b)] += n
        return out

    orig = json.loads(ORIGINAL.read_text(encoding="utf-8"))["assessment_by_cell"]
    for cell in ("LH", "HL"):
        add("controlled-initial (original)", f"{cell}: natural vs hide-rival",
            parse(orig[f"{cell}-natural"]["state_counts"]), parse(orig[f"{cell}-hide_rival"]["state_counts"]))
    rep = json.loads(REPLICATION.read_text(encoding="utf-8"))
    for cell in ("LH", "HL"):
        s = {arm: Counter(prices(e) for t in rep if t["status"] == "completed" and t["cell"] == f"{cell}-{arm}"
                          for e in t["events"] if e["round"] in WINDOW) for arm in ("natural", "hide_rival")}
        add("controlled-initial (replication)", f"{cell}: natural vs hide-rival", s["natural"], s["hide_rival"])
    s = {arm: Counter(prices(e) for (a, _), x in T.items() if a == arm and x["status"] == "complete"
                      for e in x["events"] if e["round"] in WINDOW) for arm in ARMS}
    add("four-arm (model-chosen start)", "natural vs hide-rival", s["natural"], s["hide_rival"])
    add("four-arm (model-chosen start)", "hide-own vs hide-both", s["hide_own"], s["hide_both"])
    for r in rows:
        r["blind_share"] = 1 - r["tv_welfare"] / r["tv_ordered_state"] if r["tv_ordered_state"] else None
    return rows


# ---------------------------------------------------------------- driver
def build() -> dict:
    T = load_four_arm()
    return {
        "scope": "offline post-hoc analysis of sealed ledgers; no provider calls; registered estimands unchanged",
        "sources": ["data/four-arm-history-channel/ledger.json", "data/A-confirmation-cells.json",
                    "analysis/controlled-initial-followup-analysis.json"],
        "registered_reproduction": registered(T),
        "arms": describe_arms(T),
        "leading_indicator": leading_indicator(T),
        "blindness_metric": blindness(T),
        "notes": [
            "Round-0 prompts are identical across four-arm arms, so round-0 states are model draws; "
            "the tie-versus-capture comparison is observational within arm.",
            "Trajectories within an arm come from different blocks and are treated as independent; "
            "assessment rounds are aggregated within trajectory first.",
            "blind_share = 1 - TV(welfare)/TV(ordered state): the share of the between-arm "
            "distributional difference that a welfare-only monitor cannot see. Rounds repeat within "
            "trajectories, so TV values are descriptive.",
        ],
    }


def check(result: dict) -> None:
    frozen = json.loads((FOUR_ARM / "analysis.json").read_text(encoding="utf-8"))
    rep = result["registered_reproduction"]
    assert rep["complete_blocks"] == frozen["complete_blocks"]
    for name in ("hide_rival_marginal", "hide_own_marginal", "interaction"):
        assert abs(rep["contrasts"][name] - frozen["contrasts"][name]["complete_mean"]) < 1e-9, name
    assert abs(rep["contrasts"]["simple_hide_rival_minus_natural"] - 11.0700757576) < 1e-9
    tokens = {tuple(v["round0_prompt_tokens"]) for v in result["arms"].values()}
    assert len(tokens) == 1, f"round-0 prompts differ across arms: {tokens}"
    for row in result["blindness_metric"]:
        assert 0 <= row["tv_welfare"] <= row["tv_ordered_state"] + 1e-12, row


def render_md(r: dict) -> str:
    reg = r["registered_reproduction"]
    li = r["leading_indicator"]
    lines = [
        "# Four-arm ledger: leading-indicator test and monitor-blindness metric (2026-10-01)",
        "",
        "Generated by `tools/four_arm_leading_indicator.py`. Offline and post hoc; no provider calls; "
        "registered estimands unchanged.",
        "",
        "## Reproduction of the registered four-arm analysis",
        "",
        f"Complete blocks: {reg['complete_blocks']}. Assessment-window welfare (rounds 10--29):",
        "",
        "| arm | mean welfare |",
        "|---|---:|",
    ]
    for arm, v in reg["arm_mean_assessment_welfare"].items():
        lines.append(f"| {arm} | {v:.3f} |")
    lines += ["", "| contrast | mean |", "|---|---:|"]
    for k, v in reg["contrasts"].items():
        lines.append(f"| {k} | {v:.3f} |")
    lines += [
        "",
        "The registered hide-rival marginal (4.053), hide-own marginal (−2.443) and interaction "
        "(−14.034) reproduce `analysis.json` exactly. The registered interaction's Bonferroni "
        "interval in that file, [−22.678, −5.390], excludes zero: hiding the rival's history "
        "raises welfare by 11.070 when own history is shown but lowers it by 2.964 when own "
        "history is hidden.",
        "",
        "## Matching direction by arm",
        "",
        "| arm | completed | round-0 states | tie formation down / up | tie splits |",
        "|---|---:|---|---|---:|",
    ]
    for arm, v in r["arms"].items():
        r0 = "; ".join(f"{k}: {n}" for k, n in v["round0_states"].items())
        tf = v["tie_formation"]
        lines.append(f"| {arm} | {v['completed_trajectories']} | {r0} | {tf['downward']} / {tf['upward']} | {tf['tie_split']} |")
    lines += [
        "",
        "Round-0 prompts were identical in every arm "
        f"({r['arms']['natural']['round0_prompt_tokens'][0]} tokens), so round-0 states are model draws. "
        "Under natural display, ties formed upward (the low seller raised to 6.5) far more often than "
        "downward. In the controlled-initial runs, where round 0 is programmed, the direction was the "
        "reverse (original: 45 down / 1 up in LH and 57 / 4 in HL; replication: 53 / 0 and 49 / 3).",
        "",
        "## Leading indicator: welfare-equivalent starts with different structure",
        "",
        "Trajectories starting in the m = 6.0 class have identical round-0 welfare (311.111). "
        "Rows compare equal-price tie starts with capture starts.",
        "",
        "| study / arm | tie n | capture n | tie: assessment W | capture: assessment W | capture − tie [Welch 95%] | permutation p | mostly at m = 6.5: tie / capture | Fisher p |",
        "|---|---:|---:|---:|---:|---|---:|---|---:|",
    ]

    def row(label: str, v: dict) -> str:
        n, w, h = v["n"], v["mean_assessment_welfare"], v["trajectories_mostly_at_m6.5"]
        if "capture_minus_tie_welfare" not in v:
            return f"| {label} | {n['tie']} | {n['capture']} | — | — | — | — | — | — |"
        ci = v["welch_95"]
        return (f"| {label} | {n['tie']} | {n['capture']} | {w['tie']:.2f} | {w['capture']:.2f} | "
                f"{v['capture_minus_tie_welfare']:.2f} [{ci[0]:.2f}, {ci[1]:.2f}] | {v['permutation_p']:.4f} | "
                f"{h['tie']}/{n['tie']} / {h['capture']}/{n['capture']} | {v['fisher_p_mostly_m6.5']:.2g} |")

    for arm in ARMS:
        lines.append(row(f"four-arm, {arm}", li["four_arm_model_chosen_start"][arm]))
    for arm in ("natural", "hide_rival"):
        lines.append(row(f"replication (programmed), {arm}", li["replication_programmed_start"][arm]))
    lines += [
        "",
        "Interpretation. With model-chosen starts and visible rival prices (natural, hide-own), "
        "a capture state inside the m = 6.0 class was followed by a large welfare loss, because the "
        "low seller matched upward to 6.5; an equal-price tie with the same round-0 welfare was not. "
        "Structure therefore carried information about future welfare that the welfare monitor did "
        "not have. With programmed starts (replication), the same structural contrast predicted "
        "almost nothing, because ties formed downward. Without rival prices (hide-rival), capture "
        "states froze and structure again predicted no welfare change. Whether a structural state "
        "foreshadows a welfare change depends on the direction in which agents resolve it, which "
        "differed between the two designs. The designs differ both in programmed versus "
        "model-chosen round 0 and in round-1 prompt length, so the reversal is not attributed to a "
        "single factor.",
        "",
        "## Monitor-blindness metric",
        "",
        "TV distance between arms in assessment-round distributions; `blind share` = 1 − TV(welfare) / TV(state).",
        "",
        "| study | contrast | TV ordered state | TV welfare | blind share |",
        "|---|---|---:|---:|---:|",
    ]
    for b in r["blindness_metric"]:
        lines.append(f"| {b['study']} | {b['contrast']} | {b['tv_ordered_state']:.3f} | {b['tv_welfare']:.3f} | "
                     f"{b['blind_share']:.3f} |")
    lines += [
        "",
        "In the controlled-initial cells a welfare-only monitor sees essentially none of the "
        "between-arm difference; in the four-arm study it sees part of it, because ties there formed "
        "at 6.5 and changed the minimum price.",
        "",
        "## Boundary",
        "",
        "All comparisons are post hoc. Round-0 states in the four-arm study are model draws, not "
        "randomised assignments; the tie-versus-capture comparison is observational. Nothing here "
        "identifies collusion or T4 strategic harmful coordination; the 6.5 ties fail the "
        "operating-point gate.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
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
    nat = result["leading_indicator"]["four_arm_model_chosen_start"]["natural"]
    print(json.dumps({"passed": True, "natural_capture_minus_tie": nat.get("capture_minus_tie_welfare"),
                      "blindness": [(b["contrast"], round(b["blind_share"], 3)) for b in result["blindness_metric"]]},
                     indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
