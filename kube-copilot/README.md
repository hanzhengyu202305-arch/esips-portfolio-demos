# Kube Copilot

Preparation project for `Accenture_01 Kubernetes_DevOps.pdf`.

## Brief fit

The official brief asks for a prototype or workflow recommendation engine that uses generative AI to automate Kubernetes-based CI/CD pipeline work, then assesses correctness, security, reliability, risk, and limits.

This local project keeps the LLM layer simulated and focuses on the engineering core:

- Generate a Dockerfile, Kubernetes Deployment, Kubernetes Service, GitHub Actions workflow, and validation checklist from structured deployment requirements.
- Validate generated infrastructure-as-code for pinned image tags, resource requests and limits, readiness and liveness probes, and CI presence.
- Produce a small report that separates machine-generated config from human review points.
- Export a small policy pack as `reports/policy-pack.json` and `reports/policy-pack.md` so the validation rules are reviewable as a reusable artifact.

The generated Kubernetes YAML now follows the shape of the official examples in `github-references/kubernetes-examples`: `Deployment` selectors match pod labels, `Service` defaults to `ClusterIP`, containers expose HTTP ports, and resource requests/limits plus readiness/liveness probes are explicit.

Policy rules are documented in [`docs/policy-rules.md`](docs/policy-rules.md). Static review fixtures live under `fixtures/safe/`, `fixtures/partial/`, and `fixtures/risky/`.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 -m kube_copilot.cli --out demo-output
make report
make policy-pack
```

## Portfolio talking points

- Shows Kubernetes, Docker, CI/CD, and IaC validation basics.
- Gives a concrete answer to "where is AI useful, and where do humans still need to review?"
- Can later be connected to a real LLM by replacing the structured generator with prompt/model output while keeping the same validator.
- `make report` writes `reports/risk-comparison.md` and `reports/policy-matrix.md`, showing safe, partial-remediation, and risky generated configs.
- `make policy-pack` writes `reports/policy-pack.json` and `reports/policy-pack.md`, turning the same rules into a compact reviewer artifact.
