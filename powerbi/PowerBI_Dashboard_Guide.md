# Power BI Dashboard Implementation Guide

## 1. Canvas Setup & Theme
- **Report Dimensions**: 16:9 Standard (1280 x 720 px or 1920 x 1080 px).
- **Color Palette**:
  - Primary Brand: Deep Navy (`#1E3A8A`)
  - Accent / Positive: Emerald Green (`#10B981`)
  - Warning / Alert: Crimson Red (`#EF4444`)
  - Accent Neutral: Slate Gray (`#64748B`)
  - Background: Off-white Canvas (`#F8FAFC`)

## 2. Dashboard Layout Architecture (3 Core Pages)

### Page 1: Executive Churn Overview & KPIs
1. **Top Header**: Title, Last Refreshed timestamp, Dynamic Risk Alert banner.
2. **KPI Card Row (Top)**:
   - `Total Customers` (e.g. 10,500)
   - `Churn Rate` with conditional color formatting (Target < 20%)
   - `Total MRR` ($) & `Lost Monthly MRR` ($)
   - `Projected 15% Reduction Annual Retained Revenue` (Highlight Card)
3. **Left Slicer Panel**:
   - Contract Type slicer (Tile format)
   - Internet Service slicer (Dropdown)
   - Risk Tier slicer (Multi-select)
   - Tenure Range Slider (1 to 72 months)
4. **Visual 1 (Donut Chart)**: Churn Distribution (Active vs Churned).
5. **Visual 2 (Clustered Column Chart)**: Churn Rate by Contract Type & Payment Method.
6. **Visual 3 (Area Chart)**: Customer Tenure Cohort vs Churn Probability.

### Page 2: Risk Tier Segmentation & Early Warning Alerts
1. **Top Banner**: `Critical Risk Alert Status` (dynamic DAX measure).
2. **Visual 1 (Treemap / Bar Chart)**: MRR at Stake broken down by Risk Tier.
3. **Visual 2 (Scatter Plot / Bubble Chart)**:
   - X-Axis: `UsageFrequencyLogins` (Engagement)
   - Y-Axis: `SupportTickets` (Friction)
   - Size: `MonthlyCharges` (Value)
   - Color: `RiskTier`
4. **Visual 3 (Interactive Table / Matrix)**:
   - Columns: `CustomerID`, `ContractType`, `TenureMonths`, `MonthlyCharges`, `SupportTickets`, `RiskTier`, `RecommendedIntervention`.
   - Conditional formatting: Red background on Critical risk rows.

### Page 3: Retention Scenario Simulator (~15% Reduction Target)
1. **What-If Parameter Slider**:
   - `Target Churn Reduction %` (Default: 15%, Range: 5% to 30%).
2. **Dynamic KPI Responses**:
   - Customers Saved: `[Projected Retained Customers]`
   - Annual Revenue Saved: `[Projected Retained Annual Revenue]`
   - Campaign ROI calculation.
3. **Actionable Roadmap**: Priority intervention matrix and cost-benefit breakdown.
