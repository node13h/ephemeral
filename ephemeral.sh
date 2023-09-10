#!/usr/bin/env sh

# Copyright (C) 2019-2023 Sergej Alikov <sergej.alikov@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

set -eu

BIND="${1:-0.0.0.0:8080}"

num_cores=$(nproc)
num_workers=$((2 * num_cores + 1))

exec gunicorn --bind="$BIND" --workers="$num_workers" ephemeral.wsgi
