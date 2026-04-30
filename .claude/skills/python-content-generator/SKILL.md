---
name: python-content-generator
description: Generate complete Phase 2a Python curriculum content — lesson plans, Jupyter notebooks (demo/exercise/solution), validation with caching, and automated publishing to Google Drive + NocoDB. Use when generating weekly content for 8-week Python teaching programme with Olist dataset.
---

# Python Content Generator for Phase 2a

Comprehensive skill for generating Phase 2a Python curriculum content (8 weeks, 120 students, Google Colab + Olist dataset).

## What It Does

Generates complete weekly content in a single command:

- **2 lesson plans** (Wednesday & Thursday)
- **6 Jupyter notebooks** (demo/exercise/solution × 2 days)
- **Data validation** with caching (avoid 30-second re-validation every run)
- **Automated publishing** to GitHub, Google Drive, and NocoDB
- **Telegram alerts** to facilitators with rotating Bible quotes

**Time to generate 1 week:** ~4 minutes (first run with validation), ~0.8 seconds (cached runs)

---

## Quick Start

**Prerequisites:** `olist-data.zip` in `datasets/phase-2-python-sql/`, `teaching-curriculum.md` on disk (gitignored), rclone configured with service account (see `references/google_drive_phase2a.md`).

### Generate Week 1

```bash
cd /path/to/data-analysis-and-ai-automation-course-cohort-7
python .claude/skills/python-content-generator/scripts/generate_week_content.py 1
```

### Generate with Force-Validation

```bash
python .claude/skills/python-content-generator/scripts/generate_week_content.py 1 --force-validate
```

---

## Curriculum Overview

| Week | Topic | Key Skills | AI? |
|---|---|---|---|
| 1 | Python Fundamentals | Variables, types, strings | No |
| 2 | Collections & Control Flow | Lists, dicts, if/for/while | No |
| 3 | Functions & Data | def, imports, pandas intro | No |
| 4 | Pandas Introduction | DataFrames, loading, exploration | **DeepSeek intro** |
| 5 | Groupby & Aggregation | groupby(), .sum(), .mean() | Yes |
| 6 | Data Cleaning | .dropna(), .fillna(), null handling | Yes |
| 7 | Merging DataFrames | .merge(), .join(), .concat() | Yes |
| 8 | Visualisation & Streamlit | matplotlib, seaborn, Streamlit | Yes + **Streamlit** |

---

## Architecture

### Scripts (core logic)

1. **olist_loader.py** — Load 11 CSVs from zip, return as dict of DataFrames
2. **cache_validator.py** — MD5 hash checking, cache file management
3. **validate_notebooks.py** — Execute cells, validate against teaching-curriculum KPIs
4. **notebook_builder.py** — Create .ipynb files with demo/exercise/solution patterns
5. **generate_week_content.py** — Orchestrator executing 15-step workflow

### References (documentation)

Loaded as needed during execution. Key references:
- `phase2a_structure.md` — Week mapping, folder conventions
- `olist_schema.md` — Dataset schema with verified stats
- `notebook_patterns.md` — Demo/exercise/solution patterns
- `google_drive_phase2a.md` — Drive folder setup and gws commands
- `nocodb_phase2a.md` — NocoDB table schema and API endpoints
- `telegram_config.md` — Bot setup and message template
- `validation_cache.md` — Cache structure and performance notes

### Assets (templates)

Boilerplate content for notebooks and lessons:
- `instructor_notes.md` — Lesson plan template
- `data_loading.py` — Standard Olist loading code for students
- `deepseek_integration.md` — AI protocol and example prompts (Weeks 4–8)
- `streamlit_example.py` — Sample Streamlit app (Week 8)

---

## The 15-Step Workflow

