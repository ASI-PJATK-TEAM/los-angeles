from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
from autogluon.tabular import TabularPredictor
import os

app = FastAPI()
local_path = "../kedro/data/06_models/crime_model/"
prod_path = "./model"

value = os.getenv("ENV", "local")

if value == "prod":
    local_path = prod_path

model = TabularPredictor(local_path)

AREAS = [
    "77th Street", "Central", "Devonshire", "Foothill", "Harbor", "Hollenbeck", "Hollywood",
    "Mission", "N Hollywood", "Newton", "Northeast", "Olympic", "Pacific", "Rampart",
    "Southeast", "Southwest", "Topanga", "Van Nuys", "West LA", "West Valley", "Wilshire"
]

class CrimeRequest(BaseModel):
    area: str
    date: str  # YYYY-MM-DD

def get_hour_bin(hour: int) -> str:
    if 6 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def get_season(month: int) -> str:
    return {
        12: "winter", 1: "winter", 2: "winter",
        3: "spring", 4: "spring", 5: "spring",
        6: "summer", 7: "summer", 8: "summer",
        9: "autumn", 10: "autumn", 11: "autumn"
    }[month]

def prepare_features_from_input(area: str, date: str) -> pd.DataFrame:
    dt = datetime.strptime(date, "%Y-%m-%d")
    hour_bin = get_hour_bin(dt.hour)
    season = get_season(dt.month)
    weekday = dt.weekday()

    data = {}

    # one-hot dla area
    for a in AREAS:
        data[f"area_{a}"] = [1 if a == area else 0]

    # one-hot dla hour_bin
    for bin in ["morning", "afternoon", "evening", "night"]:
        data[f"hour_bin_{bin}"] = [1 if bin == hour_bin else 0]

    # one-hot dla weekday
    for i in range(7):
        data[f"weekday_{i}"] = [1 if i == weekday else 0]

    # one-hot dla season
    for s in ["winter", "spring", "summer", "fall"]:
        data[f"season_{s}"] = [1 if s == season else 0]

    return pd.DataFrame(data)

def classify_crime_risk(score: float) -> str:
    if score < 350:
        return "Low"
    elif score < 500:
        return "Medium"
    elif score < 700:
        return "High"
    else:
        return "Very High"


@app.post("/predict")
def predict_crime(req: CrimeRequest):
    features_df = prepare_features_from_input(req.area, req.date)
    print(model.feature_metadata.to_dict())
    prediction = model.predict(features_df)[0]
    risk = classify_crime_risk(prediction)

    return {
        "predicted_crime_score": float(prediction),
        "risk_level": risk
    }