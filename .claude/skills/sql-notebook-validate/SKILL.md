---
name: sql-notebook-validate
description: >
  Validate a generated Phase 2b SQL notebook before it is committed.
  Calls the pre-committed validate_sql_notebook_cli.py script to execute
  %%sql cells against a local file-based SQLite Olist DB, check structure,
  and confirm every self-check assert passes. Reads the JSON result and
  surfaces rework_notes if validation fails. Used internally by
  /sql-content-generator.
---

# SQL Notebook Validator

Quality gate between notebook generation and git commit for Phase 2b SQL. Calls a pre-committed script — no reasoning about nbconvert or jupysql mechanics on every run.

SQL notebooks query a file-based SQLite database with the `%%sql` cell magic (jupysql). Each exercise question is a **three-cell block**: a question markdown, a `%%sql qN <<` answer cell, and a plain-Python check cell whose `assert`s print `✅ Qn correct`.

---

## Inputs

- **Notebook path**: absolute or repo-relative path to the `.ipynb` file
- **Context bundle path**: `.pipeline-cache/week-NN-context.json`
- **Week number** (for routing Week 1–2 syntax-only vs Week 3+ full execution)
- **Generation state path**: `.pipeline-cache/week-NN-generation-state.json` (for checkpoint writes)
- **Notebook key**: one of `wed-demo`, `wed-exercises`, `wed-solutions`, `thu-demo`, `thu-exercises`, `thu-solutions`

## Output

- Validation report at `.pipeline-cache/week-NN-{day}-{type}-validation.json`
- Returns `status: "pass"` or `status: "fail"` with `rework_notes`

---

## Step 0a — Install dependencies

The `%%sql` magic requires **jupysql** (and its `prettytable` dependency) installed in the kernel. The notebook's own setup cell runs `%load_ext sql`, so once jupysql is installed, `nbconvert --execute` runs the SQL cells natively.

```bash
pip install jupysql prettytable nbformat nbconvert jupyter_client ipykernel
```

Run this once before validating (idempotent — pip skips already-installed packages).

## Step 0b — Ensure Olist data is available (Weeks 3+ only)

For Weeks 1–2, skip this step entirely (syntax-only validation).

For Weeks 3–8: the script executes `%%sql` cells that read the Olist CSVs into SQLite. The raw CSVs must be on disk before running.

**Primary source — local zip** (always try this first):

```bash
if [ -d "/tmp/olist_data" ] && [ -n "$(ls /tmp/olist_data/*.csv 2>/dev/null)" ]; then
  echo "Olist data already available at /tmp/olist_data"
else
  LOCAL_ZIP="datasets/phase-2-python-sql.zip"
  if [ -f "$LOCAL_ZIP" ]; then
    echo "Extracting Olist data from local zip..."
    mkdir -p /tmp/olist_data
    unzip -q "$LOCAL_ZIP" -d /tmp/olist_data/
    echo "✅ Olist data extracted to /tmp/olist_data/"
  else
    echo "ERROR: datasets/phase-2-python-sql.zip not found — cannot validate execution"
    # Fall back to syntax-only check (see below)
  fi
fi

export OLIST_DATA_PATH="/tmp/olist_data"
```

`OLIST_DATA_PATH` must point at the directory holding the raw Olist CSVs (e.g. `olist_orders_dataset.csv`). The script reads this env var to patch the setup cell's `DATA_DIR`.

Do NOT use Google Drive MCP to download the zip — the file exceeds the 10 MB Drive MCP download limit. The local zip at `datasets/phase-2-python-sql.zip` is the canonical source.

**If the local zip is missing** (e.g. a fresh container without the repo):
1. Run structure check and syntax check only (skip nbconvert execution).
2. If both pass, write the report with `"status": "pass"` plus `"skipped_execution": true, "skipped_execution_reason": "datasets/phase-2-python-sql.zip not found"`.
3. Update the generation state checkpoint to `"validated"` as normal.
4. Log a warning but **do not abort the pipeline**.

---

## Step 1 — Derive output path

```python
from pathlib import Path
week_str = f"week-{week:02d}"
nb_name = Path(notebook_path).stem  # e.g. "week-03-wed-solutions"
output_path = f".pipeline-cache/{nb_name}-validation.json"
```

## Step 2 — Run the validation script

