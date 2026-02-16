# frontend/app.py
from flask import Flask, render_template, request, redirect, url_for, session
from backend.app.main import load_schools
from backend.app.engine.ranker import rank_schools
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Preload schools when the app starts
print("Preloading school data...")
load_schools()
print("School data loaded!")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            session["user"] = {
                "lat": float(request.form["lat"]),
                "lon": float(request.form["lon"]),
                "max_budget": float(request.form["max_budget"]),
                "max_distance": float(request.form["max_distance"])
            }
        except ValueError:
            return render_template("index.html", error="Please enter valid numbers.")
        
        return redirect(url_for("results"))
    
    user = session.get("user")
    return render_template("index.html", user=user)

@app.route("/results")
def results():
    user = session.get("user")
    if not user:
        return redirect(url_for("home"))
    
    try:
        # Get all schools from cache
        raw_schools = load_schools()
        ranked = rank_schools(raw_schools, user)
        top_results = ranked[:10]  # Show top 10
    except Exception as e:
        print("ERROR in ranking schools:", e)
        top_results = []
    
    return render_template("results.html", schools=top_results)

if __name__ == "__main__":
    app.run(debug=True)