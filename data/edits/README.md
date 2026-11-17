# The Wikimedia live edit stream for EditStream (P8)

Every edit on Wikipedia and its sister projects appears within seconds in a public stream.
EditStream's `producer.py` reads it and sends each event to your Kafka topic `wiki-edits`.
This folder also holds `late_and_duplicate.py`, which builds the test stream for task 12.

| File | What it is |
|---|---|
| `README.md` | The stream's address, its events, the polite-use rules and the test stream |
| `late_and_duplicate.py` | Makes the test topic `wiki-edits-test` from your own `wiki-edits` and prints the right answer |

## The address

```text
https://stream.wikimedia.org/v2/stream/recentchange
```

- It never ends: the server keeps the connection open and sends events as they happen.
- The format is Server-Sent Events (SSE): plain text with `content-type: text/event-stream`. Each event is a few lines; the `data:` line holds the event as JSON.
- EventStreams itself runs on Kafka. Each event's SSE `id` is a JSON list with the Kafka topic, partition and time it came from.
- On 13 November 2026 a 100-second read returned HTTP 200 and 4,272 events, about 43 a second. Expect 20 to 50 a second, depending on the hour.

In Python, `requests-sse` reads the stream (this is what task 8 uses):

```python
import json
from requests_sse import EventSource

headers = {"User-Agent": "editstream/1.0 (github.com/<your-id>)"}
with EventSource("https://stream.wikimedia.org/v2/stream/recentchange", headers=headers) as stream:
    for event in stream:
        if event.type == "message":
            change = json.loads(event.data)
            if change["meta"]["domain"] == "canary":
                continue                     # a test event: skip it
            print(change["wiki"], change["type"], change["title"])
```

## One event

A real `edit` event from English Wikipedia, read on 13 November 2026 (an edit by a bot):

```json
{
  "$schema": "/mediawiki/recentchange/1.0.0",
  "meta": {
    "uri": "https://en.wikipedia.org/wiki/Egg_Harbour",
    "request_id": "df86d342-007b-4b9f-bed5-cefe9c15e053",
    "id": "dbea06a8-ffda-48ac-a5fa-631aa272eeee",
    "domain": "en.wikipedia.org",
    "stream": "mediawiki.recentchange",
    "dt": "2026-11-12T20:43:08.532Z",
    "topic": "codfw.mediawiki.recentchange",
    "partition": 0,
    "offset": 2148861904
  },
  "id": 2089572789,
  "type": "edit",
  "namespace": 0,
  "title": "Egg Harbour",
  "title_url": "https://en.wikipedia.org/wiki/Egg_Harbour",
  "comment": "Dating maintenance tags: {{Use dmy dates}}",
  "timestamp": 1794516187,
  "user": "AnomieBOT",
  "bot": true,
  "notify_url": "https://en.wikipedia.org/w/index.php?diff=1385329393&oldid=1385325905",
  "minor": true,
  "length": {
    "old": 1292,
    "new": 1311
  },
  "revision": {
    "old": 1385325905,
    "new": 1385329393
  },
  "server_url": "https://en.wikipedia.org",
  "server_name": "en.wikipedia.org",
  "server_script_path": "/w",
  "wiki": "enwiki",
  "parsedcomment": "Dating maintenance tags: {{Use dmy dates}}"
}
```

Some events have fields this one lacks, such as `patrolled`. Your code must not expect every field in every event.

## The fields EditStream uses

Compare your `EVENT_SCHEMA` (task 10) with this table. A name or a type that differs gives you a column of nulls.

| Field | JSON type | Spark type | Meaning |
|---|---|---|---|
| `meta.id` | string | `StringType` | A unique id (a UUID) for this event. EditStream calls it `event_id` |
| `meta.domain` | string | `StringType` | The site, for example `en.wikipedia.org`, `www.wikidata.org` or `canary` |
| `type` | string | `StringType` | `edit`, `new` (a new page), `log`, `categorize` or `external` |
| `title` | string | `StringType` | The page's title |
| `user` | string | `StringType` | Who made the change: a user name, or an IP address for people who are not signed in |
| `bot` | boolean | `BooleanType` | `true` when a bot account made the change |
| `timestamp` | number | `LongType` | When the change happened, in Unix seconds (seconds since 1970-01-01 UTC). This is the event time |
| `wiki` | string | (Kafka key) | The wiki's short name, for example `enwiki`. `producer.py` uses it as the message key |

`meta.dt` is the same moment as text with milliseconds. It is usually 0 to 10 seconds after `timestamp`.
`language` in EditStream is the first part of `meta.domain`: `en` from `en.wikipedia.org`.
Only some events are Wikipedia edits: many are edits on Wikidata or Commons, page moves and log entries, and about 4 in 10 of the Wikipedia edits come from bots.

## Polite use: the rules