```bash
python3 .claude/skills/sql-content-generator/scripts/validate_sql_notebook_cli.py \
  --notebook "<notebook_path>" \
  --week <N> \
  --context ".pipeline-cache/week-NN-context.json" \
  --output "<output_path>"
```

The script exits 0 for pass, 1 for fail. It handles:
- **Structural check** — demo: the 8-section teaching markers; exercises/solutions: the three-cell-per-question pattern (a setup cell, ≥2 question markdowns, and check cells containing `assert` + `✅`).
- **Python syntax check** — `compile()` on code cells; `%%sql` (and other cell magics) are skipped because their body is SQL, and inline `!`/`%` line magics are stripped.
- **Path patching + execution** — for Week 3+ demo/solutions, rewrites a temp copy: `DATA_DIR` → `$OLIST_DATA_PATH`, `DB_PATH` → a fresh tempfile `.db`, the jupysql connection string `sqlite:////content/olist.db` → the same temp `.db`, and comments out `from google.colab import drive` + `drive.mount(...)`. Then runs `jupyter nbconvert --execute`.
- **Check-cell gate** — see below.
- **Cell count bounds** — demo 20–34, exercises/solutions 16–30 (each question ≈ 3 cells).

If `jupyter`/`nbconvert`/`jupysql` is not installed, the script prints the pip install command — run it (Step 0a) and retry.

### The check-cell gate (key SQL upgrade)

Exercise notebooks have **blank** `%%sql` answer cells, so their check-cell asserts can never run green — the script therefore **never executes exercise notebooks** (structure + syntax only).

**Solutions** notebooks ARE executed. A solutions notebook passes only if nbconvert produces **zero cell errors** — which means every `assert` in every self-check cell passed. If a check cell raises `AssertionError`, the script classifies it as a **`check_failed`** rework note naming the cell (distinct from a generic `runtime_error`), because it means the `%%sql` answer above it returned a value that does not match the asserted expected result. This catches a wrong query or a wrong expected value pulled from the verified Olist stats.

## Step 3 — Read the result

```python
import json
with open(output_path) as f:
    report = json.load(f)

status = report["status"]              # "pass" or "fail"
rework_notes = report["rework_notes"]  # non-empty string only when fail
failures = report["failures"]          # list of failure dicts (error_type: check_failed | runtime_error | ...)
```

## Step 4 — Update generation state checkpoint

```python
import json

with open(state_path) as f:
    state = json.load(f)

if status == "pass":
    state["notebooks"][notebook_key]["status"] = "validated"
    state["notebooks"][notebook_key]["validation_report"] = output_path
else:
    state["notebooks"][notebook_key]["status"] = "validating"  # caller will rework
    state["notebooks"][notebook_key]["rework_notes"] = rework_notes

with open(state_path, "w") as f:
    json.dump(state, f, indent=2)
```

## Step 5 — Return result to orchestrator

**Do not end your turn here.** Return the result to the orchestrator and let it immediately continue the notebook loop. Print only the one-line status, then control returns to the orchestrator.

If `status == "pass"`: print the one-line pass summary. The orchestrator proceeds to the next notebook.

If `status == "fail"`: print the one-line fail summary and return the `rework_notes` string. The orchestrator will either:
- Re-spawn `/sql-notebook-generate` with `rework_notes` injected (first failure)
- Flag as `needs_human_review` (second failure)

Print summary:
```
✅ Validation PASSED: week-03-wed-solutions.ipynb (24 cells, 0 failures)
```
or:
```
❌ Validation FAILED: week-03-wed-solutions.ipynb
   Failures: 1 | See: .pipeline-cache/week-03-wed-solutions-validation.json
   Rework notes: 1. Cell 11 ('assert int(q3.iloc[0][...'): check_failed — the %%sql answer returned a value that does not match the asserted expected result ...
```

---

## Error Handling

- **Script not found**: the script is at `.claude/skills/sql-content-generator/scripts/validate_sql_notebook_cli.py` — check path
- **jupysql not installed**: `%%sql` cells error with "Cell magic `%%sql` not found" — run Step 0a and retry
- **nbconvert not installed**: script prints the install command; run it and retry
- **Context bundle missing**: script exits with a clear error — abort validation
- **Notebook path wrong**: script exits with a clear error — check generation state for the actual output path
