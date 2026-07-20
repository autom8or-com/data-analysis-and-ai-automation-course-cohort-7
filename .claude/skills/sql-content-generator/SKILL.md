---
name: sql-content-generator
description: >
  Generate complete Phase 2b SQL curriculum content — lesson plans, Jupyter notebooks
  (demo/exercise/solution) taught with the %%sql cell magic (jupysql), validation with
  caching, and automated publishing to GitHub, Google Drive + NocoDB. Use when generating
  weekly content for the 8-week SQL teaching programme with the Olist dataset.

  Orchestrates /sql-week-context → /sql-notebook-generate (×6) →
  /sql-notebook-validate (×6) → /sql-week-publish. Uses Claude Opus 4.8
  sub-agents for content generation and Sonnet 4.6 for validation and ops.

  Triggered automatically by the "Phase 2b SQL — Weekly Content" Claude Routine
  (Tuesday 11:00 WAT) or invoked manually with a week number argument.
---

# SQL Content Generator — Orchestrator

Generates one complete week of Phase 2b SQL content by chaining four specialised skills. SQL is taught with the `%%sql` cell magic (jupysql) against a file-based SQLite database — students write raw SQL, not `pd.read_sql("...")` strings. Runs quality validation before every commit. Checkpoints after each notebook so interrupted runs can resume.

---

## Curriculum Schedule

| Week | Topic | AI? |
|---|---|---|
| 1 | SELECT, WHERE, ORDER BY, LIMIT | No |
| 2 | GROUP BY, Aggregates, HAVING | No |
| 3 | JOINs | No |
| 4 | CASE WHEN, String & Date Functions | **DeepSeek intro** |
| 5 | Subqueries & Window Functions | Yes |
| 6 | Multi-table Joins & Complex Aggregations | Yes |
| 7 | CTEs & Advanced Analytics | Yes |
| 8 | End-to-End Business Analysis (Capstone) | Yes |

Weeks 1–3 are no-AI; DeepSeek is introduced at Week 4 and assists Weeks 4–8.

---

## Quick Start

**Generate Week 2** (next unreleased week):
```
/sql-content-generator 2
```

**Auto-detect next unreleased week** (used by the Claude Routine):
```
/sql-content-generator
```

**Resume interrupted run**:
```
/sql-content-generator 3
```
(Resumes from checkpoint automatically — skips already-validated notebooks)

---

## Context Compression Recovery

**If your context was compressed and you are resuming mid-pipeline**, do this immediately before anything else:

```python
import json
# Find the active checkpoint
import glob
checkpoints = glob.glob(".pipeline-cache/sql-week-*-generation-state.json")
if checkpoints:
    with open(sorted(checkpoints)[-1]) as f:
        state = json.load(f)
    week = state["week_number"]
    slug = state["week_slug"]
    pending = [k for k,v in state["notebooks"].items() if v["status"] != "validated"]
    print(f"Resuming Week {week} ({slug}). Still to generate: {pending}")
    # Check out the branch
    import subprocess
    subprocess.run(["git", "checkout", state["branch_name"]], check=True)
    # Skip to Step 5 — generate remaining notebooks
```

Do NOT restart from Step 0 after a resume. The checkpoint is the authoritative source of pipeline state. Jump directly to generating the first notebook that is not `status: "validated"`.

---

## Workflow

### Step 0 — Determine week number

If no argument is given:
1. Read `.gitignore`
2. Find the lowest week number that is still whole-folder gitignored (i.e., has a line like `curriculum/phase-2b-sql/weeks-01-08-teaching/<slug>/`)
3. That is the week to generate

If the argument is given, use it directly. Validate it is 1–8.

### Step 1 — Check for existing checkpoint

Read `.pipeline-cache/sql-week-NN-generation-state.json` if it exists.

If the checkpoint exists and `pipeline_status = "in_progress"`:
- Print: "Resuming Week N from checkpoint. Completed: [list of validated notebooks]."
- Skip to the first notebook that is not `status: "validated"`

If no checkpoint, create a fresh one:

