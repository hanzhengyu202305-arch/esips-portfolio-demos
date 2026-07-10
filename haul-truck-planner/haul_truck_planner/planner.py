from dataclasses import dataclass, field
from heapq import heappop, heappush
from math import inf, isfinite
from typing import Iterable


Point = tuple[int, int]


@dataclass(frozen=True)
class EnergyModel:
    base_kwh_per_cell: float = 1.0
    uphill_kwh_per_grade: float = 5.0
    downhill_kwh_credit_per_grade: float = 4.0
    max_regen_credit_kwh: float = 0.4
    minimum_step_kwh: float = 0.6
    charge_gain_kwh: float = 6.0
    risk_weight: float = 1.0
    energy_quantum_kwh: float = 0.1


@dataclass(frozen=True)
class MineMap:
    width: int
    height: int
    blocked: set[Point]
    charging: set[Point]
    grades: dict[Point, float]
    risk_zones: dict[Point, float] = field(default_factory=dict)
    energy_model: EnergyModel = field(default_factory=EnergyModel)

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
    expanded_states: int = 0


def plan_route(mine: MineMap, start: Point, goal: Point, truck: Truck) -> RouteResult:
    """Plan an energy-feasible route using Dijkstra over position and battery state."""
    validate_problem(mine, start, goal, truck)
    start_energy = _quantize_energy(truck.initial_kwh, mine.energy_model.energy_quantum_kwh)
    queue: list[tuple[float, Point, float]] = [(0.0, start, start_energy)]
    best: dict[tuple[Point, float], float] = {(start, start_energy): 0.0}
    previous: dict[tuple[Point, float], tuple[Point, float] | None] = {(start, start_energy): None}
    expanded_states = 0

    while queue:
        cost, point, energy = heappop(queue)
        state = (point, energy)
        if cost > best.get(state, inf):
            continue
        expanded_states += 1
        if point == goal:
            return _reconstruct(previous, state, truck.initial_kwh, mine, expanded_states)

        for next_point in mine.neighbors(point):
            consumed = energy_cost(mine, next_point)
            next_energy = energy - consumed
            if next_energy < truck.reserve_kwh:
                continue
            if next_point in mine.charging:
                next_energy = min(
                    truck.capacity_kwh,
                    next_energy + mine.energy_model.charge_gain_kwh,
                )
            next_energy = _quantize_energy(next_energy, mine.energy_model.energy_quantum_kwh)
            next_cost = cost + _planning_cost(mine, next_point)
            next_state = (next_point, next_energy)
            if next_cost < best.get(next_state, inf):
                best[next_state] = next_cost
                previous[next_state] = state
                heappush(queue, (next_cost, next_point, next_energy))

    raise ValueError("no energy-feasible route found")


def plan_route_astar(mine: MineMap, start: Point, goal: Point, truck: Truck) -> RouteResult:
    """Plan an energy-feasible route using A* over position and battery state."""
    validate_problem(mine, start, goal, truck)
    start_energy = _quantize_energy(truck.initial_kwh, mine.energy_model.energy_quantum_kwh)
    queue: list[tuple[float, float, Point, float]] = [
        (_heuristic(mine, start, goal), 0.0, start, start_energy)
    ]
    best: dict[tuple[Point, float], float] = {(start, start_energy): 0.0}
    previous: dict[tuple[Point, float], tuple[Point, float] | None] = {(start, start_energy): None}
    expanded_states = 0

    while queue:
        _priority, cost, point, energy = heappop(queue)
        state = (point, energy)
        if cost > best.get(state, inf):
            continue
        expanded_states += 1
        if point == goal:
            return _reconstruct(previous, state, truck.initial_kwh, mine, expanded_states)

        for next_point in mine.neighbors(point):
            consumed = energy_cost(mine, next_point)
            next_energy = energy - consumed
            if next_energy < truck.reserve_kwh:
                continue
            if next_point in mine.charging:
                next_energy = min(
                    truck.capacity_kwh,
                    next_energy + mine.energy_model.charge_gain_kwh,
                )
            next_energy = _quantize_energy(next_energy, mine.energy_model.energy_quantum_kwh)
            next_cost = cost + _planning_cost(mine, next_point)
            next_state = (next_point, next_energy)
            if next_cost < best.get(next_state, inf):
                best[next_state] = next_cost
                previous[next_state] = state
                priority = next_cost + _heuristic(mine, next_point, goal)
                heappush(queue, (priority, next_cost, next_point, next_energy))

    raise ValueError("no energy-feasible route found")


