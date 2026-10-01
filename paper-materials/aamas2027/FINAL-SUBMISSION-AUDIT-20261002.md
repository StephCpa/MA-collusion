# Final submission audit — 2026-10-02

This record freezes what has been verified for the current AAMAS candidate. It
separates evidence that is complete from gates that still require an external
resource or an author decision.

## Verified locally

| item | evidence | result |
|---|---|---|
| Offline statistical and structural checks | `tools/check_materials.py` | `passed=true`, `failures=0` |
| Manuscript compilation | local `pdflatex` + BibTeX, three LaTeX passes | 8 pages; no undefined citations/references or overfull boxes |
| Anonymity scan | `check_materials.py` plus PDF text inspection | anonymous author line only; no private path, key or named repository in candidate text |
| Public JSON metadata | `tools/sanitize_request_metadata.py` and `tools/sanitize_four_arm_ledger.py` | provider request IDs, logical request IDs and system fingerprints removed |
| Supplement integrity | `aamas2027-supplement-v0.3.zip/package-manifest.json` | 97 archive entries, 96 manifest files, zero hash/size mismatches |
| Offline handoff | `releases/MA-collusion-submission-candidate-20261002.bundle` | verified complete Git bundle at commit `8b1f1c8` |

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
   when the organizer archive is available; the current archive request timed
   out and no substitute has been introduced.
2. Prepare an anonymized repository or upload-only supplement URL if the
   submission system requires external access. Do not link the named public
   GitHub repository in a double-blind submission.
3. Preserve the missing pre-analysis selection record for the candidate
   `delta_W=5` margin as a limitation, unless collaborators locate the original
   dated record.

No further paid experiment is required for the paper's current bounded claim.
A grid-extension or T4 positive-control run would be a separate study and
must not be silently folded into this submission.
