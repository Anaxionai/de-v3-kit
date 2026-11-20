-- RetailBase staging: the raw sales file, exactly as it arrived. Task 7.
-- Run it from retailbase/ with:
--   docker exec -i datalab-postgres-1 psql -U de -d retailbase < sql/01_staging.sql
CREATE SCHEMA IF NOT EXISTS staging;

-- TODO(task 7): drop and create staging.sales_raw with these ten columns, in the order of
-- the file's columns, each with a type that loads the file. price must be numeric(12,3),
-- never a float type.
--   invoice, stock_code, description, quantity, invoice_date, price, customer_id, country,
--   source_sheet, source_row
