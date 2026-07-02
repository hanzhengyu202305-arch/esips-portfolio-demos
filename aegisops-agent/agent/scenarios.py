from __future__ import annotations

from dataclasses import asdict, dataclass


GLOBAL_BLOCKED_FILES = [
    ".github/workflows/*",
    "agent/evaluation/gold_labels.json",
    "apps/demo-api/tests/*",
    "tests/*",
]


@dataclass(frozen=True)
class ScenarioSpec:
    scenario_id: str
    slug: str
    title: str
    category: str
    root_cause_id: str
    failure_summary: str
    raw_log: str
    evidence_signals: list[dict]
    allowed_files: list[str]
    blocked_files: list[str]
    validation_kind: str
    runbook_query: str
    broken_files: dict[str, str]
    fixed_files: dict[str, str]
    manual_debug_minutes: int
    human_review_minutes: int

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def full_id(self) -> str:
        return f"{self.scenario_id}_{self.slug}"


def _blocked(extra: list[str] | None = None) -> list[str]:
    return GLOBAL_BLOCKED_FILES + (extra or [])


SERVICE_BROKEN = """def calculate_discount(order_total: float, customer_tier: str) -> float:
    if customer_tier == "gold":
        return round(order_total * 0.01, 2)
    return 0.0
"""

SERVICE_FIXED = """def calculate_discount(order_total: float, customer_tier: str) -> float:
    if customer_tier == "gold" and order_total >= 100:
        return round(order_total * 0.10, 2)
    return 0.0
"""

REQUIREMENTS_BROKEN = """fastapi==0.115.0
uvicorn==0.30.6
"""

REQUIREMENTS_FIXED = """fastapi==0.115.0
uvicorn==0.30.6
pydantic==2.9.2
"""

GITHUB_ENV_BROKEN = """env:
  APP_MODE: ""
steps:
  - run: pytest
"""

GITHUB_ENV_FIXED = """env:
  APP_MODE: "demo"
steps:
  - run: pytest
"""

K8S_ENV_BROKEN = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: aegisops-demo-api
spec:
  template:
    spec:
      containers:
        - name: api
          image: aegisops/demo-api:latest
          env:
            - name: APP_MODE
              value: broken
"""

K8S_ENV_FIXED = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: aegisops-demo-api
spec:
  template:
    spec:
      containers:
        - name: api
          image: aegisops/demo-api:latest
          env:
            - name: APP_MODE
              value: demo
"""

PROBE_BROKEN = """readinessProbe:
  httpGet:
    path: /readyz
    port: 8000
"""

PROBE_FIXED = """readinessProbe:
  httpGet:
    path: /health
    port: 8000
"""

TAG_BROKEN = """image:
  repository: aegisops/demo-api
  tag: canary-missing
"""

TAG_FIXED = """image:
  repository: aegisops/demo-api
  tag: local
"""

SECURITY_BROKEN = """containers:
  - name: api
    image: aegisops/demo-api:local
    securityContext:
      runAsUser: 0
"""

SECURITY_FIXED = """containers:
  - name: api
    image: aegisops/demo-api:local
    securityContext:
      runAsNonRoot: true
      runAsUser: 10001
      allowPrivilegeEscalation: false
"""

LATENCY_BROKEN = """def score_orders(orders):
    scores = []
    for order in orders:
        for other in orders:
            if order["customer_id"] == other["customer_id"]:
                pass
        scores.append(order["amount"])
    return scores
"""

LATENCY_FIXED = """def score_orders(orders):
    totals_by_customer = {}
    for order in orders:
        totals_by_customer.setdefault(order["customer_id"], 0)
        totals_by_customer[order["customer_id"]] += order["amount"]
    return [totals_by_customer[order["customer_id"]] for order in orders]
"""


