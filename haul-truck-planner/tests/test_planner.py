import unittest

from haul_truck_planner.experiments import compare_shortest_and_energy_aware
from haul_truck_planner.planner import MineMap, Truck, plan_route


class HaulTruckPlannerTests(unittest.TestCase):
    def test_plans_route_that_uses_charging_lane_when_energy_is_tight(self):
        mine = MineMap(
            width=5,
            height=4,
            blocked={(1, 1), (1, 2), (3, 1)},
            charging={(2, 2)},
            grades={(2, 1): 0.16, (2, 2): -0.05},
        )
        truck = Truck(capacity_kwh=10.0, initial_kwh=6.2, reserve_kwh=1.0)

        result = plan_route(mine, start=(0, 0), goal=(4, 3), truck=truck)

        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (4, 3))
        self.assertIn((2, 2), result.path)
        self.assertGreaterEqual(min(result.energy_trace), truck.reserve_kwh)

    def test_reports_no_route_when_reserve_cannot_be_maintained(self):
        mine = MineMap(width=3, height=1, blocked=set(), charging=set(), grades={})
        truck = Truck(capacity_kwh=3.0, initial_kwh=1.4, reserve_kwh=1.0)

        with self.assertRaises(ValueError):
            plan_route(mine, start=(0, 0), goal=(2, 0), truck=truck)

    def test_perception_risk_penalty_changes_route_without_blocking_cells(self):
        mine = MineMap(
            width=4,
            height=3,
            blocked=set(),
            charging=set(),
            grades={},
            risk_zones={(1, 1): 4.0, (2, 1): 4.0},
        )
        truck = Truck(capacity_kwh=10.0, initial_kwh=9.0, reserve_kwh=1.0)

        result = plan_route(mine, start=(0, 1), goal=(3, 1), truck=truck)

        self.assertEqual(result.path[0], (0, 1))
        self.assertEqual(result.path[-1], (3, 1))
        self.assertNotIn((1, 1), result.path)
        self.assertNotIn((2, 1), result.path)
        self.assertGreater(len(result.path), 4)

    def test_experiment_compares_shortest_path_with_energy_aware_path(self):
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

        self.assertFalse(comparison.shortest_feasible)
        self.assertTrue(comparison.energy_aware_feasible)
        self.assertIn("charging lane", comparison.recommendation)
        markdown = comparison.to_markdown()
        self.assertIn("| shortest path |", markdown)
        self.assertIn("## Operational takeaway", markdown)
        self.assertIn("shortest route violates the reserve constraint", markdown)
        self.assertIn("minimum energy margin", markdown)
        self.assertIn("## Interview framing", markdown)
        self.assertIn("energy-constrained routing", markdown)
        self.assertIn("ELEC5308-style", markdown)
        self.assertIn("RTSIH electric haul truck", markdown)
        self.assertIn("perception risk", markdown)


if __name__ == "__main__":
    unittest.main()
