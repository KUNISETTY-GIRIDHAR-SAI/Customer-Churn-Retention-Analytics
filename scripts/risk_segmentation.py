"""
Customer Risk Segmentation & RFM Behavioral Scoring
Performs multi-dimensional behavioral segmentation based on usage frequency,
monetary contribution, tenure, and support friction to identify high-risk cohorts
and formulate targeted retention strategies.
"""

import os
import pandas as pd
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "processed", "customer_churn_cleaned_10k.csv")
output_path = os.path.join(script_dir, "..", "data", "processed", "customer_segments_actionable.csv")
reports_dir = os.path.join(script_dir, "..", "reports")

df = pd.read_csv(data_path)

# Calculate RFM-style Behavioral Scores
# R: Recency (Days since last interaction - lower is more recent, higher is at risk of disengagement)
# F: Frequency (Monthly logins)
# M: Monetary (Monthly charges)

df["R_Score"] = pd.qcut(df["LastInteractionDays"], 4, labels=[4, 3, 2, 1]).astype(int)
df["F_Score"] = pd.qcut(df["UsageFrequencyLogins"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
df["M_Score"] = pd.qcut(df["MonthlyCharges"], 4, labels=[1, 2, 3, 4]).astype(int)
df["RFM_Index"] = df["R_Score"] * 100 + df["F_Score"] * 10 + df["M_Score"]

# Segment Definitions
def assign_actionable_segment(row):
    if row["RiskTier"] in ["Critical", "High"] and row["M_Score"] >= 3:
        return "High-Value At-Risk (Tier 1 Priority)"
    elif row["RiskTier"] in ["Critical", "High"] and row["M_Score"] < 3:
        return "Price-Sensitive At-Risk (Tier 2 Priority)"
    elif row["SupportTickets"] >= 3:
        return "Service-Friction Cohort (CS Outreach)"
    elif row["TenureMonths"] <= 12 and row["ContractType"] == "Month-to-month":
        return "Early Onboarding Vulnerable"
    elif row["RiskTier"] == "Low" and row["M_Score"] >= 3:
        return "Champions & Brand Advocates"
    else:
        return "Stable Core Users"

df["RetentionSegment"] = df.apply(assign_actionable_segment, axis=1)

# Recommended Interventions per segment
intervention_map = {
    "High-Value At-Risk (Tier 1 Priority)": "Executive account manager check-in + 20% 12-month contract lock discount + Dedicated support line",
    "Price-Sensitive At-Risk (Tier 2 Priority)": "Downgrade prevention offer + Value pack bundling + Flexible payment terms",
    "Service-Friction Cohort (CS Outreach)": "Priority technical resolution SLA + Root cause ticket audit + 1-month free service waiver",
    "Early Onboarding Vulnerable": "Structured 90-day onboarding workflow + Feature adoption webinars + Proactive check-ins",
    "Champions & Brand Advocates": "Referral reward program + Early beta access + Loyalty perks",
    "Stable Core Users": "Periodic newsletter + Self-service tips + Upsell opportunities"
}

df["RecommendedIntervention"] = df["RetentionSegment"].map(intervention_map)

# Summary of Segments
seg_summary = df.groupby("RetentionSegment").agg(
    CustomerCount=("CustomerID", "count"),
    AvgMonthlyCharges=("MonthlyCharges", "mean"),
    TotalMRR=("MonthlyCharges", "sum"),
    ChurnRate=("Churn", lambda x: (x == "Yes").mean() * 100),
    AvgTickets=("SupportTickets", "mean")
).reset_index().sort_values("TotalMRR", ascending=False)

print("\n--- RETENTION ACTIONABLE SEGMENTS ---")
print(seg_summary.to_string(index=False))

df.to_csv(output_path, index=False)
print(f"\nSaved enriched customer segmentation dataset to: {output_path}")
