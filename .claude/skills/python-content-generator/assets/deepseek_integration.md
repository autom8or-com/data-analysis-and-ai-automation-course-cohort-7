# DeepSeek Integration Guide (Weeks 4–8)

## Protocol: How Students Use DeepSeek

From Week 4, students use DeepSeek to help write and debug code. The protocol:

1. **Understand first**: Before prompting, students must describe in plain English what they want to achieve
2. **Prompt with context**: Provide DataFrame name, relevant column names, and the specific question
3. **Validate the output**: Every output from DeepSeek must be verified against expected values
4. **Never copy blindly**: Students must be able to explain every line of generated code

---

## Sample Prompt Template (Teach Students This)

```
I have a pandas DataFrame called `orders` with columns:
- order_id (string)
- customer_id (string)
- order_status (string: "delivered", "cancelled", etc)
- order_purchase_timestamp (datetime)

How do I count the number of orders for each order_status 
and sort the result from highest to lowest?
```

**Expected DeepSeek response:**
```python
status_counts = orders['order_status'].value_counts().sort_values(ascending=False)
print(status_counts)
```

---

## Verification Against Curriculum

**CRITICAL RULE**: If DeepSeek's answer doesn't match the verified value in the curriculum, the code is wrong — not the curriculum.

**Example:**
- Curriculum says: Total delivered orders = 96,482
- DeepSeek code produces: 96,480
- **Action**: Tell student to revise the prompt or check for filtering issues

---

## Week-by-Week DeepSeek Prompts

### Week 4: Pandas Introduction

**Prompt 1**: "Count how many orders exist in the dataset and display the first 5"
**Expected output**: Total: 99,441; then df.head()

**Prompt 2**: "What are the column names and data types in the orders DataFrame?"
**Expected output**: orders.info() output

### Week 5: Groupby & Aggregation

**Prompt 3**: "Group orders by customer_state and count orders per state"
**Expected output**: Series with states as index, order counts as values

### Week 6: Data Cleaning

**Prompt 4**: "Find rows where product_category_name is null and count them"
**Expected output**: ~201 nulls (or similar number from curriculum)

### Week 7: Merging

**Prompt 5**: "Merge orders with customers on customer_id. Show the merged shape and first 3 rows"
**Expected output**: Shape, first 3 rows showing combined data

---

## Common DeepSeek Mistakes (and Fixes)

### Mistake 1: Wrong method name
- **DeepSeek gives**: `orders.group_by('status')`
- **Correct**: `orders.groupby('status')`
- **Why**: pandas uses `groupby()` not `group_by()`

### Mistake 2: Missing aggregation
- **DeepSeek gives**: `orders.groupby('order_status')`  (returns GroupBy object)
- **Correct**: `orders.groupby('order_status').size()`  (returns counts)
- **Why**: GroupBy object must have aggregation method

### Mistake 3: Wrong null check
- **DeepSeek gives**: `orders[orders['product_id'] == None]`
- **Correct**: `orders[orders['product_id'].isna()]`
- **Why**: pandas uses `.isna()` not `== None` for null checks

---

## How to Grade DeepSeek-Generated Code

1. **Run the code**: Execute in Colab notebook
2. **Compare output**: Does it match the expected value from curriculum?
3. **Check explanation**: Can the student explain what each line does?
4. **Give feedback**: If wrong, ask them to revise the prompt, not accept the code blindly

---

## Instructor Tips

- **Celebrate good prompts**: When a student writes a clear prompt, praise it
- **Show bad prompts**: Model what happens when you ask DeepSeek vague questions
- **Verify always**: Never assume DeepSeek is right — always check against curriculum
- **Use as teaching tool**: Show how DeepSeek makes mistakes and how to fix them
