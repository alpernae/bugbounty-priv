#!/usr/bin/env python3
from pathlib import Path
import sys

required = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/index.md",
    "references/coverage-matrix.md",
    "references/false-positive-reduction.md",
    "references/workflows/scope-and-authorization.md",
    "assets/report-template.md",
    "scripts/new_finding.py",
    "scripts/api_key_exposure_triage.py",
]

base = Path(__file__).resolve().parents[1]
missing = [p for p in required if not (base / p).exists()]
if missing:
    print("Missing files:")
    for p in missing:
        print(f" - {p}")
    sys.exit(1)
print("Skill structure OK")
