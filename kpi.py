from config import ENGAGEMENT_COLS, BURNOUT_WLB_THRESHOLD

def add_engagement(df):
    df["EngagementScore"] = df[ENGAGEMENT_COLS].mean(axis=1)
    return df

def add_burnout(df):
    df["BurnoutRisk"] = "Low"

    mask = (
        (df["OverTime"] == "Yes") &
        (df["WorkLifeBalance"] <= BURNOUT_WLB_THRESHOLD)
    )

    df.loc[mask, "BurnoutRisk"] = "High"
    return df

def add_stress(df):
    df["TravelFlag"] = (df["BusinessTravel"] != "Non-Travel").astype(int)
    df["OvertimeFlag"] = (df["OverTime"] == "Yes").astype(int)

    df["WorkStressScore"] = df["TravelFlag"] + df["OvertimeFlag"]
    return df