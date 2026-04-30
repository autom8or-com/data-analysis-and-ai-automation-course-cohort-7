---
name: excel-content-generator
description: >
  Generates complete weekly session content for Phase 1 Excel of the PORA Academy curriculum.
  Produces filled lesson plans, instructor demo workbooks, student exercise workbooks, and
  solution workbooks for both Wednesday and Thursday sessions of a given week.
  Always branches off main using the naming pattern content/{slug}.

  Trigger this skill whenever the user asks to generate, create, build, or prepare content
  for a specific phase and week — e.g. "generate content for phase 1, week 2",
  "create week 3 Excel materials", "build week 4 files". The phase is required in the trigger.
  Do NOT trigger for general Excel help, curriculum editing, or non-Phase 1 phases.
---

## Context

- Repository: `/Users/HP/data-analysis-and-ai-automation-course-cohort-7/`
- Curriculum source: `curriculum/phase-1-excel/teaching-curriculum.md`
- Dataset zip: `datasets/phase-1-excel/teaching/teaching-data.zip` — contains `data.csv` (541,909 rows, 8 columns)
- Session folders: `curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/`
  - Each week has `01-wednesday/` and `02-thursday/`
  - Each day has: `lesson-plan.md`, `lecture-materials/`, `exercises/`, `solutions/`

---

## Workflow

### Step 1 — Parse the request

Extract from the user's message:
- **Week number** (1–6)
- Look up the matching folder slug from this table:

| Week | Folder slug |
|---|---|
| 1 | `week-01-data-import-and-navigation` |
| 2 | `week-02-excel-basics` |
| 3 | `week-03-advanced-functions` |
| 4 | `week-04-pivot-tables-and-charts` |
| 5 | `week-05-power-query-part-1` |
| 6 | `week-06-power-query-part-2` |

### Step 2 — Create the git branch

```bash
cd /Users/HP/data-analysis-and-ai-automation-course-cohort-7
git checkout main
git checkout -b content/week-NN-slug
```

Replace `NN` with zero-padded week number and `slug` with the folder slug above.
Example: `content/week-02-excel-basics`

### Step 3 — Read the curriculum

Read `curriculum/phase-1-excel/teaching-curriculum.md` and extract the full content for the requested week — both Wednesday and Thursday sessions, including:
- Learning objectives
- Session outline and timings
- All formulas and verified outputs
- Group exercise questions and expected answers
- Weekly assignment text

Keep this in memory — you will use it to fill the lesson plans and to design the workbooks.

### Step 4 — Extract the data sample

The 1,000-row sample drives all Excel workbooks this week. Extract it once:

```python
import zipfile
import pandas as pd

zip_path = "/Users/HP/data-analysis-and-ai-automation-course-cohort-7/datasets/phase-1-excel/teaching/teaching-data.zip"

# The CSV lives at a nested path inside the zip — not at the root
with zipfile.ZipFile(zip_path) as z:
    with z.open("datasets/phase-1-excel/teaching/data.csv") as f:
        df = pd.read_csv(f, nrows=1000, dtype=str)  # dtype=str preserves leading zeros, InvoiceNo as text
```

Reuse `df` for all workbooks — do not re-extract multiple times.

> **Troubleshooting:** If you get a `KeyError` on the file path, run `z.namelist()` to print the actual paths inside the zip before opening.

**Column order:** InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

### Step 5 — Fill lesson-plan.md (both days)

For each day, rewrite the existing sparse `lesson-plan.md` template with the full session content drawn from the curriculum. Use this structure:

```markdown
# Week NN — [Day]: [Session Title]
## Phase 1 Excel | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** NN of 6
**Session:** [Wednesday / Thursday]
**Topic:** [Topic name]

---

## Pre-Session Checklist

- [ ] Dataset loaded (data.csv — UCI Online Retail, 541,909 rows)
- [ ] Demo workbook open: `lecture-materials/week-NN-[wed|thu]-demo.xlsx`
- [ ] Exercise file ready: `exercises/week-NN-[wed|thu]-exercises.xlsx`
- [ ] Projector / screen sharing ready

---

## Learning Objectives

[Pull verbatim from curriculum]

---

## Session Plan

| Time | Activity | Notes |
|---|---|---|
[Fill from curriculum timings — adapt to 2-hour block]

---

## Concepts & Verified Outputs

[For each concept in the session: what to demonstrate, the exact formula, and the verified output value from the curriculum]

---

## Group Exercise

[Pull full exercise questions and expected answers from curriculum]

---

## Assignment

[Pull assignment text verbatim from curriculum — Thursday sessions only]

---

## Instructor Notes

[Include any instructor notes or common mistakes from the curriculum for this week]
```

