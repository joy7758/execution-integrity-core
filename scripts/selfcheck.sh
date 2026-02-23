#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

cd "${REPO_DIR}"
python3 example.py
python3 verify_export.py execution_log.json
python3 tests/test_export_verify.py
echo "SELF_CHECK: PASS"
