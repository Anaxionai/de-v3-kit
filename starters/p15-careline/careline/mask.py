"""Find and mask personal data in free text, and guard every model call.

Task 7 masks every visit note before anything else happens. From task 9 on,
every text sent to a model passes assert_masked() first. The patterns are the
ones the briefs give in full.
"""

# P13's widened phone pattern (P13, task 11): ten digits, with or without one
# space or dash after the fifth. It also finds the digits inside "+91 98765 43210"
# and "098765-43210".
PHONE = r"[0-9]{5}[ -]?[0-9]{5}"
# An email address (task 7, step 6).
EMAIL = r"[\w.+-]+@[\w-]+(\.[\w-]+)+"


def load_names(conn) -> list[str]:
    """Every first name and surname in raw.patients and raw.doctors, each once, sorted.

    A full name such as "Ravi D'Souza" gives "Ravi" and "D'Souza".
    Given complete: it is one query, not the point of the task.
    """
    rows = conn.execute("SELECT full_name FROM raw.patients UNION SELECT full_name FROM raw.doctors").fetchall()
    return sorted({word for (full_name,) in rows for word in full_name.split()})


def find_personal(text: str, names: list[str]) -> list[tuple[str, str]]:
    """Return what in `text` looks like personal data, as (kind, value) pairs.

    - "phone" for every match of PHONE;
    - "email" for every "@";
    - "name" for every name in `names` found as a whole word, in any case:
      "GAURI" and "gauri" are both "Gauri". Escape each name (re.escape), because
      a name such as "D'Souza" holds a character that means something in a pattern.

    An empty list means the text is clean. An appointment id such as "A09783001"
    is not a phone number.
    """
    raise NotImplementedError("TODO(task 7): find phone numbers, @ and names")


def mask_text(text: str, names: list[str]) -> str:
    """Return `text` with its personal data replaced, in this order:

    1. every email (EMAIL) by "[EMAIL]";
    2. every phone number (PHONE) by "[PHONE]";
    3. every name in `names`, as a whole word in any case, by "[NAME]".

    Emails go first, so the names inside an email address do not break it apart.
    Everything else stays as it is.
    """
    raise NotImplementedError("TODO(task 7): mask emails, then phone numbers, then names")


def assert_masked(texts: list[str], names: list[str]) -> None:
    """The guard in front of every model call: embed_texts(), ask() and extract_batch().

    Raise ValueError when find_personal() finds anything in any of `texts`.
    The message names the kind and which text, never the value, for example
    "text 3 holds a phone number": an error message can end up in a log or a chat.
    Return None when every text is clean.
    """
    raise NotImplementedError("TODO(task 9): refuse any text that still holds personal data")
