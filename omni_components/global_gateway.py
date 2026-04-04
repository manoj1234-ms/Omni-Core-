import os
from flask import Flask, request, jsonify, redirect, make_response
from flask_cors import CORS
try:
    from omni_components.shared_world_logic import GlobalOmniCore
    from omni_components.os_hook import OSHook
except ModuleNotFoundError:
    from shared_world_logic import GlobalOmniCore
    from os_hook import OSHook

app = Flask(__name__)
CORS(app) # Enable Global Cross-Origin access
core = GlobalOmniCore()
os_hook = OSHook(core=core)

# --- OMNI-SHIELD SECURITY PROTOCOL ---
OMNI_KEY = os.environ.get("OMNI_KEY", "OMNI-MASTER-2026")
DASHBOARD_PASS = os.environ.get("DASHBOARD_PASS", "AGI-ACCESS-42")

@app.route("/", methods=["GET"])
def index():
    try:
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(script_dir, "landing.html")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Could not load landing page: {e}"}), 500

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        if request.form.get("password") == DASHBOARD_PASS:
            resp = make_response(redirect("/dashboard"))
            resp.set_cookie("omni_auth", "true")
            return resp
        else:
            return "<h1 style='color:red; text-align:center;'>Access Denied</h1>", 401
    if request.cookies.get("omni_auth") != "true":
        return '<h2>🔒 OMNI-CORE LOCKED</h2><form method="POST"><input type="password" name="password"/><button>UNLOCK</button></form>'
    try:
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_path = os.path.join(script_dir, "dashboard.html")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ONLINE", "active_agents": len(core.active_agents)})

@app.route("/attach", methods=["POST"])
def attach_agent():
    if request.headers.get("X-Omni-Key") != OMNI_KEY:
        return jsonify({"status": "UNAUTHORIZED"}), 401
    data = request.json
    core.attach_agent(data.get("agent_id"), data.get("agent_type", "general"))
    return jsonify({"status": "CONNECTED"})

@app.route("/think", methods=["POST"])
def validate_thought():
    if request.headers.get("X-Omni-Key") != OMNI_KEY:
        return jsonify({"status": "UNAUTHORIZED"}), 401
    data = request.json
    result = core.process_global_task(data.get("agent_id"), data.get("task"), data.get("action"))
    return jsonify(result)

@app.route("/execute", methods=["POST"])
def execute_system():
    if request.headers.get("X-Omni-Key") != OMNI_KEY:
        return jsonify({"status": "UNAUTHORIZED"}), 401
    data = request.json
    result = os_hook.execute_system_command(data.get("agent_id"), data.get("command"))
    return jsonify(result)

@app.route("/write", methods=["POST"])
def write_file():
    if request.headers.get("X-Omni-Key") != OMNI_KEY:
        return jsonify({"status": "UNAUTHORIZED"}), 401
    data = request.json
    result = os_hook.write_autonomous_file(data.get("filename"), data.get("content"))
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