From the Wikitech [EventStreams page](https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams_HTTP_Service) and the Wikimedia [User-Agent policy](https://foundation.wikimedia.org/wiki/Policy:Wikimedia_Foundation_User-Agent_Policy):

1. **Send a User-Agent that names your program and a way to contact you**, for example `editstream/1.0 (github.com/<your-id>)`. A missing or generic one can get HTTP 403.
2. **Open one connection.** Never run two producers at the same time.
3. **Expect the connection to close after 15 minutes.** The server ends every connection then. `requests-sse` connects again by itself and carries on from the last event it saw (the `Last-Event-ID` header).
4. **Skip canary events** (`meta.domain` is `canary`). Wikimedia sends them a few times an hour to test the stream. They are not edits.
5. **Ask for history sparingly.** The stream keeps about 7 to 31 days, and `?since=<time>` reads from that time. The page says: "Please be kind when providing timestamps." EditStream reads only live events, so it never needs `since`.
6. The service is meant for "small scale external tool developers". A student project is exactly that.

## The test stream for task 12: `late_and_duplicate.py`

Live edits arrive in a different order every day, so nobody can say what a correct count is. The test stream fixes that.
The script takes 600 of **your** Wikipedia edits from `wiki-edits`, gives them new times on a fixed ten-minute timeline, and sends them to a new topic `wiki-edits-test` in a planned order.

Run it in Git Bash from `editstream/` (its uv environment has `confluent-kafka`), with Kafka running:

```bash
uv run python ~/de-kit/data/edits/late_and_duplicate.py
```

What it does:

1. It reads `wiki-edits` from the start, with its own throw-away consumer that commits nothing, so your consumer group `editstream-counter` is not touched. It keeps the first 600 events (oldest first) whose `type` is `edit`, whose `meta.domain` ends with `.wikipedia.org` and whose `meta.id` it has not seen.
2. It deletes `wiki-edits-test` if it exists and creates it again with **1 partition**. With one partition, Spark reads the messages in the order they were sent, and every run gives the same batches.
3. It moves the 600 edits onto **2026-01-01 10:00:00 to 10:09:59 UTC**, one edit a second, 60 a minute. It rewrites `timestamp` and `meta.dt` to the new time and keeps every other field, including `meta.id`, `wiki`, `title`, `user` and `bot`.
4. It sends them with `wiki` as the key, in time order, except for these planted groups:
   - **30 duplicates**: 30 edits from 10:02:00 to 10:07:59 are sent a second time, byte for byte, about 1 minute of event time after the first copy.
   - **20 late edits**: the edits of 10:05:40 to 10:05:59 are held back and sent right after the last 10:06 edit.
   - **10 very late edits**: the edits of 10:01:00 to 10:01:09 are held back and sent after the last 10:09 edit.
   - **1 clock tick**: one more real edit, with a new `meta.id` and its time set to 10:15:00, is sent last.
5. It prints the right answer.

That is 631 messages. With the defaults it prints exactly this (run on 13 November 2026 against the kit's Kafka):

```text
read 600 Wikipedia edits from wiki-edits
created wiki-edits-test with 1 partition
sent 631 messages to wiki-edits-test:
  600 edits moved onto 2026-01-01 10:00:00 to 10:09:59 UTC, 60 per minute
  30 duplicates: sent a second time, about 1 minute later
  20 late edits from 10:05:40 to 10:05:59, sent after the 10:06 edits (about 1 minute late)
  10 very late edits from 10:01:00 to 10:01:09, sent after the 10:09 edits (about 8 minutes late)
  1 clock tick at 10:15:00, sent last: it closes every window before 10:13 for a 2-minute watermark
right answer for one-minute windows with a 2-minute watermark:
window_start          edits
2026-01-01 10:00:00   60
2026-01-01 10:01:00   50
2026-01-01 10:02:00   60
(10:03 to 10:09: 60 each)
total                 590
a job that does not drop duplicates shows 620
```

The window labels are in UTC. Your edits differ from everyone else's, but the counts are the same for every student.

**Checked on a real Spark.** On 13 November 2026 a replay as task 12 describes it (Spark 4.2.1, `maxOffsetsPerTrigger` 25, `trigger(availableNow=True)`, a 2-minute watermark, append mode to the `memory` sink) counted 620 without `dropDuplicates`, 590 with it, and 600 when the whole topic was read in one batch.

If the script stops with `Not enough edits: found <N> Wikipedia edits in wiki-edits, need 600. Run producer.py for 5 more minutes.`, do that: `uv run python producer.py --seconds 300`, then run the script again.
Other messages: `topic wiki-edits not found` means you have not created and filled the topic (task 8); `cannot reach Kafka` means Kafka is not running in `editstream/`.

Running the script again is safe: it deletes and re-creates the test topic, and the same `wiki-edits` gives the same messages.

| Option | Meaning | Default |
|---|---|---|
| `--bootstrap` | Kafka's address from your laptop | `localhost:9092` |
| `--from-topic` | The topic your producer filled | `wiki-edits` |
| `--to-topic` | The test topic. It is deleted and created again | `wiki-edits-test` |
| `--edits` | Edits on the timeline: 600 or more, a multiple of 60 | `600` |
| `--seed` | Chooses which edits are sent twice | `42` |
| `--check` | Test the plan in memory, without Kafka | (off) |

The briefs and their right answers use the defaults. Change none of them for task 12.
`--check` builds the plan from made-up edits, checks every group above and the right answer, and ends with `check passed`. It needs no Kafka and no `confluent-kafka`.

The script talks only to your own Kafka. It never contacts Wikimedia.

## Licence and credit

The events describe edits to Wikimedia projects. The text on those projects, page titles and edit summaries included, is licensed CC BY-SA 4.0 under the Wikimedia Terms of Use. The EventStreams page states no separate licence for the stream.
EditStream keeps the events in Kafka and in the Git-ignored `data/` folder. Only a few pasted rows, screenshots and this README's example event leave your laptop. Credit them like this, for example in your product README:

```text
Edit events from Wikimedia EventStreams (https://stream.wikimedia.org/v2/stream/recentchange), describing edits to Wikimedia projects, CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
```

User names in the events are public on Wikipedia. Do not collect anything else about the people behind them.
