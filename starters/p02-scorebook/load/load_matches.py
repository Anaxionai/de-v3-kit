"""Load every Cricsheet IPL match file into the scorebook database.

Task 8. Run it from scorebook/:

    uv run python load/load_matches.py data/matches

Task 24's reload_match.py imports this file, so main() runs only under
if __name__ == "__main__": at the end. Keep it that way.
"""

import os
import sys
import time
from pathlib import Path

import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://de:de@localhost:5432/scorebook")

# The deliveries columns, in the order delivery_rows() returns them and COPY reads them.
DELIVERY_COLUMNS = (
    "match_id, innings_no, over_no, ball_no, batter_id, bowler_id, non_striker_id, "
    "runs_batter, runs_extras, runs_total, extra_type, wicket_kind, player_out_id"
)


def read_match(path: Path) -> dict:
    """Return the parsed JSON of one match file. Read the text as UTF-8."""
    raise NotImplementedError("TODO(task 8): write read_match(path)")


def player_rows(info: dict) -> dict[str, str]:
    """Return a dictionary from player id to name, for every name in the team lists of
    info["players"]. Find each name's id in info["registry"]["people"]: names are not
    unique, ids are."""
    raise NotImplementedError("TODO(task 8): write player_rows(info)")


def match_row(match_id: int, info: dict) -> tuple:
    """Return one row for matches, in the column order of your sql/schema.sql.

    - season: str(info["season"]), because some files store the season as a number.
    - match_date: the first date in info["dates"].
    - city, winner and player_of_match can be missing: use .get(), which gives None.
    - result: "win", "tie" or "no result", from info["outcome"]. For a tie, store the team
      in outcome["eliminator"] as winner: it won the super over.
    - player_of_match_id: the id, not the name, of the first award winner, or None.
    """
    raise NotImplementedError("TODO(task 8): write match_row(match_id, info)")


def innings_rows(match_id: int, match: dict) -> list[tuple]:
    """Return one row per innings of the match: match_id, innings_no (1, 2, then 3 and up
    for super overs), batting_team, bowling_team, is_super_over (from
    innings.get("super_over", False)) and target_runs (from "target", or None)."""
    raise NotImplementedError("TODO(task 8): write innings_rows(match_id, match)")


def delivery_rows(match_id: int, match: dict) -> list[tuple]:
    """Return one row per ball bowled, in the order of DELIVERY_COLUMNS.

    - over_no is the JSON "over" plus 1, so the first over is 1.
    - ball_no counts the balls of the over from 1 with enumerate: every ball, wides and
      no-balls included.
    - batter_id, bowler_id, non_striker_id and player_out_id are ids, not names.
    - extra_type: "wides" or "noballs" if present, else the first key of "extras", else None.
    - wicket_kind and player_out_id come from the first item of "wickets", else None.
    """
    raise NotImplementedError("TODO(task 8): write delivery_rows(match_id, match)")


def main(folder: Path) -> None:
    """Load every .json file in folder into the four tables. Safe to run again."""
    started = time.perf_counter()
    paths = sorted(folder.glob("*.json"))
    with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
        # TODO(task 8): collect the players of all the files with player_rows, TRUNCATE the
        # four tables, insert the players, then for each file insert its match, its innings,
        # and its deliveries with cur.copy(f"COPY deliveries ({DELIVERY_COLUMNS}) FROM STDIN").
        raise NotImplementedError("TODO(task 8): load the files, then delete this line")
        # Given: the row counts and the time. They run once your load replaces the line above.
        for table in ("players", "matches", "innings", "deliveries"):
            count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {count} rows")
    print(f"Loaded {len(paths)} files in {time.perf_counter() - started:.1f} seconds")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
