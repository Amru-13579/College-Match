import unittest

from backend.app.engine.features import (
    compute_base_score,
    compute_climate_score,
    compute_distance,
    compute_score,
    haversine_miles,
)


class FeatureTests(unittest.TestCase):
    def test_haversine_is_zero_for_same_point(self):
        self.assertEqual(haversine_miles(33.64, -117.84, 33.64, -117.84), 0)

    def test_haversine_matches_expected_irvine_to_los_angeles_distance(self):
        distance = haversine_miles(33.6846, -117.8265, 34.0522, -118.2437)
        self.assertAlmostEqual(distance, 35.4, delta=2.0)

    def test_compute_distance_uses_school_and_user_coordinates(self):
        school = {"lat": 34.0522, "lon": -118.2437}
        user = {"lat": 33.6846, "lon": -117.8265}

        distance = compute_distance(school, user)

        self.assertAlmostEqual(distance, 35.4, delta=2.0)

    def test_compute_base_score_rewards_lower_tuition_and_distance(self):
        school = {"tuition_in": 10000, "distance": 100}
        user = {"max_budget": 20000, "max_distance": 400}

        score = compute_base_score(school, user)

        self.assertAlmostEqual(score, 0.6, places=3)

    def test_compute_climate_score_prefers_warm_for_higher_average_temperature(self):
        climate = {"avg_temp_f": 72, "annual_precip_in": 12}

        score = compute_climate_score(climate, "warm")

        self.assertGreater(score, 0.8)

    def test_compute_score_includes_climate_when_preference_is_set(self):
        school = {
            "tuition_in": 10000,
            "distance": 100,
            "climate": {"avg_temp_f": 72, "annual_precip_in": 12},
        }
        user = {
            "max_budget": 20000,
            "max_distance": 400,
            "climate_preference": "warm",
        }

        score = compute_score(school, user)

        self.assertAlmostEqual(score, 0.675, places=3)


if __name__ == "__main__":
    unittest.main()
