# frontend/app.py
from flask import Flask, render_template, request, redirect, url_for, session
from backend.app.main import load_schools
from backend.app.engine.ranker import rank_schools
from backend.app.clients.geocode import geocode

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Preload schools when the app starts
print("Preloading school data...")
load_schools()
print("School data loaded!")

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    error = None

    if request.method == "POST":
        location = request.form.get("location", "").strip()
        coords = geocode(location)

        if not coords:
            error = f"Could not find location: '{location}'"
        else:
            lat, lon = coords
            user = {
                "lat": lat,
                "lon": lon,
                "max_budget": float(request.form["max_budget"]),
                "max_distance": float(request.form["max_distance"]),
            }
            schools = load_schools()
            results = rank_schools(schools, user)

    return render_template("index.html", results=results, error=error)

if __name__ == "__main__":
    app.run(debug=True)