---
name: sql-week-context
description: >
  Extract and structure the curriculum context for one week of Phase 2b SQL.
  Reads teaching-curriculum.md for the target week, extracts Wed/Thu sections and
  concepts, parses the verified expected values from the ```sql blocks, and writes a
  structured JSON context bundle that all downstream generation and validation skills
  use as their single source of truth. Used internally by /sql-content-generator — can
  also be called standalone to inspect or regenerate the context bundle without
  re-running full generation.
---

# SQL Week Context Extractor

Produces `.pipeline-cache/sql-week-NN-context.json` — the single source of truth for one week's content generation. All downstream skills read from this bundle and must NOT re-read `teaching-curriculum.md` directly.

The critical job of this skill is to capture, **per exercise, the verified expected value(s)** parsed from the curriculum's `sql` blocks and their `**Expected:**` lines, so the generator can seed the locked check-cell `assert`s without inventing numbers.

---

## Inputs

- **Week number** (1–8), passed as an argument
- `curriculum/phase-2b-sql/teaching-curriculum.md` (on disk, may be gitignored)
- `.claude/skills/sql-content-generator/references/olist_schema.md` (verified stats table)
- `.claude/skills/sql-content-generator/assets/sql_setup.py` (the standard setup cell)

## Outputs

- `.pipeline-cache/sql-week-NN-context.json` — full structured context bundle
- `curriculum/phase-2b-sql/weeks-01-08-teaching/<week-slug>/teaching-curriculum.md` — per-week extract committed with the content branch

---

## Week Slug Mapping

| Week | Slug |
|---|---|
| 1 | `week-01-select-where-order-by` |
| 2 | `week-02-groupby-aggregates-having` |
| 3 | `week-03-joins` |
| 4 | `week-04-case-when-and-date-functions` |
| 5 | `week-05-subqueries-and-window-functions` |
| 6 | `week-06-multi-table-joins` |
| 7 | `week-07-ctes-and-advanced-analytics` |
| 8 | `week-08-end-to-end-analysis` |

---

## Workflow

### Step 1 — Validate prerequisites

```bash
CURRICULUM="curriculum/phase-2b-sql/teaching-curriculum.md"

if [ ! -f "$CURRICULUM" ]; then
  echo "ERROR: teaching-curriculum.md not found at $CURRICULUM"
  echo "This file is gitignored — it must exist on disk."
  exit 1
fi
```

Abort immediately if `teaching-curriculum.md` is missing. Do not attempt to generate content without it.

### Step 2 — Extract the week's curriculum section

Read `teaching-curriculum.md`. Locate the section for the requested week using the heading pattern:

```
## Week N — <Topic Name>
```

**Critical**: Extract ONLY the lines between this week's heading and the next week's heading (or end of file for Week 8). Do not bleed content from adjacent weeks. Use line number ranges to enforce this boundary.

Extract separately:
- **Wednesday section**: lines between `### Wednesday Session:` and `### Thursday Session:` within the week block
- **Thursday section**: lines between `### Thursday Session:` and the next `## Week` heading

From each day's section, extract:
- `objectives`: the learning objective(s) (from the `**Objective:**` line)
- `concepts`: list of `{name, description, example_sql, verified_outputs}` objects — one per `**Concept N:**` taught. `example_sql` is the raw SQL from the ```sql block.
- `group_exercise`: full text of the group exercise / Thursday exercises (markdown, preserve verbatim)
- `exercises`: list of individual exercises, each with its SQL and expected value (see Step 3)
- `timing`: session timeline if present

From the week section, also extract:
- `assignment_text`: the weekly assignment (the `**Weekly Assignment:**` block at end of Thursday)
- `special_notes`: any Week 4 DeepSeek intro notes, Week 8 capstone notes

### Step 3 — Parse verified expected values (single source of truth for asserts)

For every ```sql block in the week, look at the line(s) immediately after it. Capture:
- Lines of the form `**Expected: <value>**` (e.g. `**Expected: 96,478**`, `**Expected: R$154.10**`)
- Inline answers in the assignment of the form `*(Answer: <value>)*`

Normalise each captured value (strip thousands separators and currency symbols into a numeric form, but keep the display string too) and attach it to the exercise/concept it belongs to. Each exercise entry should look like:

```json
{
  "id": "q1",
  "question": "How many orders have a NULL delivery date?",
  "sql": "SELECT COUNT(*) AS null_delivery FROM orders WHERE order_delivered_customer_date IS NULL",
  "expected_display": "2,965",
  "expected_value": 2965,
  "assert_column": "null_delivery"
}
```

Do NOT recompute values from the dataset (that could introduce drift from curriculum values). Parse only what is documented in the curriculum. Cross-check against the verified-stats table in `olist_schema.md`; if a value in the curriculum and the schema disagree, keep the **curriculum** value and log a warning.

