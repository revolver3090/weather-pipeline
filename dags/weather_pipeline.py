from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from datetime import datetime
import requests
from google.cloud import bigquery

# Configuration
PROJECT_ID = "weather-pipeline-493600"
DATASET = "weather_data"
RAW_TABLE = "raw_weather"
CLEAN_TABLE = "clean_weather"

# 1. EXTRACT + LOAD (API → BigQuery raw)
def extract_and_load():
    cities = {
        "CDMX": (19.43, -99.13),
        "Guadalajara": (20.67, -103.35),
        "Monterrey": (25.68, -100.31)
    }

    client = bigquery.Client()
    rows = []

    for city, (lat, lon) in cities.items():
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m"
        data = requests.get(url).json()

        for t, temp in zip(data["hourly"]["time"], data["hourly"]["temperature_2m"]):
            rows.append({
                "timestamp": t,
                "temperature": temp,
                "city": city
            })
    table_id = f"{PROJECT_ID}.{DATASET}.{RAW_TABLE}"
    errors = client.insert_rows_json(table_id, rows)

    if errors:
        raise Exception(f"Errors when inserting: {errors}")
    else:
        print(f"inserted {len(rows)} rows in {table_id}")

# 2. TRANSFORM (BigQuery SQL)
transform_query = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET}.{CLEAN_TABLE}` AS
SELECT
  DATE(TIMESTAMP(timestamp)) AS date,
  city,
  AVG(temperature) AS temp_average
FROM `{PROJECT_ID}.{DATASET}.{RAW_TABLE}`
GROUP BY date, city
"""

# 3. VALIDATE (check data)
def validate():
    client = bigquery.Client()

    query = f"""
    SELECT COUNT(*) as total
    FROM `{PROJECT_ID}.{DATASET}.{CLEAN_TABLE}`
    """

    result = list(client.query(query))[0][0]

    if result == 0:
        raise Exception("Table clean is empty")
    else:
        print(f"✔ Valid data: {result} rows in  clean_weather")

# DAG
with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["weather", "bigquery", "etl"]
) as dag:

    extract_task = PythonOperator(
        task_id="extract_and_load",
        python_callable=extract_and_load
    )

    transform_task = BigQueryInsertJobOperator(
        task_id="transform_data",
        configuration={
            "query": {
                "query": transform_query,
                "useLegacySql": False,
            }
        },
        gcp_conn_id="google_cloud_default"
    )

    validate_task = PythonOperator(
        task_id="validate_data",
        python_callable=validate
    )

    # Task Flow
    extract_task >> transform_task >> validate_task