"""
Interactive Customer Churn & Retention Analytics Dashboard
A high-fidelity replica of the Power BI report built with Streamlit.
Features dynamic filtering, Customer Lifetime Value (CLV) metrics,
Risk Tier Alerts, and an interactive 15% Churn Reduction What-If Simulator.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import altair as alt

st.set_page_config(
    page_title="Customer Churn & Retention Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Power BI aesthetic
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        border-left: 5px solid #1E3A8A;
        margin-bottom: 12px;
    }
    .metric-title { font-size: 0.85rem; color: #64748B; font-weight: 600; text-transform: uppercase; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #0F172A; }
    .metric-delta { font-size: 0.85rem; font-weight: 600; }
    .delta-red { color: #EF4444; }
    .delta-green { color: #10B981; }
    .alert-banner {
        background-color: #FEF2F2;
        border: 1px solid #FCA5A5;
        border-left: 6px solid #EF4444;
        color: #991B1B;
        padding: 12px 16px;
        border-radius: 6px;
        font-weight: 600;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "..", "data", "processed", "customer_churn_cleaned_10k.csv")
    if not os.path.exists(path):
        # Generate on the fly if not found
        import subprocess, sys
        gen_script = os.path.join(current_dir, "..", "scripts", "generate_dataset.py")
        subprocess.run([sys.executable, gen_script], check=True)
    return pd.read_csv(path)

df = load_data()

# Sidebar: Interactive Filters (Mimics Power BI Slicer Panel)
st.sidebar.image("https://img.icons8.com/color/96/power-bi.png", width=50)
st.sidebar.title("Dashboard Slicers")
st.sidebar.markdown("---")

contract_filter = st.sidebar.multiselect(
    "Contract Type",
    options=df["ContractType"].unique(),
    default=df["ContractType"].unique()
)

internet_filter = st.sidebar.multiselect(
    "Internet Service",
    options=df["InternetService"].unique(),
    default=df["InternetService"].unique()
)

risk_filter = st.sidebar.multiselect(
    "Risk Tier",
    options=["Critical", "High", "Medium", "Low"],
    default=["Critical", "High", "Medium", "Low"]
)

tenure_range = st.sidebar.slider(
    "Tenure Range (Months)",
    min_value=int(df["TenureMonths"].min()),
    max_value=int(df["TenureMonths"].max()),
    value=(int(df["TenureMonths"].min()), int(df["TenureMonths"].max()))
)

# Apply filters
filtered_df = df[
    (df["ContractType"].isin(contract_filter)) &
    (df["InternetService"].isin(internet_filter)) &
    (df["RiskTier"].isin(risk_filter)) &
    (df["TenureMonths"].between(tenure_range[0], tenure_range[1]))
]

# Top Title & Alert Banner
st.title("🎯 Customer Churn & Retention Analytics")
st.markdown("**Executive Power BI Analytics Suite** | Data-driven retention intelligence for 10,000+ accounts")

# Dynamic Alert
critical_active = len(filtered_df[(filtered_df["RiskTier"] == "Critical") & (filtered_df["Churn"] == "No")])
if critical_active > 0:
    st.markdown(f"""
    <div class="alert-banner">
        🚨 <strong>HIGH-PRIORITY ATTRITION ALERT:</strong> {critical_active:,} active accounts currently flagged in 
        <strong>CRITICAL RISK TIER</strong> (${filtered_df[(filtered_df['RiskTier'] == 'Critical') & (filtered_df['Churn'] == 'No')]['MonthlyCharges'].sum():,.2f} MRR at immediate risk). Immediate retention intervention recommended.
    </div>
    """, unsafe_allow_html=True)

# Main Metrics Row
total_cust = len(filtered_df)
churned_cust = len(filtered_df[filtered_df["Churn"] == "Yes"])
churn_rate = (churned_cust / total_cust * 100) if total_cust > 0 else 0
total_mrr = filtered_df["MonthlyCharges"].sum()
lost_mrr = filtered_df[filtered_df["Churn"] == "Yes"]["MonthlyCharges"].sum()
avg_monthly = filtered_df["MonthlyCharges"].mean() if total_cust > 0 else 0
clv = (avg_monthly / (churn_rate / 100)) if churn_rate > 0 else 0
projected_savings_15 = (lost_mrr * 12) * 0.15

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Customers</div>
        <div class="metric-value">{total_cust:,}</div>
        <div class="metric-delta">Active: {total_cust - churned_cust:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    churn_color = "delta-red" if churn_rate > 20 else "delta-green"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Churn Rate</div>
        <div class="metric-value">{churn_rate:.1f}%</div>
        <div class="metric-delta {churn_color}">Churned: {churned_cust:,}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Monthly MRR Loss</div>
        <div class="metric-value">${lost_mrr:,.0f}</div>
        <div class="metric-delta delta-red">Annualized: ${lost_mrr*12:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Customer Lifetime Value (CLV)</div>
        <div class="metric-value">${clv:,.0f}</div>
        <div class="metric-delta">Avg Spend: ${filtered_df['TotalCharges'].mean():,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10B981;">
        <div class="metric-title">15% Retention Target</div>
        <div class="metric-value" style="color: #10B981;">+${projected_savings_15:,.0f}</div>
        <div class="metric-delta delta-green">Annual Retained Rev</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs for Views
tab1, tab2, tab3 = st.tabs(["📊 Churn Behavioral Analysis", "⚠️ Risk Tier & Attrition Pipeline", "🎛️ 15% Reduction Scenario Simulator"])

with tab1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Churn Rate by Contract Type")
        contract_data = filtered_df.groupby("ContractType")["Churn"].value_counts(normalize=True).unstack().fillna(0) * 100
        contract_data = contract_data.reset_index()
        chart1 = alt.Chart(contract_data).transform_fold(
            fold=["No", "Yes"],
            as_=["Status", "Percentage"]
        ).mark_bar().encode(
            x=alt.X("ContractType:N", title="Contract Type"),
            y=alt.Y("Percentage:Q", title="Percentage (%)"),
            color=alt.Color("Status:N", scale=alt.Scale(domain=["No", "Yes"], range=["#10B981", "#EF4444"])),
            tooltip=["ContractType:N", "Status:N", alt.Tooltip("Percentage:Q", format=".1f")]
        ).properties(height=320)
        st.altair_chart(chart1, use_container_width=True)

    with col_b:
        st.subheader("Tenure Distribution by Churn Status")
        hist_chart = alt.Chart(filtered_df).mark_area(opacity=0.4).encode(
            x=alt.X("TenureMonths:Q", bin=alt.Bin(maxbins=30), title="Tenure (Months)"),
            y=alt.Y("count()", stack=None, title="Customer Count"),
            color=alt.Color("Churn:N", scale=alt.Scale(domain=["No", "Yes"], range=["#3B82F6", "#EF4444"]))
        ).properties(height=320)
        st.altair_chart(hist_chart, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Support Tickets vs Churn Rate")
        ticket_churn = filtered_df.groupby("SupportTickets")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
        ticket_chart = alt.Chart(ticket_churn).mark_line(point=True, color="#EF4444").encode(
            x=alt.X("SupportTickets:O", title="Number of Support Tickets"),
            y=alt.Y("Churn:Q", title="Churn Rate (%)"),
            tooltip=["SupportTickets", alt.Tooltip("Churn:Q", format=".1f")]
        ).properties(height=300)
        st.altair_chart(ticket_chart, use_container_width=True)

    with col_d:
        st.subheader("Payment Method Churn Comparison")
        pay_churn = filtered_df.groupby("PaymentMethod")["Churn"].apply(lambda x: (x == "Yes").mean() * 100).reset_index()
        pay_chart = alt.Chart(pay_churn).mark_bar(color="#6366F1").encode(
            x=alt.X("Churn:Q", title="Churn Rate (%)"),
            y=alt.Y("PaymentMethod:N", sort="-x", title="Payment Method"),
            tooltip=["PaymentMethod", alt.Tooltip("Churn:Q", format=".1f")]
        ).properties(height=300)
        st.altair_chart(pay_chart, use_container_width=True)

with tab2:
    st.subheader("Customer Risk Tier Breakdown & Escalation Matrix")
    r_col1, r_col2 = st.columns([1, 2])
    with r_col1:
        tier_counts = filtered_df["RiskTier"].value_counts().reset_index()
        tier_counts.columns = ["RiskTier", "Count"]
        pie_chart = alt.Chart(tier_counts).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="RiskTier", type="nominal", scale=alt.Scale(
                domain=["Low", "Medium", "High", "Critical"],
                range=["#10B981", "#F59E0B", "#F97316", "#EF4444"]
            )),
            tooltip=["RiskTier", "Count"]
        ).properties(height=300)
        st.altair_chart(pie_chart, use_container_width=True)

    with r_col2:
        st.markdown("**At-Risk Accounts Requiring Immediate Retention Action**")
        high_risk_table = filtered_df[
            (filtered_df["RiskTier"].isin(["Critical", "High"])) &
            (filtered_df["Churn"] == "No")
        ][["CustomerID", "ContractType", "TenureMonths", "MonthlyCharges", "SupportTickets", "RiskTier", "ChurnRiskScore"]].head(10)
        st.dataframe(high_risk_table, use_container_width=True)

with tab3:
    st.subheader("🎛️ What-If Retention Scenario Simulator")
    st.markdown("Simulate the financial and operational impact of reducing customer attrition using data-driven interventions.")
    
    sim_col1, sim_col2 = st.columns([1, 2])
    with sim_col1:
        target_pct = st.slider("Target Churn Reduction (%)", min_value=5, max_value=30, value=15, step=1)
        retention_cost_per_user = st.number_input("Retention Incentive Cost per Account ($)", min_value=10, max_value=250, value=85)
        
        sim_saved_cust = int(churned_cust * (target_pct / 100))
        sim_annual_rev = (lost_mrr * 12) * (target_pct / 100)
        sim_total_cost = sim_saved_cust * retention_cost_per_user
        sim_net_roi = sim_annual_rev - sim_total_cost
        roi_ratio = (sim_net_roi / sim_total_cost * 100) if sim_total_cost > 0 else 0

    with sim_col2:
        st.markdown(f"""
        ### Projected Financial Returns ({target_pct}% Attrition Reduction)
        - 👥 **Customers Saved Annually**: **{sim_saved_cust:,}** accounts
        - 💵 **Gross Annual Retained Revenue**: **${sim_annual_rev:,.2f}**
        - 🏷️ **Total Campaign Investment**: **${sim_total_cost:,.2f}**
        - 🚀 **Net Annualized Profit**: **${sim_net_roi:,.2f}**
        - 📈 **Net Campaign Return on Investment (ROI)**: **{roi_ratio:.1f}%**
        """)
        
        st.success(f"Targeting a **{target_pct}% reduction** preserves **${sim_annual_rev:,.2f}** in recurring revenue with **{roi_ratio:.1f}% ROI**!")
