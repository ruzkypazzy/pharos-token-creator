#!/bin/bash
# pharos-token-creator — Foundry-port smoke test
# Tests the deploy.py CLI (the only Python script — used for forge command rendering)
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "Test 1: deploy.py --help"
python3 "$SKILL_DIR/scripts/deploy.py" --help 2>&1 | grep -q "Usage" && echo "  OK"

echo "Test 2: deploy.py render --template standard"
python3 "$SKILL_DIR/scripts/deploy.py" render --template standard --name "Test" --symbol TSK --supply 1000000 --chain mainnet 2>&1 | grep -q "FOUNDRY_PRIVATE_KEY" && echo "  OK: env-var prefix used"

echo "All smoke tests passed."
