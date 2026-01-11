from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import json
import requests
import pandas as pd
from sqlalchemy import create_engine

# config
BASE_DIR = "/Users/manavgupta/PycharmProjects/weatherdatapipeline"
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
DB_PATH = os.path.join(BASE_DIR, "weather.db")
API_KEY = os.getenv("OPENWEATHER_API_KEY")


def extract_weather():
    os.makedirs(RAW_DIR, exist_ok=True)
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Ludhiana&appid={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()

    file_path = os.path.join(
        RAW_DIR, f"weather_{datetime.now().strftime('%Y%m%d_%H')}.json"
    )
    with open(file_path, "w") as f:
        json.dump(response.json(), f)
    return file_path


def transform_weather(**context):
    file_path = context['ti'].xcom_pull(task_ids='extract_weather')
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    with open(file_path) as f:
        data = json.load(f)

    df = pd.DataFrame([{
        "city": data["name"],
        "temperature_c": round(data["main"]["temp"] - 273.15, 2),
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["main"],
        "timestamp": datetime.fromtimestamp(data["dt"])
    }])

    output_path = os.path.join(
        PROCESSED_DIR, os.path.basename(file_path).replace(".json", ".csv")
    )
    df.to_csv(output_path, index=False)
    return output_path


def load_weather(**context):
    csv_path = context['ti'].xcom_pull(task_ids='transform_weather')
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df = pd.read_csv(csv_path)
    df.to_sql("weather_data", engine, if_exists="append", index=False)


with DAG(
    dag_id="hourly_weather_etl",
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 * * * *",
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id="extract_weather",
        python_callable=extract_weather
    )

    transform = PythonOperator(
        task_id="transform_weather",
        python_callable=transform_weather,
        provide_context=True
    )

    load = PythonOperator(
        task_id="load_weather",
        python_callable=load_weather,
        provide_context=True
    )

    extract >> transform >> load
