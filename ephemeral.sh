#!/usr/bin/env bash

set -euo pipefail

gunicorn --bind=0.0.0.0:3000 --workers=2 ephemeral.wsgi