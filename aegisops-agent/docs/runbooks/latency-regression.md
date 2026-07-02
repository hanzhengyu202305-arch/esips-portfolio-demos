# Latency Regression

Symptoms:

- p95 latency increases after an aggregation change.
- Code repeats the same lookup inside a nested loop.

Fix pattern:

- Precompute totals by key.
- Replace O(n^2) loops with a single pass and indexed lookup.
