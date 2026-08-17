#!/bin/sh
set -e
case "${DATABASE_URL:-}" in
  postgresql*|postgres*)
    alembic upgrade head
    ;;
esac
exec "$@"
