from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_doctor(reports_dir: Path | str = Path("reports")) -> Path:
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)
    payload = {
        "project": "aegisops-agent",
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "checks": {
            "project_root": {
                "ok": (PROJECT_ROOT / "Makefile").exists() and (PROJECT_ROOT / "agent").exists(),
                "detail": str(PROJECT_ROOT),
            },
            "pytest": _python_module_check("pytest"),
            "fastapi": _python_module_check("fastapi"),
            "docker": _binary_check("docker", required=False),
            "kind": _binary_check("kind", required=False),
            "kubectl": _binary_check("kubectl", required=False),
        },
    }
    path = reports_path / "doctor.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def render_doctor_markdown(doctor_json_path: Path, output_path: Path | None = None) -> Path:
    payload = json.loads(doctor_json_path.read_text(encoding="utf-8"))
    output = output_path or doctor_json_path.with_suffix(".md")
    lines = [
        "# AegisOps Environment Doctor",
        "",
        f"- project: `{payload['project']}`",
        f"- python_version: `{payload['python_version']}`",
        f"- platform: `{payload['platform']}`",
        "",
        "| check | ok | detail |",
        "| --- | ---: | --- |",
    ]
    for name, check in payload["checks"].items():
        lines.append(f"| {name} | {str(check['ok']).lower()} | {check['detail']} |")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def _python_module_check(module_name: str) -> dict:
    try:
        __import__(module_name)
    except Exception as exc:
        return {"ok": False, "detail": f"not importable: {exc}"}
    return {"ok": True, "detail": "importable"}


def _binary_check(binary_name: str, required: bool) -> dict:
    path = shutil.which(binary_name)
    if path:
        return {"ok": True, "detail": path}
    detail = "missing; optional dry-run fallback is available"
    if required:
        detail = "missing; required for this command"
    return {"ok": False, "detail": detail}
