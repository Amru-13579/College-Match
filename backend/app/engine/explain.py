LOCALE_MAP = {
    11: "large city", 12: "midsize city", 13: "small city",
    21: "large suburb", 22: "midsize suburb", 23: "small suburb",
    31: "small town", 32: "small town", 33: "remote town",
    41: "rural area", 42: "rural area", 43: "remote area",
}


def explain(school, user):
    """Generate a human-readable explanation for why a school was recommended."""
    reasons = []

    # Budget
    tuition = school.get("tuition_in")
    budget = user.get("max_budget")
    if tuition and budget:
        savings = budget - tuition
        pct = savings / budget * 100
        if pct >= 50:
            reasons.append(f"well within your budget at ${tuition:,} tuition (${savings:,.0f} under your limit)")
        elif pct >= 20:
            reasons.append(f"fits your budget at ${tuition:,} tuition")
        else:
            reasons.append(f"within your budget at ${tuition:,} tuition")

    # Distance
    dist = school.get("distance")
    if dist is not None:
        if dist < 25:
            reasons.append("very close to home")
        elif dist < 100:
            reasons.append(f"only {dist:.0f} miles from home")
        elif dist < 300:
            reasons.append(f"a manageable {dist:.0f} miles away")
        else:
            reasons.append(f"{dist:.0f} miles away")

    # Admission rate
    rate = school.get("admission_rate")
    if rate:
        if rate >= 0.7:
            reasons.append(f"has accessible admissions ({rate * 100:.0f}% acceptance rate)")
        elif rate >= 0.4:
            reasons.append(f"moderately selective ({rate * 100:.0f}% acceptance rate)")
        elif rate >= 0.2:
            reasons.append(f"selective ({rate * 100:.0f}% acceptance rate)")
        else:
            reasons.append(f"highly selective ({rate * 100:.0f}% acceptance rate)")

    # Size
    size = school.get("size")
    if size:
        if size < 2000:
            reasons.append("offers a small, close-knit campus")
        elif size < 10000:
            reasons.append("mid-sized campus community")
        else:
            reasons.append(f"large campus with {size:,} students")

    # Setting
    locale = school.get("locale")
    setting = LOCALE_MAP.get(locale)
    if setting:
        reasons.append(f"located in a {setting}")

    # Build sentence
    if not reasons:
        return "Meets your search criteria."

    return "This school is a good match: " + ", ".join(reasons) + "."