def energy_cost(mine: MineMap, point: Point) -> float:
    grade = mine.grades.get(point, 0.0)
    model = mine.energy_model
    uphill_penalty = max(grade, 0.0) * model.uphill_kwh_per_grade
    downhill_credit = min(
        abs(min(grade, 0.0)) * model.downhill_kwh_credit_per_grade,
        model.max_regen_credit_kwh,
    )
    return max(
        model.minimum_step_kwh,
        model.base_kwh_per_cell + uphill_penalty - downhill_credit,
    )


def _planning_cost(mine: MineMap, point: Point) -> float:
    risk_penalty = mine.risk_zones.get(point, 0.0) * mine.energy_model.risk_weight
    return energy_cost(mine, point) + risk_penalty


def _reconstruct(
    previous: dict[tuple[Point, float], tuple[Point, float] | None],
    end_state: tuple[Point, float],
    initial_kwh: float,
    mine: MineMap,
    expanded_states: int,
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
    return RouteResult(
        path=path,
        energy_trace=energy_trace,
        total_cost=round(total_cost, 2),
        expanded_states=expanded_states,
    )


def _heuristic(mine: MineMap, point: Point, goal: Point) -> float:
    distance = abs(point[0] - goal[0]) + abs(point[1] - goal[1])
    return distance * mine.energy_model.minimum_step_kwh


def validate_problem(mine: MineMap, start: Point, goal: Point, truck: Truck) -> None:
    if mine.width <= 0 or mine.height <= 0:
        raise ValueError("mine dimensions must be positive")
    for label, point in (("start", start), ("goal", goal)):
        if not _in_bounds(mine, point):
            raise ValueError(f"{label} point is outside the mine map")
        if point in mine.blocked:
            raise ValueError(f"{label} point cannot be blocked")

    point_sets = {
        "blocked": mine.blocked,
        "charging": mine.charging,
        "grade": set(mine.grades),
        "risk": set(mine.risk_zones),
    }
    for label, points in point_sets.items():
        if any(not _in_bounds(mine, point) for point in points):
            raise ValueError(f"{label} point is outside the mine map")
    if mine.blocked & mine.charging:
        raise ValueError("charging points cannot also be blocked")
    if any(not isfinite(value) for value in mine.grades.values()):
        raise ValueError("grade values must be finite")
    if any(not isfinite(value) or value < 0 for value in mine.risk_zones.values()):
        raise ValueError("risk values must be finite and non-negative")

    truck_values = (truck.capacity_kwh, truck.initial_kwh, truck.reserve_kwh)
    if any(not isfinite(value) for value in truck_values):
        raise ValueError("truck energy values must be finite")
    if truck.capacity_kwh <= 0:
        raise ValueError("truck capacity must be positive")
    if not 0 <= truck.reserve_kwh <= truck.initial_kwh <= truck.capacity_kwh:
        raise ValueError("truck energy must satisfy 0 <= reserve <= initial <= capacity")
    _validate_energy_model(mine.energy_model)


def _validate_energy_model(model: EnergyModel) -> None:
    values = (
        model.base_kwh_per_cell,
        model.uphill_kwh_per_grade,
        model.downhill_kwh_credit_per_grade,
        model.max_regen_credit_kwh,
        model.minimum_step_kwh,
        model.charge_gain_kwh,
        model.risk_weight,
        model.energy_quantum_kwh,
    )
    if any(not isfinite(value) for value in values):
        raise ValueError("energy model values must be finite")
    if model.base_kwh_per_cell <= 0 or model.minimum_step_kwh <= 0:
        raise ValueError("energy consumption values must be positive")
    if model.charge_gain_kwh <= 0 or model.energy_quantum_kwh <= 0:
        raise ValueError("charging and quantization values must be positive")
    if any(value < 0 for value in values[1:4]) or model.risk_weight < 0:
        raise ValueError("energy penalties and risk weight must be non-negative")


def _in_bounds(mine: MineMap, point: Point) -> bool:
    x, y = point
    return 0 <= x < mine.width and 0 <= y < mine.height


def _quantize_energy(energy: float, quantum: float) -> float:
    return round(round(energy / quantum) * quantum, 8)
