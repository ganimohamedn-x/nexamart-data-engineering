from pathlib import Path
from google.cloud import bigquery

# Find the project's SQL folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = PROJECT_DIR / "sql"

# Connect to BigQuery.
client = bigquery.Client(project="nexamart-data-engineering")

# List the SQL files in the order we want to run them.
sql_files = [
    "monthly_sales.sql",
    "product_performance.sql",
    "customer_spending.sql",
]

# Run each SQL transformation.
for filename in sql_files:
    sql_file = SQL_DIR / filename

    print(f"Running {filename}...")

    sql = sql_file.read_text()
    job = client.query(sql)
    job.result()

    print(f"Completed {filename} successfully!")

print("All pipeline transformations completed!")