### Step 6 — Create Excel workbooks

Create **3 workbooks per day × 2 days = 6 workbooks** total.

Use `openpyxl` to create each file. Apply the `document-skills:xlsx` skill for technical guidance on openpyxl patterns, formatting, and formula writing.

> **Solutions are git-ignored.** Every `solutions/` folder is explicitly listed in `.gitignore`. Students who clone the repo will never see solution workbooks — they only exist on the instructor's local machine and on branches pushed by the instructor. Never put answers in the exercise workbook.

#### File naming and locations

| Day | Workbook | Path |
|---|---|---|
| Wednesday | Demo | `01-wednesday/lecture-materials/week-NN-wed-demo.xlsx` |
| Wednesday | Exercises | `01-wednesday/exercises/week-NN-wed-exercises.xlsx` |
| Wednesday | Solutions | `01-wednesday/solutions/week-NN-wed-solutions.xlsx` |
| Thursday | Demo | `02-thursday/lecture-materials/week-NN-thu-demo.xlsx` |
| Thursday | Exercises | `02-thursday/exercises/week-NN-thu-exercises.xlsx` |
| Thursday | Solutions | `02-thursday/solutions/week-NN-thu-solutions.xlsx` |

All paths are relative to the week folder, e.g.:
`curriculum/phase-1-excel/weeks-01-06-teaching/week-02-excel-basics/01-wednesday/lecture-materials/week-02-wed-demo.xlsx`

#### Workbook roles

**Demo workbook** (`*-demo.xlsx`):
- Shows the *end state* of the instructor's live demonstration — the completed sheets the instructor will build step by step in class
- Includes the 1,000-row `Raw Data` sheet plus any additional sheets built during the session (e.g. `Summary Stats`, `Pivot Analysis`, `Dashboard`)
- All formulas are written and returning verified values
- Add a first sheet called `Instructor Notes` with: session topic, verified outputs to confirm during demo, and common mistakes to watch

**Exercise workbook** (`*-exercises.xlsx`):
- Has the 1,000-row `Raw Data` sheet (identical to demo)
- Has an `Instructions` sheet listing all exercise questions (numbered, pulled from curriculum)
- Has a `Workspace` sheet with column headers and any scaffolding (e.g. question labels, partial table structure) but **formula cells are blank** — students fill them in
- Never pre-fill the answer cells

**Solution workbook** (`*-solutions.xlsx`):
- Identical structure to exercise workbook
- All formula cells filled with correct answers
- Add a note row above each answer explaining what the formula does (e.g. a row above: `"Q1: Count UK transactions using COUNTIF"`)

#### Week-by-week sheet structure

The sheets to build vary by week — derive from the curriculum content:

| Week | Demo sheets | Exercise/Solution extra sheet |
|---|---|---|
| 1 | `Instructor Notes`, `Raw Data` | `Instructions` (written questions only — no formula workspace) |
| 2 | `Instructor Notes`, `Raw Data`, `Summary Stats` | `Instructions`, `Summary Stats Workspace` |
| 3 | `Instructor Notes`, `Raw Data`, `Revenue Analysis` | `Instructions`, `Formula Workspace` |
| 4 | `Instructor Notes`, `Raw Data`, `Pivot Results` (static summary tables — note: pivot tables cannot be created programmatically; provide static equivalent and a note for instructor) | `Instructions`, `Summary Workspace` |
| 5 | `Instructor Notes`, `Raw Data`, `PQ Steps Log` (table showing each step, row count before/after) | `Instructions`, `Cleaning Tracker` |
| 6 | `Instructor Notes`, `Raw Data`, `Clean Data` (filtered 1K sample), `Calculated Columns` | `Instructions`, `Column Workspace` |

#### Formula integrity rule

