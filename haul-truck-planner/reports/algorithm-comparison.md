# Haul Truck Planner algorithm comparison

This report compares geometric shortest path, battery-state Dijkstra, and A* energy-aware planning on the same synthetic mine map.

| strategy | feasible | min_energy_margin_kwh | expanded_states | charging_used | avoids_risk_cells | role |
| --- | --- | ---: | ---: | --- | --- | --- |
| geometric shortest path | False | -1.80 | n/a | False | False | baseline that violates reserve |
| battery-state Dijkstra | True | 1.40 | 37 | True | True | correctness baseline |
| A* energy-aware planner | True | 1.40 | 23 | True | True | experimental planner comparison |

## Heuristic Boundary

Dijkstra remains the correctness baseline. A* uses the same battery-state transition model and a conservative Manhattan-distance lower bound under this simplified cost model. It is included to show path-planning comparison, not production optimisation.

## Engineering Takeaway

The shortest path has a negative reserve margin. Both energy-aware planners use the charging lane, avoid the high perception-risk cells in this scenario, and reach the goal above reserve.
