from flask import Flask, render_template, request, redirect, url_for, session
from backend.app.main import load_schools
from backend.app.data.majors import all_major_labels
from backend.app.engine.ranker import rank_schools
from backend.app.clients.geocode import geocode
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def parse_optional_int(value):
    value = (value or "").strip()
    return int(value) if value else None


def parse_optional_slider_min(value, floor):
    parsed = parse_optional_int(value)
    if parsed is None or parsed <= floor:
        return None
    return parsed


def parse_optional_percent(value):
    value = (value or "").strip()
    return float(value) / 100.0 if value else None


@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    major_options = all_major_labels()

    if request.method == "POST":
        location = request.form.get("location", "").strip()
        coords = geocode(location)

        if not coords:
            error = f"Could not find location: '{location}'"
            return render_template("index.html", error=error, form=request.form)

        lat, lon = coords
        climate_preference = request.form.get("climate_preference", "any")
        major = request.form.get("major", "").strip()
        session["user"] = {
            "lat": lat,
            "lon": lon,
            "max_budget": float(request.form["max_budget"]),
            "max_distance": float(request.form["max_distance"]),
            "min_size": parse_optional_int(request.form.get("min_size")),
            "max_size": parse_optional_int(request.form.get("max_size")),
            "min_admission_rate": parse_optional_percent(request.form.get("min_admission_rate")),
            "max_admission_rate": None,
            "min_sat": parse_optional_slider_min(request.form.get("min_sat"), 400),
            "min_act": parse_optional_slider_min(request.form.get("min_act"), 1),
            "major": major or None,
            "climate_preference": climate_preference,
        }
        session["form"] = {
            "location": location,
            "max_budget": request.form["max_budget"],
            "max_distance": request.form["max_distance"],
            "min_size": request.form.get("min_size", ""),
            "max_size": request.form.get("max_size", ""),
            "min_admission_rate": request.form.get("min_admission_rate", ""),
            "min_sat": request.form.get("min_sat", "400"),
            "min_act": request.form.get("min_act", "1"),
            "major": major,
            "climate_preference": climate_preference,
        }
        return redirect(url_for("results"))

    return render_template("index.html", error=error, form=session.get("form", {}), major_options=major_options)


@app.route("/results")
def results():
    user = session.get("user")
    if not user:
        return redirect(url_for("home"))

    schools = load_schools()
    ranked = rank_schools(schools, user)

    return render_template("results.html", schools=ranked[:10], user=user)


if __name__ == "__main__":
    app.run(debug=True)
