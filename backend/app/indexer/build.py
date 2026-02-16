import os
import json
import requests
from dotenv import load_dotenv
from backend.app.data.field_map import FIELD_MAP, API_FIELDS

load_dotenv()

API_KEY = os.getenv("COLLEGE_API_KEY")
URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "schools.json")


def normalize(raw):
    """Convert dot-notation API keys to clean keys."""
    school = {}
    for clean_key, api_key in FIELD_MAP.items():
        school[clean_key] = raw.get(api_key)
    return school


def fetch_all_schools():
    """Fetch every school from College Scorecard with pagination."""
    all_schools = []
    page = 0

    while True:
        params = {
            "api_key": API_KEY,
            "fields": API_FIELDS,
            "per_page": 100,
            "page": page,
        }

        print(f"Fetching page {page}...")
        resp = requests.get(URL, params=params)
        resp.raise_for_status()

        results = resp.json().get("results", [])
        if not results:
            break

        all_schools.extend(normalize(r) for r in results)
        page += 1

    return all_schools


def build():
    """Fetch all schools and write to local JSON."""
    schools = fetch_all_schools()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(schools, f, indent=2)

    print(f"Done — saved {len(schools)} schools to {OUTPUT_PATH}")


if __name__ == "__main__":
    build()