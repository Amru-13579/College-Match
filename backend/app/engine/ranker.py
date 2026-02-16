from backend.app.engine.features import compute_distance, compute_score, build_explanation


def rank_schools(schools, user):
    # Compute distances
    for school in schools:
        school["distance"] = compute_distance(school, user)

    # Hard filter: score to sort
    filtered = []
    for s in schools:
        if (
            s.get("tuition_in") is not None
            and s.get("distance") is not None
            and s["tuition_in"] <= user["max_budget"]
            and s["distance"] <= user["max_distance"]
        ):
            s["score"] = compute_score(s, user)
            if s["score"] is None:
                continue
            s["explanation"] = build_explanation(s)
            filtered.append(s)

    return sorted(filtered, key=lambda x: x["score"], reverse=True)