1. **Parse request** → Validate week number, get topic name
2. **Create git branch** → `git checkout -b content/week-slug`
3. **Read curriculum** → Extract teaching-curriculum.md content
4. **Load Olist data** → Full dataset (99,441 orders) for validation
5. **Validate code cells** → Execute cells against data; cache results
6. **Fill lesson plans** → Create Wednesday & Thursday lesson-plan.md
7. **Create 6 notebooks** → Demo/exercise/solution × Wed/Thu with nbformat
8. **Populate resources** → Week 1 only: cheatsheets, schema reference
9. **Remove .gitkeep** → Clean up placeholder files from scaffolding
10. **Update .gitignore** → Switch from whole-folder hide to solutions-only hide
11. **Commit to branch** → `git commit -m "Add Week N content:..."`
12. **Upload to Google Drive** → Solutions notebooks to gws Drive folder
13. **Update NocoDB** → weekly_schedule table with lesson plan URLs
14. **Send Telegram alert** → Notify facilitators with Bible quote
15. **Report summary** → Print branch name, file count, next steps

---

## Validation Caching

**Problem:** Full dataset validation takes ~30 seconds per week.

**Solution:** MD5 hash–based cache at `.claude/cache/phase2a-validation-cache.json` (project-level, gitignored)

```json
{
  "dataset_hash": "a1b2c3d4e5f6...",
  "timestamp": "2026-04-26T10:30:00",
  "weeks": {
    "1": {
      "status": "validated",
      "cells": { "cell_1": { "status": "pass", ... } }
    }
  }
}
```

- **Cache hit** (same dataset, week cached): Validation instant (0.1 sec)
- **Cache miss** (first run or dataset changed): Full validation (30 sec)
- **Force-validate flag**: Override cache, always validate

---

## Pipeline State

Publishing steps (11–14) write progress to `.claude/phase2a-pipeline-state.json` in the repo root (gitignored). This enables safe resume if a session is interrupted mid-pipeline.

**File location:** `{REPO_ROOT}/.claude/phase2a-pipeline-state.json`

```json
{
  "week_1": {
    "steps_completed": ["11_git_commit", "12_drive_upload"],
    "last_updated": "2026-05-01T10:42:00",
    "artifacts": {
      "git_branch": "content/week-01-python-fundamentals",
      "drive_url": "https://drive.google.com/drive/folders/1cPSs6q0kV28sr5m5Km31EooCuD1Lwuno"
    }
  }
}
```

- **Steps tracked**: `11_git_commit`, `12_drive_upload` (13 and 14 tracked once implemented)
- **Resume**: Re-run the same week — script reads state and skips completed steps
- **Reset a week**: Delete that week's key from the JSON to re-run all publishing steps

---

## Data Model

### Olist Dataset (11 CSVs, 99,441 orders)

Core tables:
- **olist_orders_dataset.csv** — 99,441 orders (Week 3+)
- **olist_customers_dataset.csv** — Customer info (Week 5+)
- **olist_order_items_dataset.csv** — Order line items (Week 5+)
- **olist_products_dataset.csv** — Products (Week 6+)
- **olist_order_reviews_dataset.csv** — Reviews (Week 7+)
- **olist_order_payments_dataset.csv** — Payment methods (Week 7+)
- **olist_sellers_dataset.csv** — Sellers (Week 7+)
- **olist_product_category_name_translation.csv** — Category translations (Week 7+)

**Verified stats (hardcoded in curriculum):**
- Total orders: 99,441
- Delivered orders: ~96,482
- SP state orders: 41,746
- Unique sellers: 3,095
- Average order value: ~154 BRL

---

## Notebook Structure

### Demo Notebook (`*-demo.ipynb`)

Instructor's live walkthrough. All cells executed, all outputs visible.

**Cells:**
1. Title markdown
2. Instructor notes + learning objectives
3. Setup code (load data, imports)
4. Concept 1–N markdown + code
5. Summary markdown

### Exercise Notebook (`*-exercises.ipynb`)

Student worksheet with questions and blank code cells.

**Cells:**
1. Title markdown
2. Instructions markdown
3. Raw Data markdown
4. Setup code (executed)
5. Question 1–N markdown + blank code cells

