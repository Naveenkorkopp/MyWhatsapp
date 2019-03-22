#!/bin/bash
set -e
cmd="$@"

echo "DB HOST: " $DJANGO_DB_HOST
echo "DB USER: " $DJANGO_DB_USER

if [ "$DJANGO_DB_HOST" ] && [ "$DJANGO_DB_USER" ] && [ "$DJANGO_DB_PASSWORD" ]; then
  export DATABASE_URL=postgres://$DJANGO_DB_USER:$DJANGO_DB_PASSWORD@$DJANGO_DB_HOST:$DJANGO_DB_PORT/$DJANGO_DB_NAME
else
  export DATABASE_URL=postgres://chat_box:chat_box@postgres:5432/chat_box
fi

echo "DATABASE_URL ==> $DATABASE_URL"

function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect("$DATABASE_URL")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
 >&2 echo "Postgres is unavailable - sleeping"
 sleep 1
done

>&2 echo "Postgres is up - continuing..."

# -z tests for empty, if TRUE, $cmd is empty, run migrate only when using postgres DB locally
if [ -z $cmd ]; then
  >&2 echo "Running default command (collectstatic + gunicorn)"
    python /app/manage.py collectstatic --noinput
  if [ "$DJANGO_DB_HOST" == "postgres" ] || [ -z "$DJANGO_DB_HOST" ]; then
    >&2 echo "Running default command (migrate)"
    python /app/manage.py migrate --noinput
  else
    >&2 echo "No migration required connecting to $DJANGO_DB_HOST"
  fi
  python /app/manage.py runserver 0:8000
else
  >&2 echo "Running command passed (by the compose file)"
  exec $cmd
fi
