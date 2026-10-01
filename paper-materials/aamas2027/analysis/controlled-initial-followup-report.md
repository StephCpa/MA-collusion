# Controlled-initial follow-up diagnostics (2026-09-28)

> **Scope.** Post-hoc, offline, descriptive/sensitivity analysis of the sealed continuation ledger. No provider calls were made. This report does not change the registered estimands or establish T4 strategic harmful coordination.

## 1. Round 0 versus round 1

Round 0 is programmed, so the arm-invariance check is a design check rather than a treatment test. Any display-arm difference first becomes observable after the first model decision in round 1.

| Initial cell | Natural round-1 states | Hide-rival round-1 states |
|---|---|---|
| LL | {'(6,6)': 46} | {'(6,6)': 48} |
| LH | {'(6,6)': 23, '(6,6.5)': 24, '(6.5,6)': 1} | {'(6,6.5)': 47} |
| HL | {'(6,6)': 30, '(6.5,6)': 17, '(6.5,6.5)': 1} | {'(6.5,5.5)': 1, '(6.5,6)': 46, '(6.5,6.5)': 1} |
| HH | {'(6.5,6.5)': 48} | {'(6.5,6.5)': 47} |

All completed round-0 observations match their programmed initial state in both arms. The round-1 table is the appropriate descriptive gate for a possible prompt/display effect before later trajectory persistence.

| Initial cell | Paired blocks | Round-1 tie fraction: natural − hide-rival | Round-1 minimum price: natural − hide-rival | Tie sign count (+ / 0 / −) |
|---|---:|---:|---:|---|
| LL | 46 | 0.0000 | 0.0000 | 0 / 46 / 0 |
| LH | 47 | 0.4681 | 0.0000 | 22 / 25 / 0 |
| HL | 48 | 0.6250 | 0.0104 | 30 / 18 / 0 |
| HH | 47 | 0.0000 | 0.0000 | 0 / 47 / 0 |

The paired round-1 contrasts are descriptive fixed-round sensitivities; they do not replace block-level registered welfare inference.

## 2. Welfare support and exact joint states

| Cell | Completed trajectories | Assessment states | m=6.0 fraction | m=6.5 fraction | Two-point support? |
|---|---:|---|---:|---:|---|
| HH-hide_rival | 47 | {'(6.5,6.5)': 940} | 0.0000 | 1.0000 | False |
| HH-natural | 48 | {'(6.5,6.5)': 960} | 0.0000 | 1.0000 | False |
| HL-hide_rival | 48 | {'(6.5,6)': 960} | 1.0000 | 0.0000 | False |
| HL-natural | 48 | {'(6,6)': 793, '(6.5,6)': 141, '(6.5,6.5)': 26} | 0.9729 | 0.0271 | True |
| LH-hide_rival | 47 | {'(6,6.5)': 940} | 1.0000 | 0.0000 | False |
| LH-natural | 48 | {'(6,6)': 832, '(6,6.5)': 108, '(6.5,6.5)': 20} | 0.9792 | 0.0208 | True |
| LL-hide_rival | 48 | {'(6,6)': 960} | 1.0000 | 0.0000 | False |
| LL-natural | 46 | {'(6,6)': 920} | 1.0000 | 0.0000 | False |

In the asymmetric cells, the welfare support is concentrated on the two minimum-price levels 6.0 and 6.5, although the joint state can still distinguish `(6.0,6.0)` from `(6.0,6.5)`. The labels `m=6.0` and `m=6.5` are used instead of calling 6.0 a universally low price.

## 3. Choice conditional on a previous-round rival price of 6.5

| Initial | Arm | Seller | N | Match 6.5 | Undercut 6.0 | Profit-max undercut 5.5 | Other |
|---|---|---|---:|---:|---:|---:|---:|
| HH | hide_rival | seller_a | 1363 | 1363 | 0 | 0 | 0 |
| HH | hide_rival | seller_b | 1363 | 1363 | 0 | 0 | 0 |
| HH | natural | seller_a | 1392 | 1392 | 0 | 0 | 0 |
| HH | natural | seller_b | 1392 | 1392 | 0 | 0 | 0 |
| HL | hide_rival | seller_a | 1 | 1 | 0 | 0 | 0 |
| HL | hide_rival | seller_b | 1392 | 1 | 1390 | 1 | 0 |
| HL | natural | seller_a | 30 | 30 | 0 | 0 | 0 |
| HL | natural | seller_b | 330 | 33 | 297 | 0 | 0 |
| LH | hide_rival | seller_a | 1363 | 0 | 1363 | 0 | 0 |
| LH | natural | seller_a | 286 | 28 | 258 | 0 | 0 |
| LH | natural | seller_b | 28 | 28 | 0 | 0 | 0 |

This table separates matching, a one-grid-step undercut, and the one-shot profit-maximizing undercut for the tested settlement rule. It conditions on the previous public state only; it is not a dynamic best-response or collusion test.

## 4. Paired block sensitivity

| Initial | Pairs | Metric | Natural − hide-rival mean | 95% paired t interval | Positive / zero / negative pairs |
|---|---:|---|---:|---|---|
| LH | 47 | equal-price fraction | 0.8851 | [0.7944, 0.9759] | 44 / 3 / 0 |
| LH | 47 | profit HHI | -0.4426 | [-0.4879, -0.3972] | 0 / 3 / 44 |
| LH | 47 | minimum price | 0.0106 | [-0.0108, 0.0321] | 1 / 46 / 0 |
| HL | 48 | equal-price fraction | 0.8531 | [0.7566, 0.9497] | 46 / 2 / 0 |
| HL | 48 | profit HHI | -0.4266 | [-0.4748, -0.3783] | 0 / 2 / 46 |
| HL | 48 | minimum price | 0.0135 | [-0.0078, 0.0349] | 3 / 45 / 0 |

These are post-hoc block-paired sensitivity summaries, not new registered primary tests. They quantify the structural contrast at the independent block level while keeping repeated rounds nested within trajectories.

## 5. Operating-point benchmark

The settlement arithmetic places the symmetric 5.5 state at the joint-profit maximum (112.500 per seller; total welfare 337.500). The symmetric 6.0 and 6.5 states observed in the study yield 111.111 and 106.944 per seller, respectively, and welfare 311.111 and 281.944. Thus equal-price matching at the observed upper states is not, by itself, a cartel certificate: both sellers could improve by moving together toward 5.5. This is an arithmetic benchmark, not a claim about model preferences or equilibrium.

## 6. Interpretation boundary

- Round 0 is programmed and therefore cannot provide an arm-effect test.
- Round-1 and conditional action counts are descriptive; model decisions are simultaneous and not a causal mediation estimate.
- Assessment-round counts repeat within trajectories and are not independent samples.
- Paired t intervals are sensitivity summaries only; they do not replace the registered welfare estimands.
- A two-point welfare support reflects the settlement/grid in this run and does not identify preferences above the 6.5 ceiling.

## Reproducibility

Run:

```powershell
$env:PYTHONPATH='src;research'
& 'C:/Users/76790/anaconda3/python.exe' research/derive_controlled_initial_followup_20260928.py
```

Outputs are `analysis.json` and this report. Raw ledgers and registered analyses are not overwritten.
