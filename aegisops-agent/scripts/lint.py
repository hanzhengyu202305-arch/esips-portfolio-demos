from __future__ import annotations

import compileall
import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ok = True
    for path in [ROOT / "agent", ROOT / "apps" / "demo-api" / "app", ROOT / "scripts"]:
        ok = compileall.compile_dir(str(path), quiet=1) and ok

    if importlib.util.find_spec("ruff") is not None:
        completed = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "agent", "apps/demo-api/app", "scripts"],
            cwd=ROOT,
            text=True,
            check=False,
        )
        ok = completed.returncode == 0 and ok
    else:
        print("ruff not installed; compile lint passed")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
