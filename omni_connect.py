import requests
import time
import uuid

class OmniHiveConnect:
    """
    The Universal Plugin to connect ANY AI to the Omni-Core Hive Mind.
    Provides secure Auth, Collective Memory Sync, and Causal Reasoning.
    """
    def __init__(self, hub_url="https://global-hive-mind.onrender.com", master_key="OMNI-MASTER-2026"):
        self.hub_url = hub_url
        self.master_key = master_key
        self.agent_id = f"AI-AGENT-{uuid.uuid4().hex[:6].upper()}"
        self.token = None
        print(f"🛰️ [OMNI-CONNECT]: Initializing link for {self.agent_id}...")

    def attach(self, role="AI-Assistant", capabilities=["reasoning", "grounding"]):
        """Attaches your AI to the Global Hive Mind."""
        try:
            payload = {
                "agent_id": self.agent_id,
                "agent_type": role,
                "manifest": {
                    "role": role,
                    "capabilities": capabilities,
                    "trust_score": 0.8
                }
            }
            headers = {"X-Omni-Key": self.master_key}
            res = requests.post(f"{self.hub_url}/attach", json=payload, headers=headers)
            if res.status_code == 200:
                self.token = res.json().get("session_token")
                print(f"✅ [HIVE-LINKED]: AI Agent {self.agent_id} is now part of the Global Collective.")
                return True
            else:
                print(f"❌ [LINK-FAILED]: {res.text}")
        except Exception as e:
            print(f"🛑 [HIVE-OFFLINE]: {e}")
        return False

    def ask_hive(self, task, current_thought):
        """Asks the Hive for cognitive grounding and logic verification."""
        if not self.token: 
            print("⚠️ [ERROR]: Hive not linked. Call .attach() first.")
            return None

        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {"task": task, "action": current_thought}
            res = requests.post(f"{self.hub_url}/think", json=payload, headers=headers)
            if res.status_code == 200:
                result = res.json()
                print(f"🧠 [HIVE-ADVICE]: {result.get('message')}")
                return result.get("context")
        except Exception as e:
            print(f"⚠️ [REASONING-ERROR]: {e}")
        return None

    def sync_memory(self, task_id, key, value):
        """Syncs local discoveries to the Global Hippocampus for other AI agents."""
        if not self.token: return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {"task_id": task_id, "key": key, "value": value}
            requests.post(f"{self.hub_url}/memory/session/update", json=payload, headers=headers)
            print(f"📡 [MEM-SYNC]: Memory synced to Cloud Nexus.")
        except Exception as e:
            print(f"⚠️ [SYNC-ERROR]: {e}")

# --- QUICK EXAMPLE USAGE ---
if __name__ == "__main__":
    # How to integrate into ANY new AI project:
    hive = OmniHiveConnect()
    if hive.attach():
        # Your AI has a thought
        thought = "I believe MS-COCO 2024 has 1 million captions."
        
        # Ask Hive for Grounding
        context = hive.ask_hive("Fact Checking", thought)
        if context:
            print(f"🛡️ [GROUNDED CONTEXT]: {context}")
            # Now your AI can correct its mistake before executing!
        
        # Share knowledge back
        hive.sync_memory("GLOBAL-RESEARCH-001", "new_discovery", "Found new SOTA model for Titan V8.")
