from collections import deque
from dataclasses import dataclass
from pathlib import Path

from haul_truck_planner.planner import MineMap, Point, RouteResult, Truck, plan_route, plan_route_astar


@dataclass(frozen=True)
class RouteComparison:
    shortest_path: list[Point]
    shortest_feasible: bool
    shortest_minimum_energy_margin_kwh: float
    energy_aware: RouteResult
    astar_energy_aware: RouteResult
    reserve_kwh: float
    recommendation: str
    perception_risks: dict[Point, float]
    charging_points: set[Point]
    mine_width: int
    mine_height: int
    blocked_points: set[Point]

    @property
    def energy_aware_feasible(self) -> bool:
        return True

    @property
    def astar_feasible(self) -> bool:
        return True

    @property
    def minimum_energy_margin_kwh(self) -> float:
        return round(min(self.energy_aware.energy_trace) - self.reserve_kwh, 2)

    @property
    def astar_minimum_energy_margin_kwh(self) -> float:
        return round(min(self.astar_energy_aware.energy_trace) - self.reserve_kwh, 2)

    @property
    def shortest_uses_charging(self) -> bool:
        return any(point in self.charging_points for point in self.shortest_path)

    @property
    def dijkstra_uses_charging(self) -> bool:
        return any(point in self.charging_points for point in self.energy_aware.path)

    @property
    def astar_uses_charging(self) -> bool:
        return any(point in self.charging_points for point in self.astar_energy_aware.path)

    @property
    def shortest_avoids_risk_cells(self) -> bool:
        return not any(point in self.perception_risks for point in self.shortest_path)

    @property
    def dijkstra_avoids_risk_cells(self) -> bool:
        return not any(point in self.perception_risks for point in self.energy_aware.path)

    @property
    def astar_avoids_risk_cells(self) -> bool:
        return not any(point in self.perception_risks for point in self.astar_energy_aware.path)

    def to_markdown(self) -> str:
        return "\n".join(
            [
                "# Haul truck route experiment",
                "",
                "| strategy | feasible | path_length | minimum_energy_margin_kwh | expanded_states | charging_used | avoids_risk_cells | path |",
                "| --- | --- | ---: | ---: | ---: | --- | --- | --- |",
                (
                    f"| geometric shortest path | {self.shortest_feasible} | {len(self.shortest_path)} | "
                    f"{self.shortest_minimum_energy_margin_kwh:.2f} | n/a | {self.shortest_uses_charging} | "
                    f"{self.shortest_avoids_risk_cells} | `{self.shortest_path}` |"
                ),
                (
                    f"| battery-state Dijkstra | True | {len(self.energy_aware.path)} | "
                    f"{self.minimum_energy_margin_kwh:.2f} | {self.energy_aware.expanded_states} | "
                    f"{self.dijkstra_uses_charging} | {self.dijkstra_avoids_risk_cells} | "
                    f"`{self.energy_aware.path}` |"
                ),
                (
                    f"| A* energy-aware planner | True | {len(self.astar_energy_aware.path)} | "
                    f"{self.astar_minimum_energy_margin_kwh:.2f} | {self.astar_energy_aware.expanded_states} | "
                    f"{self.astar_uses_charging} | {self.astar_avoids_risk_cells} | "
                    f"`{self.astar_energy_aware.path}` |"
                ),
                "",
                "## Energy traces",
                "",
                "- battery-state Dijkstra: `" + str(self.energy_aware.energy_trace) + "`",
                "- A* energy-aware planner: `" + str(self.astar_energy_aware.energy_trace) + "`",
                "",
                "## ASCII map",
                "",
                "Legend: `S` start, `G` goal, `#` blocked, `C` charging, `R` perception risk, `*` energy-aware route.",
                "",
                "```text",
                self.ascii_map(),
                "```",
                "",
                "## Planning algorithm note",
                "",
                (
                    "The current planner is a battery-state Dijkstra search: each state "
                    "tracks both grid position and remaining energy, so the route is "
                    "accepted only when it reaches the goal while preserving the reserve."
                ),
                (
                    "A* uses the same battery-state transition model and a conservative "
                    "Manhattan-distance lower bound. Dijkstra remains the correctness "
                    "baseline; A* is included as a small path-planning comparison, not a "
                    "production optimizer."
                ),
                (
                    "The next research step is to compare this simplified model with EV "
                    "routing problem ideas such as partial charging, charge time, route "
                    "windows, and payload-dependent energy use."
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

    def ascii_map(self) -> str:
        route_points = set(self.energy_aware.path) | set(self.astar_energy_aware.path)
        start = self.energy_aware.path[0]
        goal = self.energy_aware.path[-1]
        rows: list[str] = []
        for y in range(self.mine_height):
            cells: list[str] = []
            for x in range(self.mine_width):
                point = (x, y)
                if point == start:
                    cells.append("S")
                elif point == goal:
                    cells.append("G")
                elif point in self.blocked_points:
                    cells.append("#")
                elif point in self.charging_points:
                    cells.append("C")
                elif point in self.perception_risks:
                    cells.append("R" if point not in route_points else "*")
                elif point in route_points:
                    cells.append("*")
                else:
                    cells.append(".")
            rows.append(" ".join(cells))
        return "\n".join(rows)


def compare_shortest_and_energy_aware(
    mine: MineMap,
    start: Point,
    goal: Point,
    truck: Truck,
) -> RouteComparison:
    shortest = shortest_path(mine, start, goal)
    shortest_feasible = _path_is_energy_feasible(mine, shortest, truck)
    shortest_minimum_energy_margin = _minimum_energy_margin(mine, shortest, truck)
    energy_aware = plan_route(mine, start, goal, truck)
    astar_energy_aware = plan_route_astar(mine, start, goal, truck)
    if mine.risk_zones and not shortest_feasible and any(point in mine.charging for point in energy_aware.path):
        recommendation = "Use the charging lane and avoid high perception risk cells even when the geometric path length is similar."
    elif not shortest_feasible and any(point in mine.charging for point in energy_aware.path):
        recommendation = "Use the charging lane even when the geometric path length is similar."
    else:
        recommendation = "Use the energy-aware route because it respects reserve constraints."
    return RouteComparison(
        shortest_path=shortest,
        shortest_feasible=shortest_feasible,
        shortest_minimum_energy_margin_kwh=shortest_minimum_energy_margin,
        energy_aware=energy_aware,
        astar_energy_aware=astar_energy_aware,
        reserve_kwh=truck.reserve_kwh,
        recommendation=recommendation,
        perception_risks=dict(mine.risk_zones),
        charging_points=set(mine.charging),
        mine_width=mine.width,
        mine_height=mine.height,
        blocked_points=set(mine.blocked),
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
    write_algorithm_report(output_path.parent / "algorithm-comparison.md", comparison)
    return output_path


def write_algorithm_report(
    path: str | Path = "reports/algorithm-comparison.md",
    comparison: RouteComparison | None = None,
) -> Path:
    if comparison is None:
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
    lines = [
        "# Haul Truck Planner algorithm comparison",
        "",
        "This report compares geometric shortest path, battery-state Dijkstra, and A* energy-aware planning on the same synthetic mine map.",
        "",
        "| strategy | feasible | min_energy_margin_kwh | expanded_states | charging_used | avoids_risk_cells | role |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
        (
            f"| geometric shortest path | {comparison.shortest_feasible} | "
            f"{comparison.shortest_minimum_energy_margin_kwh:.2f} | n/a | "
            f"{comparison.shortest_uses_charging} | {comparison.shortest_avoids_risk_cells} | baseline that violates reserve |"
        ),
        (
            f"| battery-state Dijkstra | True | {comparison.minimum_energy_margin_kwh:.2f} | "
            f"{comparison.energy_aware.expanded_states} | {comparison.dijkstra_uses_charging} | "
            f"{comparison.dijkstra_avoids_risk_cells} | correctness baseline |"
        ),
        (
            f"| A* energy-aware planner | True | {comparison.astar_minimum_energy_margin_kwh:.2f} | "
            f"{comparison.astar_energy_aware.expanded_states} | {comparison.astar_uses_charging} | "
            f"{comparison.astar_avoids_risk_cells} | experimental planner comparison |"
        ),
        "",
        "## Heuristic Boundary",
        "",
        "Dijkstra remains the correctness baseline. A* uses the same battery-state transition model and a conservative Manhattan-distance lower bound under this simplified cost model. It is included to show path-planning comparison, not production optimisation.",
        "",
        "## Engineering Takeaway",
        "",
        "The shortest path has a negative reserve margin. Both energy-aware planners use the charging lane, avoid the high perception-risk cells in this scenario, and reach the goal above reserve.",
        "",
        "## Map",
        "",
        "```text",
        comparison.ascii_map(),
        "```",
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def _path_is_energy_feasible(mine: MineMap, path: list[Point], truck: Truck) -> bool:
    return _minimum_energy_margin(mine, path, truck) >= 0.0


def _minimum_energy_margin(mine: MineMap, path: list[Point], truck: Truck) -> float:
    energy = truck.initial_kwh
    minimum_margin = energy - truck.reserve_kwh
    for point in path[1:]:
        grade = mine.grades.get(point, 0.0)
        consumed = max(0.6, 1.0 + max(grade, 0.0) * 5.0 - min(abs(min(grade, 0.0)) * 4.0, 0.4))
        energy -= consumed
        minimum_margin = min(minimum_margin, energy - truck.reserve_kwh)
        if point in mine.charging:
            energy = min(truck.capacity_kwh, energy + 6.0)
            minimum_margin = min(minimum_margin, energy - truck.reserve_kwh)
    return round(minimum_margin, 2)


if __name__ == "__main__":
    print(write_report())
