---
name: python-week-publish
description: >
  Perform all post-generation publishing operations for one Phase 2a Python week:
  update .gitignore for progressive disclosure, remove .gitkeep placeholders,
  git commit and push, create the GitHub PR, upload solutions to Google Drive,
  and send Telegram notifications. Reads the generation checkpoint to skip
  already-completed steps (safe to re-run after interruption).
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

git push -u origin content/${SLUG}
```

Checkpoint: set `publishing.git_committed = true`, `publishing.git_pushed = true`

### Step P6 — Create GitHub PR

Use the `gh` CLI or GitHub MCP tools to create the PR:

```bash
WEEK_NUM=$(printf "%02d" $WEEK)
SLUG="week-${WEEK_NUM}-<slug>"
TOPIC=$(cat .claude/cache/week-${WEEK_NUM}-context.json | python3 -c "import json,sys; print(json.load(sys.stdin)['topic_name'])")

# Count any needs_human_review notebooks
NEEDS_REVIEW=$(python3 -c "
import json
with open('.claude/cache/week-${WEEK_NUM}-generation-state.json') as f:
    s = json.load(f)
count = sum(1 for v in s['notebooks'].values() if v['status'] == 'needs_human_review')
print(count)
")

REVIEW_NOTE=""
if [ "$NEEDS_REVIEW" -gt 0 ]; then
  REVIEW_NOTE="⚠️ **${NEEDS_REVIEW} notebook(s) flagged for human review** — see NEEDS_HUMAN_REVIEW.md in the branch"
fi

# Programme-level week number
# Excel: 6 teaching + 2 project + 1 break = 9 weeks before Python starts
OFFSET="${PHASE_2A_WEEK_OFFSET:-9}"
PROGRAMME_WEEK=$((WEEK + OFFSET))

gh pr create \
  --title "Phase 2a Python — Week ${WEEK}: ${TOPIC}" \
  --body "## Phase 2a Python — Week ${WEEK}: ${TOPIC}
**Programme Week:** ${PROGRAMME_WEEK} of 16

### Generated Content
- ✅ Wednesday demo notebook
- ✅ Wednesday exercises notebook  
- ✅ Thursday demo notebook
- ✅ Thursday exercises notebook
- ✅ 2 lesson plans (self-contained)
- 📂 Solutions uploaded to Google Drive (gitignored)

${REVIEW_NOTE}

### Validation Summary
All code cells validated before commit. See \`.claude/cache/week-${WEEK_NUM}-*-validation.json\` for details.

### Review Commands
Post a comment with one of:
- \`/approve\` — merge and publish to students
- \`/rework [your feedback]\` — AI revises notebooks based on your notes
- \`/reject [reason]\` — close PR and delete branch" \
  --base main \
  --head content/${SLUG}
```

Save the PR number and URL to the generation state.

Checkpoint: set `publishing.pr_created = true`, `publishing.pr_url = <url>`, `publishing.pr_number = <number>`

### Step P7 — Upload solutions to Google Drive

Solutions are gitignored — Google Drive is the only permanent storage.

```bash
WEEK_NUM=$(printf "%02d" $WEEK)
SLUG="week-${WEEK_NUM}-<slug>"
TOPIC=$(cat .claude/cache/week-${WEEK_NUM}-context.json | python3 -c "import json,sys; print(json.load(sys.stdin)['topic_name'])")
DRIVE_FOLDER="Week ${WEEK_NUM} - ${TOPIC}"

# Upload solutions from both days
rclone copy \
  curriculum/phase-2a-python/weeks-01-08-teaching/${SLUG}/01-wednesday/solutions/ \
  "gdrive-course:${GDRIVE_PHASE2A_PATH}/${DRIVE_FOLDER}/wednesday-solutions/" \
  --progress

rclone copy \
  curriculum/phase-2a-python/weeks-01-08-teaching/${SLUG}/02-thursday/solutions/ \
  "gdrive-course:${GDRIVE_PHASE2A_PATH}/${DRIVE_FOLDER}/thursday-solutions/" \
  --progress
```

If rclone fails: log warning and continue. The PR is already created — this is recoverable.

Checkpoint: set `publishing.drive_uploaded = true`, `publishing.drive_folder = <folder name>`

### Step P8 — Send Telegram notification

```bash
WEEK_NUM=$(printf "%02d" $WEEK)
PR_URL=$(python3 -c "import json; s=json.load(open('.claude/cache/week-${WEEK_NUM}-generation-state.json')); print(s['publishing']['pr_url'])")

# Programme-level week number: read PHASE_2A_WEEK_OFFSET from env (default 8)
# Excel: 6 teaching + 2 project + 1 break = 9 weeks before Python starts
OFFSET="${PHASE_2A_WEEK_OFFSET:-9}"
PROGRAMME_WEEK=$((WEEK + OFFSET))

MSG="📬 *Phase 2a Python — Week ${WEEK} (Programme Week ${PROGRAMME_WEEK}) PR Ready*

*Topic:* ${TOPIC}
*Branch:* \`content/${SLUG}\`
*PR:* ${PR_URL}

✅ Notebooks validated
📂 Solutions on Google Drive

*Review actions (comment on PR):*
• \`/approve\` — merge and publish
• \`/rework [feedback]\` — AI reworks notebooks
• \`/reject [reason]\` — close and delete branch"

curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_REVIEWER_CHAT_ID}" \
  -d "message_thread_id=${CONTENT_PIPELINE_TOPIC_ID}" \
  -d "parse_mode=Markdown" \
  --data-urlencode "text=${MSG}"
```

Checkpoint: set `publishing.telegram_sent = true`

### Step P9 — Final summary

```
✅ Week N publishing complete
   PR: <url>
   Branch: content/<slug>
   Drive: <folder path>
   Notebooks validated: 6/6 (or 5/6 with 1 flagged for review)

Next: Review the PR and comment /approve when ready.
```

---

## Error Handling

- **git push fails** (branch exists remotely): use `git push --force-with-lease` for the content branch only
- **gh CLI not available**: use GitHub API directly via curl with `$GITHUB_TOKEN`
- **rclone not configured**: log warning, skip Drive upload, continue to Telegram
- **Telegram fails**: log warning, continue — PR is the primary deliverable
- **Any step fails after git push**: re-running this skill will skip completed steps and retry from the failed step
