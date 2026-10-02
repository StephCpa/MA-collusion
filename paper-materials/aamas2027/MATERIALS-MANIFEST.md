# Materials manifest

## Manuscript

- `latex/history-display-observability.tex` — anonymous staging source (enriched 2026-10-02: expanded introduction and related work, recoverability proposition, dynamics and boundary-condition results, restructured discussion).
- `latex/history-display-observability.bib` — bibliography used by the source (46 entries, all cited).
- `latex/history-display-observability-staging.pdf` — compiled staging build (acmart; main text ends on page 8 and the references continue onto page 9, as the AAMAS 2027 rules allow).

## Figures

Manuscript order (2026-10-02); see `figures/figure-manifest.json` and `figures/captions.md`.

- Figure 1 `figures/fig1-framework-evidence-map.*` — framework and evidence map (new; `tools/build_fig1_framework.py`).
- Figure 2 `figures/fig2-observability-boundary.*` — welfare classes, the m = 6.0 allocations and assessment-window composition (new; `tools/build_fig2_observability.py`).
- Figure 3 `figures/fig-dynamics-structure-welfare.*` — per-round and per-block structural and welfare contrasts (new; `tools/build_fig_dynamics.py`).
- Figure 4 `figures/fig2-welfare-versus-structure.*` — registered welfare and structural contrasts (`tools/build_fig2_replication.py`; restyled 2026-10-02).
- Figure 5 `figures/fig3-direction-and-leading-indicator.*` — matching direction and leading indicator (`tools/build_fig3_direction.py`; restyled 2026-10-02).
- Figure 6 `figures/fig-boundary-conditions.*` — agent class, captive consumers and number of sellers (new; `tools/build_fig_boundary.py`).
- Retired, kept for provenance: `figures/framework-observability.*` with `framework-manifest.json`, `figures/fig1-equivalence-and-structure.*`, `figures/fig3-transition-direction.*`.
- `figures/original-controlled-initial-descriptives.*` (regenerated from the public metadata-free ledger; descriptive only; supplement).
- `analysis/figure-qa-20261002/` — font-floor, collision and panel-alignment audit of the six manuscript figures.

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
- Structure dynamics for both controlled-initial runs (`analysis/structure-dynamics-20261002.*`): per-round equal-price and welfare contrasts with block-bootstrap bands, block-level window contrasts and assessment-window composition; descriptive.

## Data

- `data/A-confirmation-*` — Candidate A ledger, frozen analysis and status.
- `data/four-arm-history-channel/` — four-arm ledger and registered analysis (uploaded 2026-10-01; one private path in `analysis.json` replaced by a project-relative path; provider request IDs and system fingerprints removed from the public ledger).
- `data/original-controlled-initial/` — metadata-free derived ledger for the original controlled-initial descriptive comparisons; raw request metadata excluded.

## Tools (offline; no provider calls)

- `tools/observability_certificate.py` — derives the T1 partition and separating observables, evaluates the T4 operating-point gate, re-settles every ledger round.
- `tools/candidate_a_structural.py` — reproduces `data/A-confirmation-analysis.json` exactly (never writes it) and computes the protocol structural primary `D_tie`.
- `tools/build_fig2_replication.py` — regenerates Figure 4 (file stem `fig2-welfare-versus-structure`) byte-reproducibly.
- `tools/four_arm_leading_indicator.py` — reproduces the registered four-arm contrasts, runs the leading-indicator test and the blindness metric.
- `tools/settlement_generalization.py` — exact welfare-blindness arithmetic for more sellers and captive consumers.
- `tools/qlearning_baseline.py` — seeded Q-learning baseline under the four display arms, with programmed-start and impulse evaluations.
- `tools/sanitize_controlled_initial_ledger.py`, `tools/controlled_initial_descriptives.py` and `tools/build_original_descriptive_figures.py` — create, summarize and visualize the public controlled-initial ledger without provider metadata.
- `tools/sanitize_four_arm_ledger.py` and `tools/sanitize_request_metadata.py` — remove provider request IDs, logical request IDs and system fingerprints while retaining fields required by the offline checks.
- `tools/verify_supplement.py` — independently verifies ZIP manifest hashes and the public request-metadata policy.
- `tools/structural_leave_one_block_out.py` — recomputes the registered structural primary after deleting each complete block in turn.
- `tools/build_fig3_direction.py` — regenerates Figure 5 (file stem `fig3-direction-and-leading-indicator`).
- `tools/figstyle.py` — shared palette, font sizes and byte-stable export for all manuscript figures; optional panel-alignment gate.
- `tools/build_fig1_framework.py`, `tools/build_fig2_observability.py`, `tools/build_fig_dynamics.py`, `tools/build_fig_boundary.py` — regenerate Figures 1, 2, 3 and 6.
- `tools/structure_dynamics.py` — computes the per-round and block-level dynamics from the public ledgers and checks them against the frozen paired sensitivities and the replication primary.
- `tools/check_materials.py` — manuscript-to-analysis number check (including the dynamics and robustness numbers), citation/figure check, anonymity scan, optional PDF check that the main text ends by page 8 and the log has no overfull boxes.

