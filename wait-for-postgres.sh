#!/bin/sh
# wait-for-postgres.sh: Espera a que PostgreSQL esté listo

set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -p 5432; do
  echo "Waiting for postgres at $host..."
  sleep 2
done

exec $cmd
