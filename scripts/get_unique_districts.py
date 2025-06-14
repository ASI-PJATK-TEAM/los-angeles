import pandas as pd
from pathlib import Path

# Ścieżka do pliku CSV
csv_path = Path("kedro/data/01_raw/crime_raw.csv")
output_path = csv_path.parent / "unique_regions.csv"

# Wczytaj dane
df = pd.read_csv(csv_path, low_memory=False)

# Wyciągnij unikalne regiony
regions = df[["AREA", "AREA NAME"]].drop_duplicates().sort_values("AREA")

# Zapisz do pliku CSV
regions.to_csv(output_path, index=False)

print(f"✅ Saved unique regions to: {output_path}")