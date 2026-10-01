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
No API key or private filesystem path is present in the uploaded files.
