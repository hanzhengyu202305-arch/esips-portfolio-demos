# Docker Build Missing Dependencies

Symptoms:

- Image build fails with `ModuleNotFoundError`.
- The import works locally only when the developer environment has extra packages.

Fix pattern:

- Add the missing dependency to the image requirements file.
- Keep the patch scoped to packaging metadata.
- Rerun a docker dry-run or equivalent validation.
