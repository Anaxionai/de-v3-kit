-- Freshness: the newest day of silver that has all 24 hours. pagelake/freshness.py runs this file.
-- With no complete day, return NULL (or no row): freshness.py treats it as LATE.

-- TODO(task 14): FROM {silver}, the newest day with GROUP BY day HAVING count(DISTINCT hour) = 24.
