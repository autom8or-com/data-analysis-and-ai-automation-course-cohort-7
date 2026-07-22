---
name: sql-week-publish
description: >
  Perform all post-generation publishing operations for one Phase 2b SQL week:
  update .gitignore for progressive disclosure, remove .gitkeep placeholders,
  upload solutions to Google Drive AND write the .drive-solutions-url file,
  then git commit (including that file) and push.
  PR creation and Telegram notification are handled automatically by the
  sql-content-publish.yml GitHub Actions workflow triggered on push to
  content/sql-week-*. Reads the generation checkpoint to skip already-completed
  steps (safe to re-run). Used internally by /sql-content-generator. Can be
  called standalone to retry failed publishing steps without re-running generation.
---

# SQL Week Publisher

Handles all publishing ops after notebooks are validated. Idempotent — reads `.pipeline-cache/sql-week-NN-generation-state.json` and skips completed steps. Safe to call multiple times.

---

## Inputs

- **Week number** (1–8)
- **Week slug** (from the slug mapping below)
- **Generation state path**: `.pipeline-cache/sql-week-NN-generation-state.json`

## Prerequisite

All 6 notebooks must have `status: "validated"` or `status: "needs_human_review"` in the generation state. Do not call this skill if any notebook has `status: "pending"` or `status: "generating"`.

The 6 notebooks per week are `{wed,thu}-{demo,exercises,solutions}`:
`week-NN-wed-demo.ipynb`, `week-NN-wed-exercises.ipynb`, `week-NN-wed-solutions.ipynb`,
`week-NN-thu-demo.ipynb`, `week-NN-thu-exercises.ipynb`, `week-NN-thu-solutions.ipynb`.
Demo + exercises are committed to git; **solutions are gitignored** and live only on Google Drive.

---

## Week Slug Mapping

| Week | Slug (folder name) | Topic Name |
|---|---|---|
| 1 | `01-select-where-order-by` | SELECT, WHERE & ORDER BY |
| 2 | `02-groupby-aggregates-having` | GROUP BY, Aggregates & HAVING |
| 3 | `03-joins` | Joins |
| 4 | `04-case-when-and-date-functions` | CASE WHEN & Date Functions |
| 5 | `05-subqueries-and-window-functions` | Subqueries & Window Functions |
| 6 | `06-multi-table-joins` | Multi-Table Joins |
| 7 | `07-ctes-and-advanced-analytics` | CTEs & Advanced Analytics |
| 8 | `08-end-to-end-analysis` | End-to-End Analysis |

- Curriculum path: `curriculum/phase-2b-sql/weeks-01-08-teaching/<slug>/`
- Branch namespace: `content/sql-week-<slug>` (e.g. `content/sql-week-01-select-where-order-by`).
  This is **distinct** from the Phase 2a `content/week-*` branches — the two pipelines must never cross-fire.

---

## Publishing Steps (in order)

**CRITICAL — DO NOT STOP BETWEEN STEPS**: Execute all publishing steps (P1 through P9) in a single continuous run. After each step completes, immediately begin the next one. Do not write a response or end your turn between steps. Only write output at Step P9 (the final summary).

**CRITICAL — ORDERING (the publish-ordering fix)**: The Google Drive upload **and** writing `{WEEK_PATH}/.drive-solutions-url` (Step P5) MUST happen **BEFORE** the git commit (Step P6). The `git push` is what triggers `sql-content-publish.yml`, and that workflow **reads `{WEEK_PATH}/.drive-solutions-url`** to build the facilitator's solutions link. If the file is not committed before the push, the workflow cannot find it and will send facilitators a warning instead of a real link. So the commit in Step P6 MUST include `.drive-solutions-url`. Never reorder P5 after P6. (Phase 2a shipped Week 5 with a wrong generic link because it uploaded to Drive *after* the push — this ordering exists specifically to prevent that.)

Read the generation state file first. Skip any step whose key is already `true` in the `publishing` block.

### Step P1 — Update .gitignore

Remove the whole-folder gitignore entry for this week and replace with solutions-only entries:

```bash
WEEK_NUM=$(printf "%02d" $WEEK)
SLUG="<slug>"   # e.g. 01-select-where-order-by
WEEK_PATH="curriculum/phase-2b-sql/weeks-01-08-teaching/${SLUG}"

# Remove the whole-folder line
sed -i "/${WEEK_PATH//\//\\/}\//d" .gitignore

# Add solutions-only entries (only if not already present)
grep -qF "${WEEK_PATH}/01-wednesday/solutions/" .gitignore || \
  echo "${WEEK_PATH}/01-wednesday/solutions/" >> .gitignore
grep -qF "${WEEK_PATH}/02-thursday/solutions/" .gitignore || \
  echo "${WEEK_PATH}/02-thursday/solutions/" >> .gitignore
```

Checkpoint: set `publishing.gitignore_updated = true`

