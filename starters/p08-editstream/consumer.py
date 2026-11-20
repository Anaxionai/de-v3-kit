"""Read wiki-edits as the consumer group editstream-counter, and commit offsets yourself.

Task 9. Run it from the editstream/ folder, with Kafka running:

    uv run python consumer.py                    # until 10 empty polls in a row
    uv run python consumer.py --crash-after 250  # stop hard after 250 messages
"""

from pathlib import Path

BOOTSTRAP = "localhost:9092"  # Kafka from your laptop
TOPIC = "wiki-edits"
GROUP = "editstream-counter"
COMMIT_EVERY = 100  # messages processed between two commits
EMPTY_POLLS_TO_STOP = 10
PROCESSED_LOG = Path("data") / "processed.log"  # data/ is ignored by Git


def parse_args(argv: list[str] | None = None):
    """Read the command line with argparse: --crash-after N, a whole number, default none."""
    raise NotImplementedError("TODO(task 9): add the --crash-after option")


def make_consumer():
    """Return a confluent_kafka Consumer on BOOTSTRAP in the group GROUP.

    Turn auto commit off, and start from the earliest offset when the group
    has no committed offset yet.
    """
    raise NotImplementedError("TODO(task 9): configure the consumer")


def process(msg, log) -> None:
    """Append one line "<partition>:<offset> <wiki>" for the message to the open log file.

    The wiki is json.loads(msg.value())["wiki"].
    """
    raise NotImplementedError("TODO(task 9): process one message")


def main(argv: list[str] | None = None) -> None:
    """Consume TOPIC and commit after the work, never before it.

    - Subscribe, then loop on consumer.poll(1.0). Skip a None message or one
      with msg.error() set.
    - Process each message. After every COMMIT_EVERY processed messages, call
      consumer.commit(asynchronous=False) and print "committed after <N> messages".
    - With --crash-after N: after N processed messages call os._exit(1), with no
      commit and no close, like a power cut.
    - After EMPTY_POLLS_TO_STOP empty polls in a row: commit, close the consumer
      and print the total.
    """
    raise NotImplementedError("TODO(task 9): the poll, process and commit loop")


if __name__ == "__main__":
    main()
