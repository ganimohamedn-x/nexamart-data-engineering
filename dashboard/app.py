
import streamlit as st
import pandas as pd
from google.cloud import bigquery

# Page setup
st.set_page_config(
    page_title="NexaMart Analytics",
    page_icon="🛒",
    layout="wide",
)

st.title("🛒 NexaMart Analytics")
st.caption("Cloud-powered e-commerce sales and customer insights")

# Connect to BigQuery
@st.cache_resource
def get_client():
    return bigquery.Client(project="nexamart-data-engineering")


client = get_client()


# Load an analytics table into a Pandas DataFrame
@st.cache_data(ttl=300)
def load_table(table_name):
    query = f"""
        SELECT *
        FROM `nexamart-data-engineering.nexamart_analytics.{table_name}`
    """
    return client.query(query).to_dataframe()


try:
    monthly_sales = load_table("monthly_sales")
    products = load_table("product_performance")
    customers = load_table("customer_spending")

    # Calculate headline metrics
    total_revenue = products["total_revenue"].sum()
    total_units = products["total_units_sold"].sum()
    total_orders = monthly_sales["total_orders"].sum()
    customer_count = len(customers)

    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Delivered Revenue", f"${total_revenue:,.2f}")
    col2.metric("Delivered Orders", f"{total_orders:,}")
    col3.metric("Units Sold", f"{total_units:,}")
    col4.metric("Customers with Purchases", f"{customer_count:,}")

    st.divider()

    # Monthly revenue chart
    st.subheader("Monthly Revenue Trend")

    monthly_sales["order_month"] = pd.to_datetime(
        monthly_sales["order_month"]
    )

    monthly_sales = monthly_sales.sort_values("order_month")

    st.line_chart(
        monthly_sales.set_index("order_month")[["total_revenue"]]
    )

    # Product performance
    st.subheader("Product Performance")

    top_products = products.sort_values(
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

    # Customer spending
    st.subheader("Top Customers by Spending")

    top_customers = customers.sort_values(
        "total_spent", ascending=False
    ).head(10)

    st.dataframe(
        top_customers,
        use_container_width=True,
        hide_index=True,
    )

    # Allow users to inspect the underlying monthly figures
    with st.expander("View monthly sales data"):
        st.dataframe(
            monthly_sales,
            use_container_width=True,
            hide_index=True,
        )

    st.caption("Data source: NexaMart BigQuery analytics tables")

except Exception as error:
    st.error("The dashboard couldn't load its BigQuery data.")
    st.exception(error)
