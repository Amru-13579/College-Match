import os
import json
from backend.app.engine.ranker import rank_schools

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "schools.json")


def load_schools():
    """Load schools from local JSON index."""
    with open(DATA_PATH, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    user = {
        "lat": 33.64,
        "lon": -117.84,

        # existing filters
        "max_budget": 25000,
        "max_distance": 3000,

        # new filters
        "min_size": 2000,
        "max_size": 40000,
        "min_admission_rate": 0.4,
        "max_admission_rate": None,
        "min_sat": 1000,
        "min_act": 20,

        # climate preference
        "climate_preference": "any"
    }

    schools = load_schools()
    ranked = rank_schools(schools, user)

    for school in ranked[:5]:
        print(school["name"], school["score"], school["explanation"])