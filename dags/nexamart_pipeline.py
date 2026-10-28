from datetime import timedelta
from pathlib import Path

import pendulum
from airflow.sdk import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryInsertJobOperator,
)

PROJECT_ID = "nexamart-data-engineering"
PROJECT_DIR = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_DIR / "sql"

default_args = {
    "owner": "nexamart",
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="nexamart_analytics_pipeline",
    description="Transform NexaMart data in BigQuery",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 10, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["nexamart", "bigquery", "analytics"],
) as dag:

    monthly_sales = BigQueryInsertJobOperator(
        task_id="monthly_sales",
        project_id=PROJECT_ID,
	location="africa-south1",
        configuration={
            "query": {
                "query": (SQL_DIR / "monthly_sales.sql").read_text(),
                "useLegacySql": False,
            }
        },
    )

    product_performance = BigQueryInsertJobOperator(
        task_id="product_performance",
        project_id=PROJECT_ID,
	location="africa-south1",
        configuration={
            "query": {
                "query": (SQL_DIR / "product_performance.sql").read_text(),
                "useLegacySql": False,
            }
        },
    )

    customer_spending = BigQueryInsertJobOperator(
        task_id="customer_spending",
        project_id=PROJECT_ID,
	location="africa-south1",
        configuration={
            "query": {
                "query": (SQL_DIR / "customer_spending.sql").read_text(),
                "useLegacySql": False,
            }
        },
    )

    monthly_sales >> product_performance >> customer_spending
