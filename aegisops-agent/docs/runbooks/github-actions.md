# GitHub Actions Environment Variables

Symptoms:

- CI fails before tests execute meaningful assertions.
- Logs show an empty or invalid environment setting.

Fix pattern:

- Set safe explicit defaults in CI env configuration.
- Avoid patching the workflow itself in the agent preview.
