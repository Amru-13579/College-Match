import math


def haversine_miles(lat1, lon1, lat2, lon2):
    """Great-circle distance between two points (miles). --> equation based on theory"""
    R = 3958.8
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


def compute_distance(school: dict, user: dict):
    """Returns distance in miles or None if missing coords."""
    if (
        user.get("lat") is None or user.get("lon") is None
        or school.get("lat") is None or school.get("lon") is None
    ):
        return None
    return haversine_miles(user["lat"], user["lon"], school["lat"], school["lon"])


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def compute_base_score(school: dict, user: dict, w_tuition=0.6, w_distance=0.4):
    """
    Weighted score in [0,1]. Returns None if missing inputs.
    Need to have the user's school['tuition_in'], school['distance'], user['max_budget'], user['max_distance'].
    """
    tuition = school.get("tuition_in")
    dist = school.get("distance")
    max_budget = user.get("max_budget")
    max_distance = user.get("max_distance")

    if tuition is None or dist is None or max_budget is None or max_distance is None:
        return None
    if max_budget <= 0 or max_distance <= 0:
        return None

    # Normalize tuition and distance to [0,1] where 1 is best.
    tuition_score = 1.0 - clamp01(tuition / max_budget)
    distance_score = 1.0 - clamp01(dist / max_distance)
    return (w_tuition * tuition_score) + (w_distance * distance_score)


def compute_climate_score(climate: dict, preference: str):
    if not climate or not preference or preference == "any":
        return None

    avg_temp_f = climate.get("avg_temp_f")
    annual_precip_in = climate.get("annual_precip_in")
    if avg_temp_f is None or annual_precip_in is None:
        return None

    if preference == "warm":
        return clamp01((avg_temp_f - 45) / 30)
    if preference == "cool":
        return clamp01((75 - avg_temp_f) / 30)
    if preference == "mild":
        return 1.0 - clamp01(abs(avg_temp_f - 62) / 15)
    if preference == "dry":
        return 1.0 - clamp01(annual_precip_in / 60)
    if preference == "rainy":
        return clamp01(annual_precip_in / 60)

    return None


def compute_score(school: dict, user: dict):
    base_score = compute_base_score(school, user)
    if base_score is None:
        return None

    climate_pref = user.get("climate_preference", "any")
    climate_score = compute_climate_score(school.get("climate"), climate_pref)
    if climate_pref == "any" or climate_score is None:
        return base_score

    return (0.45 * (1.0 - clamp01(school["tuition_in"] / user["max_budget"]))) + (
        0.30 * (1.0 - clamp01(school["distance"] / user["max_distance"]))
    ) + (0.25 * climate_score)


def build_explanation(school: dict):
    tuition = school.get("tuition_in")
    dist = school.get("distance")

    tuition_str = f"${tuition:,.0f}" if tuition is not None else "N/A"
    dist_str = f"{dist:.1f} miles away" if dist is not None else "Distance N/A"

    city = school.get("city")
    state = school.get("state")
    loc = ", ".join([p for p in [city, state] if p])
    if loc:
        return f"{tuition_str} tuition • {dist_str} • {loc}"
    return f"{tuition_str} tuition • {dist_str}"
