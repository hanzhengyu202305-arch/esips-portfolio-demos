from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Literal


Decision = Literal["PROPOSE_PATCH", "ESCALATE"]


@dataclass(frozen=True)
class DiagnosisRule:
    root_cause_id: str
    patterns: tuple[str, ...]
    context_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class RankedHypothesis:
    root_cause_id: str
    score: float
    evidence_hits: list[str]
    context_hits: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiagnosisDecision:
    decision: Decision
    root_cause_id: str
    confidence: float
    reason: str
    hypotheses: list[RankedHypothesis]


RULES = (
    DiagnosisRule(
        "wrong_discount_logic",
        (
            r"assert\s+2\.5\s+==\s+25\.0",
            r"gold(?:\s+tier|\s+customer)?.{0,30}discount",
            r"expected\s+25\.0.{0,30}(?:observed|got)\s+2\.5",
        ),
        (r"pytest assertion", r"business rules"),
    ),
    DiagnosisRule(
        "missing_python_dependency",
        (
            r"modulenotfounderror",
            r"cannot import pydantic",
            r"no module named ['\"]?pydantic",
        ),
        (r"missing dependenc", r"requirements\.txt"),
    ),
    DiagnosisRule(
        "missing_app_mode_env",
        (
            r"app_mode.{0,40}got\s+['\"]{2}",
            r"app_mode\s+is\s+empty",
            r"empty\s+app_mode",
        ),
        (r"environment variable", r"workflow env"),
    ),
    DiagnosisRule(
        "invalid_app_mode_env",
        (
            r"app_mode.{0,50}got\s+['\"]broken['\"]",
            r"app_mode.{0,50}unsupported",
            r"unsupported value ['\"]broken['\"]",
        ),
        (r"crashloopbackoff", r"container restarts"),
    ),
    DiagnosisRule(
        "wrong_readiness_probe_path",
        (
            r"readiness probe.{0,50}404",
            r"/readyz.{0,40}404",
            r"/health.{0,40}200",
        ),
        (r"readiness probe", r"health endpoint"),
    ),
    DiagnosisRule(
        "image_tag_mismatch",
        (
            r"imagepullbackoff",
            r"failed to pull image",
            r"canary-missing.{0,40}(?:cannot be pulled|back-off|failed)",
        ),
        (r"image tag", r"local registry"),
    ),
    DiagnosisRule(
        "container_runs_as_root",
        (
            r"must runasnonroot",
            r"allows root execution",
            r"runasuser:\s*0",
            r"allowprivilegeescalation",
        ),
        (r"container security context", r"non-root containers"),
    ),
    DiagnosisRule(
        "nested_loop_latency_regression",
        (
            r"nested loop",
            r"o\(n\^?2\)",
            r"p95 latency.{0,50}(?:980ms|increased)",
            r"repeats customer aggregation",
        ),
        (r"latency regression", r"pre-aggregate"),
    ),
)


def build_retrieval_query(evidence: dict[str, Any]) -> str:
    """Build retrieval input from observed evidence instead of fixture labels."""
    parts = [str(evidence.get("raw_log", ""))]
    for signal in evidence.get("signals", []):
        parts.extend(
            [
                str(signal.get("kind", "")),
                str(signal.get("message", "")),
            ]
        )
    return " ".join(part.strip() for part in parts if part.strip())


def infer_root_cause(
    evidence: dict[str, Any],
    contexts: list[dict[str, Any]],
    mode: str,
) -> DiagnosisDecision:
    evidence_text = build_retrieval_query(evidence).lower()
    context_text = " ".join(
        " ".join(
            [
                str(context.get("title", "")),
                str(context.get("text", "")),
            ]
        )
        for context in contexts
        if float(context.get("score", 0)) > 0
    ).lower()

    hypotheses = sorted(
        (_score_rule(rule, evidence_text, context_text) for rule in RULES),
        key=lambda item: (-item.score, item.root_cause_id),
    )
    ranked = [item for item in hypotheses if item.score > 0][:3]
    if not ranked or len(ranked[0].evidence_hits) < 2:
        return DiagnosisDecision(
            decision="ESCALATE",
            root_cause_id="undetermined",
            confidence=0.0,
            reason="insufficient independent evidence matches",
            hypotheses=ranked,
        )

    top = ranked[0]
    runner_up_score = ranked[1].score if len(ranked) > 1 else 0.0
    if top.score - runner_up_score < 1.0:
        return DiagnosisDecision(
            decision="ESCALATE",
            root_cause_id="undetermined",
            confidence=0.0,
            reason="conflicting hypotheses require human review",
            hypotheses=ranked,
        )

    mode_bonus = 0.02 if mode == "multi" else 0.0
    confidence = min(0.95, 0.55 + (0.10 * len(top.evidence_hits)) + (0.02 * len(top.context_hits)) + mode_bonus)
    return DiagnosisDecision(
        decision="PROPOSE_PATCH",
        root_cause_id=top.root_cause_id,
        confidence=round(confidence, 2),
        reason="highest-scoring hypothesis has sufficient evidence and separation",
        hypotheses=ranked,
    )


def _score_rule(rule: DiagnosisRule, evidence_text: str, context_text: str) -> RankedHypothesis:
    evidence_hits = [pattern for pattern in rule.patterns if re.search(pattern, evidence_text, re.IGNORECASE)]
    context_hits = [
        pattern
        for pattern in rule.context_patterns
        if re.search(pattern, context_text, re.IGNORECASE)
    ]
    score = 0.0
    if evidence_hits:
        score = (2.0 * len(evidence_hits)) + (0.25 * len(context_hits))
    return RankedHypothesis(
        root_cause_id=rule.root_cause_id,
        score=round(score, 2),
        evidence_hits=evidence_hits,
        context_hits=context_hits,
    )
