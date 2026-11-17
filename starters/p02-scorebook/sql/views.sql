-- Scorebook views: the season leaderboards. Task 23.
-- Run it after schema.sql and the load, twice, with: bash psql.sh < sql/views.sql
-- Running schema.sql again drops these views (CASCADE): run this file again after a reset.

-- TODO(task 23): drop the materialised view season_batting_mv, then the views
-- season_bowling, season_batting and regular_balls, so the file can run again.

-- regular_balls: every column of deliveries plus season, batting_team and bowling_team,
-- for innings that are not super overs.
-- TODO(task 23): create the view regular_balls.

-- season_batting: per season and player, runs, matches (COUNT(DISTINCT match_id)) and
-- position (RANK() by runs within the season), read from regular_balls.
-- TODO(task 23): create the view season_batting.

-- season_bowling: per season and player, the wickets a bowler earns (as in your q02) and
-- position, read from regular_balls.
-- TODO(task 23): create the view season_bowling.

-- season_batting_mv: a materialised view of SELECT * FROM season_batting.
-- TODO(task 23): create the materialised view season_batting_mv.
