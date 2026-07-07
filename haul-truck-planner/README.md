# Haul Truck Planner

Preparation project for `RTSIH - Opt-OO - Trajectory planning for electric haul trucks.pdf`.

## Brief fit

The official brief focuses on electric haul truck route selection, energy-efficient driving, recharge/refuel logistics, renewable variability, operational impact, algorithm design, mathematical methods, and computational experiments.

This local project implements a small energy-aware route planner:

- Grid-based mine map with blocked cells, grades, and charging lanes.
- ELEC5308-style perception risk layer, where detected hazards become soft route costs.
- Battery-state Dijkstra planner over position and remaining energy.
- A* energy-aware planner using the same transition model and a conservative distance lower bound.
- Battery reserve constraint so infeasible routes are rejected.
- Demo route where the truck must use a charging lane to reach the destination.

## Run

```bash
python3 -m unittest discover -s tests -v
python3 -m haul_truck_planner.demo
make report
```

## Portfolio talking points

- Bridges EE, robotics/control, software, and optimisation.
- Maps cleanly to the RTSIH electric haul truck trajectory-planning brief while reusing ELEC5308-style perception + planning language.
- Easy to extend into richer EV routing constraints, time windows, stochastic renewable charging, fleet dispatch, and charging queue simulation.
- Gives a visual story: map -> constraints -> feasible route -> energy trace.
- `make report` writes `reports/route-experiment.md`, comparing geometric shortest path, battery-state Dijkstra, and A* energy-aware planning.
- Algorithm comparison notes are in [`docs/algorithm-comparison.md`](docs/algorithm-comparison.md) and `reports/algorithm-comparison.md`.
- Sensitivity analysis is in `reports/sensitivity-lab.md`, showing how reserve, charging, and risk assumptions change feasibility and route choice.
- Current claim is a small synthetic planning prototype, not a production mine dispatch optimizer.