Every formula written into a workbook must:
1. Reference cells that actually exist in the 1,000-row sample
2. Produce a non-zero/non-error result on the sample
3. Use the correct column letters (A=InvoiceNo, B=StockCode, C=Description, D=Quantity, E=InvoiceDate, F=UnitPrice, G=CustomerID, H=Country)

For formulas that aggregate the full dataset (e.g. `COUNTA(A:A)-1 = 541,909`), note in the cell comment or adjacent cell: *"Full dataset answer: [verified value]. Your 1,000-row sample will return a different number — this is expected."*

#### Formatting standards

- Header row: bold, white text, dark blue fill (`#1F3864`)
- Alternate row shading: light blue (`#DCE6F1`) every other row
- Freeze top row on all data sheets
- Column widths: auto-fit to content
- Number format: currency columns (UnitPrice, Revenue) → `£#,##0.00`; quantity → `#,##0`

### Step 7 — Populate resources (Week 1 only)

When generating Week 1, fill in the three sparse resource files in `curriculum/phase-1-excel/resources/` using content from the curriculum. They contain scaffold tables with blank cells — complete them:

- **`excel-formula-cheatsheet.md`** — fill in the Purpose and Example columns for every formula row across all sections, using the verified examples from the curriculum (Weeks 1–6).
- **`keyboard-shortcuts.md`** — fill in every blank Action entry; add any shortcuts referenced across all 6 weeks that aren't already listed.
- **`power-query-reference.md`** — fill in the M formula column for every step row, and complete the Custom Column Formulas table with verified values from Weeks 5–6.

These are student-facing reference cards — write complete, usable entries, not placeholder text.

### Step 8 — Remove .gitkeep files

After creating real files in a folder, delete the `.gitkeep` placeholder:

```bash
rm path/to/folder/.gitkeep
```

Only remove `.gitkeep` in folders that now have actual content.

### Step 9 — Update .gitignore

The repo uses **progressive disclosure**: each week's folder is hidden entirely until its content is generated. Released weeks expose only their `solutions/` as hidden (instructor-only); everything else is visible to students.

**The `.gitignore` structure on main:**
- Released weeks → two `solutions/` entries only (e.g. `week-01.../solutions/`, `week-02.../solutions/`)
- Unreleased weeks → one whole-folder entry (e.g. `curriculum/phase-1-excel/weeks-01-06-teaching/week-03-advanced-functions/`)
- All future phases (Phase 2a, 2b, 2c, Phase 3) → whole-folder entries for their entire `weeks-*-teaching/` directories

**Week 1:** Already live, solutions already ignored. Skip this step.

**Weeks 2–6:** In `.gitignore`, find the whole-folder entry for this week and **replace** it with two `solutions/`-only entries:

```
# Before (unreleased):
curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/

# After (released — solutions still hidden):
curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/01-wednesday/solutions/
curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/02-thursday/solutions/
```

The two `solutions/` entries for weeks 2–6 are **already present** in `.gitignore` (below the whole-folder line) — you only need to delete the whole-folder line. The solutions entries stay exactly as they are.

Stage `.gitignore` together with the week content so they land in the same commit.

### Step 10 — Commit to branch

Stage and commit all changes:

```bash
git add curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/
git add .gitignore
git commit -m "Add Week NN content: lesson plans, demo workbooks, exercises, solutions"
```

Inform the user which branch the content is on and suggest they review before merging to main.

---

### Step 11 — Upload solutions to Google Drive

After committing, upload the two solution files to the course Drive folder.

#### Hardcoded folder IDs

| Folder | ID |
|---|---|
| Root — Data Analysis and AI Automation Course Cohort 7 | `1cPSs6q0kV28sr5m5Km31EooCuD1Lwuno` |
| Phase 1 - Excel | `1EP7dR1ns_6iiVS7mbqPW505ZZeybceOL` |

> Other phases will have their own IDs added here when those skills are built.

#### Week name lookup (human-readable Drive folder names)

| Week | Drive folder name |
|---|---|
| 1 | `Week 1 - Data Import and Navigation` |
| 2 | `Week 2 - Excel Basics` |
| 3 | `Week 3 - Advanced Functions` |
| 4 | `Week 4 - Pivot Tables and Charts` |
| 5 | `Week 5 - Power Query Part 1` |
| 6 | `Week 6 - Power Query Part 2` |

