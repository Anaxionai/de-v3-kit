# The sample month: not here yet

This folder is for students whose data.gov.in key has not arrived. It will hold one real month of raw market-price files, in exactly the layout `get_prices.py` writes, so that PriceWatch's `load` and `report` commands work without a key.

## Why it is empty

On 13 November 2026 the data.gov.in API answered every call without a key with HTTP 400, and the kit builders had no key. The site's Download button needs a form and a captcha and returns the whole dataset, not one month. So no real month could be saved, and the kit does not ship made-up prices that look like real data.

## What you do meanwhile

- Ask your mentor. Your centre can tell you when the sample arrives, or when your key should arrive.
- Do the parts of the task that need no download: the settings, the reader tested on a small file you write by hand, and the tests.
- Check the email you signed up with, including the spam folder. A key is usually ready within minutes of signing up.

## For the kit maintainers: how to fill this folder

With a data.gov.in key (one person, about 30 minutes), from the kit's root folder:

1. Check the key and the field names:
   ```bash
   export DATA_GOV_IN_KEY=<your key>
   uv run --python 3.12 python data/prices/get_prices.py --check
   ```
   Expect `Key accepted`, `All 11 columns are there.` and `Filters work: ...`.
2. Build the sample month:
   ```bash
   uv run --python 3.12 python data/prices/get_prices.py --month 2026-10 --out data/prices/sample \
     --state Maharashtra --state Haryana --state Punjab --state Rajasthan --state "Tamil Nadu" --state Kerala
   ```
   These states hold the problems the P1 briefs rely on: coriander at 5 to 40 (Maharashtra), the comma name in Faridabad (Haryana), Garh Shankar (Punjab), the Jodhpur yards (Rajasthan), `Vadamadurai ` with a trailing space (Tamil Nadu) and values 100 times too large (Kerala). Keep the folder under 2 MB: drop or add states until it fits and still has coriander rows below 100, empty days, at least one zero price and one row whose minimum is above its maximum.
3. Delete this README, then update "The sample month" in `../README.md` with the month, the states, the row count and the size.
4. Never commit the key. It stays in your shell or in an ignored `.env`.
