# AegisOps Scenario Matrix

| scenario | category | root_cause_id | allowed_files | validation |
| --- | --- | --- | --- | --- |
| S1 | pytest | wrong_discount_logic | `apps/demo-api/app/service.py` | pytest |
| S2 | docker | missing_python_dependency | `apps/demo-api/requirements.txt`<br>`apps/demo-api/Dockerfile` | docker-dry-run |
| S3 | ci | missing_app_mode_env | `ci/env.example.yml` | ci-dry-run |
| S4 | kubernetes | invalid_app_mode_env | `k8s/overlays/broken-env/deployment.yaml` | k8s-dry-run |
| S5 | kubernetes | wrong_readiness_probe_path | `k8s/overlays/broken-probe/deployment.yaml` | k8s-dry-run |
| S6 | kubernetes | image_tag_mismatch | `k8s/overlays/healthy/kustomization.yaml` | k8s-dry-run |
| S7 | security | container_runs_as_root | `k8s/overlays/insecure/deployment.yaml` | security-dry-run |
| S8 | latency | nested_loop_latency_regression | `apps/demo-api/app/service.py` | latency-dry-run |
