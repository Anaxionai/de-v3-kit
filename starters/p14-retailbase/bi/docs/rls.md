# RetailBase row-level security

## Role and rules

<!-- TODO(task 13): the role's name and both DAX rules, the one on dim_customer and the one on country_manager. -->

## Tests

<!-- TODO(task 13): the three View as tests. For each, the countries and the revenue you saw in Power BI, and the revenue from bi/sql/check_rls.sql. -->

| Viewed as | Countries seen | Revenue in Power BI | Revenue in SQL |
|---|---|---|---|
| france.manager@example.com | | | |
| germany.manager@example.com | | | |
| nobody@example.com | | | |

## Sales with no customer

<!-- TODO(task 13): who sees the Unknown sales, and why. -->

## When a manager moves

<!-- TODO(task 13): what changes when a manager moves to another country, in which table and file (dw.country_manager, sql/05_country_manager.sql), and what stays the same. -->

## A customer who moved country

<!-- TODO(task 13): one customer with dim_customer rows in two countries (from your P3 change batch): which of their sales each country's manager sees, and why. -->

## What RLS does not protect

<!-- TODO(task 13): who still sees every row: workspace members, and anyone with your .pbix file. -->
