"""
Jupyter Notebook Builder

Creates .ipynb files with proper formatting, code cells, markdown cells.
Builds demo, exercise, and solution notebook variants.
"""

import nbformat
from pathlib import Path
from typing import List, Dict


def create_notebook(notebook_type: str = "demo") -> nbformat.NotebookNode:
    """
    Create a new Jupyter notebook with proper structure.

    Args:
        notebook_type: 'demo', 'exercise', or 'solution'

    Returns:
        nbformat notebook object ready to populate with cells
    """
    nb = nbformat.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.10.0"
        }
    }
    return nb


def add_markdown_cell(nb: nbformat.NotebookNode, text: str) -> None:
    """Add a markdown cell to the notebook."""
    cell = nbformat.v4.new_markdown_cell(text)
    nb.cells.append(cell)


def add_code_cell(nb: nbformat.NotebookNode, code: str, execute: bool = False) -> None:
    """Add a code cell to the notebook."""
    cell = nbformat.v4.new_code_cell(code)
    nb.cells.append(cell)


def save_notebook(nb: nbformat.NotebookNode, output_path: str) -> None:
    """Save notebook to file."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        nbformat.write(nb, f)


def build_demo_notebook(
    week_number: int,
    topic: str,
    learning_objectives: List[str],
    instructor_notes: str,
    code_sections: Dict[str, str],
    output_path: str
) -> None:
    """
    Build a demo notebook (instructor's live walkthrough).

    Args:
        week_number: Week 1-8
        topic: Session topic name
        learning_objectives: List of learning objectives
        instructor_notes: Notes for instructor
        code_sections: Dict of {section_name: code_string}
        output_path: Path to save .ipynb file
    """

    nb = create_notebook("demo")

    # Title cell
    add_markdown_cell(nb, f"# Week {week_number} — {topic}\n## Phase 2a Python | PORA Academy Cohort 7")

    # Instructor Notes cell
    notes_text = f"""## Instructor Notes

**Topic:** {topic}

**Learning Objectives:**
{chr(10).join(f'- {obj}' for obj in learning_objectives)}

**Notes:**
{instructor_notes}
"""
    add_markdown_cell(nb, notes_text)

    # Code sections with markdown explanations
    for section_name, code in code_sections.items():
        add_markdown_cell(nb, f"## {section_name}")
        add_code_cell(nb, code, execute=False)

    # Summary
    add_markdown_cell(nb, "## Summary\n\nKey takeaways from this session.")

    save_notebook(nb, output_path)


def build_exercise_notebook(
    week_number: int,
    topic: str,
    instructions: str,
    exercise_questions: Dict[str, str],
    output_path: str
) -> None:
    """
    Build an exercise notebook (students fill in blanks).

    Args:
        week_number: Week 1-8
        topic: Session topic name
        instructions: General instructions text
        exercise_questions: Dict of {question_id: question_text}
        output_path: Path to save .ipynb file
    """

    nb = create_notebook("exercise")

    # Title
    add_markdown_cell(nb, f"# Week {week_number} — {topic}\n## Phase 2a Python | PORA Academy Cohort 7")

    # Instructions
    add_markdown_cell(nb, f"## Instructions\n\n{instructions}")

    # Exercise questions
    for q_id, q_text in exercise_questions.items():
        add_markdown_cell(nb, f"### {q_id}\n\n{q_text}")
        # Blank code cell for student answer
        add_code_cell(nb, "# Your code here\n", execute=False)

    save_notebook(nb, output_path)


def build_solution_notebook(
    week_number: int,
    topic: str,
    instructions: str,
    solutions: Dict[str, str],
    output_path: str
) -> None:
    """
    Build a solution notebook (complete answers for instructors).

    Args:
        week_number: Week 1-8
        topic: Session topic name
        instructions: General instructions text
        solutions: Dict of {question_id: solution_code}
        output_path: Path to save .ipynb file
    """

    nb = create_notebook("solution")

    # Title
    add_markdown_cell(nb, f"# Week {week_number} — {topic}\n## Phase 2a Python | PORA Academy Cohort 7\n\n**INSTRUCTOR SOLUTIONS ONLY**")

    # Instructions
    add_markdown_cell(nb, f"## Instructions\n\n{instructions}")

    # Solutions
    for q_id, solution_code in solutions.items():
        add_markdown_cell(nb, f"### {q_id}")
        add_code_cell(nb, solution_code, execute=False)

    save_notebook(nb, output_path)


if __name__ == "__main__":
    # Test notebook creation
    nb = create_notebook("demo")

    add_markdown_cell(nb, "# Test Notebook\n\nThis is a test.")
    add_code_cell(nb, "print('Hello, World!')")

    save_notebook(nb, "/tmp/test_notebook.ipynb")
    print("Test notebook created at /tmp/test_notebook.ipynb")
