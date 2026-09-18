# Customer Churn Prediction & Retention Analytics

![Interactive Dashboard Preview](https://img.shields.io/badge/Live_Dashboard-Interactive_HTML-06B6D4?style=for-the-badge&logo=powerbi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit_Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Analytics-CC292B?style=for-the-badge&logo=sqlite&logoColor=white)

An end-to-end Data Analyst portfolio case study addressing customer attrition for a prominent Indian retail bank. This project demonstrates data engineering, statistical hypothesis testing, analytical SQL querying, machine learning classification with class imbalance treatment (SMOTE), and executive business intelligence dashboarding.

---

## 📊 Live Interactive Dashboard
You can immediately view and interact with the executive dashboard by opening [`powerbi/index.html`](file:///powerbi/index.html) in any browser, or review [`powerbi/dashboard_guide.md`](file:///powerbi/dashboard_guide.md) to replicate the design in Power BI Desktop using [`powerbi/powerbi_export.csv`](file:///powerbi/powerbi_export.csv).

---

## 📂 Project Architecture

```
├── data/
│   ├── indian_bank_customer_churn.csv    # Raw dataset (with intentional anomalies)
│   ├── cleaned_indian_bank_churn.csv   # Post-cleaning dataset
│   └── churn_analytics.db               # SQLite database layer
├── notebooks/
│   ├── 01_data_cleaning_and_eda.ipynb   # Data wrangling, visual EDA & Hypothesis Testing
│   ├── 02_churn_prediction_model.ipynb  # ML Pipeline (SMOTE, Logistic Reg, Random Forest)
│   └── 03_sql_analytics.ipynb          # SQL execution & analytics via SQLAlchemy
├── sql/
│   ├── schema.sql                       # DDL schema for analytics table
│   └── analytical_queries.sql           # 8 advanced business queries (CTEs, Window Functions)
├── powerbi/
│   ├── index.html                       # Standalone interactive browser dashboard
│   ├── powerbi_export.csv               # ML predictions & risk-segmented dataset
│   └── dashboard_guide.md               # Step-by-step Power BI construction guide
├── outputs/
│   └── stats.json                       # Execution metrics & evaluation outputs
├── requirements.txt                     # Project dependencies
└── README.md                            # Executive report & portfolio documentation
```

---

## 🔍 Data Cleaning & Quality Audit
The raw dataset contains **10,050 records** with real-world data quality anomalies:
- **Duplicates**: 50 exact duplicate rows identified and removed.
- **Missing Values**: 142 missing ages and 195 missing salaries imputed using median distributions.
- **Corrupted Types**: String currency formatting (`₹ 65,000.00`) normalized to standard IEEE floating-point numbers.
- **Post-Cleaning Count**: **10,000 unique records**.

---

## 🧪 Statistical Hypothesis Testing
- **Hypothesis**: Senior customers (Age > 50) have a statistically higher churn probability than younger cohorts.
- **Test Conducted**: Chi-Square Test of Independence ($\chi^2$).
- **Test Statistic**: $\chi^2 = 89.6149$, **$p$-value = $2.89 \times 10^{-21}$** ($p < 0.001$).
- **Business Interpretation**: The disparity in retention between age brackets is statistically significant and not due to random variation. Older clients represent a vulnerable segment needing bespoke advisory retention.

---

## 🤖 Machine Learning & Class Imbalance Treatment

### Addressing Severe Class Imbalance
In banking portfolios, customer churn is naturally imbalanced (**10.73% churn rate** in this cohort). Naive classification models predict the majority class (retention) with misleadingly high 89% accuracy but fail on minority recall.

To address this:
1. **SMOTE (Synthetic Minority Over-sampling Technique)** was applied to balance training distributions.
2. **Decision Threshold Tuning** was performed over the Precision-Recall curve to optimize the F1-Score for retention campaigns.

### Model Evaluation Summary

| Model | Accuracy | Precision (Churn) | Recall (Churn) | F1-Score | ROC-AUC | Strategy Fit |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression (SMOTE)** | 65.40% | 18.41% | **64.65%** | **0.2866** | **0.6941** | Broad Campaign (Prioritizes catching all at-risk accounts) |
| **Random Forest (SMOTE + Tuned @ 0.49)** | **76.30%** | **21.16%** | 44.19% | 0.2861 | 0.6712 | Cost-Sensitive (Higher precision for expensive retention perks) |

> 💡 **Interview Talking Point on F1 Score & Cost Sensitivity:**
> In retention economics, a false negative (losing a high-value customer without noticing) is significantly more expensive than a false positive (offering a small discount to a customer who wasn't going to churn). Hence, we prioritize Recall & ROC-AUC via SMOTE and threshold calibration over raw accuracy.

---

## 🗄️ SQL Analytics Layer
The project includes a production SQLite data warehouse layer executing advanced queries:
1. **Overall & Regional Churn**: CTE calculations for metropolitan churn rates.
2. **Product Overload Index**: Window function (`SUM() OVER`) computing cumulative churn across product tiers.
3. **Engagement Matrix**: Grouping inactive vs active accounts to identify high-risk segments.
4. **Financial Profiling**: Ranking regions and balances by churn volume using `RANK()`.

---

## 📈 Strategic Business Recommendations

1. **Implement Product Holding Threshold**: Customers with 3 or more products experience a surge in churn probability. Re-orient cross-selling incentives from volume to product engagement and feature adoption.
2. **Senior Wealth Advisory Unit**: Deploy dedicated relationship managers for accounts where Age > 50, providing personalized estate and retirement planning.
3. **Automated Inactive Reactivation Trigger**: Initiate targeted fee waivers and loyalty bonus incentives within 30 days of an account transitioning to inactive status.
4. **High-Balance Churn Prevention**: Accounts with balances in the top quartile who show reduced transaction velocity should be routed to priority banking teams.
5. **Continuous BI Monitoring**: Utilize the Power BI / web dashboard to monitor regional churn velocity week-over-week.

---

## 🛠️ How to Run Locally

```bash
# 1. Clone repository
git clone https://github.com/gahlawataanchal69-ops/Customer-Churn-Prediction.git
cd Customer-Churn-Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Jupyter to view executed notebooks
jupyter notebook
```
