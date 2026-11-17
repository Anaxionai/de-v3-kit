"""Make a test stream with late and duplicate edits, for EditStream (P8, task 12).

It reads 600 real Wikipedia edits that your producer already put in `wiki-edits`,
moves them onto a fixed ten-minute timeline (2026-01-01 10:00:00 to 10:09:59 UTC,
one edit a second), and sends them to `wiki-edits-test` in an order that tests
windows, watermarks and deduplication:

- 30 edits are sent a second time, byte for byte, about 1 minute later;
- the 20 edits of 10:05:40 to 10:05:59 are held back and sent after the 10:06 edits;
- the 10 edits of 10:01:00 to 10:01:09 are held back and sent after the 10:09 edits;
- one more edit, with its time set to 10:15:00, is sent last as a clock tick.

The test topic has 1 partition, so Spark reads the messages in the order they were sent,
and every run gives the same batches. At the end the script prints the right answer.

Run it from editstream/ (its uv environment has confluent-kafka), with Kafka running:

    uv run python ~/de-kit/data/edits/late_and_duplicate.py

Test the plan without Kafka:

    uv run python ~/de-kit/data/edits/late_and_duplicate.py --check
"""

import argparse
import copy
import json
import random
import sys
import time
import uuid
from collections import Counter
from datetime import UTC, datetime, timedelta

START = datetime(2026, 1, 1, 10, 0, 0, tzinfo=UTC)   # the first edit of the test stream
WATERMARK_DELAY = 120                                 # seconds: the job's 2-minute watermark
DUPLICATES = 30
LATE = (5 * 60 + 40, 5 * 60 + 60)                     # 10:05:40 to 10:05:59, as seconds after START
VERY_LATE = (1 * 60, 1 * 60 + 10)                     # 10:01:00 to 10:01:09
DUPLICATE_FROM = (2 * 60, 8 * 60)                     # originals of the duplicates: 10:02:00 to 10:07:59


# ---------------------------------------------------------------- 1. read real edits from Kafka

def is_wikipedia_edit(change: dict) -> bool:
    meta = change.get("meta") or {}
    return (change.get("type") == "edit" and str(meta.get("domain", "")).endswith(".wikipedia.org")
            and bool(meta.get("id")) and isinstance(change.get("timestamp"), int) and bool(change.get("wiki")))


def read_edits(bootstrap: str, topic: str, wanted: int) -> list[dict]:
    """Read `topic` from its earliest offset and return Wikipedia edits, oldest first.

    It uses a throw-away consumer: it assigns every partition itself and commits nothing,
    so your consumer group's offsets are not touched.
    """
    from confluent_kafka import OFFSET_BEGINNING, Consumer, KafkaException, TopicPartition

    consumer = Consumer({"bootstrap.servers": bootstrap, "group.id": "late-and-duplicate-reader",
                         "enable.auto.commit": False, "auto.offset.reset": "earliest"})
    try:
        try:
            metadata = consumer.list_topics(topic, timeout=10)
        except KafkaException:
            sys.exit(f"cannot reach Kafka at {bootstrap}. Start it with `docker compose up -d` in editstream/.")
        if topic not in metadata.topics or metadata.topics[topic].error is not None:
            sys.exit(f"topic {topic} not found. Create it and fill it with producer.py (task 8).")

        # The last offset of each partition now: we stop there, even if your producer is still running.
        end = {}
        for p in metadata.topics[topic].partitions:
            low, high = consumer.get_watermark_offsets(TopicPartition(topic, p), timeout=10)
            if high > low:
                end[p] = high
        consumer.assign([TopicPartition(topic, p, OFFSET_BEGINNING) for p in end])

        found: dict[int, list] = {p: [] for p in end}   # per partition: (timestamp, partition, offset, edit)
        done: set[int] = set()
        empty_polls = 0
        while len(done) < len(end) and empty_polls < 10:
            message = consumer.poll(1.0)
            if message is None:
                empty_polls += 1
                continue
            empty_polls = 0
            if message.error():
                raise KafkaException(message.error())
            p, offset = message.partition(), message.offset()
            if p in done:
                continue
            try:
                change = json.loads(message.value())
            except (TypeError, ValueError):
                change = {}
            if is_wikipedia_edit(change):
                found[p].append((change["timestamp"], p, offset, change))
            if offset >= end[p] - 1 or len(found[p]) > wanted:   # enough from this partition
                done.add(p)
                consumer.pause([TopicPartition(topic, p)])
    finally:
        consumer.close()

    edits, ids = [], set()
    for _, _, _, change in sorted((item for items in found.values() for item in items), key=lambda i: i[:3]):
        if change["meta"]["id"] not in ids:                      # each edit once
            ids.add(change["meta"]["id"])
            edits.append(change)
    return edits


