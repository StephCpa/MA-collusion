# Cross-model boundary note — 2026-10-02

The workspace contains additional Qwen3.7-Flash and GLM-5.3 pricing studies,
but they are not interchangeable replications of the DeepSeek history-display
study. This note records the non-pooling decision so that future revisions do
not accidentally turn a collection of different estimands into a cross-model
claim.

| study | model / task | observed result | why it is not pooled here |
|---|---|---|---|
| E01 Delivery v0.1 | Qwen3.7-Flash, one-shot A2/A3 delivery, 1,920 requests | all requests usable; registered three-category A2−A3 contrast exactly 0 | one-shot delivery, not a closed-loop 30-round history intervention |
| E02 mechanism diagnostic | Qwen3.7-Flash, fixed-horizon prompt probes | payoff-table and translation probes; two invalid strategy calls retained | diagnostic prompt estimand, not the AAMAS trajectory ledger |
| EXP-045 offline-rule audit | GLM-5.3, 20 forced-tool autonomous trajectories | 351/400 assessment rounds tied; no candidate offline rule exactly generates all held-out windows | different provider, model, prompt and settlement run; rule audit rather than history-display factorial |
| Candidate A / four-arm study | DeepSeek `deepseek-flash`, repeated two-seller market | structural history-display effects and welfare-blind joint-state changes | current manuscript's registered target |

The manuscript therefore makes a conditional one-deployment claim and states
explicitly that the replication is not cross-model. The other studies remain
valuable as a future transportability analysis, but pooling their outcomes now
would conflate delivery, competence, rule-generation and closed-loop
information-policy estimands.
