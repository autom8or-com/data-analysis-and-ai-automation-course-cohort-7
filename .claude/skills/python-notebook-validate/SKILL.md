---
name: python-notebook-validate
description: >
  Validate a generated Phase 2a Python notebook before it is committed.
  Executes all code cells, compares outputs to verified_stats from the context bundle,
  checks all 8 mandatory sections are present, and writes a structured validation
  report. If validation fails, produces detailed rework_notes for the generation
  skill to act on. Used internally by /python-content-generator.
---

# Python Notebook Validator

Quality gate between notebook generation and git commit. Catches runtime errors, wrong expected outputs, and structural violations before they reach students.

---

## Inputs

- **Notebook path**: absolute path to the `.ipynb` file to validate
- **Context bundle path**: `.claude/cache/week-NN-context.json`
- **Week number** (for routing Week 1–2 vs Week 3+ validation mode)

## Output

Validation report written to `.claude/cache/week-NN-{day}-{type}-validation.json`.

Returns `status: "pass"` or `status: "fail"`.

---

## Validation Report Schema

```json
{
  "notebook_path": "curriculum/.../week-03-wed-demo.ipynb",
  "status": "pass",
  "validated_at": "2026-05-29T11:10:00Z",
  "cells_checked": 18,
  "code_cells_executed": 12,
  "failures": [
    {
      "cell_index": 7,
      "cell_source_snippet": "print(orders_df.shape)",
      "error_type": "runtime_error",
      "expected": "(99441, 8)",
      "actual": "NameError: name 'orders_df' is not defined",
      "fix_hint": "Add data loading cell before this cell"
    }
  ],
  "structure_check": {
    "has_title_and_objectives": true,
    "has_business_hook": true,
    "has_concept_intro_with_code": true,
    "has_going_deeper": true,
    "has_common_mistakes": false,
    "has_mini_challenge": true,
    "has_group_exercise": true,
    "has_summary_and_preview": true,
    "sections_missing": ["has_common_mistakes"]
  },
  "cell_count": 22,
  "cell_count_ok": true,
  "rework_notes": "1. Cell 7 (print(orders_df.shape)) raises NameError — data loading cell must come before Week 3+ data references. 2. Section §5 Common Mistakes is missing entirely — add a markdown + code cell pair showing a TypeError with correction."
}
```

---

## Workflow

### Step 1 — Load the notebook and context bundle

```python
import json, nbformat

with open(notebook_path) as f:
    nb = nbformat.read(f, as_version=4)

with open(context_bundle_path) as f:
    ctx = json.load(f)

verified_stats = ctx.get('verified_stats', {})
week_number = ctx['week_number']
notebook_type = 'demo'  # derive from filename: demo/exercises/solutions
day = 'wed'             # derive from filename: wed/thu
```

### Step 2 — Determine validation mode

**Weeks 1–2**: syntax-only validation (no pandas, no Drive mounting possible)
- Use `compile(source, '<string>', 'exec')` on each code cell
- Skip execution, skip output comparison
- Still check structure

**Weeks 3–8**: full execution validation
- Before execution, substitute Colab Drive paths with local paths from the zip file
- Run via nbconvert with timeout

### Step 3 — Structural check

Scan the notebook's markdown cells for the presence of all 8 required sections. Use these marker phrases to detect sections (case-insensitive):

| Section | Marker phrases to look for |
|---|---|
| §1 Title + Objectives | "learning objectives", "by the end of this session", "week N —" |
| §2 Business Hook | "in the olist dataset", "olist", cell is the SECOND markdown cell with no code before it |
| §3 Concept + Code | More than 3 markdown+code pairs in the middle of the notebook |
| §4 Going Deeper | "going deeper", "advanced", "edge case", "extension" |
| §5 Common Mistakes | "common mistake", "wrong", "raises", "typeerror", "nameerror" |
| §6 Mini-Challenge | "mini-challenge", "challenge", "⏱" |
| §7 Group Exercise | "group exercise", "group activity", the group_exercise text from context bundle |
| §8 Summary + Preview | "session summary", "coming up", "summary table" |

For exercises and solutions, apply the 5-part structure check instead (title, setup, questions, group exercise, assignment).

### Step 4 — Syntax check (all weeks)

