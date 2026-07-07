# Mine Route Sensitivity Lab

This report extends the haul-truck planner from one route result into a small sensitivity analysis. It varies reserve, charging access, and perception-risk assumptions to show when the route remains feasible, changes path, or fails.

| scenario | feasible | path_changed | min_energy_margin_kwh | charging_used | route | takeaway |
| --- | --- | --- | ---: | --- | --- | --- |
| baseline | True | False | 1.40 | True | `[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 3), (4, 3)]` | route is feasible only because it uses the charging lane |
| reserve raised | False | n/a | n/a | n/a | n/a | the same mine map becomes infeasible under a stricter safety reserve |
| charger offline | False | n/a | n/a | n/a | n/a | charging infrastructure is a feasibility constraint, not a cosmetic route feature |
| south charger added | True | True | 3.20 | True | `[(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]` | extra charging access can change the preferred route and improve energy margin |
| risk-aware south detour | True | True | 3.20 | True | `[(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (2, 3), (3, 3), (4, 3)]` | the planner can choose a safer detour when charging alternatives exist |

## Scenario Changes

- **baseline**: default reserve, grade, charging, and perception-risk settings
- **reserve raised**: increase reserve from 1.0 kWh to 2.0 kWh
- **charger offline**: remove the only charging point from the map
- **south charger added**: add a second charging point on the south lane
- **risk-aware south detour**: raise perception risk on the middle charging lane while keeping a south charger available

## Engineering Takeaways

- Reserve thresholds can turn a route from feasible to infeasible without changing the map geometry.
- Charging points are operational constraints; removing one can remove all feasible routes.
- Adding a charger can change the selected path and improve the energy margin.
- Perception-risk costs are useful when there is a feasible alternative route.

## Boundary

This is a deterministic synthetic sensitivity lab. It supports engineering discussion about constraints and tradeoffs, but it is not a production mine dispatch optimiser.
