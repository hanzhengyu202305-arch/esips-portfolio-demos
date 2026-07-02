from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.scenarios import get_scenario  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--patched-dir", default="reports/patched")
    args = parser.parse_args()

    scenario = get_scenario(args.scenario)
    patched_dir = Path(args.patched_dir)
    texts = []
    for relative_path, fallback in scenario.fixed_files.items():
        patched_path = patched_dir / relative_path
        texts.append(patched_path.read_text(encoding="utf-8") if patched_path.exists() else fallback)
    merged = "\n".join(texts)

    if scenario.scenario_id == "S2":
        return _assert("pydantic" in merged, "docker dry-run requires pydantic dependency")
    if scenario.scenario_id in {"S4", "S3"}:
        return _assert("value: demo" in merged or 'APP_MODE: "demo"' in merged, "APP_MODE must be demo")
    if scenario.scenario_id == "S5":
        return _assert("path: /health" in merged, "readiness probe must use /health")
    if scenario.scenario_id == "S6":
        return _assert("tag: local" in merged, "image tag must use local")
    if scenario.scenario_id == "S7":
        return _assert(
            "runAsNonRoot: true" in merged and "allowPrivilegeEscalation: false" in merged,
            "securityContext must enforce non-root execution",
        )
    if scenario.scenario_id == "S8":
        return _assert("totals_by_customer" in merged, "latency fix should avoid nested loop")

    print(f"{scenario.scenario_id} {scenario.validation_kind} passed")
    return 0


def _assert(condition: bool, message: str) -> int:
    if condition:
        print(f"passed: {message}")
        return 0
    print(f"failed: {message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
