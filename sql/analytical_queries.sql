-- analytical_queries.sql
-- 1. Overall Churn Rate
SELECT 
    COUNT(*) as total_customers,
    SUM(Churn) as churned_customers,
    ROUND(SUM(Churn) * 100.0 / COUNT(*), 2) as churn_rate_pct
FROM customer_churn;

-- 2. Churn Rate by Location (using CTE)
WITH LocationStats AS (
    SELECT 
        Location,
        COUNT(*) as total,
        SUM(Churn) as churned
    FROM customer_churn
    GROUP BY Location
)
SELECT 
    Location,
    total,
    churned,
    ROUND((churned * 100.0) / total, 2) as churn_rate_pct
FROM LocationStats
ORDER BY churn_rate_pct DESC;

-- 3. Average Balance and Salary of Churned vs Non-Churned
SELECT 
    CASE WHEN Churn = 1 THEN 'Churned' ELSE 'Retained' END as Status,
    ROUND(AVG(Balance), 2) as avg_balance,
    ROUND(AVG(EstimatedSalary), 2) as avg_salary,
    COUNT(*) as customer_count
FROM customer_churn
GROUP BY Churn;

-- 4. Churn by Number of Products (Window Function for cumulative total)
SELECT 
    NumOfProducts,
    COUNT(*) as customer_count,
    SUM(Churn) as churned,
    ROUND(AVG(Churn) * 100, 2) as churn_rate_pct,
    SUM(COUNT(*)) OVER (ORDER BY NumOfProducts) as running_total_customers
FROM customer_churn
GROUP BY NumOfProducts;

-- 5. Identifying High-Risk Segments (Age > 50 and Inactive)
SELECT 
    Gender,
    COUNT(*) as segment_size,
    ROUND(AVG(Churn) * 100, 2) as churn_rate_pct
FROM customer_churn
WHERE Age > 50 AND IsActiveMember = 0
GROUP BY Gender
ORDER BY churn_rate_pct DESC;

-- 6. Rank Locations by Churn Volume using Window Functions
SELECT 
    Location,
    SUM(Churn) as total_churned,
    RANK() OVER (ORDER BY SUM(Churn) DESC) as churn_rank
FROM customer_churn
GROUP BY Location;

-- 7. Analyzing Tenure impact on Churn
SELECT 
    Tenure,
    COUNT(*) as total_customers,
    SUM(Churn) as churned,
    ROUND((SUM(Churn) * 100.0) / COUNT(*), 2) as churn_rate_pct
FROM customer_churn
GROUP BY Tenure
ORDER BY Tenure;

-- 8. Customer Profile: Highly Engaged vs Low Engagement
SELECT 
    CASE 
        WHEN NumOfProducts > 1 AND IsActiveMember = 1 THEN 'High Engagement'
        ELSE 'Low Engagement'
    END as engagement_level,
    COUNT(*) as customers,
    ROUND(AVG(Churn) * 100, 2) as churn_rate_pct
FROM customer_churn
GROUP BY engagement_level;
