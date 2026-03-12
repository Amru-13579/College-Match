import unittest
from unittest.mock import patch

try:
    from frontend.app import app
    FLASK_AVAILABLE = True
except ModuleNotFoundError:
    app = None
    FLASK_AVAILABLE = False


@unittest.skipUnless(FLASK_AVAILABLE, "Flask is not installed in this environment")
class RouteTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret"
        self.client = app.test_client()

    def test_home_get_renders_search_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CollegeMatch", response.data)

    @patch("frontend.app.geocode", return_value=(33.6405, -117.8443))
    def test_home_post_redirects_to_results_on_valid_input(self, mock_geocode):
        response = self.client.post(
            "/",
            data={
                "location": "Irvine, CA",
                "max_budget": "25000",
                "max_distance": "500",
                "climate_preference": "warm",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/results")
        mock_geocode.assert_called_once_with("Irvine, CA")

    @patch("frontend.app.geocode", return_value=None)
    def test_home_post_renders_error_when_geocode_fails(self, mock_geocode):
        response = self.client.post(
            "/",
            data={
                "location": "Unknown",
                "max_budget": "25000",
                "max_distance": "500",
                "climate_preference": "warm",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Could not find location", response.data)
        mock_geocode.assert_called_once_with("Unknown")

    def test_results_redirects_home_without_session(self):
        response = self.client.get("/results")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")

    @patch("frontend.app.rank_schools")
    @patch("frontend.app.load_schools")
    def test_results_renders_ranked_schools_with_session(self, mock_load_schools, mock_rank_schools):
        mock_load_schools.return_value = [{"name": "Test University"}]
        mock_rank_schools.return_value = [
            {
                "name": "Test University",
                "city": "Irvine",
                "state": "CA",
                "tuition_in": 12000,
                "distance": 20,
                "score": 0.85,
                "explanation": "Strong match.",
            }
        ]

        with self.client.session_transaction() as session:
            session["user"] = {
                "lat": 33.6405,
                "lon": -117.8443,
                "max_budget": 25000.0,
                "max_distance": 500.0,
                "climate_preference": "warm",
            }

        response = self.client.get("/results")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test University", response.data)
        mock_load_schools.assert_called_once()
        mock_rank_schools.assert_called_once()


if __name__ == "__main__":
    unittest.main()
