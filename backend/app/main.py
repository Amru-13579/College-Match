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
        "max_budget": 25000,
        "max_distance": 3000,
    }

    schools = load_schools()
    ranked = rank_schools(schools, user)

    for school in ranked[:5]:
        print(school["name"], school["score"], school["explanation"])