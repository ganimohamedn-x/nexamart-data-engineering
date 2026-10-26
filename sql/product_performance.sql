CREATE OR REPLACE TABLE
  `nexamart-data-engineering.nexamart_analytics.product_performance` AS

SELECT
  p.product_id,
  p.product_name,
  p.category,
  SUM(oi.quantity) AS total_units_sold,
  ROUND(SUM(oi.line_total), 2) AS total_revenue

FROM `nexamart-data-engineering.nexamart_staging.products` AS p

INNER JOIN `nexamart-data-engineering.nexamart_staging.order_items` AS oi
  ON p.product_id = oi.product_id

INNER JOIN `nexamart-data-engineering.nexamart_staging.orders` AS o
  ON oi.order_id = o.order_id

WHERE o.order_status = 'Delivered'

GROUP BY
  p.product_id,
  p.product_name,
  p.category;
