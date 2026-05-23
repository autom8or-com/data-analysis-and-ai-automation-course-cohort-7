# Week 2 — Collections & Control Flow
## Wednesday | Phase 2a Python | PORA Academy Cohort 7

### Wednesday: matplotlib & seaborn Basics

**Learning objectives:**
- Create bar charts, line charts, and histograms with matplotlib
- Format charts (title, labels, figsize, colours)
- Use seaborn for cleaner charts
- Save charts to file

> **Note:** Every chart built today will be embedded inside a Streamlit dashboard on Thursday. matplotlib figures are passed directly to `st.pyplot()` — so the skills are directly connected.

**Session outline (2 hours)**

**Part 1 — matplotlib Foundations (30 min)**

```python
import pandas as pd
import matplotlib.pyplot as plt

orders = pd.read_csv('olist_orders_dataset.csv')
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['month'] = orders['order_purchase_timestamp'].dt.to_period('M')

# Monthly orders 2017 (verified)
orders_2017 = orders[orders['order_purchase_timestamp'].dt.year == 2017]
monthly = orders_2017.groupby('month')['order_id'].count()

# Line chart
plt.figure(figsize=(12, 5))
plt.plot(monthly.index.astype(str), monthly.values, marker='o', linewidth=2, color='steelblue')
plt.title('Monthly Orders — Olist 2017', fontsize=14)
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# November 2017 spike to 7,544 should be visually prominent (Black Friday)

# Bar chart — order status
status = orders['order_status'].value_counts().head(5)
plt.figure(figsize=(8, 4))
plt.bar(status.index, status.values, color=['#2ecc71','#3498db','#e74c3c','#f39c12','#9b59b6'])
plt.title('Order Status Distribution')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
```

**Part 2 — seaborn (30 min)**

```python
import seaborn as sns

# Review score distribution
reviews = pd.read_csv('olist_order_reviews_dataset.csv')

plt.figure(figsize=(8, 4))
sns.countplot(data=reviews, x='review_score', palette='RdYlGn')
plt.title('Review Score Distribution — Olist')
plt.xlabel('Review Score')
plt.ylabel('Count')
plt.tight_layout()
plt.show()
# Expected visual: 5-star dominates (57,328), 1-star is second (11,424)

# Payment type pie chart
payments = pd.read_csv('olist_order_payments_dataset.csv')
pay_counts = payments['payment_type'].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(pay_counts.values, labels=pay_counts.index, autopct='%1.1f%%',
        colors=['#3498db','#e74c3c','#2ecc71','#f39c12','#9b59b6'])
plt.title('Payment Method Distribution')
plt.show()
# credit_card: 73.9%, boleto: 19.0%, voucher: 5.6%, debit_card: 1.5%
```

**Part 3 — Group Exercise (40 min)**

```python
# Each group builds 3 charts using verified data:

# Chart 1: Monthly order volume for 2017 (line chart)
# Peak should show: November 2017 = 7,544 orders

# Chart 2: Top 10 states by total orders (horizontal bar chart)
# SP should be far ahead at 41,746

# Chart 3: Review score distribution (bar chart)
# Scores 1-5, count for each
# Expected: [11424, 3151, 8179, 19142, 57328]
```

---


[Full curriculum in teaching-curriculum.md]
