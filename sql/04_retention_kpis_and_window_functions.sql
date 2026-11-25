-- =====================================================================
-- Project: Customer Churn & Retention Analytics
-- Script 04: Retention KPIs, Window Functions, and 15% Reduction Projection
-- Uses: SUM() OVER(), LAG(), DENSE_RANK(), Scenario Simulation
-- =====================================================================

USE churn_analytics_db;

-- 1. Cumulative Revenue Loss Running Total
SELECT 
    risk_tier,
    COUNT(*) AS churned_count,
    ROUND(SUM(monthly_charges), 2) AS lost_mrr_by_tier,
    -- Window function: Running total across risk tiers
    ROUND(SUM(SUM(monthly_charges)) OVER (ORDER BY FIELD(risk_tier, 'Critical', 'High', 'Medium', 'Low')), 2) AS cumulative_lost_mrr
FROM customer_churn
WHERE churn = 'Yes'
GROUP BY risk_tier
ORDER BY FIELD(risk_tier, 'Critical', 'High', 'Medium', 'Low');

-- 2. Projected ~15% Churn Reduction Financial Model
WITH current_churn_summary AS (
    SELECT 
        COUNT(*) AS total_customers,
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS total_churned,
        SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END) AS monthly_churn_revenue_loss,
        SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END) * 12 AS annual_churn_revenue_loss
    FROM customer_churn
)
SELECT 
    total_customers,
    total_churned AS current_annual_churned,
    ROUND(current_annual_churned * 0.15, 0) AS customers_saved_15pct_target,
    ROUND(annual_churn_revenue_loss, 2) AS current_annual_loss,
    ROUND(annual_churn_revenue_loss * 0.15, 2) AS annual_revenue_saved_projection,
    ROUND((annual_churn_revenue_loss * 0.15) / 12, 2) AS monthly_retained_mrr_lift
FROM current_churn_summary;
