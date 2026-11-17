# OpenAQ sample pages: not here yet

This folder is for students whose OpenAQ key has not arrived. It should hold real API pages, saved in exactly the layout ClearAir writes, so that `load-api --raw` works without a key:

```
sample/<run-id>/locations-001.json
sample/<run-id>/<sensor-id>/page-001.json
sample/<run-id>/<sensor-id>/page-002.json
```

`<run-id>` is the UTC start of the run, rounded down to the hour, for example `20261112T0800Z`.

## Why it is empty

On 13 November 2026 every OpenAQ API call answered 401 without a key, and the kit builders had no key. OpenAQ's documentation shows only short example answers (one or two results), which cannot show paging. So no real pages could be saved, and the kit does not ship made-up pages that look like real data.

## What you do meanwhile

- Ask your mentor. Your centre can tell you when the pages arrive, or when your key should arrive.
- Build the parts of the task that need no API call: the settings, the client tested with a fake page, and the tests.
- Check the email you signed up with, including the spam folder.

## For the kit maintainers: how to fill this folder

1. With a staff key, run ClearAir's own `load-api` for one city (for example Bengaluru, `12.9716,77.5946`, radius 25,000 m, `PARAMETER=pm25`) over 7 days, so each sensor has more than 100 hours and needs at least 2 pages.
2. Keep at least 3 sensors, and only locations whose `licenses` entry says `redistributionAllowed: true` and `commercialUseAllowed: true` (for example CC BY 4.0). Drop the other locations from `locations-001.json` and delete their sensor folders.
3. Keep the pages unchanged otherwise, and keep the folder under 2 MB.
4. Add a `NOTICE.md` here that credits OpenAQ ("Air-quality data from OpenAQ (openaq.org)") and names each location's provider and licence.
5. Add the folder to `design/KIT-LAYOUT.md` as `data/airquality/sample/` and update this README.
