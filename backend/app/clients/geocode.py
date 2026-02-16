import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode(location):
    """Convert a location string (zip code, city/state) to (lat, lon)."""
    params = {
        "q": location,
        "format": "json",
        "limit": 1,
        "countrycodes": "us",
    }
    headers = {
        "User-Agent": "CollegeMatch/1.0"
    }

    try:
        resp = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=5)
        resp.raise_for_status()
    except requests.RequestException:
        return None

    results = resp.json()
    if not results:
        return None

    return float(results[0]["lat"]), float(results[0]["lon"])