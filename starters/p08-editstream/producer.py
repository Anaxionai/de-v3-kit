"""Read the live Wikipedia edit stream and send every event to the Kafka topic wiki-edits.

Task 8. Run it from the editstream/ folder, with Kafka running:

    uv run python producer.py --seconds 120

It prints one line at the end: sent <N> events to wiki-edits in <S> seconds
"""

STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"
BOOTSTRAP = "localhost:9092"  # Kafka from your laptop
TOPIC = "wiki-edits"
# Wikimedia refuses generic clients: name your tool and a contact, such as your GitHub page.
USER_AGENT = "editstream/1.0 (github.com/<your-id>)"


def parse_args(argv: list[str] | None = None):
    """Read the command line with argparse: --seconds, a whole number, default 60."""
    raise NotImplementedError("TODO(task 8): add the --seconds option")


def is_canary(change: dict) -> bool:
    """True for Wikimedia's test events: change["meta"]["domain"] is "canary"."""
    raise NotImplementedError("TODO(task 8): spot a canary event")


def main(argv: list[str] | None = None) -> None:
    """Send live events to TOPIC for --seconds seconds.

    - Open STREAM_URL with EventSource from requests_sse, with a User-Agent header.
    - For each event whose type is "message": change = json.loads(event.data).
      Skip canary events.
    - Send the others with a confluent_kafka Producer on BOOTSTRAP:
      produce(TOPIC, key=change["wiki"], value=event.data), then poll(0).
    - When the time is up, leave the loop, call flush() and print
      "sent <N> events to wiki-edits in <S> seconds".
    """
    raise NotImplementedError("TODO(task 8): read the stream and produce to Kafka")


if __name__ == "__main__":
    main()
