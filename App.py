import streamlit as st
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')

# Import from filters and charts
try:
    from filters import load_and_clean_data, apply_filters, get_kpi_metrics
    from charts import (
        pie_chart_treatment,
        histogram_age,
        line_chart_age_distribution,
        bar_chart_by_country,
        scatter_age_work_interfere,
        box_plot_age_by_treatment,
        heatmap_correlation,
        area_chart_company_size,
        count_plot_remote_work,
        violin_plot_age_by_gender,
    )
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Mental Health in Tech Dashboard — 70177772",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
.main { background-color: #F8F9FA; }
.block-container { padding-top: 1.5rem; }
.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #2E86AB;
}
.kpi-value { font-size: 28px; font-weight: 700; color: #2E86AB; }
.kpi-label { font-size: 12px; color: #666; margin-top: 4px; }
.section-header {
    background: linear-gradient(90deg, #2E86AB, #1D3557);
    color: white;
    padding: 10px 18px;
    border-radius: 8px;
    margin: 20px 0 12px 0;
    font-weight: 600;
    font-size: 16px;
}
.stMetric { background: white; border-radius: 8px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Load data with error handling ─────────────────────────────────
@st.cache_data
def get_data():
    """Load data with multiple path attempts"""
    possible_paths = [
        'data/survey.csv',
        'survey.csv',
        './data/survey.csv',
        '../data/survey.csv',
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                return load_and_clean_data(path)
        except Exception as e:
            continue
    
    # If all paths fail
    st.error("❌ Dataset file 'survey.csv' not found!")
    st.write("**Expected location:** `data/survey.csv`")
    st.write("**Current working directory:**", os.getcwd())
    
    # Show what files exist
    if os.path.exists('.'):
        st.write("**Files in current directory:**", os.listdir('.'))
    if os.path.exists('data'):
        st.write("**Files in data folder:**", os.listdir('data'))
    
    return None

df_raw = get_data()

# Stop if no data
if df_raw is None:
    st.stop()

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR — ALL FILTERS
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.image(
        "https://img.icons8.com/color/96/brain.png",
        width=60
    )
    st.title("Dashboard Filters")
    st.caption("Student ID: 70177772")
    st.markdown("---")
    
    # 1 — Category Filter: Gender
    st.subheader("1. Gender Filter")
    gender_options = sorted(df_raw['Gender'].unique().tolist())
    gender_filter = st.multiselect(
        "Select Gender",
        options=gender_options,
        default=gender_options,
        key="gender"
    )
    
    st.markdown("---")
    
    # 2 — Numerical Range Slider: Age
    st.subheader("2. Age Range")
    age_min = int(df_raw['Age'].min())
    age_max = int(df_raw['Age'].max())
    age_range = st.slider(
        "Select Age Range",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max),
        key="age_slider"
    )
    
    st.markdown("---")
    
    # 3 — Multi-Select Filter: Country
    st.subheader("3. Country")
    country_options = sorted(df_raw['Country'].unique().tolist())
    country_filter = st.multiselect(
        "Select Country(s)",
        options=country_options,
        default=country_options,
        key="country"
    )
    
    st.markdown("---")
    
    # 4 — Multi-Select Filter: Treatment
    st.subheader("4. Treatment Status")
    treatment_options = df_raw['treatment'].unique().tolist()
    treatment_filter = st.multiselect(
        "Select Treatment Status",
        options=treatment_options,
        default=treatment_options,
        key="treatment"
    )
    
    st.markdown("---")
    
    # 5 — Multi-Select Filter: Remote Work
    st.subheader("5. Remote Work")
    remote_options = df_raw['remote_work'].unique().tolist()
    remote_filter = st.multiselect(
        "Select Remote Work Status",
        options=remote_options,
        default=remote_options,
        key="remote_work"
    )
    
    st.markdown("---")
    
    # 6 — Search / Text Filter
    st.subheader("6. Search / Text Filter")
    search_text = st.text_input(
        "Search (Country, State, etc.)",
        value="",
        placeholder="e.g. United States, CA...",
        key="search"
    )
    
    st.markdown("---")
    
    # 7 — Reset All Filters Button
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state.gender = gender_options
        st.session_state.age_slider = (age_min, age_max)
        st.session_state.country = country_options
        st.session_state.treatment = treatment_options
        st.session_state.remote_work = remote_options
        st.session_state.search = ""
        st.rerun()
    
    st.markdown("---")
    st.caption("Instructor: Ali Hassan Sherazi")
    st.caption("Course: Exploratory Data Analysis")

# ── Apply all filters ─────────────────────────────────────────────
df = apply_filters(
    df_raw,
    gender_filter=gender_filter,
    age_range=age_range,
    country_filter=country_filter,
    treatment_filter=treatment_filter,
    remote_filter=remote_filter,
    search_text=search_text,
)

kpi = get_kpi_metrics(df)

# ═══════════════════════════════════════════════════════════════════
# MAIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div style='background:linear-gradient(135deg,#1D3557,#2E86AB);
padding:24px 28px; border-radius:12px; margin-bottom:20px;'>
 <h1 style='color:white; margin:0; font-size:28px;'>
🧠 Mental Health in Tech Survey Dashboard
 </h1>
 <p style='color:#A8DADC; margin:6px 0 0 0; font-size:14px;'>
Student ID: 70177772  &nbsp;| &nbsp;
Dataset: Mental Health in Tech Survey  &nbsp;| &nbsp;
Course: Exploratory Data Analysis  &nbsp;| &nbsp;
Instructor: Ali Hassan Sherazi
 </p>
</div>
""", unsafe_allow_html=True)

# Filter status
if len(df) < len(df_raw):
    st.info(
        f"🔍 Filters active — showing {len(df):,} of "
        f"{len(df_raw):,} total records."
    )
else:
    st.success(f"✅ Showing all {len(df):,} records — no filters applied.")

# ── KPI Cards ─────────────────────────────────────────────────────
st.markdown(
    "<div class='section-header'>📊 KPI Summary Cards</div>",
    unsafe_allow_html=True
)
c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
kpi_items = [
    (c1, kpi['total_records'], "Total Respondents"),
    (c2, kpi['avg_age'], "Avg Age"),
    (c3, f"{kpi['treatment_yes_pct']}%", "Seek Treatment"),
    (c4, f"{kpi['family_history_pct']}%", "Family History"),
    (c5, f"{kpi['remote_work_pct']}%", "Remote Work"),
    (c6, f"{kpi['tech_company_pct']}%", "Tech Company"),
    (c7, f"{kpi['benefits_pct']}%", "Has Benefits"),
    (c8, kpi['countries'], "Countries"),
]

for col, val, label in kpi_items:
    with col:
        st.markdown(
            f"""<div class='kpi-card'>
             <div class='kpi-value'>{val}</div>
             <div class='kpi-label'>{label}</div>
             </div>""",
            unsafe_allow_html=True
        )

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SECTION 1 — DISTRIBUTION ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>📈 Section 1 — Distribution Analysis</div>",
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Chart 1 — Pie Chart: Treatment Distribution")
    st.write("Proportional breakdown of those seeking mental health treatment.")
    if len(df) > 0:
        st.pyplot(pie_chart_treatment(df))
    else:
        st.warning("No data available for current filters.")

with col2:
    st.subheader("Chart 2 — Histogram: Age Distribution")
    st.write("Frequency distribution of respondent ages with mean and median lines.")
    if len(df) > 0:
        st.pyplot(histogram_age(df))
    else:
        st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
# SECTION 2 — TREND & COMPARISON ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>📉 Section 2 — Trend & Comparison Analysis</div>",
    unsafe_allow_html=True
)
st.subheader("Chart 3 — Line Chart: Age Distribution by Treatment")
st.write("How does age distribution vary between those seeking treatment?")
if len(df) > 0:
    st.pyplot(line_chart_age_distribution(df))
else:
    st.warning("No data available for current filters.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Chart 4 — Bar Chart: Respondents by Country")
    st.write("Comparing survey participation across different countries.")
    if len(df) > 0:
        st.pyplot(bar_chart_by_country(df))
    else:
        st.warning("No data available for current filters.")

with col2:
    st.subheader("Chart 9 — Count Plot: Remote Work Distribution")
    st.write("Frequency count of remote work status by treatment.")
    if len(df) > 0:
        st.pyplot(count_plot_remote_work(df))
    else:
        st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
# SECTION 3 — RELATIONSHIP ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>🔗 Section 3 — Relationship Analysis</div>",
    unsafe_allow_html=True
)
st.subheader("Chart 5 — Scatter Plot: Age vs Work Interference")
st.write("Relationship between age and how mental health interferes with work.")
if len(df) > 0:
    st.pyplot(scatter_age_work_interfere(df))
else:
    st.warning("No data available for current filters.")

st.subheader("Chart 6 — Box Plot: Age by Treatment Status")
st.write("Spread, median, and outliers of age across treatment groups.")
if len(df) > 0:
    st.pyplot(box_plot_age_by_treatment(df))
else:
    st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
# SECTION 4 — ADVANCED ANALYSIS
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>🔬 Section 4 — Advanced Analysis</div>",
    unsafe_allow_html=True
)
st.subheader("Chart 7 — Heatmap: Feature Correlation Matrix")
st.write("Which features are most strongly correlated with seeking treatment?")
if len(df) > 0:
    st.pyplot(heatmap_correlation(df))
else:
    st.warning("No data available for current filters.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Chart 8 — Area Chart: Company Size Distribution")
    st.write("Cumulative distribution of employees by company size.")
    if len(df) > 0:
        st.pyplot(area_chart_company_size(df))
    else:
        st.warning("No data available for current filters.")

with col2:
    st.subheader("Chart 10 — Violin Plot: Age by Gender & Treatment")
    st.write("Distribution and probability density of age across gender and treatment.")
    if len(df) > 0:
        st.pyplot(violin_plot_age_by_gender(df))
    else:
        st.warning("No data available for current filters.")

# ═══════════════════════════════════════════════════════════════════
# SECTION 5 — DATA TABLE
# ═══════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='section-header'>📋 Section 5 — Filtered Data Table</div>",
    unsafe_allow_html=True
)
st.write(f"Showing {len(df):,} rows matching current filters.")

display_cols = ['Timestamp', 'Age', 'Gender', 'Country', 'state',
                'self_employed', 'family_history', 'treatment',
                'work_interfere', 'no_employees', 'remote_work',
                'tech_company', 'benefits', 'care_options',
                'wellness_program', 'seek_help', 'anonymity', 'leave']

st.dataframe(
    df[display_cols].reset_index(drop=True),
    use_container_width=True,
    height=350
)

# Download filtered data button
csv = df[display_cols].to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='mental_health_filtered_data.csv',
    mime='text/csv',
)

# ── Key Findings ──────────────────────────────────────────────────
st.markdown(
    "<div class='section-header'>💡 Key Findings & Conclusion</div>",
    unsafe_allow_html=True
)
st.markdown(f"""
| # | Finding | Detail |
|---|---------|--------|
| 1 | **Treatment Seeking Rate** | {kpi['treatment_yes_pct']}% of respondents seek treatment for mental health |
| 2 | **Family History Impact** | {kpi['family_history_pct']}% have family history of mental illness |
| 3 | **Remote Work Prevalence** | {kpi['remote_work_pct']}% work remotely in tech industry |
| 4 | **Benefits Availability** | {kpi['benefits_pct']}% have mental health benefits at work |
| 5 | **Tech Company Dominance** | {kpi['tech_company_pct']}% work at tech companies |
| 6 | **Average Age** | Respondents average {kpi['avg_age']} years old |
| 7 | **Geographic Diversity** | Survey covers {kpi['countries']} different countries |
| 8 | **Total Participation** | {kpi['total_records']} professionals participated in survey |

**Conclusion**
Mental health awareness in the tech industry is critical. The data shows significant 
portions of workers seek treatment, have family history, and work remotely. 
Company size, benefits availability, and workplace culture all impact mental health outcomes.
""")

st.success("✅ Dashboard Complete — Student ID: 70177772 | All 10 Charts | All 6 Filters")
st.caption(
    "Dataset: Mental Health in Tech Survey (OSMI) | "
    "Tools: Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit"
)