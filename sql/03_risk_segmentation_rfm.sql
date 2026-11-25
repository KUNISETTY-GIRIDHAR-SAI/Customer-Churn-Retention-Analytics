-- =====================================================================
-- Project: Customer Churn & Retention Analytics
-- Script 03: Risk Segmentation & Behavioral RFM Scoring
-- Uses: NTILE() Window Functions, CTEs, Ranking, High-Risk Identification
-- =====================================================================

USE churn_analytics_db;

-- Behavioral NTILE segmentation based on Recency, Frequency, and Monetary metrics
WITH customer_rfm_quartiles AS (
    SELECT 
        customer_id,
        tenure_months,
        monthly_charges,
        usage_frequency_logins,
        support_tickets,
        last_interaction_days,
        risk_tier,
        churn,
        -- Window functions to divide active customers into quartiles
        NTILE(4) OVER (ORDER BY last_interaction_days DESC) AS r_quartile, -- 4 = most disengaged
        NTILE(4) OVER (ORDER BY usage_frequency_logins ASC) AS f_quartile,  -- 4 = lowest usage
        NTILE(4) OVER (ORDER BY monthly_charges DESC) AS m_quartile         -- 4 = highest value
    FROM customer_churn
    WHERE churn = 'No' -- Focus on active retention candidates
),
segmented_customers AS (
    SELECT 
        customer_id,
        tenure_months,
        monthly_charges,
        support_tickets,
        risk_tier,
        r_quartile,
        f_quartile,
        m_quartile,
        CASE 
            WHEN risk_tier IN ('Critical', 'High') AND m_quartile = 4 THEN 'Tier 1: High-Value At-Risk'
            WHEN risk_tier IN ('Critical', 'High') AND m_quartile < 4 THEN 'Tier 2: Mid/Low-Value At-Risk'
            WHEN support_tickets >= 3 THEN 'Tier 3: High Support Friction'
            WHEN tenure_months <= 12 AND f_quartile = 4 THEN 'Tier 4: Disengaged New Customer'
            ELSE 'Tier 5: Healthy Core'
        END AS priority_retention_segment
    FROM customer_rfm_quartiles
)
SELECT 
    priority_retention_segment,
    COUNT(*) AS target_customer_count,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_bill,
    ROUND(SUM(monthly_charges), 2) AS total_mrr_at_risk,
    ROUND(AVG(support_tickets), 1) AS avg_support_tickets,
    ROUND(SUM(monthly_charges) * 12, 2) AS annual_revenue_exposure
FROM segmented_customers
GROUP BY priority_retention_segment
ORDER BY total_mrr_at_risk DESC;
