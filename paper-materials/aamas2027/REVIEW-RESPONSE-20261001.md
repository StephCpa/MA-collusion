# Response to review and revision record (2026-10-01)

**Scope.** No separate reviewer report was attached to the revision request.
This response therefore covers the latest review on record, the review of the
supervision-target map v0.1 (items 1–7 below and its "preserve" list), together
with every issue found in a full audit of the materials against the sealed
ledger and frozen analyses. If a separate reviewer report exists, it should be
added here and answered point by point.

No provider calls were made. The frozen `data/A-confirmation-analysis.json` was
read and reproduced but not modified.

## Headline change

The Candidate A independent replication had finished but was not in the
manuscript. Its result record also mislabeled the four
`descriptive_deltas` (0, 0, 0.4213, 0). The record called them "equal-price
persistence" and concluded that A "does not independently confirm a positive
general tie effect". In fact those values are hide-rival-minus-natural
**welfare** deltas. The protocol's structural primary had not been computed. It
is now computed from the sealed ledger by `tools/candidate_a_structural.py`,
which also reproduces every frozen number exactly:

| contrast | blocks | mean | 95% block-t | + / 0 / − | completion range |
|---|---:|---:|---|---|---|
| LH | 45 | 0.819 | [0.712, 0.926] | 42 / 3 / 0 | — |
| HL | 45 | 0.842 | [0.739, 0.945] | 41 / 4 / 0 | — |
| D_tie | 42 | 0.830 | [0.743, 0.917] | 42 / 0 / 0 | [0.792, 0.841] |

The structural decision rule is met. The welfare-equivalence decision stays
inconclusive: the completion range for J, [−4.891, 5.688], exceeds δ_W = 5. The
replication now appears in the abstract, the contributions, §4.3, §5.4, Table 4,
Figure 2 and the limitations. It is described as within-deployment (same alias
and fingerprint on all 21,982 logged calls), not cross-model. The amended
execution is disclosed, including the interim-result inspection before the
continuation.

## Point-by-point: review of supervision-target map v0.1

