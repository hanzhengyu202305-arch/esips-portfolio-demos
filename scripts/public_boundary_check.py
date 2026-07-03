from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
    ".venv",
    "venv",
}

SKIP_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
}

ALLOWLIST_FILES = {
    ".gitignore",
    "scripts/public_boundary_check.py",
}

SAFE_CONTEXT_MARKERS = (
    "boundary",
    "do not add",
    "do not include",
    "does not include",
    "must not include",
    "needs official confirmation",
    "no private",
    "no secrets",
    "not belong",
    "not include",
    "not included",
    "private data",
    "public repository",
    "avoid saying",
    "examples only",
    "human review",
    "no real secrets",
    "real secrets",
    "secrets remain absent",
    "absent from examples",
)

RISK_PATTERNS = {
    "WAM": re.compile(r"\bWAM\b", re.IGNORECASE),
    "transcript": re.compile(r"\btranscript\b", re.IGNORECASE),
    "SONIA": re.compile(r"\bSONIA\b"),
    "Canvas": re.compile(r"\bCanvas\b"),
    "password": re.compile(r"\bpassword\b", re.IGNORECASE),
    "API key": re.compile(r"\b(API[_ -]?key|OPENAI_API_KEY|sk-[A-Za-z0-9_-]{12,})\b", re.IGNORECASE),
    "secret": re.compile(r"\bsecret(s)?\b|BEGIN [A-Z ]*PRIVATE KEY", re.IGNORECASE),
    "token": re.compile(r"\b(access[_ -]?token|refresh[_ -]?token|bearer\s+[A-Za-z0-9._-]+)\b", re.IGNORECASE),
    "mailbox": re.compile(r"\bmailbox\b", re.IGNORECASE),
    "email content": re.compile(r"\bemail content\b", re.IGNORECASE),
    "CV": re.compile(r"\bCV\b"),
    "resume private draft": re.compile(r"\bresume private draft\b", re.IGNORECASE),
    "/Users path": re.compile(r"/Users/"),
    ".env": re.compile(r"(^|/)\.env($|[.\s:/])|`\.env`"),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check that the public repo does not contain private application material.")
    parser.add_argument("--root", default=str(ROOT), help="Repository root to scan.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = scan(root)
    if findings:
        print("FAIL public boundary check")
        for path, line_no, label, line in findings:
            print(f"- {path}:{line_no}: matched {label}: {line}")
        return 1

    print("PASS public boundary check")
    return 0


def scan(root: Path) -> list[tuple[str, int, str, str]]:
    findings: list[tuple[str, int, str, str]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or _should_skip(path, root):
            continue
        rel_path = path.relative_to(root).as_posix()
        if rel_path in ALLOWLIST_FILES:
            continue
        text = _read_text(path)
        if text is None:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if _safe_boundary_line(line):
                continue
            for label, pattern in RISK_PATTERNS.items():
                if pattern.search(line):
                    findings.append((rel_path, line_no, label, line.strip()))
    return findings


def _should_skip(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    if any(part in SKIP_DIRS for part in rel_parts):
        return True
    return path.suffix.lower() in SKIP_SUFFIXES


def _read_text(path: Path) -> str | None:
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            return None


def _safe_boundary_line(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in SAFE_CONTEXT_MARKERS)


if __name__ == "__main__":
    sys.exit(main())
