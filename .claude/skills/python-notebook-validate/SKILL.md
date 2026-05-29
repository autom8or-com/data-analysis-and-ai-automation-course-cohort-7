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
- **Context bundle path**: `.claude/cache/week-NN-context.json`
- **Week number** (for routing Week 1–2 syntax-only vs Week 3+ full execution)
- **Generation state path**: `.claude/cache/week-NN-generation-state.json` (for checkpoint writes)
- **Notebook key**: one of `wed-demo`, `wed-exercises`, `wed-solutions`, `thu-demo`, `thu-exercises`, `thu-solutions`

## Output

- Validation report at `.claude/cache/week-NN-{day}-{type}-validation.json`
- Returns `status: "pass"` or `status: "fail"` with `rework_notes`

---

## Step 1 — Derive output path

```python
# Derive from notebook path
# e.g. curriculum/.../week-03-.../01-wednesday/lecture-materials/week-03-wed-demo.ipynb
# → .claude/cache/week-03-wed-demo-validation.json
import re
week_str = f"week-{week:02d}"
nb_name = Path(notebook_path).stem  # e.g. "week-03-wed-demo"
output_path = f".claude/cache/{nb_name}-validation.json"
```

## Step 2 — Run the validation script

```bash
python3 .claude/skills/python-content-generator/scripts/validate_notebook_cli.py \
  --notebook "<notebook_path>" \
  --week <N> \
  --context ".claude/cache/week-NN-context.json" \
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

If `status == "pass"`: report success. Done.

If `status == "fail"`: return the `rework_notes` string to the orchestrator. The orchestrator will either:
- Re-spawn `/python-notebook-generate` with `rework_notes` injected (first failure)
- Flag as `needs_human_review` (second failure)

Print summary:
```
✅ Validation PASSED: week-03-wed-demo.ipynb (22 cells, 0 failures)
```
or:
```
❌ Validation FAILED: week-03-wed-demo.ipynb
   Failures: 2 | See: .claude/cache/week-03-wed-demo-validation.json
   Rework notes: 1. Cell 7 ('print(orders_df.shape)'): runtime_error — ...
```

---

## Error Handling

- **Script not found**: the script is at `.claude/skills/python-content-generator/scripts/validate_notebook_cli.py` — check path
- **nbconvert not installed**: script will print the install command; run it and retry
- **Context bundle missing**: script exits with clear error — abort validation
- **Notebook path wrong**: script exits with clear error — check generation state for actual output path
