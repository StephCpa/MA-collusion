# Integrity audit — 2026-10-02

Mode: full (claim-support, numeric, terminology, figure/text, citation-key and
artifact-integrity checks). This is an offline audit; no provider calls were
made.

## Artifacts checked

- `latex/history-display-observability.tex` and `.bib`
- all JSON/Markdown analyses under `analysis/`
- Candidate A and four-arm data under `data/`
- figure captions and manifests
- `tools/check_materials.py` and the four reproduction/check scripts
- the current submission-gate register

## Claim-evidence matrix

| claim | status | evidence and boundary |
|---|---|---|
| History display changes joint-action structure in the tested deployment | supported | Candidate A structural primary: `D_tie = 0.830`, interval `[0.743, 0.917]`, completion range `[0.792, 0.841]`; reproduction check passes. |
| Welfare and joint-action structure can disagree under minimum-price settlement | supported, conditional | Observability certificate derives the 10-class collapse and re-settles 11,375 replication rounds with zero mismatches. The manuscript states the settlement/grid boundary. |
| The blind spot is not a general false-negative rate | supported | The paper reports treatment-specific TV values and explicitly rejects a general monitoring-error claim. |
| Structure can lead welfare in the four-arm run | supported as post hoc/descriptive | Leading-indicator analysis reproduces `-27.94167` capture-minus-tie welfare and the matching-direction counts; the manuscript labels the comparison post hoc and observational. |
| A strategic collusion or harmful-coordination mechanism was demonstrated | correctly not claimed | X2 is local and fails the operating-point gate; the conclusion explicitly withholds collusion and T4 claims. |
| Q-learning provides a positive-control/agent-class comparison | supported, scoped | Saved seeded JSON reproduces the welfare contrasts and impulse counts; it is clearly separated from the LLM evidence. |

## Numeric consistency findings

- `check_materials.py`: passed with zero failures.
- Candidate A, leading-indicator, observability-certificate and settlement
  checks: all passed.
- `D_tie`, welfare contrasts, completion ranges, blindness metric, settlement
  shares and Q-learning values agree between manuscript-facing records and
  their generating JSON files.
- No contradictory duplicate value was found in the checked manuscript,
  captions or analysis records.
- A1 and A5 remain provenance limitations rather than numeric inconsistencies:
  the numerical convention is reproducible, but the dated pre-analysis
  selection records are absent.

## Citation and metadata findings

- 25 cited keys; 25 bibliography keys; zero missing keys and zero duplicate
  keys.
- The bibliography contains a mixture of journal, conference and arXiv
  records. Entries without DOI are conference-style records rather than
  unresolved citation keys; venue/title/year fields are present for the
  checked entries.
- This audit did not perform a new literature search or certify external
  citation context beyond the supplied bibliography.

## Severity and safe edits

- **Blocking:** official AAMAS template is unavailable; the current PDF remains
  a staging `acmart` build.
- **Submission-risk:** the public repository is not anonymous; do not link it
  from a double-blind submission.
- **Provenance:** attach the δW selection record and original completion-range
  selection record if available. Otherwise retain the current candidate/limited
  wording.
- **Data availability (partly resolved):** a metadata-free original
  controlled-initial ledger and descriptive summarizer are now included. The
  original figure builder and private raw request archive remain excluded, so
  the original figure-generation path is still not fully public.

No numerical or claim wording was silently changed during this audit.

Next CCFA owner: paper-writer/template-migration pass after the official AAMAS
archive is available.

No-invention status: all reported values above are copied from supplied
analysis artifacts or reproduced by their checks; no missing result was
imputed.
