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
