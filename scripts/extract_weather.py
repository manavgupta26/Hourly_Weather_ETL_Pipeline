import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

URL = (
    "https://api.openweathermap.org/data/2.5/weather?"
    "q=Ludhiana&appid=" + API_KEY
)

# ✅ Get project root safely
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")

def extract_weather():
    response = requests.get(URL)
    response.raise_for_status()

    os.makedirs(RAW_DIR, exist_ok=True)

    file_path = os.path.join(
        RAW_DIR,
        f"weather_{datetime.now().strftime('%Y%m%d_%H')}.json"
    )

    with open(file_path, "w") as f:
        json.dump(response.json(), f)

    return file_path
