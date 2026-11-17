# IPL ball-by-ball data

This folder holds one IPL (Indian Premier League) season, one row per ball, for your first SQL queries in the Launchpad. It also holds `get_matches.py`, which downloads every IPL match for Scorebook (P2).

| File | What it is | Size |
|---|---|---|
| `season.csv` | Every ball of the 2026 IPL season: 74 matches, 28 March to 31 May 2026, 17,523 rows | 2,630,140 bytes |
| `season-published.csv` | The same season as a careless website published it. It is wrong on purpose: week 1 asks you to find out why | 2,640,571 bytes |
| `get_matches.py` | Downloads every IPL match from Cricsheet as one JSON file per match (P2) | script |
| `NOTICE.md` | The Cricsheet licence notice for the files in this folder | text |

## Source and licence

Match data from Cricsheet (https://cricsheet.org/), licensed under the Open Data Commons Attribution License 1.0 (https://opendatacommons.org/licenses/by/1-0/).

- `season.csv` and `season-published.csv` were built from Cricsheet's `ipl_csv2.zip` (file `all_matches.csv`), downloaded on 13 November 2026. They are a changed copy: we kept the 2026 season, renamed and dropped columns, and removed 4 super-over balls. `season-published.csv` was changed further, on purpose.
- You may use, share and change the data, as long as you credit Cricsheet. When you publish a result from this data, for example on your GitHub profile, add the line above. `NOTICE.md` explains the licence's conditions.

## The columns of `season.csv`

The file has a header row, commas between values, UTF-8 text and LF line endings. It is sorted by `match_date`, `match_id`, `innings`, `over_no` and `ball_no`.

| Column | Meaning | Example |
|---|---|---|
| `match_id` | Cricsheet's number for the match | `1527674` |
| `match_date` | The day the match started, `YYYY-MM-DD` | `2026-03-28` |
| `venue` | The ground. Every venue name holds a comma, so it is written in double quotes | `"M Chinnaswamy Stadium, Bengaluru"` |
| `innings` | `1` for the team that batted first, `2` for the chase | `1` |
| `over_no` | The over, from 1 to 20 | `1` |
| `ball_no` | The delivery inside the over, counted from 1 (see below) | `4` |
| `batting_team` | The team batting | `Sunrisers Hyderabad` |
| `bowling_team` | The team bowling | `Royal Challengers Bengaluru` |
| `batter` | The batter facing this ball (the striker) | `Abhishek Sharma` |
| `non_striker` | The other batter, at the bowler's end | `TM Head` |
| `bowler` | The bowler | `JA Duffy` |
| `runs_batter` | Runs the batter scored off this ball: 0, 1, 2, 3, 4 or 6 (5 is rare) | `6` |
| `runs_extras` | Extra runs on this ball: wides, no-balls, byes, leg byes and penalties | `0` |
| `runs_total` | All runs on this ball: `runs_total = runs_batter + runs_extras` | `6` |
| `wicket_kind` | How a batter got out on this ball. Empty when nobody got out | `caught` |
| `player_out` | The batter who got out. Empty when nobody got out | `V Kohli` |

Notes:
- **`ball_no` can be more than 6.** A wide or a no-ball does not count as one of the over's six legal balls, so the bowler bowls again. Cricsheet counts every delivery, so an over with two wides has `ball_no` 1 to 8. In 2026, 845 rows have `ball_no` above 6, and the highest is 11.
- **`(match_id, innings, over_no, ball_no)` is unique** in `season.csv`: no two rows share it. Remember this in week 1.
- **`wicket_kind` values in 2026**: `caught` (655), `bowled` (114), `run out` (41), `lbw` (30), `caught and bowled` (22), `stumped` (12), `hit wicket` (2), `retired hurt` (2), `retired out` (1) and `obstructing the field` (1). A `retired hurt` batter is not out in the scorebook, but Cricsheet still names them in `player_out`.
- **Names are written as Cricsheet writes them**: often initials and a surname (`V Kohli`, `JC Buttler`), sometimes a full name (`Shubman Gill`). To find how a name is spelled, use `WHERE batter LIKE '%Kohli%'`.
- Super overs (the tie-breaker after a tied match) are left out: only innings 1 and 2 are in the file.

Numbers for checking your own results: 10 teams, 13 venues, 1,426 sixes, 27,450 runs in total (`SUM(runs_total)`).

## Open the file in the DuckDB web shell

The DuckDB web shell runs SQL inside your browser. Nothing is installed, and your file never leaves your computer.

1. Download `season.csv` from this folder on GitHub: open the file, then select the **Download raw file** button.
2. Open https://shell.duckdb.org/ in Chrome or Edge.
3. Select **Import**, choose `season.csv`, and wait for the line `Registered: season.csv`. Dragging the file onto an empty prompt also works.
4. Make a table from the file:

   ```sql
   CREATE TABLE balls AS SELECT * FROM 'season.csv';
   DESCRIBE balls;
   SELECT * FROM balls LIMIT 5;
   ```

5. `DESCRIBE balls;` lists the 16 columns above. DuckDB reads `match_date` as a `DATE` and the number columns as `BIGINT`.

The shell forgets tables when you reload the page. If that happens, import the file again and run the `CREATE TABLE` line again.

## `season-published.csv`

It has the same 16 columns, the same header and the same sort order as `season.csv`. A careless website published it from the same season, and one of its numbers is wrong. Week 1 asks you to find which number, and why. Never treat it as a correct copy of the season.

## `get_matches.py` (Scorebook, P2)

It downloads Cricsheet's `ipl_json.zip` (about 5 MB) and saves one JSON file per match into one folder. It uses only the Python standard library. Run it inside your `scorebook/` folder in Git Bash:

```bash
uv run python ~/de-kit/data/ipl/get_matches.py --out data/matches
```

It prints how many match files it saved, for example `Saved 1243 match files to data/matches`. It also saves Cricsheet's `README.txt` (the list of matches) and `LICENSE.txt` into the same folder. Add `--league wpl` to download the Women's Premier League instead. Run `uv run python ~/de-kit/data/ipl/get_matches.py --help` to see every option.

The JSON format is described on Cricsheet's page https://cricsheet.org/format/json/. The data is under the same licence: credit Cricsheet in your project's README.

## Do not commit the data

Keep downloaded match files and copies of these CSV files out of Git. Your course repository ignores `data/` folders; commit your queries and results instead.
