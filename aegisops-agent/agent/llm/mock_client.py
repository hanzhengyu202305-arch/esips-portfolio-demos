from __future__ import annotations

from typing import Any

from agent.diagnosis_engine import infer_root_cause
from agent.schemas import Diagnosis


class MockLLM:
    """Deterministic stand-in for the original portfolio demo LLM."""

    def diagnose(
        self,
        scenario: Any,
        evidence: dict[str, Any],
        contexts: list[dict[str, Any]],
        mode: str,
    ) -> Diagnosis:
        decision = infer_root_cause(evidence, contexts, mode)
        evidence_refs = [
            str(signal.get("id"))
            for signal in evidence.get("signals", [])
            if signal.get("id")
        ]
        context_refs = [
            str(context.get("id") or context.get("path") or context.get("title"))
            for context in contexts
        ]
        return Diagnosis(
            scenario_id=scenario.scenario_id,
            root_cause_id=decision.root_cause_id,
            confidence=decision.confidence,
            decision=decision.decision,
            decision_reason=decision.reason,
            ranked_hypotheses=[item.to_dict() for item in decision.hypotheses],
            evidence_refs=evidence_refs,
            retrieved_context_refs=context_refs,
            impact=scenario.failure_summary,
            fix_plan=(
                [f"Patch {path} using the scenario allowlist." for path in scenario.fixed_files]
                if decision.decision == "PROPOSE_PATCH"
                else ["Stop automated remediation and request human evidence review."]
            ),
        )

    def estimate_tokens(self, scenario: Any, mode: str) -> tuple[int, int]:
        prompt_tokens = 520 + len(scenario.raw_log.split()) * 2
        completion_tokens = 180 + len(scenario.fixed_files) * 40
        if mode == "multi":
            prompt_tokens += 260
            completion_tokens += 120
        return prompt_tokens, completion_tokens
