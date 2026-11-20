# Online Retail II: the sales data for RetailBase (P3 and P14)

RetailBase (P3) models two years of real sales from an online shop as a star schema in PostgreSQL. RetailBase part 2 (P14) adds a Power BI report on the same warehouse, in `retailbase/bi/`, and rebuilds the warehouse from these scripts first.
This folder holds the scripts that download the data and make your customer change batch. The data itself is never in the kit or in your repository.

| File | What it does |
|---|---|
| `get_retail.py` | Downloads the published workbook and saves it as one CSV file, `online_retail_II.csv`. |
| `make_changes.py` | Writes your own customer change batch, `customer_changes.csv`, for the slowly changing dimension in task 11. |

## Source and licence

- **Dataset:** "Online Retail II", UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **DOI:** https://doi.org/10.24432/C5CG6D
- **Creator:** Daqing Chen. Donated to the repository on 20 September 2019.
- **What it is:** every sale of a UK-based online shop from 1 December 2009 to 9 December 2011. The shop sells gift-ware for all occasions, and many of its customers are wholesalers (shops that buy to sell again).
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0): https://creativecommons.org/licenses/by/4.0/legalcode
  You may copy, change and share the data, also for paid work, if you credit the source, link the licence and say what you changed.
- **What the kit changes:** `get_retail.py` converts the workbook from Excel (`.xlsx`) to CSV, joins its two worksheets into one file, and adds two columns, `Sheet` and `SheetRow`. It does not change any value.

**Citation** (as the UCI page gives it). Copy it into your `retailbase/README.md` in task 13:

```text
Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D.
```

**Licence line** to copy with it:

```text
Licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Converted from .xlsx to one CSV file with the course kit's get_retail.py: the two worksheets joined, and the columns Sheet and SheetRow added.
```

The UCI page is not connected with this course and does not endorse it.

## Get the data

In your `retailbase/` folder in Git Bash, run:

```bash
uv run ~/de-kit/data/retail/get_retail.py --out data
```

The first lines of the script (between `# /// script` and `# ///`) tell uv that it needs Python 3.12 and the package `openpyxl`, which reads Excel files.
uv builds a separate environment for the script, so your own project is not changed.

It downloads `https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip` (45,622,418 bytes) and converts the workbook inside it.
On the build laptop this took 114 seconds in all. You see:

```text
Downloading https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip (about 45 MB) ...
  10 MB
  20 MB
  30 MB
  40 MB
Converting the workbook to CSV (about 2 minutes) ...
Sheet Year 2009-2010: 525,461 rows
Sheet Year 2010-2011: 541,910 rows
Wrote data/online_retail_II.csv: 1,067,371 rows, 10 columns
```

The result, `data/online_retail_II.csv`, is 116,441,405 bytes (about 111 MB). Git must not commit it: check that your `.gitignore` holds `data/`.

- **Slow internet?** Download the zip once, for example from a centre computer, then run `uv run ~/de-kit/data/retail/get_retail.py --out data --zip <path to online+retail+ii.zip>`.
- **Stopped half-way?** Run the same command again. The script writes `online_retail_II.csv.part` first and renames it only at the end, so a half-written file never looks finished.
- **`WARNING: expected 1,067,371 rows`?** The publisher may have changed the file. Tell your mentor before you go on: the briefs' numbers come from this exact file.

## The ten columns

The file is UTF-8, comma separated, with one header line. A value with a comma in it is in double quotes, so read it with `csv` or pandas, never with `split(",")`.

| # | Column | What it holds | Example |
|---|---|---|---|
| 1 | `Invoice` | The invoice number: 6 digits. It starts with `C` for a cancellation and with `A` for a bad-debt adjustment. | `489434`, `C489449` |
| 2 | `StockCode` | The product code: usually 5 digits and an optional letter. Some codes are services, not products, such as `POST`. | `85048`, `79323P` |
| 3 | `Description` | The product name. Empty when missing. | `PINK CHERRY LIGHTS` |
| 4 | `Quantity` | Units on this invoice line, a whole number. Negative on cancellations and stock adjustments. | `12`, `-1` |
| 5 | `InvoiceDate` | Date and time of the invoice, `YYYY-MM-DD HH:MM:SS`. The seconds are always `00`. | `2009-12-01 07:45:00` |
| 6 | `Price` | Unit price in pounds sterling (£), with up to 3 decimals. The course does not convert it to rupees. | `6.95`, `18`, `0.001` |
| 7 | `Customer ID` | The customer number: a 5-digit whole number. Empty when the customer is unknown. | `13085` |
| 8 | `Country` | The country where the customer lives. | `United Kingdom` |
| 9 | `Sheet` | The worksheet the row came from: `Year 2009-2010` or `Year 2010-2011`. Added by the kit. | `Year 2009-2010` |
| 10 | `SheetRow` | The row number in that worksheet. Row 2 is the first data row, because row 1 is the header. Added by the kit. | `2` |

