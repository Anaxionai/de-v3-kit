-- RetailBase customer dimension as SCD type 2, and the change batch. Task 11.
-- Run it from retailbase/ with:
--   docker exec -i datalab-postgres-1 psql -U de -d retailbase < sql/04_scd2_customer.sql
-- Run it twice: the second run must change nothing.

-- Add the validity columns
-- TODO(task 11): add valid_from, valid_to and is_current to dw.dim_customer, each only if it
-- does not exist yet, NOT NULL, with the defaults '1900-01-01', '9999-12-31' and true.

-- The batch table
-- TODO(task 11): create staging.customer_changes, if it does not exist, with the batch's
-- three columns: customer_id, country and changed_on.

-- Each customer's newest batch row. The batch table keeps old batches, so read from here.
-- TODO(task 11): create the view staging.latest_changes, in a way that can run again:
-- each customer's newest row of staging.customer_changes (ROW_NUMBER() by changed_on DESC,
-- keep 1).

-- Apply the batch: the UPDATE and the INSERT succeed or fail together.
BEGIN;

-- TODO(task 11): an UPDATE from staging.latest_changes that closes each current row whose
-- country differs.

-- TODO(task 11): an INSERT from staging.latest_changes of a new current row for each
-- customer with no current row. A row with no change adds nothing.

COMMIT;
