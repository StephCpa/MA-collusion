# Reproducibility metadata register

This register consolidates the metadata that are already present in the frozen
X1/X2 ledgers and explicitly marks fields that must be captured before any new
paid confirmation batch. It is not a substitute for the raw request records.

## Frozen X1/X2 runs

| field | X1 replacement | X2 forced deviation |
|---|---|---|
| run identifier | `x1-live-replacement-20260930T0628+0800` | `x2-live-20260930T0638+0800` |
| requested model alias | `deepseek-flash` | `deepseek-flash` |
| returned fingerprint | `aeb56401ca74e127821c4f9126dcb669` | `aeb56401ca74e127821c4f9126dcb669` |
| temperature | 0.3 | 0.3 |
| max output tokens | 256 | 256 |
| thinking mode | recorded in manifest | recorded in plan and request rows |
| schedule seed | 2026093001 | 2026093002 |
| request retries/repair | replacement run has no reused logical IDs; see ledger | no retries, no repair |
| planned calls | 576 | 7,680 |

The complete prompts, rendered schemas, request order and response rows remain
in the corresponding frozen run directories. The first timed-out X1 launch is
quarantined and excluded.

## Fields required before Candidate A or B

The pre-launch manifest must additionally record: provider endpoint family,
SDK and API-version identifiers, exact system/developer prompt hashes, schema
hashes for every arm, history truncation/rebuild rules, thinking configuration
including null versus disabled state, execution start/end timestamps, request
ordering, concurrency setting, stop and retry policy, price quote timestamp,
and the returned model/fingerprint distribution. Missing values must be
written as `not captured`, never inferred after the fact.

## Status

X1/X2 are reproducible from their sealed artifacts for the reported analyses,
but the API/SDK version fields were not uniformly captured in the original
manifests. Therefore M11 remains a submission gate for any new paid run. This
register closes the documentation gap without upgrading the evidential claim
or authorizing a new call.
