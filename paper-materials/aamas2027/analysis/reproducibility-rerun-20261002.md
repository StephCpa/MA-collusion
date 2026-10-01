# Reproducibility rerun — 2026-10-02

This record captures a fresh offline rerun after the claim--evidence matrix was
added. It is a verification log, not a new inferential analysis.

| check | result |
|---|---|
| `observability_certificate.py --check` | passed; 10 T1 classes; 11,375 ledger rounds re-settled; separating observables: `equal_price`, `profit_hhi`, `seller_a_profit`, `seller_b_profit`, `share_disparity` |
| `candidate_a_structural.py --check` | passed; `D_tie=0.830357`; block-t 95% `[0.743426, 0.917289]`; completion range `[0.791667, 0.841146]` |
| `four_arm_leading_indicator.py --check` | passed; natural capture-minus-tie `-27.941667`; blindness metrics reproduced |
| `structural_leave_one_block_out.py` | 42 complete blocks; full mean `0.830357`; leave-one-out range `[0.826220, 0.850000]`; all positive |
| `verify_supplement.py` | passed; 105 archive entries; 104 manifest files; zero hash mismatches; zero metadata-key hits |
| project regression (`pytest -q`) | 386 passed in 64.19 s |

All checks were run from the local candidate workspace. The rerun confirms
that the manuscript-facing numbers and the sealed public package remain
aligned; it does not upgrade any descriptive or boundary-limited result to a
causal or strategic claim.
