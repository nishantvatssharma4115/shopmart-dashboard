# 🛒 ShopSmart E-Commerce Sales Dashboard

> **A complete end-to-end data analytics portfolio project** — from synthetic data generation and SQL-based business intelligence to interactive visualisations and a browser-ready analytics dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=flat&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![Chart.js](https://img.shields.io/badge/Chart.js-4.x-FF6384?style=flat&logo=chartdotjs&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Offline_Dashboard-E34F26?style=flat&logo=html5&logoColor=white)

---

## 📌 Project Description

This project simulates a real-world e-commerce analytics pipeline for a fictional retail brand, **ShopSmart**, covering the full data lifecycle — generation, cleaning, SQL analysis, and visual storytelling. A dataset of **300 realistic sales transactions** across regions, product categories, and customer segments is programmatically generated and analysed to surface actionable business insights. The findings are presented through a **professional offline analytics dashboard** built with HTML and Chart.js — ready to deploy or screenshot for a portfolio.

---

## 🧩 The Business Problem

E-commerce companies collect thousands of orders every day but often struggle to turn raw transactional data into clear, decision-ready insights. Business stakeholders need answers to questions like:

- *Which product categories are driving the most revenue?*
- *Which months experience sales slumps — and why?*
- *Are our discounts actually improving order volumes, or just eroding margins?*
- *Where are our VIP customers, and how loyal are they?*

This project addresses those questions by building a complete analytics pipeline from scratch — **no external datasets required**.

---

## 🛠️ Tools & Technologies

| Layer | Technology | Purpose |
|---|---|---|
| **Data Generation** | Python · NumPy · Random | Synthetic dataset creation with realistic distributions |
| **Data Wrangling** | Pandas | Cleaning, type-fixing, deduplication, feature engineering |
| **Database Layer** | SQLite (sqlite3) | Persistent storage + 5 business SQL queries |
| **Statistical Viz** | Matplotlib · Seaborn | 6 publication-quality chart PNGs |
| **Dashboard** | HTML · CSS · Chart.js | Offline-ready interactive analytics dashboard |

---

## 📊 Dataset Overview

| Column | Type | Description |
|---|---|---|
| `Order ID` | String | Unique order identifier (ORD-0001 → ORD-0300) |
| `Date` | datetime64 | Random date between Jan–Dec 2023 |
| `Region` | Category | North · South · East · West |
| `Product Category` | Category | Electronics · Clothing · Food · Beauty · Sports |
| `Product Name` | Category | 5 products per category |
| `Units Sold` | int64 | 1 – 50 units per order |
| `Unit Price` | float64 | ₹5 – ₹999 per unit |
| `Discount Percent` | float64 | 0% – 40% |
| `Customer Segment` | Category | New · Returning · VIP |
| `Total Revenue` | float64 | Units × Price × (1 − Discount/100) |

---

## 🔍 Key Business Insights

1. **📦 Electronics leads revenue despite equal order volumes** — with ₹5,82,340 in total revenue, Electronics outperforms other categories primarily due to high-ticket SKUs like Laptops and Smartphones. Targeted upselling here can significantly improve average order value.

2. **📅 February and September are peak revenue months** — contributing over 21% of annual revenue combined. These spikes align with seasonal demand; stocking up and running targeted campaigns before these months is critical for revenue maximisation.

3. **👥 Returning customers (36.7%) and VIP customers (35.7%) dominate orders** — together accounting for 72.4% of all transactions. This signals strong retention but highlights a growth opportunity in new customer acquisition through referral programmes or first-order discounts.

4. **🗺️ The North region carries the highest average discount rate (20.89%)** — exceeding other regions by up to 2.95 percentage points. Without a corresponding boost in volume, this suggests margin leakage that warrants a regional pricing policy review.

5. **📉 November is the weakest month with only ₹1,05,200 in revenue** — a 70% drop from the February peak. Introducing flash sales, loyalty reward events, or curated gift bundles in October–November could effectively smoothen the seasonal revenue curve.

---

## 📁 File Structure

```
DVA_project_portfolio/
│
├── generate_data.py           # Main Python script (542 lines, fully commented)
│   ├── Section 1–9  →         Data generation (NumPy, Pandas, Random)
│   ├── Section 10   →         Data cleaning (nulls, dupes, dtypes, Total Revenue)
│   ├── Section 11   →         SQLite database + 5 business SQL queries
│   └── Section 12   →         6 Matplotlib/Seaborn charts saved as PNG
│
├── dashboard.html             # Standalone offline analytics dashboard
│   ├── Dark professional theme with sticky navbar
│   ├── 4 animated KPI cards
│   ├── 6 interactive Chart.js charts
│   └── Key Business Insights + Footer
│
├── ecommerce_sales_data.csv   # Cleaned dataset (300 rows × 10 columns)
├── shopmart.db                # SQLite database with 'sales' table
│
├── chart1.png                 # Bar  — Revenue by Product Category
├── chart2.png                 # Line — Monthly Revenue Trend
├── chart3.png                 # Pie  — Orders by Customer Segment
├── chart4.png                 # Box  — Unit Price Distribution by Category
├── chart5.png                 # Heat — Metric Correlation Heatmap
└── chart6.png                 # Bar  — Orders by Region
```

---

## ✅ Skills Demonstrated

| Skill | What was done |
|---|---|
| 🧹 **Data Cleaning** | Handled injected missing values with category-median imputation; removed duplicate rows; fixed data types including datetime conversion |
| 🔬 **Exploratory Data Analysis** | Used `df.describe()`, `.dtypes`, `.isnull()` checks; computed grouped aggregations to understand distributions |
| 🗄️ **SQL Queries** | Wrote 5 business-focused queries in SQLite covering GROUP BY, ORDER BY, LIMIT, STRFTIME for time-series analysis, and AVG/SUM aggregations |
| 📊 **Data Visualisation** | Created 6 chart types (bar, line, pie, boxplot, heatmap, countplot) using Matplotlib and Seaborn with professional formatting |
| 🖥️ **Dashboard Design** | Designed and built a fully offline HTML dashboard with Chart.js, glassmorphism-inspired cards, responsive grid layout, and analyst-level insight writing |

---

## 🚀 How to Run

**Prerequisites:** Python 3.10+, with the following libraries installed:
```bash
pip install pandas numpy matplotlib seaborn
```

**Run the pipeline:**
```bash
python generate_data.py
```

This will generate `ecommerce_sales_data.csv`, `shopmart.db`, and all 6 chart PNGs.

**View the dashboard:**
```bash
# Simply double-click dashboard.html in your file explorer
# or open it from terminal:
open dashboard.html          # macOS
start dashboard.html         # Windows
```
> ⚠️ Requires an internet connection on first load for Chart.js CDN. Once cached, it works fully offline.

---

## 👤 Author

**Nishant Sharma**
Data Visualisation & Analytics · Rishihood University · 2025–26

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-181717?style=flat&logo=github)](https://github.com)

---

*Built by **Nishant Sharma** as part of the Data Visualisation & Analytics coursework to demonstrate a complete, industry-relevant analytics workflow.*
