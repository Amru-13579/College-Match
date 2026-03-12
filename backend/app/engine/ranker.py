from backend.app.clients.climate import populate_climate_for_schools
from backend.app.engine.features import compute_base_score, compute_distance, compute_score
from backend.app.engine.explain import explain

CLIMATE_ENRICH_LIMIT = 100


def rank_schools(schools, user):
    for school in schools:
        school["distance"] = compute_distance(school, user)

    filtered = []
    for s in schools:
        if (
            s.get("tuition_in") is not None
            and s.get("distance") is not None
            and s["tuition_in"] <= user["max_budget"]
            and s["distance"] <= user["max_distance"]
        ):
            s["base_score"] = compute_base_score(s, user)
            if s["base_score"] is None:
                continue
            filtered.append(s)

    climate_pref = user.get("climate_preference", "any")
    candidates = filtered
    if climate_pref != "any":
        candidates = sorted(filtered, key=lambda x: x["base_score"], reverse=True)[:CLIMATE_ENRICH_LIMIT]
        populate_climate_for_schools(candidates)

    for school in candidates:
        school["score"] = compute_score(school, user)
        school["explanation"] = explain(school, user)

    ranked = [school for school in candidates if school.get("score") is not None]
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
