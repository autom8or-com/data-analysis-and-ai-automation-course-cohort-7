---
name: python-week-context
description: >
  Extract and structure the curriculum context for one week of Phase 2a Python.
  Reads teaching-curriculum.md for the target week, extracts Wed/Thu sections,
  computes Olist data stats, and writes a structured JSON context bundle that
  all downstream generation and validation skills use as their single source of truth.
  Used internally by /python-content-generator — can also be called standalone to
  inspect or regenerate the context bundle without re-running full generation.
---

# Python Week Context Extractor

Produces `.pipeline-cache/week-NN-context.json` — the single source of truth for one week's content generation. All downstream skills read from this bundle and must NOT re-read `teaching-curriculum.md` directly.

---

## Inputs

- **Week number** (1–8), passed as an argument
- `curriculum/phase-2a-python/teaching-curriculum.md` (on disk, may be gitignored)
- `datasets/phase-2-python-sql/olist-data.zip` (for verified stats, Weeks 3+)

## Outputs

- `.pipeline-cache/week-NN-context.json` — full structured context bundle
- `curriculum/phase-2a-python/weeks-01-08-teaching/<week-slug>/teaching-curriculum.md` — per-week extract committed with the content branch

---

## Week Slug Mapping

| Week | Slug |
|---|---|
| 1 | `week-01-python-fundamentals` |
| 2 | `week-02-collections-and-control-flow` |
| 3 | `week-03-functions-and-data` |
| 4 | `week-04-pandas-introduction` |
| 5 | `week-05-groupby-and-aggregation` |
| 6 | `week-06-data-cleaning` |
| 7 | `week-07-merging-dataframes` |
| 8 | `week-08-visualisation-and-streamlit` |

---

## Workflow

### Step 1 — Validate prerequisites

```bash
CURRICULUM="curriculum/phase-2a-python/teaching-curriculum.md"
OLIST_ZIP="datasets/phase-2-python-sql/olist-data.zip"

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

or

```
# Week N:
```

**Critical**: Extract ONLY the lines between this week's heading and the next week's heading (or end of file for Week 8). Do not bleed content from adjacent weeks. Use line number ranges to enforce this boundary.

Extract separately:
- **Wednesday section**: lines between `### Wednesday` and `### Thursday` within the week block
- **Thursday section**: lines between `### Thursday` and the next `## Week` heading

From each day's section, extract:
- `objectives`: list of learning objectives (bullet points under "Learning Objectives" or "By the end of this session")
- `concepts`: list of `{name, description, example_code, verified_outputs}` objects — one per concept taught
- `group_exercise`: full text of the group exercise (markdown, preserve verbatim)
- `exercises`: list of individual exercises
- `timing`: session timeline if present

From the week section, also extract:
- `assignment_text`: the weekly assignment (usually at end of Thursday section)
- `special_notes`: any Week 4 DeepSeek intro notes, Week 8 Streamlit notes

### Step 3 — Compute Olist data stats (Weeks 3+)

For Weeks 1–2, skip this step (no pandas used in sessions).

For Weeks 3–8, extract verified stats from the curriculum text — look for lines containing expected output values like:
- `99,441 orders`
- `41,746` or `41746`
- `R$ 154` or similar

Do NOT recompute from data (that could introduce drift from curriculum values). Instead, parse the verified outputs that are already documented in the curriculum.

The `olist_tables_used` list is determined by scanning which CSV filenames appear in the curriculum code blocks for this week:
- `olist_orders_dataset.csv` → "orders" (Week 3+)
- `olist_customers_dataset.csv` → "customers" (Week 5+)
- `olist_order_items_dataset.csv` → "order_items" (Week 5+)
- `olist_products_dataset.csv` → "products" (Week 6+)
- `olist_order_reviews_dataset.csv` → "reviews" (Week 7+)
- `olist_order_payments_dataset.csv` → "payments" (Week 7+)
- `olist_sellers_dataset.csv` → "sellers" (Week 7+)

