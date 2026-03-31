# 📊 Sales Analysis — Superstore Dataset

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-16A34A?style=flat)

> End-to-end sales analysis covering revenue trends, product performance,
> regional breakdowns, and discount impact — built with SQL and Python.

---

## 🎯 Business Problem

1. Where is revenue growing or declining?
2. Which products and categories are most profitable?
3. Which regions are underperforming?
4. How is discounting affecting the bottom line?

---

## 📁 Project Structure
```
sales-analysis/
├── data/
│   └── superstore.csv
├── sql/
│   └── sales_analysis.sql
├── notebooks/
│   └── sales_analysis.py
├── outputs/
│   ├── 01_revenue_trend.png
│   ├── 02_category_performance.png
│   ├── 03_regional_analysis.png
│   ├── 04_segment_analysis.png
│   └── 05_discount_impact.png
└── README.md
```

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| SQL | Data extraction and aggregations |
| Python — pandas | Data cleaning and analysis |
| Python — matplotlib, seaborn | Charts and visualizations |

---

## 💡 Key Insights

| # | Insight |
|---|---------|
| 1 | Technology has highest revenue but Office Supplies has best margin |
| 2 | Tables and Bookcases are loss-making due to heavy discounting |
| 3 | West region leads revenue — Central has lowest margin |
| 4 | Orders with more than 30% discount generate negative profit on average |
| 5 | Corporate segment has highest revenue per customer |

---

## ▶️ How to Run
```bash
pip install pandas matplotlib seaborn
python notebooks/sales_analysis.py
```

---
## 📋 Business Recommendations

Based on the analysis, here are five concrete actions I would recommend to the business:

| # | Finding | Recommendation | Expected Impact |
|---|---------|---------------|-----------------|
| 1 | Tables and Bookcases have negative profit margins due to 35%+ average discounts | Cap discounts at 15% for furniture sub-categories immediately | Recover an estimated $50K+ in annual profit |
| 2 | Central region has the lowest profit margin despite decent revenue | Audit Central region's discounting practices and sales team incentives | Align Central margins with West region benchmark |
| 3 | Orders with more than 30% discount generate negative profit on average | Introduce discount approval workflow for anything above 20% | Reduce margin erosion across all categories |
| 4 | Corporate segment has the highest revenue per customer | Prioritise Corporate account retention — assign dedicated account managers | Protect the highest-value customer segment |
| 5 | Office Supplies has the best profit margin but lowest revenue share | Increase marketing spend on Office Supplies — high margin, room to grow | Improve overall portfolio profitability |

### Key Metric to Watch
If discount cap recommendation is implemented, the overall profit margin is projected to improve from **12% to approximately 17-18%** based on current order distribution.

## 🤝 Connect

- LinkedIn: [your-linkedin-url]
- Email: [your-email]