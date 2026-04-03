from flask import Flask, request, jsonify
try:
    from omni_components.shared_world_logic import GlobalOmniCore
except ModuleNotFoundError:
    from shared_world_logic import GlobalOmniCore

app = Flask(__name__)
core = GlobalOmniCore()

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ONLINE", "vision": "Omni-Core Global AI Synthesis", "active_agents": len(core.active_agents)})

@app.route("/attach", methods=["POST"])
def attach_agent():
    data = request.json
    agent_id = data.get("agent_id")
    agent_type = data.get("agent_type", "general")
    
    if not agent_id:
        return jsonify({"status": "ERROR", "message": "Missing agent_id"}), 400
        
    core.attach_agent(agent_id, agent_type)
    return jsonify({"status": "CONNECTED", "welcome": f"Agent {agent_id} attached to the World-Core."})

@app.route("/think", methods=["POST"])
def validate_thought():
    data = request.json
    agent_id = data.get("agent_id")
    task = data.get("task")
    action = data.get("action")
    
    if not all([agent_id, task, action]):
        return jsonify({"status": "ERROR", "message": "Missing Agent Data (id/task/action)"}), 400
        
    # Check if the agent is already in our hive
    if agent_id not in core.active_agents:
        core.attach_agent(agent_id) # Auto-attach for world-wide compatibility
        
    # Process through the Hive Mind: Goal Tree -> Hippocampus -> Causal Validator
    result = core.process_global_task(agent_id, task, action)
    
    return jsonify(result)

@app.route("/hippocampus", methods=["GET"])
def query_memory():
    query = request.args.get("q", "general")
    memories = core.hippocampus.retrieve_relevant_context(query)
    return jsonify({"query": query, "collective_context": memories})

@app.route("/stats", methods=["GET"])
def get_global_stats():
    # Retrieve the latest verified logic facts
    all_logic = core.hippocampus.memory_store.get("verified_world_logic", [])
    
    return jsonify({
        "status": "ONLINE",
        "dopamine": core.limbic.dopamine,
        "cortisol": core.limbic.cortisol,
        "agent_count": len(core.active_agents),
        "recent_logic": all_logic[-5:] if all_logic else [],
        "drift_blocks": core.goal_tree.drift_count
    })

import os
if __name__ == "__main__":
    # Starting the Global AI Brain on a Dynamic Port for Cloud Compatibility
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 [GLOBAL GATEWAY]: Launching World-AI Entrance Portal on Port {port}...")
    app.run(host="0.0.0.0", port=port)
