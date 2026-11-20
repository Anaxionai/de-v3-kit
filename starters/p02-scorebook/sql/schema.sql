-- Scorebook schema: the four tables. Task 7.
-- Run it from scorebook/ with: bash psql.sh < sql/schema.sql
-- It can run again at any time: it drops and recreates the four tables.
DROP TABLE IF EXISTS deliveries, innings, matches, players CASCADE;

-- One row is one person who was in a team for at least one match.
-- players is written out as a worked example. Write the other three the same way.
CREATE TABLE players (
    player_id TEXT PRIMARY KEY,   -- the id in info.registry.people: names are not unique
    name      TEXT NOT NULL
);

-- TODO(task 7): for matches, innings and deliveries, give every column a type, NOT NULL
-- where the JSON always has a value, a primary key, and a line "One row is one ..." above
-- the table. Until then each table below is created with no columns.

CREATE TABLE matches (
    -- match_id, season, match_date, city, venue, team1, team2, toss_winner, toss_decision,
    -- winner, result, win_by_runs, win_by_wickets, player_of_match_id
);

CREATE TABLE innings (
    -- match_id, innings_no, batting_team, bowling_team, is_super_over, target_runs
    -- TODO(task 7): a foreign key from innings to matches
);

CREATE TABLE deliveries (
    -- match_id, innings_no, over_no, ball_no, batter_id, bowler_id, non_striker_id,
    -- runs_batter, runs_extras, runs_total, extra_type, wicket_kind, player_out_id
    -- TODO(task 7): foreign keys to innings (both key columns) and to players, and
    -- CHECK (runs_total = runs_batter + runs_extras)
);
