# RetailBase model

## Normalised model

TODO(task 8): draw the source data in third normal form: CUSTOMER, PRODUCT, INVOICE and
INVOICE_LINE, with `PK` and `FK` marks. Below the diagram, name two raw columns that
repeat a fact, the normal form each breaks, and the table that now holds the fact.

```mermaid
erDiagram
    %% TODO(task 8): your four entities and their relationships
```

## Star schema

TODO(task 8): draw FACT_SALES joined to DIM_DATE, DIM_CUSTOMER and DIM_PRODUCT, with the
columns the brief names. Each dimension has a surrogate key and its source key.

```mermaid
erDiagram
    %% TODO(task 8): the fact, the three dimensions and their relationships
```

## Grain

TODO(task 8): finish the sentence "One row of `dw.fact_sales` is ...". Name the columns
that identify a row, and say from your profile why `invoice` and `stock_code` are not enough.

## Measures

TODO(task 8): each measure, how it is computed from the raw columns, and whether it is
additive.

## Decisions

TODO(task 8): a reason for each loading rule in the brief, and your own two rules: one
country for a customer who has two, and one description for a product that has many.
