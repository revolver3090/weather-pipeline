provider "google" {
  project     = var.project_id
  region      = "us-central1"
  credentials = file("C:/Users/Gerardo/airflow-project/keys/key.json")
}
# Dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "weather_data"
  location   = "US"
}

# Tabla raw
resource "google_bigquery_table" "raw_weather" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "raw_weather"

  schema = jsonencode([
    {
      name = "timestamp"
      type = "TIMESTAMP"
      mode = "NULLABLE"
    },
    {
      name = "temperature"
      type = "FLOAT"
      mode = "NULLABLE"
    },
    {
      name = "city"
      type = "STRING"
      mode = "NULLABLE" 
    }
      
  ])
}

# 📊 Tabla clean
resource "google_bigquery_table" "clean_weather" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "clean_weather"

  schema = jsonencode([
    {
      name = "date"
      type = "DATE"
      mode = "NULLABLE"
    },
    {
      name = "city"
      type = "STRING"
      mode = "NULLABLE"
    },
    {
      
      name = "temp_average"
      type = "FLOAT"
      mode = "NULLABLE"
    }
  ])
}