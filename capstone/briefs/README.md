# The capstone briefs

Choose one of these four data products for your capstone, or pitch your own. Each brief names the users and their question, a real public data source that no course project uses, what you must build, what is out of scope, the route for an 8 GB laptop, the cost and what the demo must show.

| Brief | The question | The user | The data source |
|---|---|---|---|
| [Clean Hours](clean-hours.md) | Which 3-hour window in the next 48 hours has the cleanest grid electricity in each region, and how good were last month's forecasts? | The operations planner of an electric-van depot | Carbon Intensity API (Great Britain), CC BY 4.0, no key |
| [City Fix](city-fix.md) | Which complaint types take longest to close in each borough, and is the time to close getting shorter? | An operations analyst at a city's transport agency | NYC Open Data, 311 Service Requests, no restrictions on use, app token advised |
| [River Rise](river-rise.md) | How many hours after heavy rain does each river station peak, and which came closest to its typical high level? | A council's flood-response planner | Environment Agency flood-monitoring API (England), Open Government Licence, no key |
| [Research Pulse](research-pulse.md) | How many articles does each of 20 journals publish a month, and how many citations do they gather in their first year? | A university library's journal-subscriptions manager | Crossref REST API, metadata free to use, no key |

How they differ:

- **Clean Hours** and **River Rise** need no key and no sign-up. Your mentor may suggest one of them if you are at the Guided level.
- **City Fix** has the largest source and the slowest API. Its hard part is the incremental load by a change timestamp.
- **River Rise** has the most data: a 62 MB file a day. Its hard part is reading only what you need.
- **Research Pulse** has nested JSON and cursor paging. Its hard part is a weekly snapshot of a number that keeps changing.

If two briefs appeal to you, pick the one whose user you understand best. You write that user's question next, in CP1 task 8.

## Pitch your own product

You may build your own data product instead, if it passes the four tests in the [capstone README](../README.md#pitch-your-own-product). In short:

1. It fits about 40 hours across weeks 28 to 30 (M1 about 18 hours, M2 about 17, M3 about 5), with one or two sources.
2. It covers all seven required parts.
3. Its main source is real, public, reachable and changes over time, and its licence allows use in a paid course. A "non-commercial only" licence fails this test.
4. It needs no real personal data (or masks it after the raw layer, as in P13), and at most three ideas the course has not taught.

### Before you pitch: check the source by hand

A source you cannot reach is not a plan. Before you show your mentor, do these four checks and keep the output for CP1 task 9:

1. **It answers.** Run `curl -s -o /dev/null -w "%{http_code} %{size_download}\n" "<data address>"`. You should see `200` and a size in bytes.
2. **It is data.** Run `curl -s "<data address>" | head -c 800`. You should see JSON or CSV, not an HTML web page.
3. **You may use it.** Find the licence or the terms of use on the publisher's own site. Write its name and address. Look for "non-commercial", "no redistribution" or "personal use only": each one fails test 3.
4. **It changes.** Find the date of the newest record. If nothing changed in the last month, the source fails test 3: a capstone pipeline must have new data to load.

### What makes a pitch too big

- More than two sources, or a source that needs a paid plan.
- A live stream when the user decides once a day or once a week.
- A source that holds real people's names, phone numbers, emails or health records, with no plan to mask them after the raw layer.
- A tool or language the course has not taught, such as a new database, a new orchestrator or a web framework. An HTTP API as your serving part counts as one untaught idea.
- A source the course already used, with the same question as its project. Choose a new source or a new question, so that the work is your own.

### How to pitch

In CP1 task 7, write `## Product` in your `capstone/PLAN.md` with `Brief: own idea` in the top lines, and run the `curl` check above. Show `## Product` to your mentor the same day. Your mentor tells you early if the pitch is too big, and may suggest one of the four briefs instead.