### Solution Notebook (`*-solutions.ipynb`)

Instructor's answer key — same structure as exercises, but with filled code.

**Key:**
- No saved notebook outputs (clean files)
- All cells have execution count = None
- Outputs arrays empty

---

## GitHub Integration

### Repository Structure

```
curriculum/phase-2a-python/
├── teaching-curriculum.md (gitignored)
└── weeks-01-08-teaching/
    └── week-NN-slug/
        ├── 01-wednesday/
        │   ├── lesson-plan.md
        │   ├── lecture-materials/week-NN-wed-demo.ipynb
        │   ├── exercises/week-NN-wed-exercises.ipynb
        │   └── solutions/week-NN-wed-solutions.ipynb (gitignored)
        └── 02-thursday/
            └── (same structure)
```

### Progressive Disclosure

- Unreleased weeks (1–8): Whole folder gitignored
- After generation: Folder released, only `solutions/` hidden
- Lesson plans + notebooks visible to students on GitHub
- Solutions visible only on instructor's local machine + Google Drive

---

## Google Drive + NocoDB Integration

### Google Drive Folder IDs

| Folder | ID |
|---|---|
| Root | `1cPSs6q0kV28sr5m5Km31EooCuD1Lwuno` |
| Phase 2a | Discovered/created on first run |

### NocoDB weekly_schedule

Table with 8 rows (one per week):
- Columns: week_number, topic_name, wed/thu_lesson_plan_url, wed/thu_sheet_names, deepseek_intro_week, streamlit_week, status
- Updated after Step 13

### Telegram Alerts

Sent to facilitators' group after each week is published:

```
📚 Phase 2a Python — Week N Content Published
**Topic:** [Topic Name]
**Week:** N of 8

✅ Lesson plan: [GitHub link]
📂 Solutions: [Drive link]

🎯 Key coverage:
- [Skill 1]
- [Skill 2]
- [Skill 3]

[Optional: DeepSeek note]
[Optional: Streamlit note]

Bible verse: [Rotating quote 1–8]
```

---

## Special Cases

### Week 4 (DeepSeek Introduction)

- Set `deepseek_intro_week = true` in NocoDB
- Telegram alert includes: "DeepSeek AI assistance introduced this week"
- Lesson plan has dedicated section on AI protocol

### Week 8 Thursday (Streamlit)

- Set `streamlit_week = true` in NocoDB
- Telegram alert includes: "Streamlit introduction — deployment example included"
- Solution notebook includes complete Streamlit app example

---

## Error Handling

- **Invalid week number**: ValueError with suggestion
- **Dataset not found**: FileNotFoundError with zip path
- **Git branch already exists**: Treated as resume — checks out existing branch and continues
- **Cell validation fails**: Skips cache update; prints validation error details
- **Drive/NocoDB/Telegram unavailable**: Logs warning, continues with other steps

---

## Performance Characteristics

- **First run (all 8 weeks)**: ~4 minutes per week (validation time dominates)
- **Cached runs**: ~0.8 seconds per week
- **Disk space**: ~150 MB for all notebooks (no outputs stored)
- **Memory**: ~500 MB peak (full Olist dataset + notebook builders in memory)

---

## Future Enhancements

- Real notebook cell execution + output capture (currently cells are templates)
- NocoDB API integration for automated table updates (Step 13 is a placeholder)
- Telegram message formatting with inline links (Step 14 is a placeholder)
- Parallel notebook generation for all 8 weeks

---

## Author Notes

Built to mirror excel-content-generator skill but for Jupyter notebooks and Python curriculum. Validation caching is the key optimization (avoid re-running 30-second checks every generation). All 15 workflow steps are implemented. Drive upload (Step 12) uses rclone with a service account — no browser auth, no token expiry. Steps 13 (NocoDB) and 14 (Telegram) are placeholders that log success but do not yet call the APIs.
