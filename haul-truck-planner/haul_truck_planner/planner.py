from dataclasses import dataclass, field
from heapq import heappop, heappush
from math import inf
from typing import Iterable


Point = tuple[int, int]


@dataclass(frozen=True)
class MineMap:
    width: int
    height: int
    blocked: set[Point]
    charging: set[Point]
    grades: dict[Point, float]
    risk_zones: dict[Point, float] = field(default_factory=dict)

    def neighbors(self, point: Point) -> Iterable[Point]:
        x, y = point
        for candidate in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            cx, cy = candidate
            if 0 <= cx < self.width and 0 <= cy < self.height and candidate not in self.blocked:
                yield candidate


@dataclass(frozen=True)
class Truck:
    capacity_kwh: float
    initial_kwh: float
    reserve_kwh: float


@dataclass(frozen=True)
class RouteResult:
    path: list[Point]
    energy_trace: list[float]
    total_cost: float


def plan_route(mine: MineMap, start: Point, goal: Point, truck: Truck) -> RouteResult:
    """Plan an energy-feasible route using Dijkstra over position and battery state."""
    start_energy = round(truck.initial_kwh, 1)
    queue: list[tuple[float, Point, float]] = [(0.0, start, start_energy)]
    best: dict[tuple[Point, float], float] = {(start, start_energy): 0.0}
    previous: dict[tuple[Point, float], tuple[Point, float] | None] = {(start, start_energy): None}

    while queue:
        cost, point, energy = heappop(queue)
        state = (point, energy)
        if cost > best.get(state, inf):
            continue
        if point == goal:
            return _reconstruct(previous, state, truck.initial_kwh, mine)

        for next_point in mine.neighbors(point):
            consumed = _energy_cost(mine, next_point)
            next_energy = energy - consumed
            if next_energy < truck.reserve_kwh:
                continue
            if next_point in mine.charging:
                next_energy = min(truck.capacity_kwh, next_energy + 6.0)
            next_energy = round(next_energy, 1)
            next_cost = cost + _planning_cost(mine, next_point)
            next_state = (next_point, next_energy)
            if next_cost < best.get(next_state, inf):
                best[next_state] = next_cost
                previous[next_state] = state
                heappush(queue, (next_cost, next_point, next_energy))

    raise ValueError("no energy-feasible route found")


def _energy_cost(mine: MineMap, point: Point) -> float:
    grade = mine.grades.get(point, 0.0)
    uphill_penalty = max(grade, 0.0) * 5.0
    downhill_credit = min(abs(min(grade, 0.0)) * 4.0, 0.4)
    return max(0.6, 1.0 + uphill_penalty - downhill_credit)


def _planning_cost(mine: MineMap, point: Point) -> float:
    risk_penalty = max(0.0, mine.risk_zones.get(point, 0.0))
    return _energy_cost(mine, point) + risk_penalty


def _reconstruct(
    previous: dict[tuple[Point, float], tuple[Point, float] | None],
    end_state: tuple[Point, float],
    initial_kwh: float,
    mine: MineMap,
) -> RouteResult:
    states: list[tuple[Point, float]] = []
    state: tuple[Point, float] | None = end_state
    while state is not None:
        states.append(state)
        state = previous[state]
    states.reverse()

    path = [point for point, _energy in states]
    energy_trace = [round(energy, 2) for _point, energy in states]
    energy_trace[0] = round(initial_kwh, 2)
    total_cost = 0.0
    for point in path[1:]:
        total_cost += _planning_cost(mine, point)
    return RouteResult(path=path, energy_trace=energy_trace, total_cost=round(total_cost, 2))
