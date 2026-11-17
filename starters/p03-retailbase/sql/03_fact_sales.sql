-- RetailBase sales fact. Task 10, changed in task 11.
-- Run it from retailbase/ with:
--   docker exec -i datalab-postgres-1 psql -U de -d retailbase < sql/03_fact_sales.sql

-- Drop and create dw.fact_sales
-- TODO(task 10): the nine columns of your model (invoice_no, line_no, date_key,
-- customer_key, product_key, quantity, unit_price, amount, is_cancellation), the primary
-- key (invoice_no, line_no), and a foreign key to each dimension.

-- The CTE over staging.sales_raw
-- TODO(task 10): leave out the first sheet's copy of the shared days
-- (source_sheet = 'Year 2009-2010' AND invoice_date >= '2010-12-01'), and compute
-- line_no, amount and is_cancellation.

-- The insert
-- TODO(task 10): look up date_key, product_key and customer_key in the dimensions: first
-- with plain JOIN, then with LEFT JOIN and COALESCE(..., 0) for products and customers.
-- TODO(task 11): match the customer version that was valid on the invoice date.
