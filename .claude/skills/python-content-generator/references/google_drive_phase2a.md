# Google Drive Setup for Phase 2a Python

## Root Folder Structure

| Name | ID | Purpose |
|---|---|---|
| Data Analysis and AI Automation Course Cohort 7 | `1cPSs6q0kV28sr5m5Km31EooCuD1Lwuno` | Root of all course content |
| Phase 2a - Python | Discovered/created on first run | Week folders + solution notebooks |

## Week Folder Names (Drive display)

| Week | Drive Folder Name |
|---|---|
| 1 | `Week 1 - Python Fundamentals` |
| 2 | `Week 2 - Collections & Control Flow` |
| 3 | `Week 3 - Functions & Data` |
| 4 | `Week 4 - Pandas Introduction` |
| 5 | `Week 5 - Groupby & Aggregation` |
| 6 | `Week 6 - Data Cleaning` |
| 7 | `Week 7 - Merging DataFrames` |
| 8 | `Week 8 - Visualisation & Streamlit` |

## Folder Structure Under Each Week

```
Week N - [Topic]
├── Wednesday
│   └── Solutions/
│       └── week-NN-wed-solutions.ipynb
└── Thursday
    └── Solutions/
        └── week-NN-thu-solutions.ipynb
```

---

## Timing: Drive Upload Happens Pre-Merge (Step P7)

Drive upload runs during the Routine (Step P7 of `/python-week-publish`), **before the PR is merged**.

This is by design:
- Solutions notebooks are **gitignored** — they are never committed to git
- Drive is the only permanent storage for solutions
- Solutions need to be on Drive *before* content goes live, so instructors have the answer key ready
- The reviewer can verify solutions on Drive during PR review

If content is reworked, solutions are re-uploaded (overwrite existing files).

---

## How Drive Upload Works (MCP Connector)

Drive uploads use the **Google Drive MCP connector** added to the Claude Routine — no rclone, no service account JSON key, no OAuth setup required.

The connector is already added to both Routines (`pora-content-pipeline` environment → Connectors tab → Google Drive ✅).

The `/python-week-publish` skill (Step P7) uses MCP tools to:
1. Find or create `Week NN - <Topic>` folder under `GDRIVE_PHASE2A_FOLDER_ID`
2. Find or create `wednesday-solutions` and `thursday-solutions` sub-folders
3. Upload each `.ipynb` solution file

### Required environment variable

`GDRIVE_PHASE2A_FOLDER_ID` — the Drive folder ID of the Phase 2a solutions parent folder (the "Phase 2a - Python" folder under the course root). Set in the Routine's environment tab.

---

## Co-teacher Access

No setup required. The Google Drive MCP connector authenticates via the connected Google account (the same account used to set up the connector in Claude Code). Co-teachers need to be given Viewer/Editor access to the Drive folder directly — no rclone or service account needed.
