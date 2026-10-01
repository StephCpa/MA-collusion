"""Consistency gate for the paper-facing materials.

Fails (exit 1) if any of the following drift:

1. the settlement certificate or the Candidate A reproduction no longer passes;
2. a number quoted in the manuscript no longer matches the analysis file it is
   derived from (each claim below names its source);
3. a citation key is missing from the bibliography, or a figure is missing;
4. a private path, user name, e-mail address or key-like string appears in any
   text file of the materials or the supplement ZIP;
5. (optional, with --pdf) the compiled staging PDF exceeds 8 pages or reports
   overfull boxes.

Offline only.  Run from the repository root:

    python paper-materials/aamas2027/tools/check_materials.py [--pdf path/to/build.pdf --log path/to/build.log]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
MATERIALS = HERE.parent
TEX = MATERIALS / "latex" / "history-display-observability.tex"
BIB = MATERIALS / "latex" / "history-display-observability.bib"
FIGURES = MATERIALS / "figures"
ORIGINAL = MATERIALS / "analysis" / "controlled-initial-followup-analysis.json"
REPLICATION = MATERIALS / "analysis" / "A-confirmation-structural-20261001.json"
CERTIFICATE = MATERIALS / "analysis" / "observability-certificate.json"
FOUR_ARM = MATERIALS / "analysis" / "four-arm-leading-indicator-20261001.json"
SETTLEMENT = MATERIALS / "analysis" / "settlement-generalization-20261001.json"
FROZEN_FOUR_ARM = MATERIALS / "data" / "four-arm-history-channel" / "analysis.json"

sys.path.insert(0, str(HERE))
import candidate_a_structural  # noqa: E402
import four_arm_leading_indicator  # noqa: E402
import observability_certificate  # noqa: E402
import settlement_generalization  # noqa: E402

PRIVATE = re.compile(
    rb"[A-Za-z]:\\\\(?:Users|work)|[A-Za-z]:/Users/|/home/[a-z]|/Users/[A-Za-z]|anaconda3|"
    rb"[\w.+-]+@[\w-]+\.(?:edu|com|org|cn|net)\b|sk-[A-Za-z0-9]{20,}"
)
TEXT_SUFFIXES = {".md", ".tex", ".bib", ".json", ".py", ".txt", ".csv"}


def f(x: float, nd: int = 3) -> str:
    return f"{x:.{nd}f}"


def interval(ci: list[float], nd: int = 3) -> list[str]:
    return [f(ci[0], nd), f(ci[1], nd)]


def claims() -> list[tuple[str, list[str]]]:
    """(source description, strings that must appear in the manuscript)."""
    orig = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    rep = json.loads(REPLICATION.read_text(encoding="utf-8"))
    cert = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    out = []
    sens = orig["paired_block_sensitivity_natural_minus_hide_rival"]
    for cell in ("LH", "HL"):
        t = sens[cell]["tie"]
        out.append((f"original {cell} paired tie", [f(t["mean_natural_minus_hide_rival"]), *interval(t["t_interval_95"])]))
    for name in ("D_asym", "J"):
        r = orig["registered_context"][name]
        out.append((f"original {name}", [f(r["mean"]), *interval(r["planned_completion_range"])]))
    sp = rep["structural_primary"]
    for cell in ("LH", "HL"):
        out.append((f"replication {cell}", [f(sp[cell]["mean"]), *interval(sp[cell]["block_t_95"])]))
    d = sp["D_tie"]
    out.append(("replication D_tie", [f(d["mean"]), *interval(d["block_t_95"]), *interval(d["completion_range"])]))
    for name in ("D_asym", "J"):
        r = rep["registered_welfare"][name]
        out.append((f"replication {name}", [f(r["mean"]), *interval(r["bonferroni_block_t_95"]),
                                            *interval(r["completion_range"]["full_grid_welfare_support"])]))
    cells = rep["cells"]
    for name in ("LH-natural", "HL-natural"):
        eq = cells[name]["assessment_equal_rounds"]
        out.append((f"replication {name} equal rounds", [f"{eq[0]}/{eq[1]}"]))
    out.append(("replication round-1 ties",
                [f"{cells['LH-natural']['round1_states'].get('(6,6)', 0)}/{cells['LH-natural']['completed']}",
                 f"{cells['HL-natural']['round1_states'].get('(6,6)', 0)}/{cells['HL-natural']['completed']}"]))
    led = cert["ledger_validation"]
    out.append(("certificate ledger validation", [f"{led['rounds_checked']:,}"]))
    gate = cert["operating_point_gate"]
    out.append(("certificate benchmarks", [f(gate["stage_nash_profit_per_seller"]), f(gate["joint_profit_per_seller"]),
                                           f(gate["symmetric_ties"]["6.0"]["calvano_delta"]),
                                           f(gate["symmetric_ties"]["6.5"]["calvano_delta"])]))
    four = json.loads(FOUR_ARM.read_text(encoding="utf-8"))
    frozen = json.loads(FROZEN_FOUR_ARM.read_text(encoding="utf-8"))["contrasts"]
    con = four["registered_reproduction"]["contrasts"]
    out.append(("four-arm registered contrasts", [f(con["interaction"]), f(con["simple_hide_rival_minus_natural"]),
                                                  f(-con["simple_hide_both_minus_hide_own"]),
                                                  *interval(frozen["interaction"]["complete_primary_interval"])]))
    li = four["leading_indicator"]["four_arm_model_chosen_start"]
    nat = li["natural"]
    out.append(("four-arm leading indicator, natural",
                [f(abs(nat["capture_minus_tie_welfare"]), 2), *interval(nat["welch_95"], 2),
                 f"{nat['trajectories_mostly_at_m6.5']['capture']} of {nat['n']['capture']}", f"{nat['n']['tie']} tie"]))
    out.append(("four-arm leading indicator, hide-own and hide-rival",
                [f(li["hide_own"]["capture_minus_tie_welfare"], 2), f(li["hide_rival"]["capture_minus_tie_welfare"], 2),
                 *interval(li["hide_rival"]["welch_95"], 2)]))
    prog = four["leading_indicator"]["replication_programmed_start"]["natural"]
    out.append(("programmed-start split", [f(prog["capture_minus_tie_welfare"], 2), *interval(prog["welch_95"], 2)]))
    tf = four["arms"]["natural"]["tie_formation"]
    out.append(("four-arm tie formation", [f"{tf['upward']} times against {tf['downward']} downward"]))
    blind = {(b["study"], b["contrast"]): b["blind_share"] for b in four["blindness_metric"]}
    controlled = [v for (st, _), v in blind.items() if st.startswith("controlled")]
    out.append(("blindness metric", [f"{round(100 * min(controlled))}--{round(100 * max(controlled))}\\%",
                                     f"{round(100 * blind[('four-arm (model-chosen start)', 'natural vs hide-rival')])}\\%"]))
    gen = json.loads(SETTLEMENT.read_text(encoding="utf-8"))
    shares = [row["blind_share"] for row in gen["n_sellers_homogeneous_bertrand"]]
    out.append(("settlement generalization", [*(f(x) for x in shares),
                                              f"\\theta\\ge{gen['theta_needed_to_resolve_tie_vs_capture']['0.01']:.2f}"]))
    return out


def check_claims(tex: str) -> list[str]:
    errors = []
    for source, needles in claims():
        for needle in needles:
            # Negative numbers are typeset as $-x$ in the manuscript.
            variants = {needle, needle.replace("-", "$-") + "$" if needle.startswith("-") else needle}
            if not any(v in tex for v in variants):
                errors.append(f"manuscript does not quote {needle!r} from {source}")
    return errors


def check_latex(tex: str) -> list[str]:
    errors = []
    bib = BIB.read_text(encoding="utf-8")
    cited = {k.strip() for g in re.findall(r"\\cite\{([^}]+)\}", tex) for k in g.split(",")}
    keys = set(re.findall(r"^@\w+\{([^,]+),", bib, flags=re.M))
    errors += [f"undefined citation {k}" for k in sorted(cited - keys)]
    for name in re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex):
        if not (FIGURES / name).exists():
            errors.append(f"missing figure {name}")
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S)
    words = len(re.findall(r"\b[\w'-]+\b", abstract.group(1))) if abstract else 0
    if not 100 <= words <= 300:
        errors.append(f"abstract has {words} words")
    if "anonymous" not in tex.lower():
        errors.append("anonymous review option missing")
    return errors


def check_private() -> list[str]:
    errors = []
    for path in sorted(MATERIALS.rglob("*")):
        if path.is_file() and path.suffix in TEXT_SUFFIXES and path.name != "check_materials.py":
            hit = PRIVATE.search(path.read_bytes())
            if hit:
                errors.append(f"private pattern {hit.group(0)[:40]!r} in {path.relative_to(MATERIALS)}")
        if path.is_file() and path.suffix == ".zip":
            with zipfile.ZipFile(path) as zf:
                for name in zf.namelist():
                    if name.endswith("check_materials.py") or name.endswith("audit_aamas_submission.py"):
                        continue
                    hit = PRIVATE.search(zf.read(name))
                    if hit:
                        errors.append(f"private pattern {hit.group(0)[:40]!r} in {path.name}:{name}")
    return errors


def check_pdf(pdf: Path, log: Path | None) -> list[str]:
    errors = []
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True, errors="replace")
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    if pages > 8:
        errors.append(f"staging PDF has {pages} pages")
    if log is not None:
        text = log.read_text(encoding="utf-8", errors="replace")
        if "Overfull \\hbox" in text:
            errors.append("overfull hbox in LaTeX log")
        if re.search(r"undefined (citations|references)", text, re.I):
            errors.append("undefined citations or references in LaTeX log")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--log", type=Path)
    args = parser.parse_args()
    errors: list[str] = []
    cert = observability_certificate.build()
    try:
        observability_certificate.check(cert)
    except AssertionError as exc:
        errors.append(f"certificate: {exc!r}")
    for name, module in (("candidate A reproduction", candidate_a_structural),
                         ("four-arm reproduction", four_arm_leading_indicator),
                         ("settlement generalization", settlement_generalization)):
        try:
            module.check(module.build())
        except AssertionError as exc:
            errors.append(f"{name}: {exc!r}")
    tex = TEX.read_text(encoding="utf-8")
    errors += check_claims(tex)
    errors += check_latex(tex)
    errors += check_private()
    if args.pdf:
        errors += check_pdf(args.pdf, args.log)
    for e in errors:
        print(f"FAIL  {e}")
    print(json.dumps({"passed": not errors, "failures": len(errors)}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
