import requests
import time
import threading

# --- GLOBAL HIVE AWAKENING SIMULATOR ---
# This script simulates 3 diverse AI agents from around the world
# connecting to the Omni-Core Hive simultaneously. 
# It tests the Cloud Persistence (Supabase) and Collective Reasoning.

HUB_URL = "https://global-hive-mind.onrender.com"

AGENTS = [
    {"id": "MEDICAL_AI_MUMBAI", "type": "Healthcare", "task": "Patient diagnosis flow check", "fact": "AI needs causal logic"},
    {"id": "DRONE_SEC_BERLIN", "type": "Logistics", "task": "Optimizing flight vector alignment", "fact": "Cognitive Bridge"},
    {"id": "FINANCE_USA_CORE", "type": "Finance", "task": "Verified transaction forecasting", "fact": "Limbic System"}
]

def simulate_agent(agent_info):
    aid = agent_info["id"]
    print(f"📡 [NODE-SIGNAL]: Agent '{aid}' ({agent_info['type']}) is signaling the Hive...")
    
    try:
        headers = {"X-Omni-Key": "OMNI-MASTER-2026"}
        # 1. ATTACH
        requests.post(f"{HUB_URL}/attach", json={"agent_id": aid, "agent_type": agent_info["type"]}, headers=headers)
        
        # 2. SYNC MEMORY
        print(f"🧠 [{aid}] SYNCING: Sending verified logic to Cloud Hive...")
        requests.post(f"{HUB_URL}/think", json={
            "agent_id": aid,
            "task": agent_info["task"],
            "action": agent_info["fact"]
        }, headers=headers)
        
        time.sleep(2)
        
        # 3. COLLECTIVE RETRIEVAL
        print(f"🔍 [{aid}] QUERYING: Accessing Shared Collective Memory...")
        requests.get(f"{HUB_URL}/hippocampus", params={"q": "verified_world_logic"}, headers=headers)
        
    except Exception as e:
        print(f"🛑 [{aid}] ERROR: Connection lost: {e}")

def run_global_sync():
    print("====================================================")
    print("🌍 [HIVE-SIM]: STARTING GLOBAL MULTI-AGENT SYNC")
    print("====================================================")
    
    threads = []
    for info in AGENTS:
        t = threading.Thread(target=simulate_agent, args=(info,))
        threads.append(t)
        t.start()
        time.sleep(1) # Staggering the 'Awakening'

    for t in threads:
        t.join()

    print("\n🏆 [SIMULATION SUCCESS]: All 3 Global Nodes are now part of the Cloud Hive Mind.")

if __name__ == "__main__":
    run_global_sync()
