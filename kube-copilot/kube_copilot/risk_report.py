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
        "| case | validation | reviewer decision | blocking | warning | manual review |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for name, workspace in cases.items():
        report = validate_workspace(workspace)
        validation = "PASS" if report.passed else "FAIL"
        decision = _reviewer_decision(report.findings)
        grouped = _group_findings(report.findings)
        blocking = _join_findings(grouped["blocking"])
        warning = _join_findings(grouped["warning"])
        manual_review = _join_findings(grouped["manual_review"])
        lines.append(f"| {name} | {validation} | {decision} | {blocking} | {warning} | {manual_review} |")
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
            "- Treat credential handling, RBAC, network policy, cluster quota, rollout window, and business risk as manual review items.",
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
        ("structural YAML parsing", "validator integrity", "comments cannot spoof controls"),
        ("every container checked", "policy coverage", "unsafe sidecar fails"),
        ("host namespace and hostPath rejected", "host isolation", "host-boundary cases fail"),
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
            "- `reports/adversarial-validation.md` shows comment spoofing, unsafe sidecar, and multi-document bypass attempts being rejected.",
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


def adversarial_workspaces() -> dict[str, GeneratedWorkspace]:
    safe = generate_workspace(
        app_name="safe-api",
        image="ghcr.io/example/safe-api:1.0.0",
        port=8080,
        replicas=2,
        cpu_limit="500m",
        memory_limit="512Mi",
    )
    comment_spoof = _workspace_with_deployment(
        safe,
        """apiVersion: apps/v1
kind: Deployment
metadata:
  name: comment-spoof
spec:
  template:
    spec:
      # runAsNonRoot: true
      containers:
        - name: api
          image: example/api:latest
          # limits: {cpu: 500m, memory: 512Mi}
          # readinessProbe: {httpGet: {path: /health, port: 8080}}
          securityContext:
            privileged: true
            allowPrivilegeEscalation: true
""",
    )
    unsafe_sidecar = _workspace_with_deployment(
        safe,
        safe.files["k8s/deployment.yaml"]
        + """---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: unsafe-sidecar
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
      containers:
        - name: app
          image: example/app:1.0.0
          readinessProbe: {httpGet: {path: /health, port: 8080}}
          livenessProbe: {httpGet: {path: /health, port: 8080}}
          resources:
            requests: {cpu: 100m, memory: 128Mi}
            limits: {cpu: 200m, memory: 256Mi}
          securityContext:
            allowPrivilegeEscalation: false
        - name: debug-sidecar
          image: example/debug:latest
          privileged: true
""",
    )
    second_document = _workspace_with_deployment(
        safe,
        safe.files["k8s/deployment.yaml"]
        + """---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hidden-unsafe
spec:
  template:
    spec:
      hostPID: true
      volumes:
        - name: host-root
          hostPath: {path: /}
      containers:
        - name: hidden
          image: example/hidden:latest
""",
    )
    return {
        "safe baseline": safe,
        "comment spoof": comment_spoof,
        "unsafe sidecar": unsafe_sidecar,
        "unsafe second document": second_document,
    }


def render_adversarial_validation() -> str:
    lines = [
        "# Kube Copilot Adversarial Validation",
        "",
        "These cases attack validator assumptions that plain text search commonly misses.",
        "",
        "| case | expected | observed | key findings |",
        "| --- | --- | --- | --- |",
    ]
    for name, workspace in adversarial_workspaces().items():
        report = validate_workspace(workspace)
        expected = "PASS" if name == "safe baseline" else "FAIL"
        observed = "PASS" if report.passed else "FAIL"
        findings = "; ".join(report.findings[:5]) if report.findings else "none"
        lines.append(f"| {name} | {expected} | {observed} | {findings} |")
    lines.extend(
        [
            "",
            "## Why This Matters",
            "",
            "The validator parses every YAML document and every application or init container. Comments do not count as controls, and an unsafe sidecar or second Deployment cannot hide behind a safe first container.",
            "",
            "## Boundary",
            "",
            "This is a focused local policy demo, not schema validation, admission control, or a replacement for mature Kubernetes security tools.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_adversarial_report(path: str | Path = "reports/adversarial-validation.md") -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_adversarial_validation(), encoding="utf-8")
    return output_path


def _workspace_with_deployment(workspace: GeneratedWorkspace, deployment: str) -> GeneratedWorkspace:
    files = dict(workspace.files)
    files["k8s/deployment.yaml"] = deployment
    return GeneratedWorkspace(app_name=workspace.app_name, files=files)


def _reviewer_decision(findings: list[str]) -> str:
    if not findings:
        return "PASS"
    if len(findings) <= 3:
        return "PARTIAL"
    return "FAIL"


def _group_findings(findings: list[str]) -> dict[str, list[str]]:
    grouped = {"blocking": [], "warning": [], "manual_review": []}
    for finding in findings:
        if finding in {
            "image tag must not be latest",
            "runAsNonRoot must be true",
            "privileged containers are not allowed",
            "privilege escalation must be disabled",
            "ci workflow is required",
        }:
            grouped["blocking"].append(finding)
        elif finding in {
            "cpu limit is required",
            "memory limit is required",
            "cpu request is required",
            "memory request is required",
            "readiness probe is required",
            "liveness probe is required",
            "resource requests are required",
        }:
            grouped["warning"].append(finding)
        else:
            grouped["manual_review"].append(finding)
    if not findings:
        grouped["manual_review"].append("credential handling, RBAC, rollout window, and production context still require human review")
    return grouped


def _join_findings(findings: list[str]) -> str:
    return "; ".join(findings) if findings else "none"


def write_report(path: str = "reports/risk-comparison.md") -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(compare_safe_and_risky_workspace(), encoding="utf-8")
    write_policy_matrix(output_path.parent / "policy-matrix.md")
    write_adversarial_report(output_path.parent / "adversarial-validation.md")
    return output_path


def write_policy_matrix(path: str | Path = "reports/policy-matrix.md") -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(policy_matrix_markdown(), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    print(write_report())
