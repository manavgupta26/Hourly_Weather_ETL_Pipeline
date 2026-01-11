import os
import json
import pandas as pd
from datetime import datetime

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

def transform_weather(file_path):
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # ✅ Convert relative path → absolute path
    if not os.path.isabs(file_path):
        file_path = os.path.join(BASE_DIR, file_path)

    with open(file_path) as f:
        data = json.load(f)

    transformed = {
        "city": data["name"],
        "temperature_c": round(data["main"]["temp"] - 273.15, 2),
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["main"],
        "timestamp": datetime.fromtimestamp(data["dt"])
    }

    df = pd.DataFrame([transformed])

    output_path = os.path.join(
        PROCESSED_DIR,
        os.path.basename(file_path).replace(".json", ".csv")
    )

    df.to_csv(output_path, index=False)
    return output_path

