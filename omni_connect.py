import requests
import time
import uuid

class OmniHiveConnect:
    """
    The Universal Plugin to connect ANY AI to the Omni-Core Hive Mind (v3.1).
    Provides: Scored Grounding, Multi-Agent Consensus, and Global Memory.
    """
    def __init__(self, hub_url="https://global-hive-mind.onrender.com", master_key="OMNI-MASTER-2026"):
        self.hub_url = hub_url
        self.master_key = master_key
        self.agent_id = f"AI-AGENT-{uuid.uuid4().hex[:6].upper()}"
        self.token = None
        print(f"🛰️ [OMNI-CONNECT v3.1]: Initializing link for {self.agent_id}...")

    def attach(self, role="AI-Assistant", capabilities=["grounding", "consensus"]):
        """Attaches your AI to the secure hive."""
        try:
            payload = {
                "agent_id": self.agent_id,
                "agent_type": role,
                "manifest": {"role": role, "capabilities": capabilities, "trust_score": 0.9}
            }
            headers = {"X-Omni-Key": self.master_key}
            res = requests.post(f"{self.hub_url}/attach", json=payload, headers=headers)
            if res.status_code == 200:
                self.token = res.json().get("session_token")
                print(f"✅ [HIVE-LINKED]: Agent '{self.agent_id}' is now verified.")
                return True
        except Exception as e:
            print(f"🛑 [HIVE-OFFLINE]: {e}")
        return False

    def ground_thought(self, thought):
        """Asks the Hive for mathematical grounding and confidence score (v3.1)."""
        if not self.token: return None
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {"thought": thought}
            res = requests.post(f"{self.hub_url}/ground", json=payload, headers=headers)
            if res.status_code == 200:
                result = res.json()
                print(f"🧠 [GROUNDING]: Confidence: {result.get('confidence')} | Risk: {result.get('risk', 'high')}")
                return result
        except Exception as e:
            print(f"⚠️ [REASONING-ERROR]: {e}")
        return None

    def run_consensus(self, thoughts_list):
        """Runs a multi-agent vote on a list of collective thoughts."""
        if not self.token: return None
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {"thoughts": thoughts_list}
            res = requests.post(f"{self.hub_url}/consensus", json=payload, headers=headers)
            return res.json()
        except:
            return None

    def sync_memory(self, task_id, key, value):
        if not self.token: return
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            payload = {"task_id": task_id, "key": key, "value": value}
            requests.post(f"{self.hub_url}/memory/session/update", json=payload, headers=headers)
        except:
            pass

# --- QUICK v3.1 TEST ---
if __name__ == "__main__":
    hub = "https://global-hive-mind.onrender.com"
    hive = OmniHiveConnect(hub_url=hub)
    if hive.attach():
        # Example: Scored Grounding
        result = hive.ground_thought("Titan V8 image transformer performance")
        print(f"🛡️ [RESULT]: {result}")
