# Phase 2a Python Curriculum Structure

## Overview
8 weeks of Python instruction with Google Colab, Olist dataset (99,441 orders).
- **Weeks 1–3**: Core Python (no AI)
- **Weeks 4–8**: Pandas + DeepSeek integration

## Week Mapping

| Week | Folder Slug | Topic | Key Skills |
|---|---|---|---|
| 1 | `week-01-python-fundamentals` | Variables, types, strings | print(), f-strings, type conversion |
| 2 | `week-02-collections-and-control-flow` | Lists, dicts, if/for/while | Iteration, conditionals, indexing |
| 3 | `week-03-functions-and-data` | Functions, imports, CSV intro | def, parameters, pandas.read_csv() |
| 4 | `week-04-pandas-introduction` | DataFrames, loading data | df.head(), df.info(), df.describe(), DeepSeek intro |
| 5 | `week-05-groupby-and-aggregation` | groupby(), aggregation | .sum(), .mean(), .count(), .agg() |
| 6 | `week-06-data-cleaning` | Missing values, duplicates, types | .dropna(), .fillna(), .astype() |
| 7 | `week-07-merging-dataframes` | join, merge, concat | .merge(), .join(), .concat() |
| 8 | `week-08-visualisation-and-streamlit` | Plotting, Streamlit | matplotlib, seaborn, streamlit basics |

## Session Folder Convention

```
curriculum/phase-2a-python/
├── teaching-curriculum.md          (all-weeks reference, instructor-only)
└── weeks-01-08-teaching/
    └── week-NN-slug/
        ├── 01-wednesday/
        │   ├── lesson-plan.md
        │   ├── lecture-materials/
        │   │   └── week-NN-wed-demo.ipynb
        │   ├── exercises/
        │   │   └── week-NN-wed-exercises.ipynb
        │   └── solutions/
        │       └── week-NN-wed-solutions.ipynb
        └── 02-thursday/
            └── (same structure)
```

## Dataset Reference
- **Zip path**: `datasets/phase-2-python-sql/olist-data.zip`
- **Total rows**: 99,441 orders (11 CSVs)
- **Mount path in Colab**: Students receive gauth mount code in shared Drive

## Key Verified Stats (from teaching-curriculum)
- Total orders: 99,441
- SP state orders: 41,746
- Unique sellers: 3,095
- Products with null category: ~200
- Average order value: ~154 BRL
