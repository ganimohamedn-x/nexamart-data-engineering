
import streamlit as st
import pandas as pd
from google.cloud import bigquery

# --------------------------------------------------
# Page setup
# --------------------------------------------------
st.set_page_config(
    page_title="NexaMart Analytics",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 NexaMart Analytics")
st.caption("Cloud-powered e-commerce sales and customer insights")

# --------------------------------------------------
# Connect to BigQuery
# --------------------------------------------------
@st.cache_resource
def get_client():
    return bigquery.Client(project="nexamart-data-engineering")


client = get_client()


@st.cache_data(ttl=300)
def load_table(table_name):
    query = f"""
        SELECT *
        FROM `nexamart-data-engineering.nexamart_analytics.{table_name}`
    """
    return client.query(query).to_dataframe()


# --------------------------------------------------
# Load analytics data
# --------------------------------------------------
try:
    monthly_sales = load_table("monthly_sales")
    products = load_table("product_performance")
    customers = load_table("customer_spending")

    # Ensure consistent date and numeric types
    monthly_sales["order_month"] = pd.to_datetime(
        monthly_sales["order_month"]
    )
    monthly_sales["total_revenue"] = pd.to_numeric(
        monthly_sales["total_revenue"], errors="coerce"
    ).fillna(0)
    monthly_sales["total_orders"] = pd.to_numeric(
        monthly_sales["total_orders"], errors="coerce"
    ).fillna(0)

    products["total_revenue"] = pd.to_numeric(
        products["total_revenue"], errors="coerce"
    ).fillna(0)
    products["total_units_sold"] = pd.to_numeric(
        products["total_units_sold"], errors="coerce"
    ).fillna(0)

    customers["total_spent"] = pd.to_numeric(
        customers["total_spent"], errors="coerce"
    ).fillna(0)

    # --------------------------------------------------
    # Sidebar filters
    # --------------------------------------------------
    st.sidebar.header("Dashboard Filters")

    min_month = monthly_sales["order_month"].min().date()
    max_month = monthly_sales["order_month"].max().date()

    selected_dates = st.sidebar.date_input(
        "Order date range",
        value=(min_month, max_month),
        min_value=min_month,
        max_value=max_month,
    )

    filtered_sales = monthly_sales.copy()

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered_sales = monthly_sales[
            (monthly_sales["order_month"].dt.date >= start_date.replace(day=1))
            & (monthly_sales["order_month"].dt.date <= end_date)
        ].copy()

    # Product category filter
    if "category" in products.columns:
        categories = sorted(products["category"].dropna().unique().tolist())
        selected_categories = st.sidebar.multiselect(
            "Product categories",
            options=categories,
            default=categories,
        )
        filtered_products = products[
            products["category"].isin(selected_categories)
        ].copy()
    else:
        filtered_products = products.copy()
        st.sidebar.caption(
            "Category filtering isn't available in the current analytics table."
        )

    # --------------------------------------------------
    # Business overview
    # --------------------------------------------------
    st.subheader("Business Overview")

    total_revenue = filtered_products["total_revenue"].sum()
    total_units = int(filtered_products["total_units_sold"].sum())
    total_orders = int(filtered_sales["total_orders"].sum())
    customer_count = len(customers)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Delivered Revenue", f"{total_revenue:,.2f}")
    col2.metric("Delivered Orders", f"{total_orders:,}")
    col3.metric("Units Sold", f"{total_units:,}")
    col4.metric("Customers with Purchases", f"{customer_count:,}")

    st.caption(
        "Revenue is shown in dataset units; no currency has been assumed."
    )

    st.divider()

    # --------------------------------------------------
    # Monthly revenue trend
    # --------------------------------------------------
    st.subheader("Monthly Revenue Trend")

    if filtered_sales.empty:
        st.info("No monthly sales data is available for this date range.")
    else:
        chart_sales = filtered_sales.sort_values("order_month")
        st.line_chart(
            chart_sales.set_index("order_month")[["total_revenue"]]
        )

        st.dataframe(
            chart_sales,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # --------------------------------------------------
    # Product performance
    # --------------------------------------------------
    st.subheader("Product Performance")

    if filtered_products.empty:
        st.info("No products match the selected categories.")
    else:
        top_products = filtered_products.sort_values(
            "total_revenue", ascending=False
        ).head(10)

        st.bar_chart(
            top_products.set_index("product_name")[["total_revenue"]]
        )

        st.dataframe(
            top_products,
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # --------------------------------------------------
    # Customer spending
    # --------------------------------------------------
    st.subheader("Top Customers by Spending")

    top_customers = customers.sort_values(
        "total_spent", ascending=False
    ).head(10)

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True,
    )

    st.caption("Data source: NexaMart analytics tables in Google BigQuery.")

except Exception as error:
    st.error("The dashboard couldn't load its BigQuery data.")
    st.exception(error)
