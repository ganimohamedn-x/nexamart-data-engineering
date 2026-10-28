# NexaMart — Cloud Data Engineering Pipeline

NexaMart is a retail analytics data engineering project that transforms customer, product, order, and order-item data into business-ready insights using Google Cloud Platform.

The project demonstrates cloud data storage, SQL-based analytics, workflow orchestration with Apache Airflow, and interactive visualization with Streamlit.

## Project Overview

Retail businesses need reliable ways to transform raw operational data into useful insights. NexaMart demonstrates a cloud-based workflow for organizing retail data, generating analytical tables, and presenting results through a dashboard.

### Architecture

```text
Retail CSV Data
      |
      v
Google Cloud Storage
   (Raw Data)
      |
      v
Google BigQuery
   (SQL Analytics)
      |
      v
Analytical Tables
      |
      +-------------------+
      |                   |
      v                   v
 Apache Airflow      Streamlit Dashboard
 (Orchestration)     (Visualization)
```

*Apache Airflow orchestrates the SQL transformation tasks. The Streamlit dashboard presents the resulting analytics.*

## Technologies Used

- **Google Cloud Storage:** Stores raw CSV source data.
- **Google BigQuery:** Provides cloud-based data storage and SQL analytics.
- **Apache Airflow:** Orchestrates the analytical SQL tasks and tracks their execution status.
- **Python:** Supports pipeline execution and application development.
- **Streamlit:** Provides an interactive dashboard for exploring analytical results.
- **SQL:** Transforms retail data into reporting tables.
- **Git and GitHub:** Version control and project documentation.

## Data Sources

The project uses four CSV datasets:

| Dataset | Number of records |
|---|---:|
| Customers | 500 |
| Products | 30 |
| Orders | 1,000 |
| Order items | 2,500 |

These datasets represent the raw retail data used by the analytics workflow.

## Analytics Pipeline

The project generates three analytical tables in BigQuery:

### 1. Monthly Sales
Aggregates sales data by month to support revenue trend analysis.

### 2. Product Performance
Summarizes product-level performance to help identify products contributing to sales.

### 3. Customer Spending
Aggregates customer spending to support customer-level purchasing analysis.

Apache Airflow manages these three tasks through the `nexamart_analytics_pipeline` DAG:

- `monthly_sales`
- `product_performance`
- `customer_spending`

The DAG has been manually triggered and successfully completed with all three tasks reporting success.

## Google Cloud Resources

The project uses the following BigQuery project and datasets:

- **Google Cloud project:** `nexamart-data-engineering`
- **Raw dataset:** `nexamart_raw`
- **Staging dataset:** `nexamart_staging`
- **Analytics dataset:** `nexamart_analytics`
- **BigQuery region:** `africa-south1`

The analytical outputs are stored in the analytics dataset.

## Dashboard

The Streamlit dashboard provides a visual interface for exploring the project's analytical outputs.

The dashboard was successfully launched during development. Its purpose is to make the results of the SQL transformations easier to inspect and understand.

## Repository Structure

```text
nexamart-data-engineering/
├── config/
├── dags/
│   └── nexamart_pipeline.py
├── dashboard/
├── data/
├── docs/
├── sql/
│   ├── monthly_sales.sql
│   ├── product_performance.sql
│   └── customer_spending.sql
├── src/
│   └── run_pipeline.py
├── tests/
└── README.md
```

## Project Goals

This project was built to develop practical experience with:

- Cloud-based data storage and analytics.
- SQL transformations and analytical data modeling.
- Workflow orchestration with Apache Airflow.
- Python-based pipeline execution.
- Interactive business intelligence dashboards.
- Version control and project documentation.

## Future Improvements

Potential next steps include:

- Automating pipeline execution on a recurring schedule.
- Expanding data quality checks and pipeline failure handling.
- Adding pipeline monitoring and logging.
- Improving dashboard interactivity and business metrics.
- Documenting setup and deployment steps for reproducibility.

## Author

**Mohamed Noor Gani**

Management Information Systems graduate building practical experience in cloud data engineering, business systems, analytics, and process automation.

Project repository: [NexaMart Data Engineering](https://github.com/ganimohamedn-x/nexamart-data-engineering)
