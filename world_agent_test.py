import requests
import json
import time

# --- WORLD-WIDE AI SIMULATOR ---
# This script simulates a Medical AI Agent in India attaching 
# to the Omni-Core Hive Mind on Port 5000.

GATEWAY_URL = "http://127.0.0.1:5000"
AGENT_ID = "MED_AI_IND_01"

def simulate_world_connection():
    print(f"\n📡 [WORLD-CONNECT]: Agent '{AGENT_ID}' (Healthcare) is connecting to Global Core...")
    
    # 1. ATTACH (Registration)
    attach_res = requests.post(f"{GATEWAY_URL}/attach", json={"agent_id": AGENT_ID, "agent_type": "Medical"})
    print(f"🔗 [GATEWAY]: {attach_res.json()['welcome']}")

    # 2. THINK (Validation & Goal Sync)
    print(f"\n🧠 [THINKING]: Agent '{AGENT_ID}' is processing patient logic...")
    thought_payload = {
        "agent_id": AGENT_ID,
        "task": "Verifying medical diagnosis logic core.",
        "action": "AI needs causal logic"
    }
    think_res = requests.post(f"{GATEWAY_URL}/think", json=thought_payload).json()
    msg = think_res.get('message', think_res.get('reason', 'Unknown Response'))
    print(f"🛡️ [VERIFICATION]: Status: {think_res['status']} | {msg}")

    # 3. HALLUCINATION CHECK (Testing Causal Validator)
    print(f"\n⚠️ [THINKING]: Agent '{AGENT_ID}' is drifting into hallucination...")
    hallucination_payload = {
        "agent_id": AGENT_ID,
        "task": "Considering experimental telepathy.",
        "action": "Quantum-Telepathy for medicine"
    }
    hall_res = requests.post(f"{GATEWAY_URL}/think", json=hallucination_payload).json()
    msg = hall_res.get('message', hall_res.get('reason', 'Unknown Response'))
    print(f"🛡️ [VERIFICATION]: Status: {hall_res['status']} | {msg}")

    # 4. MEMORY QUERY (Hippocampus Hippocampus)
    print(f"\n🔍 [RETRIEVING]: Querying the Shared World Knowledge for 'Grounded' concepts...")
    mem_res = requests.get(f"{GATEWAY_URL}/hippocampus", params={"q": "grounded_logic"})
    print(f"🧠 [SHARED HIPPOCAMPUS]: Results for world-search: {mem_res.json()['collective_context']}")

if __name__ == "__main__":
    try:
        simulate_world_connection()
        print("\n🏆 [GLOBAL TEST]: World-AI Synthesis Simulation COMPLETE and SUCCESSFUL.")
    except Exception as e:
        print(f"❌ [ERROR]: Connection failed for world-agent: {e}")
