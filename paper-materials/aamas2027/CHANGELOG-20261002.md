# Change Log — AAMAS 2027 Submission Materials

## Scope

This update consolidates the reproducibility package and the bounded empirical
paper claim. It does not upgrade the paper to a claim of collusion or causal
identification beyond the registered observables.

## Manuscript and submission package

- Declared `paper-materials/aamas2027/latex/history-display-observability.tex`
  as the canonical manuscript source.
- Added the staging PDF and recorded its page count and SHA-256 fingerprint.
- Expanded the bibliography and audited all citation keys: 25 cited keys and
  25 bibliography entries, with no missing or uncited keys.
- Added the AAMAS requirements check, submission gates, author decisions,
  delivery status, review response, and integrity audit documents.
- Added an AI-assisted-methodology disclosure record and anonymization notes.

## Evidence and analyses

- Added the claim--evidence matrix and a reproducibility rerun record.
- Added the observability certificate, including the complete T1 partition and
  ledger-backed checks.
- Added the Candidate-A confirmation analysis, leading-indicator analysis, and
  structural leave-one-block-out stability analysis.
- Added settlement generalization across two, three, and four sellers.
- Added the render-only Q-learning baseline as a clearly separated non-LLM
  positive-control analysis.
- Added controlled-initial descriptives and the corresponding figure sources.
- Recorded the manuscript-source divergence audit so the older standalone draft
  cannot be merged implicitly with the canonical source.

## Data, figures, and tools

- Included the sanitized original controlled-initial ledger and the four-arm
  history-channel ledger/analysis artifacts.
- Added reproducible figure builders and figure manifests for the manuscript
  figures.
- Added material, supplement, claim-matrix, observability, and supplement-zip
  validators.
- Included the single ZIP supplement (`aamas2027-supplement-v0.3.zip`) with
  manifest and hash verification.

## Verification status

- Full project test suite: 386 passed.
- Material validator: passed.
- Claim-evidence matrix validator: passed (C1--C5).
- Observability certificate: passed; 10 T1 classes and 11,375 ledger rounds
  checked.
- Supplement verifier: passed; 105 archive entries and 104 manifest files.
- Final staging PDF: 8 pages and text-extractable.

## Remaining author-side gates

The package intentionally records, rather than silently resolves, the gates
that require author action: migration to the official AAMAS template, a dated
pre-analysis selection record, an anonymized repository URL for double-blind
review, and final provider-ID closure. These are submission gates, not hidden
changes to the scientific claim.

## Manuscript enrichment and figure redesign (later on 2026-10-02)

No provider calls, paid runs or changes to registered estimands. Every number
added to the manuscript comes from an existing public ledger or analysis file
and is gated by `tools/check_materials.py`.

### Manuscript

- Introduction rewritten around the monitoring problem (oversight of pricing
  agents, the welfare-class blind spot, the open question), with four
  contributions.
- Related work expanded from four short paragraphs to four topical subsections:
  algorithmic pricing and tacit collusion; price transparency and disclosure;
  multi-agent learning and language-model agents; monitoring, auditing and
  identification. The bibliography grew from 25 to 46 entries (all cited); new
  entries were checked against publisher or proceedings records.
- Section 3 now states a recoverability criterion and Proposition 1 (welfare
  classes, which targets a welfare monitor can and cannot recover, and the
  total-variation bound behind the blind-share metric). The former
  equivalence-class table is replaced by Figure 2A.
- New results: first-decision divergence and per-block stability
  (round-1 pooled contrasts 0.553 and 0.476; 46/47 and 42/42 blocks positive;
  welfare contrast exactly zero in 43/47 and 41/42 blocks; sign test
  4.547e-13; leave-one-block-out 0.826--0.850), assessment-window composition,
  and a boundary-conditions subsection (Q-learning agent class, 2--4 sellers,
  captive consumers). Table 2 gained a round-1 column and is set at its natural
  size.
- The captive-consumer statement now names the pair it refers to: a 1% welfare
  monitor needs theta >= 0.11 to separate the (6.0, 6.0) tie from the
  (6.0, 6.5) capture state, and a 5% monitor cannot at any feasible theta.
- Discussion restructured into a conditional observability boundary, rival
  explanations, monitor design, strategic tests and limitations.
- Layout: the main text ends on page 8 and the references continue onto
  page 9, as the AAMAS 2027 rules allow (at most 8 pages of main text,
  references unlimited).

### Figures

- Figure 1 (`fig1-framework-evidence-map.*`) and Figure 2
  (`fig2-observability-boundary.*`) redesigned from reproducible sources.
- New Figure 3 (`fig-dynamics-structure-welfare.*`) and Figure 6
  (`fig-boundary-conditions.*`).
- Figures 4 and 5 restyled (grid lines and one overlapping label removed);
  values unchanged.
- All six figures share `tools/figstyle.py`, pass a 5 pt font floor and a
  collision audit with zero failures, and rebuild to byte-identical PDFs
  (`analysis/figure-qa-20261002/`). Superseded figures are kept and marked
  retired in `figures/figure-manifest.json`.

### Analyses, tools and supplement

- `tools/structure_dynamics.py` writes `analysis/structure-dynamics-20261002.*`
  from the public ledgers and checks itself against the frozen paired
  sensitivities and the replication primary.
- `tools/check_materials.py`: the PDF gate now enforces "main text ends by
  page 8" instead of "at most 8 PDF pages", and the dynamics and robustness
  numbers are new gated claims.
- Claim-evidence matrix extended with C6 (first-decision divergence) and C7
  (agent-class and market-rule boundaries).
- Supplement v0.4 (`aamas2027-supplement-v0.4.zip`, README in
  `SUPPLEMENT-README-v0.4.md`): v0.3 plus the new builders, figure PDFs,
  dynamics analysis, figure QA, extended claim matrix and the current gates
  record. Extracted into a clean directory, it regenerates all six figure PDFs
  and the dynamics JSON byte-for-byte.

### Verification

- `tools/check_materials.py --pdf ... --log ...`: passed, 0 failures.
- `tools/check_claim_evidence_matrix.py`: passed, C1--C7.
- `tools/verify_supplement.py aamas2027-supplement-v0.4.zip`: passed;
  121 archive entries, 120 manifest files, no hash or metadata-key failures.
- Staging PDF: 9 pages (main text ends on page 8), 661,617 bytes, SHA-256
  `aa457cc3b8c03d7423ab529e7edf209c5d9633b4a04e4b88bb242c59e6cee863`.
- The 386-test project suite lives outside this repository and was not rerun
  for this update.
