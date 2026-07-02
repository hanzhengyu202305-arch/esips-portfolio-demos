from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


Mode = Literal["single", "multi"]


@dataclass(frozen=True)
class IncidentCase:
    scenario_id: str
    repo_path: str
    mode: Mode
    evidence_paths: list[str]
    allowed_files: list[str]
    blocked_files: list[str]
    validation_commands: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class Diagnosis:
    scenario_id: str
    root_cause_id: str
    confidence: float
    evidence_refs: list[str]
    retrieved_context_refs: list[str]
    impact: str
    fix_plan: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class PatchResult:
    scenario_id: str
    files_changed: list[str]
    diff_path: str
    patch_applied: bool
    validation_passed: bool
    commands_run: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class EvalResult:
    scenario_id: str
    mode: Mode
    root_cause_correct: bool
    fix_successful: bool
    latency_seconds: float
    prompt_tokens: int
    completion_tokens: int
    estimated_cost_usd: float
    tool_calls: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class AgentRunResult:
    diagnosis: Diagnosis
    patch: PatchResult
    metrics: EvalResult
    run_dir: str

    def to_dict(self) -> dict:
        return {
            "diagnosis": self.diagnosis.to_dict(),
            "patch": self.patch.to_dict(),
            "metrics": self.metrics.to_dict(),
            "run_dir": self.run_dir,
        }
