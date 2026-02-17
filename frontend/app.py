from flask import Flask, render_template, request, redirect, url_for, session
from backend.app.main import load_schools
from backend.app.engine.ranker import rank_schools
from backend.app.clients.geocode import geocode
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def home():
    error = None

    if request.method == "POST":
        location = request.form.get("location", "").strip()
        coords = geocode(location)

        if not coords:
            error = f"Could not find location: '{location}'"
            return render_template("index.html", error=error, form=request.form)

        lat, lon = coords
        session["user"] = {
            "lat": lat,
            "lon": lon,
            "max_budget": float(request.form["max_budget"]),
            "max_distance": float(request.form["max_distance"]),
        }
        session["form"] = {
            "location": location,
            "max_budget": request.form["max_budget"],
            "max_distance": request.form["max_distance"],
        }
        return redirect(url_for("results"))

    return render_template("index.html", error=error, form=session.get("form", {}))


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