---
name: sql-notebook-generate
description: >
  Generate one Jupyter notebook (demo, exercises, or solutions) for one day of a
  Phase 2b SQL week, using Claude Opus 4.8 to EXPAND the curriculum skeleton into a
  fully realized pedagogical experience. SQL is taught with the `%%sql` cell magic
  (jupysql) against a file-based SQLite Olist database — NOT `pd.read_sql`. Enforces
  the mandatory demo section structure and the three-cell self-checking exercise
  pattern. All expected values come from the verified curriculum. Used internally by
  /sql-content-generator. Can be called standalone to regenerate a single notebook
  with optional rework notes.
---

# SQL Notebook Generator

Generates one `.ipynb` file by expanding the Week's curriculum section into a complete SQL teaching experience. Invoked as a Claude Opus 4.8 sub-agent by the orchestrator (`/sql-content-generator`).

This skill is the SQL sibling of `python-notebook-generate`. The teaching philosophy, PRIME DIRECTIVE style, and cell-quality discipline are identical; the query surface is different — **every query is a `%%sql` cell magic, never `pd.read_sql`.**

---

## Inputs

- **Week number** (1–8)
- **Day**: `wed` or `thu`
- **Notebook type**: `demo`, `exercises`, or `solutions`
- **Curriculum**: `curriculum/phase-2b-sql/teaching-curriculum.md` (authoritative — read the target Week's section)
- **Schema + verified stats**: `.claude/skills/sql-content-generator/references/olist_schema.md`
- **Setup cell**: `.claude/skills/sql-content-generator/assets/sql_setup.py`
- **Rework notes** (optional): specific improvements to make if regenerating

## Output

One `.ipynb` at the standard path:

```
curriculum/phase-2b-sql/weeks-01-08-teaching/<week-slug>/<day-folder>/
  lecture-materials/week-NN-<day>-demo.ipynb        (demo)
  exercises/week-NN-<day>-exercises.ipynb            (exercises)
  solutions/week-NN-<day>-solutions.ipynb            (solutions)
```

Day folder: `01-wednesday` or `02-thursday`. Filenames: `week-NN-{wed,thu}-{demo,exercises,solutions}.ipynb`.

---

## PRIME DIRECTIVE

**The curriculum section is a SKELETON. EXPAND it. NEVER copy heading text or bullet points verbatim as cell content. Every markdown cell must be a complete, human explanation. Every `%%sql` cell must be an executable query that produces a specific, verifiable result.**

**Expected values are SACRED. Every `-- Expected:` comment and every `assert` seed value must come verbatim from `teaching-curriculum.md` or `olist_schema.md`. NEVER invent a count, sum, average, or KPI. If the curriculum does not state a value for a query you want to write, either pick a query whose value IS verified, or write a demo-only query with no numeric claim.**

When given rework notes, treat them as the primary improvement specification. Apply them precisely — do not regenerate from scratch.

---

## The setup cell (EVERY notebook, all weeks)

The **first code cell of every notebook** — demo, exercises, and solutions alike — is the verbatim contents of `.claude/skills/sql-content-generator/assets/sql_setup.py`. Read that file and paste its contents as the cell source. Do not paraphrase, trim, or "improve" it. It:

- mounts Drive and loads the 8 Olist CSVs into a **file-based** SQLite DB at `/content/olist.db`;
- runs `%load_ext sql`, sets `%config SqlMagic.autopandas = True`, and connects jupysql via `%sql sqlite:////content/olist.db`.

Because `autopandas = True`, **every `%%sql` result is a pandas DataFrame** — which is what makes the self-check cells able to `assert` on `.iloc` / `.shape` directly.

The markdown title cell precedes the setup cell in every notebook (title first, then setup).

---

## Query style — `%%sql`, never pandas

All SQL runs through the jupysql cell magic:

- **Plain query** (demo, and any display query):
  ```sql
  %%sql
  SELECT order_status, COUNT(*) AS n
  FROM orders
  GROUP BY order_status
  ```
- **Captured query** (used by the self-check pattern) — assign the DataFrame to a name with `<<`:
  ```sql
  %%sql q1 <<
  SELECT COUNT(*) AS n FROM orders WHERE order_status = 'delivered'
  ```
  After this cell, `q1` is a pandas DataFrame; `int(q1.iloc[0]['n'])` is the scalar.

Never write `pd.read_sql(...)`, `conn.execute(...)`, or `sqlite3` cursor code in a teaching cell. Students meet raw SQL first; the Python wrapper is Phase 2c.

Respect the SQLite gotchas in `olist_schema.md`: dates are TEXT (use `strftime`), force REAL division with `* 1.0`, use `IS NULL` / `IS NOT NULL` (never `= NULL`), `!=` and `<>` both work, no `FULL OUTER JOIN`.

---

## MANDATORY SECTION STRUCTURE — Demo notebooks

Every demo notebook MUST contain all 8 sections in this order. Missing any section is a validation failure. (Adapted from the Phase 2a 8-section structure for SQL.)

### §1 — Title + Learning Objectives (1 markdown cell)

```markdown
# Week N — [Topic]: [Session Subtitle]
## Phase 2b SQL | PORA Academy Cohort 7

By the end of this session, you will be able to:
- [Objective 1 from the curriculum's Objective line]
- [Objective 2 …]
- [Objective 3 …]
```

Objectives come from the Week's `**Objective:**` line — do not invent new ones.

### §2 — Setup (1 code cell)

The verbatim `sql_setup.py` contents (see "The setup cell" above). One short markdown line may introduce it.

### §3 — Business Context Hook (1 markdown cell)

Open with the Olist scenario that makes the concept tangible, using a verified stat:

> "The `orders` table holds 99,441 orders, but only 96,478 are actually delivered. To answer a business question like *how many orders never reached the customer*, we need `WHERE` to filter rows."

Minimum 2–3 sentences. Establish *why* before any SQL.

### §4 — Concept Introduction + Live Query (1 markdown + 1 `%%sql` code cell per concept)

For each concept in the Week's day section (e.g. Wednesday: SELECT, WHERE, AND/OR, ORDER BY + LIMIT):

- **Markdown cell**: plain-English explanation — what the clause does (not just its name), an everyday analogy, minimum 3 full sentences.
- **`%%sql` code cell**: a real query on real tables. Where the curriculum gives a verified count, add `-- Expected: <value>` as a SQL comment on the relevant line. Display queries (e.g. `SELECT ... LIMIT 10`) need no numeric claim.

### §5 — Going Deeper (1 markdown + 1 `%%sql` cell)

One extension beyond the core: a NULL gotcha (`IS NULL` vs `= NULL`), integer-division truncation and the `* 1.0` fix, `strftime` on TEXT dates, or `!=` excluding NULLs. Runnable; markdown explains why it matters.

### §6 — Common Mistakes (1 markdown + 1 `%%sql` cell)

Show the exact mistake a beginner makes, then the fix. Put the WRONG version in a SQL comment (never run crashing/misleading SQL), then the CORRECT query live:

```sql
%%sql
-- ── COMMON MISTAKE ──────────────────────────────────
-- WRONG — matches ZERO rows, NULL is never '= NULL':
--   SELECT COUNT(*) FROM orders WHERE order_delivered_customer_date = NULL
-- CORRECT — use IS NULL:
SELECT COUNT(*) AS n
FROM orders
WHERE order_delivered_customer_date IS NULL   -- Expected: 2,965
```

### §7 — Mini-Challenge (1 markdown + 1 `%%sql` scaffold cell)

A 5–10 minute individual task solvable with only today's clauses. Markdown states the task and the expected result; the code cell is a `%%sql` scaffold with `-- Your query here`. Include `⏱ ~5 minutes`.

### §8 — Summary + Preview (1 markdown cell)

```markdown
## Session Summary

| Clause | What it does | Example |
|---|---|---|
| `SELECT` | choose columns | `SELECT order_id FROM orders` |
| `WHERE`  | filter rows | `WHERE order_status = 'delivered'` |

---
**Coming up [Wednesday/Thursday]**: [next session topic from the curriculum]
```

---

## Exercises notebook structure

The core deliverable of this skill is the **three-cell self-checking exercise pattern**. An exercises notebook is:

1. **Title + Instructions** (1 markdown cell): title, "Fill in each `%%sql` cell, then run the check cell below it — a ✅ means your query is correct. Do not edit the check cells."
2. **Setup** (1 code cell): verbatim `sql_setup.py`.
3. **Questions** (3 cells each — see below), 3–5 per notebook.
4. NEVER pre-fill an answer. NEVER add a solutions section.

### The three-cell self-check pattern (per question)

**(a) Markdown cell** — question statement + expected hint:
```markdown
## Question N — [short title]

[The task in plain English.]

**Expected:** [verified value, e.g. 96,478 delivered orders]
```

**(b) Answer code cell** — a blank `%%sql` capture scaffold, EXACTLY:
```sql
%%sql qN <<
-- Your query here
```
(In an **exercises** notebook this stays blank. In a **solutions** notebook it is filled with the real `SELECT`.)

**(c) Check code cell** — plain Python, marked do-not-edit, asserting on the captured DataFrame with the verified value, then a ✅ print:
```python
# --- CHECK QN — do not edit ---
assert int(qN.iloc[0]['n']) == 96478, "QN: expected 96,478 delivered orders"
print("✅ QN correct")
```

Because `autopandas = True`, `qN` is a pandas DataFrame. Seed every assertion from a value that appears verbatim in `teaching-curriculum.md` or `olist_schema.md`. Match the column alias used in the answer query (`AS n` → `qN.iloc[0]['n']`). For non-count checks use `.shape` (row count of a `LIMIT`/list query), `.iloc[0][col]`, or `round(float(...), 2)` for money/averages.

The check cell must be **correct and runnable** — it should pass the moment a correct query is filled into cell (b).

---

## Solutions notebook structure

Mirror the exercises notebook **exactly** (same questions, same check cells), but:

- First cell adds: `> ⚠️ **INSTRUCTOR USE ONLY** — Do not share with students`.
- Every blank `%%sql qN <<` / `-- Your query here` is replaced with the complete, correct `SELECT` (still capturing to `qN`).
- Keep every check cell verbatim — running the solution notebook top-to-bottom should print all ✅.
- Same question count and same check values as the exercises notebook.

---

## Demo vs exercises vs solutions — quick contrast

| | Query cells | Numeric claim | Checks |
|---|---|---|---|
| **demo** | plain `%%sql`, no blanks | `-- Expected: <value>` comment | none |
| **exercises** | `%%sql qN <<` + `-- Your query here` (blank) | `**Expected:**` in markdown | check cell kept, seeded |
| **solutions** | `%%sql qN <<` filled with real SELECT | `**Expected:**` in markdown | check cell kept, seeded |

---

## AI assistance (Weeks 4–8 only)

Weeks 1–3 are **no-AI**. From Week 4, after §4 in demo notebooks add a "Using DeepSeek" section covering the prompt-then-verify protocol: ask DeepSeek to draft SQL, run it, and confirm the result against the verified expected value before trusting it. Never let AI-drafted SQL bypass the self-check. Do not add any AI section to Weeks 1–3.

---

## Code / query quality rules (absolute — violation fails validation)

1. **`%%sql` only** — no `pd.read_sql`, no `sqlite3` cursors in teaching cells.
2. **Verified values only** — every `-- Expected:` and every `assert` seed is verbatim from the curriculum / schema.
3. **No crashing cells** — show wrong SQL as a comment; only correct SQL runs.
4. **NULL discipline** — `IS NULL` / `IS NOT NULL`, never `= NULL`.
5. **REAL division** — force with `* 1.0` when a percentage/ratio is computed.
6. **TEXT dates** — use `strftime(...)`, never date-typed operations.
7. **Alias match** — check cells reference the exact column alias the answer query produces.
8. **Setup first** — the `sql_setup.py` cell is the first code cell of every notebook.
9. **No saved outputs** — `outputs: []` and `execution_count: null` on every cell.

---

## Cell count targets

- **Demo notebooks**: 18–28 cells (title + setup + 8 sections, some concepts multi-cell).
- **Exercises notebooks**: title + setup + (3 cells × 3–5 questions) = **11–17 cells**.
- **Solutions notebooks**: same count as the matching exercises notebook.

Fewer = too sparse; more = over-engineered. Aim for the middle.

---

## nbformat build guidance

Build the notebook as nbformat v4 and write with `nbformat.write` (or hand-assemble the JSON and `json.dump`). Either is acceptable; the result must be valid nbformat v4.

```python
import nbformat

nb = nbformat.v4.new_notebook()
nb.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.10.0"},
}

nb.cells.append(nbformat.v4.new_markdown_cell("# Week 1 — SELECT, WHERE, ORDER BY, LIMIT\n..."))
nb.cells.append(nbformat.v4.new_code_cell(SQL_SETUP_CONTENTS))     # verbatim sql_setup.py
nb.cells.append(nbformat.v4.new_markdown_cell("## Question 1 — ...\n\n**Expected:** 96,478 ..."))
nb.cells.append(nbformat.v4.new_code_cell("%%sql q1 <<\n-- Your query here"))
nb.cells.append(nbformat.v4.new_code_cell(
    "# --- CHECK Q1 — do not edit ---\n"
    "assert int(q1.iloc[0]['n']) == 96478, \"Q1: expected 96,478 delivered orders\"\n"
    "print(\"✅ Q1 correct\")"
))

for c in nb.cells:                      # never save pre-run outputs
    if c.cell_type == "code":
        c.execution_count = None
        c.outputs = []

with open(output_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)
```

A worked reference notebook demonstrating the full three-cell self-check pattern lives at
`.claude/skills/sql-notebook-generate/examples/week-01-wed-exercises.ipynb`. Read it before generating your first exercises notebook.
