{{ config(enabled=false) }}
-- int_github__repository_names: each repository's latest name up to a point in time; the snapshot
-- in snapshots/repository_names.yml reads it.
--
-- TODO(task 25): delete the config line at the top when you write this model. Until then dbt skips
--   this file, so the dbt build in task 23 does not try to build an empty model.
-- TODO(task 25): from stg_github__events (with ref()), only events with created_at up to
--   var('as_of', '9999-12-31'). One row per repo_id: the repo_name of its latest event, and
--   name_first_seen_at, the earliest created_at among its events with that name.
