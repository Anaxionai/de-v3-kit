# Runs psql on the scorebook database in the data lab. Use it from scorebook/, for example: bash psql.sh < sql/schema.sql
docker compose -f ~/de-kit/datalab/docker-compose.yml exec -T postgres psql -U de -d scorebook "$@"
