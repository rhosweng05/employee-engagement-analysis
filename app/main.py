import streamlit as st
from utils import load_data, normalize_data, filter_data
from kpi import add_engagement, add_burnout, add_stress
import visuals as vz
from config import APP_TITLE, DEFAULT_THRESHOLD

# =========================
# 🔹 PAGE CONFIG
# =========================
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide"
)

st.title("📊 Employee Engagement & Burnout Dashboard")

# =========================
# 🔹 LOAD DATA
# =========================
df = load_data("Palo Alto Networks.csv")
df = normalize_data(df)

# =========================
# 🔹 SIDEBAR FILTERS
# =========================
st.sidebar.header("🔧 Filters")

dept = st.sidebar.selectbox(
    "Department",
    ["All"] + sorted(df["Department"].dropna().unique())
)

overtime = st.sidebar.selectbox(
    "OverTime", ["All", "Yes", "No"]
)

tenure = st.sidebar.slider(
    "Years at Company",
    0,
    int(df["YearsAtCompany"].max()),
    (0, 10)
)

threshold = st.sidebar.slider(
    "Engagement Threshold",
    0.0, 1.0, DEFAULT_THRESHOLD
)

# =========================
# 🔹 APPLY FILTERS
# =========================
df = filter_data(df, dept, overtime, tenure)

# =========================
# 🔹 KPI CALCULATIONS
# =========================
df = add_engagement(df)
df = add_burnout(df)
df = add_stress(df)

# =========================
# 🔹 TABS (PROFESSIONAL UI)
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview",
    "🔥 Burnout Analysis",
    "📈 Workforce Insights",
    "🚨 Manager Panel"
])

# =========================
# 📊 TAB 1: OVERVIEW
# =========================
with tab1:
    vz.show_kpis(df)
    vz.advanced_kpis(df)

    st.divider()

    vz.engagement_chart(df)

# =========================
# 🔥 TAB 2: BURNOUT
# =========================
with tab2:
    vz.burnout_chart(df)
    vz.burnout_by_department(df)

# =========================
# 📈 TAB 3: INSIGHTS
# =========================
with tab3:
    vz.joblevel_chart(df)
    vz.overtime_chart(df)

    st.divider()

    vz.tenure_analysis(df)
    vz.role_analysis(df)
    vz.travel_stress(df)

    st.divider()

    vz.correlation_heatmap(df)

# =========================
# 🚨 TAB 4: MANAGER PANEL
# =========================
with tab4:
    vz.manager_table(df, threshold)
    vz.smart_insights(df)