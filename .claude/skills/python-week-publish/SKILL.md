---
name: python-week-publish
description: >
  Perform all post-generation publishing operations for one Phase 2a Python week:
  update .gitignore for progressive disclosure, remove .gitkeep placeholders,
  git commit and push, and upload solutions to Google Drive.
  PR creation and Telegram notification are handled automatically by the
  content-publish.yml GitHub Actions workflow triggered on push to content/week-*.
  Reads the generation checkpoint to skip already-completed steps (safe to re-run).
  Used internally by /python-content-generator. Can be called standalone to
  retry failed publishing steps without re-running generation.
---

# Python Week Publisher

Handles all publishing ops after notebooks are validated. Idempotent — reads `.claude/cache/week-NN-generation-state.json` and skips completed steps. Safe to call multiple times.

---

## Inputs

- **Week number** (1–8)
- **Week slug** (from the slug mapping in `/python-week-context`)
- **Generation state path**: `.claude/cache/week-NN-generation-state.json`

## Prerequisite

All 6 notebooks must have `status: "validated"` or `status: "needs_human_review"` in the generation state. Do not call this skill if any notebook has `status: "pending"` or `status: "generating"`.

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

## Publishing Steps (in order)

Read the generation state file first. Skip any step whose key is already `true` in the `publishing` block.

### Step P1 — Update .gitignore

Remove the whole-folder gitignore entry for this week and replace with solutions-only entries:

```bash
WEEK_NUM=$(printf "%02d" $WEEK)
SLUG="week-${WEEK_NUM}-<slug>"
WEEK_PATH="curriculum/phase-2a-python/weeks-01-08-teaching/${SLUG}"

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
find curriculum/phase-2a-python/weeks-01-08-teaching/<slug>/ -name ".gitkeep" -delete
echo "Removed .gitkeep files"
```

Checkpoint: set `publishing.gitkeep_removed = true`

### Step P3 — Generate lesson plans

For each day (Wed + Thu), write `lesson-plan.md` using the context bundle.

Lesson plan format — self-contained, not "see teaching-curriculum.md":

```markdown
# Week N — [Topic Name]: [Day] Session
## Phase 2a Python | PORA Academy Cohort 7

**Date**: [TBD] | **Duration**: 2 hours | **Location**: Google Colab

---

## Pre-Session Checklist

- [ ] Olist dataset accessible on Google Drive (shared folder link in Telegram)
- [ ] Demo notebook open in Colab: [notebook filename]
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
| 0:00–0:10 | Setup & recap | Students open Colab, load data |
| 0:10–0:45 | [Concept 1 name] | Demo + mini-challenge |
| 0:45–1:15 | [Concept 2 name] | Demo + mini-challenge |
| 1:15–1:45 | Group Exercise | [Group exercise title from context] |
| 1:45–2:00 | Debrief & preview | Share expected answers, preview next session |

---

## Key Concepts

[For each concept in context bundle]:
### [Concept Name]
[Concept description from context bundle]

Expected outputs:
[All verified_outputs from context bundle for this concept]

Common mistake to watch for:
[From §5 of the demo notebook]

---

## Group Exercise

[Full group exercise text from context bundle.group_exercise — verbatim]

**Expected outputs**: [verified_outputs for the exercise]

---
[Thursday only]:
## Weekly Assignment

[context bundle.assignment_text — verbatim]
```

Write to:
- `curriculum/.../week-NN-slug/01-wednesday/lesson-plan.md`
- `curriculum/.../week-NN-slug/02-thursday/lesson-plan.md`

Checkpoint: set `publishing.lesson_plans_written = true`

### Step P4 — Week 1 resources (Week 1 only)

For Week 1 only, copy these files into `01-wednesday/lecture-materials/`:
```bash
cp .claude/skills/python-content-generator/assets/data_loading.py \
   curriculum/.../week-01-python-fundamentals/01-wednesday/lecture-materials/
```

Checkpoint: set `publishing.resources_copied = true` (or skip + set true for non-Week-1)

### Step P5 — Git commit and push

```bash
git config user.email "pipeline@pora.academy"
git config user.name "PORA Content Pipeline"

SLUG="week-$(printf '%02d' $WEEK)-<slug>"
TOPIC=$(cat .claude/cache/week-${WEEK}-context.json | python3 -c "import json,sys; print(json.load(sys.stdin)['topic_name'])")

git add curriculum/phase-2a-python/weeks-01-08-teaching/${SLUG}/
git add .gitignore

git commit -m "Add Phase 2a Python Week ${WEEK} content: ${TOPIC}

Generated by Claude Routine — 6 notebooks validated, lesson plans complete.
Branch: content/${SLUG}"

# Embed GITHUB_TOKEN in remote URL — required in Routine environment (no interactive auth)
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/autom8or-com/data-analysis-and-ai-automation-course-cohort-7.git"
git push -u origin content/${SLUG}
```

Checkpoint: set `publishing.git_committed = true`, `publishing.git_pushed = true`

### Step P6 — (handled by GitHub Actions)

PR creation is handled automatically by `.github/workflows/content-publish.yml`,
which triggers on the `git push` in Step P5. No action required here.

Checkpoint: set `publishing.pr_created = "handled_by_gha"`

### Step P7 — Upload solutions to Google Drive

Solutions are gitignored — Google Drive is the only permanent storage.

**Prerequisites**: The Google Drive MCP connector must be added to this Routine's connectors at `claude.ai/code/routines`. The `GDRIVE_PHASE2A_FOLDER_ID` environment variable must be set in the Routine's environment (the Drive folder ID of the Phase 2a solutions parent folder).

Use the Google Drive MCP tools to complete these steps:

1. **Find or create the week subfolder** inside the Phase 2a parent folder (`GDRIVE_PHASE2A_FOLDER_ID`):
   - Target folder name: `Week NN - <Topic Name>` (e.g. `Week 02 - Collections & Control Flow`)
   - Search for an existing folder with that name under the parent ID
   - If not found, create it

2. **Find or create** `wednesday-solutions` and `thursday-solutions` sub-folders inside the week folder

3. **Upload each solution notebook** using the MCP create/upload tool:
   - Read each `.ipynb` file from `curriculum/.../week-NN-slug/01-wednesday/solutions/`
   - Upload to the `wednesday-solutions` folder
   - Repeat for `02-thursday/solutions/` → `thursday-solutions` folder

If any MCP call fails: log the warning and continue. The PR is already created — Drive upload is recoverable.

Checkpoint: set `publishing.drive_uploaded = true`, `publishing.drive_folder = "Week NN - <Topic>"`

### Step P8 — (handled by GitHub Actions)

Telegram notification to the reviewer group is sent by `.github/workflows/content-publish.yml`
immediately after PR creation. No action required here.

Checkpoint: set `publishing.telegram_sent = "handled_by_gha"`

### Step P9 — Final summary

```
✅ Week N publishing complete
   Branch: content/<slug>
   Drive: <folder path>
   Notebooks validated: 6/6 (or 5/6 with 1 flagged for review)
   PR + Telegram: triggered by git push → content-publish.yml workflow

Next: Wait ~30s for content-publish.yml to create the PR, then check GitHub.
      Review the PR and comment /approve when ready.
```

---

## Error Handling

- **git push fails** (branch exists remotely): use `git push --force-with-lease` for the content branch only
- **Google Drive MCP unavailable**: log warning, skip Drive upload, continue — PR creation still triggers from the push
- **PR not created after push**: check GitHub Actions tab for `content-publish.yml` run; re-trigger by pushing an empty commit if needed
- **Any step fails after git push**: re-running this skill will skip completed steps and retry from the failed step
