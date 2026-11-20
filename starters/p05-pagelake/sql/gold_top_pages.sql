-- Gold table top_pages: the 10 most-viewed articles per day and language.
-- Columns: day, lang, rank, title, views. gold.py writes it to gold/top_pages/top_pages.parquet.

-- TODO(task 10): FROM {silver}, without the title '-' and the titles in sql/not_articles.csv (a LEFT JOIN to
--   read_csv('sql/not_articles.csv')): views summed per day, lang and title, numbered with row_number()
--   per day and lang (most views first, title breaks ties), ranks 1 to 10 kept.
