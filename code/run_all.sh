#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
cd "$HERE"
python verify_isalhg_all_k.py
python stress_isalhg.py
python audit_specification_defects.py
python - <<'PY2'
import json
from pathlib import Path
root=Path('..').resolve()
for name in (
    'isalhg_exhaustive_all_k.json',
    'isalhg_random_stress.json',
    'isalhg_specification_audit.json',
):
    path = root/'results'/name
    assert path.exists(), path
    d=json.loads(path.read_text())
    if 'failure_count' in d:
        assert d['failure_count']==0, (name,d['failure_count'])
assert (root/'results'/'isalhg_specification_audit.json').stat().st_size > 0
print('All automated checks passed.')
PY2
