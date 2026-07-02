from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX = PROJECT_ROOT / "agent" / "memory" / "index.json"


EMBEDDED_RUNBOOKS = [
    {
        "id": "runbook-pytest",
        "title": "Pytest Assertion Failures",
        "path": "docs/runbooks/pytest-failure.md",
        "text": "Compare the assertion message with business rules, patch the implementation, and rerun pytest.",
    },
    {
        "id": "runbook-docker",
        "title": "Docker Build Missing Dependencies",
        "path": "docs/runbooks/docker-build.md",
        "text": "ModuleNotFoundError during image build usually means requirements.txt is missing a package.",
    },
    {
        "id": "runbook-ci",
        "title": "GitHub Actions Environment Variables",
        "path": "docs/runbooks/github-actions.md",
        "text": "Check workflow env defaults and make required application settings explicit.",
    },
    {
        "id": "runbook-k8s-crashloop",
        "title": "Kubernetes CrashLoopBackOff",
        "path": "docs/runbooks/kubernetes-crashloop.md",
        "text": "Inspect pod logs, environment variables, and deployment overlays when a container restarts.",
    },
    {
        "id": "runbook-k8s-probe",
        "title": "Kubernetes Readiness Probe Failures",
        "path": "docs/runbooks/k8s-readiness-probe.md",
        "text": "Compare readiness probe paths with application routes and use a lightweight health endpoint.",
    },
    {
        "id": "runbook-security",
        "title": "Container Security Context",
        "path": "docs/runbooks/container-security.md",
        "text": "Prefer non-root containers and disable privilege escalation in Kubernetes manifests.",
    },
    {
        "id": "runbook-latency",
        "title": "Latency Regression",
        "path": "docs/runbooks/latency-regression.md",
        "text": "Look for nested loops or repeated work, then cache or pre-aggregate by key.",
    },
]


def build_index(
    source_dir: Path | str = PROJECT_ROOT / "docs" / "runbooks",
    index_path: Path | str = DEFAULT_INDEX,
) -> Path:
    source_path = Path(source_dir)
    docs: list[dict[str, Any]] = []
    if source_path.exists():
        for path in sorted(source_path.glob("*.md")):
            docs.append(
                {
                    "id": path.stem,
                    "title": path.stem.replace("-", " ").title(),
                    "path": str(path.relative_to(PROJECT_ROOT)),
                    "text": path.read_text(encoding="utf-8"),
                }
            )
    if not docs:
        docs = EMBEDDED_RUNBOOKS

    target = Path(index_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(docs, indent=2), encoding="utf-8")
    return target


def retrieve(
    query: str,
    index_path: Path | str = DEFAULT_INDEX,
    limit: int = 3,
) -> list[dict[str, Any]]:
    target = Path(index_path)
    if not target.exists():
        build_index(index_path=target)
    docs = json.loads(target.read_text(encoding="utf-8"))
    query_terms = set(_terms(query))
    scored = []
    for doc in docs:
        haystack = " ".join([str(doc.get("title", "")), str(doc.get("text", ""))])
        score = len(query_terms & set(_terms(haystack)))
        scored.append({**doc, "score": score})
    return sorted(scored, key=lambda item: (-item["score"], str(item["id"])))[:limit]


def _terms(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())
