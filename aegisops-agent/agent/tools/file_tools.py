from __future__ import annotations

import difflib
from fnmatch import fnmatch
from pathlib import Path


class PatchSafetyError(RuntimeError):
    """Raised when a generated patch attempts to touch a disallowed path."""


def validate_patch_targets(
    files_changed: list[str],
    allowed_files: list[str],
    blocked_files: list[str],
) -> None:
    for path in files_changed:
        if any(fnmatch(path, pattern) for pattern in blocked_files):
            raise PatchSafetyError(f"Patch target is blocked: {path}")
        if not any(fnmatch(path, pattern) for pattern in allowed_files):
            raise PatchSafetyError(f"Patch target is not in allowed_files: {path}")


def generate_unified_diff(
    broken_files: dict[str, str],
    fixed_files: dict[str, str],
) -> str:
    chunks: list[str] = []
    for path in sorted(fixed_files):
        before = broken_files.get(path, "")
        after = fixed_files[path]
        chunks.extend(
            difflib.unified_diff(
                before.splitlines(keepends=True),
                after.splitlines(keepends=True),
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
            )
        )
    return "".join(chunks)


def write_patch_preview(
    run_dir: Path,
    broken_files: dict[str, str],
    fixed_files: dict[str, str],
    allowed_files: list[str],
    blocked_files: list[str],
) -> tuple[Path, Path, list[str]]:
    files_changed = sorted(fixed_files)
    validate_patch_targets(files_changed, allowed_files, blocked_files)

    run_dir.mkdir(parents=True, exist_ok=True)
    diff_text = generate_unified_diff(broken_files, fixed_files)
    diff_path = run_dir / "patch.diff"
    diff_path.write_text(diff_text, encoding="utf-8")

    patched_dir = run_dir / "patched"
    for relative_path, content in fixed_files.items():
        target = patched_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    return diff_path, patched_dir, files_changed
