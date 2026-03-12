import unittest
from unittest.mock import Mock, patch

import requests

from backend.app.clients.geocode import geocode


class GeocodeTests(unittest.TestCase):
    @patch("backend.app.clients.geocode.requests.get")
    def test_geocode_returns_coordinates_from_first_result(self, mock_get):
        response = Mock()
        response.json.return_value = [{"lat": "33.6405", "lon": "-117.8443"}]
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        coords = geocode("Irvine, CA")

        self.assertEqual(coords, (33.6405, -117.8443))
        mock_get.assert_called_once()

    @patch("backend.app.clients.geocode.requests.get")
    def test_geocode_returns_none_when_api_errors(self, mock_get):
        mock_get.side_effect = requests.RequestException("boom")

        coords = geocode("bad input")

        self.assertIsNone(coords)

    @patch("backend.app.clients.geocode.requests.get")
    def test_geocode_returns_none_when_no_results(self, mock_get):
        response = Mock()
        response.json.return_value = []
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        coords = geocode("missing")

        self.assertIsNone(coords)


if __name__ == "__main__":
    unittest.main()
