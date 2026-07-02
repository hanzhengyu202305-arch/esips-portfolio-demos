# Haul truck route experiment

| strategy | feasible | path_length | path |
| --- | --- | ---: | --- |
| shortest path | False | 8 | `[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (4, 1), (4, 2), (4, 3)]` |
| energy-aware path | True | 8 | `[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (3, 3), (4, 3)]` |

## Energy trace

`[6.2, 5.2, 4.2, 2.4, 7.6, 6.6, 5.6, 4.6]`

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
