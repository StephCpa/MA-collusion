"""How much does a welfare-only monitor miss under other settlement rules?

Two offline generalisations of the observability certificate, both on the
manuscript's grid {2.0, ..., 6.5}, cost 1 and linear demand Q(p) = 100(10-p)/9:

1. More sellers (N = 2, 3, 4) in homogeneous Bertrand.  States are ordered
   price vectors; welfare depends only on the minimum price, and the
   allocation is the seller-profit vector.  We count welfare classes and the
   share of allocation-distinct state pairs that welfare cannot separate.

2. Captive consumers (N = 2).  A share theta of the market is captive to each
   seller and buys at that seller's price; the remaining 1 - 2 theta are
   shoppers who buy from the cheapest seller (ties split), as in shopper/loyal
   models of price dispersion.  theta = 0 is exactly the manuscript's
   settlement.  Welfare is then
       W(pA, pB) = (1 - 2 theta) W(min) + theta W(pA) + theta W(pB),
   so welfare starts to separate tie and capture states.  For a monitor that
   resolves welfare only to a relative tolerance eps, we report the share of
   allocation-distinct pairs it still cannot separate.

The blind share is (allocation-distinct pairs with |dW| <= eps * mean W) /
(allocation-distinct pairs), under a uniform distribution over ordered states.
Offline; no provider calls.

    python paper-materials/aamas2027/tools/settlement_generalization.py --check --write
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
OUT_JSON = MATERIALS / "analysis" / "settlement-generalization-20261001.json"
OUT_MD = MATERIALS / "analysis" / "settlement-generalization-20261001.md"

GRID = tuple(Fraction(4 + i, 2) for i in range(10))
THETAS = (0.0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4)
EPSILONS = (0.0, 0.001, 0.01, 0.05)


def W(p: Fraction) -> Fraction:
    q = 100 * (10 - p) / 9
    return (10 - p) * q / 2 + (p - 1) * q


def industry_profit(p: Fraction) -> Fraction:
    return (p - 1) * 100 * (10 - p) / 9


# ---------------------------------------------------------------- N sellers
def n_seller_counts(n: int) -> dict:
    groups: Counter = Counter()      # (welfare class, allocation) -> states
    welfare_classes: Counter = Counter()
    allocations: Counter = Counter()
    hhi_values: dict[Fraction, set] = {}
    for prices in product(GRID, repeat=n):
        m = min(prices)
        winners = tuple(p == m for p in prices)
        k = sum(winners)
        alloc = tuple(industry_profit(m) / k if w else Fraction(0) for w in winners)
        groups[(m, alloc)] += 1
        welfare_classes[m] += 1
        allocations[alloc] += 1
        hhi_values.setdefault(m, set()).add(Fraction(1, k))
    states = len(GRID) ** n
    alloc_distinct = comb(states, 2) - sum(comb(c, 2) for c in allocations.values())
    blind = sum(comb(c, 2) for c in welfare_classes.values()) - sum(comb(c, 2) for c in groups.values())
    return {
        "sellers": n,
        "ordered_states": states,
        "welfare_classes": len(welfare_classes),
        "largest_class": max(welfare_classes.values()),
        "attainable_hhi_in_bottom_class": sorted(float(h) for h in hhi_values[min(GRID)]),
        "allocation_distinct_pairs": alloc_distinct,
        "welfare_blind_allocation_distinct_pairs": blind,
        "blind_share": blind / alloc_distinct,
    }


# ---------------------------------------------------------------- captive consumers
def captive_state(pa: Fraction, pb: Fraction, theta: Fraction) -> tuple[Fraction, tuple[Fraction, Fraction]]:
    m = min(pa, pb)
    shoppers = 1 - 2 * theta
    welfare = shoppers * W(m) + theta * W(pa) + theta * W(pb)
    k = (pa == m) + (pb == m)
    shop = [shoppers * industry_profit(m) / k if p == m else Fraction(0) for p in (pa, pb)]
    profits = (shop[0] + theta * industry_profit(pa), shop[1] + theta * industry_profit(pb))
    return welfare, profits


def captive_blindness(theta_f: float) -> dict:
    """Tie versus capture at the same minimum price: can a welfare monitor tell them apart?

    The fixed comparison set is every pair {(m, m), (m, p)} or {(m, m), (p, m)} with p > m
    (90 pairs on this grid): the T3b-versus-T3a distinction at equal minimum price.  A pair
    is blind at resolution eps if |W(tie) - W(capture)| <= eps * W(tie).
    """
    theta = Fraction(theta_f).limit_denominator(1000)
    pairs = []
    for m in GRID:
        for p in GRID:
            if p > m:
                pairs += [((m, m), (m, p)), ((m, m), (p, m))]
    out = {"theta": float(theta), "tie_capture_pairs": len(pairs), "by_epsilon": {}}
    for eps in EPSILONS:
        e = Fraction(eps).limit_denominator(100000)
        blind = 0
        for tie, cap in pairs:
            w_tie = captive_state(*tie, theta)[0]
            if abs(w_tie - captive_state(*cap, theta)[0]) <= e * w_tie:
                blind += 1
        out["by_epsilon"][str(eps)] = blind / len(pairs)
    w_tie, _ = captive_state(Fraction(6), Fraction(6), theta)
    w_cap, _ = captive_state(Fraction(6), Fraction(13, 2), theta)
    out["tie_vs_capture_6.0_relative_welfare_gap"] = float((w_tie - w_cap) / w_tie)
    # Mirror states (pA, pB) and (pB, pA) always share welfare but swap the profit vector.
    mirror_same = all(captive_state(a, b, theta)[0] == captive_state(b, a, theta)[0]
                      for a, b in product(GRID, GRID) if a != b)
    out["mirror_states_always_welfare_equal"] = mirror_same
    return out


def build() -> dict:
    sellers = [n_seller_counts(n) for n in (2, 3, 4)]
    captive = [captive_blindness(t) for t in THETAS]
    gap_unit = float((W(Fraction(6)) - W(Fraction(13, 2))) / W(Fraction(6)))
    return {
        "scope": "offline arithmetic; no provider calls",
        "grid": [float(p) for p in GRID],
        "n_sellers_homogeneous_bertrand": sellers,
        "captive_consumers_duopoly": captive,
        "theta_needed_to_resolve_tie_vs_capture": {
            str(eps): (eps / gap_unit if eps > 0 else 0.0) for eps in EPSILONS
        },
    }


def check(r: dict) -> None:
    two = r["n_sellers_homogeneous_bertrand"][0]
    assert two["ordered_states"] == 100 and two["welfare_classes"] == 10 and two["largest_class"] == 19
    three = r["n_sellers_homogeneous_bertrand"][1]
    assert three["welfare_classes"] == 10 and three["largest_class"] == 271
    assert three["attainable_hhi_in_bottom_class"] == [1 / 3, 0.5, 1.0]
    shares = [row["blind_share"] for row in r["n_sellers_homogeneous_bertrand"]]
    assert shares == sorted(shares), "blind share should not fall as sellers are added"
    rows = r["captive_consumers_duopoly"]
    assert rows[0]["theta"] == 0.0 and all(v == 1.0 for v in rows[0]["by_epsilon"].values())
    assert all(row["by_epsilon"]["0.0"] == 0.0 for row in rows[1:])
    for eps in ("0.001", "0.01", "0.05"):
        col = [row["by_epsilon"][eps] for row in rows]
        assert col == sorted(col, reverse=True), (eps, col)
    assert all(row["mirror_states_always_welfare_equal"] for row in rows)


def render_md(r: dict) -> str:
    lines = [
        "# Settlement generalization: what a welfare-only monitor misses (2026-10-01)",
        "",
        "Generated by `tools/settlement_generalization.py`; exact arithmetic, offline. Blind share = share of "
        "allocation-distinct pairs of ordered states that a welfare monitor cannot separate (uniform over states).",
        "",
        "## More sellers, homogeneous Bertrand",
        "",
        "| sellers | ordered states | welfare classes | largest class | HHI values in bottom class | blind share |",
        "|---:|---:|---:|---:|---|---:|",
    ]
    for row in r["n_sellers_homogeneous_bertrand"]:
        hhi = ", ".join(f"{h:.2f}" for h in row["attainable_hhi_in_bottom_class"])
        lines.append(f"| {row['sellers']} | {row['ordered_states']:,} | {row['welfare_classes']} | {row['largest_class']:,} | "
                     f"{{{hhi}}} | {row['blind_share']:.3f} |")
    lines += [
        "",
        "The number of welfare classes stays at 10 while the state space grows as 10^N, so the share of "
        "allocation differences invisible to welfare grows with the number of sellers.",
        "",
        "## Captive consumers (duopoly)",
        "",
        "Fixed comparison set: the 90 tie-versus-capture pairs at equal minimum price (T3b versus T3a). "
        "Entries are the share of those pairs a welfare monitor with relative resolution ε cannot separate.",
        "",
        "| captive share θ per seller | exact welfare | ε = 0.1% | ε = 1% | ε = 5% | (6.0,6.0) vs (6.0,6.5) welfare gap |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for row in r["captive_consumers_duopoly"]:
        b = row["by_epsilon"]
        lines.append(f"| {row['theta']:.2f} | {b['0.0']:.3f} | {b['0.001']:.3f} | {b['0.01']:.3f} | {b['0.05']:.3f} | "
                     f"{100 * row['tie_vs_capture_6.0_relative_welfare_gap']:.2f}% |")
    th = r["theta_needed_to_resolve_tie_vs_capture"]

    def need(eps: str) -> str:
        # Two captive groups cannot exceed the whole market, so theta <= 0.5.
        return f"θ ≥ {th[eps]:.2f}" if th[eps] <= 0.5 else "a captive share above the feasible maximum of 0.5"

    lines += [
        "",
        "θ = 0 is the manuscript's settlement. Exact welfare separates tie and capture states as soon as "
        "θ > 0, but a monitor with finite resolution does not: the (6.0, 6.0) versus (6.0, 6.5) gap equals "
        f"θ × {100 * r['captive_consumers_duopoly'][1]['tie_vs_capture_6.0_relative_welfare_gap'] / 0.01:.2f}% "
        f"of welfare, so a monitor resolving 1% needs {need('0.01')} to see it, and one resolving 5% would "
        f"need {need('0.05')}.",
        "",
        "Homogeneous Bertrand is therefore the extreme case, not a special one: the blind spot shrinks with "
        "differentiation but persists for any monitor whose welfare resolution is coarser than the "
        "allocation-driven welfare differences. One part never shrinks: welfare is symmetric in seller "
        "identity, so mirror states (pA, pB) and (pB, pA) always have equal welfare and swapped profits; "
        "a welfare monitor can never tell which seller captured the market.",
        "",
    ]
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
        OUT_JSON.write_text(json.dumps(r, indent=2) + "\n", encoding="utf-8")
        OUT_MD.write_text(render_md(r), encoding="utf-8")
    print(render_md(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
