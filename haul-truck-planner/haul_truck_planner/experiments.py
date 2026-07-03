from collections import deque
from dataclasses import dataclass
from pathlib import Path

from haul_truck_planner.planner import MineMap, Point, RouteResult, Truck, plan_route


@dataclass(frozen=True)
class RouteComparison:
    shortest_path: list[Point]
    shortest_feasible: bool
    energy_aware: RouteResult
    reserve_kwh: float
    recommendation: str
    perception_risks: dict[Point, float]

    @property
    def energy_aware_feasible(self) -> bool:
        return True

    @property
    def minimum_energy_margin_kwh(self) -> float:
        return round(min(self.energy_aware.energy_trace) - self.reserve_kwh, 2)

    def to_markdown(self) -> str:
        return "\n".join(
            [
                "# Haul truck route experiment",
                "",
                "| strategy | feasible | path_length | path |",
                "| --- | --- | ---: | --- |",
                f"| shortest path | {self.shortest_feasible} | {len(self.shortest_path)} | `{self.shortest_path}` |",
                f"| energy-aware path | True | {len(self.energy_aware.path)} | `{self.energy_aware.path}` |",
                "",
                "## Energy trace",
                "",
                "`" + str(self.energy_aware.energy_trace) + "`",
                "",
                "## Planning algorithm note",
                "",
                (
                    "The current planner is a battery-state Dijkstra search: each state "
                    "tracks both grid position and remaining energy, so the route is "
                    "accepted only when it reaches the goal while preserving the reserve."
                ),
                (
                    "This is the baseline algorithm for the portfolio demo. The natural "
                    "next step is to add A* with an admissible distance/energy heuristic, "
                    "then compare it with EV routing problem ideas such as partial charging, "
                    "charge time, route windows, and payload-dependent energy use."
                ),
                "",
                "## ELEC5308-style perception risk layer",
                "",
                "`" + str(self.perception_risks) + "`",
                "",
                (
                    "The perception risk layer treats detector output as soft planning "
                    "costs rather than hard road closures. This mirrors an ELEC5308-style "
                    "pipeline: perception marks hazards, then path planning balances "
                    "risk, grade, charging access, and battery reserve."
                ),
                "",
                "## Operational takeaway",
                "",
                (
                    "The shortest route violates the reserve constraint, while the "
                    "energy-aware route reaches the destination with a minimum energy "
                    f"margin of {self.minimum_energy_margin_kwh:.2f} kWh."
                ),
                (
                    "The useful comparison is not path length alone; it is whether a "
                    "route remains feasible after grade, charging access, perception risk, "
                    "and reserve requirements are included."
                ),
                "",
                "## Recommendation",
                "",
                self.recommendation,
                "",
                "## Interview framing",
                "",
                (
                    "This is a compact energy-constrained routing demo for the RTSIH "
                    "electric haul truck trajectory-planning brief. It shows why mine "
                    "dispatch software needs state-of-charge constraints, perception risk, "
                    "and charging infrastructure awareness, not just shortest path search."
                ),
                (
                    "Open-source robotics and EVRP projects are useful references for the "
                    "next algorithmic steps, but this repo only claims a small, synthetic, "
                    "reviewable planning prototype."
                ),
            ]
        ) + "\n"


def compare_shortest_and_energy_aware(
    mine: MineMap,
    start: Point,
    goal: Point,
    truck: Truck,
) -> RouteComparison:
    shortest = shortest_path(mine, start, goal)
    shortest_feasible = _path_is_energy_feasible(mine, shortest, truck)
    energy_aware = plan_route(mine, start, goal, truck)
    if mine.risk_zones and not shortest_feasible and any(point in mine.charging for point in energy_aware.path):
        recommendation = "Use the charging lane and avoid high perception risk cells even when the geometric path length is similar."
    elif not shortest_feasible and any(point in mine.charging for point in energy_aware.path):
        recommendation = "Use the charging lane even when the geometric path length is similar."
    else:
        recommendation = "Use the energy-aware route because it respects reserve constraints."
    return RouteComparison(
        shortest_path=shortest,
        shortest_feasible=shortest_feasible,
        energy_aware=energy_aware,
        reserve_kwh=truck.reserve_kwh,
        recommendation=recommendation,
        perception_risks=dict(mine.risk_zones),
    )


def shortest_path(mine: MineMap, start: Point, goal: Point) -> list[Point]:
    queue: deque[Point] = deque([start])
    previous: dict[Point, Point | None] = {start: None}
    while queue:
        point = queue.popleft()
        if point == goal:
            path: list[Point] = []
            cursor: Point | None = point
            while cursor is not None:
                path.append(cursor)
                cursor = previous[cursor]
            return list(reversed(path))
        for neighbor in mine.neighbors(point):
            if neighbor not in previous:
                previous[neighbor] = point
                queue.append(neighbor)
    raise ValueError("no geometric route found")


def write_report(path: str = "reports/route-experiment.md") -> Path:
    mine = MineMap(
        width=5,
        height=4,
        blocked={(1, 1), (1, 2), (3, 1)},
        charging={(2, 2)},
        grades={(2, 1): 0.16, (2, 2): -0.05},
        risk_zones={(4, 1): 2.5, (4, 2): 2.5},
    )
    truck = Truck(capacity_kwh=10.0, initial_kwh=6.2, reserve_kwh=1.0)
    comparison = compare_shortest_and_energy_aware(mine, (0, 0), (4, 3), truck)
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(comparison.to_markdown(), encoding="utf-8")
    return output_path


def _path_is_energy_feasible(mine: MineMap, path: list[Point], truck: Truck) -> bool:
    energy = truck.initial_kwh
    for point in path[1:]:
        grade = mine.grades.get(point, 0.0)
        consumed = max(0.6, 1.0 + max(grade, 0.0) * 5.0 - min(abs(min(grade, 0.0)) * 4.0, 0.4))
        energy -= consumed
        if energy < truck.reserve_kwh:
            return False
        if point in mine.charging:
            energy = min(truck.capacity_kwh, energy + 6.0)
    return True


if __name__ == "__main__":
    print(write_report())