The UCI page still lists older column names (`InvoiceNo`, `UnitPrice`, `CustomerID`). The file uses the names above.

## Known problems

Every number below was measured on the published file on 13 November 2026. Your task 7 profile should find the same numbers.

1. **The two sheets overlap.** 1 to 9 December 2010 is in both sheets, row for row: 1,088 invoices and 22,523 rows in each. The file has 1,067,371 rows; without the first sheet's copy it has 1,044,848. The course keeps the second sheet's copy.
2. **Cancellations.** 19,494 rows on 8,292 invoices start with `C`. One of them (invoice `C496350`, stock code `M`, "Manual") has a positive quantity.
3. **Missing customer.** 243,007 rows (22.8%) have no `Customer ID`. 98.8% of them are in the United Kingdom. Once the overlap is left out, 235,287 rows have no customer.
4. **Stock adjustments.** 3,457 rows have a negative quantity but are not cancellations. All of them have price 0 and no customer. Their descriptions are notes such as "damages", "thrown away" or "?".
5. **Bad-debt adjustments.** 6 rows have an invoice starting with `A` and the stock code `B`. 5 of them have a negative price.
6. **Missing description.** 4,382 rows have no description. 4 descriptions are only digits (`20713`, `21494`, `22467`, `22719`).
7. **Codes that are not products.** For example `POST` (postage), `DOT` (dotcom postage), `M` (manual), `C2` (carriage), `D` (discount), `S` (samples), `BANK CHARGES`, `AMAZONFEE`, `ADJUST`, `CRUK` (CRUK commission), `TEST001`, and 9 gift-voucher codes that start with `gift_0001_`.
8. **One product, two spellings.** 173 stock codes appear in both upper and lower case, such as `85123A` and `85123a`. 1,232 codes have more than one description. One code has a space at the end (`47503J `).
9. **Repeated lines.** 42,638 pairs of `Invoice` and `StockCode` appear on more than one row in the whole file (21,234 once the overlap is left out). 34,335 rows are exact copies of another row (11,812 once the overlap is left out). The course keeps them as separate invoice lines.
10. **Customers with two countries.** 13 customers appear with two countries, for example customer 12370 with Austria and Cyprus.
11. **Country names that are not countries, or not standard.** `EIRE` (Ireland), `RSA` (South Africa), `USA`, `Unspecified`, `European Community`, `Channel Islands` and `West Indies`.
12. **Money is in pounds sterling**, not rupees. Without the overlap, `SUM(Quantity)` is 10,441,844 and `SUM(Quantity * Price)` is 18,909,762.118.

## Your customer change batch (task 11)

In your `retailbase/` folder, after `get_retail.py`, run:

```bash
uv run ~/de-kit/data/retail/make_changes.py --student <your-id>
```

`<your-id>` is your GitHub username in lower case. The script reads `data/online_retail_II.csv` and writes `data/customer_changes.csv` in about 6 seconds. You see:

```text
Wrote data/customer_changes.csv: 60 rows (40 moves, 10 new customers, 10 with no change)
```

The file has the header `customer_id,country,changed_on` and 60 rows in random order, one row per customer:

| Kind | Rows | What it is |
|---|---|---|
| Move | 40 | An existing customer who now lives in another country, from the date `changed_on`. |
| New customer | 10 | A customer id from 19001 to 19999. The file's largest id is 18287, so these customers have no sales yet. |
| No change | 10 | An existing customer with the country they already have. Your SCD code must add nothing for these rows. |

How the rows are chosen:

- Rows of the first sheet dated from 2010-12-01 are left out, as in your fact table.
- Moves and no-change rows use only customers with exactly one country in the file, never one of the 13 customers with two countries.
- A moved customer has sales on at least two different days, and `changed_on` is one of those days other than the first. So each moved customer has sales before the change and sales on or after it, and both versions of the customer get fact rows.
- The new country of a move is one of France, Germany, Netherlands, Spain, Belgium, Switzerland, Portugal, Australia, Sweden, Italy, Norway and Denmark, and never the old country.
- A no-change row and a new customer get a `changed_on` in 2011, before 2011-12-10. Dates are ISO dates, such as `2011-05-29`.

The same `--student` always gives the same batch, on any computer and any Python version from 3.12. Capital letters and spaces around the id do not matter. Your mentor can make your batch again to check your numbers. Different students get different batches, so your task 12 countries differ from a classmate's.

Checked on the build laptop with five ids: every batch classifies as 10 new, 40 moves and 10 with no change; the SCD type 2 load grows `dw.dim_customer` from 5,943 to 5,993 rows (5,953 current); every fact row finds exactly one customer version; and between 11 and 15 countries show a difference in task 12.

`make_changes.py` checks its own batch before it writes the file. If a rule above is broken, it stops with a message and writes nothing.
