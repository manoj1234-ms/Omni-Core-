import os
import time
import jwt
import threading
from typing import List, Optional
from fastapi import FastAPI, Header, HTTPException, Body, Depends, Request
from pydantic import BaseModel
from functools import wraps

# --- IMPORTING THE GUTS (Brain & Hands) ---
try:
    from omni_components.shared_world_logic import GlobalOmniCore
    from omni_components.os_hook import OSHook
except ImportError:
    from shared_world_logic import GlobalOmniCore
    from os_hook import OSHook

app = FastAPI(title="Omni-Core AGI Hive Hub (v1.1 - Monitoring & Pulse)")

# --- GLOBAL OMNI-SHIELD ---
SECRET_KEY = os.environ.get("SECRET_KEY", "OMNI_SECRET_HIVE_MVP_99")
MASTER_KEY = os.environ.get("OMNI_KEY", "OMNI-MASTER-2026")

# --- INITIALIZE BRAIN ---
core = GlobalOmniCore()
os_hook = OSHook(core=core)
agent_heartbeats = {} # {agent_id: timestamp}

# --- SCHEMAS ---
class AgentManifest(BaseModel):
    agent_id: str
    role: str
    capabilities: List[str]
    trust_score: float = 0.5

# --- MONITORING BACKGROUND THREAD ---
def prune_stale_agents():
    """
    Cleaner: Removes agents that haven't pulsed for > 60 seconds.
    Ensures the Hive Swarm only contains ACTIVE nodes.
    """
    while True:
        now = time.time()
        stale_agents = [aid for aid, ts in agent_heartbeats.items() if (now - ts) > 60]
        for aid in stale_agents:
            print(f"💀 [CLEANER]: Node '{aid}' is UNRESPONSIVE. Pruning from Hive.")
            if aid in core.active_agents:
                del core.active_agents[aid]
            del agent_heartbeats[aid]
        time.sleep(10)

threading.Thread(target=prune_stale_agents, daemon=True).start()

# --- SECURITY UTILS ---
def generate_token(agent_id: str):
    payload = {"agent_id": agent_id, "exp": time.time() + 86400}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

async def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        agent_id = payload['agent_id']
        # Register pulse
        agent_heartbeats[agent_id] = time.time()
        return agent_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Session Token.")

# --- ENDPOINTS ---

@app.get("/health")
def health():
    return {
        "status": "ONLINE", 
        "active_nodes": len(core.active_agents),
        "swarm_pulse": f"{len(agent_heartbeats)} nodes pulsing"
    }

@app.post("/heartbeat")
async def pulse(agent_id: str = Depends(verify_token)):
    """
    Stage 3: Keep-Alive Protocol. Agents must pulse every 30s.
    """
    agent_heartbeats[agent_id] = time.time()
    return {"status": "PULSE_RECEIVED", "timestamp": agent_heartbeats[agent_id]}

@app.post("/attach")
def attach_node(manifest: AgentManifest, x_omni_key: str = Header(...)):
    if x_omni_key != MASTER_KEY:
        raise HTTPException(status_code=403, detail="Omni-Shield Blocked Access.")
    
    core.attach_agent(manifest.agent_id, manifest.dict())
    agent_heartbeats[manifest.agent_id] = time.time()
    
    token = generate_token(manifest.agent_id)
    return {"status": "SUCCESS", "session_token": token}

@app.post("/think")
async def process_reasoning(task: str = Body(...), action: str = Body(...), agent_id: str = Depends(verify_token)):
    print(f"🧠 [HIVE-THINK]: Agent '{agent_id}' claims: {action}")
    result = core.process_global_task(agent_id, task, action)
    return result

@app.post("/tasks/create")
async def delegate_complex_task(task: str = Body(...), agent_id: str = Depends(verify_token)):
    """
    Stage 2: Task Orchestration (Planner + Router).
    """
    print(f"🧩 [HIVE-ORCHESTRATOR]: New complex goal from '{agent_id}': {task}")
    result = core.orchestrate_complex_task(task)
    return result

@app.post("/memory/session/update")
async def update_session(task_id: str = Body(...), key: str = Body(...), value: str = Body(...), agent_id: str = Depends(verify_token)):
    """
    Stage 3: Collective Memory Sync.
    """
    core.hippocampus.update_session_workspace(task_id, key, value)
    return {"status": "SUCCESS", "synced_by": agent_id}

@app.get("/memory/session/query")
async def query_session(task_id: str, agent_id: str = Depends(verify_token)):
    """
    Stage 3: Collective Memory Retrieval.
    """
    state = core.hippocampus.get_session_workspace(task_id)
    return state

@app.post("/execute/write")
async def write_file(filename: str = Body(...), content: str = Body(...), agent_id: str = Depends(verify_token)):
    print(f"📝 [HIVE-WRITE]: Agent '{agent_id}' writing to: {filename}")
    result = os_hook.write_autonomous_file(filename, content)
    return result

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5111))
    uvicorn.run(app, host="0.0.0.0", port=port)
