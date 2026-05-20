import plotly.express as px
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# =========================
# 🔹 KPI SECTION
# =========================
def show_kpis(df):
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Avg Engagement", round(df["EngagementScore"].mean(), 2))

    c2.metric("High Burnout %",
              round((df["BurnoutRisk"] == "High").mean() * 100, 2))

    c3.metric("Avg Work-Life Balance",
              round(df["WorkLifeBalance"].mean(), 2))

    c4.metric("Attrition %",
              round(df["Attrition"].mean() * 100, 2))


def advanced_kpis(df):
    st.subheader("📊 Advanced Workforce KPIs")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Avg Stress Score",
              round(df["WorkStressScore"].mean(), 2))

    c2.metric("Overtime %",
              round((df["OverTime"] == "Yes").mean() * 100, 2))

    c3.metric("Low WLB %",
              round((df["WorkLifeBalance"] <= 2).mean() * 100, 2))

    c4.metric("High Engagement %",
              round((df["EngagementScore"] > 0.7).mean() * 100, 2))


# =========================
# 🔹 BASIC CHARTS
# =========================
def engagement_chart(df):
    st.subheader("📊 Engagement vs Attrition")

    fig = px.histogram(
        df,
        x="EngagementScore",
        color="Attrition",
        marginal="box",
        nbins=20
    )

    st.plotly_chart(fig, use_container_width=True)


def burnout_chart(df):
    st.subheader("🔥 Burnout Distribution")

    fig = px.pie(
        df,
        names="BurnoutRisk",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================
# 🔹 ADVANCED ANALYTICS
# =========================

def burnout_by_department(df):
    st.subheader("🔥 Burnout by Department")

    temp = df.groupby(["Department", "BurnoutRisk"]).size().reset_index(name="Count")

    fig = px.bar(
        temp,
        x="Department",
        y="Count",
        color="BurnoutRisk",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)


def joblevel_chart(df):
    st.subheader("📈 Job Level vs Engagement")

    fig = px.box(
        df,
        x="JobLevel",
        y="EngagementScore",
        color="Department"
    )

    st.plotly_chart(fig, use_container_width=True)


def overtime_chart(df):
    st.subheader("⏱️ Overtime Impact on Engagement")

    temp = df.groupby("OverTime")["EngagementScore"].mean().reset_index()

    fig = px.bar(
        temp,
        x="OverTime",
        y="EngagementScore",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)


def tenure_analysis(df):
    st.subheader("📈 Tenure vs Engagement")

    fig = px.scatter(
        df,
        x="YearsAtCompany",
        y="EngagementScore",
        color="Attrition",
        trendline="ols"
    )

    st.plotly_chart(fig, use_container_width=True)


def role_analysis(df):
    st.subheader("💼 Role-wise Engagement")

    fig = px.box(
        df,
        x="JobRole",
        y="EngagementScore",
        color="Attrition"
    )

    st.plotly_chart(fig, use_container_width=True)


def travel_stress(df):
    st.subheader("✈️ Travel Impact on Stress")

    fig = px.box(
        df,
        x="BusinessTravel",
        y="WorkStressScore",
        color="Attrition"
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================
# 🔹 CORRELATION HEATMAP
# =========================
def correlation_heatmap(df):
    st.subheader("📊 Correlation Heatmap")

    numeric_df = df.select_dtypes(include='number')

    fig, ax = plt.subplots()
    sns.heatmap(numeric_df.corr(), cmap="coolwarm", ax=ax)

    st.pyplot(fig)


# =========================
# 🔹 MANAGER PANEL
# =========================
def manager_table(df, threshold):
    st.subheader("🚨 High-Risk Employees")

    risky = df[df["EngagementScore"] < threshold]

    st.dataframe(
        risky[
            [
                "JobRole",
                "Department",
                "EngagementScore",
                "BurnoutRisk",
                "OverTime",
                "WorkLifeBalance"
            ]
        ]
    )


# =========================
# 🔹 SMART INSIGHTS
# =========================
def smart_insights(df):
    st.subheader("🧠 Smart Insights")

    burnout_rate = (df["BurnoutRisk"] == "High").mean() * 100
    attrition_rate = df["Attrition"].mean() * 100
    wlb = df["WorkLifeBalance"].mean()

    if burnout_rate > 30:
        st.warning("⚠️ High burnout detected across workforce")

    if attrition_rate > 20:
        st.error("🚨 Attrition rate is critically high")

    if wlb < 2.5:
        st.info("💡 Work-life balance needs improvement")

    st.success("✅ Monitor overtime and improve employee experience to reduce attrition.")