#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$POSTGRES_USER" -c '\q' &> /dev/null; do
  >&2 echo "Postgres está indisponível - aguardando..."
  sleep 2
done

>&2 echo "Postgres está pronto - executando comando"
exec $cmd
