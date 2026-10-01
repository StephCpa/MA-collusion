# Materials manifest

## Manuscript

- `latex/history-display-observability.tex` — anonymous eight-page staging source (revised 2026-10-01).
- `latex/history-display-observability.bib` — bibliography used by the source.
- `latex/history-display-observability-staging.pdf` — compiled staging build (acmart, 8 pages including references).

## Figures

- `figures/fig1-equivalence-and-structure.*` (original run)
- `figures/fig2-welfare-versus-structure.*` (regenerated 2026-10-01 with the replication; `tools/build_fig2_replication.py`)
- `figures/fig3-direction-and-leading-indicator.*` (new 2026-10-01; `tools/build_fig3_direction.py`)
- `figures/fig3-transition-direction.*` (original-run counts; retired from the manuscript, kept for the supplement)
- `figures/original-controlled-initial-descriptives.*` (regenerated from the public metadata-free ledger; descriptive only)
- `figures/framework-observability.*`
- accompanying captions and figure manifests.

## Evidence and analysis

- controlled-initial follow-up report and analysis (private source paths replaced by project-relative paths on 2026-10-01; no values changed);
- Candidate A confirmation result record (corrected 2026-10-01) and raw trajectory ledger;
- Candidate A structural primary and descriptive record (`analysis/A-confirmation-structural-20261001.*`, new);
- settlement observability certificate and operating-point gate (`analysis/observability-certificate.*`, new);
- X1/X2 statistical qualification (gap-direction label corrected);
- fixed-history qualification;
- offline initial-state baseline ("absorbing" wording removed);
- reproducibility metadata register;
- completion-range convention audit (`analysis/completion-range-convention-20261002.md`);
- four-arm reproduction, leading-indicator test and monitor-blindness metric (`analysis/four-arm-leading-indicator-20261001.*`, new);
- settlement generalization to 3–4 sellers and captive consumers (`analysis/settlement-generalization-20261001.*`, new);
- Q-learning classical-agent baseline under the four display arms (`analysis/qlearning-baseline-20261001.*`, new).
- A8 offline round-1 prompt-difference diagnostic (`analysis/a8-prompt-diff-20261002.*`, derived from sealed local request logs; raw requests excluded).
- Exact block-sign robustness check for the registered structural primary (`analysis/structural-sign-test-20261002.*`); descriptive only and kept separate from the registered interval.
- Leave-one-block-out structural sensitivity (`analysis/structural-leave-one-block-out-20261002.*`), with all 42 deletion estimates remaining positive.

## Data

- `data/A-confirmation-*` — Candidate A ledger, frozen analysis and status.
- `data/four-arm-history-channel/` — four-arm ledger and registered analysis (uploaded 2026-10-01; one private path in `analysis.json` replaced by a project-relative path; provider request IDs and system fingerprints removed from the public ledger).
- `data/original-controlled-initial/` — metadata-free derived ledger for the original controlled-initial descriptive comparisons; raw request metadata excluded.

## Tools (offline; no provider calls)

- `tools/observability_certificate.py` — derives the T1 partition and separating observables, evaluates the T4 operating-point gate, re-settles every ledger round.
- `tools/candidate_a_structural.py` — reproduces `data/A-confirmation-analysis.json` exactly (never writes it) and computes the protocol structural primary `D_tie`.
- `tools/build_fig2_replication.py` — regenerates Figure 2 byte-reproducibly.
- `tools/four_arm_leading_indicator.py` — reproduces the registered four-arm contrasts, runs the leading-indicator test and the blindness metric.
- `tools/settlement_generalization.py` — exact welfare-blindness arithmetic for more sellers and captive consumers.
- `tools/qlearning_baseline.py` — seeded Q-learning baseline under the four display arms, with programmed-start and impulse evaluations.
- `tools/sanitize_controlled_initial_ledger.py`, `tools/controlled_initial_descriptives.py` and `tools/build_original_descriptive_figures.py` — create, summarize and visualize the public controlled-initial ledger without provider metadata.
- `tools/sanitize_four_arm_ledger.py` and `tools/sanitize_request_metadata.py` — remove provider request IDs, logical request IDs and system fingerprints while retaining fields required by the offline checks.
- `tools/verify_supplement.py` — independently verifies ZIP manifest hashes and the public request-metadata policy.
- `tools/structural_leave_one_block_out.py` — recomputes the registered structural primary after deleting each complete block in turn.
- `tools/build_fig3_direction.py` — regenerates Figure 3.
- `tools/check_materials.py` — manuscript-to-analysis number check, citation/figure check, anonymity scan, optional PDF page/overfull check.

## Protocols and supplement

- `SUPPLEMENT-README-v0.3.md` — source copy of the anonymous ZIP README, kept synchronized with the current package contents and sanitization policy;
- Candidate A independent-confirmation protocol (execution status note added; frozen text preserved);
- B1--B4 feedback-surface 2x2 protocol;
- anonymous AAMAS supplementary ZIP v0.3 (refreshed 2026-10-02; 105 archive entries, 1.35 MB compressed) and v0.1 (unchanged, for provenance); v0.2 is superseded and remains in git history. JSON artifacts in the public ZIP are recursively stripped of provider request IDs, logical request IDs and system fingerprints.

## Review response

- `REVIEW-RESPONSE-20261001.md` — point-by-point response and the list of corrections.
- `SUBMISSION-GATES-20261002.md` — current status of template, provenance, anonymity and optional-experiment gates.
- `FINAL-SUBMISSION-AUDIT-20261002.md` — evidence freeze for compilation, anonymity, public metadata sanitization, supplement integrity and the remaining external gates.
- `AAMAS-REQUIREMENTS-CHECK-20261002.md` — official submission-rule check, including the AI-assisted methodology disclosure and dual-submission author checks.
- `analysis/ai-disclosure-evidence-20261002.md` — separates documented experimental-model metadata from author-side AI-assistance fields that still require author certification.
- `analysis/cross-model-boundary-20261002.md` — records why available Qwen/GLM studies are not pooled with the DeepSeek closed-loop estimand.
- `analysis/claim-evidence-matrix-20261002.*` — machine-readable scope control linking manuscript claims to reproducing artifacts and interpretation boundaries.
- `analysis/reproducibility-rerun-20261002.md` — fresh offline verification log for the manuscript-facing checks and public supplement.
- `NEXT-ACTIONS-20261002.md` — collaborator handoff checklist separating completed work, author decisions and actions that require a new protocol.
- `INTEGRITY-AUDIT-20261002.md` — claim/evidence, numeric, citation-key and artifact-integrity audit.
- `DELIVERY-STATUS-20261002.md` — local branch and remote-delivery status.

Raw provider request/response logs are excluded by design. The trajectory
ledger is included because it is the primary data object needed to inspect the
reported missingness, completion-range and structural-primary analyses.
