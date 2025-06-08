"""
This is a boilerplate pipeline 'reporting'
generated using Kedro 0.19.13
"""

import matplotlib.pyplot as plt

def generate_crime_score_distribution(model):
    import pandas as pd
    from pathlib import Path

    # Wczytaj dane z CSV, które były używane do treningu
    df = pd.read_csv("data/05_model_input/model_input_x.csv")
    y_pred = model.predict(df)

    # Wygeneruj wykres
    plt.figure(figsize=(10, 6))
    plt.hist(y_pred, bins=30, edgecolor='black')
    plt.title("Predicted Crime Score Distribution")
    plt.xlabel("Crime Score")
    plt.ylabel("Frequency")
    plt.grid(True)

    # Zapisz do pliku
    output_path = Path("data/07_reporting/crime_score_distribution.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path)
    plt.close()