For each code cell, run:

```python
import ast, py_compile, tempfile, os

for i, cell in enumerate(nb.cells):
    if cell.cell_type != 'code':
        continue
    source = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
    try:
        compile(source, f'<cell_{i}>', 'exec')
    except SyntaxError as e:
        failures.append({
            'cell_index': i,
            'cell_source_snippet': source[:100],
            'error_type': 'syntax_error',
            'expected': 'valid Python syntax',
            'actual': str(e),
            'fix_hint': f'Fix syntax on line {e.lineno}: {e.msg}'
        })
```

### Step 5 — Execution check (Weeks 3+)

For Weeks 3–8 demo and solution notebooks only. Skip exercise notebooks (they have blank cells).

First, patch the data loading paths:

```python
for cell in nb.cells:
    if cell.cell_type == 'code':
        source = ''.join(cell.source) if isinstance(cell.source, list) else cell.source
        # Replace Drive mount path with local zip extraction path
        source = source.replace(
            "'/content/drive/MyDrive/",
            f"'<local-olist-extracted-path>/"
        )
        cell.source = source
```

Then execute with nbconvert:

```bash
pip install nbconvert jupyter_client ipykernel -q
jupyter nbconvert --to notebook --execute \
  --ExecutePreprocessor.timeout=60 \
  --ExecutePreprocessor.kernel_name=python3 \
  --output /tmp/week-NN-<day>-<type>-executed.ipynb \
  <notebook_path>
```

If execution fails, parse the error output to identify which cell failed and what the traceback was.

### Step 6 — Output comparison (Weeks 3+ demo/solution)

After execution, compare cell outputs to `verified_stats` where applicable. Look for cells that print known KPIs:

- If a cell's output contains a number, check if it should match a `verified_stats` value
- Match on the first printed number in the cell output
- Allow ±1% tolerance for floating point values
- Exact match required for integer counts (99441, 41746, etc.)

### Step 7 — Cell count check

| Notebook type | Min cells | Max cells |
|---|---|---|
| Demo | 20 | 30 |
| Exercises | 14 | 22 |
| Solutions | 14 | 22 |

Outside range → warning (not failure) but include in rework_notes.

### Step 8 — Compile rework_notes

If `status = fail`, write a clear, actionable `rework_notes` string that the generation skill can act on. Format:

```
1. Cell N (<snippet>): <what's wrong> — <how to fix>
2. Missing section §5 Common Mistakes: add markdown explaining [TypeError/NameError] + code cell with WRONG comment then CORRECT fix
3. Cell count 18 is below minimum 20: add 2 more cells to §3 (a second concept or a Going Deeper extension)
```

The rework_notes must be specific enough that a re-generation pass can fix all issues without human interpretation.

### Step 9 — Write the validation report

```python
import json
from datetime import datetime, timezone

report = {
    "notebook_path": str(notebook_path),
    "status": "pass" if not failures and all(structure_check.values()) else "fail",
    "validated_at": datetime.now(timezone.utc).isoformat(),
    "cells_checked": total_cells,
    "code_cells_executed": executed_count,
    "failures": failures,
    "structure_check": structure_check,
    "cell_count": len(nb.cells),
    "cell_count_ok": min_cells <= len(nb.cells) <= max_cells,
    "rework_notes": rework_notes_string
}

os.makedirs('.claude/cache', exist_ok=True)
report_path = f'.claude/cache/week-{week:02d}-{day}-{nb_type}-validation.json'
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)
```

Print summary:
```
✅ Validation PASSED: curriculum/.../week-03-wed-demo.ipynb (18 cells, 0 failures)
```
or
```
❌ Validation FAILED: curriculum/.../week-03-wed-demo.ipynb
   Failures: 2 (1 runtime_error, 1 missing_section)
   See: .claude/cache/week-03-wed-demo-validation.json
   Rework notes: [summary]
```

---

## Error Handling

- **nbconvert not installed**: run `pip install nbconvert jupyter_client ipykernel -q` then retry
- **Execution timeout** (cell exceeds 60s): mark as `runtime_error` with `"actual": "TimeoutError: cell timed out after 60s"`
- **Kernel start failure**: fall back to syntax-only check and log warning
- **Context bundle missing**: abort with clear message
