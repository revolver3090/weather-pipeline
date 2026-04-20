# 🌦️ Weather Data Pipeline (Airflow + BigQuery + Terraform)

## 🚀 Overview

This project implements an end-to-end data pipeline that:

- Extracts weather data from a public API
- Loads raw data into BigQuery
- Transforms data into aggregated format (multi-city)
- Validates data quality
- Visualizes results in Looker Studio
- Manages infrastructure using Terraform

---

## ❓ Problem Statement

Organizations often need to monitor and compare environmental conditions across multiple locations, but raw weather data is:

- Fragmented across APIs
- Not structured for analysis
- Difficult to compare across cities over time

This project solves that by building a pipeline that:

- Centralizes weather data into a single data warehouse
- Standardizes and aggregates the data
- Enables easy comparison of temperature trends across multiple cities
--

## 🧱 Architecture

Terraform → BigQuery → Airflow (Docker) → Looker Studio

---

## ⚙️ Tech Stack

- Apache Airflow (Docker)
- Google BigQuery
- Terraform
- Looker Studio
- Python
- Git

---

## 🧩 Prerequisites

Make sure you have installed:

### 💻 Software

- Docker Desktop
- Python 3.8+
- Git
- Terraform

---

### ☁️ Google Cloud Platform (GCP)

1. Create a GCP project  
2. Enable BigQuery API  
3. Create a Service Account  
4. Assign roles:
   - BigQuery Data Editor  
   - BigQuery Job User  
5. Download `key.json`

###

🚀Reproducibility
1️⃣ Clone the repository

git clone https://github.com/revolver3090/weather-pipeline.git

cd weather-pipeline

2️⃣ Configure environment

Create your .env file:
AIRFLOW_UID=50000

3️⃣ Add credentials

Place your file:

keys/key.json

4️⃣ Provision infrastructure (Terraform)

cd terraform

terraform init

terraform apply

This will create:

Dataset: weather_data

Tables: raw_weather
clean_weather

5️⃣ Run Airflow

cd ..

docker compose up


Wait 1–2 minutes.

Open:

http://localhost:8080

#Airflow Connection Setup

In Airflow UI:

Conn Id: google_cloud_default

Conn Type: Google Cloud

Project Id: your GCP project ID

Keyfile JSON: paste the content of key.json

6️⃣ Run the pipeline

Enable DAG: weather_pipeline

Click Trigger DAG

🔄 Pipeline Description

1. Extract & Load

Calls weather API

Inserts data into raw_weather

Supports multiple cities:

Mexico City
Guadalajara
Monterrey


📊 Visualization (Looker Studio)
Connect to BigQuery

Select table: clean_weather

Recommended chart:
Dimension: fecha
Metric: temp_promedio
Breakdown: city

fecha       | city        | temp_promedio
----------------------------------------
2026-04-20  | CDMX        | 22.1
2026-04-20  | Guadalajara | 24.3

⚠️ Notes
Service Account is created manually (IAM permissions)
key.json must NOT be uploaded to GitHub
Use .env for reproducibility
