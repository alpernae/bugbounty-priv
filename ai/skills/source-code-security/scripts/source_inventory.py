#!/usr/bin/env python3
import os
from collections import Counter

EXTENSIONS = {
    ".js": "javascript", ".ts": "typescript", ".jsx": "javascript", ".tsx": "typescript",
    ".py": "python", ".java": "java", ".php": "php", ".go": "go",
    ".rb": "ruby", ".cs": "csharp", ".kt": "kotlin", ".rs": "rust",
}

SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", "__pycache__", ".venv", "target"}

def main(root="."):
    counts = Counter()
    examples = {}
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            ext = os.path.splitext(name)[1].lower()
            if ext in EXTENSIONS:
                lang = EXTENSIONS[ext]
                counts[lang] += 1
                examples.setdefault(lang, os.path.join(current, name))
    print("# Source inventory")
    for lang, count in counts.most_common():
        print(f"- {lang}: {count} files; sample={examples.get(lang)}")

if __name__ == "__main__":
    main()
