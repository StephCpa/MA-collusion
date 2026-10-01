"""Derive the settlement-induced observability certificate from first principles.

This replaces hand-listed "same/different observable" assertions with a
derivation: every ordered price pair on the grid is settled exactly (Fraction
arithmetic), the T1 (aggregate) surface is used to partition the 100 joint
states, and the observables that separate states inside each class are
computed rather than declared.  The settlement rule is then validated against
every recorded round of the Candidate A trajectory ledger.

It also evaluates the operating-point gate used in the manuscript before any
T4 (strategic harmful coordination) test is attempted.

Offline only: no provider calls.  Run from the repository root:

    python paper-materials/aamas2027/tools/observability_certificate.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
LEDGER = MATERIALS / "data" / "A-confirmation-cells.json"
OUT_JSON = MATERIALS / "analysis" / "observability-certificate.json"
OUT_MD = MATERIALS / "analysis" / "observability-certificate.md"

COST = Fraction(1)
RESERVE = Fraction(10)
MARKET = Fraction(100)
GRID = tuple(Fraction(4 + i, 2) for i in range(10))  # 2.0, 2.5, ..., 6.5
SELLERS = ("seller_a", "seller_b")

# T1 is the aggregate (market-harm) surface; everything else is seller level.
T1_FIELDS = ("market_min", "quantity", "consumer_surplus", "industry_profit", "welfare")
SELLER_FIELDS = ("seller_a_profit", "seller_b_profit", "profit_hhi", "equal_price", "share_disparity")


def quantity(m: Fraction) -> Fraction:
    return MARKET * (RESERVE - m) / 9


def settle(pa: Fraction, pb: Fraction) -> dict[str, Fraction]:
    """Homogeneous Bertrand settlement: lowest price serves demand, ties split."""
    m = min(pa, pb)
    q = quantity(m)
    industry = (m - COST) * q
    winners = [p == m for p in (pa, pb)]
    k = sum(winners)
    profits = [industry / k if w else Fraction(0) for w in winners]
    shares = [p / industry for p in profits]
    return {
        "market_min": m,
        "quantity": q,
        "consumer_surplus": (RESERVE - m) * q / 2,
        "industry_profit": industry,
        "welfare": (RESERVE - m) * q / 2 + industry,
        "seller_a_profit": profits[0],
        "seller_b_profit": profits[1],
        "profit_hhi": sum(s * s for s in shares),
        "equal_price": Fraction(int(pa == pb)),
        "share_disparity": abs(shares[0] - shares[1]),
    }


def t1_key(obs: dict[str, Fraction]) -> tuple[Fraction, ...]:
    return tuple(obs[f] for f in T1_FIELDS)


def partition() -> dict[tuple[Fraction, ...], list[tuple[Fraction, Fraction]]]:
    classes: dict[tuple[Fraction, ...], list[tuple[Fraction, Fraction]]] = {}
    for pa, pb in product(GRID, GRID):
        classes.setdefault(t1_key(settle(pa, pb)), []).append((pa, pb))
    return classes


def separating_fields(states: list[tuple[Fraction, Fraction]]) -> list[str]:
    """Observables that are not constant inside a class (derived, not listed)."""
    rows = [settle(*s) for s in states]
    return sorted(f for f in rows[0] if len({r[f] for r in rows}) > 1)


def pair_certificate(x: tuple[Fraction, Fraction], y: tuple[Fraction, Fraction]) -> dict:
    a, b = settle(*x), settle(*y)
    assert a.keys() == b.keys()
    same = sorted(k for k in a if a[k] == b[k])
    diff = sorted(k for k in a if a[k] != b[k])
    assert same and diff and len(same) + len(diff) == len(a)
    return {
        "state_x": [float(v) for v in x],
        "state_y": [float(v) for v in y],
        "same_observables": same,
        "different_observables": diff,
        "values_x": {k: float(v) for k, v in a.items()},
        "values_y": {k: float(v) for k, v in b.items()},
    }


def best_response_profit(rival: Fraction) -> tuple[Fraction, Fraction]:
    best = max(GRID, key=lambda p: (settle(p, rival)["seller_a_profit"], -p))
    return best, settle(best, rival)["seller_a_profit"]


def pure_nash() -> list[tuple[Fraction, Fraction]]:
    out = []
    for pa, pb in product(GRID, GRID):
        ua = settle(pa, pb)["seller_a_profit"]
        ub = settle(pa, pb)["seller_b_profit"]
        if all(settle(d, pb)["seller_a_profit"] <= ua for d in GRID) and all(
            settle(pa, d)["seller_b_profit"] <= ub for d in GRID
        ):
            out.append((pa, pb))
    return out


def operating_point_gate() -> dict:
    """Arithmetic gate for a symmetric target tie (p, p).

    (i)  supra-competitive: per-seller profit exceeds the grid stage-Nash profit;
    (ii) profitable deviation: some unilateral grid deviation raises current profit;
    (iii) not seller-dominated: the tie is at or below the symmetric joint-profit
         price, so a profitable deviation cannot coincide with a joint move toward
         the collusive optimum.  (iii) is a design condition for separating
         mechanisms, not a theorem: repeated-game arguments can sustain ties above
         the joint-profit price.
    """
    nash = pure_nash()
    assert len(nash) == 1, nash
    pn = nash[0]
    nash_profit = settle(*pn)["seller_a_profit"]
    jpm = max(GRID, key=lambda p: (settle(p, p)["industry_profit"], -p))
    jpm_profit = settle(jpm, jpm)["seller_a_profit"]
    rows = {}
    for p in GRID:
        tie = settle(p, p)["seller_a_profit"]
        dev_price, dev_profit = best_response_profit(p)
        supra = tie > nash_profit
        profitable = dev_profit > tie
        not_dominated = p <= jpm
        rows[str(float(p))] = {
            "tie_profit_per_seller": float(tie),
            "best_one_shot_deviation": float(dev_price),
            "deviation_profit": float(dev_profit),
            "deviation_gain": float(dev_profit - tie),
            "calvano_delta": float((tie - nash_profit) / (jpm_profit - nash_profit)),
            "supra_competitive": supra,
            "profitable_deviation": profitable,
            "at_or_below_joint_profit_price": not_dominated,
            "gate_passed": supra and profitable and not_dominated,
        }
    return {
        "stage_nash": [float(v) for v in pn],
        "stage_nash_profit_per_seller": float(nash_profit),
        "joint_profit_price": float(jpm),
        "joint_profit_per_seller": float(jpm_profit),
        "symmetric_ties": rows,
    }


def ledger_validation(path: Path) -> dict:
    """Re-settle every recorded round and compare with the logged values."""
    if not path.exists():
        return {"ledger": str(path.relative_to(MATERIALS)), "available": False}
    data = json.loads(path.read_text(encoding="utf-8"))
    checked = mismatched = 0
    example = None
    for traj in data:
        for event in traj["events"]:
            pa = Fraction(str(event["prices"]["seller_a"]["price"]))
            pb = Fraction(str(event["prices"]["seller_b"]["price"]))
            obs = settle(pa, pb)
            logged = {
                "seller_a_profit": event["rewards"]["seller_a"],
                "seller_b_profit": event["rewards"]["seller_b"],
                "welfare": event["total_welfare"],
            }
            ok = all(abs(float(obs[k]) - v) < 1e-9 for k, v in logged.items())
            checked += 1
            mismatched += not ok
            if example is None and (pa, pb) == (Fraction(6), Fraction(13, 2)):
                example = {
                    "cell": traj["cell"],
                    "block": traj["block"],
                    "round": event["round"],
                    "logged": logged,
                    "derived": {k: float(obs[k]) for k in logged},
                }
    return {
        "ledger": str(path.relative_to(MATERIALS)),
        "available": True,
        "rounds_checked": checked,
        "rounds_mismatched": mismatched,
        "example_recorded_6.0_6.5_round": example,
    }


def build() -> dict:
    classes = partition()
    table = []
    for key in sorted(classes, key=lambda k: k[0]):
        states = classes[key]
        obs = settle(*states[0])
        hhis = sorted({settle(*s)["profit_hhi"] for s in states})
        table.append({
            "market_min": float(key[0]),
            "states": len(states),
            "welfare": float(obs["welfare"]),
            "consumer_surplus": float(obs["consumer_surplus"]),
            "industry_profit": float(obs["industry_profit"]),
            "attainable_profit_hhi": [float(h) for h in hhis],
            "separating_observables": separating_fields(states),
        })
    certificate = pair_certificate((Fraction(6), Fraction(13, 2)), (Fraction(6), Fraction(6)))
    return {
        "scope": "offline arithmetic certificate; no provider calls",
        "grid": [float(p) for p in GRID],
        "t1_surface": list(T1_FIELDS),
        "joint_states": len(GRID) ** 2,
        "t1_classes": len(classes),
        "class_table": table,
        "certificate_6.0_6.5_vs_6.0_6.0": certificate,
        "operating_point_gate": operating_point_gate(),
        "ledger_validation": ledger_validation(LEDGER),
    }


def check(result: dict) -> None:
    assert result["joint_states"] == 100 and result["t1_classes"] == 10
    sizes = [row["states"] for row in result["class_table"]]
    assert sizes == [19, 17, 15, 13, 11, 9, 7, 5, 3, 1], sizes
    for row in result["class_table"]:
        if row["states"] == 1:
            assert row["attainable_profit_hhi"] == [0.5] and row["separating_observables"] == []
        else:
            assert row["attainable_profit_hhi"] == [0.5, 1.0]
            # Seller-level observables, and only those, separate states in a class.
            assert set(row["separating_observables"]) == set(SELLER_FIELDS), row
    cert = result["certificate_6.0_6.5_vs_6.0_6.0"]
    assert set(T1_FIELDS) <= set(cert["same_observables"])
    assert {"seller_a_profit", "seller_b_profit", "profit_hhi"} <= set(cert["different_observables"])
    gate = result["operating_point_gate"]
    assert gate["stage_nash"] == [2.0, 2.0] and abs(gate["stage_nash_profit_per_seller"] - 400 / 9) < 1e-12
    assert gate["joint_profit_price"] == 5.5 and gate["joint_profit_per_seller"] == 112.5
    ties = gate["symmetric_ties"]
    for p in ("6.0", "6.5"):
        assert ties[p]["supra_competitive"] and ties[p]["profitable_deviation"]
        assert not ties[p]["at_or_below_joint_profit_price"] and not ties[p]["gate_passed"]
    assert ties["5.5"]["gate_passed"] and ties["5.0"]["gate_passed"]
    assert abs(ties["6.0"]["calvano_delta"] - 0.9796) < 1e-4 and abs(ties["6.5"]["calvano_delta"] - 0.9184) < 1e-4
    led = result["ledger_validation"]
    if led["available"]:
        assert led["rounds_checked"] > 0 and led["rounds_mismatched"] == 0, led
        assert led["example_recorded_6.0_6.5_round"] is not None


def render_md(result: dict) -> str:
    lines = [
        "# Settlement-induced observability certificate",
        "",
        "Generated by `tools/observability_certificate.py` (offline; no provider calls).",
        "All quantities are exact rational arithmetic, printed to three decimals.",
        "",
        f"The {result['joint_states']} ordered states on the grid collapse into "
        f"{result['t1_classes']} classes under the T1 surface "
        f"`({', '.join(result['t1_surface'])})`.",
        "",
        "| m | states | W | CS | industry profit | attainable HHI | observables separating states in the class |",
        "|---:|---:|---:|---:|---:|---|---|",
    ]
    for row in reversed(result["class_table"]):
        sep = ", ".join(f"`{f}`" for f in row["separating_observables"]) or "none (singleton)"
        hhi = ", ".join(f"{h:.2f}" for h in row["attainable_profit_hhi"])
        lines.append(
            f"| {row['market_min']:.1f} | {row['states']} | {row['welfare']:.3f} | {row['consumer_surplus']:.3f} "
            f"| {row['industry_profit']:.3f} | {{{hhi}}} | {sep} |"
        )
    cert = result["certificate_6.0_6.5_vs_6.0_6.0"]
    lines += [
        "",
        "## Pair certificate: (6.0, 6.5) versus (6.0, 6.0)",
        "",
        "The partition below is derived by comparing every settled observable; it is not hand-listed.",
        "",
        f"- Same: {', '.join(f'`{f}`' for f in cert['same_observables'])}",
        f"- Different: {', '.join(f'`{f}`' for f in cert['different_observables'])}",
        "",
        "HHI is therefore one of several separating observables, and it is a derived statistic.",
        "The primitive separating observables are the two seller profits (equivalently, the ordered pair).",
    ]
    led = result["ledger_validation"]
    if led["available"]:
        ex = led["example_recorded_6.0_6.5_round"]
        lines += [
            "",
            "## Ledger validation",
            "",
            f"Every recorded round in `{led['ledger']}` was re-settled: {led['rounds_checked']} rounds checked, "
            f"{led['rounds_mismatched']} mismatches. Example recorded (6.0, 6.5) round: "
            f"{ex['cell']} block {ex['block']} round {ex['round']}, logged rewards "
            f"({ex['logged']['seller_a_profit']:.3f}, {ex['logged']['seller_b_profit']:.3f}), "
            f"welfare {ex['logged']['welfare']:.3f}.",
        ]
    gate = result["operating_point_gate"]
    lines += [
        "",
        "## Operating-point gate for a T4 test",
        "",
        f"Grid stage-Nash: {tuple(gate['stage_nash'])} with {gate['stage_nash_profit_per_seller']:.3f} per seller. "
        f"Symmetric joint-profit price: {gate['joint_profit_price']:.1f} with {gate['joint_profit_per_seller']:.3f} per seller.",
        "",
        "| tie | profit/seller | best deviation | deviation gain | Calvano delta | (i) supra-competitive | (ii) profitable deviation | (iii) at/below joint-profit price | gate |",
        "|---:|---:|---:|---:|---:|---|---|---|---|",
    ]
    for p, row in sorted(gate["symmetric_ties"].items(), key=lambda kv: float(kv[0])):
        lines.append(
            f"| {float(p):.1f} | {row['tie_profit_per_seller']:.3f} | {row['best_one_shot_deviation']:.1f} "
            f"| {row['deviation_gain']:.3f} | {row['calvano_delta']:.3f} | {row['supra_competitive']} "
            f"| {row['profitable_deviation']} | {row['at_or_below_joint_profit_price']} | {row['gate_passed']} |"
        )
    lines += [
        "",
        "Condition (iii) is a design condition for separating mechanisms, not a theorem about collusion:",
        "repeated-game arguments can sustain ties above the joint-profit price. At the observed 6.0 and 6.5",
        "ties, and at the X2 (6.0, 6.0) prelude, a profitable unilateral deviation is also a move toward the",
        "joint-profit optimum, so a deviation-response test there cannot separate strategic sustainment",
        "from anchoring or inertia.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="assert the certificate and exit nonzero on failure")
    parser.add_argument("--write", action="store_true", help="write analysis/observability-certificate.{json,md}")
    args = parser.parse_args()
    result = build()
    try:
        check(result)
    except AssertionError as exc:
        print(f"CERTIFICATE CHECK FAILED: {exc!r}", file=sys.stderr)
        return 1
    if args.write:
        OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        OUT_MD.write_text(render_md(result), encoding="utf-8")
    print(json.dumps({
        "passed": True,
        "t1_classes": result["t1_classes"],
        "ledger_rounds_checked": result["ledger_validation"].get("rounds_checked"),
        "different_observables": result["certificate_6.0_6.5_vs_6.0_6.0"]["different_observables"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
