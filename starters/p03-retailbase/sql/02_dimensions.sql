-- RetailBase dimensions: dates, products and customers. Task 9.
-- Run it from retailbase/ with:
--   docker exec -i datalab-postgres-1 psql -U de -d retailbase < sql/02_dimensions.sql
-- It must run twice without an error.

-- Schema and drops
-- TODO(task 9): create the schema dw if it does not exist, then drop dw.fact_sales and the
-- three dimensions if they exist.

-- dw.dim_date: one row per day from 2009-01-01 to 2011-12-31
-- TODO(task 9): date_key (integer primary key, 20101201 for 1 December 2010), full_date
-- (date, unique) and your attributes: year, quarter, month, month_name and day_name.
-- Fill it with generate_series.

-- dw.dim_product: one row per product code
-- TODO(task 9): product_key (an identity primary key), stock_code (unique) and description.
-- Load one row per UPPER(stock_code), with one trimmed description chosen by your rule.

-- dw.dim_customer: one row per customer
-- TODO(task 9): customer_key (an identity primary key), customer_id (not unique: task 11
-- gives a customer a second row) and country. Load one row per customer_id that is not
-- NULL, with one country chosen by your rule.

-- Unknown members
-- TODO(task 9): key 0 in dw.dim_product (stock_code UNKNOWN, description Unknown product)
-- and in dw.dim_customer (customer_id 0, country Unknown).
