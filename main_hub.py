import os
import time
import jwt
import threading
from typing import List, Optional
from fastapi import FastAPI, Header, HTTPException, Body, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from functools import wraps

# --- OMNI-CORE V3.1: PRODUCTION GROUNDING & CONSENSUS ---
try:
    from omni_components.shared_world_logic import GlobalOmniCore
    from omni_components.os_hook import OSHook
except ImportError:
    from shared_world_logic import GlobalOmniCore
    from os_hook import OSHook

app = FastAPI(title="Omni-Core AGI Hive Hub (v4.3 - THE FINAL ARCHITECTURE)")

# --- GLOBAL CORS & SECURITY ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.environ.get("SECRET_KEY", "OMNI_SECRET_HIVE_MVP_99")
MASTER_KEY = os.environ.get("OMNI_KEY", "OMNI-MASTER-2026")
DASHBOARD_PASS = os.environ.get("DASHBOARD_PASS", "AGI-ACCESS-42")

core: Optional[GlobalOmniCore] = None
os_hook: Optional[OSHook] = None
agent_heartbeats = {} # {agent_id: timestamp}

def prune_stale_agents():
    while True:
        if core:
            now = time.time()
            core.apply_trust_decay()
            
            stale_agents = [aid for aid, ts in agent_heartbeats.items() if (now - ts) > 60]
            for aid in stale_agents:
                if aid in core.active_agents:
                    del core.active_agents[aid]
                if aid in agent_heartbeats:
                    del agent_heartbeats[aid]
        time.sleep(10)

@app.on_event("startup")
async def startup_event():
    """
    🧬 Omni-Core v4.3: Secure Async Initialization.
    Prevents port-binding delays on Render by deferring heavy sync logic.
    """
    global core, os_hook
    print("\n🚀 [OMNI-CORE]: Initializing v4.3 Cognitive Engines...")
    core = GlobalOmniCore()
    os_hook = OSHook(core=core)
    
    # Deferred sync to prevent startup hangs
    threading.Thread(target=core.sync_global_knowledge, daemon=True).start()
    threading.Thread(target=prune_stale_agents, daemon=True).start()
    print("✅ [OMNI-CORE]: Engines Active. Port bound.")

# --- MODELS ---
class GroundRequest(BaseModel):
    thought: str

class ConsensusRequest(BaseModel):
    thoughts: List[dict] # [{"agent_id": "...", "thought": "...", "confidence": 0.5}]

# --- AUTH UTILS ---
def generate_token(agent_id: str):
    payload = {"agent_id": agent_id, "exp": time.time() + 86400}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

async def verify_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token type")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["agent_id"]
    except:
        raise HTTPException(status_code=401, detail="Access Denied")

# --- v4.3 CORE ENDPOINTS (CWEVS) ---

@app.post("/attach")
async def attach_agent(data: dict = Body(...), x_omni_key: str = Header(None)):
    """Registers agent into the secure hive."""
    if x_omni_key != MASTER_KEY:
        raise HTTPException(status_code=403, detail="Invalid Master Key")
    
    agent_id = data.get("agent_id")
    manifest = data.get("manifest", {})
    core.attach_agent(agent_id, manifest)
    agent_heartbeats[agent_id] = time.time()
    
    return {"status": "ATTACHED", "session_token": generate_token(agent_id)}

@app.post("/ground")
async def ground_engine(req: GroundRequest, agent_id: str = Depends(verify_token)):
    """The v3.1 Grounding Module: Thought -> Scored Fact."""
    agent_heartbeats[agent_id] = time.time()
    print(f"🌍 [GROUND-REQ]: {agent_id} is grounding: '{req.thought[:40]}'")
    
    result = core.validator.verify_grounding(req.thought)
    
    # Track grounding in memory
    core.hippocampus.add_memory("grounding_log", f"{agent_id} verified: {req.thought}")
    
    return result

@app.post("/consensus")
async def consensus_engine(req: ConsensusRequest, agent_id: str = Depends(verify_token)):
    """Multi-Agent Consensus Engine: Weighted Voting."""
    agent_heartbeats[agent_id] = time.time()
    print(f"🤝 [CONSENSUS-REQ]: Running hive vote on {len(req.thoughts)} inputs.")
    
    result = core.validator.run_consensus(req.thoughts)
    return result

# --- LEGACY SUPPORT ---
@app.post("/think")
async def think_v2(data: dict = Body(...), agent_id: str = Depends(verify_token)):
    """Backward compat for /think using the new Grounding Engine."""
    task = data.get("task", "general")
    action = data.get("action", "")
    
    grounded = core.validator.verify_grounding(action)
    
    if grounded.get("verified"):
        return {"status": "SUCCESS", "message": grounded.get("corrected"), "context": grounded.get("corrected")}
    else:
        return {"status": "WARNING", "message": "Low logic confidence.", "confidence": grounded.get("confidence")}

# --- UI ROUTES ---
@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    # Professional Landing HTML (Simplified for brevity)
    return """
    <html><head><title>Omni-Core AGI</title><style>body{background:#000;color:#0f0;font-family:monospace;text-align:center;padding:50px;}</style></head>
    <body><h1>🛰️ OMNI-CORE HIVE HUB (v4.3)</h1><p>The Production-Ready AGI Intelligence Layer.</p>
    <p><i>Lead Architect: Manoj Sharma</i></p>
    <a href="/dashboard" style="color:#0f0">[ ACCESS HIVE DASHBOARD ]</a></body></html>
    """

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_view():
    # Dashboard HTML (Simplified)
    return f"""
    <html><head><title>Hive Dashboard</title><style>body{{background:#000;color:#0f0;font-family:monospace;padding:20px;}}</style></head>
    <body><h2>📊 OMNI-HIVE LOGS (Live)</h2><div id='log'>Active Nodes: {len(core.active_agents)}</div></body></html>
    """

@app.get("/health")
async def health():
    if not core:
        return {"status": "STARTING", "active_nodes": 0, "version": "4.3.0-CWEVS"}
    return {"status": "ONLINE", "active_nodes": len(core.active_agents), "version": "4.3.0-CWEVS"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5112)))
