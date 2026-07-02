# Pytest Assertion Failures

Symptoms:

- A deterministic unit test fails with an unexpected value.
- The failure points to application logic rather than infrastructure.

Fix pattern:

- Compare expected and observed values.
- Patch the smallest implementation surface.
- Rerun pytest before preparing a PR summary.