### Step P2 — Remove .gitkeep files

```bash
SLUG="<slug>"
WEEK_PATH="curriculum/phase-2b-sql/weeks-01-08-teaching/${SLUG}"
rm -f ${WEEK_PATH}/01-wednesday/lecture-materials/.gitkeep
rm -f ${WEEK_PATH}/01-wednesday/exercises/.gitkeep
rm -f ${WEEK_PATH}/02-thursday/lecture-materials/.gitkeep
rm -f ${WEEK_PATH}/02-thursday/exercises/.gitkeep
echo "Removed .gitkeep files"
```

Checkpoint: set `publishing.gitkeep_removed = true`

### Step P3 — Generate lesson plans

For each day (Wed + Thu), write `lesson-plan.md` using the context bundle.

Lesson plan format — self-contained, not "see teaching-curriculum.md":

```markdown
# Week N — [Topic Name]: [Day] Session
## Phase 2b SQL | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab (SQLite via %%sql)

---

## Pre-Session Checklist

- [ ] Olist CSVs accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: [notebook filename]
- [ ] Setup cell runs and loads all 8 tables (Colab: Drive mounted + dataset zip present; local: CSVs auto-detected)
- [ ] Student exercise link ready to share
- [ ] Projector connected, Colab running

---

## Learning Objectives

By the end of this session, students will be able to:
1. [Objective 1 from context bundle]
2. [Objective 2 from context bundle]
3. [Objective 3 from context bundle]

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
| 0:00–0:10 | Setup & recap | Students open Colab, run sql_setup.py |
| 0:10–0:45 | [Concept 1 name] | Demo + mini-challenge |
| 0:45–1:15 | [Concept 2 name] | Demo + mini-challenge |
| 1:15–1:45 | Group Exercise | [Group exercise title from context] |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview next session |

---

## Key Concepts

[For each concept in context bundle]:
### [Concept Name]
[Concept description from context bundle]

Expected outputs (verified against the Olist dataset):
[All verified_outputs from context bundle for this concept]

Common mistake to watch for:
[From §5 of the demo notebook — e.g. integer division, `= NULL`, TEXT dates]

---

## Group Exercise

[Full group exercise text from context bundle.group_exercise — verbatim]

**Expected outputs**: [verified_outputs for the exercise]

---
[Thursday only]:
## Weekly Assignment

[context bundle.assignment_text — verbatim]
```

**Tool to use**: Write the files using the `Write` tool directly — do NOT use Python subprocess, shell heredoc, or any shell redirection. Lesson plan content contains backticks and triple-quoted code blocks that break shell quoting. Build the full markdown string in memory and call Write once per file.

Write to:
- `${WEEK_PATH}/01-wednesday/lesson-plan.md`
- `${WEEK_PATH}/02-thursday/lesson-plan.md`

Checkpoint: set `publishing.lesson_plans_written = true`

### Step P4 — Week 1 resources (Week 1 only)

For Week 1 only, copy the shared setup helper into both days' `lecture-materials/`:
```bash
cp .claude/skills/sql-content-generator/assets/sql_setup.py \
   ${WEEK_PATH}/01-wednesday/lecture-materials/
cp .claude/skills/sql-content-generator/assets/sql_setup.py \
   ${WEEK_PATH}/02-thursday/lecture-materials/
```

Checkpoint: set `publishing.resources_copied = true` (or skip + set true for non-Week-1)

### Step P5 — Upload solutions to Google Drive AND write .drive-solutions-url

**THIS STEP MUST RUN BEFORE THE COMMIT IN STEP P6.** The push in P6 triggers
`sql-content-publish.yml`, which reads `${WEEK_PATH}/.drive-solutions-url` to build the
facilitator's Drive link. That file MUST be created here and committed in P6 — otherwise the
workflow warns instead of linking.

Solutions (`week-NN-{wed,thu}-solutions.ipynb`) are gitignored — Google Drive is the only permanent storage.

**Prerequisites**: The Google Drive MCP connector must be added to this Routine's connectors at `claude.ai/code/routines`.

**Parent folder** — this is a NEW Phase 2b parent (do not reuse the Phase 2a folder):

1. **Find or create the Phase 2b parent folder**:
   - Use `mcp__Google-Drive__search_files` to find a folder named `Phase 2b SQL`.
   - If not found, create it with `mcp__Google-Drive__create_file` (mimeType: `application/vnd.google-apps.folder`).
   - Note its folder ID — this is the value that belongs in the `GDRIVE_PHASE2B_FOLDER_ID`
     GitHub variable (phase-level link only; the workflow does **not** use it as a per-week fallback).

2. **Find or create the week subfolder** inside the `Phase 2b SQL` parent:
   - Target folder name: `Week NN - <Topic Name>` (e.g. `Week 03 - Joins`)
   - Search for an existing folder with that name and parent ID; create if not found.

