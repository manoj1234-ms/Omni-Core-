import requests
import json

# --- OMNI-CORE V2 REGISTRY TEST ---
HUB_URL = "http://127.0.0.1:5010"
HEADERS = {"X-Omni-Key": "OMNI-MASTER-2026"}

def test_v2_registration():
    print("🚀 [TESTING REGISTRY V2]: Capabilities-Based Manifest...")
    
    # 1. REGISTER AGENT WITH MANIFEST
    payload = {
        "agent_id": "EXPERT_CODER_AI",
        "role": "Lead Developer",
        "capabilities": ["python", "flask", "system_design"],
        "trust_score": 0.98
    }
    
    res = requests.post(f"{HUB_URL}/agents/register", json=payload, headers=HEADERS).json()
    print(f"Status: {res.get('status')}")
    print(f"Registered Capabilities: {res.get('capabilities')}")

    # 2. CREATE A TASK SHELL (Stage 2)
    print("\n🧠 [TESTING TASK ORCHESTRATION]: Creating complex task...")
    task_payload = {
        "agent_id": "EXPERT_CODER_AI",
        "task": "Create a secure AGI gateway using flask."
    }
    task_res = requests.post(f"{HUB_URL}/tasks/create", json=task_payload, headers=HEADERS).json()
    print(f"Status: {task_res.get('status')}")
    
    print("\n📋 [ORCHESTRATED TASK GRAPH]:")
    for assignment in task_res.get('assignments', []):
        print(f" 🎯 Step: {assignment['subtask']}")
        print(f"    -> Agent: [{assignment['assigned_to']}] (using {assignment['capability_used']})")

if __name__ == "__main__":
    try:
        test_v2_registration()
    except Exception as e:
        print(f"🛑 [ERROR]: Connection failed. Is the gateway running on 5002? -> {e}")
