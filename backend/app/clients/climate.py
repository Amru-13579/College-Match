import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean
from threading import Lock

import requests

OPEN_METEO_CLIMATE_URL = "https://climate-api.open-meteo.com/v1/climate"
CACHE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "climate_cache.json")
CACHE_LOCK = Lock()
CLIMATE_MODEL = "EC_Earth3P_HR"
START_DATE = "2022-01-01"
END_DATE = "2024-12-31"
REQUEST_TIMEOUT = (2, 3)
SESSION = requests.Session()
MAX_CLIMATE_WORKERS = 8


def _cache_key(lat, lon):
    return f"{lat:.4f},{lon:.4f}"


def _load_cache():
    if not os.path.exists(CACHE_PATH):
        return {}

    try:
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2, sort_keys=True)


def fetch_climate_summary(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "models": CLIMATE_MODEL,
        "daily": "temperature_2m_mean,precipitation_sum",
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
    }

    try:
        response = SESSION.get(OPEN_METEO_CLIMATE_URL, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        return None

    daily = payload.get("daily") or {}
    temperatures = [value for value in daily.get("temperature_2m_mean", []) if value is not None]
    precipitation = [value for value in daily.get("precipitation_sum", []) if value is not None]

    if not temperatures or not precipitation:
        return None

    year_count = max(1, len(temperatures) / 365.0)
    avg_temp_f = mean(temperatures)
    annual_precip_in = sum(precipitation) / year_count

    summary = {
        "avg_temp_f": round(avg_temp_f, 1),
        "annual_precip_in": round(annual_precip_in, 1),
    }
    summary["label"] = describe_climate(summary)
    return summary


def get_climate_summary(lat, lon):
    if lat is None or lon is None:
        return None

    key = _cache_key(lat, lon)
    with CACHE_LOCK:
        cache = _load_cache()
        if key in cache:
            return cache[key]

    summary = fetch_climate_summary(lat, lon)
    if summary is None:
        return None

    with CACHE_LOCK:
        cache = _load_cache()
        cache[key] = summary
        _save_cache(cache)

    return summary


def populate_climate_for_schools(schools):
    pending = []
    with CACHE_LOCK:
        cache = _load_cache()
        for school in schools:
            lat = school.get("lat")
            lon = school.get("lon")
            if lat is None or lon is None:
                continue
            key = _cache_key(lat, lon)
            cached = cache.get(key)
            if cached is not None:
                school["climate"] = cached
            else:
                pending.append((school, key, lat, lon))

    if not pending:
        return

    updates = {}
    worker_count = min(MAX_CLIMATE_WORKERS, len(pending))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        future_map = {
            executor.submit(fetch_climate_summary, lat, lon): (school, key)
            for school, key, lat, lon in pending
        }
        for future in as_completed(future_map):
            school, key = future_map[future]
            try:
                summary = future.result()
            except Exception:
                summary = None
            if summary is not None:
                school["climate"] = summary
                updates[key] = summary

    if updates:
        with CACHE_LOCK:
            cache = _load_cache()
            cache.update(updates)
            _save_cache(cache)


def describe_climate(summary):
    avg_temp_f = summary["avg_temp_f"]
    annual_precip_in = summary["annual_precip_in"]

    if avg_temp_f >= 68:
        temp_label = "warm"
    elif avg_temp_f <= 52:
        temp_label = "cool"
    else:
        temp_label = "mild"

    if annual_precip_in >= 45:
        moisture_label = "rainy"
    elif annual_precip_in <= 20:
        moisture_label = "dry"
    else:
        moisture_label = "balanced"

    return f"{temp_label}, {moisture_label}"
