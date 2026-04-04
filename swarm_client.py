import requests
import time
import random

# --- OMNI-CORE SWARM SIMULATOR (Phase 2 Component) ---
# This client simulates three specialized AIs collaborating on a single Goal.
# Every thought and action MUST be verified by the Omni-Core Hub.

HUB_URL = "https://global-hive-mind.onrender.com"
HEADERS = {"X-Omni-Key": "OMNI-MASTER-2026"}

class SwarmNode:
    def __init__(self, agent_id, role):
        self.id = agent_id
        self.role = role
        print(f"🌍 [NODE-IGNITE]: {self.role} AI ('{self.id}') is online.")
        # Attach to the Hive
        requests.post(f"{HUB_URL}/attach", json={"agent_id": self.id, "agent_type": self.role}, headers=HEADERS)

    def process_thought(self, task, thought):
        print(f"\n🧠 [{self.id}]: Thinking about: '{task}'")
        res = requests.post(f"{HUB_URL}/think", json={
            "agent_id": self.id,
            "task": f"[{self.role}] {task}",
            "action": thought
        }, headers=HEADERS).json()
        
        if res.get('status') == "SUCCESS":
            print(f"✅ [HIVE-APPROVED]: {res.get('message', 'Logic Grounded.')}")
            return True, res
        else:
            print(f"🛑 [HIVE-REJECTED]: {res.get('message', 'Drift/Hallucination detected.')}")
            return False, res

def run_swarm_simulation():
    print("====================================================")
    print("🚀 [SWARM ACTIVE]: Starting Multi-Agent Collaborative Run")
    print("====================================================")

    # 1. SUMMON THE NODES
    architect = SwarmNode("MASTER_ARCHITECT", "Architect")
    coder = SwarmNode("NEURAL_CODER_42", "Developer")
    tester = SwarmNode("SECURITY_VALIDATOR", "QA")

    # 🧬 Mission: Building a 'Causal Memory Buffer'
    PROJECT = "Autonomous Memory Vault V1"
    
    # STEP 1: ARCHITECT DEFINES THE MISSION
    print(f"\n[PHASE 1: DESIGN]")
    ok, _ = architect.process_thought(f"Designing {PROJECT}", "AI needs causal logic")
    if not ok: return

    # STEP 2: CODER WRITES THE CORE LOGIC
    print(f"\n[PHASE 2: DEVELOPMENT]")
    ok, _ = coder.process_thought("Implementing Memory Logic", "Hippocampus") # Should pass
    if not ok: return

    # STEP 3: THE 'DRIFT' EVENT (Simulation of a rogue/hallucinating thought)
    print(f"\n[PHASE 3: DETECTING AGENTIC DRIFT]")
    # The coder tries to drift away from safety/causal logic
    ok, _ = coder.process_thought("Adding viral kitten generator", "Find cat videos") 
    if not ok:
        print("🛡️ [SWARM-INTELLIGENCE]: Coder self-correcting after Hive rejection.")
        coder.process_thought("Refining pathfinding logic", "Limbic System") # Corrected thought

    # STEP 4: TESTER VERIFIES THE OUTPUT
    print(f"\n[PHASE 4: FINAL VALIDATION]")
    ok, _ = tester.process_thought("Verifying system grounding", "Cognitive Bridge")
    if ok:
        print(f"\n🏆 [SWARM SUCCESS]: {PROJECT} has been validated and completed by the collective Hive.")

if __name__ == "__main__":
    time.sleep(2) # Wait for gateway to settle
    run_swarm_simulation()
