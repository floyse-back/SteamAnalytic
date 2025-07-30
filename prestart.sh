#!/usr/bin/env bash

if [ "$RUN_PRESTANT" == "1" ];then
  set -e

  echo "Run apply migrations.."
  alembic upgrade head
  echo "Migrations applied!"
fi
  sleep 15

exec "$@"
