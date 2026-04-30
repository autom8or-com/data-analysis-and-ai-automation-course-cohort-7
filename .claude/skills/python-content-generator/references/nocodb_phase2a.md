# NocoDB Configuration for Phase 2a Python

## Connection Details

- **Base URL**: `https://nocodb.aiautom8or.com`
- **API Token**: Stored in skill assets (loaded from file)
- **Auth Header**: `xc-token: {token}`

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

## Sheet Names Example

```json
{
  "week-NN-wed-demo.ipynb": ["Instructor Notes", "Raw Data", "Concept 1"],
  "week-NN-wed-exercises.ipynb": ["Instructions", "Setup", "Question 1"],
  "week-NN-wed-solutions.ipynb": ["Instructions", "Setup", "Question 1"]
}
```

## Special Flags

- **Week 4**: Set `deepseek_intro_week = true`
- **Week 8 Thursday**: Set `streamlit_week = true`
