# main.py

import os
import requests
from dotenv import load_dotenv
from backend.app.engine.ranker import rank_schools

load_dotenv()

API_KEY = os.getenv("COLLEGE_API_KEY")
URL = "https://api.data.gov/ed/collegescorecard/v1/schools"


def get_schools(per_page=100):
    """Fetch raw school data from College Scorecard API."""
    params = {
        "api_key": API_KEY,
        "fields": "school.name,latest.cost.tuition.in_state,school.city,school.state,location.lat,location.lon",
        "per_page": per_page
    }
    response = requests.get(URL, params=params)
    data = response.json()
    return data.get("results", [])


if __name__ == "__main__":
    # Example user input for testing
    user = {
        "lat": 33.64,          # Irvine
        "lon": -117.84,
        "max_budget": 25000,
        "max_distance": 3000
    }

    raw_schools = get_schools()
    ranked = rank_schools(raw_schools, user)

    # Top 5 results
    top_results = ranked[:5]
    for school in top_results:
        print(school["name"], school["score"], school["explanation"])
