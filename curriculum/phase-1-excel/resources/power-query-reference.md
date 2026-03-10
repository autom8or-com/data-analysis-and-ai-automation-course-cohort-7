# Power Query Reference
## Phase 1 — PORA Academy Cohort 7

> To be completed. Reference: teaching-curriculum.md Weeks 5–6 for all verified M formulas.

## Common Steps

| Step | UI Location | M Formula |
|---|---|---|
| Load CSV | Data → Get Data → From Text/CSV | |
| Change data type | Transform → Data Type | `Table.TransformColumnTypes` |
| Filter rows | Home → Remove Rows | `Table.SelectRows` |
| Add custom column | Add Column → Custom Column | `Table.AddColumn` |
| Remove columns | Home → Remove Columns | `Table.RemoveColumns` |

## Custom Column Formulas (Verified)

| Column | M Formula | Verified Output |
|---|---|---|
| `Revenue` | `= [Quantity] * [UnitPrice]` | Total: £9,747,747.93 (raw) |
| `Month` | `= Date.Month([InvoiceDate])` | 1–12 |
| `Year` | `= Date.Year([InvoiceDate])` | 2010–2011 |
| `UKorInternational` | `= if [Country] = "United Kingdom" then "UK" else "International"` | |
