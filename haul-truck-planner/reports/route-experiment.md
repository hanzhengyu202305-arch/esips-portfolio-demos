# Haul truck route experiment

| strategy | feasible | path_length | minimum_energy_margin_kwh | expanded_states | charging_used | avoids_risk_cells | path |
| --- | --- | ---: | ---: | ---: | --- | --- | --- |
| geometric shortest path | False | 8 | -1.80 | n/a | False | False | `[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3)]` |
| battery-state Dijkstra | True | 8 | 1.40 | 37 | True | True | `[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 3), (4, 3)]` |
| A* energy-aware planner | True | 8 | 1.40 | 23 | True | True | `[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 3), (4, 3)]` |

## Energy traces

- battery-state Dijkstra: `[6.2, 5.2, 4.2, 2.4, 7.6, 6.6, 5.6, 4.6]`
- A* energy-aware planner: `[6.2, 5.2, 4.2, 2.4, 7.6, 6.6, 5.6, 4.6]`

## ASCII map

Legend: `S` start, `G` goal, `#` blocked, `C` charging, `R` perception risk, `*` energy-aware route.

```text
S * * . .
. # * # R
. # C . R
. . * * G
```

## Planning algorithm note

The current planner is a battery-state Dijkstra search: each state tracks both grid position and remaining energy, so the route is accepted only when it reaches the goal while preserving the reserve.
A* uses the same battery-state transition model and a conservative Manhattan-distance lower bound. Dijkstra remains the correctness baseline; A* is included as a small path-planning comparison, not a production optimizer.
The next research step is to compare this simplified model with EV routing problem ideas such as partial charging, charge time, route windows, and payload-dependent energy use.

## ELEC5308-style perception risk layer

`{(4, 1): 2.5, (4, 2): 2.5}`

The perception risk layer treats detector output as soft planning costs rather than hard road closures. This mirrors an ELEC5308-style pipeline: perception marks hazards, then path planning balances risk, grade, charging access, and battery reserve.

## Operational takeaway

The shortest route violates the reserve constraint, while the energy-aware route reaches the destination with a minimum energy margin of 1.40 kWh.
The useful comparison is not path length alone; it is whether a route remains feasible after grade, charging access, perception risk, and reserve requirements are included.

## Recommendation

Use the charging lane and avoid high perception risk cells even when the geometric path length is similar.

## Interview framing

This is a compact energy-constrained routing demo for the RTSIH electric haul truck trajectory-planning brief. It shows why mine dispatch software needs state-of-charge constraints, perception risk, and charging infrastructure awareness, not just shortest path search.
Open-source robotics and EVRP projects are useful references for the next algorithmic steps, but this repo only claims a small, synthetic, reviewable planning prototype.
