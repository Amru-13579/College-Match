from backend.app.clients.climate import populate_climate_for_schools
from backend.app.data.majors import school_offers_major
from backend.app.engine.features import compute_base_score, compute_distance, compute_score, meets_test_score_requirements
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

            # school size filter
            and (user.get("min_size") is None or (s.get("size") is not None and s.get("size") >= user["min_size"]))
            and (user.get("max_size") is None or (s.get("size") is not None and s.get("size") <= user["max_size"]))

            # admission rate filter
            and (
                user.get("min_admission_rate") is None
                or (s.get("admission_rate") is not None and s.get("admission_rate") >= user["min_admission_rate"])
            )
            and (
                user.get("max_admission_rate") is None
                or (s.get("admission_rate") is not None and s.get("admission_rate") <= user["max_admission_rate"])
            )

            # standardized test filter
            and meets_test_score_requirements(s, user)

            # major filter
            and school_offers_major(s, user.get("major"))
        ):
            s["base_score"] = compute_base_score(s, user)
            if s["base_score"] is None:
                continue
            filtered.append(s)

    candidates = filtered
    climate_candidates = sorted(filtered, key=lambda x: x["base_score"], reverse=True)[:CLIMATE_ENRICH_LIMIT]
    populate_climate_for_schools(climate_candidates)

    for school in candidates:
        school["score"] = compute_score(school, user)
        school["explanation"] = explain(school, user)

    ranked = [school for school in candidates if school.get("score") is not None]
    return sorted(ranked, key=lambda x: x["score"], reverse=True)