#### 11a — Check if the week folder already exists

Search for the week folder by name under the Phase 1 folder:

```bash
gws drive files list --params "{\"q\": \"name = 'WEEK_FOLDER_NAME' and 'PHASE1_ID' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false\", \"pageSize\": 1}" 2>/dev/null
```

Replace `WEEK_FOLDER_NAME` with the human-readable name (e.g. `Week 2 - Excel Basics`) and `PHASE1_ID` with `1EP7dR1ns_6iiVS7mbqPW505ZZeybceOL`.

- If the response contains an `"id"` field → **skip folder creation, notify the user** ("Week N folder already exists on Drive — skipping folder creation, uploading solutions only"), capture the existing week folder ID, then jump to step 11c.
- If the `files` array is empty → proceed to 11b.

#### 11b — Create the week's folder structure

Create four folders in sequence, capturing each ID for the next call:

```bash
# 1. Week folder under Phase 1
WEEK_ID=$(gws drive files create --json '{"name": "WEEK_FOLDER_NAME", "mimeType": "application/vnd.google-apps.folder", "parents": ["1EP7dR1ns_6iiVS7mbqPW505ZZeybceOL"]}' 2>/dev/null | grep '"id"' | sed 's/.*"id": "\(.*\)".*/\1/')

# 2. Wednesday subfolder
WED_ID=$(gws drive files create --json "{\"name\": \"Wednesday\", \"mimeType\": \"application/vnd.google-apps.folder\", \"parents\": [\"$WEEK_ID\"]}" 2>/dev/null | grep '"id"' | sed 's/.*"id": "\(.*\)".*/\1/')

# 3. Thursday subfolder
THU_ID=$(gws drive files create --json "{\"name\": \"Thursday\", \"mimeType\": \"application/vnd.google-apps.folder\", \"parents\": [\"$WEEK_ID\"]}" 2>/dev/null | grep '"id"' | sed 's/.*"id": "\(.*\)".*/\1/')

# 4. Solutions under Wednesday
WED_SOL_ID=$(gws drive files create --json "{\"name\": \"Solutions\", \"mimeType\": \"application/vnd.google-apps.folder\", \"parents\": [\"$WED_ID\"]}" 2>/dev/null | grep '"id"' | sed 's/.*"id": "\(.*\)".*/\1/')

# 5. Solutions under Thursday
THU_SOL_ID=$(gws drive files create --json "{\"name\": \"Solutions\", \"mimeType\": \"application/vnd.google-apps.folder\", \"parents\": [\"$THU_ID\"]}" 2>/dev/null | grep '"id"' | sed 's/.*"id": "\(.*\)".*/\1/')
```

#### 11c — Upload the solution files

Upload both solution workbooks to their respective Solutions folders:

```bash
# Wednesday solution
gws drive files create \
  --params '{"uploadType": "multipart"}' \
  --json "{\"name\": \"week-NN-wed-solutions.xlsx\", \"parents\": [\"$WED_SOL_ID\"]}" \
  --upload "curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/01-wednesday/solutions/week-NN-wed-solutions.xlsx" \
  2>/dev/null

# Thursday solution
gws drive files create \
  --params '{"uploadType": "multipart"}' \
  --json "{\"name\": \"week-NN-thu-solutions.xlsx\", \"parents\": [\"$THU_SOL_ID\"]}" \
  --upload "curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/02-thursday/solutions/week-NN-thu-solutions.xlsx" \
  2>/dev/null
```

All paths are relative to the repo root `/Users/HP/data-analysis-and-ai-automation-course-cohort-7/`.

#### 11d — Report to user

Tell the user:
- Whether folders were created or already existed
- Confirmation that both solution files were uploaded
- Direct link to the week folder: `https://drive.google.com/drive/folders/WEEK_ID`

---

## Special cases

**Week 1 (no formulas):** Both sessions are navigation-only. The exercise workbook contains only the `Instructions` sheet with the 5 written questions. No `Workspace` sheet. The `Raw Data` sheet is still included so students can follow along. The solution workbook has the `Instructions` sheet with the expected answers written in plain text.

