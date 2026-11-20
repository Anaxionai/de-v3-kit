# Daily market prices: the raw data for PriceWatch (P1)

PriceWatch (P1) reads one month of real wholesale vegetable prices from Indian markets (mandis), cleans them and reports on them.
This folder holds the download script and a sample month for students whose key has not arrived yet.

| Path | What it is |
|---|---|
| `get_prices.py` | Downloads one month of daily prices from data.gov.in as raw CSV files. It needs your free key. |
| `sample/` | One real month in exactly the same format as a download. Use it while you wait for a key. |
| `downloads/` | Where `get_prices.py` saves your months. Git ignores this folder (see `.gitignore`). |

## Source and licence

- **Dataset:** Variety-wise Daily Market Prices Data of Commodity
- **Page:** https://www.data.gov.in/resource/variety-wise-daily-market-prices-data-commodity
- **Publisher:** Directorate of Marketing and Inspection, Department of Agriculture and Farmers Welfare, Ministry of Agriculture and Farmers Welfare. The data comes from the AGMARKNET portal (https://agmarknet.gov.in), where markets report their prices every day.
- **Platform:** Open Government Data Platform India (data.gov.in). The dataset is updated daily.
- **Licence:** Government Open Data License - India (GODL-India): https://www.data.gov.in/Godl
  You may use, copy, change and publish the data, also for paid work, if you publish the attribution line below. You must not suggest that the publisher supports your work, and the publisher gives no warranty.

**Attribution line.** Copy it exactly into `DATA.md` (task 8), under your chart (task 24) and into your README (task 25):

```text
Directorate of Marketing and Inspection, Ministry of Agriculture and Farmers Welfare, 2024, Variety-wise Daily Market Prices Data of Commodity, Open Government Data Platform India, 21/05, https://www.data.gov.in/resource/variety-wise-daily-market-prices-data-commodity. Published under Government Open Data License - India: https://www.data.gov.in/Godl.
```

The line follows the template in section 5 of the licence: provider, year of publication, name of the data, platform, date of publication (day/month), address, licence and its address.
`get_prices.py` writes the same line into every `source.json`.

## Get your free key

data.gov.in gives every registered user a free API key (a secret code that the site checks on every request). Without a key the API answers `HTTP 400` with `Authorization field missing`.

1. Open https://www.data.gov.in and choose **Login | Register** at the top right. The site signs you in through **Jan Parichay**, the Government of India's single sign-on service. Create a Jan Parichay account if you have none.
2. Your account needs a verified email address, or the site will not make a key. If data.gov.in says that no email id is linked to your account:
   1. Open https://janparichay.meripehchaan.gov.in/v1/pehchaan/editprofile.html.
   2. Under **VERIFICATION DETAILS**, choose **Primary Email Id** in the list of verification parameters.
   3. Type your email address and choose **Verify**. Type the one-time code (OTP) from the email and choose **Submit**.
   4. Sign out of data.gov.in and sign in again.
3. Open **My Account** on data.gov.in (https://www.data.gov.in/user/myaccount) and generate your API key. Copy it.
4. In Git Bash, in the terminal where you will run the script, type:

   ```bash
   export DATA_GOV_IN_KEY=<your key>
   uv run python ~/de-kit/data/prices/get_prices.py --check
   ```

   `--check` makes a few small requests. It prints `Key accepted: HTTP 200`, the fields the API sent, a line that starts with `Filters work:`, and `Your key is ready.`

Keep the key secret, like a password. It stays in that terminal only: a new terminal needs the `export` line again.
Never put the key in a file that Git tracks. Your `.env.example` holds only the empty line `DATA_GOV_IN_KEY=`.

**While you wait for a key**, or when the site is slow, use the sample month: `~/de-kit/data/prices/sample` is your source folder in task 8. The sample is marked the same as a download.
If the API still refuses your key 15 minutes after you made it (`HTTP 403: Key not authorised`), use the sample and tell your mentor.

## Download a month

Run this from your `pricewatch/` folder in Git Bash, for last month:

```bash
uv run python ~/de-kit/data/prices/get_prices.py --month 2026-10
```

The script uses only the Python standard library, so there is nothing to install.
It asks for each day and each commodity in turn, with a short pause between requests, so a month takes a few minutes.
It prints one line per day with the date, the HTTP status and the row count, then a `Done:` line that names the folder, the files and the total rows:

```text
2026-10-30 Fri  HTTP 200  1,234 rows
2026-10-31 Sat  HTTP 200  1,198 rows
Done: 31 files (4 with no rows) and source.json, 35,512 rows, in C:/Users/you/de-kit/data/prices/downloads/2026-10
```

(The row counts here only show the layout. Yours depend on the month.)

| Option | What it does | Default |
|---|---|---|
| `--month YYYY-MM` | The month to download. It must be finished: last month or earlier. | (required) |
| `--commodity NAME` | A commodity, spelt exactly as the source spells it. Repeat it for more. | `Tomato`, `Onion`, `Potato`, `Brinjal`, `Coriander(Leaves)` |
| `--state NAME` | Download only this state, spelt as the source spells it. Repeat it for more. | every state |
| `--out FOLDER` | Where to save the files. | `~/de-kit/data/prices/downloads/YYYY-MM` |
| `--check` | Test your key with a few small requests, without downloading a month. | |

- **Run it again** whenever you like: it writes the same files again. It deletes the folder's `source.json` first and writes a new one only at the very end, so a folder without `source.json` is a download that did not finish.
- **The site is busy** (`HTTP 429`) or down (`HTTP 5xx`)? The script waits 5, 20 and then 60 seconds and tries again. After the fourth failure it stops with a message.
- **`Stopped: Asked for ... but got ...`** means the API sent rows for another day or commodity, so the script stopped before it filled your disk. Run `--check` and tell your mentor.

## What a download holds

One file per calendar day, named `prices-YYYY-MM-DD.csv` (the date in the name is ISO: year, month, day).
Each file is UTF-8, comma separated, and starts with this header:

```text
State,District,Market,Commodity,Variety,Grade,Arrival_Date,Min_Price,Max_Price,Modal_Price,Commodity_Code
```

A day with no reports still gets a file with the header only. Most Sundays and public holidays are like that.
Values are saved exactly as the API sends them: nothing is trimmed, renamed or converted. A market name with a comma in it is in double quotes, so read the files with `csv` or pandas, never with `split(",")`.

| Column | What it means |
|---|---|
| `State` | The state the market is in. |
| `District` | The district the market is in. |
| `Market` | The market yard (mandi). A part in brackets names one yard of a town, or a section such as `F&V` (fruits and vegetables). |
| `Commodity` | What was sold, for example `Tomato` or `Coriander(Leaves)`. |
| `Variety` | The variety of the commodity. One market can report two or more varieties of one commodity on the same day. |
| `Grade` | The quality grade the market reported. |
| `Arrival_Date` | The trading day, as day/month/year: `01/10/2026` is 1 October 2026. Read it with `datetime.strptime(text, "%d/%m/%Y")`. |
| `Min_Price` | The lowest price paid that day, in rupees per quintal. |
| `Max_Price` | The highest price paid that day, in rupees per quintal. |
| `Modal_Price` | The most common price that day, in rupees per quintal. PriceWatch uses this one. |
| `Commodity_Code` | AGMARKNET's number for the commodity. |

**Prices are rupees per quintal.** A quintal is 100 kg, so a modal price of 2450 is ₹24.50 per kilogram.
The files have no unit column. `source.json` says it once: `"price_unit": "Rs./Quintal"`.

`source.json` sits next to the day files. It names the dataset, the publisher, the page, the licence and the attribution line, the month, the price unit, the commodities and states, the time of the download (`downloaded_at`), and the list `files`: each file's `name`, `date` and `rows` (data rows, without the header).
Task 8 checks every file's row count against this list.

## What is messy, and why

Hundreds of markets type their own reports into one national system every day, and the files keep what each market typed. So the raw files have these problems. They are real, and the kit does not fix or add any of them: cleaning them is your work in tasks 9 to 11.

1. **One market, several spellings.** Names differ only in spaces or brackets, such as `Garh Shankar` and `GarhShankar (Kotfatuhi)`. Some names end with a space (`Vadamadurai `) or have a space before a comma (`New Grain Market , Faridabad`).
2. **Yards in brackets.** One town can have several market yards: `Jodhpur(F&V)(Paota)` and `Jodhpur(F&V)(Bhadwasia)`. One market or two? You decide, and write your reason down.
3. **Missing days.** Markets close on Sundays and holidays, and some markets skip days. A missing day is not a price of zero.
4. **Zero prices.** A few rows have a price of `0`. Nothing sells for nothing, so the row cannot be used as a price.
5. **Prices out of order.** A few rows have `Min_Price` above `Max_Price`, or a `Modal_Price` outside the minimum and the maximum.
6. **Leafy produce in another unit.** A few markets report leafy vegetables such as coriander leaves at 5 to 40, while other markets report thousands. A price of 20 per quintal is impossible, so these markets almost certainly mean per kilogram or per bunch. The file cannot tell you which, so task 11 rejects them with a rule you choose from the numbers.
7. **Decimals.** Most prices are whole numbers, but some have decimals.

## The sample month

<!-- BUILD NOTE (remove when done): sample/ is not built yet, because no data.gov.in key was available to the kit builder.
     Whoever has a key runs, from the kit folder:
       uv run --python 3.12 python data/prices/get_prices.py --month 2026-10 --out data/prices/sample --state Maharashtra --state Haryana --state Punjab --state Rajasthan --state "Tamil Nadu" --state Kerala
     then checks that sample/ is under 2 MB and still holds: coriander rows below 100 in some markets, empty days, a zero price, a min-above-max row, bracketed and comma market names.
     Add the month, the states, the row count and the size measured to this section. See work/reports/kit-k3-data-A1.md. -->

`sample/` holds one real month, downloaded with `get_prices.py`, with the same file names, header and `source.json` as your own download.
To stay small, it keeps only some states. `sample/source.json` names the month and the states.
It holds the same five commodities, real empty days and the real problems listed above. Nothing was planted: in task 9 you break your own copy.

Use it as the source folder wherever a task names your download folder, for example:

```bash
uv run python fetch.py ~/de-kit/data/prices/sample
```

The sample's prices come from the same dataset, so the same attribution line applies.
