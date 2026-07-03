from pathlib import Path

from kube_copilot.generator import GeneratedWorkspace, generate_workspace
from kube_copilot.validator import validate_workspace


def compare_safe_and_risky_workspace() -> str:
    cases = {
        "safe": generate_workspace(
            app_name="ore-api",
            image="ghcr.io/example/ore-api:1.2.0",
            port=8080,
            replicas=3,
            cpu_limit="500m",
            memory_limit="512Mi",
        ),
        "risky": generate_workspace(
            app_name="risky-api",
            image="example/risky-api:latest",
            port=8000,
            replicas=1,
            cpu_limit="",
            memory_limit="",
            secure_context=False,
        ),
        "partial": partial_remediation_workspace(),
    }

    lines = [
        "# Kube Copilot risk comparison",
        "",
        "Target ESIPS brief: `Accenture_01 Kubernetes_DevOps.pdf`.",
        "",
        (
            "This report frames Kube Copilot as a small Kubernetes-based CI/CD "
            "pipeline assistant: generation is useful, but validation and human "
            "review remain the trust boundary."
        ),
        "",
        "| case | validation | reviewer decision | findings |",
        "| --- | --- | --- | --- |",
    ]
    for name, workspace in cases.items():
        report = validate_workspace(workspace)
        validation = "PASS" if report.passed else "FAIL"
        decision = _reviewer_decision(report.findings)
        findings = "; ".join(report.findings) if report.findings else "none"
        lines.append(f"| {name} | {validation} | {decision} | {findings} |")
    lines.extend(
        [
            "",
            "## Remediation checklist",
            "",
            "- Pin image tags to immutable versions before deployment review.",
            "- Set CPU and memory requests and limits for every container.",
            "- Validate probes before rollout so health checks match the application contract.",
            "- Require non-root security contexts and reject privileged containers.",
            "- Keep generated manifests behind CI and human review gates.",
            "",
            "## Interview framing",
            "",
            "The generator can draft Kubernetes and CI/CD files, but the validator is the trust boundary.",
            "The generated YAML is not suitable for production use until it passes policy checks.",
            "Human review remains required for secrets, RBAC, production rollout, and business risk.",
            "",
            "## Public references",
            "",
            (
                "This demo is intentionally much smaller than kube-linter, kubeconform, kube-score, "
                "Polaris, Kyverno, Gatekeeper, or Datree. The shared idea is that generated "
                "Kubernetes manifests need policy-style checks before they are trusted."
            ),
        ]
    )
    return "\n".join(lines) + "\n"


def policy_matrix_markdown() -> str:
    rules = [
        ("image tag must not be `latest`", "reproducibility", "safe passes; risky fails"),
        ("CPU request required", "scheduler reliability", "safe passes; risky fails"),
        ("memory request required", "scheduler reliability", "safe passes; risky fails"),
        ("CPU limit required", "blast-radius control", "safe passes; risky fails"),
        ("memory limit required", "OOM risk control", "safe passes; risky fails"),
        ("readiness probe required", "rollout safety", "safe passes"),
        ("liveness probe required", "recovery safety", "partial fails"),
        ("`runAsNonRoot: true`", "container security", "safe passes; risky fails"),
        ("privileged container rejected", "privilege boundary", "risky fails"),
        ("privilege escalation disabled", "least privilege", "risky fails"),
        ("GitHub Actions workflow present", "CI validation gate", "partial fails"),
    ]
    lines = [
        "# Kube Copilot policy matrix",
        "",
        "This matrix documents the deterministic checks used by Kube Copilot. The demo is pre-deployment validation, not a replacement for kube-linter, kubeconform, Gatekeeper, Kyverno, or production admission control.",
        "",
        "| rule | why it matters | fixture evidence |",
        "| --- | --- | --- |",
    ]
    for rule, why, evidence in rules:
        lines.append(f"| {rule} | {why} | {evidence} |")
    lines.extend(
        [
            "",
            "## Fixtures",
            "",
            "- `fixtures/safe/` shows a pinned image, resources, probes, security context, and CI.",
            "- `fixtures/partial/` shows incremental remediation with a missing liveness probe and missing CI workflow.",
            "- `fixtures/risky/` shows a latest tag, missing resources, and insecure container settings.",
            "",
            "## Trust Boundary",
            "",
            "AI-generated Kubernetes YAML is a draft. The validator and human review decide whether the draft is suitable for further engineering work.",
        ]
    )
    return "\n".join(lines) + "\n"


def partial_remediation_workspace() -> GeneratedWorkspace:
    workspace = generate_workspace(
        app_name="partial-api",
        image="ghcr.io/example/partial-api:1.1.0",
        port=8080,
        replicas=2,
        cpu_limit="500m",
        memory_limit="512Mi",
    )
    deployment = workspace.files["k8s/deployment.yaml"]
    deployment = deployment.replace(
        "          livenessProbe:\n"
        "            httpGet:\n"
        "              path: /health\n"
        "              port: 8080\n"
        "            initialDelaySeconds: 15\n"
        "            periodSeconds: 20\n",
        "",
    )
    files = dict(workspace.files)
    files["k8s/deployment.yaml"] = deployment
    files.pop(".github/workflows/ci.yml")
    return GeneratedWorkspace(app_name=workspace.app_name, files=files)


def _reviewer_decision(findings: list[str]) -> str:
    if not findings:
        return "PASS"
    if len(findings) <= 3:
        return "PARTIAL"
    return "FAIL"


def write_report(path: str = "reports/risk-comparison.md") -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(compare_safe_and_risky_workspace(), encoding="utf-8")
    write_policy_matrix(output_path.parent / "policy-matrix.md")
    return output_path


def write_policy_matrix(path: str | Path = "reports/policy-matrix.md") -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(policy_matrix_markdown(), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print(write_report())