**Weeks 4–6 (pivot tables / Power Query):** openpyxl cannot create pivot tables or Power Query connections. For these weeks:
- The demo workbook shows *static result tables* — formatted tables containing the expected pivot/query output values from the curriculum (verified numbers). Include a clearly visible note in the sheet header: `"⚠ Instructor creates this live as a pivot table / Power Query step — this sheet shows the expected end result"`
- The exercise workbook has an `Instructions` sheet listing every exercise question, plus an empty formatted table shell (headers only, no data) for students to build into
- The solution workbook has the same static result tables as the demo workbook, with an additional column or note showing which formula or step produced each value
- The `Instructor Notes` sheet in the demo workbook must list, step by step, every live action the instructor performs to reproduce the static result shown

**Week 6 (capstone):** Thursday is the full pipeline — both the demo and exercise files are larger, incorporating all previous concepts. Build both the `Raw Data` and `Clean Data` sheets.

---

### Step 12 — Update NocoDB weekly schedule table

After the Google Drive upload, add or update the row for this week in the NocoDB `weekly_schedule` table so the lesson plan URLs and **XLSX sheet names** stay in sync.

**Connection details (from .env):**
- NocoDB base URL: `https://nocodb.aiautom8or.com`
- Table ID: `msdb2xf97gf7wb3`
- API token: `${NOCODB_API_TOKEN}`
- Auth header: `xc-token: <token>`

**URL pattern** — both URLs follow this structure (swap `01-wednesday` / `02-thursday`):
```
https://raw.githubusercontent.com/autom8or-com/data-analysis-and-ai-automation-course-cohort-7/main/curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug/01-wednesday/lesson-plan.md
```

#### 12a — Extract sheet names from generated workbooks

Before the NocoDB call, extract sheet names from all 6 XLSX files created in Step 6 using openpyxl. Build two JSON objects — one per day — mapping each filename to its list of sheet names.

```python
import json, glob, os
import openpyxl

week_dir = "curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug"
sheet_data = {}

for day_key, day_folder in [("wed", "01-wednesday"), ("thu", "02-thursday")]:
    day_path = os.path.join(week_dir, day_folder)
    mapping = {}
    for xlsx_path in sorted(glob.glob(os.path.join(day_path, "**", "*.xlsx"), recursive=True)):
        wb = openpyxl.load_workbook(xlsx_path, read_only=True)
        mapping[os.path.basename(xlsx_path)] = wb.sheetnames
        wb.close()
    sheet_data[day_key] = json.dumps(mapping)
```

The two resulting JSON strings go into `wed_sheet_names` and `thu_sheet_names` fields below. Example value:
```json
{"week-03-wed-demo.xlsx": ["Instructor Notes", "Raw Data", "Revenue Analysis"], "week-03-wed-exercises.xlsx": ["Instructions", "Raw Data", "Formula Workspace", "Revenue Analysis"], "week-03-wed-solutions.xlsx": ["Instructions", "Raw Data", "Formula Workspace", "Revenue Analysis"]}
```

#### 12b — Check if a record for this week already exists

```bash
curl -s "https://nocodb.aiautom8or.com/api/v2/tables/msdb2xf97gf7wb3/records?where=(week_number,eq,NN)" \
  -H "xc-token: ${NOCODB_API_TOKEN}"
```

- If `pageInfo.totalRows > 0` → the record exists; capture its `Id` and **go to 12d (update)**
- If `pageInfo.totalRows == 0` → no record yet; **go to 12c (create)**

#### 12c — Create a new record

```bash
curl -s -X POST "https://nocodb.aiautom8or.com/api/v2/tables/msdb2xf97gf7wb3/records" \
  -H "xc-token: ${NOCODB_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '[{
    "week_number": NN,
    "topic_name": "TOPIC_NAME",
    "phase": "phase-1-excel",
    "wed_lesson_plan_url": "WED_URL",
    "thu_lesson_plan_url": "THU_URL",
    "wed_sheet_names": "WED_SHEET_NAMES_JSON",
    "thu_sheet_names": "THU_SHEET_NAMES_JSON"
  }]'
```

**Topic name lookup:**

