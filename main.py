import streamlit as st
from utils import load_data, normalize_data, filter_data
from kpi import add_engagement, add_burnout, add_stress
import visuals as vz
from config import APP_TITLE, DEFAULT_THRESHOLD

st.set_page_config(layout="wide")
st.title("📊 Employee Engagement & Burnout Dashboard")

# Load data
df = load_data("data/hr_dataset.csv")
df = normalize_data(df)

# Sidebar filters
st.sidebar.header("🔧 Filters")

dept = st.sidebar.selectbox(
    "Department",
    ["All"] + list(df["Department"].unique())
)

overtime = st.sidebar.selectbox(
    "OverTime", ["All", "Yes", "No"]
)

tenure = st.sidebar.slider(
    "Years at Company",
    0, int(df["YearsAtCompany"].max()), (0,10)
)

threshold = st.sidebar.slider(
    "Engagement Threshold",
    0.0, 1.0, DEFAULT_THRESHOLD
)

# Apply filters
df = filter_data(df, dept, overtime, tenure)

# Add KPIs
df = add_engagement(df)
df = add_burnout(df)
df = add_stress(df)
df = add_advanced_flags(df)

# KPIs
vz.show_kpis(df)

st.divider()

# Charts
vz.engagement_chart(df)
vz.burnout_chart(df)

st.divider()

vz.joblevel_chart(df)
vz.overtime_chart(df)

st.divider()

# Manager Panel
vz.manager_table(df, threshold)