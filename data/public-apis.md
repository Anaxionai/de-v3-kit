# Free public APIs that need no key

Each API below answers JSON (a text format of names and values) without a key or a sign-up. Every address was fetched with `curl -s` from India on 13 November 2026 and answered HTTP 200. The value in the last column is what it showed that day; most of them change over time, so yours will differ.

How to call one in Git Bash (keep the address in double quotes, because `&` and `?` mean something to the shell):

```bash
curl -s -A "practice (github.com/<username>)" "<address>" -o other-api.json
uv run python -m json.tool other-api.json
```

`-A` sends a User-Agent (a short note on who is asking). Several of these services ask for one, and it costs nothing to send it to all of them.

## The list

| API | Example address | One value to read | On 13 Nov 2026 |
|---|---|---|---|
| Wikipedia page summary | `https://en.wikipedia.org/api/rest_v1/page/summary/Chess` | `description` | `Traditional board game for two players` |
| Wikipedia's most-read pages of one day | `https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/2026/11/10` | `items[0].articles[1].article` (item 0 is always `Main_Page`) | `Ramayana:_Part_1`, 840,888 views |
| USGS significant earthquakes, past week | `https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_week.geojson` | `metadata.count`, then `features[0].properties.mag` | `1`, magnitude `6.4` |
| World Bank: India's population | `https://api.worldbank.org/v2/country/IN/indicator/SP.POP.TOTL?format=json&date=2024` | the second list's first item: `[1][0].value` | `1450935791` |
| Frankfurter exchange rates | `https://api.frankfurter.dev/v1/latest?base=EUR&symbols=INR` | `rates.INR` (rupees for one euro) | `104.2118` (rates of 12 Nov) |
| GitHub repository facts | `https://api.github.com/repos/duckdb/duckdb` | `stargazers_count` | `43040` |
| Open Library book search | `https://openlibrary.org/search.json?q=data+engineering&limit=1` | `numFound`, then `docs[0].title` | `15800`, `Fundamentals of Data Engineering` |
| Crossref research papers | `https://api.crossref.org/works?query=data+engineering&rows=1` | `message.total-results` | `9471995` |
| Sunrise and sunset in Bengaluru | `https://api.sunrise-sunset.org/json?lat=12.9716&lng=77.5946&date=2026-11-13&tzid=Asia/Kolkata` | `results.sunrise` | `6:17:19 AM` |
| India Post PIN codes | `https://api.postalpincode.in/pincode/560001` | `[0].PostOffice[0].District` | `Bangalore` (10 post offices) |
| Great Britain electricity carbon intensity | `https://api.carbonintensity.org.uk/intensity` | `data[0].intensity.forecast` (grams of CO2 per kWh) | `141` |

How to read a path such as `items[0].articles[1].article`: `items` is a key, `[0]` is the first entry of a list (counting starts at 0), and each `.` goes one level deeper.

## Rules and licences, one line each

- **Wikipedia and Wikimedia**: page text is CC BY-SA 4.0; page-view numbers are CC0 1.0. Send a User-Agent, and wait for each answer before the next request. The kit's `data/pageviews/README.md` has the full rules.
- **USGS**: United States government data, public domain. The feed is updated every minute.
- **World Bank**: most World Bank datasets are CC BY 4.0 (credit "The World Bank"); check the licence label on each dataset's page.
- **Frankfurter**: open source, no key, "no quotas", but rate-limited against abuse. Rates come from central banks, including the European Central Bank.
- **GitHub**: 60 requests an hour without a key. Use it for one or two calls, not a loop.
- **Open Library**: 1 request a second without a User-Agent and email, 3 with one. Never use the API to download the whole catalogue: Open Library publishes monthly data dumps for that.
- **Crossref**: "you may use it for any purpose", but some abstracts are copyrighted by their publishers. Add `&mailto=<your email>` only if you are happy to share it.
- **Sunrise-Sunset.org**: free, but it asks for credit: write "Sun data by Sunrise-Sunset.org" in your README if you publish anything from it. Without `tzid` the times are in UTC.
- **India Post PIN codes** (`postalpincode.in`): a free service that is not run by India Post, and it publishes no terms. Fine for practice; do not build a product on it.
- **Carbon Intensity** (National Energy System Operator, Great Britain): CC BY 4.0. Its terms forbid selling access to the API or using it heavily.

## Left out on purpose

- **Open-Meteo** (weather): its free API is for non-commercial use only, so the course does not list it.
- **REST Countries** (`restcountries.com/v3.1/...`): on 13 November 2026 it answered `"This API version has been deprecated"`.
- APIs that need a free key are explained where the course uses them: `data/prices/README.md` (data.gov.in) and `data/airquality/README.md` (OpenAQ).
