from pathlib import Path

from kube_copilot.generator import generate_workspace
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
        "| case | status | findings |",
        "| --- | --- | --- |",
    ]
    for name, workspace in cases.items():
        report = validate_workspace(workspace)
        status = "PASS" if report.passed else "FAIL"
        findings = "; ".join(report.findings) if report.findings else "none"
        lines.append(f"| {name} | {status} | {findings} |")
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
            "The generated YAML is not production-ready until it passes policy checks.",
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


def write_report(path: str = "reports/risk-comparison.md") -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(compare_safe_and_risky_workspace(), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print(write_report())
