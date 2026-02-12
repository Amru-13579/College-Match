import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load backend/.env explicitly
load_dotenv(Path(__file__).resolve().parent / ".env")

API_KEY = os.getenv("SCORECARD_API_KEY")
if not API_KEY:
    raise RuntimeError("SCORECARD_API_KEY not found. Put it in backend/.env")

url = "https://api.data.gov/ed/collegescorecard/v1/schools"
params = {
    "api_key": API_KEY,
    "per_page": 1,
    "fields": "id,school.name",
}

r = requests.get(url, params=params, timeout=30)

print("Status:", r.status_code)
print("Response preview:", r.text[:300])

if r.status_code == 200:
    data = r.json()
    first = (data.get("results") or [{}])[0]
    print("Works! Key:", first.get("school.name"), "ID:", first.get("id"))
else:
    print("Key invalid")
