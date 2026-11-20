"""The failure alert: one chat message when a PageLake run fails for good (task 12).

Airflow calls send_alert(context) as the DAG's on_failure_callback. The webhook
address comes from PAGELAKE_ALERT_WEBHOOK in .env. Anyone with the address can
post to your channel, so it never goes in a committed file: .env.example holds
the name with an empty value.

The requests package is in the Airflow image. On your laptop it came with
PyIceberg in P5.
"""


def send_alert(context) -> None:
    """Post one message about the failed run to the chat webhook.

    - Read the address from PAGELAKE_ALERT_WEBHOOK. If it is empty, print one
      line saying no alert was sent, and return.
    - Build the message from context.get("ds") (the day), context.get("reason")
      and context.get("ti") (the failed task instance, with its task_id; it can
      be None).
    - Post it with requests.post(url, json={"content": message}, timeout=10).
      Discord reads "content"; Slack and Google Chat read "text".
    """
    raise NotImplementedError("TODO(task 12): post the alert to the webhook")
