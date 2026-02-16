from flask import Flask, render_template, request
from backend.app.main import load_schools
from backend.app.engine.ranker import rank_schools

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        user = {
            "lat": float(request.form["lat"]),
            "lon": float(request.form["lon"]),
            "max_budget": float(request.form["max_budget"]),
            "max_distance": float(request.form["max_distance"]),
        }
        schools = load_schools()
        results = rank_schools(schools, user)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)