# ---------------------------------------------------------------- 2. plan the test stream

def at(seconds: int) -> datetime:
    return START + timedelta(seconds=seconds)


def move(change: dict, seconds: int, new_id: str | None = None) -> bytes:
    """A copy of the edit with its time set to START + seconds, as the JSON bytes Kafka stores."""
    change = copy.deepcopy(change)
    change["timestamp"] = int(at(seconds).timestamp())
    change["meta"]["dt"] = at(seconds).strftime("%Y-%m-%dT%H:%M:%SZ")
    if new_id:
        change["meta"]["id"] = new_id
    return json.dumps(change, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def make_plan(edits: list[dict], count: int, seed: int) -> list[tuple[str, bytes]]:
    """The messages to send, in order, as (key, value). Edit i gets the time START + i seconds."""
    rng = random.Random(seed)
    values = [move(edits[i], i) for i in range(count)]
    keys = [edits[i]["wiki"] for i in range(count)]
    late = set(range(*LATE))
    very_late = set(range(*VERY_LATE))
    held_back = late | very_late

    # 30 duplicates: each is sent again after the edit 45 to 75 seconds later in event time.
    originals = rng.sample([i for i in range(*DUPLICATE_FROM) if i not in held_back], DUPLICATES)
    again_after: dict[int, list[int]] = {}
    for i in sorted(originals):
        after = rng.choice([i + d for d in range(45, 76) if i + d not in held_back])
        again_after.setdefault(after, []).append(i)

    last_of_minute_6 = 6 * 60 + 59                       # the last 10:06 edit
    plan = []
    for i in range(count):
        if i in held_back:
            continue
        plan.append((keys[i], values[i]))
        for j in again_after.get(i, []):
            plan.append((keys[j], values[j]))             # the same bytes a second time
        if i == last_of_minute_6:
            plan.extend((keys[j], values[j]) for j in sorted(late))
    plan.extend((keys[j], values[j]) for j in sorted(very_late))   # after the last edit

    # The clock tick: one more real edit, 5 minutes after the last minute, with a new id.
    tick = edits[count] if len(edits) > count else edits[0]
    tick_id = str(uuid.UUID(int=rng.getrandbits(128), version=4))
    plan.append((tick["wiki"], move(tick, (count // 60 + 5) * 60, new_id=tick_id)))
    return plan


def right_answer(count: int) -> tuple[dict[datetime, int], int]:
    """Edits per one-minute window for a job with a 2-minute watermark that drops duplicates.

    Every edit counts once, in its own minute, except the very late ones: their window
    closed long before they arrived. The clock tick's own window never closes.
    """
    per_window = Counter()
    for i in range(count):
        if i not in range(*VERY_LATE):
            per_window[at(i - i % 60)] += 1
    return dict(sorted(per_window.items())), sum(per_window.values()) + DUPLICATES


# ---------------------------------------------------------------- 3. send it to Kafka

def recreate_topic(bootstrap: str, topic: str) -> None:
    """Delete the test topic if it exists, then create it again with 1 partition."""
    from confluent_kafka import KafkaException
    from confluent_kafka.admin import AdminClient, NewTopic

    admin = AdminClient({"bootstrap.servers": bootstrap})
    if topic in admin.list_topics(timeout=10).topics:
        admin.delete_topics([topic])[topic].result()
    for _ in range(30):                                   # deleting takes a moment
        try:
            admin.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])[topic].result()
            return
        except KafkaException:
            time.sleep(1)
    sys.exit(f"could not create {topic}. Run the script again in a minute.")


def send(bootstrap: str, topic: str, plan: list[tuple[str, bytes]]) -> int:
    from confluent_kafka import Producer

    failed = []
    # One request in flight at a time keeps the messages in the order we send them, even after a retry.
    producer = Producer({"bootstrap.servers": bootstrap, "acks": "all",
                         "max.in.flight.requests.per.connection": 1})
    for key, value in plan:
        producer.produce(topic, key=key, value=value,
                         on_delivery=lambda err, _msg: failed.append(err) if err else None)
        producer.poll(0)
    producer.flush(30)
    if failed:
        sys.exit(f"{len(failed)} messages were not delivered: {failed[0]}")
    return len(plan)


# ---------------------------------------------------------------- the command line

def print_summary(count: int, from_topic: str, to_topic: str, sent: int) -> None:
    minutes = count // 60
    last = at(count - 1)
    tick = at((minutes + 5) * 60)
    windows, without_dedup = right_answer(count)
    total = sum(windows.values())
    print(f"sent {sent} messages to {to_topic}:")
    print(f"  {count} edits moved onto {START:%Y-%m-%d %H:%M:%S} to {last:%H:%M:%S} UTC, 60 per minute")
    print(f"  {DUPLICATES} duplicates: sent a second time, about 1 minute later")
    print(f"  {LATE[1] - LATE[0]} late edits from {at(LATE[0]):%H:%M:%S} to {at(LATE[1] - 1):%H:%M:%S}, "
          f"sent after the 10:06 edits (about 1 minute late)")
    print(f"  {VERY_LATE[1] - VERY_LATE[0]} very late edits from {at(VERY_LATE[0]):%H:%M:%S} to "
          f"{at(VERY_LATE[1] - 1):%H:%M:%S}, sent after the {last:%H:%M} edits (about {minutes - 2} minutes late)")
    print(f"  1 clock tick at {tick:%H:%M:%S}, sent last: it closes every window before "
          f"{tick - timedelta(seconds=WATERMARK_DELAY):%H:%M} for a 2-minute watermark")
    print("right answer for one-minute windows with a 2-minute watermark:")
    print("window_start          edits")
    starts = list(windows)
    for start in starts[:3]:
        print(f"{start:%Y-%m-%d %H:%M:%S}   {windows[start]}")
    print(f"({starts[3]:%H:%M} to {starts[-1]:%H:%M}: 60 each)")
    print(f"total                 {total}")
    print(f"a job that does not drop duplicates shows {without_dedup}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fill a 1-partition test topic with real edits re-sent late and twice, then print the right answer.")
    parser.add_argument("--bootstrap", default="localhost:9092", help="Kafka address (default localhost:9092)")
    parser.add_argument("--from-topic", default="wiki-edits", help="topic your producer filled (default wiki-edits)")
    parser.add_argument("--to-topic", default="wiki-edits-test",
                        help="test topic, deleted and created again (default wiki-edits-test)")
    parser.add_argument("--edits", type=int, default=600,
                        help="edits on the timeline: 600 or more, a multiple of 60 (default 600)")
    parser.add_argument("--seed", type=int, default=42, help="chooses the duplicates (default 42)")
    parser.add_argument("--check", action="store_true", help="test the plan in memory, without Kafka")
    args = parser.parse_args(argv)
    if args.edits < 600 or args.edits % 60:
        parser.error("--edits must be 600 or more, and a multiple of 60")
    if args.check:
        return run_check(args.edits, args.seed)
    if args.from_topic == args.to_topic:
        parser.error("--to-topic must differ from --from-topic: the test topic is deleted and created again")

    edits = read_edits(args.bootstrap, args.from_topic, args.edits)
    if len(edits) < args.edits:
        print(f"Not enough edits: found {len(edits)} Wikipedia edits in {args.from_topic}, need {args.edits}. "
              f"Run producer.py for 5 more minutes.")
        return 1
    print(f"read {args.edits} Wikipedia edits from {args.from_topic}")
    recreate_topic(args.bootstrap, args.to_topic)
    print(f"created {args.to_topic} with 1 partition")
    sent = send(args.bootstrap, args.to_topic, make_plan(edits, args.edits, args.seed))
    print_summary(args.edits, args.from_topic, args.to_topic, sent)
    return 0


# ---------------------------------------------------------------- --check: test the plan without Kafka

def replay(plan: list[tuple[str, bytes]], batch_size: int, drop_duplicates: bool) -> dict[int, int]:
    """Count edits per window the way Spark's replay does: batches of `batch_size` messages,
    a watermark that moves at the end of each batch, append mode (a window is written once
    the watermark passes its end). Returns {window start (Unix seconds): edits}."""
    watermark, newest, seen, counts = 0, 0, set(), Counter()
    for first in range(0, len(plan), batch_size):
        batch = [json.loads(value) for _, value in plan[first:first + batch_size]]
        for change in batch:
            t = change["timestamp"]
            if drop_duplicates:
                if t <= watermark or (change["meta"]["id"], t) in seen:
                    continue
                seen.add((change["meta"]["id"], t))
            window = t - t % 60
            if window + 60 <= watermark:                  # its window is already closed
                continue
            counts[window] += 1
        newest = max(newest, *(change["timestamp"] for change in batch))
        watermark = max(watermark, newest - WATERMARK_DELAY)
    return {w: n for w, n in counts.items() if w + 60 <= watermark}


def run_check(count: int, seed: int) -> int:
    problems = []

    def expect(condition: bool, message: str) -> None:
        print(("ok    " if condition else "FAIL  ") + message)
        if not condition:
            problems.append(message)

    fake = [{"$schema": "/mediawiki/recentchange/1.0.0", "type": "edit", "wiki": f"{lang}wiki",
             "title": f"Page {n}", "user": f"User {n}", "bot": n % 3 == 0, "timestamp": 1763000000 + n,
             "meta": {"id": str(uuid.UUID(int=n + 1)), "domain": f"{lang}.wikipedia.org", "dt": ""}}
            for n, lang in enumerate(["en", "de", "ar", "hi", "fr"] * (count // 5 + 1))][:count + 1]
    plan = make_plan(fake, count, seed)
    events = [json.loads(value) for _, value in plan]
    times = [e["timestamp"] - int(START.timestamp()) for e in events]
    expect(len(plan) == count + DUPLICATES + 1, f"{len(plan)} messages: {count} edits, {DUPLICATES} duplicates, 1 tick")
    expect(make_plan(fake, count, seed) == plan, "the same edits and seed give the same messages")

    values = Counter(value for _, value in plan)
    twice = [v for v, n in values.items() if n == 2]
    gaps = []
    for value in twice:
        first, second = [i for i, (_, v) in enumerate(plan) if v == value]
        gaps.append(max(times[:second]) - times[first])
    expect(len(twice) == DUPLICATES and max(values.values()) == 2, "30 edits are sent twice, byte for byte")
    expect(all(45 <= g <= 75 for g in gaps), f"each second copy comes 45 to 75 s of event time later ({min(gaps)} to {max(gaps)})")
    originals = sorted(json.loads(v)["timestamp"] - int(START.timestamp()) for v in twice)
    expect(all(DUPLICATE_FROM[0] <= t < DUPLICATE_FROM[1] and t not in range(*LATE) for t in originals),
           "the duplicated edits are from 10:02:00 to 10:07:59, outside the held-back groups")

    pos = {t: i for i, t in reversed(list(enumerate(times)))}   # first position of each time
    late_pos = [pos[t] for t in range(*LATE)]
    expect(late_pos == list(range(late_pos[0], late_pos[0] + 20)) and max(times[:late_pos[0]]) == 6 * 60 + 59,
           "the 20 late edits come together, right after the last 10:06 edit")
    very_pos = [pos[t] for t in range(*VERY_LATE)]
    expect(very_pos == list(range(len(plan) - 11, len(plan) - 1)) and max(times[:very_pos[0]]) == count - 1,
           "the 10 very late edits come after the last edit of the timeline")
    expect(times[-1] == (count // 60 + 5) * 60 and events[-1]["meta"]["id"] not in {e["meta"]["id"] for e in events[:-1]},
           "the clock tick is last, at 10:15:00 for 600 edits, with a new id")
    expect(all(e["timestamp"] == int(datetime.strptime(e["meta"]["dt"], "%Y-%m-%dT%H:%M:%SZ")
                                     .replace(tzinfo=UTC).timestamp()) for e in events), "meta.dt matches timestamp")

    windows, without_dedup = right_answer(count)
    expected = {int(w.timestamp()): n for w, n in windows.items()}
    small = replay(plan, 25, drop_duplicates=True)
    expect(small == expected, f"batches of 25 with deduplication give the right answer: total {sum(small.values())}, "
           f"10:01 = {small.get(int(at(60).timestamp()))}, 10:05 = {small.get(int(at(300).timestamp()))}")
    no_dedup = replay(plan, 25, drop_duplicates=False)
    expect(sum(no_dedup.values()) == without_dedup, f"without deduplication the total is {sum(no_dedup.values())}")
    one_batch = replay(plan, len(plan), drop_duplicates=True)
    expect(sum(one_batch.values()) == count, f"read in one batch, the total is {sum(one_batch.values())} (the Stuck line)")
    if count == 600:
        expect(sum(expected.values()) == 590 and expected[int(at(60).timestamp())] == 50 and without_dedup == 620,
               "the printed answer is 590, 10:01 = 50, 620 without deduplication")
    robust = all(replay(make_plan(fake, count, s), 25, True) == expected for s in range(1, 51))
    expect(robust, "the same answer for seeds 1 to 50")

    print()
    if problems:
        print(f"check FAILED: {len(problems)} problem(s)")
        return 1
    print("check passed. The printed answer would be:")
    print_summary(count, "wiki-edits", "wiki-edits-test", len(plan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
