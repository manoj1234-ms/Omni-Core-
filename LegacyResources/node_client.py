import requests
import json
import time
import threading

# --- OMNI-CORE NODE CLIENT (MVP V1.1 - PULSE-ACTIVE) ---
HUB_URL = "http://127.0.0.1:5111"
OMNI_KEY = "OMNI-MASTER-2026"

class OmniNode:
    def __init__(self, agent_id, role, capabilities):
        self.agent_id = agent_id
        self.role = role
        self.capabilities = capabilities
        self.token = None
        self.active = False
        print(f"🌍 [NODE-IGNITE]: Starting Node '{self.agent_id}' ({self.role})")

    def attach_to_hive(self):
        payload = {
            "agent_id": self.agent_id,
            "role": self.role,
            "capabilities": self.capabilities,
            "trust_score": 0.98
        }
        res = requests.post(f"{HUB_URL}/attach", 
                             json=payload, 
                             headers={"X-Omni-Key": OMNI_KEY}).json()
        
        if res.get("status") == "SUCCESS":
            self.token = res.get("session_token")
            self.active = True
            print(f"✅ [SYNC-COMPLETE]: Node '{self.agent_id}' registered. JWT Token received.")
            # Start Background Heartbeat
            threading.Thread(target=self._heartbeat_loop, daemon=True).start()
            return True
        else:
            return False

    def _heartbeat_loop(self):
        """
        Stage 3: Pulse to Hive every 30s to prevent pruning.
        """
        while self.active:
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                requests.post(f"{HUB_URL}/heartbeat", headers=headers)
                # print(f"💓 [HEARTBEAT]: Node '{self.agent_id}' pulsing...")
            except:
                pass
            time.sleep(30)

    def think(self, task, action):
        if not self.token: return
        headers = {"Authorization": f"Bearer {self.token}"}
        res = requests.post(f"{HUB_URL}/think", 
                             json={"task": task, "action": action}, 
                             headers=headers).json()
        print(f"🧠 [HIVE-THINK]: {self.agent_id} -> {res.get('status')}: {res.get('message')}")

def run_swarm_simulation():
    print("====================================================")
    print("🚀 [SWARM SIMULATION]: Heartbeat & Persistence Run")
    print("====================================================")

    # 1. Start Two Specialized Nodes
    node_a = OmniNode("DEV_NODE_01", "Developer", ["python"])
    node_b = OmniNode("QA_NODE_01", "Validator", ["search"])

    if node_a.attach_to_hive():
        node_a.think("Analyzing code for bugs.", "Logic verification sequence.")

    if node_b.attach_to_hive():
        node_b.think("Verifying world facts.", "Scanned latest AGI benchmarks.")

    print("\n⏳ [MONITORING]: Nodes are now pulsing. Pruning will occur if they stop.")
    print("Simulating 15s of active swarm life...")
    time.sleep(15)
    print("🏁 [SIMULATION-OVER]: Pulse loop exited.")

if __name__ == "__main__":
    run_swarm_simulation()
