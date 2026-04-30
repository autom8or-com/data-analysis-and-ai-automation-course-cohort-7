# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A curriculum repository for PORA Academy Cohort 7 — a ~14-month data analysis and AI automation programme. There is no application code, build system, or test suite. All work here is curriculum content: markdown documents, lesson plans, and datasets.

## Repository architecture

```
curriculum/          ← one folder per phase; each has teaching-curriculum.md + session folders
datasets/            ← zip files per phase/group + README.md in each subfolder (raw CSVs excluded from git)
```

**Phases and their curriculum paths:**

| Phase | Path | Session length |
|---|---|---|
| 1 — Excel | `curriculum/phase-1-excel/` | 2 hrs |
| 2a — Python | `curriculum/phase-2a-python/` | 2 hrs |
| 2b — SQL | `curriculum/phase-2b-sql/` | 2 hrs |
| 2c — Capstone | `curriculum/phase-2c-capstone/` | 2 hrs |
| 3 — AI Automation | `curriculum/phase-3-ai-automation/` | 90 min |

## Session folder convention

Every phase (except 2c which has only a top-level curriculum file) uses this pattern:

```
weeks-NN-MM-teaching/
└── week-NN-topic-slug/
    ├── 01-wednesday/
    │   ├── lesson-plan.md
    │   ├── lecture-materials/   ← notebooks/ (Phase 2) or workflows/ (Phase 3)
    │   ├── exercises/
    │   └── solutions/
    └── 02-thursday/
        └── (same structure)
```

- Week folders: `week-01-topic-slug` — always zero-padded, always lowercase-hyphenated
- Day folders: `01-wednesday` before `02-thursday` — numeric prefix enforces sort order
- Empty leaf directories contain a `.gitkeep` file

## Teaching curriculum files

Each `teaching-curriculum.md` is the authoritative, fully detailed session plan. It contains verified expected outputs (formulas, query results, KPIs) run against the actual dataset before writing. The lesson-plan.md files in session folders are sparse instructor-facing templates that reference the teaching curriculum for full detail.

**Critical principle:** every formula, query result, chart value, or KPI stated in a teaching curriculum must be verified against the actual dataset. Never write an expected output from assumption.

## Phase-specific notes

**Phase 1 — Excel**
- Datasets are in zip files: `datasets/phase-1-excel/teaching/teaching-data.zip` (UCI Online Retail, 541,909 rows) and `datasets/phase-1-excel/projects/group-N-name/group-N-data.zip`
- Group 4 uses the same file as teaching; its folder contains only a README
- `Reviews.csv` (287 MB) is excluded from git entirely — must be downloaded from Kaggle; curriculum uses `Reviews_sample_50k.csv` only
- Additional resources (cheatsheets, PQ reference): `curriculum/phase-1-excel/resources/`

**Phase 2a — Python / Phase 2b — SQL**
- Both use the Olist dataset: `datasets/phase-2-python-sql/olist-data.zip` (11 CSVs; unzip and upload to shared Google Drive)
- SQL is taught via SQLite in-memory inside Google Colab (`sqlite3` + `pd.read_sql()`), not a standalone DB
- DeepSeek AI introduced at Week 4 in both phases; Weeks 1–3 are no-AI
- Key verified Olist stats are embedded throughout both curricula — do not alter them without re-running against the data

**Phase 2c — Capstone**
- Has only `teaching-curriculum.md` at top level; no per-session folder scaffold (4-week group project)
- All 4 groups use the same Olist dataset with different analytical focus
- Deliverable: Streamlit app deployed to Streamlit Community Cloud via GitHub

**Phase 3 — AI Automation**
- 24 weeks, 90-minute sessions, structured into 7 internal Modules (not "phases" — avoid that word to prevent confusion with the programme-level phase numbering)
- Teaching case: Ready Delight Foods and Confectioneries (Nigerian peanut SME)
- Data lives in NocoDB (self-hosted), not in CSV files — students build the database in Module 1
- `lecture-materials/` subfolder is `workflows/` (n8n JSON exports), not `notebooks/`

## Content visibility and progressive disclosure

This repo uses progressive disclosure — students only see content for the current week.
All `teaching-curriculum.md` files, project specs, future week folders, and most datasets
are gitignored and exist only on the instructor's local machine.

**What is currently live (visible to students):**
- `curriculum/phase-1-excel/weeks-01-06-teaching/week-01-data-import-and-navigation/` (exercises + demo only; solutions gitignored)
- `curriculum/phase-1-excel/resources/` (cheatsheets)
- `datasets/phase-1-excel/teaching/` (teaching-data.zip)

**To release a new week:** delete the week's line from `.gitignore`, add the two `solutions/` paths
back as explicit entries, then commit content and `.gitignore` together.

**Note:** `teaching-curriculum.md` files are gitignored — read them from disk, not via `git show`.
If a file appears missing, check `.gitignore` before assuming it doesn't exist.

## File dependencies

Before starting any content generation pipeline, verify these files exist on disk:
- `curriculum/phase-2a-python/teaching-curriculum.md` (gitignored — check disk, not git)
- `datasets/phase-2-python-sql/olist-data.zip`

If either is missing, stop and tell the user immediately. Do not infer or fabricate content.

## Interruption recovery

For long-running pipelines (notebooks, Drive upload, NocoDB, Telegram):
- After each publishing step (steps 11–14: git commit, Drive upload, NocoDB, Telegram), write progress to `~/.claude/cache/phase2a-pipeline-state.json`
- On resume: read that file first, skip completed steps, check out the existing branch rather than creating a new one
- Validate that all expected output files exist on disk before marking a step complete

## Extending the curriculum

When scaffolding new session folders, follow the Python script pattern used in earlier sessions (create directories, write `.gitkeep` in empty leaf dirs, write pre-filled `lesson-plan.md`). Do not create folders manually one by one.

When writing new curriculum content, read the existing `teaching-curriculum.md` for the relevant phase first to match tone, formatting, and verification standard before adding or modifying sessions.

