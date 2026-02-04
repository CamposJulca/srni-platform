#!/bin/sh
set -e

if [ -n "$DB_HOST" ]; then
  echo "Ã¢ÂÂ³ Waiting for PostgreSQL..."
  until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
    sleep 2
  done
  echo "Ã¢Å“â€¦ PostgreSQL is ready"
else
  echo "Ã¢â€žÂ¹Ã¯Â¸Â  No DB_HOST set Ã¢â€ â€™ using SQLite (DEV mode)"
fi

echo "Ã°Å¸â€œÂ¦ Applying migrations..."
python manage.py migrate --noinput

echo "Ã°Å¸Å¡â‚¬ Starting Django"
exec "$@"
