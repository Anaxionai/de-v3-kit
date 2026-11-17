# GH Archive: GitHub events for GitPulse (P9)

GH Archive (https://www.gharchive.org) records GitHub's public events: pushes, pull requests, stars, new repositories and more.
It keeps one gzip-compressed file per hour, from 2011 to today. GitPulse loads one day of these files into Snowflake.

The course uses **1 and 2 January 2018**. A day in 2018 is about 215 MB; a day in 2024-2025 is 2.3-2.8 GB, too much for a laptop and a trial account.

## What is in this folder

| File | What it is |
|---|---|
| `get_hours.py` | Downloads the hourly files for one date. Standard library only. |
| `README.md` | This guide. |

The data is not in the kit. `get_hours.py` puts it in `data/gharchive/`, which Git ignores.

## Download the files

Run these in Git Bash, from your `gitpulse/` folder:

```bash
uv run python ~/de-kit/data/gharchive/get_hours.py --date 2018-01-01 --hours 0-23 --out data/gharchive
uv run python ~/de-kit/data/gharchive/get_hours.py --date 2018-01-02 --hours 0-2
uv run python ~/de-kit/data/gharchive/get_hours.py --date 2018-01-02 --hours 4-5
uv run python ~/de-kit/data/gharchive/get_hours.py --date 2018-01-02 --hours 3
```

| Option | Meaning | Default |
|---|---|---|
| `--date` | the day, `YYYY-MM-DD` (UTC) | (required) |
| `--hours` | one hour (`3`) or a range (`0-23`) | `0-23` |
| `--out` | the folder for the files; made if missing | `data/gharchive` |
| `--check` | download nothing; read every file to the end and count its events | off |

You see one line per file and a total. The first command took about 3 minutes here:

```text
24 hourly files for 2018-01-01 into data/gharchive/
2018-01-01-0.json.gz        6.4 MB  saved in 4 s
...
2018-01-01-23.json.gz      10.5 MB  saved in 5 s
Total: 24 of 24 files, 215.4 MB (24 downloaded, 0 already there, 0 missing)
```

Good to know:

- **Safe to run twice.** A file already there with the right size is skipped. A file is saved under a `.part` name and renamed only when complete, so a stopped download never looks finished. Run the same command again to finish it.
- **Network trouble** is retried 3 times (after 10, 20 and 40 seconds).
- **A missing hour** prints `NOT FOUND on GH Archive`, the script goes on with the next hour, and it ends with exit code 1.
- **Check your files** with `--check`. It prints the number of events in each file, which you can compare with the tables below.

## The address pattern

```text
https://data.gharchive.org/YYYY-MM-DD-H.json.gz
```

`H` is the hour in UTC with **no leading zero**: `0`, `1`, ... `23`. For example, 3 pm UTC on 1 January 2018 is `https://data.gharchive.org/2018-01-01-15.json.gz`.
The files keep these names on your disk, still gzipped.

## One line is one event

Each file is gzip-compressed JSON, **one event per line**. Look at the start of one file:

```bash
gzip -dc data/gharchive/2018-01-01-12.json.gz | head -c 600
```

Every event has these fields:

| Field | What it holds |
|---|---|
| `id` | the event id, **a string** of digits, such as `"7044972064"` |
| `type` | the event type, such as `PushEvent` |
| `actor` | who did it: `id`, `login`, `display_login`, `gravatar_id`, `url`, `avatar_url` |
| `repo` | the repository: `id`, `name` (`owner/repository`), `url` |
| `payload` | the details; different for each event type |
| `public` | `true` (every event in hour 12 checked) |
| `created_at` | when it happened, UTC, ISO format with a `Z`: `2018-01-01T12:00:00Z` |
| `org` | the organisation that owns the repository; present on 8,214 of the 30,262 events in hour 12 |

In these files every event's `created_at` falls inside the file's own hour.

## Event types

The 30 hours hold 14 event types. The ones GitPulse uses:

| GitPulse table | Event type | Useful payload fields |
|---|---|---|
| `PUSHES` | `PushEvent` | `push_id`, `ref`, `size`, `distinct_size`, `head`, `before`, `commits` |
| `PULL_REQUESTS` | `PullRequestEvent` | `action` (`opened`, `closed` or `reopened`), `number`, `pull_request.id`, `pull_request.title`, `pull_request.state`, `pull_request.merged`, `pull_request.additions`, `pull_request.deletions`, `pull_request.changed_files`, `pull_request.base.repo.language` |
| `STARS` | `WatchEvent` | `action`: always `started` (every one in hours 5 and 12 checked). **A star is a `WatchEvent` with action `started`.** |

The other 11 types are `CreateEvent`, `IssueCommentEvent`, `IssuesEvent`, `ForkEvent`, `DeleteEvent`, `PullRequestReviewCommentEvent`, `GollumEvent` (wiki edits), `ReleaseEvent`, `MemberEvent`, `CommitCommentEvent` and `PublicEvent`.

## Expected counts

Measured on 13 November 2026 by downloading the 30 files and reading every line.
Every line is valid JSON and valid UTF-8, and **no event id appears twice** in the 30 files.

### 2018-01-01, all 24 hours (task 9)

| File | Bytes (gzip) | Events |
|---|---|---|
| `2018-01-01-0.json.gz` | 6,447,611 | 20,541 |
| `2018-01-01-1.json.gz` | 5,954,037 | 21,443 |
| `2018-01-01-2.json.gz` | 5,946,029 | 21,131 |
| `2018-01-01-3.json.gz` | 5,827,891 | 22,993 |
| `2018-01-01-4.json.gz` | 5,585,061 | 19,906 |
| `2018-01-01-5.json.gz` | 5,522,349 | 20,095 |
| `2018-01-01-6.json.gz` | 5,748,010 | 22,197 |
| `2018-01-01-7.json.gz` | 7,292,562 | 24,400 |
| `2018-01-01-8.json.gz` | 7,190,625 | 24,047 |
| `2018-01-01-9.json.gz` | 6,817,623 | 24,470 |
| `2018-01-01-10.json.gz` | 7,228,760 | 25,185 |
| `2018-01-01-11.json.gz` | 8,237,275 | 27,423 |
| `2018-01-01-12.json.gz` | 9,655,965 | 30,262 |
| `2018-01-01-13.json.gz` | 11,003,870 | 33,509 |
| `2018-01-01-14.json.gz` | 11,637,741 | 35,294 |
| `2018-01-01-15.json.gz` | 12,810,755 | 36,577 |
| `2018-01-01-16.json.gz` | 12,109,136 | 36,274 |
| `2018-01-01-17.json.gz` | 11,526,208 | 35,927 |
| `2018-01-01-18.json.gz` | 11,300,354 | 34,504 |
| `2018-01-01-19.json.gz` | 11,971,559 | 35,420 |
| `2018-01-01-20.json.gz` | 11,650,833 | 34,644 |
| `2018-01-01-21.json.gz` | 12,293,041 | 36,467 |
| `2018-01-01-22.json.gz` | 11,109,828 | 33,544 |
| `2018-01-01-23.json.gz` | 10,498,578 | 31,051 |
| **Total, 24 files** | **215,365,701** | **687,304** (687,304 distinct ids) |

### 2018-01-02, hours 0 to 5 (tasks 11 and 24)

| File | Bytes (gzip) | Events |
|---|---|---|
| `2018-01-02-0.json.gz` | 10,334,124 | 31,575 |
| `2018-01-02-1.json.gz` | 12,031,960 | 37,833 |
| `2018-01-02-2.json.gz` | 12,973,568 | 41,717 |
| `2018-01-02-3.json.gz` (the late hour) | 12,797,234 | 42,280 |
| `2018-01-02-4.json.gz` | 10,798,506 | 34,093 |
| `2018-01-02-5.json.gz` | 11,669,338 | 37,714 |
| **Hours 0-2 and 4-5 (task 11)** | **57,807,496** | **182,932** |
| **Hour 3 alone (task 24)** | **12,797,234** | **42,280** |

### Events per type

| Event type | 2018-01-01 (24 hours) | 2018-01-02 hours 0-2 and 4-5 | 2018-01-02 hour 3 |
|---|---|---|---|
| `PushEvent` | 391,963 | 95,592 | 22,411 |
| `CreateEvent` | 91,647 | 24,181 | 5,357 |
| `WatchEvent` | 61,746 | 25,353 | 6,175 |
| `IssueCommentEvent` | 36,087 | 9,279 | 1,819 |
| `PullRequestEvent` | 28,836 | 7,386 | 1,553 |
| `IssuesEvent` | 22,329 | 6,100 | 1,153 |
| `ForkEvent` | 20,429 | 6,718 | 1,878 |
| `DeleteEvent` | 18,041 | 4,210 | 1,106 |
| `PullRequestReviewCommentEvent` | 5,465 | 1,611 | 255 |
| `GollumEvent` | 4,484 | 972 | 255 |
| `ReleaseEvent` | 2,410 | 555 | 114 |
| `MemberEvent` | 1,741 | 526 | 116 |
| `CommitCommentEvent` | 1,250 | 256 | 57 |
| `PublicEvent` | 876 | 193 | 31 |
| **Total** | **687,304** | **182,932** | **42,280** |

After task 9 your typed tables should hold 391,963 pushes, 28,836 pull-request events and 61,746 stars.

## Pushes: `size` and the `commits` array

A `PushEvent` in these 2018 files has three numbers about commits:

- `size`: the number of commits in the push;
- `distinct_size`: how many of them are new to the repository (each commit in `commits` has `"distinct": true` or `false`);
- `commits`: a list of the commits, each with `sha`, `author` (`name`, `email`), `message`, `distinct` and `url`.

**The rule: `commits` holds at most 20 commits.** When a push has more than 20 commits, the list keeps the first 20 (oldest first) and `size` still gives the real number. So `ARRAY_SIZE(commits)` and `size` differ exactly on the pushes with more than 20 commits.

The evidence, measured on 13 November 2026:

- In all 30 files (509,966 pushes), no `commits` list is longer than 20. 3,969 pushes have `size` above 20, and those are the only pushes where `size` and the length of `commits` differ.
- In hours 12 and 13 of 2018-01-01 (35,203 pushes):
  - 31,111 pushes of 1 to 20 commits: the list length equals `size`, and the last commit in the list is the push's `head` commit, every time.
  - 425 pushes of more than 20 commits: every list holds exactly 20 commits, and the last one is never the `head` commit. The list stops after the first 20.
  - 3,667 pushes have `size` 0 and an empty list.
  - `size` never goes above 1,000 (10 pushes show exactly 1,000), and 8 pushes have a `distinct_size` larger than `size`, up to 10,506. So `size` also looks capped, at 1,000.

Two traps for task 10:

- `LATERAL FLATTEN` drops the pushes with an empty `commits` list. Add `OUTER => TRUE` if you need every push in the result.
- **GitHub's event types page has changed.** On 7 October 2025 GitHub removed "commit summaries and counts" from push events in its Events API. The PushEvent section of the page now lists only `repository_id`, `push_id`, `ref`, `head` and `before`. The 2018 files still have `size`, `distinct_size` and `commits`, as described here.

## Repository renames (task 25)

A repository keeps its `repo.id` when its owner renames it or moves it to another account, but `repo.name` changes. These hours contain real renames.

- 1,304 of the 223,570 repository ids in the 30 files appear under more than one name.
- **106** of them have a different latest name at the end of 2018-01-01 than at 05:59 on 2018-01-02. These are the renames that the two snapshot runs of task 25 can catch.
- 62 of the 1,304 differ only in capital letters. 118 change name more than once, and at least 1 of those goes back to an earlier name, so prefer the examples below.

Five clear renames to look for, all owned by organisations. Each has only the old name on 2018-01-01 and only the new name on 2018-01-02:

| `repo.id` | Name on 2018-01-01 | Name on 2018-01-02 | First event with the new name |
|---|---|---|---|
| 91280893 | `testdrivenio/test-driven` | `testdrivenio/testdriven-site` | 00:37:34 UTC, in `2018-01-02-0.json.gz` |
| 100129043 | `baianat/builder` | `baianat/Vuse` | 01:37:46 UTC, in `2018-01-02-1.json.gz` |
| 115744711 | `DudeCoin-Parity/DudeCoin` | `Dudecoin-Protocol/Dudecoin` | 02:25:06 UTC, in `2018-01-02-2.json.gz` |
| 97200377 | `SEEK-Jobs/gradle-aws-plugin` | `seek-oss/gradle-aws-plugin` | 03:42:29 UTC, in `2018-01-02-3.json.gz` (the late hour) |
| 115895226 | `Solo-Project/platform_device_huawe_angler` | `Solo-Project/platform_device_huawei_angler` | 03:29:23 UTC, in `2018-01-02-3.json.gz` (the late hour) |

In the snapshot, the old row's `dbt_valid_to` and the new row's `dbt_valid_from` should both be the time in the last column.
The last two need hour 3 of 2018-01-02, which you load in task 24.

## Personal data: what the course keeps out

These files hold personal data about real people:

- `actor.login`, `actor.display_login`, `actor.avatar_url` and `actor.gravatar_id`: who did each action;
- in every `PushEvent`, `commits[].author.name` (the author's name) and `commits[].author.email`. GH Archive replaces the part of the email before the `@` with a 40-character hash, but the domain stays readable, for example `<hash>@gmail.com`;
- titles and text of issues, pull requests and comments, which can contain anything.

The rules for GitPulse:

- **The course keeps commit author names and emails out of every table.** Do not select `commits[].author` into any Snowflake table, dbt model or file.
- Keep `actor_login` only where a task asks for it (the actor dimension), and never publish lists of logins.
- Never commit the downloaded files. `data/` stays in `.gitignore`.

## Licence and credit

- **GH Archive states no licence and no terms of use** on its website. The course cannot point to a licence that allows use in a paid course.
- The data is GitHub's public event stream. GitHub's Acceptable Use Policies (section 7, "Information Usage Restrictions") allow researchers to use "public, non-personal information" and archivists to use "public information", and forbid using it "for spamming purposes" or "selling personal information". Your use "must comply with the GitHub Privacy Statement".
- The kit stores none of the data: each student downloads it for their own learning, and GitPulse keeps only counts and the fields named above.

Credit the source in your README: **"Data: GH Archive (https://www.gharchive.org), a record of GitHub's public events."**

## The same data in BigQuery (P12, task 12)

GH Archive is also a BigQuery public dataset, "automatically updated every hour" (gharchive.org). It has one table per day in the dataset `githubarchive.day`, for example **`githubarchive.day.20180101`** for your GitPulse day.
gharchive.org says the common event fields are columns and `payload` is a JSON string. So `type` and `created_at` are columns, and `repo` is a record whose name you read with a dot: `repo.name` (the column names were not checked in BigQuery here).

Numbers for GitPulse part 2 (P12), which compares them with BigQuery:

| What | Value | How sure |
|---|---|---|
| Athena reading the raw files of 2018-01-01 | 215,365,701 bytes (the 24 `.json.gz` files above) | measured |
| BigQuery reading `type` and `created_at` of `githubarchive.day.20180101` | about 14 MB (687,304 rows x 8 bytes for the timestamp, plus 2 bytes and the length of the type name) | estimate from Google's data-type sizes; **not run** |
| Location of `githubarchive.day` | the `US` multi-region | **not checked** (no Google Cloud account was used) |

A dry run (`bq query --dry_run`) shows the real estimate without cost. BigQuery bills at least 10 MB for each table a query reads.

## Links

- GH Archive (GH Archive): https://www.gharchive.org/
- GitHub event types (GitHub Docs): https://docs.github.com/en/rest/using-the-rest-api/github-event-types
- Upcoming changes to GitHub Events API payloads (GitHub changelog, 8 August 2025): https://github.blog/changelog/2025-08-08-upcoming-changes-to-github-events-api-payloads/
- GitHub Acceptable Use Policies (GitHub Docs): https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies
