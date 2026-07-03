from dataclasses import dataclass

from kube_copilot.generator import GeneratedWorkspace


@dataclass(frozen=True)
class ValidationReport:
    passed: bool
    findings: list[str]

    def to_markdown(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        lines = [f"# Kube Copilot validation report", "", f"Status: {status}", ""]
        if self.findings:
            lines.append("## Findings")
            lines.extend(f"- {finding}" for finding in self.findings)
        else:
            lines.append("No blocking findings.")
        return "\n".join(lines) + "\n"


def validate_workspace(workspace: GeneratedWorkspace) -> ValidationReport:
    deployment = workspace.files.get("k8s/deployment.yaml", "")
    findings: list[str] = []

    if ":latest" in deployment:
        findings.append("image tag must not be latest")
    if not _section_has_value(deployment, "limits", "cpu"):
        findings.append("cpu limit is required")
    if not _section_has_value(deployment, "limits", "memory"):
        findings.append("memory limit is required")
    if not _section_has_value(deployment, "requests", "cpu"):
        findings.append("cpu request is required")
    if not _section_has_value(deployment, "requests", "memory"):
        findings.append("memory request is required")
    if "readinessProbe:" not in deployment:
        findings.append("readiness probe is required")
    if "livenessProbe:" not in deployment:
        findings.append("liveness probe is required")
    if "securityContext:" not in deployment:
        findings.append("securityContext is required")
    if "runAsNonRoot: true" not in deployment:
        findings.append("runAsNonRoot must be true")
    if "privileged: true" in deployment:
        findings.append("privileged containers are not allowed")
    if "allowPrivilegeEscalation: false" not in deployment:
        findings.append("privilege escalation must be disabled")
    if "requests:" not in deployment:
        findings.append("resource requests are required")
    if ".github/workflows/ci.yml" not in workspace.files:
        findings.append("ci workflow is required")

    return ValidationReport(passed=not findings, findings=findings)


def _section_has_value(yaml_text: str, section: str, key: str) -> bool:
    lines = yaml_text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != f"{section}:":
            continue
        section_indent = len(line) - len(line.lstrip())
        for child in lines[index + 1 :]:
            if not child.strip():
                continue
            child_indent = len(child) - len(child.lstrip())
            if child_indent <= section_indent:
                break
            stripped = child.strip()
            if not stripped.startswith(f"{key}:"):
                continue
            value = stripped.split(":", 1)[1].strip().strip('"')
            return bool(value)
    return False
