from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import yaml

from kube_copilot.generator import GeneratedWorkspace


@dataclass(frozen=True)
class ValidationReport:
    passed: bool
    findings: list[str]

    def to_markdown(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = ["# Kube Copilot validation report", "", f"Status: {status}", ""]
        if self.findings:
            lines.append("## Findings")
            lines.extend(f"- {finding}" for finding in self.findings)
        else:
            lines.append("No blocking findings.")
        return "\n".join(lines) + "\n"


def validate_workspace(workspace: GeneratedWorkspace) -> ValidationReport:
    deployment_text = workspace.files.get("k8s/deployment.yaml", "")
    findings: list[str] = []

    try:
        documents = [document for document in yaml.safe_load_all(deployment_text) if document is not None]
    except yaml.YAMLError:
        documents = []
        findings.append("deployment YAML must be structurally valid")

    deployments = [
        document
        for document in documents
        if isinstance(document, dict) and document.get("kind") == "Deployment"
    ]
    if not deployments and "deployment YAML must be structurally valid" not in findings:
        findings.append("Deployment manifest is required")

    for deployment in deployments:
        _validate_deployment(deployment, findings)

    if ".github/workflows/ci.yml" not in workspace.files:
        findings.append("ci workflow is required")

    unique_findings = list(dict.fromkeys(findings))
    return ValidationReport(passed=not unique_findings, findings=unique_findings)


def _validate_deployment(deployment: dict[str, Any], findings: list[str]) -> None:
    pod_spec = _mapping(deployment, "spec", "template", "spec")
    pod_security = _dict_value(pod_spec, "securityContext")

    if any(pod_spec.get(field) is True for field in ("hostNetwork", "hostPID", "hostIPC")):
        findings.append("host namespaces are not allowed")
    if _uses_host_path(pod_spec):
        findings.append("hostPath volumes are not allowed")

    containers = _list_of_dicts(pod_spec.get("containers"))
    if not containers:
        findings.append("at least one application container is required")
    for container in containers:
        _validate_container(container, pod_security, findings, require_probes=True)

    for container in _list_of_dicts(pod_spec.get("initContainers")):
        _validate_container(container, pod_security, findings, require_probes=False)


def _validate_container(
    container: dict[str, Any],
    pod_security: dict[str, Any],
    findings: list[str],
    require_probes: bool,
) -> None:
    image = str(container.get("image", "")).strip()
    if not image or _uses_latest_tag(image):
        findings.append("image tag must not be latest")
    elif not _has_pinned_reference(image):
        findings.append("image tag must be pinned")

    resources = _dict_value(container, "resources")
    requests = _dict_value(resources, "requests")
    limits = _dict_value(resources, "limits")
    if not _non_empty(requests.get("cpu")):
        findings.append("cpu request is required")
    if not _non_empty(requests.get("memory")):
        findings.append("memory request is required")
    if not _non_empty(limits.get("cpu")):
        findings.append("cpu limit is required")
    if not _non_empty(limits.get("memory")):
        findings.append("memory limit is required")
    if not requests:
        findings.append("resource requests are required")

    if require_probes and not isinstance(container.get("readinessProbe"), dict):
        findings.append("readiness probe is required")
    if require_probes and not isinstance(container.get("livenessProbe"), dict):
        findings.append("liveness probe is required")

    container_security = _dict_value(container, "securityContext")
    if not pod_security and not container_security:
        findings.append("securityContext is required")
    run_as_non_root = container_security.get("runAsNonRoot", pod_security.get("runAsNonRoot"))
    if run_as_non_root is not True:
        findings.append("runAsNonRoot must be true")
    if container_security.get("privileged") is True:
        findings.append("privileged containers are not allowed")
    if container_security.get("allowPrivilegeEscalation") is not False:
        findings.append("privilege escalation must be disabled")


def _mapping(value: dict[str, Any], *keys: str) -> dict[str, Any]:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return {}
        current = current.get(key)
    return current if isinstance(current, dict) else {}


def _dict_value(value: dict[str, Any], key: str) -> dict[str, Any]:
    candidate = value.get(key)
    return candidate if isinstance(candidate, dict) else {}


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _non_empty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def _uses_latest_tag(image: str) -> bool:
    reference = image.rsplit("/", 1)[-1]
    return "@" not in reference and (":" not in reference or reference.rsplit(":", 1)[-1] == "latest")


def _has_pinned_reference(image: str) -> bool:
    reference = image.rsplit("/", 1)[-1]
    return "@sha256:" in image or (":" in reference and bool(reference.rsplit(":", 1)[-1]))


def _uses_host_path(pod_spec: dict[str, Any]) -> bool:
    for volume in _list_of_dicts(pod_spec.get("volumes")):
        if isinstance(volume.get("hostPath"), dict):
            return True
    return False
