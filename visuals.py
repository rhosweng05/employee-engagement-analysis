import plotly.express as px
import streamlit as st

def show_kpis(df):
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Avg Engagement", round(df["EngagementScore"].mean(), 2))
    c2.metric("High Burnout %", round((df["BurnoutRisk"]=="High").mean()*100,2))
    c3.metric("Avg WLB", round(df["WorkLifeBalance"].mean(), 2))
    c4.metric("Attrition %", round(df["Attrition"].mean()*100,2))


def engagement_chart(df):
    fig = px.histogram(
        df, x="EngagementScore", color="Attrition",
        title="Engagement vs Attrition"
    )
    st.plotly_chart(fig, use_container_width=True)


def burnout_chart(df):
    fig = px.pie(
        df, names="BurnoutRisk",
        title="Burnout Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)


def joblevel_chart(df):
    fig = px.box(
        df, x="JobLevel", y="EngagementScore",
        color="Department",
        title="Job Level vs Engagement"
    )
    st.plotly_chart(fig, use_container_width=True)


def overtime_chart(df):
    fig = px.bar(
        df.groupby("OverTime")["EngagementScore"].mean().reset_index(),
        x="OverTime", y="EngagementScore",
        title="Overtime Impact on Engagement"
    )
    st.plotly_chart(fig, use_container_width=True)


def manager_table(df, threshold):
    st.subheader("🚨 High-Risk Employees")

    risky = df[df["EngagementScore"] < threshold]

    st.dataframe(
        risky[[
            "JobRole", "Department", "EngagementScore",
            "BurnoutRisk", "OverTime", "WorkLifeBalance"
        ]]
    )