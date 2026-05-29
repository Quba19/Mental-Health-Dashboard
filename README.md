# Mental Health in Tech Survey — Data Visualization Dashboard
**Student ID:** 70177772  
**Course:** Exploratory Data Analysis  
**Instructor:** Ali Hassan Sherazi  
**Submission Date:** 05-June-2026

## Project Overview
A fully functional, professional-grade data visualization dashboard built on the Mental Health in Tech Survey dataset (1,259 respondents). The dashboard analyzes mental health awareness, treatment-seeking behavior, and workplace factors in the tech industry. Includes 10 chart types, 6 interactive filters, KPI cards, and a filtered data table with CSV download.

## Dataset
- **File:** `data/survey.csv`
- **Source:** OSMI (Open Sourcing Mental Illness) Survey
- **Records:** 1,259 tech industry professionals
- **Features:** 27 columns covering demographics, treatment, workplace culture

## Project Structure
dashboard_project/
├── data/
│ └── survey.csv
├── notebooks/
│ └── analysis.ipynb
├── app.py ← Main dashboard
├── charts.py ← All 10 chart functions
├── filters.py ← Data loading, cleaning, filter logic
├── requirements.txt
└── README.md

## How to Install & Run

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
streamlit run app.py

Dashboard created for EDA Project | SAP ID: 70177772