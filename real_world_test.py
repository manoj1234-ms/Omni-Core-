import requests
import json
import time

# --- OMNI-CORE REAL WORLD TEST (MVP V1.1) ---
HUB_URL = "https://global-hive-mind.onrender.com"
OMNI_KEY = "OMNI-MASTER-2026"

def handshake(agent_id, capabilities):
    payload = {"agent_id": agent_id, "role": "Researcher", "capabilities": capabilities, "trust_score": 0.9}
    res = requests.post(f"{HUB_URL}/attach", json=payload, headers={"X-Omni-Key": OMNI_KEY}).json()
    return res.get('session_token')

def run_real_world_task():
    print("====================================================")
    print("🚀 [REAL-WORLD TEST]: Agentic Search & System Action")
    print("====================================================")

    # 1. SCOUT AGENT: Perform Live Internet Search
    scout_id = "SCOUT_AI_007"
    token = handshake(scout_id, ["search", "reasoning"])
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🔍 [SCOUT]: Scanning Live Web for MS-COCO Leaderboard (2024)...")
    # This triggers CausalValidator -> DuckDuckGo
    search_res = requests.post(f"{HUB_URL}/think", 
                               json={"task": "Internet Search", "action": "Latest MS-COCO Leaderboard stats - 2024"}, 
                               headers=headers).json()
    
    print(f"📊 [SEARCH-RESULT]: {search_res.get('message', 'No verified data found.')}")

    # 2. SCRIBE AGENT: Write Findings to Local OS
    scribe_id = "SCRIBE_AI_OS"
    scribe_token = handshake(scribe_id, ["file_io", "os_access"])
    scribe_headers = {"Authorization": f"Bearer {scribe_token}"}

    content = f"OMNI-CORE RESEARCH SUMMARY: MS-COCO 2024.\nContext Found: {search_res.get('context')}"
    
    print("\n📝 [SCRIBE]: Writing research data to host system autonomously...")
    write_res = requests.post(f"{HUB_URL}/execute/write", 
                              json={"filename": "real_world_research.txt", "content": content}, 
                              headers=scribe_headers).json()
    
    if write_res.get('status') == "SUCCESS":
        print(f"✅ [SUCCESS]: File created at: {write_res.get('path', 'real_world_research.txt')}")
        print("\n📄 [FILE-CONTENT]:")
        print(content)
    else:
        print(f"🛑 [FAILED]: {write_res.get('reason', 'Unknown reason.')}")

if __name__ == "__main__":
    run_real_world_task()
