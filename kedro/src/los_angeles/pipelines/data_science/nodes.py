import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

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


def train_model(X: pd.DataFrame, y: pd.Series, model_options: dict) -> Ridge:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=model_options["test_size"],
        random_state=model_options["random_state"])

    model = Ridge(alpha=model_options["alpha"])
    model.fit(X_train, y_train)

    print(f"Train R² score: {model.score(X_train, y_train):.3f}")
    print(f"Test R² score: {model.score(X_test, y_test):.3f}")
    return model
