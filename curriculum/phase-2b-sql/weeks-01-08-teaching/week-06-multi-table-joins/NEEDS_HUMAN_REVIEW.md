# Week 6 — Needs Human Review

## `01-wednesday/lecture-materials/week-06-wed-demo.ipynb`

**Status:** Failed automated validation after 2 attempts (structural fan-out lint), all other checks pass.

**What's failing:** Cell 10 — the curriculum's verbatim documented query for the Wednesday
business question "Does price differ by review score?":

```sql
SELECT r.review_score,
       COUNT(DISTINCT oi.order_id) AS order_count,
       ROUND(AVG(oi.price), 2)     AS avg_item_price,
       ROUND(SUM(oi.price), 2)     AS total_revenue
FROM order_items oi
JOIN order_reviews r ON oi.order_id = r.order_id
GROUP BY r.review_score
ORDER BY r.review_score
```

`validate_sql_notebook_cli.py`'s static `fanout_check` flags any single `%%sql` cell that
joins 2+ of `order_items` / `order_payments` / `order_reviews` and then uses an unsafe
aggregate (`SUM`, `AVG`, or non-`DISTINCT COUNT`). This query does exactly that — it joins
`order_items` directly to `order_reviews` (both fan-out tables) and aggregates with
`AVG`/`SUM`.

**Why it wasn't reworked away:** This is not a generation bug. It is the exact query and
exact numbers documented in `teaching-curriculum.md` (lines ~1065–1087), reproduced
verbatim per repo convention that verified curriculum values must never be altered or
recomputed. The notebook already teaches the fan-out caveat explicitly in the "Going
deeper" section (cell 14) immediately following this query, including a callout that the
547 twice-reviewed orders get counted under both scores and that `total_revenue` per score
is therefore slightly inflated for those orders — this is a deliberate real-world data
teaching moment, not an oversight.

Collapsing `order_reviews` into a `WITH` CTE first (the lint's suggested fix) would change
`total_revenue`/`avg_item_price` away from the curriculum's documented and verified values
(1,812,828.22 / 127.35 for score 1 ... 7,700,489.39 / 121.22 for score 5), which would
violate the "never invent/alter verified expected output" rule in `CLAUDE.md`.

**What was fixed during rework (attempt 2):**
- Added an explicit "Group Exercise" subsection (was missing — `has_group_exercise` now passes).
- Split the grain-check cell (old cell 15, a `UNION ALL` across all 4 fact tables) into 4
  separate per-table `%%sql` cells, since the lint's static regex couldn't distinguish
  `UNION ALL` of independent counts from an actual join. Same numbers, no join fan-out.
- Fixed a `ModuleNotFoundError: pandas` in the validation environment (missing package, now
  installed) that caused a false `execution_failed` on attempt 1.

**Recommended resolution:** A human reviewer should either (a) accept this as an intentional
exception and hand-waive the lint for this cell (e.g. add a lint-allowlist comment convention
to `validate_sql_notebook_cli.py`, or manually mark this notebook reviewed/approved), or
(b) decide the curriculum text itself should be revised to use the fan-out-safe CTE pattern
going forward, in which case the documented "Expected" numbers in `teaching-curriculum.md`
would need to be re-verified and updated first — do not change them here without that
re-verification.

All other Week 6 notebooks were generated and validated independently of this issue.
