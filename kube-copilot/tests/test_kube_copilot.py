import unittest

from kube_copilot.generator import generate_workspace
from kube_copilot.risk_report import (
    compare_safe_and_risky_workspace,
    partial_remediation_workspace,
    policy_matrix_markdown,
)
from kube_copilot.validator import validate_workspace


class KubeCopilotTests(unittest.TestCase):
    def test_generates_expected_kubernetes_and_ci_artifacts(self):
        workspace = generate_workspace(
            app_name="ore-api",
            image="ghcr.io/example/ore-api:1.2.0",
            port=8080,
            replicas=3,
            cpu_limit="500m",
            memory_limit="512Mi",
        )

        self.assertIn("Dockerfile", workspace.files)
        self.assertIn("k8s/deployment.yaml", workspace.files)
        self.assertIn("k8s/service.yaml", workspace.files)
        self.assertIn(".github/workflows/ci.yml", workspace.files)
        deployment = workspace.files["k8s/deployment.yaml"]
        self.assertIn("ore-api", deployment)
        self.assertIn("ghcr.io/example/ore-api:1.2.0", deployment)
        self.assertIn("requests:", deployment)
        self.assertIn("livenessProbe:", deployment)
        self.assertIn("      securityContext:\n        runAsNonRoot: true", deployment)
        self.assertIn("      containers:\n        - name: ore-api", deployment)
        self.assertIn(
            "          securityContext:\n            allowPrivilegeEscalation: false\n            privileged: false",
            deployment,
        )
        self.assertIn("type: ClusterIP", workspace.files["k8s/service.yaml"])

    def test_validator_flags_missing_limits_and_latest_tag(self):
        workspace = generate_workspace(
            app_name="risky-api",
            image="example/risky-api:latest",
            port=8000,
            replicas=1,
            cpu_limit="",
            memory_limit="",
        )

        report = validate_workspace(workspace)

        self.assertFalse(report.passed)
        self.assertIn("image tag must not be latest", report.findings)
        self.assertIn("cpu limit is required", report.findings)
        self.assertIn("memory limit is required", report.findings)
        self.assertIn("cpu request is required", report.findings)
        self.assertIn("memory request is required", report.findings)

    def test_validator_flags_missing_liveness_probe(self):
        workspace = generate_workspace(
            app_name="probe-api",
            image="ghcr.io/example/probe-api:1.0.0",
            port=8000,
            replicas=2,
            cpu_limit="500m",
            memory_limit="512Mi",
        )
        workspace.files["k8s/deployment.yaml"] = workspace.files["k8s/deployment.yaml"].replace(
            "          livenessProbe:\n"
            "            httpGet:\n"
            "              path: /health\n"
            "              port: 8000\n"
            "            initialDelaySeconds: 15\n"
            "            periodSeconds: 20\n",
            "",
        )

        report = validate_workspace(workspace)

        self.assertFalse(report.passed)
        self.assertIn("liveness probe is required", report.findings)

    def test_validator_flags_missing_ci_workflow(self):
        workspace = generate_workspace(
            app_name="no-ci-api",
            image="ghcr.io/example/no-ci-api:1.0.0",
            port=8000,
            replicas=2,
            cpu_limit="500m",
            memory_limit="512Mi",
        )
        workspace.files.pop(".github/workflows/ci.yml")

        report = validate_workspace(workspace)

        self.assertFalse(report.passed)
        self.assertIn("ci workflow is required", report.findings)

    def test_validator_flags_privileged_security_context(self):
        workspace = generate_workspace(
            app_name="privileged-api",
            image="ghcr.io/example/privileged-api:1.0.0",
            port=8000,
            replicas=2,
            cpu_limit="500m",
            memory_limit="512Mi",
            secure_context=False,
        )

        report = validate_workspace(workspace)

        self.assertFalse(report.passed)
        self.assertIn("runAsNonRoot must be true", report.findings)
        self.assertIn("privileged containers are not allowed", report.findings)
        self.assertIn("privilege escalation must be disabled", report.findings)

    def test_validator_flags_missing_readiness_probe(self):
        workspace = generate_workspace(
            app_name="readiness-api",
            image="ghcr.io/example/readiness-api:1.0.0",
            port=8000,
            replicas=2,
            cpu_limit="500m",
            memory_limit="512Mi",
        )
        workspace.files["k8s/deployment.yaml"] = workspace.files["k8s/deployment.yaml"].replace(
            "          readinessProbe:\n"
            "            httpGet:\n"
            "              path: /health\n"
            "              port: 8000\n"
            "            initialDelaySeconds: 5\n"
            "            periodSeconds: 10\n",
            "",
        )

        report = validate_workspace(workspace)

        self.assertFalse(report.passed)
        self.assertIn("readiness probe is required", report.findings)

    def test_risk_report_compares_safe_and_risky_generation(self):
        markdown = compare_safe_and_risky_workspace()

        self.assertIn("| safe | PASS | PASS |", markdown)
        self.assertIn("| partial | FAIL | PARTIAL |", markdown)
        self.assertIn("| risky | FAIL | FAIL |", markdown)
        self.assertIn("image tag must not be latest", markdown)
        self.assertIn("ci workflow is required", markdown)
        self.assertIn("## Remediation checklist", markdown)
        self.assertIn("Pin image tags to immutable versions", markdown)
        self.assertIn("Set CPU and memory requests and limits", markdown)
        self.assertIn("Validate probes before rollout", markdown)
        self.assertIn("Require non-root security contexts", markdown)
        self.assertIn("privileged containers are not allowed", markdown)
        self.assertIn("Accenture_01 Kubernetes_DevOps", markdown)
        self.assertIn("Kubernetes-based CI/CD pipeline", markdown)
        self.assertIn("generated YAML is not suitable for production use until it passes policy checks", markdown)
        self.assertIn("kube-linter", markdown)

    def test_partial_workspace_is_incremental_not_fully_risky(self):
        report = validate_workspace(partial_remediation_workspace())

        self.assertFalse(report.passed)
        self.assertEqual(
            sorted(report.findings),
            sorted(["liveness probe is required", "ci workflow is required"]),
        )

    def test_policy_matrix_documents_all_rules_and_boundaries(self):
        markdown = policy_matrix_markdown()

        for expected in [
            "image tag must not be `latest`",
            "CPU request required",
            "memory request required",
            "CPU limit required",
            "memory limit required",
            "readiness probe required",
            "liveness probe required",
            "`runAsNonRoot: true`",
            "privileged container rejected",
            "privilege escalation disabled",
            "GitHub Actions workflow present",
        ]:
            self.assertIn(expected, markdown)
        self.assertIn("pre-deployment validation", markdown)
        self.assertIn("fixtures/partial", markdown)


if __name__ == "__main__":
    unittest.main()
