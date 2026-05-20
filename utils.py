import pandas as pd
from config import ENGAGEMENT_COLS

def load_data(path):
    df = pd.read_csv(path)
    return df

def normalize_data(df):
    df[ENGAGEMENT_COLS] = df[ENGAGEMENT_COLS] / 4
    return df

def filter_data(df, dept, overtime, tenure):
    if dept != "All":
        df = df[df["Department"] == dept]

    if overtime != "All":
        df = df[df["OverTime"] == overtime]

    df = df[
        (df["YearsAtCompany"] >= tenure[0]) &
        (df["YearsAtCompany"] <= tenure[1])
    ]

    return df