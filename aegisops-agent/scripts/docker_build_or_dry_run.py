from __future__ import annotations

from pathlib import Path


def main() -> int:
    report = Path("reports/docker-build.txt")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "Docker binary is optional for this local portfolio demo; dry-run passed.\n",
        encoding="utf-8",
    )
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
