"""Retries with backoff, for temporary failures of the API."""

import time


def is_retryable(error: Exception) -> bool:
    """Return True when another try may succeed:
    - httpx.TransportError (timeouts and lost connections);
    - ApiError with status 429, 500, 502, 503 or 504.
    Return False for every other error, such as ApiError 400, 401, 403 or 404.
    """
    raise NotImplementedError("TODO(task 12): write is_retryable()")


def call_with_retries(
    func, attempts: int = 4, base_delay: float = 1.0, sleep=time.sleep
):
    """Call func() and return its result, trying again after a temporary failure.

    - After a retryable error, wait base_delay, then twice it, then four times it
      (1, 2 and 4 seconds by default), and call func() again.
    - Call func() at most `attempts` times in all, then re-raise the last error.
    - Re-raise an error that is not retryable at once, with no wait.
    - Log a warning for each failed attempt: its number, the error and the wait.
    - Wait with the `sleep` argument, never time.sleep itself, so a test can pass
      sleep=waits.append and never wait.
    """
    raise NotImplementedError("TODO(task 12): write call_with_retries()")
