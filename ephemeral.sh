#!/usr/bin/env bash

set -euo pipefail

BIND="${1:-0.0.0.0:8080}"

num_cores=$(nproc)
num_workers=$((2 * num_cores + 1))

exec gunicorn --bind="$BIND" --workers="$num_workers" ephemeral.wsgi
