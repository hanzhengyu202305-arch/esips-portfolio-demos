from __future__ import annotations

import json
from pathlib import Path
from typing import Any


POLICY_RULES: tuple[dict[str, str], ...] = (
    {
        "id": "KC001_IMAGE_TAG_PINNED",
        "title": "Image tag is pinned",
        "severity": "blocking",
        "category": "reproducibility",
        "validator_finding": "image tag must not be latest",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC002_CPU_REQUEST",
        "title": "CPU request is set",
        "severity": "warning",
        "category": "scheduler reliability",
        "validator_finding": "cpu request is required",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC003_MEMORY_REQUEST",
        "title": "Memory request is set",
        "severity": "warning",
        "category": "scheduler reliability",
        "validator_finding": "memory request is required",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC004_CPU_LIMIT",
        "title": "CPU limit is set",
        "severity": "warning",
        "category": "blast-radius control",
        "validator_finding": "cpu limit is required",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC005_MEMORY_LIMIT",
        "title": "Memory limit is set",
        "severity": "warning",
        "category": "OOM risk control",
        "validator_finding": "memory limit is required",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC006_PROBES_PRESENT",
        "title": "Readiness and liveness probes are present",
        "severity": "warning",
        "category": "rollout safety",
        "validator_finding": "readiness probe is required; liveness probe is required",
        "fixture_evidence": "fixtures/safe passes; fixtures/partial fails liveness",
    },
    {
        "id": "KC007_RUN_AS_NON_ROOT",
        "title": "Pod runs as non-root",
        "severity": "blocking",
        "category": "container security",
        "validator_finding": "runAsNonRoot must be true",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC008_NO_PRIVILEGED_CONTAINER",
        "title": "Privileged containers are rejected",
        "severity": "blocking",
        "category": "privilege boundary",
        "validator_finding": "privileged containers are not allowed",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC009_NO_PRIVILEGE_ESCALATION",
        "title": "Privilege escalation is disabled",
        "severity": "blocking",
        "category": "least privilege",
        "validator_finding": "privilege escalation must be disabled",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC010_RESOURCE_REQUESTS",
        "title": "Resource requests block exists",
        "severity": "warning",
        "category": "scheduler reliability",
        "validator_finding": "resource requests are required",
        "fixture_evidence": "fixtures/safe passes; fixtures/risky fails",
    },
    {
        "id": "KC011_CI_WORKFLOW_PRESENT",
        "title": "CI workflow validates generated artifacts",
        "severity": "blocking",
        "category": "CI validation gate",
        "validator_finding": "ci workflow is required",
        "fixture_evidence": "fixtures/safe passes; fixtures/partial fails",
    },
)


def build_policy_pack() -> dict[str, Any]:
    return {
        "pack_id": "kube-copilot-predeploy",
        "version": "0.1.0",
        "scope": "pre-deployment generated Kubernetes and CI artifacts",
        "trust_boundary": (
            "Generated Kubernetes and CI files remain draft artifacts. The policy pack "
            "helps reviewers decide what to reject, what to fix, and what still requires human review."
        ),
        "rules": [dict(rule) for rule in POLICY_RULES],
        "public_references": [
            "kube-linter",
            "kubeconform",
            "kube-score",
            "Polaris",
            "Kyverno",
            "Gatekeeper",
            "Datree",
        ],
    }


def render_policy_pack_markdown(policy_pack: dict[str, Any]) -> str:
    lines = [
        "# Kube Copilot Policy Pack",
        "",
        f"- pack_id: `{policy_pack['pack_id']}`",
        f"- version: `{policy_pack['version']}`",
        f"- scope: `{policy_pack['scope']}`",
        "",
        "## Rules",
        "",
        "| id | severity | category | rule | validator finding | evidence |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for rule in policy_pack["rules"]:
        lines.append(
            f"| {rule['id']} | {rule['severity']} | {rule['category']} | "
            f"{rule['title']} | {rule['validator_finding']} | {rule['fixture_evidence']} |"
        )
    lines.extend(
        [
            "",
            "## Trust Boundary",
            "",
            policy_pack["trust_boundary"],
            "",
            "This policy pack is not a replacement for kube-linter, kubeconform, Gatekeeper, Kyverno, or admission control.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_policy_pack(output_dir: str | Path = "reports") -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    policy_pack = build_policy_pack()
    json_path = output_path / "policy-pack.json"
    json_path.write_text(json.dumps(policy_pack, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output_path / "policy-pack.md").write_text(render_policy_pack_markdown(policy_pack), encoding="utf-8")
    return json_path


if __name__ == "__main__":
    print(write_policy_pack())
