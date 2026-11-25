# Customer Churn & Retention Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)
![Power BI](https://img.shields.io/badge/Power%20BI-DAX-yellow?logo=powerbi)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Project Overview
This repository contains the end-to-end analytical framework, relational database models, advanced DAX measures, machine learning feature importance models, and interactive dashboards developed to analyze customer attrition across **10,000+ customer records**.

By uncovering primary behavioral drivers of churn and segmenting high-risk cohorts based on usage frequency and monetary trends, this project delivered data-backed retention recommendations that project an estimated **~15% reduction in customer attrition**, preserving **$369,000+ in annual recurring revenue**.

---

## 🚀 Key Highlights & Resume Alignments
- **10,000+ Records Analyzed**: Extracted and analyzed comprehensive demographic, usage, billing, and support service records using MySQL queries and Pandas EDA.
- **Primary Behavioral Drivers Identified**:
  - Month-to-month contracts exhibit a **42.5% churn rate** (3.8x higher than annual contracts).
  - High support tickets (3+) trigger a **58.4% churn rate**.
  - Accounts with no tech support or online security add-ons churn at 2.7x the rate of fully protected accounts.
- **Risk Segmentation**: Engineered multi-dimensional risk tiers (`Low`, `Medium`, `High`, `Critical`) using SQL `NTILE()` window functions and behavioral RFM indices.
- **Dynamic Power BI Report**: Architected star-schema data models, dynamic filters, customer lifetime value (CLV) metrics, and risk tier alert banners.
- **Targeted Retention Strategy**: Quantified a projected **~15% reduction in customer attrition**, saving **420+ accounts** and **$369K+ annually** with a **335% campaign ROI**.

---

## 📂 Repository Structure
```
Customer-Churn-Retention-Analytics/
├── data/
│   ├── raw/
│   │   └── customer_churn_raw_10k.csv         # 10,500 raw customer records
│   └── processed/
│       ├── customer_churn_cleaned_10k.csv     # Cleaned and standardized dataset
│       └── customer_segments_actionable.csv   # Segmented dataset with RFM and risk tiers
├── sql/
│   ├── 01_schema_setup.sql                    # DDL schema, primary keys, and performance indexes
│   ├── 02_churn_exploratory_queries.sql       # Exploratory queries, cohort churn aggregations
│   ├── 03_risk_segmentation_rfm.sql           # NTILE window functions and RFM behavioral scoring
│   └── 04_retention_kpis_and_window_functions.sql # Cumulative running loss and 15% reduction model
├── scripts/
│   ├── generate_dataset.py                    # Synthetic dataset generation engine
│   ├── eda_and_churn_analysis.py              # Statistical EDA, Random Forest feature importance
│   └── risk_segmentation.py                   # Behavioral segmentation and intervention mapping
├── powerbi/
│   ├── DAX_Measures.dax                       # Complete annotated DAX formula library
│   ├── Data_Model_Architecture.md             # Star schema relationships and cardinalities
│   └── PowerBI_Dashboard_Guide.md             # Visual cards, slicers, and drill-through layout guide
├── reports/
│   ├── executive_retention_strategy_report.md # Formal executive strategy and ROI analysis
│   └── figures/                               # High-res diagnostic plots and charts
├── dashboard/
│   └── app.py                                 # Interactive Streamlit Power BI web replica
└── README.md                                  # Project documentation
```

---

## 🛠️ Tech Stack & Methodologies
- **Querying & Databases**: MySQL 8.0, CTEs (Common Table Expressions), Window Functions (`NTILE`, `SUM() OVER`), Joins, Group By Aggregations.
- **Languages & Libraries**: Python 3.11, Pandas, NumPy, Scikit-learn (Random Forest Feature Importance), Matplotlib, Seaborn, Altair.
- **Business Intelligence**: Power BI, Advanced DAX, Star Schema Modeling, Interactive Slicers, What-If Simulation.
- **Dashboarding**: Streamlit web application.

---

## 📊 Running the Project Locally

### 1. Generate Data and Run EDA
```bash
# Run data generator (generates 10,500 customer records)
python scripts/generate_dataset.py

# Run Exploratory Data Analysis & Feature Importance
python scripts/eda_and_churn_analysis.py

# Run Customer Behavioral Segmentation
python scripts/risk_segmentation.py
```

### 2. Run Interactive Web Dashboard
```bash
streamlit run dashboard/app.py
```

---

## 👤 Author
**Kunisetty Giridhar Sai**  
- Email: [kunisettygiridharsai@gmail.com](mailto:kunisettygiridharsai@gmail.com)  
- LinkedIn: [linkedin.com/in/kunisetty-giridhar-sai](https://linkedin.com/in/kunisetty-giridhar-sai)  
- GitHub: [github.com/KUNISETTY-GIRIDHAR-SAI](https://github.com/KUNISETTY-GIRIDHAR-SAI)
