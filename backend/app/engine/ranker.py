import math
from backend.app.engine.explain import explain


def distance(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (math.sin(dphi / 2) ** 2
         + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def score_school(school, user):
    tuition_score  = 1 - min(school["tuition_in"] / user["max_budget"], 1)
    distance_score = 1 - min(school["distance"]   / user["max_distance"], 1)
    return 0.6 * tuition_score + 0.4 * distance_score


def rank_schools(schools, user):
    for school in schools:
        if school["lat"] and school["lon"]:
            school["distance"] = distance(
                user["lat"], user["lon"], school["lat"], school["lon"]
            )
        else:
            school["distance"] = None

    filtered = []
    for s in schools:
        if (
            s["tuition_in"] is not None
            and s["distance"] is not None
            and s["tuition_in"] <= user["max_budget"]
            and s["distance"] <= user["max_distance"]
        ):
            s["score"] = score_school(s, user)
            s["explanation"] = explain(s, user)
            filtered.append(s)

    return sorted(filtered, key=lambda x: x["score"], reverse=True)