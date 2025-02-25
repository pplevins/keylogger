import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

logs_dir = "data"
os.makedirs(logs_dir, exist_ok=True)


@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.json
    machine_name = data.get("machine")
    log = data.get("data")

    if not machine_name or not log:
        return jsonify({"error": "Invalid Data"}), 400

    machine_dir = os.path.join(logs_dir, machine_name)
    os.makedirs(machine_dir, exist_ok=True)

    # TODO: Change the structure of the data, so it will be separate json for each day.
    log_file = os.path.join(machine_dir, f"{machine_name}.json")

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


if __name__ == "__main__":
    app.run(debug=True)
