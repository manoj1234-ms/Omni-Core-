import os
from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI(title="Omni-Core Code Agent (Node 2)")

class Task(BaseModel):
    task: str

@app.get("/")
async def root():
    return {"status": "ONLINE", "agent_id": "code_agent_01"}

@app.post("/process")
async def process_task(req: Task):
    """Generates code snippets and logic models based on Omni-Core prompts."""
    print(f"💻 [CODE-AGENT]: Task received: {req.task}")
    
    # Mocking code generation for the demo
    code_output = f"// Omni-Core System Interface (Generated for {req.task})\n\n" \
                 f"module OmniCore_API {{\n" \
                 f"  export const executeHiveTask = async (task: string) => {{\n" \
                 f"    console.log(`Executing Hive Task: ${{task}}`);\n" \
                 f"    return await fetch('http://localhost:5112/orchestrate', {{\n" \
                 f"      method: 'POST',\n" \
                 f"      body: JSON.stringify({{ task }})\n" \
                 f"    }});\n" \
                 f"  }};\n" \
                 f"}}\n" \
                 f"// End of Generated Snippet"
    
    return {
        "agent": "code_agent_01",
        "content": code_output,
        "type": "code/typescript",
        "causal_score": 0.96 # Metric for code grounding
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5114)
