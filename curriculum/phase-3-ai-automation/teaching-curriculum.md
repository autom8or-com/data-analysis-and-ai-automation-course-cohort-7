# AI Automation for Business Operations
## From Data Analyst to Automation Expert: Transform Ready Delight Foods

### Course Overview

**Duration:** 24 weeks (6 months)
- **Learning Phase:** 21 weeks (42 sessions, Wed+Thu)
- **Capstone Project:** 3 weeks (6 sessions, Wed+Thu)

**Format:**
- **Live Sessions:** 90 minutes, twice weekly (Wednesday & Thursday)
- **Wednesday:** Live demo/build → Practice → Q&A
- **Thursday:** Continuation + Homework assignment (1-week deadline)
- **Module Demo Days:** Students showcase cluster work at end of each module

**Teaching Case:** Ready Delight Foods and Confectioneries (Nigerian peanut startup)

**Student Profile:**
- Completed Excel (Phase 1) + Python & SQL (Phase 2a/2b) + Streamlit Capstone (Phase 2c) at PORA Academy
- Familiar with: pandas, SQL JOINs, CTEs, relational data models, Streamlit, GitHub deployment
- Ground zero in: n8n, NocoDB, AI APIs, business automation

**Infrastructure:**
- n8n (self-hosted on Coolify)
- NocoDB (self-hosted database)
- Streamlit (for dashboards — students already proficient from Phase 2c)
- Gemini/Claude APIs (AI content generation)
- AI coding tools (v0.dev, Cursor, Bolt.new) — used in Module 6

---

# Module 1: Foundations & Data Infrastructure
## Weeks 1-2 (4 Sessions)

> **Note on prerequisites:** Students arrive with 8 weeks of Python (pandas, merging, visualisation, Streamlit), 8 weeks of SQL (JOINs, CTEs, window functions), and a deployed Streamlit capstone project. Data modelling concepts are not re-taught from scratch — only what is new (NocoDB and n8n) receives full instruction time.

---

### **Week 1: Data Infrastructure Setup**

#### Session 1 (Wed): Business Brief + Data Model + NocoDB

**Learning Objectives:**
- Analyse Ready Delight's business processes for automation opportunities
- Map the Ready Delight entity model
- Build the full NocoDB database from scratch

**Content:**
1. **Ready Delight Business Deep Dive** (15 min)
   - Review the business brief together
   - Current state: CEO doing everything manually — purchase, prep, package, market, sell
   - Pain points: no customer tracking, no order visibility, no follow-up system
   - Automation opportunities ranked by impact: social media → orders → inventory → reporting

2. **Ready Delight Data Model** (10 min)
   - *Students know ERDs from SQL Phase 2b — this is application, not instruction*
   - 6 entities: Products, Customers, Orders, Order_Items, Suppliers, Inventory_Transactions
   - Map relationships: Orders → Customers, Order_Items → Orders + Products
   - Quick Q&A: what fields does each table need?

3. **Building the NocoDB Database** (65 min)
   - What is NocoDB and why we use it: it sits on top of a real database and exposes an HTTP API — n8n can read and write to it without writing SQL
   - Accessing the shared NocoDB instance; understanding bases, tables, views
   - Live build: Products (product_id, name, category, price, cost, inventory_count)
   - Live build: Customers (customer_id, name, phone, email, type, location, acquisition_date)
   - Live build: Orders (order_id, customer_id link, order_date, status, total_amount, payment_status)
   - Live build: Order_Items (item_id, order_id link, product_id link, quantity, unit_price, subtotal)
   - Demonstrating linked records — equivalent to a SQL foreign key, but clickable in the UI
   - Students build: Suppliers and Inventory_Transactions with correct links

**Student Practice:**
- Create Suppliers and Inventory_Transactions tables with correct fields and linked records
- Add 10 sample products (Ready Delight peanut varieties, ₦ pricing)

**Wednesday Practice Questions:**
1. How does a NocoDB linked record compare to a SQL foreign key JOIN?
2. What field type would you use for order_date vs order_status?
3. What table would you query to find all products in an order?

**Homework (Assigned Thursday):**
- Complete the full Ready Delight NocoDB database:
  - Products (≥10 items), Customers (≥20), Orders (≥15 with line items), Suppliers (≥5), Inventory_Transactions (≥10)
  - Use realistic Nigerian data (Lagos addresses, Nigerian phone numbers, ₦ pricing)
- Submit screenshots of database structure and sample records

---

#### Session 2 (Thu): n8n Fundamentals + First Automations

**Learning Objectives:**
- Navigate the n8n interface and understand the node-based execution model
- Build a workflow connecting NocoDB to Google Sheets
- Create a scheduled social media automation

**Content:**
1. **What is n8n?** (15 min)
   - Low-code automation: nodes, triggers, data flow — each node transforms or routes data
   - Why n8n over writing Python scripts (visual, schedulable, runs 24/7, no server management)
   - Self-hosted on shared Coolify instance; accessing the n8n UI; credentials manager

2. **First Workflow: NocoDB → Google Sheets** (30 min)
   - Manual Trigger node
   - NocoDB node: configure credentials, query all products
   - Reading JSON data in the inspector — same concept as a Python dict/list
   - Google Sheets node: export products list
   - Test, verify, view execution history

3. **Data Transformation + Scheduling** (15 min)
   - Set node: create/modify fields; expressions (`{{ $json.price * 1.1 }}`)
   - Date formatting; ₦ currency formatting
   - Schedule Trigger: cron syntax for daily 9 AM

