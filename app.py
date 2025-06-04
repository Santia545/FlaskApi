import os
import requests
from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")

if not ORS_API_KEY:
    raise RuntimeError("Set ORS_API_KEY environment variable")

app = Flask(__name__)
CORS(app) 
##ORS_MATRIX_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"
ORS_MATRIX_URL = "https://api.openrouteservice.org/v2/matrix/driving-car"
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        res = Response()
        res.headers['X-Content-Type-Options'] = '*'
        return res
    
def compute_best_location(friends, candidates):
    all_coords = [ [f['lng'], f['lat']] for f in friends ] + [ [c['lng'], c['lat']] for c in candidates ]
    n_friends = len(friends)
    n_candidates = len(candidates)
    sources = list(range(n_friends))
    destinations = list(range(n_friends, n_friends + n_candidates))

    body = {
        "locations": all_coords,
        "sources": sources,
        "destinations": destinations,
        "metrics": ["duration"],
        "units": "m"
    }

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    resp = requests.post(ORS_MATRIX_URL, json=body, headers=headers, timeout=15)
    data = resp.json()

    if "durations" not in data:
        raise RuntimeError(f"ORS Matrix error: {data}")
    durations = data["durations"]  
    size = n_friends + n_candidates
    adj_matrix = [[None for _ in range(size)] for _ in range(size)]
    for i, row in enumerate(durations):
        for j, val in enumerate(row):
            adj_matrix[i][n_friends + j] = val if val is not None else 36000

    adj_list = {i: [] for i in range(size)}
    for i in range(n_friends):
        for j in range(n_candidates):
            cost = adj_matrix[i][n_friends + j]
            if cost is not None:
                adj_list[i].append((n_friends + j, cost))

    totals = [0] * n_candidates
    for j in range(n_candidates):
        for i in range(n_friends):
            cost = adj_matrix[i][n_friends + j]
            totals[j] += cost if cost is not None else 36000

    best_index = min(range(n_candidates), key=lambda i: totals[i])
    best = candidates[best_index].copy()
    best["total_duration_sec"] = totals[best_index]

    ranking = [
        {
            **candidates[i],
            "total_duration_sec": totals[i],
        }
        for i in sorted(range(n_candidates), key=lambda i: totals[i])
    ]
    return best, ranking, adj_list
@app.route('/')
def index():
    return "Hello world"

@app.route("/api/best-location", methods=["POST"])
def best_location():
    payload = request.get_json(force=True)
    friends = payload.get("friends", [])
    candidates = payload.get("candidates", [])

    if not friends or not candidates:
        return jsonify({"error": "friends and candidates lists are required"}), 400

    try:
        best, ranking, adj_list = compute_best_location(friends, candidates)
        return jsonify({"best": best, "ranking": ranking, "graph": adj_list})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
if __name__ == '__main__':
    app.run(debug=True)