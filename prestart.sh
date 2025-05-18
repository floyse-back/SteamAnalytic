#!/usr/bin/env bash

if [ "$RUN_PRESTANT" == "1" ];then
  set -e

  sleep 5
  echo "Run apply migrations.."
  alembic upgrade head
  echo "Migrations applied!"
fi

exec "$@"
