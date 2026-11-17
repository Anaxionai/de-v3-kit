-- Scorebook load checks. Task 9.
-- Run them from scorebook/ with: bash psql.sh -a < sql/checks.sql
-- A check that expects zero rows passes when psql prints (0 rows).

-- check 1: row counts
-- TODO(task 9): one SELECT COUNT(*) per table. matches must equal the number in data/matches/README.txt.

-- check 2: deliveries with no innings
-- TODO(task 9): LEFT JOIN innings on both key columns, keep the rows where the innings side IS NULL. Expect 0.

-- check 3: innings with no deliveries, and matches with no innings
-- TODO(task 9): two counts. Expect 0 for both.

-- check 4: duplicate delivery keys
-- TODO(task 9): GROUP BY the four key columns HAVING COUNT(*) > 1. Expect no rows.

-- check 5: names that belong to more than one player_id
-- TODO(task 9): expect at least one name.

-- check 6: innings per match
-- TODO(task 9): count the matches by their number of innings. Most have 2.
