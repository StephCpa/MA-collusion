# Four-arm history-channel ledger

This directory contains the sealed four-arm trajectory ledger from the
replacement formal history-channel study (`natural`, `hide_own`,
`hide_rival`, `hide_both`). The ledger is the data object underlying the
four-arm block analysis.

- `ledger.json` — trajectory/round-level ledger;
- `analysis.json` — registered four-arm block analysis and missingness bounds.

The replacement run planned 48 blocks and completed 44 blocks. The analysis
uses complete blocks as the inferential unit and reports completion bounds
separately. Raw provider request/response audit directories are not included.
No API key or private filesystem path is present in the uploaded files. The
public ledger retains model name, usage counts, and formatting-attempt fields
needed by the offline checks, but removes provider request IDs, logical request
IDs, and system fingerprints.

**Sanitization note (2026-10-01).** The `registration` field of `analysis.json`
contained a local absolute path; it was replaced with the project-relative path
`artifacts/history-channel-formal/20260922-deepseek-flash-v021/registration.json`.
No other value in the analysis was changed. The ledger can be regenerated from
an internal copy with `tools/sanitize_four_arm_ledger.py`; the checked-in public
file is already sanitized. It is reproduced and analysed by
`tools/four_arm_leading_indicator.py`, which reads both files and writes neither.
