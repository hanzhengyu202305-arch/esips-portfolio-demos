from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentConfig:
    project_root: Path
    reports_dir: Path


def load_config(project_root: Path | None = None) -> AgentConfig:
    root = project_root or Path(__file__).resolve().parents[1]
    return AgentConfig(project_root=root, reports_dir=root / "reports")
