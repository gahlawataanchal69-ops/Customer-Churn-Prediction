# Customer Churn Prediction & Retention Analysis

## 📌 Project Overview
This repository contains an end-to-end Data Analyst portfolio project focused on predicting customer churn for an Indian Bank. The project covers the entire data lifecycle: from data acquisition, cleaning, and exploratory data analysis (EDA), to advanced SQL querying, hypothesis testing, machine learning modeling, and Power BI dashboard preparation.

The goal of this project is to identify at-risk customers and provide actionable business recommendations to improve retention.

## 📂 Repository Structure
- **`/data`**: Contains the raw and cleaned datasets.
- **`/notebooks`**:
  - `01_data_cleaning_and_eda.ipynb`: Pandas data cleaning, visual EDA with Matplotlib/Seaborn, and Hypothesis Testing.
  - `02_churn_prediction_model.ipynb`: Machine learning models (Logistic Regression & Random Forest).
  - `03_sql_analytics.ipynb`: Python-based execution of SQL queries using SQLite and SQLAlchemy.
- **`/sql`**:
  - `schema.sql`: Table definition for the data warehouse layer.
  - `analytical_queries.sql`: Advanced SQL queries (CTEs, Window Functions, Joins).
- **`/powerbi`**:
  - `powerbi_export.csv`: Optimized export for BI tools.
  - `dashboard_guide.md`: Step-by-step guide to building the Power BI dashboard.
- **`outputs/`**: Contains generated stats.
- **`requirements.txt`**: Environment dependencies.

## 📊 Dataset
The project uses an Indian Bank Customer Churn dataset (synthetically augmented from real-world statistical baselines to include data quality issues like duplicates, missing values, and corrupted data types for demonstration purposes). 

- **Before Cleaning**: 10,050 rows
- **After Cleaning**: 10,000 rows (Removed 50 exact duplicates, imputed 150 missing ages, and fixed string/currency data types for 'Balance').

## ❓ Business Questions Answered
1. What is the overall churn rate, and how does it vary by geographic location?
2. Are older customers significantly more likely to churn than younger ones?
3. How does the number of bank products held impact customer retention?
4. What is the financial profile (average balance and salary) of a churned customer vs. a retained customer?
5. Which features are the strongest predictors of churn?

## 💡 Key Insights (Data-Backed)
1. **Overall Churn Rate**: The baseline churn rate across the bank is **16.53%**.
2. **Age Impact (Hypothesis Test)**: We hypothesized that older customers (Age > 50) have a different churn rate. A Chi-Square test confirmed this is highly statistically significant (**p-value = 4.22e-40**). Customers over 50 are a high-risk segment.
3. **Product Overload**: Churn risk increases dramatically for customers holding 3 or more products.
4. **Engagement**: Inactive members show a significantly higher propensity to leave the bank compared to highly engaged customers.

## 🤖 Machine Learning Model Results
Two classification models were trained to predict churn. Because churn is an imbalanced class, we used `class_weight='balanced'` for Random Forest and evaluated using F1 Score and Accuracy.

| Model | Accuracy | F1 Score | Notes |
|-------|----------|----------|-------|
| **Logistic Regression** | 83.50% | 0.0517 | High accuracy due to majority class prediction, but fails to capture complex minority signals. |
| **Random Forest** | 82.90% | 0.1140 | Better recall and F1 score; correctly identified non-linear relationships like the "Product Overload" effect. |

*Top Features Identified by Random Forest: Age, Balance, and Number of Products.*

## 📈 Specific Business Recommendations
Based on the analysis, here are 5 specific recommendations for the retention team:

1. **Targeted Senior Outreach**: Since the Age > 50 segment showed a statistically significant higher churn rate, deploy a dedicated relationship management team specifically for older customers, offering personalized financial check-ins.
2. **Product Rationalization**: Customers with 3+ products show elevated churn. Limit aggressive cross-selling campaigns for customers who already hold 2 products, and focus instead on usage/engagement of existing products.
3. **Engagement Reactivation Campaign**: Run an automated email/SMS campaign for customers marked as `IsActiveMember = 0` offering temporary fee waivers or bonus points to re-engage them.
4. **High-Balance Retention Perks**: Since `Balance` is a top predictor in the Random Forest model, flag customers in the top 10% of account balances who show declining activity for premium loyalty perks.
5. **Dashboard Monitoring**: Deploy the Power BI dashboard (using `powerbi_export.csv`) to regional managers, specifically using the drill-down feature on 'Location' to monitor localized churn spikes week-over-week.

## 🚀 How to Run
1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Open and run the Jupyter notebooks in the `/notebooks` folder sequentially.
4. (Optional) Follow `powerbi/dashboard_guide.md` to build the BI visuals.