### Step 4 — Determine tables used and embed the setup cell

The `olist_tables_used` list is determined by scanning which SQLite table names appear in the week's `sql` blocks (`orders`, `customers`, `order_items`, `order_payments`, `order_reviews`, `products`, `sellers`, `product_category_translation`).

Read `.claude/skills/sql-content-generator/assets/sql_setup.py` and store its full content in `colab_setup_code`. This is the verbatim first code cell of every notebook for all weeks.

### Step 5 — Write the context bundle

Create `.pipeline-cache/` directory if it doesn't exist (it is gitignored). Write the bundle:

```json
{
  "schema_version": "1.0",
  "week_number": 1,
  "week_slug": "week-01-select-where-order-by",
  "topic_name": "SELECT, WHERE, ORDER BY, LIMIT",
  "wednesday": {
    "objectives": ["Write SELECT with WHERE, ORDER BY, and LIMIT from memory"],
    "concepts": [
      {
        "name": "WHERE — filtering rows",
        "description": "Filter rows with a boolean predicate",
        "example_sql": "SELECT order_id, customer_id, order_status\nFROM orders\nWHERE order_status = 'delivered'\nLIMIT 10",
        "verified_outputs": {
          "delivered_count": {"expected_display": "96,478", "expected_value": 96478},
          "canceled_count": {"expected_display": "625", "expected_value": 625}
        }
      }
    ],
    "group_exercise": "",
    "exercises": [],
    "timing": ""
  },
  "thursday": {
    "objectives": ["..."],
    "concepts": [],
    "group_exercise": "## Thursday Exercises\n[full text verbatim]",
    "exercises": [
      {
        "id": "q1",
        "question": "How many orders have a NULL delivery date?",
        "sql": "SELECT COUNT(*) AS null_delivery FROM orders WHERE order_delivered_customer_date IS NULL",
        "expected_display": "2,965",
        "expected_value": 2965,
        "assert_column": "null_delivery"
      }
    ],
    "timing": ""
  },
  "assignment_text": "**Weekly Assignment:**\n[full text verbatim from curriculum]",
  "olist_tables_used": ["orders", "customers", "order_items", "order_payments", "order_reviews"],
  "verified_stats": {
    "total_orders": 99441,
    "delivered_orders": 96478,
    "canceled_orders": 625,
    "null_delivery_orders": 2965,
    "sp_customers": 41746,
    "boleto_payments": 19784
  },
  "colab_setup_code": "# contents of sql_setup.py verbatim...",
  "special_flags": {
    "deepseek_assisted": false,
    "capstone_week": false
  },
  "source_curriculum_path": "curriculum/phase-2b-sql/teaching-curriculum.md",
  "generated_at": "2026-07-20T11:00:00Z"
}
```

Set `special_flags.deepseek_assisted = true` for Weeks 4–8 (Weeks 1–3 are no-AI). Set `special_flags.capstone_week = true` for Week 8.

### Step 6 — Write the per-week teaching-curriculum.md

Write the extracted week section (Wednesday + Thursday + Assignment) to:

```
curriculum/phase-2b-sql/weeks-01-08-teaching/<week-slug>/teaching-curriculum.md
```

This file is committed with the content branch by `/sql-week-publish`, making the curriculum available to GitHub Actions (Claude Routines) and to future rework runs. The master `teaching-curriculum.md` remains gitignored.

Format: preserve the original markdown structure from the master curriculum exactly. Just include this week's section, not the full document.

### Step 7 — Confirm output

Print a summary:
```
✅ Week N context bundle written to .pipeline-cache/sql-week-NN-context.json
   Wednesday: N objectives, N concepts
   Thursday:  N objectives, N exercises
   Olist tables: [list]
   Verified expected values captured: N
   DeepSeek-assisted: [true/false]
   Per-week curriculum written to curriculum/.../week-NN-slug/teaching-curriculum.md
```

---

## Error Handling

- **Missing teaching-curriculum.md**: abort with clear message (Step 1)
- **Week N not found in curriculum**: print the headings found and ask to verify the week number
- **Expected value missing for an exercise**: log warning, set `expected_value: null` — do not fabricate numbers (the generator will emit that answer cell without a locked assert)
- **Cache directory creation fails**: `mkdir -p .pipeline-cache/` — run manually if needed

---

## Notes

- All expected values are parsed from curriculum text (cross-checked against `olist_schema.md`), never computed from the dataset. This keeps generated check-cell asserts consistent with what the curriculum says.
- The per-exercise `expected_value` / `assert_column` fields are what let `/sql-notebook-generate` write locked Python check cells that `assert` against `qN.iloc[0][...]` and print `✅ Qn correct`.
- The per-week `teaching-curriculum.md` allows Claude Routines to access curriculum without needing the gitignored master file.
