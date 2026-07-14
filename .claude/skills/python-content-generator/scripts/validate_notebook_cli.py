#!/usr/bin/env python3
"""
validate_notebook_cli.py — CLI validation tool for Phase 2a Python notebooks.

Usage:
    python3 validate_notebook_cli.py \
        --notebook <path-to-ipynb> \
        --week <1-8> \
        --context <path-to-week-NN-context.json> \
        --output <path-to-write-validation.json>

Exits 0 for pass, 1 for fail.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


SECTION_MARKERS = {
    "has_title_and_objectives": [
        "learning objectives", "by the end of this session", "week "
    ],
    "has_business_hook": [
        "in the olist dataset", "olist"
    ],
    "has_going_deeper": [
        "going deeper", "advanced", "edge case", "extension"
    ],
    "has_common_mistakes": [
        "common mistake", "common mistakes", "# wrong", "# correct",
        "typeerror", "nameerror", "raises", "valueerror"
    ],
    "has_mini_challenge": [
        "mini-challenge", "mini challenge", "challenge", "⏱", "your turn"
    ],
    "has_group_exercise": [
        "group exercise", "group activity"
    ],
    "has_summary_and_preview": [
        "session summary", "coming up", "summary table", "what we covered"
    ],
}

CELL_COUNT_LIMITS = {
    "demo":      (20, 30),
    "exercises": (14, 22),
    "solutions": (14, 22),
}


def get_cell_text(cell):
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


def determine_notebook_type(notebook_path: str) -> str:
    name = Path(notebook_path).stem.lower()
    if "solution" in name:
        return "solutions"
    if "exercise" in name:
        return "exercises"
    return "demo"


def determine_day(notebook_path: str) -> str:
    name = Path(notebook_path).stem.lower()
    if "thu" in name or "thursday" in name:
        return "thu"
    return "wed"


def check_structure_demo(nb_cells, ctx):
    """Check 8-section structure for demo notebooks."""
    md_texts = [
        get_cell_text(c).lower()
        for c in nb_cells
        if c.get("cell_type") == "markdown"
    ]
    all_md = " ".join(md_texts)
    code_count = sum(1 for c in nb_cells if c.get("cell_type") == "code")

    structure = {}
    for section, markers in SECTION_MARKERS.items():
        structure[section] = any(m in all_md for m in markers)

    # §3: heuristic — at least 4 code cells indicates concepts + code pairs
    structure["has_concept_intro_with_code"] = code_count >= 4

    # Cross-check group exercise against context bundle text
    for day_key in ("wednesday", "thursday"):
        ge = (ctx.get(day_key) or {}).get("group_exercise", "")
        if ge and ge[:30].lower() in all_md:
            structure["has_group_exercise"] = True
            break

    missing = [k for k, v in structure.items() if not v]
    return structure, missing


def check_structure_exercises(nb_cells):
    """Check 5-part structure for exercise/solution notebooks."""
    md_texts = [
        get_cell_text(c).lower()
        for c in nb_cells
        if c.get("cell_type") == "markdown"
    ]
    all_md = " ".join(md_texts)

    structure = {
        "has_title": any(m in all_md for m in ["week ", "exercise", "instructor use only"]),
        "has_data_setup": any(m in all_md for m in ["data", "import", "load", "setup"]),
        "has_questions": sum(
            1 for t in md_texts
            if any(m in t for m in ["question", "task", "part ", "exercise "])
        ) >= 2,
        "has_group_exercise": any(
            m in all_md for m in ["group exercise", "group activity"]
        ),
    }
    missing = [k for k, v in structure.items() if not v]
    return structure, missing


def _strip_ipython_magics(source):
    """Drop IPython line-magic (%...) and shell-escape (!...) lines so the
    remainder can be checked as plain Python. A real kernel (used in
    execution_check) interprets these lines natively; compile() cannot."""
    kept = [line for line in source.split("\n") if not line.strip().startswith(("!", "%"))]
    return "\n".join(kept)


def syntax_check_cells(nb_cells):
    failures = []
    for i, cell in enumerate(nb_cells):
        if cell.get("cell_type") != "code":
            continue
        source = get_cell_text(cell)
        if not source.strip():
            continue
        stripped = source.lstrip()
        if stripped.startswith("%%writefile"):
            # %%writefile is an IPython cell magic: the first line names the
            # target file, everything after is literal file content (usually
            # a Python app). Check that content, not the magic line itself —
            # a real kernel (used in execution_check) handles the magic fine.
            source = source.split("\n", 1)[1] if "\n" in source else ""
            if not source.strip():
                continue
        elif stripped.startswith("%%"):
            # Other cell magics (e.g. %%bash, %%time): the whole cell body is
            # not standalone Python — defer to the real kernel in execution_check.
            continue
        else:
            source = _strip_ipython_magics(source)
            if not source.strip():
                continue
        try:
            compile(source, f"<cell_{i}>", "exec")
        except SyntaxError as e:
            failures.append({
                "cell_index": i,
                "cell_source_snippet": source[:100],
                "error_type": "syntax_error",
                "expected": "valid Python syntax",
                "actual": str(e),
                "fix_hint": f"Fix syntax on line {e.lineno}: {e.msg}",
            })
    return failures


def execution_check(notebook_path: str):
    """Execute notebook via nbconvert on a path-patched copy. Returns (exec_path, error)."""
    # OLIST_DATA_PATH is set before running the Routine's validation step.
    # It points to the directory where phase-2-python-sql.zip was extracted.
    olist_data_path = os.environ.get("OLIST_DATA_PATH", "/tmp/olist_data")

    with open(notebook_path) as f:
        nb = json.load(f)

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            src = get_cell_text(cell)

            # Remove Colab-only lines that fail outside Colab
            src = src.replace(
                "from google.colab import drive",
                "# removed for validation — not in Colab",
            )
            src = src.replace(
                "drive.mount('/content/drive')",
                "# removed for validation — not in Colab",
            )

            # Patch the olist_path variable to point to the locally extracted folder
            src = src.replace(
                "olist_path = '/content/drive/MyDrive/olist-data'",
                f"olist_path = '{olist_data_path}'",
            )
            src = src.replace(
                'olist_path = "/content/drive/MyDrive/olist-data"',
                f'olist_path = "{olist_data_path}"',
            )

            cell["source"] = src

    with tempfile.NamedTemporaryFile(suffix=".ipynb", mode="w", delete=False) as tmp:
        json.dump(nb, tmp)
        tmp_path = tmp.name

    out_path = tmp_path.replace(".ipynb", "-executed.ipynb")
    try:
        result = subprocess.run(
            [
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--ExecutePreprocessor.timeout=60",
                "--ExecutePreprocessor.kernel_name=python3",
                "--output", out_path,
                tmp_path,
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode != 0:
            return None, result.stderr[-1000:]
        return out_path, None
    except subprocess.TimeoutExpired:
        return None, "nbconvert timed out after 300s"
    except FileNotFoundError:
        return None, "jupyter/nbconvert not installed — run: pip install nbconvert jupyter_client ipykernel"
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def parse_execution_failures(executed_path: str, original_cells):
    failures = []
    try:
        with open(executed_path) as f:
            exec_nb = json.load(f)
    except Exception as e:
        return [{"cell_index": 0, "error_type": "parse_error",
                 "expected": "executed notebook", "actual": str(e), "fix_hint": ""}]

    for i, cell in enumerate(exec_nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                ename = output.get("ename", "")
                evalue = output.get("evalue", "")
                src = get_cell_text(original_cells[i]) if i < len(original_cells) else ""
                failures.append({
                    "cell_index": i,
                    "cell_source_snippet": src[:100],
                    "error_type": "runtime_error",
                    "expected": "successful execution",
                    "actual": f"{ename}: {evalue}",
                    "fix_hint": f"Runtime error in cell {i} — check variable definitions and imports above",
                })
    return failures


def build_rework_notes(failures, cell_count_ok, total_cells, min_cells, max_cells=None):
    parts = []
    for i, f in enumerate(failures, 1):
        ci = f.get("cell_index")
        snip = (f.get("cell_source_snippet") or "")[:60]
        et = f.get("error_type", "")
        hint = f.get("fix_hint", "")
        if ci is not None:
            parts.append(f"{i}. Cell {ci} ({snip!r}): {et} — {hint}")
        else:
            parts.append(f"{i}. {et}: {hint}")
    if not cell_count_ok:
        n = len(parts) + 1
        if max_cells is not None and total_cells > max_cells:
            over = total_cells - max_cells
            parts.append(
                f"{n}. Cell count {total_cells} above maximum {max_cells}: "
                f"trim {over} cells (merge or cut lower-priority content)"
            )
        else:
            diff = min_cells - total_cells
            parts.append(
                f"{n}. Cell count {total_cells} below minimum {min_cells}: "
                f"add {diff} more cells to §3 or §4"
            )
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Validate a Phase 2a Python notebook")
    parser.add_argument("--notebook", required=True)
    parser.add_argument("--week", type=int, required=True)
    parser.add_argument("--context", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    try:
        with open(args.notebook) as f:
            nb = json.load(f)
    except Exception as e:
        print(f"❌ Cannot open notebook: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.context) as f:
            ctx = json.load(f)
    except Exception as e:
        print(f"❌ Cannot open context bundle: {e}", file=sys.stderr)
        sys.exit(1)

    nb_cells = nb.get("cells", [])
    nb_type = determine_notebook_type(args.notebook)
    day = determine_day(args.notebook)
    week = args.week

    failures = []

    # --- Structural check ---
    if nb_type == "demo":
        structure_check, missing = check_structure_demo(nb_cells, ctx)
    else:
        structure_check, missing = check_structure_exercises(nb_cells)

    for section in missing:
        failures.append({
            "cell_index": None,
            "cell_source_snippet": "",
            "error_type": "missing_section",
            "expected": f"Section '{section}' present",
            "actual": "Section not found in notebook",
            "fix_hint": f"Add the required section: {section}",
        })

    # --- Syntax check (all weeks) ---
    syntax_failures = syntax_check_cells(nb_cells)
    failures.extend(syntax_failures)

    # --- Execution check (Weeks 3+ demo/solutions only, skipped if syntax errors) ---
    executed_count = 0
    if week >= 3 and nb_type in ("demo", "solutions") and not syntax_failures:
        exec_path, exec_error = execution_check(args.notebook)
        if exec_error:
            failures.append({
                "cell_index": None,
                "cell_source_snippet": "",
                "error_type": "execution_failed",
                "expected": "Notebook executes without errors",
                "actual": exec_error,
                "fix_hint": "Fix the error and re-validate",
            })
        elif exec_path:
            exec_failures = parse_execution_failures(exec_path, nb_cells)
            failures.extend(exec_failures)
            executed_count = sum(1 for c in nb_cells if c.get("cell_type") == "code")
            try:
                os.unlink(exec_path)
            except OSError:
                pass

    # --- Cell count check ---
    total_cells = len(nb_cells)
    min_cells, max_cells = CELL_COUNT_LIMITS.get(nb_type, (14, 30))
    cell_count_ok = min_cells <= total_cells <= max_cells

    # --- Compile rework_notes ---
    rework_notes = build_rework_notes(failures, cell_count_ok, total_cells, min_cells, max_cells)

    status = "pass" if not failures and cell_count_ok else "fail"

    report = {
        "notebook_path": str(args.notebook),
        "notebook_type": nb_type,
        "day": day,
        "week": week,
        "status": status,
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "cells_checked": total_cells,
        "code_cells_executed": executed_count,
        "failures": failures,
        "structure_check": structure_check,
        "cell_count": total_cells,
        "cell_count_ok": cell_count_ok,
        "rework_notes": rework_notes,
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)

    if status == "pass":
        print(f"✅ Validation PASSED: {args.notebook} ({total_cells} cells, 0 failures)")
    else:
        print(f"❌ Validation FAILED: {args.notebook}")
        print(f"   Failures: {len(failures)} | Cell count OK: {cell_count_ok}")
        print(f"   Report: {args.output}")
        if rework_notes:
            preview = rework_notes[:300]
            print(f"   Rework notes: {preview}{'...' if len(rework_notes) > 300 else ''}")

    sys.exit(0 if status == "pass" else 1)


if __name__ == "__main__":
    main()
