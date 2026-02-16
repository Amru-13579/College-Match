from flask import Flask, render_template, request
from backend.app.main import get_schools
from backend.app.engine.ranker import rank_schools

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        user = {
            "lat": float(request.form.get("lat")),
            "lon": float(request.form.get("lon")),
            "max_budget": float(request.form["max_budget"]),
            "max_distance": float(request.form["max_distance"]),
        }

        # 1️⃣ Fetch raw school data from the API
        raw_schools = get_schools()

        # 2️⃣ Pass both raw_schools and user to rank_schools
        results = rank_schools(raw_schools, user)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
