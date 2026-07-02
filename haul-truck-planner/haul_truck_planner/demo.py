from haul_truck_planner.planner import MineMap, Truck, plan_route


def main() -> None:
    mine = MineMap(
        width=5,
        height=4,
        blocked={(1, 1), (1, 2), (3, 1)},
        charging={(2, 2)},
        grades={(2, 1): 0.16, (2, 2): -0.05},
        risk_zones={(4, 1): 2.5, (4, 2): 2.5},
    )
    truck = Truck(capacity_kwh=10.0, initial_kwh=6.2, reserve_kwh=1.0)
    result = plan_route(mine, start=(0, 0), goal=(4, 3), truck=truck)
    print("path:", result.path)
    print("energy_trace_kwh:", result.energy_trace)
    print("total_planning_cost:", result.total_cost)


if __name__ == "__main__":
    main()
