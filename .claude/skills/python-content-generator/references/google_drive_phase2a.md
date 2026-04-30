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

## rclone Setup (one-time per machine)

Drive uploads use **rclone with a service account** — no OAuth browser flow, no token expiry.

### Prerequisites

- rclone is installed: `brew install rclone` (already installed on this machine)
- Service account JSON key file (obtain from instructor)
- rclone remote named `gdrive-course`

### Configure rclone

Add to `~/.config/rclone/rclone.conf`:

```ini
[gdrive-course]
type = drive
scope = drive
service_account_file = /path/to/phase2a-sa-key.json
root_folder_id = 1cPSs6q0kV28sr5m5Km31EooCuD1Lwuno
```

Or run `rclone config` and follow the prompts: New remote → `gdrive-course` → Google Drive → use service account file, then edit the config to add `root_folder_id`.

### Test the connection

```bash
rclone lsd "gdrive-course:"
```

---

## rclone Commands

The orchestrator script (`generate_week_content.py`) calls these automatically in Step 12. Manual equivalents:

### Upload solution notebooks for a week

```bash
WEEK_SLUG="week-01-python-fundamentals"
WEEK_DISPLAY="Week 1 - Python Fundamentals"
DRIVE_BASE="gdrive-course:Phase 2a - Python"

rclone copy \
  "curriculum/phase-2a-python/weeks-01-08-teaching/${WEEK_SLUG}/01-wednesday/solutions/" \
  "${DRIVE_BASE}/${WEEK_DISPLAY}/Wednesday/Solutions/" \
  --progress

rclone copy \
  "curriculum/phase-2a-python/weeks-01-08-teaching/${WEEK_SLUG}/02-thursday/solutions/" \
  "${DRIVE_BASE}/${WEEK_DISPLAY}/Thursday/Solutions/" \
  --progress
```

### Check what is already on Drive

```bash
rclone lsf "gdrive-course:Phase 2a - Python/"
```

---

## Co-teacher Setup

1. Obtain the service account JSON key from the instructor
2. Save it to a secure local path (e.g. `~/.config/rclone/phase2a-sa-key.json`)
3. Copy `.env.example` to `.env` and fill in the Drive values (see root `.env`):
   ```bash
   GDRIVE_REMOTE_NAME=gdrive-course
   GDRIVE_SA_KEY_PATH=~/.config/rclone/phase2a-sa-key.json
   GDRIVE_ROOT_FOLDER_ID=1cPSs6q0kV28sr5m5Km31EooCuD1Lwuno
   GDRIVE_PHASE2A_PATH=Phase 2a - Python
   ```
4. Add to `~/.config/rclone/rclone.conf`:
   ```ini
   [gdrive-course]
   type = drive
   scope = drive
   service_account_file = /Users/YOURNAME/.config/rclone/phase2a-sa-key.json
   root_folder_id = 1cPSs6q0kV28sr5m5Km31EooCuD1Lwuno
   ```
5. Test: `rclone lsd "gdrive-course:"`
6. The instructor must share the course Drive folder with the service account email (one-time, already done)
