import os
from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import httpx
import asyncio

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
    return {"status": "ONLINE", "version": "v3.3-Cortex-Orchestrator"}

from router import route_task

@app.post("/orchestrate")
async def orchestrate_task(req: OrchestrationTask):
    task_desc = req.task
    results = {}
    
    # 🧠 OMNI-CORE CORTEX ROUTING
    agents_triggered = route_task(task_desc)
    
    if not agents_triggered:
        return {"status": "IDLE", "message": "No specialized agents triggered for this task."}
    
    tasks_to_run = []
    for agent_name in agents_triggered:
        instruction = f"Execute phase for: {task_desc}"
        tasks_to_run.append((agent_name, instruction))

    # Parallel Execution of Swarm Nodes
    async with httpx.AsyncClient() as client:
        async def call_agent(agent_name, agent_task):
            try:
                url = f"{NODES[agent_name]}/process"
                resp = await client.post(url, json={"task": agent_task}, timeout=10.0)
                return agent_name, resp.json()
            except Exception as e:
                return agent_name, {"error": str(e)}

        agent_results = await asyncio.gather(*(call_agent(name, task) for name, task in tasks_to_run))
        for name, res in agent_results:
            results[name] = res

    # Omni-Core Synthesis
    return {
        "status": "COMPLETED",
        "original_task": task_desc,
        "hive_mind_output": results,
        "consensus_score": 0.95 # Mock for now
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5112)
