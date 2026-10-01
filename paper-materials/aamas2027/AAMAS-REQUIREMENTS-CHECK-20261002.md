# AAMAS 2027 requirements check — 2026-10-02

Source: [AAMAS 2027 submission instructions](https://warwick.ac.uk/fac/sci/dcs/aamas2027/guidelines-and-policies/instructions/),
accessed 2026-10-02.

| requirement | current evidence | status |
|---|---|---|
| English, double-blind PDF | `latex/history-display-observability-staging.pdf`; anonymous author line and local anonymity scan | satisfied in staging |
| Main-track length | local PDF compilation reports 8 pages; references are separate | satisfied in staging |
| LaTeX mandatory | `latex/history-display-observability.tex` | satisfied in staging |
| Supplement is one ZIP and ≤25 MB | `aamas2027-supplement-v0.3.zip`, 1.34 MB compressed | satisfied |
| Supplement does not compromise anonymity | recursive private-path/key scan and provider-metadata sanitization | satisfied for current package |
| Official formatting template | organizer ZIP link is published, but download timed out from this environment | pending external access |
| AI-assisted methodology disclosure | the policy requires tool/version and prompt details when AI helped create hypotheses or methods | author completion required |
| Dual/thin-slice check | overlap with the authors' other submissions must be confirmed by authors | author completion required |

## AI disclosure placeholder

Before submission, authors should decide whether AI assistance materially
contributed to the hypotheses or experimental methodology. If yes, add the
exact tool name/version and the relevant prompts to this document or the
supplement, while preserving double-blind anonymity. Do not claim that this
requirement is satisfied until those details have been supplied and checked by
the authors. AI systems are not authors; the human authors remain responsible
for the paper, code and data.

## Operational note

The official template URL is recorded in `SUBMISSION-GATES-20261002.md`. Do not
replace it with an unofficial class or alter layout parameters merely to obtain
an apparently compliant PDF. The current `acmart` build is a staging artifact.
