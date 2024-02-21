#!/usr/bin/bash

set -e
set -u

cd "$(dirname "$0")"

python3.8 -m piptools compile "pyproject.toml" --extra "dev"
