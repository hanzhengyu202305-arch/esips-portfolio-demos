import tempfile
import unittest
from pathlib import Path

from haul_truck_planner.experiments import compare_shortest_and_energy_aware, render_sensitivity_lab, run_sensitivity_lab, write_report
from haul_truck_planner.planner import MineMap, Truck, plan_route, plan_route_astar


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
        self.assertGreater(result.expanded_states, 0)

    def test_astar_reaches_goal_with_reserve_under_same_constraints(self):
        mine = MineMap(
            width=5,
            height=4,
            blocked={(1, 1), (1, 2), (3, 1)},
            charging={(2, 2)},
            grades={(2, 1): 0.16, (2, 2): -0.05},
            risk_zones={(4, 1): 2.5, (4, 2): 2.5},
        )
        truck = Truck(capacity_kwh=10.0, initial_kwh=6.2, reserve_kwh=1.0)

        result = plan_route_astar(mine, start=(0, 0), goal=(4, 3), truck=truck)

        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (4, 3))
        self.assertIn((2, 2), result.path)
        self.assertGreaterEqual(min(result.energy_trace), truck.reserve_kwh)
        self.assertGreater(result.expanded_states, 0)

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
        self.assertTrue(comparison.astar_feasible)
        self.assertLess(comparison.shortest_minimum_energy_margin_kwh, 0)
        self.assertGreaterEqual(comparison.astar_minimum_energy_margin_kwh, 0)
        self.assertTrue(comparison.dijkstra_uses_charging)
        self.assertTrue(comparison.astar_uses_charging)
        self.assertFalse(comparison.shortest_avoids_risk_cells)
        self.assertTrue(comparison.dijkstra_avoids_risk_cells)
        self.assertTrue(comparison.astar_avoids_risk_cells)
        self.assertIn("charging lane", comparison.recommendation)
        markdown = comparison.to_markdown()
        self.assertIn("| geometric shortest path |", markdown)
        self.assertIn("| battery-state Dijkstra |", markdown)
        self.assertIn("| A* energy-aware planner |", markdown)
        self.assertIn("expanded_states", markdown)
        self.assertIn("charging_used", markdown)
        self.assertIn("avoids_risk_cells", markdown)
        self.assertIn("## ASCII map", markdown)
        self.assertIn("S * * . .", markdown)
        self.assertIn("## Operational takeaway", markdown)
        self.assertIn("shortest route violates the reserve constraint", markdown)
        self.assertIn("minimum energy margin", markdown)
        self.assertIn("## Planning algorithm note", markdown)
        self.assertIn("battery-state Dijkstra", markdown)
        self.assertIn("A*", markdown)
        self.assertIn("EV routing problem", markdown)
        self.assertIn("## Interview framing", markdown)
        self.assertIn("energy-constrained routing", markdown)
        self.assertIn("ELEC5308-style", markdown)
        self.assertIn("RTSIH electric haul truck", markdown)
        self.assertIn("perception risk", markdown)

    def test_sensitivity_lab_surfaces_feasible_changed_and_infeasible_cases(self):
        outcomes = run_sensitivity_lab()
        by_name = {outcome.name: outcome for outcome in outcomes}

        self.assertEqual(set(by_name), {"baseline", "reserve raised", "charger offline", "south charger added", "risk-aware south detour"})
        self.assertTrue(by_name["baseline"].feasible)
        self.assertFalse(by_name["baseline"].path_changed)
        self.assertFalse(by_name["reserve raised"].feasible)
        self.assertFalse(by_name["charger offline"].feasible)
        self.assertTrue(by_name["south charger added"].feasible)
        self.assertTrue(by_name["south charger added"].path_changed)
        self.assertTrue(by_name["risk-aware south detour"].feasible)
        self.assertTrue(by_name["risk-aware south detour"].path_changed)
        self.assertGreater(
            by_name["south charger added"].minimum_energy_margin_kwh,
            by_name["baseline"].minimum_energy_margin_kwh,
        )

        markdown = render_sensitivity_lab(outcomes)
        self.assertIn("# Mine Route Sensitivity Lab", markdown)
        self.assertIn("Reserve thresholds can turn a route from feasible to infeasible", markdown)
        self.assertIn("Charging points are operational constraints", markdown)
        self.assertIn("not a production mine dispatch optimiser", markdown)

    def test_report_generation_writes_sensitivity_lab(self):
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "route-experiment.md"

            write_report(str(report_path))

            sensitivity_path = Path(tmp) / "sensitivity-lab.md"
            self.assertTrue(report_path.is_file())
            self.assertTrue((Path(tmp) / "algorithm-comparison.md").is_file())
            self.assertTrue(sensitivity_path.is_file())
            self.assertIn("Mine Route Sensitivity Lab", sensitivity_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
