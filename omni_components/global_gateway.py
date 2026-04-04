import os
import time
import jwt
from functools import wraps
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
SECRET_KEY = os.environ.get("SECRET_KEY", "OMNI-SECRET-HIVE-99")

# --- TOKEN SECURITY DECORATOR ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"status": "UNAUTHORIZED", "message": "Missing Session Token."}), 401
        try:
            # Bearer <token>
            token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.agent_id = data['agent_id']
        except Exception as e:
            return jsonify({"status": "UNAUTHORIZED", "message": "Invalid or Expired Token."}), 401
        return f(*args, **kwargs)
    return decorated

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
    """V2/V4 Login: Returns a JWT Session Token"""
    if request.headers.get("X-Omni-Key") != OMNI_KEY:
        return jsonify({"status": "UNAUTHORIZED", "message": "Omni-Shield Active."}), 401
    
    data = request.json
    agent_id = data.get("agent_id")
    manifest = data.get("manifest", data.get("agent_type", "general"))
    
    core.attach_agent(agent_id, manifest)
    
    # Generate JWT Token (Expires in 24 hours)
    token = jwt.encode({
        "agent_id": agent_id,
        "exp": time.time() + 86400
    }, SECRET_KEY, algorithm="HS256")
    
    return jsonify({
        "status": "CONNECTED", 
        "token": token
    })

@app.route("/think", methods=["POST"])
@token_required
def validate_thought():
    data = request.json
    result = core.process_global_task(request.agent_id, data.get("task"), data.get("action"))
    return jsonify(result)

@app.route("/tasks/create", methods=["POST"])
@token_required
def create_task_v2():
    data = request.json
    main_task = data.get("task", "General Task")
    result = core.orchestrate_complex_task(main_task)
    return jsonify(result)

@app.route("/memory/session/update", methods=["POST"])
@token_required
def update_session():
    data = request.json
    core.hippocampus.update_session_workspace(data.get("task_id"), data.get("key"), data.get("value"))
    return jsonify({"status": "SUCCESS"})

@app.route("/memory/session/query", methods=["GET"])
@token_required
def get_session():
    task_id = request.args.get("task_id")
    state = core.hippocampus.get_session_workspace(task_id)
    return jsonify(state)

@app.route("/execute", methods=["POST"])
@token_required
def execute_system():
    data = request.json
    result = os_hook.execute_system_command(request.agent_id, data.get("command"))
    return jsonify(result)

@app.route("/write", methods=["POST"])
@token_required
def write_file():
    data = request.json
    result = os_hook.write_autonomous_file(data.get("filename"), data.get("content"))
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
