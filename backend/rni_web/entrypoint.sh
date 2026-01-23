#!/bin/sh
set -e

echo "⏳ Waiting for PostgreSQL..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 2
done

echo "✅ PostgreSQL is ready"

echo "📦 Applying migrations..."
python manage.py migrate --noinput

echo "🚀 Starting Django"
exec "$@"
