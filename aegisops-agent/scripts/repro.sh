#!/usr/bin/env bash
set -euo pipefail

RUNS="${RUNS:-3}"
python -m agent.main poc-repro --runs "${RUNS}"
