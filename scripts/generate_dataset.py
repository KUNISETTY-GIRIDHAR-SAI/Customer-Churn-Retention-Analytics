"""
Data Generator for Customer Churn & Retention Analytics Project
Generates 10,500 realistic customer records with demographic, behavioral,
contractual, and usage metrics, simulating enterprise telecom/SaaS customer base.
"""

import numpy as np
import pandas as pd
import os

np.random.seed(42)
NUM_RECORDS = 10500

customer_ids = [f"CUST-{10001 + i}" for i in range(NUM_RECORDS)]
genders = np.random.choice(["Male", "Female"], size=NUM_RECORDS, p=[0.505, 0.495])
senior_citizens = np.random.choice([0, 1], size=NUM_RECORDS, p=[0.838, 0.162])
partners = np.random.choice(["Yes", "No"], size=NUM_RECORDS, p=[0.48, 0.52])
dependents = np.where(partners == "Yes", np.random.choice(["Yes", "No"], size=NUM_RECORDS, p=[0.55, 0.45]), np.random.choice(["Yes", "No"], size=NUM_RECORDS, p=[0.15, 0.85]))

# Tenure in months: mixture of newer (<12m), medium (12-36m), long-term (>36m)
n1 = int(NUM_RECORDS * 0.35)
n2 = int(NUM_RECORDS * 0.35)
n3 = NUM_RECORDS - (n1 + n2)
tenure_months = np.concatenate([
    np.random.randint(1, 13, size=n1),
    np.random.randint(13, 37, size=n2),
    np.random.randint(37, 73, size=n3)
])
np.random.shuffle(tenure_months)

phone_service = np.random.choice(["Yes", "No"], size=NUM_RECORDS, p=[0.90, 0.10])
multiple_lines = np.where(
    phone_service == "Yes",
    np.random.choice(["Yes", "No"], size=NUM_RECORDS, p=[0.44, 0.56]),
    "No phone service"
)

internet_service = np.random.choice(["Fiber optic", "DSL", "No"], size=NUM_RECORDS, p=[0.44, 0.34, 0.22])

def assign_internet_addon(internet_col, prob_yes):
    return np.where(
        internet_col == "No",
        "No internet service",
        np.random.choice(["Yes", "No"], size=len(internet_col), p=[prob_yes, 1.0 - prob_yes])
    )

online_security = assign_internet_addon(internet_service, 0.38)
online_backup = assign_internet_addon(internet_service, 0.44)
device_protection = assign_internet_addon(internet_service, 0.43)
tech_support = assign_internet_addon(internet_service, 0.39)
streaming_tv = assign_internet_addon(internet_service, 0.49)
streaming_movies = assign_internet_addon(internet_service, 0.50)

# Contract type
contract_type = np.random.choice(["Month-to-month", "One year", "Two year"], size=NUM_RECORDS, p=[0.55, 0.24, 0.21])
paperless_billing = np.random.choice(["Yes", "No"], size=NUM_RECORDS, p=[0.60, 0.40])
payment_method = np.random.choice(
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
    size=NUM_RECORDS,
    p=[0.34, 0.22, 0.22, 0.22]
)

# Usage metrics (Logins, support tickets, usage frequency)
usage_frequency_logins = np.random.poisson(lam=18, size=NUM_RECORDS)
usage_frequency_logins = np.clip(usage_frequency_logins, 1, 45)

support_tickets = np.random.poisson(lam=1.4, size=NUM_RECORDS)
support_tickets = np.clip(support_tickets, 0, 10)

last_interaction_days = np.random.randint(1, 90, size=NUM_RECORDS)

# Base monthly charges
monthly_charges = np.zeros(NUM_RECORDS)
for i in range(NUM_RECORDS):
    base = 20.0
    if phone_service[i] == "Yes":
        base += 10.0
    if multiple_lines[i] == "Yes":
        base += 15.0
    if internet_service[i] == "Fiber optic":
        base += 40.0
    elif internet_service[i] == "DSL":
        base += 25.0
    
    addon_cost = sum([
        10.0 if online_security[i] == "Yes" else 0.0,
        10.0 if online_backup[i] == "Yes" else 0.0,
        10.0 if device_protection[i] == "Yes" else 0.0,
        12.0 if tech_support[i] == "Yes" else 0.0,
        15.0 if streaming_tv[i] == "Yes" else 0.0,
        15.0 if streaming_movies[i] == "Yes" else 0.0,
    ])
    noise = np.random.uniform(-4.0, 4.0)
    monthly_charges[i] = round(max(18.5, base + addon_cost + noise), 2)

total_charges = np.round(monthly_charges * tenure_months * np.random.uniform(0.96, 1.04, size=NUM_RECORDS), 2)

# Calculate realistic churn probability based on key risk factors
# Month-to-month contracts, lack of tech support, fiber optic with high complaints, high tickets, low tenure
churn_logit = (
    -1.5
    + (contract_type == "Month-to-month") * 1.55
    - (contract_type == "Two year") * 1.6
    - (contract_type == "One year") * 0.7
    + (internet_service == "Fiber optic") * 0.45
    - (tech_support == "Yes") * 0.65
    - (online_security == "Yes") * 0.55
    + (payment_method == "Electronic check") * 0.42
    + (support_tickets >= 3) * 0.95
    - (tenure_months > 24) * 0.60
    - (tenure_months > 48) * 0.80
    + (monthly_charges > 80) * 0.35
    + (usage_frequency_logins < 8) * 0.50
    + np.random.normal(0, 0.45, size=NUM_RECORDS)
)

churn_prob = 1.0 / (1.0 + np.exp(-churn_logit))
churn = np.where(churn_prob > 0.52, "Yes", "No")

# Risk score (0 to 100) and Risk Tier
risk_score = np.clip(np.round(churn_prob * 100, 1), 0.0, 100.0)
risk_tier = pd.cut(
    risk_score,
    bins=[-0.1, 30.0, 55.0, 75.0, 100.1],
    labels=["Low", "Medium", "High", "Critical"]
)

# Assemble DataFrame
df = pd.DataFrame({
    "CustomerID": customer_ids,
    "Gender": genders,
    "SeniorCitizen": senior_citizens,
    "Partner": partners,
    "Dependents": dependents,
    "TenureMonths": tenure_months,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "ContractType": contract_type,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "UsageFrequencyLogins": usage_frequency_logins,
    "SupportTickets": support_tickets,
    "LastInteractionDays": last_interaction_days,
    "ChurnRiskScore": risk_score,
    "RiskTier": risk_tier,
    "Churn": churn
})

# Save Raw and Cleaned datasets
script_dir = os.path.dirname(os.path.abspath(__file__))
raw_path = os.path.join(script_dir, "..", "data", "raw", "customer_churn_raw_10k.csv")
clean_path = os.path.join(script_dir, "..", "data", "processed", "customer_churn_cleaned_10k.csv")

df.to_csv(raw_path, index=False)
df.to_csv(clean_path, index=False)

print(f"Generated {len(df)} records.")
print(f"Overall Churn Rate: {(df['Churn'] == 'Yes').mean() * 100:.2f}%")
print(f"Risk Tier Counts:\n{df['RiskTier'].value_counts()}")
print(f"Saved raw dataset to: {raw_path}")
print(f"Saved processed dataset to: {clean_path}")
