from argparse import ArgumentParser
from pathlib import Path

from kube_copilot.generator import generate_workspace
from kube_copilot.validator import validate_workspace


def main() -> None:
    parser = ArgumentParser(description="Generate and validate a Kubernetes DevOps workspace.")
    parser.add_argument("--app-name", default="ore-api")
    parser.add_argument("--image", default="ghcr.io/example/ore-api:1.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--replicas", type=int, default=2)
    parser.add_argument("--cpu-limit", default="500m")
    parser.add_argument("--memory-limit", default="512Mi")
    parser.add_argument("--out", default="out")
    args = parser.parse_args()

    workspace = generate_workspace(
        app_name=args.app_name,
        image=args.image,
        port=args.port,
        replicas=args.replicas,
        cpu_limit=args.cpu_limit,
        memory_limit=args.memory_limit,
    )
    out_dir = Path(args.out)
    for relative_path, content in workspace.files.items():
        path = out_dir / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    report = validate_workspace(workspace)
    report_path = out_dir / "validation-report.md"
    report_path.write_text(report.to_markdown(), encoding="utf-8")
    print(f"Wrote {len(workspace.files)} files and {report_path}")


if __name__ == "__main__":
    main()

