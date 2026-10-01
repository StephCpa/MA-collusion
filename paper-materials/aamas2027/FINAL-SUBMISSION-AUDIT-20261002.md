# Final submission audit — 2026-10-02

This record freezes what has been verified for the current AAMAS candidate. It
separates evidence that is complete from gates that still require an external
resource or an author decision.

## Verified locally

| item | evidence | result |
|---|---|---|
| Offline statistical and structural checks | `tools/check_materials.py` | `passed=true`, `failures=0` |
| Repository test suite | `pytest -q` from the project root | 386 passed in 65.31 s |
| Structural-primary sign robustness | `analysis/structural-sign-test-20261002.*` | 42/42 positive block signs; exact two-sided sign probability `4.547e-13`; descriptive only |
| Observability certificate | `tools/observability_certificate.py --check` | 10 T1 classes; 11,375 ledger rounds re-settled; separating observables enumerated |
| Candidate A reproduction | `tools/candidate_a_structural.py --check` | `D_tie=0.830`; block-t 95% `[0.743, 0.917]`; completion range `[0.792, 0.841]` |
| Four-arm leading indicator | `tools/four_arm_leading_indicator.py --check` | natural capture-minus-tie welfare `-27.942`; blindness metrics reproduced |
| Classical-agent baseline | `tools/qlearning_baseline.py --render-only` | seeded offline output reproduced; explicitly non-LLM baseline, not pooled with manuscript estimates |
| Manuscript compilation | local `pdflatex` + BibTeX, three LaTeX passes | 8 pages; no undefined citations/references or overfull boxes |
| Anonymity scan | `check_materials.py` plus PDF text inspection | anonymous author line only; no private path, key or named repository in candidate text |
| Public JSON metadata | `tools/sanitize_request_metadata.py` and `tools/sanitize_four_arm_ledger.py` | provider request IDs, logical request IDs and system fingerprints removed |
| Supplement integrity | `aamas2027-supplement-v0.3.zip/package-manifest.json` and `tools/verify_supplement.py` | 100 archive entries, 99 manifest files, zero hash/size mismatches and zero metadata-key hits |
| Offline handoff | `releases/MA-collusion-submission-candidate-20261002.bundle` | verified complete Git bundle; exact commit and SHA-256 are recorded in `releases/README.md` and the adjacent checksum |

The public data therefore supports reproduction of the reported structural,
observability and bounded welfare analyses without exposing provider request
identifiers. Usage counts and formatting-attempt fields are retained only when
they are consumed by an offline check.

## Scientific scope frozen by the evidence

The manuscript claims an information-dependent change in joint-action
structure and allocation that aggregate welfare can miss. It does not claim a
general collusion result, a false-negative rate for welfare monitors, or a
strategic punishment mechanism. The T4 strategic interpretation remains gated
because the tested operating point is above the joint-profit optimum and the
current forced-deviation probe found no qualifying response.

## Remaining gates

1. Replace the staging `acmart` class with the official AAMAS 2027 template
   when the organizer archive is available; command-line download timed out
   and direct in-app-browser navigation was blocked, so no substitute has been
   introduced.
2. Prepare an anonymized repository or upload-only supplement URL if the
   submission system requires external access. Do not link the named public
   GitHub repository in a double-blind submission.
3. Preserve the missing pre-analysis selection record for the candidate
   `delta_W=5` margin as a limitation, unless collaborators locate the original
   dated record.
4. Complete the author-side AAMAS checks for AI-assisted methodology
   disclosure (exact tool/version and prompts, if applicable) and dual/thin-
   slice overlap with the authors' other submissions.

No further paid experiment is required for the paper's current bounded claim.
A grid-extension or T4 positive-control run would be a separate study and
must not be silently folded into this submission.
