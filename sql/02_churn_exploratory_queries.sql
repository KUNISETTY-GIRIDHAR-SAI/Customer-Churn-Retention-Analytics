-- =====================================================================
-- Project: Customer Churn & Retention Analytics
-- Script 02: Exploratory Data Analysis & Churn Behavioral Queries
-- Uses: Aggregations, GROUP BY, CASE statements, CTEs
-- =====================================================================

USE churn_analytics_db;

-- 1. Baseline Churn Rate & Lost MRR
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS overall_churn_rate_pct,
    ROUND(SUM(monthly_charges), 2) AS total_mrr,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS lost_mrr,
    ROUND(AVG(tenure_months), 1) AS avg_customer_tenure_months
FROM customer_churn;

-- 2. Churn Rate by Contract Type (Key Driver)
SELECT 
    contract_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS churned_revenue_loss
FROM customer_churn
GROUP BY contract_type
ORDER BY churn_rate_pct DESC;

-- 3. Churn Analysis by Tech Support & Online Security Add-ons
SELECT 
    internet_service,
    tech_support,
    online_security,
    COUNT(*) AS customer_count,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS churn_rate_pct
FROM customer_churn
WHERE internet_service != 'No'
GROUP BY internet_service, tech_support, online_security
ORDER BY churn_rate_pct DESC;

-- 4. Customer Tenure Cohort Analysis
WITH tenure_cohorts AS (
    SELECT 
        customer_id,
        churn,
        monthly_charges,
        CASE 
            WHEN tenure_months <= 6 THEN '0 - 6 Months (Critical Onboarding)'
            WHEN tenure_months <= 12 THEN '7 - 12 Months (Early Life)'
            WHEN tenure_months <= 24 THEN '13 - 24 Months (Established)'
            WHEN tenure_months <= 48 THEN '25 - 48 Months (Mature)'
            ELSE '48+ Months (Loyal)'
        END AS tenure_bucket
    FROM customer_churn
)
SELECT 
    tenure_bucket,
    COUNT(*) AS cohort_size,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_in_cohort,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(*) * 100, 2) AS cohort_churn_rate_pct,
    ROUND(SUM(monthly_charges), 2) AS cohort_mrr
FROM tenure_cohorts
GROUP BY tenure_bucket
ORDER BY cohort_churn_rate_pct DESC;
