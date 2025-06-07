import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split

def prepare_model_input(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, OneHotEncoder]:
    df = df.copy()

    categorical_cols = ["area", "crime_type", "hour_bin", "season", "weekday"]
    df = df.dropna(subset=categorical_cols)

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    encoded = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(categorical_cols))

    y = pd.Series(1, index=df.index, name="crime_count")

    return encoded_df, y, encoder


def train_model(X: pd.DataFrame, y: pd.Series) -> Ridge:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = Ridge(alpha=1.0)
    model.fit(X_train, y_train)

    print(f"Train R² score: {model.score(X_train, y_train):.3f}")
    print(f"Test R² score: {model.score(X_test, y_test):.3f}")
    return model
