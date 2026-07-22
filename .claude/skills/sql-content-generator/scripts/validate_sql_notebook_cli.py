#!/usr/bin/env python3
"""
validate_sql_notebook_cli.py — CLI validation tool for Phase 2b SQL notebooks.

Usage:
    python3 validate_sql_notebook_cli.py \
        --notebook <path-to-ipynb> \
        --week <1-8> \
        --context <path-to-week-NN-context.json> \
        --output <path-to-write-validation.json>

Exits 0 for pass, 1 for fail.

SQL specifics (vs the Phase 2a Python validator this was adapted from):
- Queries use the `%%sql` cell magic (jupysql). The notebook's first code cell
  is sql_setup.py, which does `%load_ext sql` and connects jupysql to a
  file-based SQLite DB. As long as `jupysql` + `prettytable` are installed,
  `jupyter nbconvert --execute` runs these cells natively.
- Path patching: at execution time we rewrite the setup cell's
  DATA_DIR (Drive path) to the locally extracted Olist CSV dir, DB_PATH to a
  fresh tempfile .db, and comment out the google.colab drive import + mount.
- Check-cell gate: exercise notebooks have blank answer cells (cannot run
  green), so execution runs only on SOLUTIONS (and demo). A solutions notebook
  is only "pass" if nbconvert produced ZERO cell errors — which means every
  `assert` in the plain-Python check cells passed. An AssertionError surfaced
  during execution is classified as `check_failed` (not generic runtime_error)
  and named by cell, so a wrong expected value or wrong query is caught.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


# Tables with MANY rows per order_id. Directly joining two of these (or one of
# them onto a fact column you then aggregate) fans out rows and inflates SUM/AVG/
# COUNT(*). Verified grains (see references/olist_schema.md → "Join cardinality"):
#   order_items    112,650 rows / 98,666 distinct order_id
#   order_payments 103,886 rows / 99,440 distinct order_id
#   order_reviews   99,224 rows / 98,673 distinct order_id
FANOUT_FACT_TABLES = ("order_items", "order_payments", "order_reviews")


# 8-section teaching structure markers (demo notebooks).
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
        "common mistake", "common mistakes", "-- wrong", "-- correct",
        "# wrong", "# correct", "integer division", "= null", "syntax error",
        "no such column",
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

# Each self-checking question is ~3 cells (question markdown + %%sql answer +
# plain-Python check cell), so exercise/solution notebooks run larger.
CELL_COUNT_LIMITS = {
    "demo":      (20, 34),
    "exercises": (16, 30),
    "solutions": (16, 30),
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

    # §3: heuristic — at least 4 code cells indicates concepts + query pairs
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
    """Check the self-checking 3-cell-per-question pattern for
    exercise/solution notebooks: a setup cell, >=2 question markdowns, and
    check cells containing a "✅" / assert. Lenient but present."""
    md_texts = [
        get_cell_text(c).lower()
        for c in nb_cells
        if c.get("cell_type") == "markdown"
    ]
    code_texts = [
        get_cell_text(c)
        for c in nb_cells
        if c.get("cell_type") == "code"
    ]
    all_md = " ".join(md_texts)
    all_code = "\n".join(code_texts)

    # A setup cell: the first code cell loads data / connects jupysql.
    has_setup = any(
        m in c for c in code_texts
        for m in ("load_ext sql", "%sql sqlite", "sqlite3.connect", "DB_PATH", "DATA_DIR")
    )

    structure = {
        "has_title": any(m in all_md for m in ["week ", "exercise", "instructor use only"]),
        "has_data_setup": has_setup or any(
            m in all_md for m in ["data", "import", "load", "setup"]
        ),
        "has_questions": sum(
            1 for t in md_texts
            if any(m in t for m in ["question", "task", "part ", "exercise ", "q1", "q2"])
        ) >= 2,
        # Self-check cells: at least one plain-Python cell with an assert and a
        # "✅ Qn correct" style confirmation print.
        "has_check_cells": ("assert" in all_code) and ("✅" in all_code),
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
    """Static compile() check on code cells. Skips %%sql and other cell magics
    (their body is SQL, not Python) and strips inline !/% line magics."""
    failures = []
    for i, cell in enumerate(nb_cells):
        if cell.get("cell_type") != "code":
            continue
        source = get_cell_text(cell)
        if not source.strip():
            continue
        stripped = source.lstrip()
        if stripped.startswith("%%writefile"):
            # %%writefile: first line names the target file; the rest is literal
            # file content (usually a Python app). Check that content.
            source = source.split("\n", 1)[1] if "\n" in source else ""
            if not source.strip():
                continue
        elif stripped.startswith("%%"):
            # %%sql (and any other cell magic): the whole body is SQL / not
            # standalone Python — defer to the real kernel in execution_check.
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


def _sql_body(source):
    """Return the SQL of a %%sql cell with the magic header and comment lines
    removed, lower-cased. Non-%%sql cells return ''. Comment lines (`--`) are
    dropped so the deliberately-wrong SQL shown in the §6 "common mistakes"
    comment block never trips the lint."""
    stripped = source.lstrip()
    if not stripped.startswith("%%sql"):
        return ""
    body = source.split("\n", 1)[1] if "\n" in source else ""
    lines = []
    for line in body.split("\n"):
        code = line.split("--", 1)[0]  # drop trailing/whole-line SQL comments
        if code.strip():
            lines.append(code)
    return " ".join(lines).lower()


def _has_unsafe_aggregate(q):
    """True if the query aggregates in a way fan-out would corrupt: any SUM(/AVG(,
    or a COUNT( that is not COUNT(DISTINCT ...). COUNT(DISTINCT order_id) is
    fan-out-safe and does NOT count."""
    if re.search(r"\b(sum|avg)\s*\(", q):
        return True
    for m in re.finditer(r"\bcount\s*\(\s*([^)]*)", q):
        if not m.group(1).strip().startswith("distinct"):
            return True
    return False


def fanout_check(nb_cells):
    """Static lint for join fan-out. Flags a %%sql cell whose query directly
    references (FROM/JOIN) two or more of the many-per-order fact tables AND uses
    an unsafe aggregate — unless it pre-aggregates in a WITH CTE (the correct
    fix, which makes the raw table appear only inside the CTE). This catches the
    Phase 2a Week-7 defect where order_items JOIN order_reviews + SUM(price)
    double-counted category revenue."""
    failures = []
    for i, cell in enumerate(nb_cells):
        if cell.get("cell_type") != "code":
            continue
        q = _sql_body(get_cell_text(cell))
        if not q:
            continue
        # A WITH CTE is the sanctioned pre-aggregation escape hatch.
        if re.search(r"\bwith\b", q):
            continue
        present = {
            t for t in FANOUT_FACT_TABLES
            if re.search(r"\b(from|join)\s+" + t + r"\b", q)
        }
        if len(present) >= 2 and _has_unsafe_aggregate(q):
            joined = ", ".join(sorted(present))
            failures.append({
                "cell_index": i,
                "cell_source_snippet": get_cell_text(cell)[:100],
                "error_type": "fanout_risk",
                "expected": "aggregate over one-row-per-order grain (no join fan-out)",
                "actual": f"query joins {joined} directly and then aggregates",
                "fix_hint": (
                    f"Join fan-out: {joined} each hold many rows per order_id, so joining "
                    f"them directly multiplies rows and inflates SUM/AVG/COUNT(*). "
                    f"Pre-aggregate the non-base table(s) to one row per order_id in a WITH "
                    f"CTE before joining, and use COUNT(DISTINCT order_id). See "
                    f"references/olist_schema.md → 'Join cardinality & fan-out'."
                ),
            })
    return failures


def execution_check(notebook_path: str):
    """Execute notebook via nbconvert on a path-patched copy.
    Returns (exec_path, error)."""
    # OLIST_DATA_PATH points to the directory where phase-2-python-sql.zip was
    # extracted (the raw Olist CSVs). Set before running the validation step.
    olist_data_path = os.environ.get("OLIST_DATA_PATH", "/tmp/olist_data")

    # Fresh temp .db so we never collide with a real /content/olist.db.
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    os.unlink(db_path)  # let sqlite3 create it fresh

    with open(notebook_path) as f:
        nb = json.load(f)

    # The current setup cell (sql_setup.py) is Colab/local portable: it detects
    # "not Colab" via `try: import google.colab / except ModuleNotFoundError`,
    # reads the Olist CSV folder from $OLIST_DATA_PATH and the DB path from
    # $OLIST_DB_PATH, and connects via a SQLAlchemy engine variable. So no source
    # rewriting is needed here — we just pass those env vars to the kernel below.
    #
    # The string replacements below are a BACKWARD-COMPAT fallback for any older
    # notebook still carrying the hardcoded /content setup cell. They are no-ops
    # against the portable cell (the literal strings no longer appear).
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            src = get_cell_text(cell)

            # Neutralise Colab-only Drive lines (they fail outside Colab).
            src = src.replace(
                "from google.colab import drive",
                "# from google.colab import drive  # removed for validation",
            )
            src = src.replace(
                "drive.mount('/content/drive')",
                "# drive.mount('/content/drive')  # removed for validation",
            )
            src = src.replace(
                'drive.mount("/content/drive")',
                '# drive.mount("/content/drive")  # removed for validation',
            )

            # Point DATA_DIR at the locally extracted Olist CSV folder.
            src = src.replace(
                'DATA_DIR = "/content/drive/MyDrive/cohort7/datasets/olist"',
                f'DATA_DIR = "{olist_data_path}"',
            )
            src = src.replace(
                "DATA_DIR = '/content/drive/MyDrive/cohort7/datasets/olist'",
                f"DATA_DIR = '{olist_data_path}'",
            )

            # Point DB_PATH (pandas loader) at the temp .db.
            src = src.replace(
                'DB_PATH = "/content/olist.db"',
                f'DB_PATH = "{db_path}"',
            )
            src = src.replace(
                "DB_PATH = '/content/olist.db'",
                f"DB_PATH = '{db_path}'",
            )

            # Point jupysql's connection string at the same temp .db.
            # sqlite:////content/olist.db  ->  sqlite:////<abs temp path>
            src = src.replace(
                "sqlite:////content/olist.db",
                f"sqlite:///{db_path}",
            )

            cell["source"] = src

    with tempfile.NamedTemporaryFile(suffix=".ipynb", mode="w", delete=False) as tmp:
        json.dump(nb, tmp)
        tmp_path = tmp.name

    out_path = tmp_path.replace(".ipynb", "-executed.ipynb")
    # The portable setup cell reads these at runtime: OLIST_DATA_PATH → the raw
    # Olist CSV folder, OLIST_DB_PATH → the fresh temp .db to build/query.
    exec_env = os.environ.copy()
    exec_env["OLIST_DATA_PATH"] = olist_data_path
    exec_env["OLIST_DB_PATH"] = db_path
    try:
        result = subprocess.run(
            [
                "jupyter", "nbconvert",
                "--to", "notebook",
                "--execute",
                "--ExecutePreprocessor.timeout=90",
                "--ExecutePreprocessor.kernel_name=python3",
                "--output", out_path,
                tmp_path,
            ],
            capture_output=True,
            text=True,
            timeout=420,
            env=exec_env,
        )
        # nbconvert returns non-zero when a cell raises (including
        # AssertionError). We still want to parse per-cell errors from the
        # partially-executed notebook, so return the out_path if it exists.
        if result.returncode != 0 and not os.path.exists(out_path):
            return None, result.stderr[-1000:]
        return out_path, None
    except subprocess.TimeoutExpired:
        return None, "nbconvert timed out after 420s"
    except FileNotFoundError:
        return None, ("jupyter/nbconvert not installed — run: "
                      "pip install jupysql prettytable nbformat nbconvert jupyter_client ipykernel")
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        try:
            os.unlink(db_path)
        except OSError:
            pass


def parse_execution_failures(executed_path: str, original_cells):
    """Parse per-cell error outputs. AssertionError (from a self-check cell) is
    classified as `check_failed` and names the cell, so a wrong expected value
    or wrong query is caught distinctly from a generic runtime error."""
    failures = []
    try:
        with open(executed_path) as f:
            exec_nb = json.load(f)
    except Exception as e:
        return [{"cell_index": 0, "error_type": "parse_error",
                 "expected": "executed notebook", "actual": str(e), "fix_hint": ""}]

    exec_cells = exec_nb.get("cells", [])
    for i, cell in enumerate(exec_cells):
        if cell.get("cell_type") != "code":
            continue
        for output in cell.get("outputs", []):
            if output.get("output_type") == "error":
                ename = output.get("ename", "")
                evalue = output.get("evalue", "")
                src = get_cell_text(original_cells[i]) if i < len(original_cells) else ""
                if ename == "AssertionError":
                    # A self-check assert failed → wrong query result or wrong
                    # expected value in this notebook.
                    detail = evalue.strip() or "assertion failed (no message)"
                    failures.append({
                        "cell_index": i,
                        "cell_source_snippet": src[:100],
                        "error_type": "check_failed",
                        "expected": "self-check assert passes (query returns the verified value)",
                        "actual": f"AssertionError: {detail}",
                        "fix_hint": (
                            f"Check-cell {i} failed: the %%sql answer above it returned a value "
                            f"that does not match the asserted expected result. Fix the query or "
                            f"correct the expected value against the verified Olist stats."
                        ),
                    })
                else:
                    failures.append({
                        "cell_index": i,
                        "cell_source_snippet": src[:100],
                        "error_type": "runtime_error",
                        "expected": "successful execution",
                        "actual": f"{ename}: {evalue}",
                        "fix_hint": (
                            f"Runtime error in cell {i} — check the SQL (table/column names, "
                            f"SQLite syntax) and that the setup cell ran above"
                        ),
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
                f"add {diff} more cells (e.g. another question block or worked example)"
            )
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Validate a Phase 2b SQL notebook")
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

    # --- Syntax check (all weeks; %%sql cells are skipped) ---
    syntax_failures = syntax_check_cells(nb_cells)
    failures.extend(syntax_failures)

    # --- Join fan-out lint (all notebook types; demo/exercises/solutions) ---
    # Static guard against the Phase 2a Week-7 class of defect: aggregating a
    # fact column across a direct join of two many-per-order tables.
    fanout_failures = fanout_check(nb_cells)
    failures.extend(fanout_failures)

    # --- Execution check (demo/solutions only, skipped if syntax errors) ---
    # Exercise notebooks have blank %%sql answer cells; executing them would
    # trip every self-check assert, so they are never executed. Only solutions
    # (and demo) are run — a solutions notebook is "pass" only if nbconvert
    # produced ZERO cell errors, i.e. every check-cell assert passed.
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
    min_cells, max_cells = CELL_COUNT_LIMITS.get(nb_type, (16, 34))
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