### Step 4 — Build the standard Colab data loading snippet

For Weeks 1–2, `colab_data_loading_code` is an empty string.

For Weeks 3+, read `.claude/skills/python-content-generator/assets/data_loading.py` and use its content verbatim.

### Step 5 — Write the context bundle

Create `.pipeline-cache/` directory if it doesn't exist (it is gitignored). Write the bundle:

```json
{
  "schema_version": "1.0",
  "week_number": 3,
  "week_slug": "week-03-functions-and-data",
  "topic_name": "Functions & Data",
  "wednesday": {
    "objectives": [
      "Define and call functions with parameters and return values",
      "Use Python's built-in functions on Olist data",
      "Import and use the random and math modules"
    ],
    "concepts": [
      {
        "name": "Defining Functions",
        "description": "Use def keyword to create reusable code blocks",
        "example_code": "def calculate_total(price, freight):\n    return price + freight",
        "verified_outputs": {
          "example_result": "72.19"
        }
      }
    ],
    "group_exercise": "## Group Exercise\n\nUsing the Olist data below...\n[full text verbatim from curriculum]",
    "exercises": ["Exercise 1: ...", "Exercise 2: ..."],
    "timing": "0:00 Setup | 0:10 Functions intro | 0:45 Group exercise | 1:45 Debrief"
  },
  "thursday": {
    "objectives": ["..."],
    "concepts": [...],
    "group_exercise": "...",
    "exercises": [...],
    "timing": "..."
  },
  "assignment_text": "## Weekly Assignment\n\n[full text verbatim from curriculum]",
  "olist_tables_used": ["orders", "customers", "order_items"],
  "verified_stats": {
    "total_orders": 99441,
    "delivered_orders": 96482,
    "sp_orders": 41746,
    "unique_sellers": 3095,
    "avg_order_value_brl": 154.0
  },
  "colab_data_loading_code": "# Mount Google Drive...\n[full data_loading.py content]",
  "special_flags": {
    "deepseek_intro": false,
    "streamlit_week": false
  },
  "source_curriculum_path": "curriculum/phase-2a-python/teaching-curriculum.md",
  "generated_at": "2026-05-29T11:00:00Z"
}
```

Set `special_flags.deepseek_intro = true` for Week 4. Set `special_flags.streamlit_week = true` for Week 8.

### Step 6 — Write the per-week teaching-curriculum.md

Write the extracted week section (Wednesday + Thursday + Assignment) to:

```
curriculum/phase-2a-python/weeks-01-08-teaching/<week-slug>/teaching-curriculum.md
```

This file is committed with the content branch by `/python-week-publish`, making the curriculum available to GitHub Actions (Claude Routines) and to future rework runs. The master `teaching-curriculum.md` remains gitignored.

Format: preserve the original markdown structure from the master curriculum exactly. Just include this week's section, not the full document.

### Step 7 — Confirm output

Print a summary:
```
✅ Week N context bundle written to .pipeline-cache/week-NN-context.json
   Wednesday: N objectives, N concepts
   Thursday:  N objectives, N concepts
   Olist tables: [list]
   Verified stats: N values captured
   Per-week curriculum written to curriculum/.../week-NN-slug/teaching-curriculum.md
```

---

## Error Handling

- **Missing teaching-curriculum.md**: abort with clear message (Step 1)
- **Week N not found in curriculum**: print the headings found and ask to verify the week number
- **Verified stats missing**: log warning, set empty dict — do not fabricate numbers
- **Cache directory creation fails**: `mkdir -p .pipeline-cache/` — run manually if needed

---

## Notes

- All verified_stats values are parsed from curriculum text, not computed from the dataset. This ensures consistency between what the curriculum says and what generated notebooks show.
- The per-week `teaching-curriculum.md` allows Claude Routines to access curriculum without needing the gitignored master file.
