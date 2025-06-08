import os
import subprocess
from pathlib import Path

def download_dataset():
    raw_dir = Path("kedro/data/01_raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    dataset_file = raw_dir / "crime_raw.csv"
    if dataset_file.exists():
        print("✅ Dataset already exists.")
        return

    print("📥 Downloading dataset from Kaggle...")

    kaggle_token = Path(".kaggle/kaggle.json")
    if kaggle_token.exists():
        os.environ["KAGGLE_CONFIG_DIR"] = str(kaggle_token.parent.resolve())
    else:
        raise FileNotFoundError("❌ Missing .kaggle/kaggle.json file!")

    subprocess.run([
        "kaggle", "datasets", "download",
        "-d", "samithsachidanandan/crime-data-from-2020-to-present",
        "-p", str(raw_dir),
        "--unzip"
    ], check=True)

    for file in raw_dir.glob("*.csv"):
        if file.name != "crime_raw.csv":
            file.rename(raw_dir / "crime_raw.csv")
            print(f"✅ Renamed '{file.name}' to 'crime_raw.csv'")
            break

    print("✅ Dataset downloaded and extracted to kedro/data/01_raw/")

if __name__ == "__main__":
    download_dataset()