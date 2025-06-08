from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import pickle

app = FastAPI()

with open("../kedro/data/06_models/crime_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("../kedro/data/06_models/model_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

class CrimeRequest(BaseModel):
    area: str
    date: str  # YYYY-MM-DD

def get_hour_bin(hour):
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def get_season(month):
    return {
        12: "winter", 1: "winter", 2: "winter",
        3: "spring", 4: "spring", 5: "spring",
        6: "summer", 7: "summer", 8: "summer",
        9: "autumn", 10: "autumn", 11: "autumn"
    }[month]

def prepare_features_from_input(area: str, date_str: str) -> pd.DataFrame:
    date = datetime.strptime(date_str, "%Y-%m-%d")
    hour = date.hour
    weekday = date.weekday()
    month = date.month
    season = get_season(month)
    hour_bin = get_hour_bin(hour)

    df = pd.DataFrame([{
        "area": area,
        "hour_bin": hour_bin,
        "weekday": weekday,
        "season": season
    }])

    encoded = encoder.transform(df)
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out())
    return encoded_df

def classify_crime_risk(score: float) -> str:
    if score <= 300:
        return "Low"
    elif score <= 500:
        return "Medium"
    elif score <= 700:
        return "High"
    else:
        return "Very High"

@app.post("/predict")
def predict_crime(req: CrimeRequest):
    features_df = prepare_features_from_input(req.area, req.date)
    prediction = model.predict(features_df)[0]
    risk = classify_crime_risk(prediction)
    return {
        "predicted_crime_score": float(prediction),
        "risk_level": risk
    }