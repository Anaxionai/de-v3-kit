"""Watch live Wikipedia edits as they happen: your first look at a stream.

Run it in Git Bash:

    uv run python ~/de-kit/data/map/watch_edits.py
    uv run python ~/de-kit/data/map/watch_edits.py --seconds 60 --save data/edits.jsonl --quiet

It connects to Wikimedia's EventStreams service, which sends one event for
every change on every Wikimedia wiki (about 35 events a second). It prints
one line per event, a total every 10 seconds, and a summary at the end.

Options:
  --seconds N   stop after N seconds (default 60)
  --save PATH   append every event, unchanged, to PATH: one JSON object per line
  --quiet       print only the 10-second totals and the summary

Press Ctrl+C to stop early: the summary is still printed, and every event
saved so far stays in the file.

It uses only Python's standard library, so there is nothing to install.
Edit data from Wikimedia projects via EventStreams, CC BY-SA 4.0.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

STREAM = "https://stream.wikimedia.org/v2/stream/recentchange"
USER_AGENT = (f"de-course-kit/1.0 (https://github.com/Anaxionai/de-v3-kit; data/map/watch_edits.py) "
              f"python-urllib/{sys.version_info.major}.{sys.version_info.minor}")
REPORT_EVERY = 10  # seconds between total lines


def read_events(lines):
    """Turn the stream's text lines into (event_id, data_text) pairs.

    The stream uses the server-sent events format: an event is a few lines such as
    "id: ..." and "data: {...}", and a blank line ends it.
    """
    event_id, data = None, []
    for raw in lines:
        line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
        if line == "":
            if data:
                yield event_id, "\n".join(data)
            event_id, data = None, []
        elif line.startswith("data:"):
            data.append(line[5:].lstrip(" "))
        elif line.startswith("id:"):
            event_id = line[3:].lstrip(" ")
        # other lines ("event: message", comments starting with ":") are ignored


def edit_time(event):
    """When the change was made, as a UTC datetime (None if the event has no time)."""
    if isinstance(event.get("timestamp"), int):
        return datetime.fromtimestamp(event["timestamp"], tz=UTC)
    when = event.get("meta", {}).get("dt")
    return datetime.fromisoformat(when.replace("Z", "+00:00")) if when else None


def totals_text(counts):
    """For example: 412 events (edit 230, categorize 120, new 30, log 32)."""
    kinds = ", ".join(f"{kind} {number}" for kind, number in counts.most_common())
    return f"{sum(counts.values())} events ({kinds})" if kinds else "0 events"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Print live Wikipedia edits from Wikimedia EventStreams.")
    parser.add_argument("--seconds", type=int, default=60, help="stop after this many seconds (default 60)")
    parser.add_argument("--save", metavar="PATH", help="append each event as one JSON line to this file")
    parser.add_argument("--quiet", action="store_true", help="print only the totals and the summary")
    args = parser.parse_args(argv)
    if args.seconds < 1:
        parser.error("--seconds must be 1 or more")

    # Titles arrive in every alphabet; the default Windows code page would crash on them.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    save_file = None
    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        save_file = open(args.save, "a", encoding="utf-8", newline="\n")

    counts = Counter()
    largest_delay, largest_what = None, ""
    last_id = None  # lets us resume after the server closes the connection
    started = time.monotonic()
    next_report = REPORT_EVERY
    stopped_by = "time is up"
    print(f"Listening to {STREAM} for {args.seconds} s ...", flush=True)

    try:
        finished = False
        while not finished:
            headers = {"User-Agent": USER_AGENT, "Accept": "text/event-stream"}
            if last_id:
                headers["Last-Event-ID"] = last_id
            request = urllib.request.Request(STREAM, headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    for event_id, text in read_events(response):
                        arrived = datetime.now(UTC)
                        elapsed = time.monotonic() - started
                        while next_report <= elapsed and next_report <= args.seconds:
                            print(f"total after {next_report} s: {totals_text(counts)}", flush=True)
                            next_report += REPORT_EVERY
                        if elapsed >= args.seconds:
                            finished = True
                            break
                        if event_id:
                            last_id = event_id
                        try:
                            event = json.loads(text)
                        except json.JSONDecodeError:
                            continue  # not a complete event; skip it
                        if event.get("meta", {}).get("domain") == "canary":
                            continue  # Wikimedia's test events, not real changes

                        kind = event.get("type", "?")
                        counts[kind] += 1
                        made = edit_time(event)
                        if made is not None:
                            delay = (arrived - made).total_seconds()
                            if largest_delay is None or delay > largest_delay:
                                largest_delay = delay
                                largest_what = f"{kind} on {event.get('server_name', '?')}"
                        if save_file:
                            # One whole line per event, so DuckDB never sees half an event.
                            line = text if "\n" not in text else json.dumps(event, ensure_ascii=False)
                            save_file.write(line + "\n")
                        if not args.quiet:
                            local = arrived.astimezone().strftime("%H:%M:%S")
                            print(f"{local}  {event.get('server_name', '?'):<24} {kind:<10} "
                                  f"{event.get('title', '')}", flush=True)
                if not finished:
                    print("The server closed the connection; reconnecting from the last event ...", flush=True)
            except urllib.error.HTTPError as problem:
                if problem.code in (429, 500, 502, 503, 504) and time.monotonic() - started < args.seconds:
                    print(f"The stream answered HTTP {problem.code}; trying again in 10 s ...", flush=True)
                    time.sleep(10)
                else:
                    sys.exit(f"The stream answered HTTP {problem.code}. Try again in a few minutes.")
            except (urllib.error.URLError, TimeoutError, ConnectionError) as problem:
                if time.monotonic() - started >= args.seconds:
                    break
                print(f"Connection problem ({problem}); reconnecting in 5 s ...", flush=True)
                time.sleep(5)
            if time.monotonic() - started >= args.seconds:
                finished = True
    except KeyboardInterrupt:
        stopped_by = "Ctrl+C"
    finally:
        if save_file:
            save_file.close()

    seconds = min(time.monotonic() - started, args.seconds)
    print()
    print(f"Summary ({stopped_by}):")
    print(f"  events counted: {totals_text(counts)}")
    print(f"  seconds: {seconds:.0f}")
    print(f"  saved to: {args.save if args.save else 'not saved (add --save data/edits.jsonl)'}")
    if largest_delay is None:
        print("  largest delay between an edit and its arrival: no events")
    else:
        print(f"  largest delay between an edit and its arrival: {largest_delay:.1f} s ({largest_what})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
