# Original controlled-initial descriptive summaries

Derived from `data/original-controlled-initial/ledger.json`; no provider calls. Counts are descriptive and repeated rounds are not independent observations.

| cell | complete trajectories | round-1 ties | assessment ties / rounds | assessment states |
|---|---:|---:|---:|---|
| HH-hide_rival | 47 | 47 | 940 / 940 | `{'(6.5,6.5)': 940}` |
| HH-natural | 48 | 48 | 960 / 960 | `{'(6.5,6.5)': 960}` |
| HL-hide_rival | 48 | 1 | 0 / 960 | `{'(6.5,6)': 960}` |
| HL-natural | 48 | 31 | 819 / 960 | `{'(6,6)': 793, '(6.5,6)': 141, '(6.5,6.5)': 26}` |
| LH-hide_rival | 47 | 0 | 0 / 940 | `{'(6,6.5)': 940}` |
| LH-natural | 48 | 23 | 852 / 960 | `{'(6,6)': 832, '(6,6.5)': 108, '(6.5,6.5)': 20}` |
| LL-hide_rival | 48 | 48 | 960 / 960 | `{'(6,6)': 960}` |
| LL-natural | 46 | 46 | 920 / 920 | `{'(6,6)': 920}` |

## Tie-formation directions

- `HH-hide_rival`: `{}`
- `HH-natural`: `{}`
- `HL-hide_rival`: `{'upward_matching': 1}`
- `HL-natural`: `{'downward_matching': 57, 'upward_matching': 4}`
- `LH-hide_rival`: `{}`
- `LH-natural`: `{'downward_matching': 45, 'upward_matching': 1}`
- `LL-hide_rival`: `{}`
- `LL-natural`: `{}`

The ledger intentionally excludes provider request IDs and model-call metadata.