| # | Comment | Change | Where |
|---|---|---|---|
| 1 | The certificate listed only `profit_hhi` as differing between (6.0, 6.5) and (6.0, 6.0); the two seller profits also differ. | The separating set is now **derived**, not listed. It is `seller_a_profit`, `seller_b_profit`, `profit_hhi`, `equal_price` and `share_disparity`. The paper names the two seller profits as the primitive observables and HHI as a derived one. | `tools/observability_certificate.py`, `analysis/observability-certificate.*`, manuscript §3.1 |
| 2 | The validator asserted hand-listed comparisons. | The suggested fix is implemented: the same/different partition is computed, and the script asserts disjointness, non-emptiness and full coverage. In every non-singleton class, the varying observables are checked to equal exactly the seller-level set. | `observability_certificate.py: pair_certificate, check` |
| 3 | Class collapse: 100 → 10, the 6.5 class a singleton, HHI spanning 0.50–1.00. | The full 10-class table is generated with exact rational arithmetic. In Table 1, the "HHI range 0.50–1.00" column, which implied a continuum, became "HHI values {0.50, 1.00}" ({0.50} for the singleton). | `analysis/observability-certificate.md`, Table 1 |
| 4 | T3 direction: HHI 1.0 is capture, HHI 0.5 is equal division (the cartel-like pattern). | T3 is split into **T3a capture concentration** and **T3b market division**. Results and the Discussion report direction: under natural display the asymmetric cells move from T3a toward T3b. | §3.2, Table 2, §5.1, §6 |
| 5 | T1 wording: "structurally unidentified in 3 of 4 cells". | **Partly withdrawn.** Randomization identifies the welfare treatment effect in every cell, so "unidentified" was too strong. What is limited is the support, which is pinned at m ∈ {6.0, 6.5}. The manuscript keeps the accurate wording: "estimable under the block design; … small because assessment-window support is pinned". | Table 2 |
| 6 | T4 is vacuous at the current operating point because both observed symmetric states lie above the 5.5 joint-profit optimum. | Added an arithmetic **operating-point gate** with three conditions: (i) the tie beats grid-Nash, (ii) a profitable deviation exists, and (iii) the tie is at or below the joint-profit price. The observed 6.0/6.5 ties and the X2 (6.0, 6.0) prelude pass (i)–(ii) and fail (iii). At (6.0, 6.0) the forced 5.5 is both the best one-shot deviation and the joint-profit price. Condition (iii) is stated as a design condition, not a theorem, because repeated-game arguments can sustain ties above the joint-profit price. The ties at 2.5–5.5 pass the gate. | §3.2, Table 2, §5.7, §6, Conclusion; gate table in `observability-certificate.md` |
| 7a | The validator hard-codes substantive findings. | `tools/check_materials.py` derives every quoted number from its analysis JSON and fails on drift. A negative test confirmed that it catches changed numbers, missing citations and private paths. | `tools/check_materials.py` |
| 7b | The certificate is not tied to recorded data. | All 11,375 recorded rounds of the replication ledger were re-settled, with 0 mismatches. | §4.5, certificate |
| 7c | Doc/manifest drift (the HHI 0.56–0.57 range is absent from the manifest). | HHI is exactly 1 − E/2 under tie-split, so it no longer appears as an independent result. The HHI panel was removed from Figure 2, and Table 4 omits HHI with a caption explaining why. Manuscript numbers are now gated against the analysis files. | Fig. 2, Table 4, `check_materials.py` |
| 7d | The gates lack a positive control and a minimum detectable effect. | The X2 design sensitivity is now stated (interactions of about 0.25–0.35 or larger). The hidden-rival X2 arms are identified as a structural negative control, because the shock is not displayed and N1 vs N0 is the informative contrast. A positive control for a T4 test needs a new paid run, so it is listed as an author action (A6). | §4.6, §5.7 |
| 7e | The E0–E4 tiers are unused. | Not added to the paper (page budget). T1–T4 plus the gate carry the claim boundary. The target-map document (not in this repository) should either map E0–E4 onto T1–T4 or drop them. | — |
| 7f | `closed_loop` flag missing. | The paper now separates closed-loop studies (controlled-initial, replication, X2) from single-shot ones (fixed-history, X1) in §4. The flag itself belongs in the target-map manifest, which is not in this repository. | §4 |

**Preserved as requested:**
- T2 or T3 alone is not collusion.
- No claims of absorbing states, anchoring or a false-negative rate. The one remaining "absorbing states" wording, in the offline baseline report, was removed. Anchoring is named only as an alternative the design cannot exclude.
- "Observationally equivalent under T1" is kept.
- The amended-execution disclosure is kept and extended to Candidate A.

## Corrections found in the audit

