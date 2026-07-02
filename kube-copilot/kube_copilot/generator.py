from dataclasses import dataclass
from textwrap import dedent


@dataclass(frozen=True)
class GeneratedWorkspace:
    app_name: str
    files: dict[str, str]


def generate_workspace(
    app_name: str,
    image: str,
    port: int,
    replicas: int,
    cpu_limit: str,
    memory_limit: str,
) -> GeneratedWorkspace:
    """Generate a small deployable Kubernetes/CI workspace."""
    deployment = _deployment_yaml(app_name, image, port, replicas, cpu_limit, memory_limit)
    files = {
        "Dockerfile": _dockerfile(port),
        "k8s/deployment.yaml": deployment,
        "k8s/service.yaml": _service_yaml(app_name, port),
        ".github/workflows/ci.yml": _ci_workflow(app_name),
        "validation-checklist.md": _checklist(app_name),
    }
    return GeneratedWorkspace(app_name=app_name, files=files)


def _dockerfile(port: int) -> str:
    return dedent(
        f"""\
        FROM python:3.12-slim
        WORKDIR /app
        COPY . .
        EXPOSE {port}
        CMD ["python", "-m", "http.server", "{port}"]
        """
    )


def _request_from_limit(limit: str) -> str:
    if not limit:
        return ""
    if limit.endswith("m") and limit[:-1].isdigit():
        return f"{max(int(limit[:-1]) // 2, 1)}m"
    for suffix in ("Mi", "Gi"):
        if limit.endswith(suffix) and limit[: -len(suffix)].isdigit():
            return f"{max(int(limit[: -len(suffix)]) // 2, 1)}{suffix}"
    return limit


def _deployment_yaml(
    app_name: str,
    image: str,
    port: int,
    replicas: int,
    cpu_limit: str,
    memory_limit: str,
) -> str:
    cpu_request = _request_from_limit(cpu_limit)
    memory_request = _request_from_limit(memory_limit)
    return dedent(
        f"""\
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: {app_name}
          labels:
            app: {app_name}
        spec:
          replicas: {replicas}
          selector:
            matchLabels:
              app: {app_name}
          template:
            metadata:
              labels:
                app: {app_name}
            spec:
              containers:
                - name: {app_name}
                  image: {image}
                  ports:
                    - containerPort: {port}
                  readinessProbe:
                    httpGet:
                      path: /health
                      port: {port}
                    initialDelaySeconds: 5
                    periodSeconds: 10
                  livenessProbe:
                    httpGet:
                      path: /health
                      port: {port}
                    initialDelaySeconds: 15
                    periodSeconds: 20
                  resources:
                    requests:
                      cpu: "{cpu_request}"
                      memory: "{memory_request}"
                    limits:
                      cpu: "{cpu_limit}"
                      memory: "{memory_limit}"
        """
    )


def _service_yaml(app_name: str, port: int) -> str:
    return dedent(
        f"""\
        apiVersion: v1
        kind: Service
        metadata:
          name: {app_name}
        spec:
          type: ClusterIP
          selector:
            app: {app_name}
          ports:
            - name: http
              port: {port}
              targetPort: {port}
        """
    )


def _ci_workflow(app_name: str) -> str:
    return dedent(
        f"""\
        name: validate-{app_name}
        on:
          pull_request:
          push:
            branches: [main]
        jobs:
          validate:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - name: Build image
                run: docker build -t {app_name}:ci .
              - name: Kubernetes dry-run
                run: kubectl apply --dry-run=client -f k8s/
        """
    )


def _checklist(app_name: str) -> str:
    return dedent(
        f"""\
        # Validation checklist for {app_name}

        - Image tag is pinned and reproducible.
        - CPU and memory limits are set.
        - Readiness probe points to a lightweight health endpoint.
        - CI performs Docker build and Kubernetes client-side dry-run.
        - Human review remains required for secrets, RBAC, and production rollout.
        """
    )

