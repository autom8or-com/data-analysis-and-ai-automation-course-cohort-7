# NocoDB Configuration for Phase 2a Python

## Connection Details

| Item | Value |
|---|---|
| **Base URL** | `https://nocodb.aiautom8or.com` |
| **API Token** | `NOCODB_API_TOKEN` in `.env` = `LnUQEyAyOs_v5EWDxqPGC19du1OjNHqWqpa4h63An` |
| **Auth Header** | `xc-token: {token}` |
| **Table** | `phase2a_schedule` (v2 API) or `weekly_schedule` (fallback) |
| **API Endpoint** | `POST /api/v2/db/data/noco/pora-academy/phase2a_schedule` |

## When NocoDB Is Updated

**NocoDB is updated AFTER PR merge, NOT during pipeline generation.**

The update fires from GitHub Actions workflow `.github/workflows/pr-notify.yml` under the "PR Merged → Update NocoDB" step.

This means:
- Content is generated → PR is created → you review → **you merge** → NocoDB gets `status: "published"`
- The schedule is never marked "published" for unapproved content
- The `NOCODB_API_TOKEN` must be added as a GitHub Actions secret (already done)

## weekly_schedule Table

### Column Schema

| Column | Type | Notes |
|---|---|---|
| `week_number` | Number | 1–8 |
| `phase` | Single Select | `phase-2a-python` |
| `topic_name` | Short Text | "Python Fundamentals", etc |
| `wed_lesson_plan_url` | URL | GitHub raw markdown link |
| `thu_lesson_plan_url` | URL | GitHub raw markdown link |
| `wed_sheet_names` | Long Text | JSON string of notebook sheets |
| `thu_sheet_names` | Long Text | JSON string of notebook sheets |
| `deepseek_intro_week` | Checkbox | True for Week 4 only |
| `streamlit_week` | Checkbox | True for Week 8 Thursday only |
| `status` | Single Select | `published`, `draft`, `archived` |

## URL Pattern for Lesson Plans

```
https://raw.githubusercontent.com/autom8or-com/data-analysis-and-ai-automation-course-cohort-7/main/curriculum/phase-2a-python/weeks-01-08-teaching/week-NN-slug/01-wednesday/lesson-plan.md
```

## GitHub Actions Step (pr-notify.yml)

The merge event step in `.github/workflows/pr-notify.yml`:

```yaml
- name: PR Merged → Update NocoDB
  if: github.event_name == 'pull_request' && github.event.action == 'closed' && github.event.pull_request.merged == true
  env:
    NOCODB_TOKEN: ${{ secrets.NOCODB_API_TOKEN }}
  run: |
    # Extracts week number and topic from PR title
    # Posts to NocoDB API with status: "published"
```

## Special Flags

- **Week 4**: Set `deepseek_intro_week = true`
- **Week 8 Thursday**: Set `streamlit_week = true`
