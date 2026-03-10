# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A curriculum repository for PORA Academy Cohort 7 — a ~14-month data analysis and AI automation programme. There is no application code, build system, or test suite. All work here is curriculum content: markdown documents, lesson plans, and datasets.

## Repository architecture

```
curriculum/          ← one folder per phase; each has teaching-curriculum.md + session folders
datasets/            ← raw data files, organised by phase
.artifact/           ← original/source materials; treat as read-only reference
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
- Dataset for Weeks 1–6 teaching: `datasets/phase-1-excel/teaching/data.csv` (UCI Online Retail, 541,909 rows)
- Group project datasets: `datasets/phase-1-excel/projects/group-N-name/`
- Group 4 uses the same file as teaching; its project folder contains only a README pointing to it
- Additional resources (cheatsheets, PQ reference): `curriculum/phase-1-excel/resources/`

**Phase 2a — Python / Phase 2b — SQL**
- Both use the Olist dataset: `datasets/phase-2-python-sql/` (11 CSVs, upload to shared Google Drive)
- SQL is taught via SQLite in-memory inside Google Colab (`sqlite3` + `pd.read_sql()`), not a standalone DB
- DeepSeek AI introduced at Week 4 in both phases; Weeks 1–3 are no-AI
- Key verified Olist stats are embedded throughout both curricula — do not alter them without re-running against the data

**Phase 2c — Capstone**
- No session folder scaffold (4-week project, not teaching weeks)
- All 4 groups use the same Olist dataset with different analytical focus
- Deliverable: Streamlit app deployed to Streamlit Community Cloud via GitHub

**Phase 3 — AI Automation**
- 24 weeks, 90-minute sessions, structured into 7 internal Modules (not "phases" — avoid that word to prevent confusion with the programme-level phase numbering)
- Teaching case: Ready Delight Foods and Confectioneries (Nigerian peanut SME)
- Data lives in NocoDB (self-hosted), not in CSV files — students build the database in Module 1
- Source reference (do not edit): `.artifact/ai-automation-use-case/ready_delight_automation_curriculum.md`
- `lecture-materials/` subfolder is `workflows/` (n8n JSON exports), not `notebooks/`

## Extending the curriculum

When scaffolding new session folders, follow the Python script pattern used in earlier sessions (create directories, write `.gitkeep` in empty leaf dirs, write pre-filled `lesson-plan.md`). Do not create folders manually one by one.

When writing new curriculum content, read the existing `teaching-curriculum.md` for the relevant phase first to match tone, formatting, and verification standard before adding or modifying sessions.

The `.artifact/` directory holds original source files used to build this curriculum. Treat it as read-only.