3. **Find or create** `wednesday-solutions` and `thursday-solutions` sub-folders inside the week folder.

4. **Upload each solution notebook** using `mcp__Google-Drive__create_file`:
   - Read `${WEEK_PATH}/01-wednesday/solutions/week-NN-wed-solutions.ipynb` as base64 → upload to `wednesday-solutions`.
   - Read `${WEEK_PATH}/02-thursday/solutions/week-NN-thu-solutions.ipynb` as base64 → upload to `thursday-solutions`.
   - Upload with `contentMimeType: "application/vnd.jupyter.notebook"` and `disableConversionToGoogleType: true`.

5. **Write the week Drive folder URL to the committed file** so the workflow can link directly to the week subfolder (not the parent):
   ```bash
   echo "https://drive.google.com/drive/folders/<WEEK_FOLDER_ID>" \
     > ${WEEK_PATH}/.drive-solutions-url
   ```
   Replace `<WEEK_FOLDER_ID>` with the actual ID of the `Week NN - <Topic>` subfolder.
   This file is intentionally committed — it is NOT inside solutions/ so it is not gitignored.

If a Drive MCP call fails: still write a best-effort `.drive-solutions-url` if you have the
week folder ID; if you have no URL at all, do NOT write the file (the workflow will emit its
explicit warning rather than a wrong link). Log the failure and continue.

Checkpoint: set `publishing.drive_uploaded = true`, `publishing.drive_url_written = true`, `publishing.drive_folder = "Week NN - <Topic>"`

### Step P6 — Git commit (including .drive-solutions-url) and push

The commit MUST include `${WEEK_PATH}/.drive-solutions-url` written in Step P5.

```bash
git config user.email "pipeline@pora.academy"
git config user.name "PORA Content Pipeline"

SLUG="<slug>"
WEEK_PATH="curriculum/phase-2b-sql/weeks-01-08-teaching/${SLUG}"
TOPIC="<Topic Name from the mapping table>"

# Stage content + the .gitignore change. The .drive-solutions-url lives under
# WEEK_PATH and is added here — verify it is staged before committing.
git add "${WEEK_PATH}/"
git add .gitignore
git status --porcelain "${WEEK_PATH}/.drive-solutions-url"   # must show it staged

git commit -m "Add Phase 2b SQL Week ${WEEK} content: ${TOPIC}

Generated by Claude Routine — 6 notebooks validated, lesson plans complete.
Solutions uploaded to Google Drive; .drive-solutions-url committed for the workflow.
Branch: content/sql-week-${SLUG}"

# Embed GITHUB_TOKEN in remote URL — required in Routine environment (no interactive auth)
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/autom8or-com/data-analysis-and-ai-automation-course-cohort-7.git"
git push -u origin "content/sql-week-${SLUG}"
```

Checkpoint: set `publishing.git_committed = true`, `publishing.git_pushed = true`

### Step P7 — (handled by GitHub Actions)

PR creation is handled automatically by `.github/workflows/sql-content-publish.yml`,
which triggers on the `git push` in Step P6. **Never create the PR manually** — if you create
it before the workflow runs, the workflow detects the existing PR and skips both PR creation
and the Telegram notification. No action required here.

Checkpoint: set `publishing.pr_created = "handled_by_gha"`

### Step P8 — (handled by GitHub Actions)

Telegram notification to the reviewer group is sent by `sql-content-publish.yml`
immediately after PR creation, using the committed `.drive-solutions-url` for the Drive link.
No action required here.

Checkpoint: set `publishing.telegram_sent = "handled_by_gha"`

### Step P9 — Final summary

```
✅ Week N (Phase 2b SQL) publishing complete
   Branch: content/sql-week-<slug>
   Drive: Phase 2b SQL / Week NN - <Topic>  (.drive-solutions-url committed BEFORE push)
   Notebooks: demo+exercises committed, 2 solutions on Drive (6/6 validated)
   PR + Telegram: triggered by git push → sql-content-publish.yml workflow

Next: Wait ~30s for sql-content-publish.yml to create the PR, then check GitHub.
      Review the PR and comment with the approve command (leading slash) when ready.
```

---

## Error Handling

- **git push fails** (branch exists remotely): use `git push --force-with-lease` for the content branch only.
- **Google Drive MCP unavailable**: log warning, skip Drive upload, and do NOT write a fake `.drive-solutions-url` — an absent file makes the workflow show its explicit warning rather than a wrong link. PR creation still triggers from the push.
- **`.drive-solutions-url` missing after push**: re-run this skill; P5 re-uploads (or reuses the folder) and P6 amends/commits the file, then re-push so the workflow re-reads it.
- **PR not created after push**: check GitHub Actions for the `sql-content-publish.yml` run; re-trigger by pushing an empty commit if needed.
- **Any step fails after git push**: re-running this skill skips completed steps and retries from the failed step.
