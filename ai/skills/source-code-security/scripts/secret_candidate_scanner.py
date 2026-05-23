#!/usr/bin/env python3
import os
import re
from pathlib import Path

PATTERNS = {
    "generic_api_key": re.compile(r"(?i)(api[_-]?key|secret|token)['\"\s:=]+([a-z0-9_\-]{20,})"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "stripe_secret": re.compile(r"sk_(test|live)_[A-Za-z0-9]{16,}"),
}

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "__pycache__", ".venv", "target"}

def main(root="."):
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = Path(current) / name
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue
            for label, pattern in PATTERNS.items():
                for match in pattern.finditer(text):
                    start = max(0, match.start() - 20)
                    end = min(len(text), match.end() + 20)
                    snippet = text[start:end].replace("\n", " ")
                    print(f"{label}: {path}: {snippet[:12]}...[redacted]...")

if __name__ == "__main__":
    main()
