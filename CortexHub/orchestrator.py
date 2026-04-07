import os
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import httpx
import asyncio
from router import route_task
from scoring_engine import ConfidenceEngine
from verification_engine import VerificationEngine

app = FastAPI(title="Omni-Core AGI Orchestrator (Cortex)")

# --- NODES (MICROSERVICES) REGISTRY ---
NODES = {
    "text_agent": "http://localhost:5113",
    "code_agent": "http://localhost:5114",
    "vidnexora_agent": "http://localhost:5115"
}

class OrchestrationTask(BaseModel):
    task: str

@app.get("/")
async def root():
    return {"status": "ONLINE", "version": "v4.1-Cortex-Orchestrator"}

@app.post("/orchestrate")
async def orchestrate_task(req: OrchestrationTask):
    task_desc = req.task
    results = {}
    
    # 🧠 PATENT-READY COMPONENT 1: Context-Aware Routing (V4.1)
    agents_triggered = route_task(task_desc)
    
    if not agents_triggered:
        return {"status": "IDLE", "message": "No specialized agents triggered."}
    
    # --- Agent Chaining (Graph Dependency v4.2) ---
    # Mechanism: Prompt-Level Context Fusion.
    # Logic: Previous agent output is injected as a high-priority specification inside the system prompt of the next agent.
    context_buffer = ""
    async with httpx.AsyncClient() as client:
        for agent_name in agents_triggered:
            # 🧬 Context Fusion: Inscribing stateful memory into the next instruction block.
            instruction = f"SPECIFICATION: Use previous result as grounding context.\nCONTEXT: {context_buffer}\n\nTASK: {task_desc}"
            try:
                url = f"{NODES[agent_name]}/process"
                resp = await client.post(url, json={"task": instruction}, timeout=10.0)
                agent_res = resp.json()
                results[agent_name] = agent_res
                # Update context buffer with agent output (Chain Fusion)
                agent_content = str(agent_res.get('content', ''))
                context_buffer += f"\n[{agent_name}_output]: {agent_content[:100]}..."
            except Exception as e:
                results[agent_name] = {"error": str(e)}

    # 🔬 PATENT-READY COMPONENT 2: Bulletproof Scoring (v4.3)
    scoring = ConfidenceEngine(list(results.values()))
    final_confidence = scoring.get_final_confidence(alpha=0.6) 
    
    # 🧨 PATENT-READY COMPONENT 3: Multi-Stage Recovery (CWEVS v4.3)
    verifier = VerificationEngine(confidence_score=final_confidence, threshold=0.85)
    # 🧪 Pass actual mean confidence to trigger the 0.70 safeguard floor correctly
    orchestration_mode = verifier.get_mode(mu=scoring.compute_causal_mean())
    
    recovery_executed = "None"
    if orchestration_mode == "VERIFIED_WITH_RECOVERY_L1":
        recovery_executed = verifier.execute_recovery(task_desc, level=1)
    elif orchestration_mode == "VERIFIED_WITH_FALLBACK_L2":
        recovery_executed = verifier.execute_recovery(task_desc, level=2)

    return {
        "status": "COMPLETED",
        "orchestration_mode": orchestration_mode,
        "recovery_protocol": recovery_executed,
        "patent_claims": {
            "scoring_logic": "Confidence_Weighted_Entropy_Penalization",
            "recovery_layer": "Multi_Stage_Adaptive_Recovery",
            "causal_attribution": "Weighted(Task, Format, Logic)"
        },
        "original_task": task_desc,
        "confidence_score": final_confidence,
        "entropy_variance": scoring.compute_entropy_variance(alpha=0.6)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5112)
