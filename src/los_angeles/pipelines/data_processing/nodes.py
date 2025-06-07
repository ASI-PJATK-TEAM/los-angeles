import pandas as pd

def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[[
        "DR_NO", "DATE OCC", "TIME OCC", "AREA NAME", "Crm Cd Desc", "LAT", "LON"
    ]].copy()

    df["date"] = pd.to_datetime(df["DATE OCC"], errors="coerce")

    df["hour"] = df["TIME OCC"].astype(str).str.zfill(4).str[:2].astype(int)

    df.rename(columns={
        "DR_NO": "event_id",
        "AREA NAME": "area",
        "Crm Cd Desc": "crime_type",
        "LAT": "lat",
        "LON": "lon"
    }, inplace=True)

    df.dropna(subset=["date", "lat", "lon"], inplace=True)

    df = df.sort_values("date").reset_index(drop=True)

    return df[["event_id", "date", "hour", "area", "crime_type", "lat", "lon"]]

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df["weekday"] = df["date"].dt.dayofweek  # Monday=0, Sunday=6
    df["is_weekend"] = df["weekday"].isin([5, 6])

    df["month"] = df["date"].dt.month
    df["season"] = df["month"].map({
        12: "winter", 1: "winter", 2: "winter",
        3: "spring", 4: "spring", 5: "spring",
        6: "summer", 7: "summer", 8: "summer",
        9: "fall", 10: "fall", 11: "fall"
    })

    df["hour_bin"] = pd.cut(df["hour"], bins=[0, 6, 12, 18, 24], labels=["night", "morning", "afternoon", "evening"], right=False)

    return df

def aggregate_crime(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    agg_df = df.groupby(
        ["area", "weekday", "hour_bin", "crime_type"]
    ).size().reset_index(name="crime_count")

    return agg_df