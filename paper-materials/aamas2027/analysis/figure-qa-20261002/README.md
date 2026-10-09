# Figure quality audit — 2026-10-02

Offline checks on the six figures used in the manuscript. The checks use the
open-source nature-figure audit scripts (`audit_pdf_text.py`,
`audit_figure_collisions.py`, `audit_panel_alignment.py`); they are not
redistributed here. No reported value changed as a result of the audit.

**Correction (2026-10-09).** The first version of this record said the audit
ran "at final size". It measured each PDF at its native size, and Figures 4
and 5 are scaled down in the manuscript (to 0.86 and 0.94 of the column
width), so their smallest text as placed is below the 5 pt floor. The table
now reports both sizes; Figures 4 and 5 still need enlarging.

| manuscript figure | file | smallest text, native | smallest text, as placed | collision audit | panel alignment |
|---|---|---:|---:|---|---|
| Figure 1 (redesigned 2026-10-09) | `fig1-framework-evidence-map.pdf` | 6.2 pt | 6.2 pt | 0 fail, 0 warn | not applicable (mixed diagram and data panels) |
| Figure 2 | `fig2-observability-boundary.pdf` | 5.4 pt | 5.5 pt | 0 fail, 4 warn | manual layout (colour bar and mixed panels) |
| Figure 3 | `fig-dynamics-structure-welfare.pdf` | 6.2 pt | 5.9 pt | 0 fail, 3 warn | PASS (`fig-dynamics-structure-welfare.alignment.json`) |
| Figure 4 | `fig2-welfare-versus-structure.pdf` | 5.25 pt | **4.6 pt** | 0 fail, 2 warn | single column |
| Figure 5 | `fig3-direction-and-leading-indicator.pdf` | 6.0 pt | **4.5 pt** | 0 fail, 4 warn | single column |
| Figure 6 | `fig-boundary-conditions.pdf` | 6.2 pt | 6.3 pt | 0 fail, 2 warn | PASS (`fig-boundary-conditions.alignment.json`) |

All warnings are `text-fill-edge` findings: a label partly overlaps the edge of
a filled background region by design. They were reviewed visually and left
in place:

- Figure 2: the three `W = 311.1` labels and the `6.5 tie` label sit at the
  edge of the panel background next to the bars they annotate.
- Figure 3: the legend entries and the panel C note sit on the assessment-window
  shading or the panel background.
- Figure 4: the two `0.71 (n=...)` labels sit inside the shaded candidate-margin band.
- Figure 5: the `n=tie/capture` count labels sit at the edge of the panel background.
- Figure 6: the "structure moves, welfare flat" annotation sits next to the legend frame.
- Figure 1 (2026-10-09 version): no warnings; both in-panel annotations sit wholly inside the assessment-window shading.

Rebuilding all six figures with `tools/build_*.py` reproduces byte-identical
PDFs. To repeat the alignment gate, set `NATURE_FIGURE_QA` to the directory
that contains `audit_panel_alignment.py`; `tools/figstyle.py` then writes the
alignment records into this folder.
