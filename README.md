# 🌦️ Weather Data ETL Pipeline using Apache Airflow

## 📌 Project Overview
This project implements an **end-to-end ETL pipeline** using **Apache Airflow**.  
The pipeline extracts real-time weather data from an external API, transforms the raw data into a structured format, and prepares it for further analysis or storage.

The project focuses on understanding **workflow orchestration**, **DAG scheduling**, and **ETL best practices** using Airflow.

---

## 🏗️ Architecture
Weather API → Extract → Transform → Load

---

## 🛠️ Tech Stack
- Apache Airflow
- Python 3.10
- REST APIs
- Virtual Environment (venv)

---

DAG Details

DAG Name: hourly_weather_etl
Schedule: Hourly

Tasks:

extract_weather – Fetches weather data from API

transform_weather – Cleans and formats raw data

load_weather – Loads processed data (optional)

Setup Instructions

Clone the repository
git clone <repository-url>
cd airflow

Create virtual environment
python3.10 -m venv .venv
source .venv/bin/activate

Install dependencies
pip install -r requirements.txt

Initialize Airflow
airflow db init

Start Airflow services
airflow scheduler
airflow webserver

Airflow UI will be available at:
http://localhost:8080

Running the Pipeline

Open Airflow UI

Enable the hourly_weather_etl DAG

Trigger the DAG manually or wait for the scheduled run

Monitor task logs for execution status

Key Learnings

DAG creation and scheduling in Apache Airflow

ETL pipeline design

PythonOperator usage

Task dependencies and execution order

Debugging Airflow logs

Future Enhancements

Load data into PostgreSQL or AWS S3

Add data validation and quality checks

Implement alerts and retries

Dockerize the Airflow environment
