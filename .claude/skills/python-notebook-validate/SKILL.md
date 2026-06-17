---
name: python-notebook-validate
description: >
  Validate a generated Phase 2a Python notebook before it is committed.
  Calls the pre-committed validate_notebook_cli.py script to execute cells,
  check structure, and compare outputs. Reads the JSON result and surfaces
  rework_notes if validation fails. Used internally by /python-content-generator.
---

# Python Notebook Validator

Quality gate between notebook generation and git commit. Calls a pre-committed script — no reasoning about nbconvert mechanics on every run.

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

## Step 0 — Ensure Olist data is available (Weeks 3+ only)

For Weeks 1–2, skip this step entirely.

For Weeks 3–8: the validation script executes notebook code that reads Olist CSVs. The data must be on disk before running the script.

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

Do NOT use Google Drive MCP to download the zip — the file is 45 MB and exceeds the 10 MB Drive MCP download limit. The local zip at `datasets/phase-2-python-sql.zip` is the canonical source.

**If the local zip is missing** (e.g. in a fresh container without the repo): proceed as follows:
1. Run structure check and syntax check only (skip nbconvert execution).
2. If both pass, write the validation report with `"status": "pass"` and add `"skipped_execution": true, "skipped_execution_reason": "datasets/phase-2-python-sql.zip not found"` to the report JSON.
3. Update the generation state checkpoint to `"validated"` as normal.
4. Log a warning but **do not abort the pipeline**.

---

## Step 1 — Derive output path

```python
# Derive from notebook path
# e.g. curriculum/.../week-03-.../01-wednesday/lecture-materials/week-03-wed-demo.ipynb
# → .pipeline-cache/week-03-wed-demo-validation.json
import re
week_str = f"week-{week:02d}"
nb_name = Path(notebook_path).stem  # e.g. "week-03-wed-demo"
output_path = f".pipeline-cache/{nb_name}-validation.json"  # nb_name e.g. "week-03-wed-demo"
```

## Step 2 — Run the validation script

```bash
python3 .claude/skills/python-content-generator/scripts/validate_notebook_cli.py \
  --notebook "<notebook_path>" \
  --week <N> \
  --context ".pipeline-cache/week-NN-context.json" \
  --output "<output_path>"
```

The script exits 0 for pass, 1 for fail. It handles:
- Structural section check (8-section for demo; 5-part for exercises/solutions)
- Python syntax check on all code cells (`compile()`)
- Full nbconvert execution for Weeks 3+ demo/solution notebooks
- Cell count bounds check

If `jupyter`/`nbconvert` is not installed, the script will output the install command — run it and retry.

## Step 3 — Read the result

```python
import json
with open(output_path) as f:
    report = json.load(f)

status = report["status"]          # "pass" or "fail"
rework_notes = report["rework_notes"]  # non-empty string only when fail
failures = report["failures"]      # list of failure dicts
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

**Do not end your turn here.** Return the result to the orchestrator and let it immediately continue the notebook loop. Do not write a standalone summary response — print only the one-line status below, then control returns to the orchestrator.

If `status == "pass"`: print the one-line pass summary below. The orchestrator will immediately proceed to the next notebook.

If `status == "fail"`: print the one-line fail summary below and return the `rework_notes` string. The orchestrator will either:
- Re-spawn `/python-notebook-generate` with `rework_notes` injected (first failure)
- Flag as `needs_human_review` (second failure)

Print summary:
```
✅ Validation PASSED: week-03-wed-demo.ipynb (22 cells, 0 failures)
```
or:
```
❌ Validation FAILED: week-03-wed-demo.ipynb
   Failures: 2 | See: .pipeline-cache/week-03-wed-demo-validation.json
   Rework notes: 1. Cell 7 ('print(orders_df.shape)'): runtime_error — ...
```

---

## Error Handling

- **Script not found**: the script is at `.claude/skills/python-content-generator/scripts/validate_notebook_cli.py` — check path
- **nbconvert not installed**: script will print the install command; run it and retry
- **Context bundle missing**: script exits with clear error — abort validation
- **Notebook path wrong**: script exits with clear error — check generation state for actual output path
