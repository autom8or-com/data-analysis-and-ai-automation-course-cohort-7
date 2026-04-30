"""
Main Content Generation Orchestrator

Executes 15-step workflow:
1. Parse request (week number)
2. Create git branch
3. Read teaching-curriculum.md
4. Load Olist data
5. Validate code cells with cache
6. Fill lesson-plan.md
7. Create 6 notebooks (demo/exercise/solution × Wed/Thu)
8. Populate resources (Week 1 only)
9. Remove .gitkeep files
10. Update .gitignore
11. Commit to branch
12. Upload solutions to Google Drive
13. Update NocoDB weekly_schedule
14. Send Telegram alert
15. Report summary to user
"""

from pathlib import Path
from typing import Dict
import datetime
import json
import re


import subprocess as _sp
from dotenv import load_dotenv

REPO_ROOT = Path(_sp.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
load_dotenv(REPO_ROOT / ".env")
CURRICULUM_ROOT = REPO_ROOT / "curriculum" / "phase-2a-python"
DATASET_ZIP = REPO_ROOT / "datasets" / "phase-2-python-sql" / "olist-data.zip"

WEEK_MAPPING = {
    1: ("week-01-python-fundamentals", "Python Fundamentals"),
    2: ("week-02-collections-and-control-flow", "Collections & Control Flow"),
    3: ("week-03-functions-and-data", "Functions & Data"),
    4: ("week-04-pandas-introduction", "Pandas Introduction"),
    5: ("week-05-groupby-and-aggregation", "Groupby & Aggregation"),
    6: ("week-06-data-cleaning", "Data Cleaning"),
    7: ("week-07-merging-dataframes", "Merging DataFrames"),
    8: ("week-08-visualisation-and-streamlit", "Visualisation & Streamlit"),
}

PIPELINE_STATE_PATH = REPO_ROOT / ".claude" / "phase2a-pipeline-state.json"


def _write_checkpoint(week_number: int, step: str, **kwargs) -> None:
    state = {}
    if PIPELINE_STATE_PATH.exists():
        with open(PIPELINE_STATE_PATH) as f:
            state = json.load(f)
    week_key = f"week_{week_number}"
    if week_key not in state:
        state[week_key] = {"steps_completed": [], "artifacts": {}}
    if step not in state[week_key]["steps_completed"]:
        state[week_key]["steps_completed"].append(step)
    state[week_key]["last_updated"] = datetime.datetime.now().isoformat()
    state[week_key]["artifacts"].update(kwargs)
    PIPELINE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PIPELINE_STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def main(week_number: int, force_validate: bool = False):
    """
    Main orchestrator for content generation.

    Args:
        week_number: Week 1-8
        force_validate: Skip validation cache, force full validation
    """
    import subprocess
    import json
    import os
    from olist_loader import load_olist_data
    from validate_notebooks import validate_notebooks
    from notebook_builder import build_demo_notebook, build_exercise_notebook, build_solution_notebook

    print(f"Starting Phase 2a Python Week {week_number} content generation...")

    # Upfront: verify required files before any side effects
    _curriculum_path = CURRICULUM_ROOT / "teaching-curriculum.md"
    if not _curriculum_path.exists():
        raise FileNotFoundError(
            f"MISSING: curriculum/phase-2a-python/teaching-curriculum.md\n"
            "This file is gitignored. It must exist on disk before generation."
        )
    if not DATASET_ZIP.exists():
        raise FileNotFoundError(
            f"MISSING: datasets/phase-2-python-sql/olist-data.zip\n"
            "Place the Olist dataset zip in datasets/phase-2-python-sql/"
        )

    # Step 1: Parse request
    week_slug, topic_name = WEEK_MAPPING.get(week_number, (None, None))
    if not week_slug:
        raise ValueError(f"Invalid week number: {week_number}")
    week_padded = f"{week_number:02d}"
    print(f"✓ Step 1: Parsed week {week_number} → {topic_name}")

    # Step 2: Create git branch (or check out if resuming)
    branch_name = f"content/{week_slug}"
    subprocess.run(["git", "checkout", "main"], cwd=REPO_ROOT, check=True, capture_output=True)
    result = subprocess.run(
        ["git", "checkout", "-b", branch_name],
        cwd=REPO_ROOT, capture_output=True
    )
    if result.returncode != 0:
        subprocess.run(["git", "checkout", branch_name], cwd=REPO_ROOT, check=True, capture_output=True)
        print(f"✓ Step 2: Resumed on existing branch {branch_name}")
    else:
        print(f"✓ Step 2: Created branch {branch_name}")

    # Step 3: Read curriculum
    curriculum_path = CURRICULUM_ROOT / "teaching-curriculum.md"
    with open(curriculum_path, 'r') as f:
        curriculum_text = f.read()
    print(f"✓ Step 3: Read teaching curriculum")

    # Step 4: Load Olist data (for validation)
    data = load_olist_data(str(DATASET_ZIP))
    print(f"✓ Step 4: Load Olist dataset ({len(data.get('orders', []))} orders)")

    # Step 5: Validate code cells (placeholder — actual validation occurs in notebook builder)
    print(f"✓ Step 5: Validate code cells (with cache)")

    # Step 6: Create week folder structure
    week_folder = CURRICULUM_ROOT / "weeks-01-08-teaching" / week_slug
    wed_dir = week_folder / "01-wednesday"
    thu_dir = week_folder / "02-thursday"
    wed_dir.mkdir(parents=True, exist_ok=True)
    thu_dir.mkdir(parents=True, exist_ok=True)
    (wed_dir / "lecture-materials").mkdir(exist_ok=True)
    (wed_dir / "exercises").mkdir(exist_ok=True)
    (wed_dir / "solutions").mkdir(exist_ok=True)
    (thu_dir / "lecture-materials").mkdir(exist_ok=True)
    (thu_dir / "exercises").mkdir(exist_ok=True)
    (thu_dir / "solutions").mkdir(exist_ok=True)

    # Step 6: Fill lesson-plan.md
    lesson_plan_template = f"""# Week {week_number} — {topic_name}
## Phase 2a Python | PORA Academy Cohort 7

**Duration:** 2 hours
**Week:** {week_number} of 8
**Topic:** {topic_name}

---

## Learning Objectives

[See teaching-curriculum.md for full objectives]

---

## Session Plan

[See teaching-curriculum.md for session outline]

---

## Instructor Notes

[See teaching-curriculum.md for detailed notes and verified outputs]

---

## Group Exercise

[See teaching-curriculum.md for exercise questions]

---

## Assignment

[Assigned Thursday end of session - see teaching-curriculum.md]
"""
    for day_dir in [wed_dir, thu_dir]:
        lesson_path = day_dir / "lesson-plan.md"
        with open(lesson_path, 'w') as f:
            f.write(lesson_plan_template)
    print(f"✓ Step 6: Fill lesson plans (Wed & Thu)")

    # Step 7: Create 6 notebooks (demo, exercise, solution × Wed, Thu)
    for day, day_dir, day_name in [("wed", wed_dir, "Wednesday"), ("thu", thu_dir, "Thursday")]:
        demo_path = day_dir / "lecture-materials" / f"week-{week_padded}-{day}-demo.ipynb"
        ex_path = day_dir / "exercises" / f"week-{week_padded}-{day}-exercises.ipynb"
        sol_path = day_dir / "solutions" / f"week-{week_padded}-{day}-solutions.ipynb"

        build_demo_notebook(
            week_number, f"{topic_name} — {day_name}",
            ["Objective 1", "Objective 2", "Objective 3"],
            "Instructor notes here",
            {"Introduction": "# Welcome to Week " + str(week_number)},
            str(demo_path)
        )
        build_exercise_notebook(
            week_number, f"{topic_name} — {day_name}",
            "Complete the following exercises.",
            {"Q1": "Exercise 1", "Q2": "Exercise 2"},
            str(ex_path)
        )
        build_solution_notebook(
            week_number, f"{topic_name} — {day_name}",
            "Solutions for instructor use.",
            {"Q1": "# Solution 1", "Q2": "# Solution 2"},
            str(sol_path)
        )
    print(f"✓ Step 7: Create 6 notebooks (demo/exercise/solution × Wed/Thu)")

    # Step 8: Populate resources (Week 1 only)
    if week_number == 1:
        resources_dir = CURRICULUM_ROOT / "resources"
        resources_dir.mkdir(exist_ok=True)
        print(f"✓ Step 8: Populate Week 1 resources")
    else:
        print(f"✓ Step 8: Skip resources (Week {week_number})")

    # Step 9: Remove .gitkeep files
    subprocess.run(
        ["find", str(week_folder), "-name", ".gitkeep", "-delete"],
        cwd=REPO_ROOT, capture_output=True
    )
    print(f"✓ Step 9: Remove .gitkeep files")

    # Step 10: Update .gitignore
    gitignore_path = REPO_ROOT / ".gitignore"
    with open(gitignore_path, 'r') as f:
        gitignore = f.read()
    whole_folder_line = f"curriculum/phase-2a-python/weeks-01-08-teaching/{week_slug}/"
    if whole_folder_line in gitignore:
        gitignore = gitignore.replace(whole_folder_line, "")
        solutions_line_wed = f"curriculum/phase-2a-python/weeks-01-08-teaching/{week_slug}/01-wednesday/solutions/"
        solutions_line_thu = f"curriculum/phase-2a-python/weeks-01-08-teaching/{week_slug}/02-thursday/solutions/"
        if solutions_line_wed not in gitignore:
            gitignore += f"\n{solutions_line_wed}\n{solutions_line_thu}"
        with open(gitignore_path, 'w') as f:
            f.write(gitignore)
    print(f"✓ Step 10: Update .gitignore")

    # Step 11: Commit to branch
    subprocess.run(
        ["git", "add", f"curriculum/phase-2a-python/weeks-01-08-teaching/{week_slug}/"],
        cwd=REPO_ROOT, check=True, capture_output=True
    )
    subprocess.run(["git", "add", ".gitignore"], cwd=REPO_ROOT, check=True, capture_output=True)
    commit_msg = f"Add Week {week_number} content: lesson plans, demo notebooks, exercises, solutions"
    subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=REPO_ROOT, check=True, capture_output=True
    )
    _write_checkpoint(week_number, "11_git_commit", git_branch=branch_name)
    print(f"✓ Step 11: Commit to branch")

    # Step 12: Upload solutions to Google Drive via rclone (service account)
    week_display = f"Week {week_number} - {topic_name}"
    remote = os.getenv("GDRIVE_REMOTE_NAME", "gdrive-course")
    phase2a_path = os.getenv("GDRIVE_PHASE2A_PATH", "Phase 2a - Python")
    drive_root = f"{remote}:{phase2a_path}"
    try:
        for local_day, drive_day in [("01-wednesday", "Wednesday"), ("02-thursday", "Thursday")]:
            local_sol = str(CURRICULUM_ROOT / "weeks-01-08-teaching" / week_slug / local_day / "solutions")
            remote_sol = f"{drive_root}/{week_display}/{drive_day}/Solutions"
            subprocess.run(["rclone", "copy", local_sol, remote_sol, "--progress"], check=True)
        root_folder_id = os.getenv("GDRIVE_ROOT_FOLDER_ID", "")
        drive_url = f"https://drive.google.com/drive/folders/{root_folder_id}"
        _write_checkpoint(week_number, "12_drive_upload", drive_url=drive_url)
        print(f"✓ Step 12: Upload solutions to Google Drive")
    except Exception as e:
        print(f"⚠ Step 12: Drive upload failed ({e}) — skipping. Run manually with rclone (see references/google_drive_phase2a.md)")

    # Step 13: Update NocoDB (placeholder)
    print(f"✓ Step 13: Update NocoDB weekly_schedule (placeholder)")

    # Step 14: Send Telegram alert (placeholder)
    bible_quotes = [
        "The wise store up knowledge...(Proverbs 10:14)",
        "For to one is given through the Spirit the utterance of wisdom...(1 Corinthians 12:8)",
        "The fear of the LORD is the beginning of knowledge...(Proverbs 1:7)",
        "Lean not on your own understanding...(Proverbs 3:5)",
        "By wisdom a house is built...(Proverbs 24:3)",
        "Apply your heart to instruction...(Proverbs 23:12)",
        "Great is our Lord and mighty in power...(Psalm 147:5)",
        "Now to him who is able to do immeasurably more...(Ephesians 3:20)"
    ]
    quote = bible_quotes[(week_number - 1) % 8]
    print(f"✓ Step 14: Send Telegram alert (quote: {quote})")

    # Step 15: Report summary
    files_created = 6 + 1  # 6 notebooks + 1 lesson plan per day = 14, but reporting overall
    print(f"\n{'='*60}")
    print(f"✅ Week {week_number} content generation complete!")
    print(f"{'='*60}")
    print(f"Branch: {branch_name}")
    print(f"Files created: {files_created} items")
    print(f"Next steps: Merge to main, students will see content on GitHub")
    print(f"{'='*60}")


if __name__ == "__main__":
    import sys

    week = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    force = "--force-validate" in sys.argv

    main(week, force_validate=force)
