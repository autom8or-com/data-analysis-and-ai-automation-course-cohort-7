---
name: python-notebook-generate
description: >
  Generate one Jupyter notebook (demo, exercise, or solution) for one day of a
  Phase 2a Python week, using Claude Opus 4.8 to EXPAND the curriculum skeleton
  into a fully realized pedagogical experience. Enforces the mandatory 8-section
  teaching structure. All code uses real Olist values from the context bundle.
  Invoked directly by /python-content-generator (no sub-agent spawning).
  Can also be called standalone to regenerate a single notebook with optional rework notes.
---

# Python Notebook Generator

Generates one `.ipynb` file by expanding the curriculum context into a complete teaching experience. Invoked directly by the orchestrator as a skill.

---

## Inputs

- **Week number** (1–8)
- **Day**: `wed` or `thu`
- **Notebook type**: `demo`, `exercises`, or `solutions`
- **Context bundle path**: `.pipeline-cache/week-NN-context.json`
- **Rework notes** (optional): string of specific improvements to make if regenerating

## Output

One `.ipynb` file at the standard path:

```
curriculum/phase-2a-python/weeks-01-08-teaching/<week-slug>/<day-folder>/
  lecture-materials/week-NN-<day>-demo.ipynb         (demo)
  exercises/week-NN-<day>-exercises.ipynb             (exercises)
  solutions/week-NN-<day>-solutions.ipynb             (solutions)
```

Day folder: `01-wednesday` or `02-thursday`

---

## Workflow

### Step 1 — Read the context bundle

Read `.pipeline-cache/week-NN-context.json`. Extract the relevant day's section (`wednesday` or `thursday`). This is your complete specification — do not read `teaching-curriculum.md` directly.

If rework notes are provided, read them carefully before generating. They are the primary specification for what to change.

### Step 2 — Generate the notebook

Use your full intelligence as Claude Opus 4.8 to generate the notebook. Follow all rules in the PRIME DIRECTIVE and notebook structure specifications below.

Build the notebook as a Python dict matching nbformat v4 structure, then write it using:

```python
import json, nbformat

nb = nbformat.read_current_path_or_build_from_scratch()
# ... build cells ...
with open(output_path, 'w') as f:
    nbformat.write(nb, f)
```

Or directly build the JSON structure and write with `json.dump()`. Either approach is acceptable.

### Step 3 — Write the file

Write the `.ipynb` to the correct path. Create parent directories if they don't exist.

Print confirmation:
```
✅ Generated: curriculum/.../week-NN-<day>-<type>.ipynb
   Cells: N (M markdown, K code)
   Sections: [list of 8 section names present]
```

---

## PRIME DIRECTIVE

**The context bundle is a SKELETON. EXPAND it. NEVER copy heading text or bullet points verbatim as cell content. Every markdown cell must be a complete, human explanation. Every code cell must be executable Python that produces a specific, expected output.**

When given rework notes, treat them as the primary improvement specification. Apply them precisely — do not regenerate from scratch, just improve what the notes identify.

---

## MANDATORY 8-SECTION STRUCTURE (Demo Notebooks)

Every demo notebook MUST contain all 8 sections in this order. Missing any section is a validation failure.

### §1 — Title + Learning Objectives (1 markdown cell)

```markdown
# Week N — [Topic Name]: [Session Subtitle]
## Phase 2a Python | PORA Academy Cohort 7

By the end of this session, you will be able to:
- [Objective 1 verbatim from context bundle]
- [Objective 2 verbatim from context bundle]
- [Objective 3 verbatim from context bundle]
```

Use objectives verbatim from the context bundle. Do not paraphrase or invent new objectives.

### §2 — Business Context Hook (1 markdown cell)

Open with the Olist business scenario that makes the concept tangible. Use the pattern:

> "In the Olist dataset, [real-world scenario using verified_stats values]. To [analyse/answer/solve] this, we need [today's concept]."

Minimum 2–3 sentences. Students must understand why this concept matters before seeing any code.

### §3 — Concept Introduction + Live Code (1 markdown + 1 code cell per concept)

For each concept in `context_bundle.wednesday.concepts` (or `.thursday.concepts`):

**Markdown cell**: Plain-English explanation. Must include:
- What the concept is (not just its syntax name)
- An analogy to something non-technical (everyday life, cooking, etc.)
- Minimum 3 full sentences — no bullet lists here

**Code cell**: Executable Python using real Olist values from `verified_stats`. Rules:
- Every `print()` statement includes `# expected: <value from verified_stats>` as a comment
- Variable names match what `data_loading.py` produces (e.g., `orders_df`, `customers_df`)
- Weeks 1–2: use hardcoded Olist variables (see Data Loading Rules below)
- Weeks 3+: data is already loaded via the setup cell

### §4 — Going Deeper (1 markdown + 1 code cell)

One extension beyond the core concept:
- An edge case (e.g., `None` values in cancelled orders, negative indexing, chained string methods)
- A gotcha that trips up beginners
- A more powerful version of the concept

Must be runnable code. The markdown explains why this matters.

### §5 — Common Mistakes (1 markdown + 1 code cell)

Show the exact error a student will make, then the correction. Required format:

