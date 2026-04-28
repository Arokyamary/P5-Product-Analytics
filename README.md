# Product Analytics & A/B Testing Intelligence Platform

An end-to-end product analytics platform built with Bayesian A/B testing,
funnel analysis, cohort retention, and an interactive Plotly Dash dashboard
deployed on Render.

**Live Demo:** https://p5-product-analytics.onrender.com

---

## Project Overview

This project simulates a real-world product analytics scenario where two
variants (A and B) of a product feature are tested against 50,000 users
to determine which converts better using Bayesian statistical inference.

The dataset is synthetic event-level data with 50,000 observations generated
to replicate realistic user behavior across a 5-step conversion funnel.

---

## Key Results

| Metric | Value |
|---|---|
| Total Users | 50,000 |
| Total Events | 121,000+ |
| Overall Conversion Rate | 7.0% |
| Control A CVR | 5.9% |
| Variant B CVR | 8.1% |
| Lift (B vs A) | +37.3% |
| Probability Variant B Wins | 97.2% |
| Statistical Significance | p = 0.03 |
| Est. Revenue Lift/Month | ₹4,95,394 |
| Decision | Ship Variant B |

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data generation, modeling |
| PostgreSQL | Events and users storage |
| PyMC | Bayesian A/B testing |
| Plotly Dash | Interactive dashboard |
| SQLAlchemy | Database connection |
| Faker | Synthetic data generation |
| Render | Cloud deployment |

---

## Project Architecture

```
P5_ProductAnalytics/
├── data/
│   ├── users.csv
│   └── events.csv
├── sql/
│   └── funnel_queries.sql
├── generate_events.py
├── load_to_postgres.py
├── bayesian_ab.py
├── app.py
└── requirements.txt

```

---

## How It Works

### Phase 1 — Data Generation
- Created 50,000 synthetic users assigned to Control A or Variant B
- Simulated 5-step user journey: Landing → Product View → Cart → Checkout → Purchase
- Variant B intentionally set with higher conversion rate to demonstrate statistical signal

### Phase 2 — PostgreSQL + SQL Analysis
- Stored events and users data in PostgreSQL
- Built 5-step funnel SQL query to measure dropoff at each stage
- Built week-over-week cohort retention query using window functions

### Phase 3 — Bayesian A/B Testing
- Used PyMC to model conversion rates as Beta distributions
- Ran 4,000 MCMC samples across 2 chains
- Calculated P(B > A) = 97.2% → confident decision to ship Variant B
- p-value = 0.03 confirms statistical significance

### Phase 4 — Plotly Dash Dashboard
- KPI cards: Total Users, CVR, Lift, Probability B Wins, p-value, Revenue Lift
- 5-Step Conversion Funnel with drop-off rates at each stage
- Device Split bar chart showing Traffic % vs CVR % per device

### Phase 5 — Deployment
- Deployed on Render.com as a live web service
- Accessible at: https://p5-product-analytics.onrender.com

---

## Funnel Analysis

| Step | Control A | Variant B | Drop-off |
|---|---|---|---|
| Landing | 25,000 | 25,000 | - |
| Product View | 16,200 | 16,300 | 35% |
| Cart | 6,500 | 6,520 | 60% |
| Checkout | 1,940 | 1,960 | 70% |
| Purchase | 1,477 | 2,021 | - |

---

## Device Analysis

| Device | Traffic % | CVR % |
|---|---|---|
| Mobile | 65% | ~7% |
| Desktop | 30% | ~7% |
| Tablet | 5% | ~7% |

---

## Setup & Installation

```bash
# Clone the repository
git clone https://github.com/Arokyamary/P5-Product-Analytics.git
cd P5-Product-Analytics

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate data
python generate_events.py

# Load to PostgreSQL
python load_to_postgres.py

# Run Bayesian A/B test
python bayesian_ab.py

# Launch dashboard
python app.py
```

---

## Key Learnings

- Bayesian A/B testing gives probability estimates, not just p-values
- Funnel analysis reveals exactly where users drop off in the journey
- Cohort retention shows how well a product retains users week over week
- PostgreSQL window functions are powerful for retention analysis
- 65% of users are on mobile — mobile-first UI is critical