4. **First Social Media Automation** (30 min)
   - Schedule Trigger → NocoDB (get today's featured product) → Set node (format post text) → Instagram/Facebook API → NocoDB (log activity)
   - Connect Instagram Business Account API credentials
   - Test execution end-to-end

**Live Demo:**
- NocoDB → Google Sheets workflow built from scratch
- Scheduled social post workflow end-to-end

**Student Practice:**
- Modify social post to include price in ₦ and 3 relevant Nigerian hashtags
- Change schedule to 7 PM instead of 9 AM

**Homework (1 week):**
- Build 3 workflows:
  1. Daily pending-orders email summary to CEO
  2. Low-inventory alert (products < 10 units) → email/WhatsApp
  3. Daily social post rotating through product catalog
- Document each with screenshots and execution logs

---

### **Week 2: Error Handling, Dashboard & Mini Demo Day**

#### Session 3 (Wed): Error Handling + NocoDB-Connected Streamlit Dashboard

**Learning Objectives:**
- Implement error handling and monitoring in n8n workflows
- Connect a Streamlit dashboard to NocoDB via HTTP API
- Deploy the dashboard for team access

**Content:**
1. **Error Handling in n8n** (30 min)
   - Common failures: API timeouts, bad data from NocoDB, network errors
   - Continue on Fail setting — keep the workflow running; inspect what failed later
   - Error Trigger node: a separate workflow that fires when the main one fails
   - IF node: validate data before it hits an API (e.g. check phone number not empty)
   - Logging errors to NocoDB: create Error_Log table (workflow_name, error_date, error_message, status)
   - Slack/email notification on failure

2. **Streamlit + NocoDB API** (45 min)
   - *Students know Streamlit from Phase 2c — this covers only the new skill: calling a REST API instead of SQLite*
   - NocoDB REST API: xc-token authentication header, endpoint structure
   - `requests.get()` → JSON response → `pd.DataFrame(response.json()["list"])`
   - Replace familiar `pd.read_sql()` pattern with NocoDB API call pattern
   - Build the Ready Delight KPI dashboard: total customers, total orders, total revenue (₦), products in stock, sales trend line chart, customer type breakdown
   - `@st.cache_data(ttl=300)` — cache for 5 minutes so dashboard doesn't hammer NocoDB
   - Deploy to Streamlit Community Cloud (same GitHub flow as Phase 2c); store NocoDB token in `st.secrets`

**Live Demo:**
```python
import streamlit as st, requests, pandas as pd

NOCODB_URL = "https://your-nocodb/api/v1/db/data/v1/BASE_ID"

@st.cache_data(ttl=300)
def fetch(table):
    r = requests.get(f"{NOCODB_URL}/{table}",
                     headers={"xc-token": st.secrets["NOCODB_TOKEN"]})
    return pd.DataFrame(r.json()["list"])

orders = fetch("Orders")
customers = fetch("Customers")

col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", len(orders))
col2.metric("Total Customers", len(customers))
col3.metric("Revenue", f"₦{orders['total_amount'].sum():,.0f}")
```

**Student Practice:**
- Add a "Low Inventory" section: products with < 10 units highlighted in red
- Add error handling to the daily social post workflow from Week 1

**Homework (Assigned Thursday):**
- Add error handling to all 3 homework workflows; create Error_Log table in NocoDB
- Add a "Workflow Health" panel to the Streamlit dashboard showing error counts
- Deploy updated dashboard to Streamlit Cloud; share URL

---

#### Session 4 (Thu): Mini Demo Day + Module 2 Preview

**Format:**
- Cluster presentations: 8 minutes each (up to 3 clusters)
- Peer feedback (10 min)
- Instructor feedback and best-practices recap (15 min)
- Documentation standards: naming conventions, node annotations in n8n, README files (15 min)
- Module 2 preview: Marketing Automation — what's coming (5 min)
- Open Q&A (5 min)

**Presentation Requirements (each cluster):**
- Show NocoDB database structure and explain one design decision
- Demonstrate one working scheduled workflow live
- Show deployed Streamlit dashboard with live NocoDB data
- Share one thing that broke and how you fixed it

**Assessment:**
- Database design quality and realistic sample data
- Workflow functionality and error handling
- Dashboard reflects live NocoDB data (not hardcoded)
- Ability to explain technical decisions

**Homework:**
- Based on feedback, improve your weakest workflow before Module 2 begins
- Write a 3–5 sentence LinkedIn post: "What I built this week at PORA Academy" — tag #automation #n8n #Nigeria

---

# Module 2: Marketing Automation
## Weeks 3-6 (8 Sessions)

### **Week 3: AI-Powered Content Creation**

#### Session 5 (Wed): Introduction to AI Content Generation

**Learning Objectives:**
- Understand LLMs for marketing content
- Integrate Gemini/Claude APIs with n8n
- Generate product descriptions automatically
- Create marketing copy at scale

**Content:**
1. **AI for Marketing Content** (20 min)
   - What LLMs can do (and can't do)
   - Gemini vs Claude vs GPT for content
   - Cost considerations (Gemini free tier)
   - Prompt engineering basics

2. **Setting Up AI Nodes in n8n** (25 min)
   - Google Gemini API setup
   - Claude API setup (Anthropic)
   - Configuring credentials in n8n
   - Testing API connections

3. **Generating Product Descriptions** (45 min)
   - Workflow: Product → AI → Enhanced Description
   - Prompt engineering for product descriptions:
     ```
     Create an engaging product description for Nigerian social media.
     
     Product: {product_name}
     Category: {category}
     Price: ₦{price}
     Features: {features}
     
     Make it:
     - Appealing to Lagos/Nigerian audience
     - Include emojis
     - Mention health benefits if applicable
     - Keep under 150 words
     - Include call-to-action
     ```
   - Storing generated content in NocoDB
   - Updating product descriptions in database

**Live Demo:**
- Build workflow: NocoDB (get products) → Gemini (generate descriptions) → NocoDB (update records)
- Show different prompt styles
- Demonstrate A/B testing different AI-generated descriptions

**Student Practice:**
- Generate descriptions for 10 products
- Experiment with different prompt styles
- Compare Gemini vs Claude outputs

**Wednesday Practice Questions:**
1. How would you generate social media captions for different platforms (Instagram vs Facebook)?
2. What information would make AI-generated content more specific to Ready Delight?
3. How can you ensure AI doesn't generate inappropriate content?

**Homework (Assigned Thursday):**
- Create workflows to generate:
  1. Product descriptions for all products (update NocoDB)
  2. Weekly promotional social media posts (5 different posts)
  3. Customer testimonial templates
- Create "Content_Library" table in NocoDB to store generated content
- Add metrics to dashboard: Content pieces generated this week

---

#### Session 6 (Thu): Multi-Channel Content Distribution

**Learning Objectives:**
- Schedule content across multiple platforms
- Create content calendar automation
- Personalize content by platform
- Track content performance

**Content:**
1. **Content Calendar Strategy** (20 min)
   - Planning weekly content
   - Platform-specific content (Instagram vs WhatsApp vs Email)
   - Timing for Nigerian audience
   - Content rotation and variety

2. **Building Content Calendar in NocoDB** (25 min)
   - Content_Calendar table structure:
     - Fields: post_id, content_text, platform, scheduled_date, status, performance_metrics
   - Planning week's content
   - Linking to products/campaigns

3. **Multi-Platform Distribution Workflow** (45 min)
   - Schedule Trigger (checks calendar hourly)
   - NocoDB: Get posts scheduled for current hour
   - Switch node: Route by platform
     - Instagram Business API
     - Facebook Pages API
     - WhatsApp Business API (optional)
     - Email (for newsletter)
   - Update status in calendar after posting
   - Log performance data

**Live Demo:**
- Build complete content distribution workflow
- Show platform-specific formatting
- Demonstrate scheduling logic
- Track posting success/failures

**Student Practice:**
- Create 2-week content calendar for Ready Delight
- Set up multi-platform posting workflow
- Test with sample posts

**Homework (1 week):**
- Build complete content marketing system:
  - Content_Calendar table with 30 scheduled posts
  - AI-powered content generation for all posts
  - Multi-platform distribution workflow
  - Performance tracking (save post IDs for later analysis)
- Enhance dashboard with Marketing section:
  - Posts scheduled this week
  - Posts published today
  - Content by platform breakdown
- Create workflow documentation

**Career Enablement:**
*For freelancers: Content marketing automation is highly sellable. Practice pitch: "I'll create and schedule 60 social media posts per month for ₦75,000, using AI to ensure quality and consistency."*

---

### **Week 4: Lead Capture & CRM Automation**

#### Session 7 (Wed): Building Lead Magnet System

**Learning Objectives:**
- Create lead capture forms
- Build email collection workflow
- Set up welcome email sequence
- Store leads in NocoDB CRM

**Content:**
1. **Lead Magnet Strategy** (20 min)
   - What is a lead magnet (free recipe ebook, discount code)
   - Ready Delight lead magnet ideas:
     - "10 Healthy Nigerian Snack Ideas" PDF
     - "First-time customer: 20% off" discount code
   - Landing page basics (preview of website building)

2. **Lead Capture Forms** (25 min)
   - Using NocoDB forms for lead capture
   - Custom form styling
   - Embedding form on website (n8n webhook alternative)
   - Using Typeform/Google Forms as alternative

3. **Lead Processing Workflow** (45 min)
   - Webhook Trigger (form submission)
   - Extract lead data (name, phone, email, interest)
   - NocoDB: Add to Customers table (mark as "lead")
   - Send welcome email with lead magnet
   - Tag customer with source (Instagram, Facebook, WhatsApp)
   - Schedule follow-up sequence

**Live Demo:**
- Create NocoDB lead capture form
- Build webhook workflow for form submissions
- Set up welcome email template
- Demonstrate lead tagging and segmentation

**Student Practice:**
- Design lead magnet for Ready Delight
- Create lead capture form
- Build welcome email workflow
- Test end-to-end flow

**Wednesday Practice Questions:**
1. How would you track which lead source converts best?
2. What information should you collect on lead form (balance detail vs conversion)?
3. How can you prevent spam form submissions?

**Homework (Assigned Thursday):**
- Create complete lead capture system:
  - Design lead magnet (PDF or discount code)
  - Build lead capture form with NocoDB
  - Create workflow: Form → Welcome Email → Add to CRM → Schedule Follow-up
  - Set up lead source tracking
- Create "Leads" view in NocoDB showing:
  - New leads this week
  - Leads by source
  - Leads by status (new/contacted/converted/lost)
- Add to dashboard: Lead metrics (new leads, conversion rate)

---

#### Session 8 (Thu): WhatsApp Business & Follow-Up Automation

**Learning Objectives:**
- Integrate WhatsApp Business API
- Build automated follow-up sequences
- Create customer engagement workflows
- Track communication history

**Content:**
1. **WhatsApp Business for Nigerian Market** (20 min)
   - Why WhatsApp matters in Nigeria
   - WhatsApp Business API vs WhatsApp Business App
   - Setting up WhatsApp Business API (using third-party like Twilio/360Dialog)
   - Compliance and best practices

2. **WhatsApp Integration in n8n** (25 min)
   - Configuring WhatsApp credentials
   - Sending messages via API
   - Receiving messages (webhook)
   - Message templates and approval
   - Rate limits and costs

3. **Automated Follow-Up Sequences** (45 min)
   - Day 1: Welcome message
   - Day 3: Product recommendation based on interest
   - Day 7: Limited-time offer
   - Day 14: Feedback request
   - Storing communication history in NocoDB
   - Unsubscribe handling

**Live Demo:**
- Set up WhatsApp Business API integration
- Build multi-day follow-up sequence workflow
- Show how to personalize messages with customer data
- Demonstrate communication logging

**Student Practice:**
- Create 14-day WhatsApp follow-up sequence
- Personalize messages with customer name and preferences
- Test with sample leads

**Homework (1 week):**
- Build complete CRM automation:
  - Lead capture → Welcome email + WhatsApp
  - 14-day automated follow-up (mix of email and WhatsApp)
  - Conversion tracking (lead → customer when first order placed)
  - Communication history logging
- Create "Communications" table in NocoDB:
  - Fields: comm_id, customer_id, channel, message_text, sent_date, status
- Enhance dashboard with CRM metrics:
  - Lead funnel visualization
  - Conversion rate
  - Response rate
  - Communication volume by channel
- Document customer journey map

**Career Enablement:**
*This CRM automation can be sold as standalone service: "Automated customer follow-up system that converts 30% of leads into customers - ₦150,000 setup + ₦50,000/month."*

---

### **Week 5: Marketing Analytics & Optimization**

#### Session 9 (Wed): Social Media Analytics Integration

**Learning Objectives:**
- Pull analytics data from social platforms
- Track engagement metrics
- Analyze content performance
- Create marketing performance dashboard

**Content:**
1. **Social Media APIs for Analytics** (20 min)
   - Instagram Insights API
   - Facebook Page Insights
   - Available metrics: reach, impressions, engagement, clicks
   - API rate limits and data retention

2. **Analytics Data Collection** (35 min)
   - Schedule workflow (daily collection)
   - Instagram: Get post insights
   - Facebook: Get page insights
   - Store in NocoDB "Social_Analytics" table:
     - Fields: post_id, platform, date, reach, impressions, likes, comments, shares, clicks
   - Historical data tracking

3. **Performance Analysis** (35 min)
   - Calculate engagement rate
   - Identify top-performing content types
   - Best posting times analysis
   - Content ROI (engagement per post)
   - Product mentions to sales correlation

**Live Demo:**
- Build analytics collection workflow
- Show data transformation for analysis
- Create performance comparison queries
- Identify insights from data

**Student Practice:**
- Collect analytics for past 30 days
- Calculate engagement rates
- Identify top 5 posts
- Find patterns (timing, content type, hashtags)

**Wednesday Practice Questions:**
1. Which content type performs best for Ready Delight?
2. What time of day gets highest engagement in Nigeria?
3. How would you measure ROI of social media efforts?

**Homework (Assigned Thursday):**
- Build marketing analytics system:
  - Daily social media data collection workflow
  - Performance analysis workflow (weekly summary)
  - Top content identification
  - Underperforming content flagging
- Create comprehensive marketing dashboard section:
  - Engagement rate trend
  - Reach and impressions over time
  - Top 10 posts this month
  - Content type performance comparison
  - Platform comparison (Instagram vs Facebook)
- Generate weekly marketing report (automated email to "CEO")

---

#### Session 10 (Thu): A/B Testing & Campaign Management

**Learning Objectives:**
- Design A/B tests for marketing content
- Track campaign performance
- Optimize content based on data
- Calculate marketing ROI

**Content:**
1. **A/B Testing Fundamentals** (20 min)
   - What to test: headlines, images, CTAs, posting times
   - Sample size and statistical significance
   - Test duration
   - Nigerian market considerations

2. **Campaign Management in NocoDB** (30 min)
   - "Campaigns" table structure:
     - Fields: campaign_id, name, start_date, end_date, budget, goal, status
   - "Campaign_Variants" table (for A/B tests):
     - Fields: variant_id, campaign_id, variant_name, content, platform, performance_metrics
   - Linking posts to campaigns

3. **A/B Testing Workflow** (40 min)
   - Workflow: Create two content variants using AI
   - Post both variants at same time (different accounts or audience segments)
   - Collect performance data after 24 hours
   - Determine winner based on engagement rate
   - Use winning variant for future similar content
   - Store learnings in "Content_Insights" table

**Live Demo:**
- Build A/B testing workflow
- Create two variants of product post
- Show winner determination logic
- Demonstrate insight storage

**Student Practice:**
- Design A/B test for Ready Delight peanut promotion
- Create 2 variants (different headlines or images)
- Set up tracking workflow

**Homework (1 week):**
- Execute complete marketing campaign:
  - Campaign: "Ready Delight Peanut Launch Week"
  - Goals: 100 new leads, 50 orders, ₦200,000 revenue
  - Duration: 7 days
  - Budget: ₦10,000 for ads (track spend in NocoDB)
  - Content: 14 posts (2 per day), mix of formats
  - A/B tests: Test 3 different CTAs
  - Lead magnet: 15% discount for first-time customers
- Track everything in NocoDB
- Create campaign performance dashboard
- Write campaign summary report (AI-assisted)
- Submit campaign results with insights

**Career Enablement:**
*Campaign management is high-value skill. Practice presenting ROI: "We spent ₦10,000 on marketing and generated ₦200,000 in revenue - 20x ROI."*

---

### **Week 6: Marketing Consolidation & Demo Day**

#### Session 11 (Wed): Marketing Automation Review

**Learning Objectives:**
- Review Phase 2 concepts
- Optimize existing marketing workflows
- Prepare marketing portfolio
- Demo Day preparation

**Content:**
1. **Marketing Automation Review** (40 min)
   - AI content generation best practices
   - Multi-channel distribution optimization
   - Lead capture and conversion tactics
   - Analytics and A/B testing insights

2. **Workflow Optimization** (30 min)
   - Reducing API costs (caching, batching)
   - Improving content quality with better prompts
   - Faster execution with parallel processing
   - Error handling improvements

3. **Portfolio Development** (20 min)
   - Documenting marketing automation system
   - Creating before/after metrics
   - Building case study narrative
   - Demo presentation structure

**Student Practice:**
- Optimize your marketing workflows
- Create portfolio documentation
- Prepare Demo Day presentation

**Wednesday Practice Questions:**
1. What marketing automation had biggest impact for Ready Delight?
2. How would you sell this service to a client?
3. What would you do differently if starting over?

---

#### Session 12 (Thu): **DEMO DAY 2 - Marketing Automation**

**Format:**
- Cluster presentations (20 min each)
- Live demos of marketing automation
- Campaign results presentation
- Portfolio review
- Peer and instructor feedback

**Presentation Requirements:**
- Show complete marketing automation system
- Demonstrate AI content generation
- Walk through lead capture to customer journey
- Present campaign results and ROI
- Show marketing dashboard with real data
- Explain 1-2 key insights from analytics

**Assessment Criteria:**
- System completeness and integration
- Content quality and Nigerian market fit
- Data-driven decision making
- Campaign ROI
- Presentation and storytelling
- Professional portfolio quality

**Homework:**
- Refine marketing automation based on feedback
- Create LinkedIn post showcasing your marketing automation skills
- Write case study: "How I Automated Marketing for a Nigerian Food Startup"
- Update portfolio with marketing projects

**Career Enablement:**
*Update LinkedIn profile: Add "Marketing Automation Specialist" skills. Share Demo Day presentation as post. Reach out to 5 small businesses offering free marketing audit.*

---

# Module 3: Revenue Operations
## Weeks 7-10 (8 Sessions)

### **Week 7: Order Processing Automation**

#### Session 13 (Wed): Quote Generation & Order Forms

**Learning Objectives:**
- Create automated quote generation
- Build order capture forms
- Calculate pricing with business rules
- Generate professional quotes (PDF)

**Content:**
1. **Ready Delight Pricing Strategy** (20 min)
   - Product pricing structure
   - Bulk discount tiers (1-10 pcs, 11-50 pcs, 51+ pcs)
   - Customer type pricing (individual, shop, wholesaler)
   - Delivery fees by Lagos zone
   - Tax calculations (VAT if applicable)

2. **Quote Request Form** (25 min)
   - NocoDB form for quote requests
   - Fields: customer_info, products_requested, quantities, delivery_location
   - Form validation
   - Webhook trigger on submission

3. **Automated Quote Generation** (45 min)
   - Workflow: Quote Request → Calculate Pricing → Generate PDF → Email
   - Pricing calculation logic:
     ```javascript
     // Pseudo-code
     for each product:
       base_price = product.price
       if quantity >= 51: discount = 15%
       else if quantity >= 11: discount = 10%
       else if quantity >= 1: discount = 0%
       
       if customer_type == 'wholesaler': discount += 5%
       
       line_total = base_price * quantity * (1 - discount)
     
     subtotal = sum(line_totals)
     delivery = calculate_delivery_fee(location)
     total = subtotal + delivery
     ```
   - PDF generation using HTML template + API (HTMLtoPDF)
   - Branded quote template with Ready Delight logo
   - Email quote to customer with follow-up scheduled

**Live Demo:**
- Build complete quote generation workflow
- Show pricing calculation logic
- Create professional PDF quote
- Demonstrate email delivery

**Student Practice:**
- Create quote for different customer scenarios
- Test discount calculations
- Customize PDF template

**Wednesday Practice Questions:**
1. How would you handle custom product requests (not in catalog)?
2. What validation would you add to prevent errors?
3. How can you track quote-to-order conversion rate?

**Homework (Assigned Thursday):**
- Build complete quote generation system:
  - Quote request form (NocoDB or Typeform)
  - Pricing calculation workflow with all business rules
  - PDF generation with professional template
  - Automated email with quote + follow-up in 3 days
- Create "Quotes" table in NocoDB:
  - Fields: quote_id, customer_id, quote_date, items (JSON), subtotal, delivery, total, status (sent/accepted/rejected/expired)
- Track quotes in dashboard: Quotes sent, acceptance rate, average quote value

---

#### Session 14 (Thu): Order Confirmation & Payment Integration

**Learning Objectives:**
- Build order confirmation workflow
- Integrate Nigerian payment gateways
- Handle payment verification
- Update inventory on confirmed orders

**Content:**
1. **Nigerian Payment Landscape** (20 min)
   - Paystack, Flutterwave, Interswitch
   - Payment methods: Card, bank transfer, USSD, mobile money
   - Payment confirmation webhooks
   - Handling failed payments

2. **Payment Gateway Integration** (30 min)
   - Paystack API setup
   - Creating payment links
   - Webhook configuration for payment notifications
   - Payment verification workflow

3. **Order Confirmation Workflow** (40 min)
   - Customer accepts quote → Generate payment link
   - Send payment link via email/WhatsApp
   - Webhook: Payment successful → Update order status
   - Confirm order in NocoDB (status: pending → confirmed)
   - Reduce inventory quantities
   - Send order confirmation to customer
   - Notify operations team for fulfillment
   - Schedule delivery reminder

**Live Demo:**
- Integrate Paystack payment gateway
- Build payment link generation workflow
- Show webhook payment verification
- Demonstrate inventory update

**Student Practice:**
- Create test payment scenario
- Process order from quote to payment
- Verify inventory reduction

**Homework (1 week):**
- Build complete order-to-payment system:
  - Quote accepted → Generate payment link
  - Payment webhook → Verify and confirm order
  - Inventory update workflow
  - Order confirmation emails/WhatsApp
  - Operations team notification
- Create "Payments" table:
  - Fields: payment_id, order_id, amount, method, status, transaction_ref, payment_date
- Handle payment failures and retries
- Add revenue dashboard section:
  - Today's revenue
  - This week's revenue
  - Payment method breakdown
  - Pending payments
  - Revenue trend chart

**Career Enablement:**
*Payment integration is specialized skill. Position yourself: "I integrate Nigerian payment gateways (Paystack/Flutterwave) and automate entire order-to-cash process - ₦200,000 setup fee."*

---

### **Week 8: Invoicing & Revenue Tracking**

#### Session 15 (Wed): Automated Invoice Generation

**Learning Objectives:**
- Generate professional invoices automatically
- Handle Nigerian tax requirements
- Store invoices for accounting
- Send invoices to customers

**Content:**
1. **Invoice Requirements** (15 min)
   - Nigerian invoice essentials
   - VAT handling (if registered)
   - Invoice numbering system
   - Payment terms and due dates

2. **Invoice Data Model** (20 min)
   - "Invoices" table in NocoDB:
     - Fields: invoice_id, invoice_number, order_id, customer_id, issue_date, due_date, items (JSON), subtotal, tax, total, status, paid_date
   - Linking invoices to orders and payments

3. **Invoice Generation Workflow** (55 min)
   - Trigger: Order confirmed
   - Generate invoice number (AUTO-INCREMENT or custom format: INV-2024-0001)
   - Calculate line items from order
   - Apply tax if applicable
   - Create professional PDF invoice (HTML template):
     - Ready Delight branding
     - Company details
     - Customer details
     - Itemized charges
     - Payment instructions (bank details)
     - QR code for payment link
   - Save invoice PDF to Google Drive
   - Store invoice record in NocoDB
   - Email invoice to customer
   - Schedule payment reminder workflow

**Live Demo:**
- Build invoice generation workflow
- Create professional invoice template
- Show PDF generation
- Demonstrate email delivery and storage

**Student Practice:**
- Customize invoice template with branding
- Generate invoices for different order types
- Test invoice storage and retrieval

**Wednesday Practice Questions:**
1. How would you handle invoice corrections or cancellations?
2. What information should be in payment reminders?
3. How can you track overdue invoices?

**Homework (Assigned Thursday):**
- Build complete invoicing system:
  - Automated invoice generation on order confirmation
  - Professional PDF invoices with Ready Delight branding
  - Invoice storage in Google Drive (organized by month)
  - Invoice records in NocoDB
  - Email delivery to customers
- Create invoice reminder workflow:
  - 3 days before due date: Friendly reminder
  - On due date: Payment due notice
  - 3 days after due date: Overdue notice
  - 7 days after due date: Escalation notice
- Add invoicing dashboard section:
  - Total invoiced this month
  - Total paid
  - Total outstanding
  - Overdue invoices
  - Aging analysis (0-30, 31-60, 61+ days)

---

#### Session 16 (Thu): Revenue Reporting & Analytics

**Learning Objectives:**
- Build comprehensive revenue reports
- Track key revenue metrics
- Analyze sales patterns
- Create executive revenue dashboard

**Content:**
1. **Revenue Metrics & KPIs** (20 min)
   - Total revenue (daily, weekly, monthly)
   - Average order value
   - Revenue by product
   - Revenue by customer type
   - Revenue growth rate
   - Days sales outstanding (DSO)

2. **Sales Analytics** (30 min)
   - Product performance analysis
   - Customer segment analysis
   - Peak sales times/days
   - Seasonal trends
   - Customer lifetime value (CLV)

3. **Automated Revenue Reporting** (40 min)
   - Daily revenue summary (email to CEO)
   - Weekly sales report (detailed breakdown)
   - Monthly financial report (comprehensive)
   - Quarter-end revenue review
   - AI-generated insights and recommendations
   - Report formatting and visualization

**Live Demo:**
- Build revenue analytics queries
- Create automated daily revenue email
- Generate weekly sales report
- Show AI-generated insights from revenue data

**Student Practice:**
- Query revenue data for different time periods
- Calculate key metrics
- Generate custom reports

**Homework (1 week):**
- Build complete revenue analytics system:
  - Daily revenue summary email
  - Weekly sales report (PDF) with charts
  - Monthly financial report
  - Revenue forecasting (simple trend-based)
  - AI-generated insights workflow
- Create comprehensive revenue dashboard:
  - Revenue today/week/month/year
  - Revenue vs target
  - Revenue trend line
  - Revenue by product (pie chart)
  - Revenue by customer type
  - Top 10 customers
  - DSO tracking
  - Cash flow projection (simple)
- Document the complete order-to-cash process

**Career Enablement:**
*Revenue automation is C-level concern. Practice executive presentation: "Automated revenue reporting gives you real-time visibility into business performance - see today's sales before breakfast."*

---

### **Week 9: Customer Communication & Retention**

#### Session 17 (Wed): Post-Purchase Communication

**Learning Objectives:**
- Build post-purchase email sequences
- Collect customer feedback automatically
- Handle customer support requests
- Create customer satisfaction tracking

**Content:**
1. **Post-Purchase Journey** (20 min)
   - Order confirmation → Shipping update → Delivery confirmation → Feedback request
   - Communication timing and frequency
   - Channel selection (email vs WhatsApp)

2. **Delivery Tracking & Updates** (30 min)
   - "Deliveries" table in NocoDB:
     - Fields: delivery_id, order_id, status, delivery_date, delivery_person, customer_rating
   - Status workflow: Pending → In Transit → Out for Delivery → Delivered
   - Automated status updates to customer
   - Integration with delivery service (if available)

3. **Feedback Collection** (40 min)
   - Post-delivery feedback request (24 hours after delivery)
   - NocoDB form for feedback:
     - Fields: order_id, rating (1-5), product_quality, delivery_experience, comments
   - Thank you message for feedback
   - Automated response based on rating:
     - 4-5 stars: Request review/testimonial
     - 1-3 stars: Escalate to customer service, offer resolution

**Live Demo:**
- Build delivery tracking workflow
- Create automated status update system
- Build feedback collection workflow
- Demonstrate rating-based response logic

**Student Practice:**
- Create delivery tracking workflow
- Design feedback form
- Test different rating scenarios

**Wednesday Practice Questions:**
1. How would you handle negative feedback (1-2 star ratings)?
2. What metrics indicate customer satisfaction?
3. How can you encourage repeat purchases?

**Homework (Assigned Thursday):**
- Build complete post-purchase system:
  - Order confirmation message (immediate)
  - Shipping notification (when ready)
  - Delivery update (when out for delivery)
  - Delivery confirmation (when delivered)
  - Feedback request (24 hours post-delivery)
  - Thank you + next purchase incentive (3 days after positive feedback)
- Create "Customer_Feedback" table with all responses
- Build escalation workflow for negative feedback
- Add customer satisfaction metrics to dashboard:
  - Average rating
  - NPS score (if applicable)
  - Response rate
  - Issue resolution rate
- Create monthly customer satisfaction report

---

#### Session 18 (Thu): Loyalty & Retention Automation

**Learning Objectives:**
- Build customer loyalty program
- Create repeat purchase incentives
- Identify at-risk customers
- Win-back campaign automation

**Content:**
1. **Customer Loyalty Strategy** (20 min)
   - Points-based system
   - Tiered benefits (Bronze, Silver, Gold)
   - Referral program
   - Birthday/anniversary offers

2. **Loyalty Program Implementation** (35 min)
   - "Customer_Loyalty" table:
     - Fields: customer_id, points_balance, tier, join_date, last_purchase_date, total_spend, referrals_made
   - Points earning rules:
     - ₦100 spent = 1 point
     - Referral = 50 points
     - Birthday month = 20 bonus points
   - Points redemption:
     - 100 points = ₦500 discount
   - Tier qualification:
     - Bronze: 0-499 points
     - Silver: 500-999 points
     - Gold: 1000+ points
   - Automated points accrual on purchase
   - Tier upgrade notifications

3. **Retention & Win-Back Workflows** (35 min)
   - Identify at-risk customers (no purchase in 60 days)
   - Win-back email campaign with special offer
   - Birthday/anniversary automated greetings + discount
   - Referral program automation:
     - Generate unique referral codes
     - Track referral source
     - Reward both referrer and referee

**Live Demo:**
- Build loyalty points system
- Create tier upgrade workflow
- Build win-back campaign
- Demonstrate referral tracking

**Student Practice:**
- Calculate loyalty points for sample customers
- Design win-back offer
- Create referral code generation

**Homework (1 week):**
- Build complete customer retention system:
  - Loyalty points accrual on every purchase
  - Tier management and upgrade notifications
  - Birthday automation (collect birthdays, send greetings + offer)
  - Win-back campaign for inactive customers
  - Referral program with unique codes and tracking
- Create "Referrals" table:
  - Fields: referral_code, referrer_id, referee_id, status, reward_issued
- Add retention metrics to dashboard:
  - Active customers (purchased in last 30 days)
  - Repeat purchase rate
  - Churn rate
  - Average time between purchases
  - Loyalty tier distribution
  - Referral conversion rate
- Document complete customer lifecycle automation

**Career Enablement:**
*Retention automation reduces customer acquisition costs. Pitch: "Keeping existing customers is 5x cheaper than acquiring new ones. My automation increases repeat purchases by 40%."*

---

### **Week 10: Revenue Operations Consolidation & Demo**

#### Session 19 (Wed): Revenue Operations Review

**Learning Objectives:**
- Review Phase 3 concepts
- Optimize revenue workflows
- Calculate system ROI
- Demo Day preparation

**Content:**
1. **Revenue Operations Review** (40 min)
   - Order processing best practices
   - Payment integration optimization
   - Invoicing and collections strategies
   - Customer retention tactics

2. **System ROI Calculation** (30 min)
   - Time saved per order (before vs after automation)
   - Error reduction impact
   - Faster payment collection
   - Improved customer satisfaction
   - Revenue impact from retention
   - Total ROI calculation for Ready Delight

3. **Portfolio & Case Study** (20 min)
   - Documenting revenue operations system
   - Creating metrics-based case study
   - Building sales deck for freelancing
   - Demo presentation structure

**Student Practice:**
- Calculate ROI for your automation
- Create case study narrative
- Prepare Demo Day presentation

**Wednesday Practice Questions:**
1. What was the highest-impact revenue automation?
2. How would you price this service for a client?
3. What improvements would you make to the system?

---

#### Session 20 (Thu): **DEMO DAY 3 - Revenue Operations**

**Format:**
- Cluster presentations (20 min each)
- Live demo: Quote to cash flow
- ROI presentation with numbers
- Dashboard walkthrough
- Feedback session

**Presentation Requirements:**
- Demonstrate complete order-to-cash process
- Show payment integration working
- Walk through invoice generation and delivery
- Present customer retention workflows
- Show revenue dashboard with real data
- Present ROI calculations
- Explain 2-3 key insights from revenue data

**Assessment Criteria:**
- System completeness and integration
- Payment gateway implementation
- Invoice professionalism
- Customer experience quality
- Data accuracy and reliability
- ROI quantification
- Presentation clarity

**Homework:**
- Refine revenue operations system
- Create detailed case study: "Revenue Automation for Nigerian Food Startup"
- Update portfolio with revenue projects
- Write LinkedIn article on revenue automation impact

**Career Enablement:**
*This is your strongest freelancing offering. Update LinkedIn: "Revenue Operations Automation Specialist | Paystack/Flutterwave Integration Expert | Order-to-Cash Automation." Reach out to 10 businesses offering free revenue audit.*

---

# Module 4: Business Operations
## Weeks 11-14 (8 Sessions)

### **Week 11: Inventory Management Automation**

#### Session 21 (Wed): Inventory Tracking & Replenishment

**Learning Objectives:**
- Build real-time inventory tracking
- Create automated reorder alerts
- Track inventory movements
- Calculate inventory metrics

**Content:**
1. **Inventory Management Fundamentals** (20 min)
   - Current stock levels
   - Reorder points and quantities
   - Lead times for suppliers
   - Cost tracking (FIFO/LIFO/Average)
   - Inventory turnover

2. **Inventory Data Model** (25 min)
   - Enhance "Products" table with inventory fields:
     - current_stock, reorder_point, reorder_quantity, unit_cost, supplier_id
   - "Inventory_Transactions" table:
     - Fields: transaction_id, product_id, transaction_type (purchase/sale/adjustment), quantity, unit_cost, transaction_date, reference (order_id or purchase_id)
   - "Purchases" table:
     - Fields: purchase_id, supplier_id, purchase_date, status, total_amount, received_date

3. **Inventory Tracking Workflows** (45 min)
   - Workflow 1: Update inventory on order
     - Trigger: Order confirmed
     - Reduce stock levels for ordered products
     - Create inventory transaction records
   - Workflow 2: Low stock alerts
     - Schedule: Daily check
     - Identify products below reorder point
     - Generate purchase recommendations
     - Email/Slack alert to operations manager
   - Workflow 3: Stock valuation
     - Calculate total inventory value
     - Track inventory turnover ratio
     - Identify slow-moving items

**Live Demo:**
- Build inventory update workflow
- Create low stock alert system
- Show purchase recommendation logic
- Demonstrate inventory reporting

**Student Practice:**
- Set reorder points for all products
- Process sample orders and watch inventory reduce
- Trigger low stock alerts

**Wednesday Practice Questions:**
1. How would you handle inventory adjustments (damaged goods, theft)?
2. What's the optimal reorder point for Ready Delight Peanuts?
3. How can you track inventory across multiple storage locations?

**Homework (Assigned Thursday):**
- Build complete inventory management system:
  - Automated stock reduction on order
  - Daily low stock check and alerts
  - Purchase recommendation workflow
  - Inventory valuation calculations
  - Stock movement tracking (all transactions logged)
- Create inventory dashboard section:
  - Current stock levels by product
  - Products below reorder point (highlighted)
  - Total inventory value
  - Inventory turnover rate
  - Stock movement history
  - Slow-moving items (no sales in 30 days)
- Set up inventory transaction logging for all operations

---

#### Session 22 (Thu): Supplier Management & Purchase Orders

**Learning Objectives:**
- Automate supplier communication
- Generate purchase orders
- Track supplier performance
- Manage supplier payments

**Content:**
1. **Supplier Management** (20 min)
   - "Suppliers" table enhancement:
     - Fields: supplier_id, name, contact_person, phone, email, address, payment_terms, rating, total_purchases
   - Supplier evaluation criteria (quality, delivery time, price)
   - Preferred supplier identification

2. **Purchase Order Automation** (35 min)
   - Trigger: Low stock alert or manual request
   - Workflow: Generate Purchase Order
     - Determine supplier (based on product-supplier mapping)
     - Calculate quantities (reorder_quantity or custom)
     - Create PO document (PDF):
       - PO number
       - Supplier details
       - Products and quantities
       - Expected delivery date
       - Payment terms
     - Email PO to supplier
     - Store PO in NocoDB ("Purchases" table)
     - Schedule delivery reminder

3. **Goods Receipt & Payment** (35 min)
   - Goods receipt workflow:
     - Mark purchase as "received"
     - Update inventory (increase stock)
     - Record transaction with cost
   - Supplier payment tracking:
     - Link payments to purchases
     - Track outstanding amounts
     - Payment due reminders

**Live Demo:**
- Build PO generation workflow
- Create professional PO template
- Show goods receipt process
- Demonstrate supplier payment tracking

**Student Practice:**
- Generate PO for low-stock product
- Process goods receipt
- Track supplier payment

**Homework (1 week):**
- Build complete supplier management system:
  - Automated PO generation from low stock alerts
  - Professional PO documents (PDF)
  - Email delivery to suppliers
  - Delivery reminder workflow
  - Goods receipt processing
  - Inventory update on receipt
  - Supplier payment tracking
- Create "Supplier_Payments" table:
  - Fields: payment_id, purchase_id, supplier_id, amount, payment_date, method, reference
- Add supplier management dashboard:
  - Outstanding POs
  - Expected deliveries this week
  - Supplier payment status
  - Supplier performance metrics (on-time delivery rate)
  - Total spent by supplier
- Document procurement process flow

**Career Enablement:**
*Procurement automation reduces manual work and improves supplier relationships. Position: "I automate supplier management, reducing procurement time by 60%."*

---

### **Week 12: Production Planning & Scheduling**

#### Session 23 (Wed): Production Workflow Automation

**Learning Objectives:**
- Model production process in NocoDB
- Create production schedules
- Track production status
- Calculate production costs

**Content:**
1. **Ready Delight Production Process** (20 min)
   - Review current manual process:
     1. Purchase raw materials (groundnut, oil, sugar, egg, flour)
     2. Prepare groundnut
     3. Mix eggs and sugar
     4. Coat groundnut
     5. Fry coated nuts
     6. Cool peanuts
     7. Package
   - Production time per batch
   - Raw material requirements per batch
   - Production capacity constraints

2. **Production Data Model** (25 min)
   - "Production_Batches" table:
     - Fields: batch_id, batch_number, product_id, planned_quantity, actual_quantity, start_date, completion_date, status, assigned_to, cost
   - "Production_Materials" table (raw materials):
     - Fields: material_id, name, unit, current_stock, unit_cost, reorder_point
   - "Bill_of_Materials" (BOM) table:
     - Fields: bom_id, product_id, material_id, quantity_required
   - "Production_Transactions" table:
     - Fields: transaction_id, batch_id, material_id, quantity_used, transaction_date

3. **Production Planning Workflow** (45 min)
   - Trigger: Weekly production planning (manual or based on forecast)
   - Workflow: Plan production
     - Analyze: Upcoming orders + inventory levels
     - Calculate: Required production quantities
     - Check: Raw material availability
     - Generate: Production schedule for week
     - Assign: Production batches to dates
     - Alert: Material shortages (trigger material purchase)
   - Production execution tracking:
     - Update batch status (planned → in progress → completed)
     - Record material usage
     - Calculate actual vs planned
     - Update finished goods inventory

**Live Demo:**
- Build production planning workflow
- Create BOM for Ready Delight Peanut
- Show material requirement calculation
- Demonstrate production scheduling

**Student Practice:**
- Define BOM for Ready Delight Peanut
- Plan production for 1000 units
- Calculate raw material requirements

**Wednesday Practice Questions:**
1. How much raw groundnut needed for 500 packs of peanuts?
2. What happens if you run out of a material mid-production?
3. How can you optimize production batch sizes?

**Homework (Assigned Thursday):**
- Build production management system:
  - BOM definition for all products
  - Weekly production planning workflow
  - Material requirement calculation
  - Raw material stock checking
  - Production scheduling
  - Batch tracking (status updates)
  - Material usage logging
  - Production cost calculation
- Create production dashboard:
  - This week's production schedule
  - Production status by batch
  - Material consumption tracking
  - Production cost per unit
  - Production efficiency (actual vs planned)
  - Material shortages
- Set up production alerts (delays, material shortages)

---

#### Session 24 (Thu): Quality Control & Waste Management

**Learning Objectives:**
- Implement quality control checks
- Track product quality metrics
- Manage production waste
- Calculate quality-adjusted costs

**Content:**
1. **Quality Control Process** (20 min)
   - Quality checkpoints in production
   - Pass/fail criteria
   - Rework vs reject decisions
   - Quality metrics (defect rate, pass rate)

2. **Quality Data Model** (20 min)
   - "Quality_Checks" table:
     - Fields: check_id, batch_id, check_date, inspector, pass_fail, defects_found, notes
   - "Defects" table:
     - Fields: defect_id, batch_id, defect_type, quantity, action_taken (rework/reject)

3. **Quality & Waste Tracking** (50 min)
   - Workflow: Quality inspection
     - Trigger: Production batch completed
     - Conduct quality check (manual input or IoT sensor data)
     - Record results in NocoDB
     - If failed: Create rework batch or mark as waste
     - Calculate: Quality-adjusted production quantity
   - Waste tracking:
     - Record waste quantity and type
     - Calculate waste percentage
     - Cost impact of waste
   - Quality alerts:
     - High defect rate alerts
     - Trend analysis (increasing defects)

**Live Demo:**
- Build quality inspection workflow
- Create quality check form
- Show waste calculation
- Demonstrate quality reporting

**Student Practice:**
- Record quality checks for sample batches
- Calculate waste percentages
- Identify quality trends

**Homework (1 week):**
- Build quality management system:
  - Quality check workflow (post-production)
  - Defect logging and categorization
  - Rework/reject decision workflow
  - Waste tracking and cost calculation
  - Quality trend analysis
  - Supplier quality correlation (link defects to raw material batches)
- Add quality metrics to dashboard:
  - Overall quality pass rate
  - Defect rate by product
  - Waste percentage
  - Quality cost impact
  - Quality trends over time
- Create monthly quality report
- Document quality improvement recommendations

**Career Enablement:**
*Quality automation prevents losses. Pitch: "My quality tracking system helped reduce waste from 15% to 5%, saving ₦500,000 annually."*

---

### **Week 13: Delivery & Logistics Automation**

#### Session 25 (Wed): Delivery Management System

**Learning Objectives:**
- Build delivery scheduling workflow
- Track delivery status in real-time
- Optimize delivery routes
- Manage delivery personnel

**Content:**
1. **Lagos Delivery Context** (15 min)
   - Delivery zones (Mainland, Island, Lekki, etc.)
   - Traffic patterns and optimal delivery times
   - Delivery fees by zone
   - Delivery time estimates

2. **Delivery Data Model** (25 min)
   - Enhanced "Deliveries" table:
     - Fields: delivery_id, order_id, delivery_zone, delivery_address, scheduled_date, assigned_to, status, actual_delivery_time, customer_rating, delivery_cost
   - "Delivery_Personnel" table:
     - Fields: person_id, name, phone, vehicle_type, current_location, status (available/busy), deliveries_today, rating
   - "Delivery_Routes" table:
     - Fields: route_id, date, zone, orders (array), assigned_to, total_distance, estimated_time

3. **Delivery Workflows** (50 min)
   - Workflow 1: Delivery scheduling
     - Trigger: Order ready for delivery
     - Determine delivery zone
     - Calculate delivery fee
     - Assign to delivery person (based on zone and availability)
     - Schedule delivery date/time
     - Notify delivery person
     - Send delivery ETA to customer
   - Workflow 2: Route optimization
     - Daily: Group orders by zone
     - Optimize delivery sequence
     - Create route plan
     - Assign to delivery personnel
   - Workflow 3: Delivery tracking
     - Status updates: Out for delivery → Delivered
     - Real-time location sharing (if using GPS)
     - Customer notifications
     - Proof of delivery (photo/signature)

**Live Demo:**
- Build delivery scheduling workflow
- Show zone-based assignment
- Demonstrate route planning
- Create delivery tracking system

**Student Practice:**
- Schedule deliveries for 10 orders
- Optimize route for a zone
- Track delivery status

**Wednesday Practice Questions:**
1. How would you handle failed delivery attempts?
2. What's the best way to optimize routes across Lagos?
3. How can you measure delivery personnel performance?

**Homework (Assigned Thursday):**
- Build complete delivery management system:
  - Automatic delivery scheduling on order ready
  - Zone-based delivery assignment
  - Route optimization workflow
  - Delivery status tracking
  - Customer delivery notifications
  - Delivery personnel app (simple NocoDB form for updates)
  - Proof of delivery collection
- Add delivery metrics to dashboard:
  - Deliveries today/this week
  - On-time delivery rate
  - Average delivery time by zone
  - Delivery personnel performance
  - Failed delivery analysis
  - Delivery cost per order
- Create delivery efficiency report

---

#### Session 26 (Thu): Customer Service & Issue Resolution

**Learning Objectives:**
- Build customer support ticket system
- Automate issue resolution workflows
- Track support metrics
- Improve customer satisfaction

**Content:**
1. **Customer Support in Nigerian Context** (20 min)
   - Common issues: Late delivery, product quality, payment issues
   - Support channels: WhatsApp, phone, email, social media
   - Expected response times
   - Escalation paths

2. **Support Ticket System** (30 min)
   - "Support_Tickets" table:
     - Fields: ticket_id, customer_id, issue_type, description, priority, status, created_date, assigned_to, resolved_date, resolution_notes
   - Ticket sources:
     - WhatsApp message → Create ticket
     - Email → Create ticket
     - Social media comment → Create ticket
     - Negative feedback → Create ticket

3. **Issue Resolution Workflows** (40 min)
   - Workflow 1: Ticket creation
     - Trigger: Customer message on support channels
     - AI: Classify issue type and priority
     - Create ticket in NocoDB
     - Auto-assign based on issue type
     - Send acknowledgment to customer
   - Workflow 2: Resolution tracking
     - Status updates (new → in progress → resolved)
     - SLA monitoring (response within 2 hours, resolution within 24 hours)
     - Escalation if SLA breached
   - Workflow 3: Post-resolution
     - Customer satisfaction survey
     - Request feedback
     - Identify improvement opportunities

**Live Demo:**
- Build ticket creation workflow
- Show AI-powered issue classification
- Demonstrate assignment logic
- Create resolution tracking

**Student Practice:**
- Create tickets for different issue types
- Test assignment workflow
- Track resolution

**Homework (1 week):**
- Build customer support system:
  - Multi-channel ticket creation (WhatsApp, Email, Social)
  - AI-powered issue classification
  - Automatic assignment
  - SLA tracking and escalation
  - Resolution workflows
  - Customer satisfaction surveys
  - Knowledge base integration (FAQ auto-responses)
- Create support dashboard:
  - Open tickets
  - Tickets by status
  - Average resolution time
  - SLA compliance rate
  - Customer satisfaction score
  - Issue type distribution
  - Support personnel performance
- Generate weekly support summary report

**Career Enablement:**
*Customer support automation improves retention. Showcase: "My support system reduced average resolution time from 48 hours to 4 hours, increasing customer satisfaction by 35%."*

---

### **Week 14: Operations Consolidation & Demo**

#### Session 27 (Wed): Operations Review & Integration

**Learning Objectives:**
- Review Phase 4 concepts
- Integrate all operational workflows
- Calculate operational efficiency gains
- Demo Day preparation

**Content:**
1. **Business Operations Review** (40 min)
   - Inventory management best practices
   - Production planning optimization
   - Delivery efficiency strategies
   - Customer support excellence

2. **End-to-End Integration** (30 min)
   - Order → Inventory Check → Production → Quality → Delivery → Support
   - Data flow across all systems
   - Handoff points and automation
   - Error handling across operations

3. **Operational Metrics & ROI** (20 min)
   - Production efficiency gains
   - Inventory optimization savings
   - Delivery performance improvement
   - Customer satisfaction impact
   - Total operational cost reduction
   - Time saved across operations

**Student Practice:**
- Test complete order-to-delivery flow
- Calculate operational ROI
- Prepare comprehensive demo

**Wednesday Practice Questions:**
1. What operational bottleneck had biggest impact when automated?
2. How would you scale operations for 10x growth?
3. What's next automation priority for Ready Delight?

---

#### Session 28 (Thu): **DEMO DAY 4 - Business Operations**

**Format:**
- Cluster presentations (25 min each)
- Live demo: Order through delivery
- Operational metrics presentation
- Complete dashboard walkthrough
- Final portfolio review

**Presentation Requirements:**
- Demonstrate end-to-end operations (inventory → production → delivery → support)
- Show integration between all systems
- Present operational efficiency metrics
- Walk through complete operations dashboard
- Show AI-powered quality and support systems
- Present ROI and impact quantification
- Share key operational insights

**Assessment Criteria:**
- System completeness and integration
- Operations flow efficiency
- Data accuracy and real-time updates
- Dashboard comprehensiveness
- ROI quantification
- Problem-solving approach
- Professional presentation

**Homework:**
- Complete case study: "Digital Transformation of Ready Delight Foods Operations"
- Create comprehensive portfolio showcasing all 4 phases
- Update LinkedIn with complete skill set
- Prepare for final project phase

**Career Enablement:**
*You now have complete business automation portfolio. Update LinkedIn: "Business Operations Automation Specialist | End-to-End Digital Transformation | n8n Expert." Start reaching out to businesses for paid consulting.*

---

# Module 5: Integration & Optimization
## Weeks 15-19 (10 Sessions)

### **Week 15: System Integration & Data Flow**

#### Session 29 (Wed): Connecting All Systems

**Learning Objectives:**
- Integrate all automation phases
- Create master workflows
- Build cross-functional automations
- Ensure data consistency

**Content:**
1. **System Integration Architecture** (25 min)
   - Review all systems built:
     - Marketing (content, leads, campaigns)
     - Revenue (quotes, orders, payments, invoicing)
     - Operations (inventory, production, delivery, support)
   - Data flow mapping across systems
   - Integration points and dependencies
   - Master control workflows

2. **Building Master Workflows** (35 min)
   - Master workflow 1: New Customer Journey
     - Lead capture → Welcome sequence → First order → Production → Delivery → Feedback → Loyalty
   - Master workflow 2: Repeat Customer Order
     - Order → Payment → Inventory check → Production (if needed) → Delivery → Support follow-up
   - Master workflow 3: Daily Operations
     - Morning inventory check → Production planning → Marketing posts → Revenue summary → Support tickets review

3. **Data Consistency & Validation** (30 min)
   - Ensuring data integrity across tables
   - Validation workflows
   - Data reconciliation checks
   - Error detection and correction

**Live Demo:**
- Build master customer journey workflow
- Show data flowing across all systems
- Demonstrate validation checks
- Test end-to-end integration

**Student Practice:**
- Map complete customer lifecycle
- Identify integration points
- Test cross-system workflows

**Wednesday Practice Questions:**
1. What happens if payment fails after production starts?
2. How do you ensure inventory is never negative?
3. Where are the critical failure points in the system?

**Homework (Assigned Thursday):**
- Build master integration workflows:
  - Complete new customer journey (lead to loyal customer)
  - Complete order processing (order to delivery to feedback)
  - Daily operations orchestration
- Create system health check workflow:
  - Checks all critical workflows daily
  - Validates data consistency
  - Reports any issues
- Add system health section to dashboard:
  - Workflows status (running/failed)
  - Data consistency checks
  - System uptime
  - Error rate by workflow

---

#### Session 30 (Thu): Performance Optimization & Scaling

**Learning Objectives:**
- Optimize workflow performance
- Reduce API costs
- Prepare for scaling
- Implement caching strategies

**Content:**
1. **Performance Analysis** (25 min)
   - Workflow execution time tracking
   - API call volume and costs
   - Database query optimization
   - Bottleneck identification

2. **Optimization Techniques** (35 min)
   - Batching operations
   - Caching frequently accessed data
   - Parallel processing
   - Reducing unnecessary API calls
   - Database indexing
   - Conditional execution

3. **Scaling Preparation** (30 min)
   - Handling 10x order volume
   - Managing increased data
   - Rate limiting strategies
   - Infrastructure considerations
   - Cost projections at scale

**Live Demo:**
- Optimize slow workflow
- Implement caching
- Show parallel processing
- Demonstrate cost reduction

**Student Practice:**
- Analyze workflow performance
- Identify optimization opportunities
- Implement one optimization

**Homework (1 week):**
- Optimize all major workflows:
  - Reduce execution time by 30%
  - Implement caching where appropriate
  - Batch API calls
  - Optimize database queries
- Create performance dashboard:
  - Average workflow execution time
  - API costs breakdown
  - Most expensive workflows
  - Optimization impact tracking
- Document optimization strategies
- Calculate cost savings from optimizations

---

### **Week 16: Advanced Analytics & AI Insights**

#### Session 31 (Wed): Business Intelligence & Predictive Analytics

**Learning Objectives:**
- Build advanced analytics workflows
- Use AI for business insights
- Create predictive models
- Generate executive intelligence

**Content:**
1. **Advanced Analytics** (20 min)
   - Cohort analysis
   - Customer segmentation
   - RFM analysis (Recency, Frequency, Monetary)
   - Product affinity analysis
   - Churn prediction

2. **AI-Powered Insights** (40 min)
   - Using AI to analyze business data
   - Trend identification
   - Anomaly detection in business metrics
   - Automated insight generation
   - Natural language business queries
   - Example prompts:
     ```
     Analyze sales data and identify:
     1. Top growth opportunities
     2. Underperforming products
     3. Customer segments with highest potential
     4. Operational inefficiencies
     5. Revenue optimization recommendations
     
     Data: {sales_data, customer_data, operations_data}
     ```

3. **Predictive Analytics** (30 min)
   - Sales forecasting (simple trend-based)
   - Inventory demand prediction
   - Customer churn prediction
   - Cash flow forecasting

**Live Demo:**
- Build AI insights generation workflow
- Create RFM customer segmentation
- Show sales forecasting
- Generate executive summary with AI

**Student Practice:**
- Segment customers using RFM
- Generate AI insights from business data
- Create sales forecast

**Wednesday Practice Questions:**
1. Which customer segment should Ready Delight focus on?
2. What product should be promoted next month?
3. How can AI help with strategic decisions?

**Homework (Assigned Thursday):**
- Build advanced analytics system:
  - Customer segmentation (RFM analysis)
  - Product performance analysis
  - Sales forecasting workflow
  - Churn prediction workflow
  - AI-powered weekly business insights
- Create executive intelligence dashboard:
  - Key business insights (AI-generated)
  - Customer segments performance
  - Product recommendations
  - Revenue forecast
  - Growth opportunities
  - Risk alerts
- Generate monthly executive summary report (AI-assisted)

---

#### Session 32 (Thu): Automated Reporting & Decision Support

**Learning Objectives:**
- Build comprehensive reporting suite
- Create decision support workflows
- Implement alert systems
- Generate board-ready reports

**Content:**
1. **Report Types** (20 min)
   - Operational reports (daily)
   - Management reports (weekly)
   - Executive reports (monthly)
   - Board reports (quarterly)
   - Ad-hoc analysis reports

2. **Decision Support Systems** (35 min)
   - Scenario analysis automation
   - What-if calculations
   - Decision trees for common decisions
   - ROI calculators for decisions
   - Risk assessment automation

3. **Alert & Notification Intelligence** (35 min)
   - Smart alerting (avoid alert fatigue)
   - Priority-based notifications
   - Actionable alerts
   - Alert aggregation
   - Escalation workflows

**Live Demo:**
- Build comprehensive reporting system
- Create scenario analysis workflow
- Show intelligent alerting
- Generate board-ready report

**Student Practice:**
- Design executive report
- Create scenario analysis
- Set up intelligent alerts

**Homework (1 week):**
- Build complete reporting suite:
  - Daily operations report (automated email)
  - Weekly management report (PDF)
  - Monthly executive summary
  - Quarterly board report (comprehensive)
  - Ad-hoc analysis engine (AI-powered)
- Implement smart alerting:
  - Critical alerts (immediate Slack)
  - Important alerts (daily digest)
  - Informational alerts (weekly summary)
  - Alert priority logic
- Create final integrated dashboard:
  - All metrics from all phases
  - Interactive filters
  - Drill-down capabilities
  - Export functionality
  - Mobile-responsive design
- Document complete automation system

---

### **Week 17: Production Readiness & Documentation**

#### Session 33 (Wed): System Hardening & Security

**Learning Objectives:**
- Implement security best practices
- Add comprehensive error handling
- Create backup strategies
- Ensure system reliability

**Content:**
1. **Security Hardening** (30 min)
   - Securing API credentials
   - Input validation
   - Rate limiting
   - Access control
   - Data encryption
   - Compliance considerations (NDPR for Nigeria)

2. **Comprehensive Error Handling** (30 min)
   - Error handling patterns
   - Graceful degradation
   - Retry mechanisms
   - Circuit breakers
   - Error logging and monitoring

3. **Backup & Recovery** (30 min)
   - Database backup automation
   - Workflow backup
   - Disaster recovery plan
   - Testing recovery procedures
   - Business continuity planning

**Live Demo:**
- Implement security measures
- Add comprehensive error handling
- Set up automated backups
- Test recovery procedures

**Student Practice:**
- Add security to all workflows
- Implement error handling
- Configure backups

**Wednesday Practice Questions:**
1. What's the biggest security risk in the system?
2. How would you recover from database failure?
3. What compliance requirements apply to Ready Delight?

**Homework (Assigned Thursday):**
- Harden complete system:
  - Add input validation to all entry points
  - Implement comprehensive error handling
  - Set up automated daily backups
  - Create disaster recovery documentation
  - Test all error scenarios
  - Security audit of all workflows
- Create system documentation:
  - Architecture diagram
  - Data flow diagrams
  - Workflow documentation (all workflows)
  - API documentation
  - Database schema documentation
  - Deployment guide
  - Operations manual
  - Troubleshooting guide

---

#### Session 34 (Thu): Handoff & Maintenance Planning

**Learning Objectives:**
- Prepare system for handoff
- Create maintenance procedures
- Train end users
  - Plan for future enhancements

**Content:**
1. **System Handoff** (30 min)
   - Handoff documentation
   - User training materials
   - Administrator guide
   - Support procedures
   - SLA definitions

2. **Maintenance Planning** (30 min)
   - Daily maintenance tasks
   - Weekly checks
   - Monthly optimization
   - Update procedures
   - Monitoring and alerting

3. **Future Roadmap** (30 min)
   - Phase 2 enhancements
   - Additional integrations
   - Advanced features
   - Scaling considerations

**Live Demo:**
- Walk through complete system as end user
- Show maintenance procedures
- Demonstrate troubleshooting
- Present future roadmap

**Student Practice:**
- Create user training guide
- Document maintenance tasks
- Plan future enhancements

**Homework:**
- Complete all documentation:
  - User guide (for Ready Delight staff)
  - Administrator guide
  - Maintenance schedule
  - Troubleshooting guide
  - Future enhancement roadmap
- Finalize portfolio:
  - Professional case study
  - Complete documentation
  - Video walkthrough
  - GitHub repository
  - LinkedIn showcase

**Career Enablement:**
*This documentation is what separates professional from amateur. Clients pay premium for well-documented systems they can maintain. Your portfolio is now client-ready.*

---

### **Week 18: AI Agents & Autonomous Workflows**

#### Session 35 (Wed): Building Autonomous n8n Agents

**Learning Objectives:**
- Understand the difference between a triggered workflow and an autonomous agent
- Build a multi-step agent that monitors, decides, and acts without human input
- Use the AI Agent node in n8n with tool-calling

**Content:**
1. **What is an AI Agent?** (15 min)
   - Triggered workflow: runs when something happens, follows fixed steps
   - Agent: given a goal + tools, decides its own steps to achieve the goal
   - When agents are appropriate vs. overkill
   - n8n AI Agent node: connects an LLM to a set of tools (NocoDB, email, search)

2. **Building a Ready Delight Order Monitoring Agent** (50 min)
   - Schedule Trigger (every hour)
   - AI Agent node with goal: *"Check for orders placed in the last hour that have not been confirmed. For each, check inventory, send confirmation if stock is available, or flag for manual review if not."*
   - Tools available to the agent:
     - NocoDB tool: query Orders, query Products (inventory)
     - Email tool: send confirmation to customer
     - NocoDB tool: update order status
     - NocoDB tool: create an alert record if manual review needed
   - Memory node: retain context across the agent's reasoning steps
   - Testing: seed a pending order and watch the agent handle it

3. **Loop Until node** (25 min)
   - Polling pattern: keep checking a condition until it is true
   - Example: wait for a payment to be confirmed before dispatching order
   - Loop Until + Wait node for controlled retry with backoff

**Live Demo:**
- Build the order monitoring agent end-to-end
- Trigger manually with a test pending order
- Show the agent's reasoning in the execution log

**Student Practice:**
- Add a tool that lets the agent post a "sold out" notice to Instagram if stock is zero
- Test with a pending order for an out-of-stock product

**Wednesday Practice Questions:**
1. When would you use an agent vs. a fixed n8n workflow?
2. What risks does an autonomous agent introduce compared to a scripted workflow?
3. How would you prevent an agent from sending duplicate emails?

**Homework (Assigned Thursday):**
- Extend the monitoring agent to also handle: late delivery alerts (orders past estimated date with no delivery confirmation)
- Add a "Flagged for Review" NocoDB view that the agent populates
- Document: what tools did you give the agent, and why?

---

#### Session 36 (Thu): Agent Memory, Tool Chaining & Safety

**Learning Objectives:**
- Add memory to agents so context persists across runs
- Chain multiple agent calls for complex reasoning
- Implement guardrails to prevent unintended actions

**Content:**
1. **Agent Memory Strategies** (25 min)
   - In-workflow memory (within one execution): Memory node
   - Cross-run memory: store context in NocoDB; retrieve at start of next run
   - When memory matters: e.g. agent remembers which customers it already emailed today
   - Building a "Daily Context" table in NocoDB: date, actions_taken, summary

2. **Chained Agents** (35 min)
   - Agent 1 (Analyst): reads all orders and returns a structured summary JSON
   - Agent 2 (Action): reads the summary and decides what to do (reorder, notify, escalate)
   - Separating reasoning from action: safer and easier to debug
   - Using structured output mode: force the LLM to return valid JSON

3. **Safety Guardrails** (30 min)
   - Never let an agent delete records — read + create only
   - Require human confirmation before any outbound communication above a threshold
   - Logging every agent action to NocoDB for audit trail
   - Dead man's switch: if agent hasn't run in 24 hours, send alert

**Live Demo:**
- Chained analyst → action agent
- Show structured output parsing
- Demonstrate the NocoDB audit log

**Student Practice:**
- Add a safety rule: agent can only email a customer once per 24 hours
- Verify via the NocoDB log

**Homework (1 week):**
- Build a complete autonomous Ready Delight morning briefing:
  - Runs at 7 AM daily
  - Agent reads: yesterday's orders, current inventory, pending follow-ups
  - Produces a structured summary → sends WhatsApp/email briefing to CEO
  - Logs the summary to NocoDB
- Submit: workflow JSON, sample briefing output, NocoDB log screenshot

---

### **Week 19: Advanced Prompt Engineering & AI Pipelines**

#### Session 37 (Wed): Prompt Engineering for Production

**Learning Objectives:**
- Apply systematic prompt engineering to improve LLM output quality
- Use few-shot examples and structured output formats
- Build an AI content pipeline that produces consistent, on-brand output

**Content:**
1. **Prompt Engineering Principles** (20 min)
   - Role + task + context + format = good prompt
   - Zero-shot vs. few-shot: when examples matter
   - Chain-of-thought: ask the model to reason before answering
   - Temperature and top-p: controlling creativity vs. precision
   - When to use Gemini free tier vs. Claude (cost, quality trade-offs for Nigerian SME context)

2. **Few-Shot Content Templates for Ready Delight** (35 min)
   - Product description pipeline:
     - Input: product name, category, price, key features
     - Few-shot: 3 examples of great Ready Delight product descriptions
     - Structured output: `{"headline": "...", "body": "...", "hashtags": [...]}`
   - Customer follow-up pipeline:
     - Input: customer name, last order, days since purchase
     - Role: "You are the friendly customer relationship manager for Ready Delight..."
     - Output: personalised WhatsApp message (≤160 chars)
   - Rejection/complaint response pipeline:
     - Classify complaint type first → then generate appropriate response
     - Two-step chain: classifier → responder

3. **A/B Testing AI Outputs** (35 min)
   - Storing multiple prompt variants in NocoDB
   - Generating outputs from both → logging both → tracking which performs better
   - Simple version: rotate prompts weekly; compare engagement metrics

**Live Demo:**
- Build the product description pipeline with few-shot examples
- Show structured output parsing
- A/B test two prompt styles for the same product

**Student Practice:**
- Write a few-shot prompt for a customer re-engagement message
- Test with 5 real customers from NocoDB; review outputs for quality

**Wednesday Practice Questions:**
1. When does few-shot prompting significantly outperform zero-shot?
2. How do you prevent an LLM from hallucinating product details it wasn't given?
3. What would you log to track whether AI-generated content is driving sales?

**Homework (Assigned Thursday):**
- Build a content quality pipeline:
  - Generate description → evaluate with a second LLM call (score 1-10, flag if < 7)
  - Store all outputs + scores in NocoDB Content_Library table
  - Only post content that scores ≥ 7 to social media
- Submit: workflow JSON, 10 sample outputs with scores

---

#### Session 38 (Thu): Document Processing & RAG Basics

**Learning Objectives:**
- Extract structured data from unstructured documents using LLMs
- Understand Retrieval-Augmented Generation (RAG) at a conceptual and practical level
- Build a simple supplier invoice processor for Ready Delight

**Content:**
1. **Document Processing with LLMs** (25 min)
   - Use cases: invoice extraction, order form parsing, complaint classification
   - Sending document text to an LLM: extract fields as JSON
   - Handling variability (different supplier invoice formats)
   - Validation: cross-check extracted values against NocoDB

2. **Supplier Invoice Processor** (35 min)
   - Trigger: email arrives with PDF attachment (Gmail trigger node)
   - Extract text from PDF (n8n Extract from File node)
   - LLM call: "Extract: supplier_name, invoice_number, date, line_items[{product, quantity, unit_price}], total"
   - Parse JSON response → create Inventory_Transaction record in NocoDB
   - Flag for manual review if confidence is low (missing fields)

3. **RAG Concepts for Business** (30 min)
   - What RAG is: LLM answers questions using *your* documents, not just training data
   - Practical Ready Delight application: a chatbot that answers "What products do we have in stock?" or "What was the last order from customer X?"
   - Simple RAG without a vector database: retrieve relevant NocoDB records → inject into prompt context
   - When a full vector database (Pinecone, Weaviate) is needed vs. context injection

**Live Demo:**
- Build the invoice processor end-to-end
- Test with a sample PDF invoice
- Show the NocoDB Inventory_Transaction record created automatically

**Student Practice:**
- Extend the invoice processor: if extracted total > ₦50,000, send approval request to CEO before logging
- Test with two sample invoices (one above threshold, one below)

**Homework (1 week):**
- Build a simple product Q&A over NocoDB:
  - Trigger: WhatsApp message received (or manual trigger for testing)
  - Fetch relevant products from NocoDB → inject into prompt
  - LLM answers the question using only the provided data
  - Reply via WhatsApp/email
- Module 5 Demo Day prep: prepare 8-minute cluster presentation

---

# Module 6: Client-Facing Deliverables
## Weeks 20-21 (4 Sessions)

### **Week 20: Customer-Facing Order Form & Intake Automation**

#### Session 39 (Wed): Building a Public-Facing Order Form with AI Tools

**Learning Objectives:**
- Build a customer-facing order form using AI coding tools
- Connect the form to n8n via webhook
- Trigger a full order creation workflow from a form submission

**Content:**
1. **AI Coding Tools for Frontend** (15 min)
   - v0.dev: generate HTML/React components from a text description
   - Bolt.new: full-stack instant prototypes
   - Cursor: AI pair programming for editing generated code
   - The goal here is not to become a web developer — it is to build a good-enough customer interface that connects to the automation system already built

2. **Building the Ready Delight Order Form** (45 min)
   - Use v0.dev to generate: product selector (dropdown from a static list), quantity, customer name, phone number, delivery address, submit button
   - Style for Nigerian mobile users: large touch targets, minimal images, fast load
   - Form action: POST to n8n Webhook trigger URL
   - n8n webhook workflow receives the submission:
     - Validate required fields (IF node)
     - Check inventory in NocoDB — is the product in stock?
     - Create Order record + Order_Items in NocoDB
     - Send order confirmation SMS/WhatsApp to customer
     - Send internal alert to CEO
   - Deploy form to Vercel or GitHub Pages (static HTML, no server needed)
   - Test end-to-end: submit form → NocoDB order created → confirmation sent

3. **Handling Form Errors Gracefully** (30 min)
   - What happens when the webhook fails? Add a fallback response
   - Show user a success or error message based on n8n response
   - Log all form submissions to NocoDB regardless of outcome (for audit)

**Live Demo:**
- v0.dev → generate order form HTML
- Connect to n8n webhook
- Submit test order → watch NocoDB record appear + confirmation message fire

**Student Practice:**
- Add a "Special Instructions" text field
- Update the n8n workflow to include special instructions in the CEO alert

**Wednesday Practice Questions:**
1. What is the security risk of exposing an n8n webhook URL in a public form? How do you mitigate it?
2. What happens to a form submission if the customer's internet drops mid-send?
3. How would you add a WhatsApp "Order via WhatsApp" fallback button?

**Homework (Assigned Thursday):**
- Deploy the complete order form:
  - Products populated from NocoDB via API call (not a static list)
  - Price auto-calculated client-side as user selects quantity
  - n8n workflow creates order + confirmation + CEO alert
  - Error message if NocoDB is unreachable
- Submit: deployed URL + NocoDB screenshot showing test order created

---

#### Session 40 (Thu): Connecting Automation Outputs to the Customer

**Learning Objectives:**
- Build an order status lookup page so customers can self-serve
- Send automated status updates at key order milestones
- Understand the full customer journey from form submission to delivery

**Content:**
1. **Order Status Page** (35 min)
   - Simple HTML page with an order ID input field
   - On submit: call NocoDB API (`GET /Orders?where=(order_id,eq,{id})`)
   - Display: order status, items, estimated delivery, confirmation number
   - Deploy alongside the order form (same static hosting)
   - This requires NO authentication — just the order ID (like tracking a courier)

2. **Automated Status Update Workflow** (30 min)
   - n8n Schedule Trigger (every 2 hours)
   - Query NocoDB for orders where status changed since last run
   - For each changed order: send WhatsApp/SMS with new status
   - Milestones to notify: Confirmed → Being Prepared → Out for Delivery → Delivered
   - Update `last_notified_status` field in NocoDB to avoid duplicate messages

3. **Closing the Loop: the Full Ready Delight Customer Journey** (25 min)
   - Walk through the complete automated flow end-to-end:
     1. Customer fills order form (Module 6 Wed)
     2. Order created in NocoDB; confirmation sent (Module 6 Wed)
     3. CEO sees alert; updates order status (existing UI)
     4. Customer receives status updates automatically (Module 6 Thu)
     5. Customer checks status page anytime (Module 6 Thu)
     6. After delivery: automated review request (Module 3)
     7. Review data feeds the Streamlit dashboard (Module 1)
   - This is the automation system students have built across 20 weeks, shown as a single coherent story

**Live Demo:**
- Build order status page
- Submit a test order → manually update status in NocoDB → customer receives WhatsApp update → status page reflects new state

**Student Practice:**
- Add a "request re-order" button on the status page that pre-fills the order form
- Test the full end-to-end journey as a customer

**Homework (1 week):**
- Complete the full customer-facing layer:
  - Order form (deployed, connected to n8n)
  - Order status page (deployed, reads from NocoDB)
  - Automated status update workflow (running on schedule)
  - Review request workflow triggers after delivery (connect to Module 3 work)
- Record a 2-minute screen-walk of the full customer journey — from order to status check to review request
- Submit: deployed URLs + recording

**Career Enablement:**
*This is the most visible part of the automation system — what customers actually touch. Being able to build this customer-facing layer, connected to a full backend automation, is what separates automation consultants from automation beginners. Practice pitch: "I build the complete customer journey: form → confirmation → tracking → review — all automated."*

---

### **Week 21: Embedded Dashboard & System Polish**

#### Session 41 (Wed): Embedding the Streamlit Dashboard & Final System Integration

**Learning Objectives:**
- Make the Streamlit dashboard accessible to non-technical stakeholders
- Verify all automation system components work together end-to-end
- Identify and fix remaining integration gaps before capstone

**Content:**
1. **Embedding the Streamlit Dashboard** (25 min)
   - Options for sharing with non-technical users:
     - Streamlit Community Cloud URL (already done in Module 1)
     - Embed in a simple internal webpage using an `<iframe>`
     - Password-protect via Streamlit's built-in auth or a simple n8n-verified token
   - Add a "Management Dashboard" link to the CEO alert emails from n8n
   - Use AI tools (v0.dev) to generate a simple internal portal page that links to: the order form, the status page, and the embedded dashboard in one place

2. **System Integration Audit** (40 min)
   - Students map out every workflow they have built (list in NocoDB or a shared doc)
   - For each workflow: Is it running? Is error handling in place? Is it logged?
   - Common gaps to check: Module 2 social posts still running? Module 3 invoice processor tested with real data? Module 4 inventory alerts triggered correctly?
   - Pair audit: swap workflows with another cluster; each cluster reviews the other's error handling

3. **Performance & Reliability Review** (25 min)
   - Review execution history in n8n: any failures in the last 2 weeks?
   - NocoDB data quality: any malformed records from automation?
   - Streamlit dashboard: does it still load within 5 seconds?

**Student Practice:**
- Fix the top-priority integration gap identified in the audit
- Add the dashboard link to one existing n8n notification workflow

**Wednesday Practice Questions:**
1. A client asks: "How do I know the automation is still running?" What do you show them?
2. What would break first if NocoDB went down for an hour?
3. How would you explain the value of this system to a non-technical investor in 60 seconds?

**Homework (Assigned Thursday):**
- Complete the integration audit; fix all critical gaps
- Write a one-page system overview (what each module does, what tools it uses)
- This document will form part of the Module 7 capstone documentation

---

#### Session 42 (Thu): Module 6 Demo Day

**Format:**
- Each cluster demonstrates the complete customer journey (order form → status page → dashboard) — 10 minutes per cluster
- Instructor runs a "stress test": submit 3 simultaneous orders during the demo; does the system handle it?
- Peer feedback on user experience: is the order form clear? Is the status page useful?
- Instructor feedback: system resilience, code quality, documentation
- Capstone project briefing: what Module 7 requires (full system + new business, not Ready Delight)

**Presentation Requirements:**
- Live demo of order form → NocoDB → confirmation (not slides)
- Show order status page with a real order
- Show Streamlit dashboard with live data
- Walk through one workflow's error handling

**Homework:**
- Polish any remaining gaps before Module 7
- Begin thinking about your capstone business: a different Nigerian SME that you will automate from scratch

**Career Enablement:**
*You have now built a complete automation system for a real business — visible to customers, connected end-to-end, deployed in production. This is a portfolio piece. Record a 5-minute walkthrough and post it.*

---

# Module 7: Capstone Project
## Weeks 22-24 (6 Sessions)

### **Week 22: Productionization & Documentation**

#### Session 43 (Wed): System Productionization

**Learning Objectives:**
- Prepare Ready Delight system for production use
- Implement monitoring and alerting
- Create operational procedures
- Train end users

**Content:**
1. **Production Readiness** (30 min)
   - Final system audit
   - Performance verification
   - Security check
   - Data validation
   - Backup verification

2. **Monitoring & Alerting** (30 min)
   - System health dashboard
   - Uptime monitoring
   - Error rate tracking
   - Performance metrics
   - Alert configuration

3. **User Training** (30 min)
   - Creating training materials
   - Video tutorials
   - User documentation
   - FAQ documentation
   - Support procedures

**Live Demo:**
- Complete production setup
- Configure monitoring
- Create training video
- Demonstrate system to "CEO"

**Student Practice:**
- Audit your system
- Set up monitoring
- Create user guide

**Wednesday Practice Questions:**
1. How would you train a non-technical person to use the system?
2. What's the most critical monitoring alert?
3. How do you ensure business continuity?

**Homework (Assigned Thursday):**
- Productionize Ready Delight system:
  - Complete security audit
  - Set up comprehensive monitoring
  - Create all user documentation
  - Create video tutorials (3-5 videos)
  - Prepare training presentation
- Create handoff package:
  - System documentation
  - User guides
  - Training materials
  - Maintenance procedures
  - Support contacts
- Present to "Ready Delight CEO" (role play with instructor/peer)

---

#### Session 44 (Thu): Capstone Project Kickoff

**Learning Objectives:**
- Define individual capstone project
- Plan project scope and timeline
- Create project proposal
- Begin project work

**Content:**
1. **Capstone Project Requirements** (20 min)
   - Choose your own business/client to automate
   - Must include elements from all 4 phases:
     - Marketing automation
     - Revenue operations
     - Business operations
     - Website integration
   - Real or realistic business case
   - Deliverables:
     - Complete automation system
     - Website
     - Dashboard
     - Documentation
     - Presentation

2. **Project Planning** (40 min)
   - Business selection criteria
   - Scope definition
   - Technology stack
   - Timeline (2 weeks)
   - Deliverable checklist

3. **Project Proposal** (30 min)
   - Business overview
   - Current state analysis
   - Proposed automation
   - Expected impact/ROI
   - Implementation plan

**Live Demo:**
- Example capstone project proposal
- Project planning template
- Resource allocation

**Student Practice:**
- Select business for capstone
- Draft project proposal
- Create implementation plan

**Homework:**
- Submit detailed capstone project proposal:
  - Business description and context
  - Current processes (manual state)
  - Proposed automation scope
  - Technology stack
  - Data model design
  - Workflow architecture
  - Expected impact and ROI
  - 2-week timeline
  - Risk assessment
- Get proposal approved
- Begin project work

**Career Enablement:**
*This capstone is your portfolio centerpiece. Choose wisely - ideally a business in your network that might actually use it, creating a reference client for freelancing.*

---

### **Week 23: Capstone Project Development**

#### Session 45 (Wed): Mid-Project Review & Support

**Learning Objectives:**
- Present project progress
- Get feedback and guidance
- Troubleshoot issues
- Refine implementation

**Format:**
- Individual/cluster presentations (10 min each)
- Show current progress
- Discuss challenges
- Get instructor feedback
- Peer learning and collaboration

**Content:**
Students should have completed (or be near completion):
- Database design and setup
- Core workflows (at least 50% complete)
- Basic dashboard
- Initial website (if applicable)

**Student Practice:**
- Present progress
- Demonstrate working features
- Get feedback
- Refine approach

**Wednesday Practice Questions:**
1. What's your biggest technical challenge?
2. What have you learned that wasn't in Ready Delight project?
3. How are you tracking impact/ROI?

**Homework:**
- Continue capstone development
- Address feedback from mid-project review
- Complete all core workflows
- Build comprehensive dashboard
- Begin documentation

---

#### Session 46 (Thu): Project Development & Documentation

**Learning Objectives:**
- Complete all automation workflows
- Finalize dashboard
- Complete documentation
- Prepare for final presentation

**Format:**
- Working session with instructor support
- Troubleshooting help
- Code review
- Documentation guidance

**Content:**
Students should complete:
- All workflows functional
- Dashboard comprehensive
- Website integrated (if included)
- Documentation drafted

**Student Practice:**
- Finalize all features
- Complete documentation
- Test everything
- Prepare demo

**Homework:**
- Complete entire capstone project:
  - All workflows working
  - Dashboard finalized
  - Website deployed (if included)
  - Complete documentation
  - Video demo recorded
  - Presentation prepared
- Conduct end-to-end testing
- Fix all bugs
- Prepare 15-minute presentation

**Career Enablement:**
*Focus on quantifiable results. Calculate: hours saved, revenue impact, error reduction, cost savings. These numbers sell your services.*

---

### **Week 24: Final Presentations & Course Conclusion**

#### Session 47 (Wed): **FINAL CAPSTONE PRESENTATIONS - Part 1**

**Format:**
- Professional presentations (15 min each + 5 min Q&A)
- Live system demonstrations
- ROI presentation
- Portfolio showcase

**Presentation Requirements:**
1. Business Context (2 min)
   - What business/client
   - Current challenges
   - Opportunity for automation

2. Solution Overview (3 min)
   - Automation architecture
   - Key workflows
   - Technology stack

3. Live Demonstration (8 min)
   - Show working system
   - Walk through end-to-end process
   - Highlight innovative features

4. Impact & Results (2 min)
   - Quantified ROI
   - Time savings
   - Error reduction
   - Other benefits

**Assessment Criteria:**
- Technical implementation (40%)
- Business impact (25%)
- Presentation quality (15%)
- Documentation (10%)
- Innovation (10%)

---

#### Session 48 (Thu): **FINAL CAPSTONE PRESENTATIONS - Part 2 & Course Conclusion**

**Format:**
- Continuation of presentations
- Peer recognition awards
- Instructor final feedback
- Course celebration and next steps

**Presentations:** (First half)
- Remaining student presentations
- Same format as Session 47

**Course Conclusion:** (Second half)

1. **Recognition & Awards** (20 min)
   - Best Technical Implementation
   - Best Business Impact
   - Most Innovative Solution
   - Best Presentation
   - Best Documentation

2. **Reflection & Learning** (20 min)
   - What did we accomplish?
   - From Excel to AI Automation in 6 months
   - Key skills acquired
   - Career transformation

3. **Next Steps & Career Guidance** (20 min)
   - **For Freelancers:**
     - Building client portfolio
     - Pricing your services
     - Marketing yourself
     - First client acquisition
   
   - **For Job Creators:**
     - Starting automation agency
     - Building team
     - Scaling operations
     - Business registration
   
   - **For Role Enhancers:**
     - Presenting to management
     - Internal pilot projects
     - Building internal capability
     - Career advancement

4. **Staying Connected** (10 min)
   - PORA Academy alumni network
   - Continued learning resources
   - Community support
   - Advanced courses

5. **Celebration** (20 min)
   - Course completion
   - Portfolio showcase
   - LinkedIn profile updates
   - Group photo/celebration

**Final Homework:**
- Update LinkedIn profile completely
- Publish capstone case study
- Connect with all cohort members
- Share course completion on social media
- Begin client outreach (freelancers)
- Apply for automation roles (job seekers)
- Implement in current role (enhancers)

---

# ASSESSMENT & GRADING

## Overall Assessment Structure

**Demo Days (40%)**
- Demo Day 1 (Foundations): 10%
- Demo Day 2 (Marketing): 10%
- Demo Day 3 (Revenue): 10%
- Demo Day 4 (Operations): 10%

**Weekly Homework (30%)**
- Completion and quality of assignments
- NocoDB database quality
- Workflow functionality
- Dashboard development
- Documentation

**Capstone Project (30%)**
- Technical implementation: 12%
- Business impact/ROI: 9%
- Presentation: 5%
- Documentation: 4%

## Grading Criteria

**A (90-100%):** Exceptional work, innovative solutions, comprehensive documentation, strong business impact
**B (80-89%):** Good work, functional solutions, adequate documentation, measurable impact  
**C (70-79%):** Satisfactory work, basic functionality, minimal documentation
**Below 70%:** Needs improvement

## Requirements for Completion

- Attend 80% of sessions minimum
- Complete all Demo Day presentations
- Submit 80% of weekly homework
- Complete and present capstone project
- Maintain GitHub repository with all work

---

# RESOURCES & TOOLS

## Required Tools (All Free/Freemium)

**Infrastructure:**
- n8n (shared instance on instructor's Coolify)
- NocoDB (shared instance on instructor's Coolify)
- Google Account (for Sheets, Drive, Gmail)

**Development:**
- v0.dev account (free tier)
- Cursor or VS Code (free)
- GitHub account (free)

**AI Services:**
- Gemini API (free tier)
- Claude API (optional, free tier available)

**Optional:**
- Slack workspace (for notifications)
- Paystack/Flutterwave test account
- WhatsApp Business API (via third-party free trial)

## Learning Resources

**Documentation:**
- n8n documentation: docs.n8n.io
- NocoDB documentation: docs.nocodb.com
- Streamlit documentation: docs.streamlit.io

**Sample Data:**
- Ready Delight datasets (provided)
- Nigerian business data templates
- Sample workflow templates

---

# SUPPORT STRUCTURE

## During Course

**Live Sessions:**
- Wednesday & Thursday, 90 minutes
- Live Q&A during sessions
- Instructor demonstrations

**Between Sessions:**
- Cluster peer support (encouraged)
- Shared resources in course portal
- Email support for urgent issues

**Monthly Demo Days:**
- Peer feedback
- Instructor feedback
- Collaborative learning

## Post-Course

**Alumni Network:**
- PORA Academy alumni community
- Continued peer support
- Job/client sharing

**Continued Learning:**
- Advanced courses (if developed)
- Updated materials and templates
- Industry trends sharing

---

# SUCCESS METRICS

## Student Success Indicators

**Technical Skills:**
- ✓ Build databases from scratch (NocoDB)
- ✓ Create complex n8n workflows
- ✓ Integrate APIs (Gemini, payment gateways, social media)
- ✓ Build Streamlit dashboards
- ✓ Use AI for content and insights
- ✓ Build websites with AI coding tools
- ✓ Deploy to production

**Business Skills:**
- ✓ Analyze processes for automation
- ✓ Calculate ROI
- ✓ Document systems professionally
- ✓ Present to stakeholders
- ✓ Manage projects

**Career Outcomes:**
- 🎯 Freelancing: Land 3+ paying clients within 3 months
- 🎯 Job Creation: Launch automation agency
- 🎯 Role Enhancement: Implement automation in current job

## Course Success Metrics

- 80%+ completion rate
- 90%+ student satisfaction
- 70%+ students achieve career outcome within 6 months
- Average ROI for automated businesses: 5x+

---

*This curriculum transforms data analysts into AI automation experts through hands-on learning with a real Nigerian business case. By the end, students have a complete portfolio and the skills to automate any business.*

**Course Version:** 1.0
**Created:** December 2024
**Target Start:** Q1 2025