## Protocols and supplement

- `SUPPLEMENT-README-v0.4.md` — source copy of the current anonymous ZIP README (`SUPPLEMENT-README-v0.3.md` is the v0.3 copy);
- Candidate A independent-confirmation protocol (execution status note added; frozen text preserved);
- B1--B4 feedback-surface 2x2 protocol;
- anonymous AAMAS supplementary ZIP v0.4 (2026-10-02; 121 archive entries, 1.48 MB compressed; v0.3 plus the new figure builders, figure PDFs, structure-dynamics analysis, figure QA and the extended claim matrix), with v0.3 and v0.1 kept unchanged for provenance; v0.2 is superseded and remains in git history. JSON artifacts in the public ZIP are recursively stripped of provider request IDs, logical request IDs and system fingerprints.

## Review response

- `REVIEW-RESPONSE-20261001.md` — point-by-point response and the list of corrections.
- `SUBMISSION-GATES-20261002.md` — current status of template, provenance, anonymity and optional-experiment gates.
- `FINAL-SUBMISSION-AUDIT-20261002.md` — evidence freeze for compilation, anonymity, public metadata sanitization, supplement integrity and the remaining external gates.
- `AAMAS-REQUIREMENTS-CHECK-20261002.md` — official submission-rule check, including the AI-assisted methodology disclosure and dual-submission author checks.
- `analysis/ai-disclosure-evidence-20261002.md` — separates documented experimental-model metadata from author-side AI-assistance fields that still require author certification.
- `analysis/cross-model-boundary-20261002.md` — records why available Qwen/GLM studies are not pooled with the DeepSeek closed-loop estimand.
- `analysis/claim-evidence-matrix-20261002.*` — machine-readable scope control linking manuscript claims to reproducing artifacts and interpretation boundaries.
- `analysis/reproducibility-rerun-20261002.md` — fresh offline verification log for the manuscript-facing checks and public supplement.
- `tools/check_claim_evidence_matrix.py` — verifies that every matrix claim has a valid status, complete boundary fields and existing evidence paths.
- `AUTHOR-SUBMISSION-DECISIONS-20261002.md` — author-certified submission gate form; intentionally retains unresolved fields as `PENDING`.
- `RESEARCH-INTERPRETATION-20261002.md` — paper-level synthesis separating established evidence, non-identified claims and a future T4 protocol boundary.
- `analysis/manuscript-source-divergence-20261002.md` — hash-level audit distinguishing the older workspace draft from the canonical staging source.
- `NEXT-ACTIONS-20261002.md` — collaborator handoff checklist separating completed work, author decisions and actions that require a new protocol.
- `INTEGRITY-AUDIT-20261002.md` — claim/evidence, numeric, citation-key and artifact-integrity audit.
- `DELIVERY-STATUS-20261002.md` — local branch and remote-delivery status.
- The canonical submission manuscript is the staging source under `latex/`; a separate older workspace draft is intentionally not part of the candidate source of truth.

Raw provider request/response logs are excluded by design. The trajectory
ledger is included because it is the primary data object needed to inspect the
reported missingness, completion-range and structural-primary analyses.
