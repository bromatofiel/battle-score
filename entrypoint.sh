#!/bin/bash
set -ex

echo "sleep for 3 seconds for PGSQL init"
sleep 3

exec "$@"
