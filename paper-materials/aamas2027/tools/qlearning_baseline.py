"""Classical-agent baseline: tabular Q-learning under the four display arms.

Two Q-learners play the same settlement as the LLM study (grid 2.0..6.5, cost
1, homogeneous Bertrand, linear demand).  The display arm defines the state
each learner conditions on:

    natural     (own last price, rival last price)   100 states
    hide_own    rival last price                      10 states
    hide_rival  own last price                        10 states
    hide_both   a single state                         1 state

Unlike the LLM prompts, a Q-learner always observes its own realised profit
(the reward), so hide_rival here corresponds to "rival price hidden, own
outcome shown" (cell B3 of the feedback-surface protocol), not to the LLM
hide-rival arm exactly.

Learning follows Calvano et al. (2020): alpha = 0.15, delta = 0.95,
epsilon_t = exp(-beta t), Q initialised at the discounted payoff against a
uniformly random rival.  After learning, greedy policies are evaluated:

1. the limit path reached from the final learning state (a deterministic cycle);
2. the four programmed starts of the controlled-initial study (LL, LH, HL, HH),
   30 rounds, assessment rounds 10--29, giving the same structural (equal-price
   fraction) and welfare contrasts as the LLM analysis;
3. a forced-deviation impulse in the style of X2: from the limit path, seller A
   is forced for one period to its static best response; seller B's next price
   and the path back are recorded.  This is the positive control for the X2
   design: the same test applied to an agent class known to learn
   reward-punishment strategies.

Sessions are independent; the session is the unit.  Offline, seeded, no
provider calls.

    python paper-materials/aamas2027/tools/qlearning_baseline.py --write
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
OUT_JSON = MATERIALS / "analysis" / "qlearning-baseline-20261001.json"
OUT_MD = MATERIALS / "analysis" / "qlearning-baseline-20261001.md"

GRID = np.array([2.0 + 0.5 * i for i in range(10)])
A = len(GRID)
ARMS = ("natural", "hide_own", "hide_rival", "hide_both")
N_STATES = {"natural": A * A, "hide_own": A, "hide_rival": A, "hide_both": 1}
STARTS = {"LL": (6.0, 6.0), "LH": (6.0, 6.5), "HL": (6.5, 6.0), "HH": (6.5, 6.5)}
NASH_PROFIT, JPM_PROFIT = 400 / 9, 112.5


def settlement() -> tuple[np.ndarray, np.ndarray]:
    """profit[i, j, k] for seller k when A plays GRID[i] and B plays GRID[j]; welfare[i, j]."""
    profit = np.zeros((A, A, 2))
    welfare = np.zeros((A, A))
    for i, pa in enumerate(GRID):
        for j, pb in enumerate(GRID):
            m = min(pa, pb)
            q = 100 * (10 - m) / 9
            industry = (m - 1) * q
            winners = [pa == m, pb == m]
            for k in range(2):
                profit[i, j, k] = industry / sum(winners) if winners[k] else 0.0
            welfare[i, j] = 0.5 * (10 - m) * q + industry
    return profit, welfare


PROFIT, WELFARE = settlement()
IDX = {round(float(p), 1): i for i, p in enumerate(GRID)}


def state_index(arm: str, own: np.ndarray, rival: np.ndarray) -> np.ndarray:
    if arm == "natural":
        return own * A + rival
    if arm == "hide_own":
        return rival
    if arm == "hide_rival":
        return own
    return np.zeros_like(own)


def learn(arm: str, sessions: int, steps: int, alpha: float, delta: float, beta: float, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    ns = N_STATES[arm]
    # Q0: discounted payoff of each own action against a uniformly random rival.
    q0_a = PROFIT[:, :, 0].mean(axis=1) / (1 - delta)
    q0_b = PROFIT[:, :, 1].mean(axis=0) / (1 - delta)
    Q = np.empty((sessions, 2, ns, A))
    Q[:, 0] = q0_a
    Q[:, 1] = q0_b
    acts = rng.integers(0, A, size=(sessions, 2))
    s_rows = np.arange(sessions)
    stable = np.zeros(sessions, dtype=np.int64)
    last_policy = Q.argmax(-1)
    check_every = 10_000
    chunk = 10_000
    t = 0
    while t < steps:
        n = min(chunk, steps - t)
        explore_u = rng.random((n, sessions, 2))
        random_a = rng.integers(0, A, size=(n, sessions, 2))
        for k in range(n):
            eps = math.exp(-beta * (t + k))
            s = np.stack([state_index(arm, acts[:, 0], acts[:, 1]), state_index(arm, acts[:, 1], acts[:, 0])], axis=1)
            greedy = np.stack([Q[s_rows, 0, s[:, 0]].argmax(-1), Q[s_rows, 1, s[:, 1]].argmax(-1)], axis=1)
            new = np.where(explore_u[k] < eps, random_a[k], greedy)
            r = PROFIT[new[:, 0], new[:, 1]]
            s2 = np.stack([state_index(arm, new[:, 0], new[:, 1]), state_index(arm, new[:, 1], new[:, 0])], axis=1)
            for ag in (0, 1):
                target = r[:, ag] + delta * Q[s_rows, ag, s2[:, ag]].max(-1)
                cur = Q[s_rows, ag, s[:, ag], new[:, ag]]
                Q[s_rows, ag, s[:, ag], new[:, ag]] = cur + alpha * (target - cur)
            acts = new
        t += n
        if t % check_every == 0:
            policy = Q.argmax(-1)
            changed = (policy != last_policy).reshape(sessions, -1).any(axis=1)
            stable = np.where(changed, 0, stable + check_every)
            last_policy = policy
    return {"Q": Q, "last_actions": acts, "stable_periods": stable, "final_epsilon": math.exp(-beta * steps)}


def greedy_step(arm: str, Q: np.ndarray, acts: np.ndarray) -> np.ndarray:
    rows = np.arange(Q.shape[0])
    s = np.stack([state_index(arm, acts[:, 0], acts[:, 1]), state_index(arm, acts[:, 1], acts[:, 0])], axis=1)
    return np.stack([Q[rows, 0, s[:, 0]].argmax(-1), Q[rows, 1, s[:, 1]].argmax(-1)], axis=1)


def limit_cycle(arm: str, Q: np.ndarray, start: np.ndarray, max_len: int = 2000) -> list[list[tuple[int, int]]]:
    """Deterministic greedy dynamics from `start`; return the cycle for each session."""
    cycles = []
    for i in range(Q.shape[0]):
        seen: dict[tuple[int, int], int] = {}
        path = []
        a = start[i:i + 1].copy()
        for step in range(max_len):
            key = (int(a[0, 0]), int(a[0, 1]))
            if key in seen:
                cycles.append(path[seen[key]:])
                break
            seen[key] = step
            path.append(key)
            a = greedy_step(arm, Q[i:i + 1], a)
        else:
            cycles.append(path[-1:])
    return cycles


def summarise_cycles(cycles: list[list[tuple[int, int]]]) -> dict:
    price, tie, wel, gain, lengths = [], [], [], [], []
    for c in cycles:
        lengths.append(len(c))
        price.append(np.mean([(GRID[i] + GRID[j]) / 2 for i, j in c]))
        tie.append(np.mean([i == j for i, j in c]))
        wel.append(np.mean([WELFARE[i, j] for i, j in c]))
        prof = np.mean([PROFIT[i, j].mean() for i, j in c])
        gain.append((prof - NASH_PROFIT) / (JPM_PROFIT - NASH_PROFIT))
    symmetric_points = [c[0] for c in cycles if len(c) == 1 and c[0][0] == c[0][1]]
    return {
        "mean_price": float(np.mean(price)),
        "tie_fraction": float(np.mean(tie)),
        "mean_welfare": float(np.mean(wel)),
        "profit_gain_delta": float(np.mean(gain)),
        "share_fixed_point": float(np.mean([n == 1 for n in lengths])),
        "share_symmetric_fixed_point": len(symmetric_points) / len(cycles),
        "symmetric_fixed_point_prices": {f"{GRID[i]:.1f}": int(sum(1 for p in symmetric_points if p[0] == i))
                                         for i in sorted({p[0] for p in symmetric_points})},
    }


def programmed_starts(arm: str, Q: np.ndarray) -> dict:
    out = {}
    for name, (pa, pb) in STARTS.items():
        acts = np.tile(np.array([IDX[pa], IDX[pb]]), (Q.shape[0], 1))
        eq, mins, wel = [], [], []
        for rnd in range(1, 30):
            acts = greedy_step(arm, Q, acts)
            if rnd >= 10:
                eq.append(acts[:, 0] == acts[:, 1])
                mins.append(np.minimum(GRID[acts[:, 0]], GRID[acts[:, 1]]))
                wel.append(WELFARE[acts[:, 0], acts[:, 1]])
        out[name] = {
            "equal_fraction": np.mean(eq, axis=0),
            "min_price": np.mean(mins, axis=0),
            "welfare": np.mean(wel, axis=0),
        }
    return out


def impulse(arm: str, Q: np.ndarray, cycles: list[list[tuple[int, int]]], horizon: int = 15) -> dict:
    """Force seller A to its static best response for one period from a fixed-point limit state."""
    rows = [i for i, c in enumerate(cycles) if len(c) == 1]
    responses = {"punish": 0, "match": 0, "lower": 0, "unchanged": 0, "raise": 0}
    returned = 0
    gate_rows = 0
    b_drop = []
    for i in rows:
        ia, ib = cycles[i][0]
        best = int(np.argmax(PROFIT[:, ib, 0]))
        if best == ia:
            continue  # already a best response: no profitable deviation to impose
        if ia == ib and 0 < ia <= IDX[5.5]:
            gate_rows += 1
        acts = np.array([[best, ib]])
        nxt = greedy_step(arm, Q[i:i + 1], acts)
        b_next = int(nxt[0, 1])
        if b_next < ib:
            # punish: undercut the deviation price; match: equal it; lower: cut but stay above it.
            responses["punish" if b_next < best else "match" if b_next == best else "lower"] += 1
            b_drop.append(float(GRID[ib] - GRID[b_next]))
        elif b_next == ib:
            responses["unchanged"] += 1
        else:
            responses["raise"] += 1
        a = nxt
        for _ in range(horizon):
            if int(a[0, 0]) == ia and int(a[0, 1]) == ib:
                returned += 1
                break
            a = greedy_step(arm, Q[i:i + 1], a)
    tested = sum(responses.values())
    return {
        "sessions_with_fixed_point_and_profitable_deviation": tested,
        "of_which_gate_passing_symmetric_ties": gate_rows,
        "responder_next_period": responses,
        "share_responder_lowers_price": (responses["punish"] + responses["match"] + responses["lower"]) / tested if tested else None,
        "mean_responder_price_drop": float(np.mean(b_drop)) if b_drop else 0.0,
        "share_return_to_pre_deviation_within_15": returned / tested if tested else None,
    }


def ci(x: np.ndarray) -> list[float]:
    m = float(np.mean(x))
    se = float(np.std(x, ddof=1) / math.sqrt(len(x))) if len(x) > 1 else 0.0
    return [m - 1.96 * se, m + 1.96 * se]


def contrasts(evals: dict) -> dict:
    """Natural minus hide-rival structural contrast and hide-rival minus natural welfare, by start."""
    out = {}
    for name in ("LH", "HL"):
        nat, hid = evals["natural"][name], evals["hide_rival"][name]
        d_eq = nat["equal_fraction"].mean() - hid["equal_fraction"].mean()
        d_w = hid["welfare"].mean() - nat["welfare"].mean()
        se_eq = math.sqrt(nat["equal_fraction"].var(ddof=1) / len(nat["equal_fraction"]) +
                          hid["equal_fraction"].var(ddof=1) / len(hid["equal_fraction"]))
        se_w = math.sqrt(nat["welfare"].var(ddof=1) / len(nat["welfare"]) + hid["welfare"].var(ddof=1) / len(hid["welfare"]))
        out[name] = {
            "equal_fraction_natural_minus_hide": float(d_eq),
            "equal_fraction_95": [float(d_eq - 1.96 * se_eq), float(d_eq + 1.96 * se_eq)],
            "welfare_hide_minus_natural": float(d_w),
            "welfare_95": [float(d_w - 1.96 * se_w), float(d_w + 1.96 * se_w)],
        }
    return out


def run(sessions: int, steps: int, beta: float, seed: int) -> dict:
    result = {"settings": {"sessions_per_arm": sessions, "steps": steps, "alpha": 0.15, "delta": 0.95,
                           "beta": beta, "seed": seed, "grid": GRID.tolist()},
              "arms": {}}
    evals = {}
    for k, arm in enumerate(ARMS):
        t0 = time.time()
        learned = learn(arm, sessions, steps, 0.15, 0.95, beta, seed + k)
        Q = learned["Q"]
        cycles = limit_cycle(arm, Q, learned["last_actions"])
        ev = programmed_starts(arm, Q)
        evals[arm] = ev
        result["arms"][arm] = {
            "final_epsilon": learned["final_epsilon"],
            "share_policy_stable_last_100k": float(np.mean(learned["stable_periods"] >= 100_000)),
            "limit_path": summarise_cycles(cycles),
            "programmed_starts": {n: {kk: {"mean": float(v.mean()), "ci95": ci(v)} for kk, v in d.items()}
                                  for n, d in ev.items()},
            "impulse": impulse(arm, Q, cycles),
            "seconds": round(time.time() - t0, 1),
        }
        print(f"{arm}: done in {result['arms'][arm]['seconds']} s", file=sys.stderr)
    result["contrasts_natural_vs_hide_rival"] = contrasts(evals)
    return result


def render_md(r: dict) -> str:
    s = r["settings"]
    lines = [
        "# Classical-agent baseline: Q-learning under the four display arms (2026-10-01)",
        "",
        f"Generated by `tools/qlearning_baseline.py` (offline, seeded). {s['sessions_per_arm']} independent "
        f"sessions per arm; {s['steps']:,} learning periods; alpha {s['alpha']}, delta {s['delta']}, beta {s['beta']:g}. "
        "Same grid and settlement as the LLM study. A Q-learner always observes its own realised profit, so "
        "its hide-rival arm corresponds to 'rival price hidden, own outcome shown'.",
        "",
        "## Learned play (greedy limit path from the final learning state)",
        "",
        "| arm | policy stable 100k | mean price | tie fraction | welfare | profit gain Δ | fixed point | symmetric fixed points (price: sessions) |",
        "|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for arm, v in r["arms"].items():
        lp = v["limit_path"]
        sym = ", ".join(f"{p}: {n}" for p, n in lp["symmetric_fixed_point_prices"].items()) or "—"
        lines.append(f"| {arm} | {v['share_policy_stable_last_100k']:.2f} | {lp['mean_price']:.2f} | {lp['tie_fraction']:.2f} | "
                     f"{lp['mean_welfare']:.1f} | {lp['profit_gain_delta']:.2f} | {lp['share_fixed_point']:.2f} | {sym} |")
    lines += [
        "",
        "## Programmed starts (controlled-initial analogue, rounds 10--29)",
        "",
        "| arm | start | equal-price fraction | minimum price | welfare |",
        "|---|---|---:|---:|---:|",
    ]
    for arm, v in r["arms"].items():
        for name, d in v["programmed_starts"].items():
            lines.append(f"| {arm} | {name} | {d['equal_fraction']['mean']:.3f} | {d['min_price']['mean']:.3f} | "
                         f"{d['welfare']['mean']:.2f} |")
    lines += ["", "Natural versus hide-rival (sessions independent; normal 95% intervals):", "",
              "| start | equal fraction, natural − hide | welfare, hide − natural |", "|---|---|---|"]
    for name, c in r["contrasts_natural_vs_hide_rival"].items():
        lines.append(f"| {name} | {c['equal_fraction_natural_minus_hide']:.3f} [{c['equal_fraction_95'][0]:.3f}, "
                     f"{c['equal_fraction_95'][1]:.3f}] | {c['welfare_hide_minus_natural']:.2f} "
                     f"[{c['welfare_95'][0]:.2f}, {c['welfare_95'][1]:.2f}] |")
    lines += [
        "",
        "## Forced-deviation impulse (X2-style positive control)",
        "",
        "From each fixed-point limit state where seller A has a profitable deviation, A is forced to its "
        "static best response for one period; seller B's next greedy price is recorded.",
        "",
        "| arm | sessions tested | gate-passing ties | B lowers price | B unchanged | mean B price drop | back to pre-deviation within 15 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for arm, v in r["arms"].items():
        im = v["impulse"]
        rsp = im["responder_next_period"]
        low = im["share_responder_lowers_price"]
        ret = im["share_return_to_pre_deviation_within_15"]
        lines.append(f"| {arm} | {im['sessions_with_fixed_point_and_profitable_deviation']} | "
                     f"{im['of_which_gate_passing_symmetric_ties']} | {'—' if low is None else f'{low:.2f}'} | "
                     f"{rsp['unchanged']} | {im['mean_responder_price_drop']:.2f} | {'—' if ret is None else f'{ret:.2f}'} |")
    nat = r["arms"]["natural"]
    im = nat["impulse"]
    c = r["contrasts_natural_vs_hide_rival"]
    lines += [
        "",
        "## Interpretation",
        "",
        f"- With both prices in the state (natural), Q-learners reached supra-competitive play "
        f"(profit gain Δ = {nat['limit_path']['profit_gain_delta']:.2f}); with only one of them (hide-own: "
        "rival price only; hide-rival: own price only) they converged to the (2.0, 2.0) grid-Nash outcome, "
        "even though they always observe their own profit.",
        f"- For this agent class the display contrast is visible to a welfare monitor: from the LH and HL "
        f"starts, hiding the rival raised welfare by {c['LH']['welfare_hide_minus_natural']:.1f} and "
        f"{c['HL']['welfare_hide_minus_natural']:.1f} units. The LLM's display effect instead stayed inside "
        "a welfare class. Whether display effects are welfare-visible therefore depends on the agent class.",
        f"- Positive control for the X2 design: at natural-display fixed points "
        f"({im['of_which_gate_passing_symmetric_ties']} of {im['sessions_with_fixed_point_and_profitable_deviation']} "
        f"at gate-passing ties), the one-period forced deviation lowered the responder's next price in "
        f"{100 * im['share_responder_lowers_price']:.0f}% of sessions, and "
        f"{100 * im['share_return_to_pre_deviation_within_15']:.0f}% returned to the pre-deviation state "
        "within 15 periods: the punish-and-return pattern reported for Q-learning pricing agents. The test "
        "design detects such a response when the agent has learned one.",
        f"- Caveat: only {100 * nat['share_policy_stable_last_100k']:.0f}% of natural-arm sessions had a greedy "
        "policy unchanged over the last 100,000 periods, so learning had not fully converged everywhere; the "
        "limit-path and impulse results use the final greedy policy.",
        "",
        "## Boundary",
        "",
        "This is a simulation baseline, not evidence about the LLM. It shows what the same "
        "settlement, display arms and tests produce for an agent class with known learning dynamics.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    # Keep diagnostics printable on Windows locales whose default console
    # codec is GBK. Reports are written as UTF-8 below; this only affects the
    # terminal stream.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--sessions", type=int, default=200)
    parser.add_argument("--steps", type=int, default=2_000_000)
    parser.add_argument("--beta", type=float, default=4e-6)
    parser.add_argument("--seed", type=int, default=20261001)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--render-only", action="store_true",
                        help="re-render the Markdown report from the saved JSON without re-running")
    args = parser.parse_args()
    if args.render_only:
        result = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        OUT_MD.write_text(render_md(result), encoding="utf-8")
        print(render_md(result))
        return 0
    result = run(args.sessions, args.steps, args.beta, args.seed)
    if args.write:
        OUT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        OUT_MD.write_text(render_md(result), encoding="utf-8")
    print(render_md(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
