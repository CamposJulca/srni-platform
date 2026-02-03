#!/bin/sh
set -e

if [ -n "$DB_HOST" ]; then
  echo "⏳ Waiting for PostgreSQL..."
  until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
    sleep 2
  done
  echo "✅ PostgreSQL is ready"
else
  echo "ℹ️  No DB_HOST set → using SQLite (DEV mode)"
fi

echo "📦 Applying migrations..."
python manage.py migrate --noinput

echo "🚀 Starting Django"
exec "$@"
