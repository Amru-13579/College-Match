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


def meets_test_score_requirements(school: dict, user: dict) -> bool:
    """
    SAT and ACT are alternative standardized-test pathways.
    If both minimums are set, a school should qualify if it can satisfy either one.
    """
    min_sat = user.get("min_sat")
    min_act = user.get("min_act")

    if min_sat is None and min_act is None:
        return True

    sat_avg = school.get("sat_avg")
    act_mid = school.get("act_mid")

    sat_ok = min_sat is not None and sat_avg is not None and sat_avg >= min_sat
    act_ok = min_act is not None and act_mid is not None and act_mid >= min_act

    if min_sat is not None and min_act is not None:
        return sat_ok or act_ok
    if min_sat is not None:
        return sat_ok
    return act_ok


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))


def infer_school_type(school: dict) -> str:
    """
    Best-effort school type classification from the fields currently indexed.
    If a degree-level field is added later, this helper can prefer that instead.
    """
    name = (school.get("name") or "").strip().lower()
    predominant_degree = school.get("predominant_degree")
    tuition = school.get("tuition_in")
    ownership = school.get("ownership")

    if predominant_degree is not None:
        if predominant_degree >= 3:
            return "four_year"
        return "sub_bachelor"

    explicit_two_year_patterns = (
        "community college",
        "junior college",
    )
    if any(pattern in name for pattern in explicit_two_year_patterns):
        return "sub_bachelor"

    # Fallback heuristic: public, low-tuition schools without "university" in the name
    # are usually community-college style options in this dataset.
    if (
        ownership == 1
        and tuition is not None
        and tuition <= 6000
        and "university" not in name
    ):
        return "sub_bachelor"

    return "four_year"


def compute_affordability_score(tuition: float, max_budget: float) -> float | None:
    """
    Returns 1.0 once tuition is comfortably under budget.
    This avoids over-rewarding ultra-cheap schools when the user can afford much more.
    """
    if tuition is None or max_budget is None or max_budget <= 0:
        return None

    comfortable_threshold = 0.6 * max_budget
    if tuition <= comfortable_threshold:
        return 1.0

    remaining_budget_band = max_budget - comfortable_threshold
    if remaining_budget_band <= 0:
        return 1.0 - clamp01(tuition / max_budget)

    return 1.0 - clamp01((tuition - comfortable_threshold) / remaining_budget_band)


def compute_school_type_fit(school: dict, user: dict) -> float:
    """
    Sub-bachelor schools are useful when budgets are tight, but become less likely
    to be the intended target as the user's budget rises.
    """
    max_budget = user.get("max_budget")
    school_type = infer_school_type(school)

    if max_budget is None or school_type != "sub_bachelor":
        return 1.0

    budget_slack = clamp01((max_budget - 12000) / 28000)
    return 1.0 - (0.65 * budget_slack)


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

    # Treat "comfortably affordable" as good enough instead of always rewarding the cheapest option.
    tuition_score = compute_affordability_score(tuition, max_budget)
    if tuition_score is None:
        return None
    distance_score = 1.0 - clamp01(dist / max_distance)
    school_type_fit = compute_school_type_fit(school, user)
    return (0.45 * tuition_score) + (0.40 * distance_score) + (0.15 * school_type_fit)


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

    tuition_score = compute_affordability_score(school.get("tuition_in"), user.get("max_budget"))
    if tuition_score is None:
        return None

    distance_score = 1.0 - clamp01(school["distance"] / user["max_distance"])
    school_type_fit = compute_school_type_fit(school, user)
    return (
        0.35 * tuition_score
        + 0.25 * distance_score
        + 0.15 * school_type_fit
        + 0.25 * climate_score
    )


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