| ID | Issue | Fix |
|---|---|---|
| E1 | Candidate A result record mislabeled welfare deltas as equal-price persistence, and the protocol structural primary was never computed. | Corrected record with a correction note. New `A-confirmation-structural-20261001.*`. Protocol status line updated, with the frozen text preserved. |
| E2 | §5.3 said the 28/286 (LH) and 33/330 (HL) 6.5 choices were "upward moves by the initially low seller". Figure 3's own data, extracted from the PDF vectors, shows only 1 (LH) and 4 (HL) upward tie-formation events. The rest are continuations of a few (6.5, 6.5) ties. | Rewritten. |
| E3 | "The initially low seller changed at round 1 in … 4% of HL trajectories". The round-1 states give 1/48 (2%). The 4% belongs to the hide-rival arm. | Corrected to 2% in each cell. |
| E4 | "current tie-split profit from 222.222", but 222.222 is the capture profit. | "from the capture profit 222.222 to the tie-split profit 106.944". |
| E5 | The hide-rival conditional counts condition on a rival price the seller never sees. | Stated explicitly. These counts describe freezing, not a response. |
| E6 | "No next-round response … whether rival prices were visible or hidden" implied a symmetric test, but the hidden arms cannot display the shock. | Hidden arms described as a structural negative control. N1 vs N0 is the informative null. |
| E7 | The X1 qualification note labeled the BR gap "continuing-minus-terminal". The protocol and values are terminal-minus-continuing. | Label corrected; values unchanged. |
| E8 | Private local paths, including a Windows user directory and a local project directory, appeared in `controlled-initial-followup-analysis.json` and `-report.md`, which breaks the anonymity promise in the README. | Replaced with project-relative paths and `python`. No values changed. The anonymity scan now covers all text files and both ZIPs. |
| E9 | `\graphicspath` pointed to directories that do not exist in this repository, so the source did not compile from `latex/`. | Points to `../figures/`. |
| E10 | Figure 2 plotted the four-arm study's post-hoc contrast on the same axis as the registered contrasts (different study and estimand). Its interval also did not match the bootstrap interval in the text. Two axis labels overlapped. | Rebuilt as a validated two-series forest plot with both runs, completion ranges and the δ_W band, regenerated byte-reproducibly from the analysis files. |
| E11 | The original-run completion ranges and the four-arm registered factorial effect (4.053, [−0.314, 8.420]) were missing from the welfare section. | Added. |
| E12 | Table 1 "HHI range". | See item 3. |
| E13 | Bibliography: "Denicolo" lacked its accent; Leibo et al. and CAMEL were cited as arXiv-only. | Fixed; cited as AAMAS '17 and NeurIPS 2023. Added Arunachaleswaran et al. (ITCS 2025, supra-competitive prices without threats) and Motwani et al. (NeurIPS 2024, steganographic collusion over explicit channels), both checked against their venue listings. |
| E14 | Figures had no `\Description` (acmart accessibility warnings). | Added. |
| E15 | The supplement still carried E7 and the 0.974 Wilson wording in its evidence-to-claim audit. | Supplement v0.2 built with corrections, the replication ledger and the new tools, plus a regenerated SHA-256 manifest. v0.1 is kept unchanged. |

The page budget holds: the staging PDF is 8 pages including references, with no
overfull boxes and all citations resolved. The abstract is 242 words.

## Requires author action (not done here)

- **A1.** Attach the pre-launch record showing when δ_W = 5 was selected. The protocol requires this "before any call". Until then the paper calls δ_W = 5 the protocol's *candidate* margin.
- **A2.** Migrate to the official AAMAS 2027 template, then rerun `check_materials.py --pdf … --log …`. The acmart "CCS concepts / ACM reference format" warnings are template-specific.
- **A3.** This repository's commit metadata, and its owner name, are not anonymous. Do not link it from the submission; use an anonymized mirror if a supplement URL is needed.
- **A4.** The original controlled-initial ledger and the builder for Figures 1 and 3 (`research/build_paper_figures_20260928.py`) are not in these materials. Original-run descriptive numbers (first-change rates, ever-change rates, tie-formation counts) can therefore be checked only against the frozen JSON and figure, not re-derived. Consider adding them to the supplement.
- **A5.** The support convention behind the original run's completion ranges is not documented in the paper-facing files. The replication's convention is documented and verified: full grid support, with observed partial rounds retained.
- **A6.** A gate-passing T4 test needs a new paid run and explicit approval. That means a programmed 5.0 or 5.5 tie, a declared deviation and response rule, and a positive control. None was launched.
- **A7.** The ledger keeps provider request IDs (random UUIDs). Decide whether reviewers need them.

## Verification

```text
python paper-materials/aamas2027/tools/observability_certificate.py --check --write   # passed; 11,375 rounds, 0 mismatches
python paper-materials/aamas2027/tools/candidate_a_structural.py --check --write      # passed; frozen D_asym, J, ranges and deltas reproduced to 1e-9
python paper-materials/aamas2027/tools/build_fig2_replication.py                      # byte-identical PDF on rebuild
python paper-materials/aamas2027/tools/check_materials.py --pdf <pdf> --log <log>     # passed; 8 pages, no overfull boxes
```
