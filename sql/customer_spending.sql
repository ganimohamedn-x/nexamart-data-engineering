CREATE OR REPLACE TABLE
  `nexamart-data-engineering.nexamart_analytics.customer_spending` AS

SELECT
  c.customer_id,
  c.first_name,
  c.last_name,
  COUNT(DISTINCT o.order_id) AS total_orders,
  ROUND(SUM(oi.line_total), 2) AS total_spent

FROM `nexamart-data-engineering.nexamart_staging.customers` AS c

INNER JOIN `nexamart-data-engineering.nexamart_staging.orders` AS o
  ON c.customer_id = o.customer_id

INNER JOIN `nexamart-data-engineering.nexamart_staging.order_items` AS oi
  ON o.order_id = oi.order_id

WHERE o.order_status = 'Delivered'

GROUP BY
  c.customer_id,
  c.first_name,
  c.last_name;
