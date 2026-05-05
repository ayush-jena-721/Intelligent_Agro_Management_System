import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
PANCHANG_PATH = BASE_DIR / "data" / "raw" / "panchangam_dataset.jsonl"

def load_panchang():
    records = []

    with open(PANCHANG_PATH, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    df = pd.DataFrame(records)

    df["date"] = pd.to_datetime(df["date"]).dt.floor("h")
    print(df.head())
    print(df.columns)

    return df


def get_panchang_for_date(df, selected_datetime):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    target_date = pd.to_datetime(selected_datetime).date()

    row = df[df["date"].dt.date == target_date]

    if row.empty:
        # 🔥 fallback to nearest date (IMPORTANT)
        idx = (df["date"] - pd.Timestamp(selected_datetime)).abs().idxmin()
        return df.loc[[idx]]

    return row.iloc[[0]]

def merge_with_weather(weather_df, panch_row):
    weather_df = weather_df.copy()
    panch_row = panch_row.copy()

    # Ensure both are single row
    weather_df = weather_df.iloc[[0]].reset_index(drop=True)
    panch_row = panch_row.iloc[[0]].reset_index(drop=True)

    # 🔥 SIMPLE CONCAT (NO JOIN BUGS)
    df = pd.concat([weather_df, panch_row], axis=1)

    return df