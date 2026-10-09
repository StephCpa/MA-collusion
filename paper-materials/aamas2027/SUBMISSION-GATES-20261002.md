# Submission-gate register (2026-10-02)

This file distinguishes completed evidence from author decisions still needed.
It is not a claim that every gate is closed.

| gate | status | evidence / remaining action |
|---|---|---|
| A1: pre-launch selection of `delta_W = 5` | open | A repository-wide search on 2026-10-02 found no dated pre-call selection record. Attach one if it exists elsewhere, or keep the margin labeled a candidate in the manuscript. |
| A2: official AAMAS template | blocked externally | The organizer ZIP was attempted through both the command-line network path and the in-app browser on 2026-10-02; the former timed out and the latter blocked direct ZIP navigation. On 2026-10-09 the cloud session's egress policy refused `warwick.ac.uk` (HTTP 403), so the official archive is still unavailable there. No substitute class was introduced; migrate once the official archive is available. The AAMAS submission ID 3336 is set with `\acmSubmissionID{3336}`, which the acmart-based class prints under the anonymous author line. |
| A3: double-blind repository | open | Do not link the named public repository from an anonymous submission; prepare an anonymized mirror if a supplement URL is required. |
| A4: original controlled-initial raw ledger/builder | partial, substantially resolved | A metadata-free 384-cell ledger, descriptive summarizer and a public replacement figure builder are now included. The private raw request archive and original `build_paper_figures_20260928.py` remain excluded; the original figure counts are still marked as frozen descriptive evidence. |
| A5: original completion-range support convention | partial | The numerical convention is now reconstructed and documented in `analysis/completion-range-convention-20261002.md`; the original dated pre-analysis selection record is still missing. |
| A6: gate-passing T4 positive-control run | intentionally not run | Not required for the bounded observability paper. Requires a new paid run and explicit approval if a strategic-maintenance claim is added. |
| A7: provider request IDs | closed for public package | Provider request IDs, logical request IDs and system fingerprints were removed from the public JSON artifacts and supplement ZIP. Internal raw ledgers remain outside the candidate package. |
| A8: round-1 prompt comparison | complete | Sanitized result is in `analysis/a8-prompt-diff-20261002.*`; the reversal remains an initial-state/generalization question. |

## Current package state

The staging source remains a double-blind `acmart` build whose main text ends
on page 8, with references continuing onto page 9 as the AAMAS rules allow. The
candidate branch has passed `tools/check_materials.py` with zero failures and
was compiled locally after adding a compatibility fallback for `\\Description`,
but it is not the final official-template build.
