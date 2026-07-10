# Portfolio Adversarial Review

Overall status: **PASS**

Challenges passed: **12/12**

The suite attacks assumptions behind the three demos instead of only replaying happy paths.

| id | project | attack | expected | observed | result | evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AEG-01 | AegisOps | tamper fixture gold label | infer invalid_app_mode_env from evidence | invalid_app_mode_env | PASS | diagnosis is independent of ScenarioSpec.root_cause_id |
| AEG-02 | AegisOps | remove all diagnostic evidence | ESCALATE | ESCALATE | PASS | insufficient independent evidence matches |
| AEG-03 | AegisOps | inject equally supported conflicting causes | ESCALATE | ESCALATE | PASS | conflicting hypotheses require human review |
| AEG-04 | AegisOps | force an escalation decision before remediation | no patch and no validation commands | patch_applied=False, commands=0 | PASS | agent flow stops before patch preview and validation |
| KUBE-01 | Kube Copilot | safe baseline | PASS | PASS | PASS | no blocking findings |
| KUBE-02 | Kube Copilot | comment spoof | FAIL | FAIL | PASS | image tag must not be latest; cpu request is required; memory request is required |
| KUBE-03 | Kube Copilot | unsafe sidecar | FAIL | FAIL | PASS | image tag must not be latest; cpu request is required; memory request is required |
| KUBE-04 | Kube Copilot | unsafe second document | FAIL | FAIL | PASS | host namespaces are not allowed; hostPath volumes are not allowed; image tag must not be latest |
| HAUL-01 | Haul Truck Planner | compare A* against Dijkstra correctness baseline | same optimal cost (7.6) | A* cost 7.6 | PASS | expanded states: Dijkstra=37, A*=23 |
| HAUL-02 | Haul Truck Planner | initial energy exceeds battery capacity | reject input | truck energy must satisfy 0 <= reserve <= initial <= capacity | PASS | battery-state invariant |
| HAUL-03 | Haul Truck Planner | charging point overlaps blocked road | reject input | charging points cannot also be blocked | PASS | map topology invariant |
| HAUL-04 | Haul Truck Planner | raise per-cell energy consumption above available margin | no feasible route | no energy-feasible route found | PASS | explicit EnergyModel sensitivity |

## First-Principles Interpretation

- AegisOps must derive a diagnosis from evidence and abstain when evidence is missing or contradictory.
- Kube Copilot must inspect parsed structure across documents and containers, not trust matching words.
- Haul Truck Planner must reject impossible states and keep A* consistent with the Dijkstra baseline.

## Boundary

These deterministic negative controls test portfolio failure handling. They do not prove production robustness or formal security assurance.
