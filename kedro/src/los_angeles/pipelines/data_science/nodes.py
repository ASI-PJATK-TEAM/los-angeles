import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt

def prepare_model_input(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, OneHotEncoder]:
    df = df.copy()
    print("PREP INPUT COLS:", df.columns)
    categorical_cols = ["area", "hour_bin", "weekday", "season"]
    df = df.dropna(subset=categorical_cols)

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))

    y = df["crime_count"]

    return encoded_df, y, encoder


def train_automl_model(X: pd.DataFrame, y: pd.Series,
                       params: dict):
    y_series = y.iloc[:, 0].rename("crime_count")
    train_df = pd.concat([X, y_series], axis=1)

    predictor = TabularPredictor(
        label="crime_count",
        path="data/06_models/crime_model"
    ).fit(
        train_df,
        time_limit=params["time_limit"],
        presets=params["presets"],
        verbosity=params["verbosity"],
    )

    print("\n📊 Leaderboard:")
    leaderboard_df = predictor.leaderboard(silent=False)

    print("\n📄 Fit Summary:")
    predictor.fit_summary()

    print("\n🔥 Feature Importance:")
    fi_df = predictor.feature_importance(train_df)
    fi_df.head(20).plot(kind="barh", y="importance", figsize=(8, 10), title="Top 20 Feature Importances")
    plt.gca().invert_yaxis()
    plt.xlabel("Importance (increase in RMSE when shuffled)")
    plt.ylabel("Feature")
    plt.tight_layout()
    plt.savefig("data/07_reporting/feature_importance.png")
    plt.close()

    leaderboard_df.to_csv("data/07_reporting/leaderboard.csv", index=False)
    fi_df.to_csv("data/07_reporting/feature_importance.csv", index=False)

    return predictor