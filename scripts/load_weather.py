import os
import pandas as pd
from sqlalchemy import create_engine

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "weather.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

def load_weather(csv_path):
    # Convert relative path → absolute
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(BASE_DIR, csv_path)

    df = pd.read_csv(csv_path)

    df.to_sql(
        "weather_data",
        engine,
        if_exists="append",
        index=False
    )

    print("Data appended to database")

