# Algorithm Comparison

The Haul Truck Planner compares three strategies on the same synthetic mine map:

| strategy | purpose |
| --- | --- |
| Geometric shortest path | Baseline that ignores battery reserve, charging, grade, and risk. |
| Battery-state Dijkstra | Correctness baseline over `(position, remaining energy)` states. |
| A* energy-aware planner | Experimental planner comparison using the same energy transitions plus a conservative distance lower bound. |

## External Anchors

The planning language is grounded in public robotics and routing references:

- PythonRobotics is a useful reference for inspectable grid-search and A* examples.
- Vehicle-routing references such as Google OR-Tools help frame future constraints: time windows, route costs, charging decisions, and operational constraints.
- Electric-vehicle routing projects show why state of charge and charging access are central constraints.

This repo only implements a compact synthetic experiment. It uses those references for vocabulary and roadmap direction, not for a production solver claim.

## Why Dijkstra Remains The Baseline

Charging access and battery reserve make the state space more complex than a simple shortest path. Dijkstra over battery state is easier to reason about and remains the correctness baseline in this demo.

## What A* Adds

A* uses the same feasibility rules as Dijkstra:

- The route cannot go below reserve.
- Charging cells refill energy up to capacity.
- Grade changes energy use.
- Perception-risk cells add soft planning cost.

The heuristic is intentionally conservative for the simplified grid. If this model expands into richer EV routing with charge time, queueing, payload, or stochastic renewable charging, the heuristic would need to be revisited.

## Report

Run:

```bash
make report
```

Read:

```text
reports/algorithm-comparison.md
reports/route-experiment.md
```

## Boundary

This is a compact planning prototype for interview evidence. It is not a production mine dispatch optimizer or full fleet simulator.