```json
{
  "schema_version": "2.0",
  "week_number": N,
  "week_slug": "<slug>",
  "topic_name": "",
  "branch_name": "content/sql-<slug>",
  "context_bundle_path": ".pipeline-cache/sql-week-NN-context.json",
  "started_at": "<ISO timestamp>",
  "last_updated": "<ISO timestamp>",
  "pipeline_status": "in_progress",
  "notebooks": {
    "wed-demo":      {"status": "pending", "attempts": 0, "output_path": null, "rework_notes": null},
    "wed-exercises": {"status": "pending", "attempts": 0, "output_path": null, "rework_notes": null},
    "wed-solutions": {"status": "pending", "attempts": 0, "output_path": null, "rework_notes": null},
    "thu-demo":      {"status": "pending", "attempts": 0, "output_path": null, "rework_notes": null},
    "thu-exercises": {"status": "pending", "attempts": 0, "output_path": null, "rework_notes": null},
    "thu-solutions": {"status": "pending", "attempts": 0, "output_path": null, "rework_notes": null}
  },
  "publishing": {
    "gitignore_updated": false,
    "gitkeep_removed": false,
    "lesson_plans_written": false,
    "resources_copied": false,
    "git_committed": false,
    "git_pushed": false,
    "pr_created": false,
    "pr_url": null,
    "pr_number": null,
    "drive_uploaded": false,
    "drive_folder": null,
    "telegram_sent": false
  }
}
```

### Step 2 — Create git branch

```bash
git checkout main && git pull origin main
git checkout -b content/sql-<slug> 2>/dev/null || git checkout content/sql-<slug>
```

Branch names are `content/sql-week-NN-slug` (NOT `content/week-*`) so the SQL pipeline's workflows and the Python pipeline's never collide. If the branch already exists (resume): check it out and continue.

### Step 3 — Extract week context

Call `/sql-week-context N`. This skill:
- Reads `curriculum/phase-2b-sql/teaching-curriculum.md`
- Extracts the week's Wed/Thu sections, concepts, group exercise, assignment, and the **verified expected values** parsed from the `sql` blocks and their `Expected:` lines
- Writes `.pipeline-cache/sql-week-NN-context.json`
- Writes the per-week `teaching-curriculum.md` to the week folder

Update `topic_name` in the checkpoint from the context bundle.

**After Step 3 completes, continue immediately to Step 4. Do not stop, summarise, or wait for input.**

### Step 4 — Install dependencies

```bash
pip install nbformat nbconvert jupyter_client ipykernel jupysql -q
```

`jupysql` is required so validation can execute the `%%sql` cells; the rest drive notebook execution. Run once; skip if already installed. The validation environment also needs the Olist data: extract `datasets/phase-2-python-sql.zip` to `/tmp/olist_data` and set `OLIST_DATA_PATH=/tmp/olist_data` (the validate skill builds the file-based SQLite DB from it).

### Step 5 — Generate and validate 6 notebooks

**CRITICAL — DO NOT STOP BETWEEN NOTEBOOKS**: This is a loop over 6 notebooks. After each notebook's generate–validate cycle completes, immediately begin the next one. Do not write a response, summarise progress, or end your turn between notebooks. Do not stop until all 6 notebooks have `status: "validated"` or `status: "needs_human_review"`. Only write output when the entire loop is done and you are ready to call Step 6.

Process notebooks in this order: `wed-demo`, `wed-exercises`, `wed-solutions`, `thu-demo`, `thu-exercises`, `thu-solutions`. Notebook filenames are `week-NN-{wed,thu}-{demo,exercises,solutions}.ipynb`.

Every notebook's **first code cell** is the `sql_setup.py` content (file-based SQLite `/content/olist.db` + `%load_ext sql` + `autopandas = True` + `%sql sqlite:////content/olist.db`). Teaching/answer cells are `%%sql` cells with raw SQL. Each exercise question is a markdown cell (question + expected hint) followed by an answer cell `%%sql qN <<` (blank in exercises, filled in solutions) and a locked plain-Python check cell whose `assert`s come from the verified values in the context bundle and print `✅ Qn correct`.

For each notebook that is NOT already `status: "validated"`:

#### 5a. Generate

Update checkpoint: `status = "generating"`, increment `attempts`.

Spawn a Claude Opus 4.8 sub-agent to execute `/sql-notebook-generate` with:
- Week number
- Day (`wed` or `thu`)
- Notebook type (`demo`, `exercises`, or `solutions`)
- Context bundle path: `.pipeline-cache/sql-week-NN-context.json`
- Rework notes (if this is a retry): the `rework_notes` from the previous validation failure

The sub-agent generates the notebook and writes it to the correct path.

#### 5b. Validate

Update checkpoint: `status = "validating"`.

Call `/sql-notebook-validate` with:
- The notebook path just written
- Context bundle path
- Week number

Read the validation report.

#### 5c. Handle result

**If `status = "pass"`**:
- Update checkpoint: `status = "validated"`, `output_path = <path>`
- Print: `✅ [notebook-key] validated (N cells, attempt K)`
- Save checkpoint to disk immediately

