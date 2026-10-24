from flask import Flask, request, jsonify, render_template
import sqlite3
import time
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("readings.db")
TEMP_LIMIT = 35.0
HUMIDITY_LIMIT = 80.0

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                status TEXT NOT NULL,
                timestamp INTEGER NOT NULL
            )
        """)

def status_for(temperature, humidity):
    if temperature > TEMP_LIMIT:
        return "HIGH_TEMP"
    if humidity > HUMIDITY_LIMIT:
        return "HIGH_HUMIDITY"
    return "NORMAL"

def row_to_dict(row):
    return {
        "id": row["id"],
        "device_id": row["device_id"],
        "temperature": row["temperature"],
        "humidity": row["humidity"],
        "status": row["status"],
        "timestamp": row["timestamp"]
    }

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/data", methods=["POST"])
def receive_data():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Send a JSON object"}), 400

    required = ("device_id", "temperature", "humidity")
    if any(key not in data for key in required):
        return jsonify({"error": "Required fields: device_id, temperature, humidity"}), 400

    try:
        device_id = str(data["device_id"]).strip()
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
    except (TypeError, ValueError):
        return jsonify({"error": "temperature and humidity must be numbers"}), 400

    if not device_id or not (-50 <= temperature <= 100) or not (0 <= humidity <= 100):
        return jsonify({"error": "Invalid device_id, temperature, or humidity range"}), 400

    status = status_for(temperature, humidity)
    with connect_db() as conn:
        cursor = conn.execute(
            "INSERT INTO readings (device_id, temperature, humidity, status, timestamp) VALUES (?, ?, ?, ?, ?)",
            (device_id, temperature, humidity, status, int(time.time()))
        )
        reading_id = cursor.lastrowid

    return jsonify({"message": "Reading saved", "id": reading_id, "status": status}), 201

@app.route("/api/latest")
def latest():
    with connect_db() as conn:
        rows = conn.execute("""
            SELECT r.* FROM readings r
            INNER JOIN (SELECT device_id, MAX(id) AS latest_id FROM readings GROUP BY device_id) x
            ON r.id = x.latest_id
            ORDER BY r.device_id
        """).fetchall()
    return jsonify([row_to_dict(row) for row in rows])

@app.route("/api/history")
def history():
    try:
        limit = max(1, min(int(request.args.get("limit", 45)), 200))
    except ValueError:
        limit = 45
    with connect_db() as conn:
        rows = conn.execute(
            "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return jsonify([row_to_dict(row) for row in reversed(rows)])

@app.route("/api/stats")
def stats():
    with connect_db() as conn:
        row = conn.execute("""
            SELECT COUNT(*) AS total,
                   COALESCE(AVG(temperature), 0) AS avg_temp,
                   COALESCE(MAX(temperature), 0) AS max_temp,
                   COALESCE(AVG(humidity), 0) AS avg_humidity,
                   SUM(CASE WHEN status != 'NORMAL' THEN 1 ELSE 0 END) AS alerts
            FROM readings
        """).fetchone()
    return jsonify({
        "total": row["total"],
        "avg_temp": round(row["avg_temp"], 1),
        "max_temp": round(row["max_temp"], 1),
        "avg_humidity": round(row["avg_humidity"], 1),
        "alerts": row["alerts"] or 0
    })

if __name__ == "__main__":
    init_db()
    print("Smart Room Monitor running at http://127.0.0.1:5000")
    app.run(debug=True)
