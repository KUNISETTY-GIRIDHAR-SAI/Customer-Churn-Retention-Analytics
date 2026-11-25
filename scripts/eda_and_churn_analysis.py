"""
Exploratory Data Analysis and Churn Driver Analysis
Computes key statistical metrics, correlations, feature importances using Random Forest / Logistic Regression,
and outputs high-resolution diagnostic charts.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Set style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.sans-serif': 'Segoe UI', 'font.size': 10})

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "processed", "customer_churn_cleaned_10k.csv")
reports_dir = os.path.join(script_dir, "..", "reports")
figures_dir = os.path.join(reports_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

df = pd.read_csv(data_path)
print(f"Loaded {len(df)} records for EDA.")

# 1. Summary Statistics & Churn Rate
total_customers = len(df)
churned = df[df["Churn"] == "Yes"]
churn_rate = len(churned) / total_customers * 100
total_monthly_rev = df["MonthlyCharges"].sum()
lost_monthly_rev = churned["MonthlyCharges"].sum()

print("\n--- EXECUTIVE SUMMARY ---")
print(f"Total Customer Base: {total_customers:,}")
print(f"Churned Customers: {len(churned):,} ({churn_rate:.2f}%)")
print(f"Total Monthly Recurring Revenue (MRR): ${total_monthly_rev:,.2f}")
print(f"Lost Monthly Revenue to Churn: ${lost_monthly_rev:,.2f}")
print(f"Projected 15% Churn Reduction Annual Savings: ${lost_monthly_rev * 0.15 * 12:,.2f}")

# 2. Plot 1: Churn by Contract Type
fig, ax = plt.subplots(figsize=(8, 5))
contract_churn = df.groupby(["ContractType", "Churn"]).size().unstack(fill_value=0)
contract_pct = contract_churn.div(contract_churn.sum(axis=1), axis=0) * 100
contract_pct.plot(kind="bar", stacked=True, color=["#10B981", "#EF4444"], ax=ax, edgecolor="none", width=0.6)
ax.set_title("Customer Churn Rate by Contract Type", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Percentage (%)", fontsize=11)
ax.set_xlabel("Contract Type", fontsize=11)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Churned", frameon=True)
for p in ax.patches:
    h = p.get_height()
    if h > 5:
        ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., p.get_y() + h / 2.),
                    ha='center', va='center', color='white', fontweight='bold', fontsize=10)
plt.tight_layout()
fig.savefig(os.path.join(figures_dir, "churn_by_contract.png"), dpi=300)
plt.close()

# 3. Plot 2: Tenure Distribution vs Churn
fig, ax = plt.subplots(figsize=(9, 5))
sns.kdeplot(data=df, x="TenureMonths", hue="Churn", common_norm=False, fill=True, palette={"Yes": "#EF4444", "No": "#3B82F6"}, alpha=0.4, ax=ax)
ax.set_title("Customer Tenure Distribution (Active vs Churned)", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Tenure (Months)", fontsize=11)
ax.set_ylabel("Density", fontsize=11)
ax.axvline(12, color='gray', linestyle='--', alpha=0.7, label='Year 1 Critical Threshold')
ax.legend(title="Status", labels=["Active", "Churned", "12-Month Milestone"])
plt.tight_layout()
fig.savefig(os.path.join(figures_dir, "tenure_vs_churn.png"), dpi=300)
plt.close()

# 4. Plot 3: Risk Tier Breakdown and At-Risk Revenue
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
tier_counts = df["RiskTier"].value_counts()[["Low", "Medium", "High", "Critical"]]
colors = ["#10B981", "#F59E0B", "#F97316", "#EF4444"]
ax1.pie(tier_counts, labels=tier_counts.index, autopct="%1.1f%%", startangle=140, colors=colors, explode=(0, 0, 0.05, 0.08))
ax1.set_title("Customer Distribution by Risk Tier", fontsize=13, fontweight="bold")

tier_rev = df.groupby("RiskTier", observed=True)["MonthlyCharges"].sum()[["Low", "Medium", "High", "Critical"]]
sns.barplot(x=tier_rev.index, y=tier_rev.values, palette=colors, ax=ax2)
ax2.set_title("Monthly Recurring Revenue (MRR) by Risk Tier", fontsize=13, fontweight="bold")
ax2.set_ylabel("Monthly Revenue ($)", fontsize=11)
ax2.set_xlabel("Risk Tier", fontsize=11)
for i, v in enumerate(tier_rev.values):
    ax2.text(i, v + 5000, f"${v:,.0f}", ha='center', fontweight='bold', fontsize=10)
plt.tight_layout()
fig.savefig(os.path.join(figures_dir, "risk_tier_revenue.png"), dpi=300)
plt.close()

# 5. Machine Learning Feature Importance (Drivers of Churn)
cat_cols = df.select_dtypes(include=["object"]).columns.drop(["CustomerID", "Churn"])
df_encoded = df.copy()
le = LabelEncoder()
for c in cat_cols:
    df_encoded[c] = le.fit_transform(df_encoded[c].astype(str))
df_encoded["Churn_Binary"] = (df_encoded["Churn"] == "Yes").astype(int)

features = [
    "TenureMonths", "MonthlyCharges", "TotalCharges", "UsageFrequencyLogins",
    "SupportTickets", "LastInteractionDays", "ContractType", "InternetService",
    "OnlineSecurity", "TechSupport", "PaymentMethod", "PaperlessBilling"
]
X = df_encoded[features]
y = df_encoded["Churn_Binary"]

rf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
rf.fit(X, y)

importance_df = pd.DataFrame({"Feature": features, "Importance": rf.feature_importances_}).sort_values("Importance", ascending=True)

fig, ax = plt.subplots(figsize=(9, 6))
sns.barplot(data=importance_df, y="Feature", x="Importance", palette="Blues_d", ax=ax)
ax.set_title("Top Primary Behavioral & Contractual Drivers of Churn", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Relative Feature Importance Score", fontsize=11)
ax.set_ylabel("Factor", fontsize=11)
for p in ax.patches:
    width = p.get_width()
    ax.annotate(f"{width:.3f}", (width + 0.003, p.get_y() + p.get_height() / 2.),
                va='center', fontsize=9, fontweight='bold', color='#1E293B')
plt.tight_layout()
fig.savefig(os.path.join(figures_dir, "feature_importance_drivers.png"), dpi=300)
plt.close()

print("EDA analysis completed. Generated all diagnostic figures in reports/figures/")