**If `status = "fail"` and `attempts < 2`**:
- Update checkpoint: `status = "reworking"`, `rework_notes = <from validation report>`
- Print: `⚠ [notebook-key] failed validation (attempt K). Reworking: [rework_notes summary]`
- Go back to Step 5a with the rework notes

**If `status = "fail"` and `attempts >= 2`**:
- Update checkpoint: `status = "needs_human_review"`, keep `rework_notes`
- Write `NEEDS_HUMAN_REVIEW.md` to the week folder with the failure details
- Print: `⚠ [notebook-key] flagged for human review after 2 attempts. Continuing with other notebooks.`
- Continue to next notebook (do NOT abort the pipeline)

### Step 6 — Publish

**Continue immediately from Step 5 without ending your turn.** When all 6 notebooks are `validated` or `needs_human_review`, call `/sql-week-publish N`.

This skill handles all remaining ops: gitignore, lesson plans, git commit, PR creation, Drive upload, Telegram.

### Step 7 — Update pipeline status

```json
{
  "pipeline_status": "complete",
  "last_updated": "<ISO timestamp>"
}
```

Print final summary:
```
═══════════════════════════════════════════════════
✅ Week N Pipeline Complete
═══════════════════════════════════════════════════
Topic: [Topic Name]
PR: <url>

Notebooks:
  ✅ wed-demo (validated, 1 attempt)
  ✅ wed-exercises (validated, 1 attempt)
  ✅ wed-solutions (validated, 2 attempts — rework applied)
  ✅ thu-demo (validated, 1 attempt)
  ✅ thu-exercises (validated, 1 attempt)
  ⚠  thu-solutions (needs human review — see NEEDS_HUMAN_REVIEW.md)

Next steps:
  1. Review the PR: <url>
  2. Comment /approve to publish, /rework [feedback] to improve, /reject [reason] to close
```

---

## Rework Flow (triggered by Claude Routine on PR comment)

When called from the Content Rework Routine with a PR number and rework instructions:

1. Identify the PR branch: `gh pr view <PR_NUMBER> --json headRefName --jq '.headRefName'`
2. Check out the branch: `git checkout <branch>`
3. Read the rework instructions from the PR comment
4. Determine which notebooks to rework:
   - If instructions mention specific notebooks (demo, exercises), target those
   - If instructions are general ("add more business context"), apply to all demo notebooks
5. For each targeted notebook:
   - Set `rework_notes = <reviewer instructions>`
   - Spawn `/sql-notebook-generate` sub-agent with the rework notes
   - Run `/sql-notebook-validate`
   - If validated: replace the file on disk
6. Commit: `git commit -m "Rework: [brief summary of changes]"`
7. Push to the same branch (PR updates automatically)
8. Comment on the PR: `gh pr comment <PR_NUMBER> --body "Rework applied: [summary]"`

---

## Checkpoint File

**Path**: `.pipeline-cache/sql-week-NN-generation-state.json` (gitignored)

Update this file after every state transition. The file enables:
- Resume after timeout or interruption
- Visibility into pipeline progress
- Rework targeting (which notebooks needed fixes)

**Reset a week** (to force full regeneration):
```bash
rm .pipeline-cache/sql-week-NN-generation-state.json
```

---

## Prerequisites

- `curriculum/phase-2b-sql/teaching-curriculum.md` on disk (may be gitignored; must exist locally or in Routine workspace)
- `datasets/phase-2-python-sql.zip` in the repo — the validate skill extracts it to `/tmp/olist_data`; set `OLIST_DATA_PATH` to reuse a pre-extracted folder
- `GITHUB_TOKEN` environment variable (for `git push` via authenticated remote URL)
- `GDRIVE_PHASE2B_FOLDER_ID` environment variable — Google Drive folder ID for Phase 2b solutions upload
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_REVIEWER_CHAT_ID`, `CONTENT_PIPELINE_TOPIC_ID` (for Telegram — used by `content-publish.yml` GHA, not the Routine directly)

---

## Anchor references (single source of truth)

- **Setup cell**: `.claude/skills/sql-content-generator/assets/sql_setup.py` — the verbatim first code cell of every notebook.
- **Schema + verified stats**: `.claude/skills/sql-content-generator/references/olist_schema.md` — table/column names, join paths, and the verified values that seed check-cell asserts.

Every expected query result MUST come from `teaching-curriculum.md` or `olist_schema.md`. NEVER invent numbers.
