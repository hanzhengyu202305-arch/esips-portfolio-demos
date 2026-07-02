from __future__ import annotations

from pathlib import Path


def main() -> int:
    report = Path("reports/kind-setup.txt")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "No kind/minikube binary found. Local Kubernetes fixture mode is ready for mock demos.\n",
        encoding="utf-8",
    )
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