SCENARIOS: dict[str, ScenarioSpec] = {
    "S1": ScenarioSpec(
        scenario_id="S1",
        slug="pytest_failure",
        title="pytest failure because discount logic is wrong",
        category="pytest",
        root_cause_id="wrong_discount_logic",
        failure_summary="pytest assertion fails because gold customer discount is 1% instead of 10%.",
        raw_log="""tests/test_demo_api.py::test_discount_logic_is_deterministic FAILED
E       assert 2.5 == 25.0
E        + where 2.5 = calculate_discount(order_total=250.0, customer_tier='gold')
""",
        evidence_signals=[
            {
                "id": "pytest:S1:assertion",
                "kind": "pytest",
                "message": "Gold tier discount expected 25.0 but observed 2.5.",
                "severity": "high",
            }
        ],
        allowed_files=["apps/demo-api/app/service.py"],
        blocked_files=_blocked(),
        validation_kind="pytest",
        runbook_query="pytest assertion wrong business logic discount",
        broken_files={"apps/demo-api/app/service.py": SERVICE_BROKEN},
        fixed_files={"apps/demo-api/app/service.py": SERVICE_FIXED},
        manual_debug_minutes=18,
        human_review_minutes=5,
    ),
    "S2": ScenarioSpec(
        scenario_id="S2",
        slug="docker_build_failure",
        title="Docker build failure because a dependency is missing",
        category="docker",
        root_cause_id="missing_python_dependency",
        failure_summary="Docker build imports pydantic but the image requirements omit it.",
        raw_log="""Step 7/8 : RUN python -c "import pydantic"
ModuleNotFoundError: No module named 'pydantic'
The command '/bin/sh -c python -c "import pydantic"' returned a non-zero code: 1
""",
        evidence_signals=[
            {
                "id": "docker:S2:missing-module",
                "kind": "docker-build",
                "message": "Image build cannot import pydantic.",
                "severity": "high",
            }
        ],
        allowed_files=["apps/demo-api/requirements.txt", "apps/demo-api/Dockerfile"],
        blocked_files=_blocked(),
        validation_kind="docker-dry-run",
        runbook_query="Docker build missing python dependency ModuleNotFoundError",
        broken_files={"apps/demo-api/requirements.txt": REQUIREMENTS_BROKEN},
        fixed_files={"apps/demo-api/requirements.txt": REQUIREMENTS_FIXED},
        manual_debug_minutes=20,
        human_review_minutes=6,
    ),
    "S3": ScenarioSpec(
        scenario_id="S3",
        slug="github_actions_env_failure",
        title="GitHub Actions failure because APP_MODE is missing",
        category="ci",
        root_cause_id="missing_app_mode_env",
        failure_summary="CI starts the app with an empty APP_MODE environment variable.",
        raw_log="""Run pytest
RuntimeError: APP_MODE must be one of demo, test, prod; got ''
Error: Process completed with exit code 1.
""",
        evidence_signals=[
            {
                "id": "gha:S3:empty-env",
                "kind": "github-actions",
                "message": "APP_MODE is empty in CI env.",
                "severity": "medium",
            }
        ],
        allowed_files=["ci/env.example.yml"],
        blocked_files=_blocked(),
        validation_kind="ci-dry-run",
        runbook_query="GitHub Actions missing environment variable APP_MODE",
        broken_files={"ci/env.example.yml": GITHUB_ENV_BROKEN},
        fixed_files={"ci/env.example.yml": GITHUB_ENV_FIXED},
        manual_debug_minutes=22,
        human_review_minutes=6,
    ),
    "S4": ScenarioSpec(
        scenario_id="S4",
        slug="k8s_crashloop",
        title="Kubernetes CrashLoopBackOff because APP_MODE is invalid",
        category="kubernetes",
        root_cause_id="invalid_app_mode_env",
        failure_summary="Pod restarts because APP_MODE is set to an unsupported value.",
        raw_log="""kubectl get pods
aegisops-demo-api-7f8c9d   0/1   CrashLoopBackOff   5   4m
kubectl logs aegisops-demo-api-7f8c9d
RuntimeError: APP_MODE must be one of demo, test, prod; got 'broken'
""",
        evidence_signals=[
            {
                "id": "k8s:S4:invalid-env",
                "kind": "kubernetes",
                "message": "Deployment sets APP_MODE to unsupported value 'broken'.",
                "severity": "high",
            }
        ],
        allowed_files=["k8s/overlays/broken-env/deployment.yaml"],
        blocked_files=_blocked(),
        validation_kind="k8s-dry-run",
        runbook_query="Kubernetes CrashLoopBackOff invalid environment variable APP_MODE",
        broken_files={"k8s/overlays/broken-env/deployment.yaml": K8S_ENV_BROKEN},
        fixed_files={"k8s/overlays/broken-env/deployment.yaml": K8S_ENV_FIXED},
        manual_debug_minutes=28,
        human_review_minutes=8,
    ),
    "S5": ScenarioSpec(
        scenario_id="S5",
        slug="k8s_probe_failure",
        title="Kubernetes readiness probe path is wrong",
        category="kubernetes",
        root_cause_id="wrong_readiness_probe_path",
        failure_summary="The pod is running but not ready because readiness probes call /readyz.",
        raw_log="""Readiness probe failed: HTTP probe failed with statuscode: 404
GET /readyz returned 404 while /health returned 200.
""",
        evidence_signals=[
            {
                "id": "k8s:S5:probe-404",
                "kind": "kubernetes",
                "message": "Readiness probe path /readyz does not exist.",
                "severity": "medium",
            }
        ],
        allowed_files=["k8s/overlays/broken-probe/deployment.yaml"],
        blocked_files=_blocked(),
        validation_kind="k8s-dry-run",
        runbook_query="Kubernetes readiness probe wrong path 404 health",
        broken_files={"k8s/overlays/broken-probe/deployment.yaml": PROBE_BROKEN},
        fixed_files={"k8s/overlays/broken-probe/deployment.yaml": PROBE_FIXED},
        manual_debug_minutes=25,
        human_review_minutes=7,
    ),
    "S6": ScenarioSpec(
        scenario_id="S6",
        slug="image_tag_mismatch",
        title="Kubernetes ImagePullBackOff because image tag is missing",
        category="kubernetes",
        root_cause_id="image_tag_mismatch",
        failure_summary="Deployment references an image tag that does not exist in the local registry.",
        raw_log="""Failed to pull image "aegisops/demo-api:canary-missing"
Back-off pulling image "aegisops/demo-api:canary-missing"
""",
        evidence_signals=[
            {
                "id": "k8s:S6:image-tag",
                "kind": "kubernetes",
                "message": "Image tag canary-missing cannot be pulled.",
                "severity": "high",
            }
        ],
        allowed_files=["k8s/overlays/healthy/kustomization.yaml"],
        blocked_files=_blocked(),
        validation_kind="k8s-dry-run",
        runbook_query="Kubernetes ImagePullBackOff image tag mismatch",
        broken_files={"k8s/overlays/healthy/kustomization.yaml": TAG_BROKEN},
        fixed_files={"k8s/overlays/healthy/kustomization.yaml": TAG_FIXED},
        manual_debug_minutes=24,
        human_review_minutes=7,
    ),
    "S7": ScenarioSpec(
        scenario_id="S7",
        slug="container_security_failure",
        title="Container security failure because the API runs as root",
        category="security",
        root_cause_id="container_runs_as_root",
        failure_summary="Policy validation flags a root container and missing privilege escalation controls.",
        raw_log="""policy check failed
container api must runAsNonRoot and must set allowPrivilegeEscalation=false
""",
        evidence_signals=[
            {
                "id": "security:S7:root-container",
                "kind": "security",
                "message": "Container securityContext allows root execution.",
                "severity": "high",
            }
        ],
        allowed_files=["k8s/overlays/insecure/deployment.yaml"],
        blocked_files=_blocked(),
        validation_kind="security-dry-run",
        runbook_query="Kubernetes container securityContext runAsNonRoot allowPrivilegeEscalation",
        broken_files={"k8s/overlays/insecure/deployment.yaml": SECURITY_BROKEN},
        fixed_files={"k8s/overlays/insecure/deployment.yaml": SECURITY_FIXED},
        manual_debug_minutes=30,
        human_review_minutes=9,
    ),
    "S8": ScenarioSpec(
        scenario_id="S8",
        slug="latency_regression",
        title="Latency regression because order scoring uses a nested loop",
        category="latency",
        root_cause_id="nested_loop_latency_regression",
        failure_summary="The scoring path regressed after adding an O(n^2) customer aggregation loop.",
        raw_log="""benchmark failed
p95 latency increased from 120ms to 980ms after order scoring change
""",
        evidence_signals=[
            {
                "id": "latency:S8:nested-loop",
                "kind": "benchmark",
                "message": "Nested loop repeats customer aggregation for every order.",
                "severity": "medium",
            }
        ],
        allowed_files=["apps/demo-api/app/service.py"],
        blocked_files=_blocked(),
        validation_kind="latency-dry-run",
        runbook_query="Python latency regression nested loop precompute totals by customer",
        broken_files={"apps/demo-api/app/service.py": LATENCY_BROKEN},
        fixed_files={"apps/demo-api/app/service.py": LATENCY_FIXED},
        manual_debug_minutes=35,
        human_review_minutes=10,
    ),
}


def list_scenarios() -> list[ScenarioSpec]:
    return [SCENARIOS[key] for key in sorted(SCENARIOS)]


def get_scenario(scenario_id: str) -> ScenarioSpec:
    try:
        return SCENARIOS[scenario_id]
    except KeyError as exc:
        known = ", ".join(sorted(SCENARIOS))
        raise KeyError(f"Unknown scenario {scenario_id!r}; expected one of: {known}") from exc
