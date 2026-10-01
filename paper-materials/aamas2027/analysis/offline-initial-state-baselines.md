# Offline initial-state and imitation-baseline sensitivity

This report uses sealed EXP-045 trajectories and deterministic counterfactual rules only; `network_calls=0`. The closed-loop grid enumerates every ordered initial pair on the original grid. It is a stress test of heuristic explanations, not a causal estimate of an LLM policy.

## Held-out action matches

| rule | mean assessment match | exact generator of every held-out trajectory? |
|---|---:|---|
| `simultaneous_myopic_br` | 0.0675 | no |
| `mechanical_undercut` | 0.0675 | no |
| `match_if_equal_else_copy_rival` | 0.8750 | no |
| `match_if_equal_else_undercut` | 0.8688 | no |
| `inertia_own_price` | 0.8863 | no |

The imitation-like rules (`match_if_equal_else_copy_rival`, `match_if_equal_else_undercut`) match 87.50% and 86.875% of held-out assessment actions, respectively, while own-price inertia matches 88.625% in the parent audit. None is an exact generator, so these are compatible descriptive baselines rather than identified mechanisms.

## Initial-state counterfactuals

| rule | equal starts preserved | unequal starts ending equal | unequal starts ending at floor | max updates |
|---|---:|---:|---:|---:|
| `simultaneous_myopic_br` | 1/10 | 90/90 | 90/90 | 8 |
| `mechanical_undercut` | 1/10 | 90/90 | 90/90 | 9 |
| `match_if_equal_else_copy_rival` | 10/10 | 0/90 | 0/90 | 30 |
| `match_if_equal_else_undercut` | 10/10 | 90/90 | 90/90 | 9 |
| `inertia_own_price` | 10/10 | 0/90 | 0/90 | 0 |

The copying rule preserves every initial pair, including (6.0, 6.0), (6.5, 6.5), and (6.0, 6.5); it can therefore sustain high-price ties without strategic punishment. Match-if-equal-else-undercut preserves all ten equal-price starts (including high and mid prices) but drives most unequal starts to the floor. Myopic best response and mechanical undercutting drive every grid start to the floor. This demonstrates why the observed persistent high-price states do not, by themselves, identify collusion or a strategic response. (Wording revised 2026-10-01: the earlier text called these states "absorbing", which the evidence does not establish.)

## Observed unequal-state transitions

- all transitions: `{'observations': 268, 'copy_rival_rate': 0.35447761194029853, 'inertia_own_rate': 0.39552238805970147, 'one_step_undercut_rate': 0.376865671641791}`
- assessment transitions: `{'observations': 92, 'copy_rival_rate': 0.40217391304347827, 'inertia_own_rate': 0.5, 'one_step_undercut_rate': 0.34782608695652173}`

These conditional rates are descriptive and are not a substitute for the proposed feedback-surface experiment. They provide an offline audit of the copying/inertia alternative without adding paid model calls.

## Reproduction

```powershell
python research/initial_state_baseline_sensitivity.py
```
