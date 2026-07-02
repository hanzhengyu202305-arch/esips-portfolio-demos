from __future__ import annotations

from pathlib import Path

from agent.graph.nodes import run_agent_flow
from agent.schemas import AgentRunResult


def run_multi_agent(
    scenario_id: str,
    reports_dir: Path | str = Path("reports"),
) -> AgentRunResult:
    return run_agent_flow(scenario_id, mode="multi", reports_dir=reports_dir)
