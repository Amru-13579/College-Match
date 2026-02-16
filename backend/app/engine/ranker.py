# ranker.py

import math


def normalize_school(raw):
    return {
        "name": raw.get("school.name"),
        "tuition": raw.get("latest.cost.tuition.in_state"),
        "city": raw.get("school.city"),
        "state": raw.get("school.state"),
        "lat": raw.get("location.lat"),
        "lon": raw.get("location.lon"),
    }


def distance(lat1, lon1, lat2, lon2):
    R = 3958.8  # miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def score_school(school, user):
    tuition_score = 1 - min(school["tuition"] / user["max_budget"], 1)
    distance_score = 1 - min(school["distance"] / user["max_distance"], 1)

    return 0.6 * tuition_score + 0.4 * distance_score


def rank_schools(raw_schools, user):
    schools = [normalize_school(s) for s in raw_schools]

    # Compute distance
    for school in schools:
        if school["lat"] and school["lon"]:
            school["distance"] = distance(
                user["lat"], user["lon"],
                school["lat"], school["lon"]
            )
        else:
            school["distance"] = None

    # Hard filtering
    filtered = []
    for s in schools:
        if (
            s["tuition"] is not None
            and s["distance"] is not None
            and s["tuition"] <= user["max_budget"]
            and s["distance"] <= user["max_distance"]
        ):
            s["score"] = score_school(s, user)
            s["explanation"] = (
                f"${s['tuition']} tuition • "
                f"{round(s['distance'],1)} miles away"
            )
            filtered.append(s)

    ranked = sorted(filtered, key=lambda x: x["score"], reverse=True)

    return ranked
