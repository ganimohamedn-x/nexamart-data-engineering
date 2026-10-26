CREATE OR REPLACE TABLE
  `nexamart-data-engineering.nexamart_analytics.monthly_sales` AS

SELECT
  DATE_TRUNC(DATE(o.order_date), MONTH) AS order_month,
  COUNT(DISTINCT o.order_id) AS total_orders,
  SUM(oi.quantity) AS total_units_sold,
  ROUND(SUM(oi.line_total), 2) AS total_revenue

FROM `nexamart-data-engineering.nexamart_staging.orders` AS o

INNER JOIN `nexamart-data-engineering.nexamart_staging.order_items` AS oi
  ON o.order_id = oi.order_id

WHERE o.order_status = 'Delivered'

GROUP BY order_month
ORDER BY order_month ASC;
