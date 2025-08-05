#!/usr/bin/env bash

sleep 15
if [ "$RUN_PRESTANT" == "1" ];then
  set -e
  sleep 15
  echo "Run apply migrations.."
  alembic upgrade head
  echo "Migrations applied!"
fi
sleep 45
exec "$@"