```python
# ── COMMON MISTAKE ───────────────────────────────────────────
# WRONG — this raises TypeError:
# print("Total: " + 72.19)   # TypeError: can only concatenate str (not "float") to str

# CORRECT — convert to string first:
print("Total: " + str(72.19))   # Total: 72.19

# EVEN BETTER — use an f-string (reads like the result):
print(f"Total: {72.19}")        # Total: 72.19
```

Never write actually-crashing code. Show errors as comments only.

### §6 — Mini-Challenge (1 markdown + 1 scaffolded code cell)

A 5–10 minute individual exercise. Rules:
- Markdown: state the task clearly + show expected output
- Code cell: provide all necessary variables (pre-defined, do not change), then `# Your code here` for each blank
- Must be solvable using only concepts taught so far in this session
- Include a time hint: `⏱ ~5 minutes`

### §7 — Group Exercise (1 markdown + 1 scaffolded code cell)

Pull the group exercise verbatim from `context_bundle.wednesday.group_exercise` (or `.thursday`). Rules:
- Markdown: scenario text + numbered tasks, exactly as in the curriculum
- Code cell: all input variables pre-defined (do not change values), blank lines for each task
- This is the main 30-minute collaborative activity

### §8 — Summary + Preview (1 markdown cell)

Required format:

```markdown
## Session Summary

| Concept | Key Syntax | Example |
|---|---|---|
| [Concept 1] | `[syntax]` | `[one-liner]` |
| [Concept 2] | `[syntax]` | `[one-liner]` |

---
**Coming up [Wednesday/Thursday]**: [Next session topic from context bundle]
```

---

## Exercise Notebook Structure (5 parts)

1. **Title + Instructions** (1 markdown): title, "Read each question carefully", expected output format
2. **Data Setup** (1 code cell, Weeks 3+): `data_loading.py` snippet or hardcoded variables (Weeks 1–2)
3. **Questions** (1 markdown + 1 blank code cell per question):
   - Markdown: question number + text + expected output hint
   - Code cell: given variables if needed, then `# Your code here`
   - Include group exercise from context bundle as final set of questions
4. **Assignment** (Thursday only, 1 markdown): `context_bundle.assignment_text` verbatim
5. NEVER pre-fill any answer. NEVER add a solutions section.

---

## Solution Notebook Structure

Mirror the exercise notebook exactly, but:
- First cell adds: `> ⚠️ **INSTRUCTOR USE ONLY** — Do not share with students`
- Every `# Your code here` blank is replaced with complete, working code
- Add `# Q1: [question summary]` above each solution block
- Add `# → [expected output]` after the last line of each answer
- No saved notebook outputs (keep `outputs: []` in all cells, `execution_count: null`)

---

## Data Loading Rules

**Weeks 1–2** (no pandas, no Drive mounting):
```python
# Real Olist values — no data loading needed this week
order_id = "e481f51cbdc54678b7cc49136f2d6af7"
item_price = 58.90
freight_value = 13.29
seller_city = "sao paulo"
product_category = "housewares"
order_status = "delivered"
total_orders = 99441
sp_state_orders = 41746
```

**Weeks 3+**: The first code cell is the standard data loading setup from `context_bundle.colab_data_loading_code`. Do not invent alternative loading methods.

**Week 4+**: After §3, add a "Using AI Assistance" section before §4. Include the DeepSeek protocol (4 rules). Read from `.claude/skills/python-content-generator/assets/deepseek_integration.md` for the exact protocol text.

**Week 8 Thursday**: Use Streamlit in §3 code cells. Read `.claude/skills/python-content-generator/assets/streamlit_example.py` for the complete example app.

---

## Code Quality Rules

These rules are absolute — violating any of them will cause validation failure:

1. **No combined statements**: `print('a')print('b')` is forbidden. Each statement on its own line.
2. **No undefined variables**: every variable must be assigned before use. If a setup cell defines `orders_df`, all subsequent code cells can reference it. If a concept section introduces a new variable, define it first.
3. **No missing sections**: all 8 sections must be present in demos, all 5 parts in exercises.
4. **Expected output comments**: every `print()` in a demo must have `# expected: <value>` where value comes from `verified_stats`.
5. **Realistic values**: all numeric examples must use values from `verified_stats` or be clearly labeled as invented examples (only when no real value is available).
6. **Try/except for deliberate errors**: if showing what an error looks like, wrap it in `try/except` or comment it out — never let a code cell crash the notebook.

---

## Cell Count Targets

- **Demo notebooks**: 20–30 cells (markdown + code combined)
- **Exercise notebooks**: 14–22 cells
- **Solution notebooks**: 14–22 cells (same count as exercises)

Fewer cells = content is too sparse. More cells = content is over-engineered. Aim for the middle.

---

## nbformat Structure

Build notebooks with this exact structure:

```python
import nbformat

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

# Add cells:
nb.cells.append(nbformat.v4.new_markdown_cell("## Title\n..."))
nb.cells.append(nbformat.v4.new_code_cell("print('hello')  # expected: hello"))

with open(output_path, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
```

Keep `outputs: []` and `execution_count: null` on all cells — never save pre-run outputs.
