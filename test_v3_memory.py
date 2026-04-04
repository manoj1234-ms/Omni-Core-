import requests
import time

# --- OMNI-CORE V2 MEMORY TEST ---
HUB_URL = "http://127.0.0.1:5000" # Using verify-port from Stage 2
HEADERS = {"X-Omni-Key": "OMNI-MASTER-2026"}
TASK_ID = "GLOBAL_DEPLOYMENT_PLAN"

def test_v2_memory_sync():
    print(f"🚀 [TESTING STAGE 3]: Multi-Agent Context Persistence for Task: {TASK_ID}")
    
    # 1. AGENT A: Writing State to the Hive
    print("\n👤 [AGENT A]: Logging infrastructure details to Shared Memory...")
    payload_a = {
        "task_id": TASK_ID,
        "key": "cloud_provider",
        "value": "Render"
    }
    requests.post(f"{HUB_URL}/memory/session/update", json=payload_a, headers=HEADERS)
    
    payload_b = {
        "task_id": TASK_ID,
        "key": "deployment_status",
        "value": "Initializing..."
    }
    requests.post(f"{HUB_URL}/memory/session/update", json=payload_b, headers=HEADERS)

    # 2. AGENT B: Reading State from the Hive
    print("\n👤 [AGENT B]: Retrieving current task context from Shared Memory...")
    res = requests.get(f"{HUB_URL}/memory/session/query?task_id={TASK_ID}").json()
    
    print(f"📦 [HIVE-STATE]: {res.get('data')}")
    
    if res.get('data', {}).get('cloud_provider') == "Render":
        print("✅ [SYNC SUCCESS]: Agent B successfully synchronized with Agent A's context.")
    else:
        print("🛑 [SYNC FAILED]: Memory context is inconsistent.")

if __name__ == "__main__":
    test_v2_memory_sync()