| Week | topic_name |
|---|---|
| 1 | `Data Import & Navigation` |
| 2 | `Excel Basics` |
| 3 | `Advanced Functions` |
| 4 | `Pivot Tables & Charts` |
| 5 | `Power Query Part 1` |
| 6 | `Power Query Part 2` |

After creating, verify by re-fetching the record and confirm `totalRows == 1`.

#### 12d — Update an existing record

If a record already existed (from 12b), patch it with fresh URLs and sheet names using its `Id`:

```bash
curl -s -X PATCH "https://nocodb.aiautom8or.com/api/v2/tables/msdb2xf97gf7wb3/records" \
  -H "xc-token: ${NOCODB_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '[{
    "Id": RECORD_ID,
    "wed_lesson_plan_url": "WED_URL",
    "thu_lesson_plan_url": "THU_URL",
    "wed_sheet_names": "WED_SHEET_NAMES_JSON",
    "thu_sheet_names": "THU_SHEET_NAMES_JSON"
  }]'
```

#### 12e — Report to user

Tell the user whether the record was created or updated, and confirm both lesson plan URLs and sheet name counts that are now stored.

---

### Step 13 — Send Telegram alert to facilitators' group

After the NocoDB update, send a summary alert to the facilitators' group.

**Connection details (from .env):**
- Bot token: `${TELEGRAM_BOT_TOKEN}`
- Facilitators' group chat ID: `${TELEGRAM_GROUP_CHAT_ID}` (Pora-Academy_Data-Analytics_Resource_Group)

**Rotating Bible quote** — pick by week number (cycles back if > 6):

| Week | Quote |
|---|---|
| 1 | *"And whatever you do, do it heartily, as to the Lord and not to men."* — Colossians 3:23 |
| 2 | *"Serve wholeheartedly, as if you were serving the Lord, not people."* — Ephesians 6:7 |
| 3 | *"I can do all things through Christ who strengthens me."* — Philippians 4:13 |
| 4 | *"Each of you should use whatever gift you have received to serve others, as faithful stewards of God's grace."* — 1 Peter 4:10 |
| 5 | *"Be strong and courageous. Do not be afraid, for the Lord your God will be with you wherever you go."* — Joshua 1:9 |
| 6 | *"Those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary."* — Isaiah 40:31 |

Build and send the message:

```bash
# Select quote by week number (1-indexed, wraps after 6)
QUOTES=(
  ""And whatever you do, do it heartily, as to the Lord and not to men." — Colossians 3:23"
  ""Serve wholeheartedly, as if you were serving the Lord, not people." — Ephesians 6:7"
  ""I can do all things through Christ who strengthens me." — Philippians 4:13"
  ""Each of you should use whatever gift you have received to serve others, as faithful stewards of God's grace." — 1 Peter 4:10"
  ""Be strong and courageous. Do not be afraid, for the Lord your God will be with you wherever you go." — Joshua 1:9"
  ""Those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary." — Isaiah 40:31"
)
QUOTE=${QUOTES[$(( (NN - 1) % 6 ))]}

curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_GROUP_CHAT_ID}" \
  --data-urlencode "text=🎉 Week NN content is ready!

📚 Week NN — TOPIC_NAME

Lesson plans and exercises are live on GitHub:
🔗 https://github.com/autom8or-com/data-analysis-and-ai-automation-course-cohort-7/tree/main/curriculum/phase-1-excel/weeks-01-06-teaching/week-NN-slug

Solution workbooks are on Google Drive:
🔗 https://drive.google.com/drive/folders/WEEK_DRIVE_ID

May God grant you grace this week. 🙏

✨ $QUOTE"
```

Replace `NN`, `TOPIC_NAME`, `week-NN-slug`, and `WEEK_DRIVE_ID` with values from earlier steps.

---

## Output summary to user

After all files are created, tell the user:
- Branch name
- List of all files created (relative paths)
- Any formulas that are sample-only (full-dataset verified values noted)
- Google Drive: whether the week folder was created or already existed, confirmation both solution files were uploaded, and the link to the week folder
- NocoDB: whether the weekly schedule record was created or updated, the two lesson plan URLs, and the sheet names stored per day (file count + total sheet count)
- Next steps: review the branch, open workbooks to spot-check formulas, then merge to main when ready
