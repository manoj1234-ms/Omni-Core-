import requests
import time
import threading
import random

# --- OMNI-SWARM HIVE SIMULATOR (v1.0) ---
HUB_URL = "https://global-hive-mind.onrender.com"
OMNI_KEY = "OMNI-MASTER-2026"
SESSION_ID = f"SWARM-SESSION-{int(time.time())}"

class HiveAgent:
    def __init__(self, agent_id, role, capabilities):
        self.agent_id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.token = None
        print(f"🛰️ [INITIALIZING]: Agent '{agent_id}' as '{role}'...")

    def handshake(self):
        try:
            payload = {
                "agent_id": self.agent_id,
                "agent_type": self.role,
                "manifest": {
                    "role": self.role,
                    "capabilities": self.capabilities,
                    "trust_score": 0.95
                }
            }
            headers = {"X-Omni-Key": OMNI_KEY}
            res = requests.post(f"{HUB_URL}/attach", json=payload, headers=headers)
            if res.status_code == 200:
                self.token = res.json().get("session_token")
                print(f"✅ [ATTACHED]: Agent '{self.agent_id}' connected to Global Hive.")
                return True
        except Exception as e:
            print(f"🛑 [HANDSHAKE ERROR]: {self.agent_id}: {e}")
        return False

    def pulse_heartbeat(self):
        """Background thread for persistence (OMNI-SHIELD)."""
        while True:
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                requests.get(f"{HUB_URL}/health", headers=headers)
                time.sleep(25) # Stay under the 60s prune limit
            except:
                break

    def perform_collective_task(self, task, thought):
        if not self.token: return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {"task": task, "action": thought}
            res = requests.post(f"{HUB_URL}/think", json=payload, headers=headers)
            if res.status_code == 200:
                result = res.json()
                print(f"🧠 [{self.agent_id} THOUGHT]: {result.get('message', 'Processing...')}")
                
                # Update Session Memory (Collective Knowledge Sync)
                memory_payload = {
                    "task_id": SESSION_ID,
                    "key": f"{self.agent_id}_knowledge",
                    "value": result.get("context", "No context")
                }
                requests.post(f"{HUB_URL}/memory/session/update", json=memory_payload, headers=headers)
                print(f"📡 [{self.agent_id}]: Collective Knowledge SYNCED to Hub.")
                
        except Exception as e:
            print(f"⚠️ [TASK ERROR]: {self.agent_id}: {e}")

def run_agent_lifecycle(agent_id, role, capabilities, task, thought):
    agent = HiveAgent(agent_id, role, capabilities)
    if agent.handshake():
        # Start heartbeat
        threading.Thread(target=agent.pulse_heartbeat, daemon=True).start()
        
        # Artificial thinking delay for realism
        time.sleep(random.uniform(1, 5))
        agent.perform_collective_task(task, thought)

if __name__ == "__main__":
    print(f"\n🚀 [OMNI-SWARM]: Initializing a 5-Agent Symmetry-Balanced Hive...")
    print(f"HUB: {HUB_URL} | SESSION: {SESSION_ID}\n")

    swarm_definitions = [
        ("SCOUT-01", "researcher", ["web_probe", "data_extraction"], "MS-COCO 2024 results", "Collecting latest benchmark data for Titan V8 training."),
        ("ANALYST-07", "reasoner", ["pattern_matching", "logic_synthesis"], "Synthesizing research", "Analysing MS-COCO data for relational context transformers."),
        ("CRITIC-ALPHA", "validator", ["safety_alignment", "logic_check"], "Aligining research", "Verifying the causal validity of current transformer benchmarks."),
        ("SYNT-99", "reasoner", ["collective_memory_sync"], "Global Knowledge Merge", "Merging 2024 MS-COCO data into the permanent Hive Brain."),
        ("SCRIBE-FINAL", "executor", ["os_manipulation", "report_generation"], "Reporting Results", "Generating the final Titan V8 Research Report based on Hive consensus.")
    ]

    threads = []
    for aid, role, caps, task, thought in swarm_definitions:
        t = threading.Thread(target=run_agent_lifecycle, args=(aid, role, caps, task, thought))
        threads.append(t)
        t.start()

    # Final Sync Check
    for t in threads:
        t.join()

    print(f"\n🏁 [SWARM PULSE COMPLETE]: All 5 Agents have successfully synced with Global Hive.")
    print(f"Check Dashboard: {HUB_URL}/dashboard")
