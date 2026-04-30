# Jupyter Notebook Patterns & Templates

## Cell Structure

### Demo Notebook (`*-demo.ipynb`)
Instructor's walkthrough — all cells executed, all outputs visible.

**Typical cell sequence:**
1. **Title markdown** — Week N, topic, session heading
2. **Instructor Notes markdown** — Learning objectives, time budget, key messages
3. **Setup code** (Weeks 3+) — Import pandas, load Olist data
4. **Concept 1–N markdown** — Section headings explaining the concept
5. **Code cell per concept** — Working, executable code with verified output
6. **Summary markdown** — Key takeaways, next steps

### Exercise Notebook (`*-exercises.ipynb`)
Student worksheet — has questions, blank code cells.

**Typical structure:**
1. **Title markdown**
2. **Instructions markdown**
3. **Raw Data markdown**
4. **Setup code** (executed)
5. **Question 1–N markdown** — Question text, desired output hint
6. **Blank code cells** — `# Your code here\n` as placeholder

### Solution Notebook (`*-solutions.ipynb`)
Instructor's answer key — same structure as exercises, but with complete code.

## Code Cell Patterns

### Data Loading (Week 3+)
```python
import pandas as pd
orders = pd.read_csv("/content/drive/MyDrive/olist-data/olist_orders_dataset.csv")
print(f"Loaded {len(orders):,} orders")
orders.head()
```

### Exploration Pattern
```python
print(f"Shape: {orders.shape}")
print(f"Columns: {orders.columns.tolist()}")
orders.head()
```

### Aggregation Pattern (Week 5+)
```python
status_counts = orders['order_status'].value_counts()
print(status_counts)
```

### Merge Pattern (Week 7)
```python
orders_with_customers = orders.merge(customers, on='customer_id', how='left')
print(f"Merged shape: {orders_with_customers.shape}")
```

### Streamlit Pattern (Week 8 Thursday)
```python
import streamlit as st
st.title("Olist Order Analysis")
orders = pd.read_csv("olist_orders_dataset.csv")
st.write(f"Total orders: {len(orders):,}")
st.bar_chart(orders['order_status'].value_counts())
```

## Execution Notes

- **Demo notebook**: All cells execute and produce output
- **Exercise notebook**: Setup cells execute; student cells are blank
- **Solution notebook**: All cells execute (used for instructor verification)
- **No saved outputs**: .ipynb files generated with `execution_count = None` and empty `outputs` arrays
