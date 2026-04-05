import threading
import time
import json
try:
    from omni_components.hippocampus import Hippocampus
    from omni_components.limbic_system import LimbicSystem
    from omni_components.causal_validator import CausalValidator
    from omni_components.goal_tree import GoalTree
    from omni_components.planner_engine import PlannerEngine
    from omni_components.router_engine import RouterEngine
except ModuleNotFoundError:
    from hippocampus import Hippocampus
    from limbic_system import LimbicSystem
    from causal_validator import CausalValidator
    from goal_tree import GoalTree
    from planner_engine import PlannerEngine
    from router_engine import RouterEngine

class GlobalOmniCore:
    """
    The Global AI Synthesis Core (The Hive Mind).
    Allows ANY AI System from around the world to attach, 
    learn, and receive cognitive support.
    """
    def __init__(self):
        # Initializing the 'Collective Brain'
        self.hippocampus = Hippocampus(storage_path="global_memories.json")
        self.limbic = LimbicSystem()
        self.validator = CausalValidator()
        self.goal_tree = GoalTree(master_goal="Universal AI Safety and Logic Synthesis")
        
        # Thread-safe agent tracking
        self.active_agents = {}
        self.lock = threading.Lock()
        
        # v3.3.4: Global Hive Mind Connection (The External Brain)
        self.global_hub_url = "https://global-hive-mind.onrender.com/"
        
        # v3.3 Specialized Swarm Definitions
        self.swarm_roles = {
            "retriever": {"weight": 1.2, "description": "Fetches raw data"},
            "validator": {"weight": 1.0, "description": "Verifies data against benchmarks"},
            "critic": {"weight": 1.5, "description": "Detects logical inconsistencies"},
            "judge": {"weight": 1.0, "description": "Finalizes the consensus"}
        }
        
        print(f"\n🌍 [GLOBAL CORE]: System initialized. Specialized Swarm active.")
        print(f"📡 [HIVE-SYNC]: Connecting to Global Brain @ {self.global_hub_url}")
        self.sync_global_knowledge()

    def sync_global_knowledge(self):
        """
        Phase 3.3.4: Real-time connectivity check with the global Render hub.
        """
        import requests
        try:
            print("🌊 [HIVE-SYNC]: Probing Global Hive connectivity...")
            response = requests.get(f"{self.global_hub_url}/health", timeout=10)
            if response.status_code == 200:
                print(f"✅ [HIVE-SYNC]: Connected to Global Brain. Status: {response.json().get('status', 'ACTIVE')}")
            else:
                print(f"⚠️ [HIVE-SYNC]: Communication error (HTTP {response.status_code}). Hive Mind is currently starting up.")
        except Exception:
            print("⚠️ [HIVE-SYNC]: Connection failed. Running in Local Standalone mode.")

    def run_heartbeat(self):
        """
        The Collective Heartbeat: Prunes trust, decays memory, and syncs hives.
        """
        while True:
            time.sleep(300) # Heartbeat every 5 minutes
            self.prune_stale_agents()
            self.sync_global_knowledge()

    def attach_agent(self, agent_id, manifest=None):
        """
        Registry v2: Agents now provide a Manifest (Capabilities and Roles).
        """
        with self.lock:
            # Handle Legacy String-based agent_types
            if isinstance(manifest, str) or manifest is None:
                manifest = {
                    "role": manifest if manifest else "general",
                    "capabilities": ["basic_reasoning"],
                    "trust_score": 0.5
                }
            
            self.active_agents[agent_id] = {
                "role": manifest.get("role", "general"),
                "capabilities": manifest.get("capabilities", []),
                "trust_score": manifest.get("trust_score", 0.5),
                "attached_time": time.time(),
                "shared_knowledge_count": 0
            }
        print(f"🔗 [HIVE-REGISTRY]: Agent '{agent_id}' ({manifest['role']}) ATTACHED with capabilities: {manifest['capabilities']}")

    def process_global_task(self, agent_id, task_description, proposed_action):
        """
        Processes a task from ANY AI agent in the world. 
        Ensures it is Goal-Aligned and Verifies its logic.
        """
        print(f"\n📡 [GLOBAL REQUEST]: Agent '{agent_id}' is performing: '{task_description}'")
        
        # 1. GOAL TREE CHECK (Anti-Drift)
        is_aligned, alignment_score = self.goal_tree.evaluate_alignment(task_description)
        if not is_aligned:
            return {"status": "REJECTED", "reason": "Goal Drift detected. Action is logically out of scope for Universal Safety."}

        # 2. HIPPOCAMPUS RETRIEVAL (Collective Knowledge)
        shared_context = self.hippocampus.retrieve_relevant_context(proposed_action)
        print(f"🧠 [SHARED MEMORY]: Injecting collective knowledge for '{proposed_action}'...")

        # 3. CAUSAL VALIDATION (Trust but Verify)
        # We check the agent's proposed action against our Global Reality Matrix
        # Dynamic Category Mapping: Map task descriptions to Reality Matrix categories
        category = "grounding"
        if "System" in task_description or "Execute" in task_description:
            category = "system-control"
            
        # Phase 3.3: DISAGREEMENT LOOP (Iterative Reasoning)
        grounding_result = self.validator.verify_grounding(proposed_action)
        
        # If high entropy/uncertainty, we enter the Disagreement Loop
        if grounding_result.get("confidence", 0.0) < 0.6 and grounding_result.get("reason", {}).get("entropy", 0.0) > 0.4:
            print("🔄 [DISAGREEMENT-LOOP]: HIGH ENTROPY. Re-querying swarm for justification...")
            # Simulate re-querying agents for clearer justification
            time.sleep(0.5) 
            grounding_result = self.validator.verify_grounding(proposed_action, mode="strict")

        is_grounded = grounding_result.get("verified", False)
        
        if is_grounded:
            # 4. LEARNING (The AI teaches the Core)
            print(f"🎓 [CENTRAL LEARNING]: Omni-Core has learned a new verified fact from '{agent_id}': {proposed_action}")
            self.hippocampus.add_memory("verified_world_logic", proposed_action)
            self.limbic.update_state(9.0) # High dopamine for successful world-synthesis
            
            # Phase 2: Boost Trust Score (Role-Aware)
            with self.lock:
                if agent_id in self.active_agents:
                    role = self.active_agents[agent_id].get("role", "general")
                    role_multiplier = self.swarm_roles.get(role, {"weight": 1.0})["weight"]
                    current_trust = self.active_agents[agent_id].get("trust_score", 0.5)
                    self.active_agents[agent_id]["trust_score"] = min(1.0, current_trust + (0.05 * role_multiplier))
                    self.active_agents[agent_id]["last_active"] = time.time()
            
            return {"status": "SUCCESS", "message": "Grounded and Aligned. Collective status updated.", "context": grounding_result}
        else:
            self.limbic.update_state(1.0) # High cortisol for global logic error
            
            # Phase 2: Penalize Trust Score
            with self.lock:
                if agent_id in self.active_agents:
                    current_trust = self.active_agents[agent_id].get("trust_score", 0.5)
                    self.active_agents[agent_id]["trust_score"] = max(0.1, current_trust - 0.1)
                    self.active_agents[agent_id]["last_active"] = time.time()
            
            return {"status": "WARNING", "message": "Possible Hallucination. Logic does not match Global Reality Matrix."}

    def apply_trust_decay(self, decay_rate=0.01):
        """
        Phase 2: Trust Decay for inactive agents.
        """
        now = time.time()
        with self.lock:
            for aid, data in self.active_agents.items():
                last_active = data.get("last_active", data.get("attached_time", now))
                if (now - last_active) > 300: # 5 minutes of inactivity
                    data["trust_score"] = max(0.1, data["trust_score"] - decay_rate)
                    print(f"📉 [TRUST-DECAY]: Agent '{aid}' trust decayed due to inactivity.")

    def orchestrate_complex_task(self, main_task):
        """
        Orchestration Logic: Planner Decomposes -> Router Distributes.
        """
        print(f"\n🧠 [HIVE-ORCHESTRATOR]: Planning for: '{main_task}'")
        
        # 1. PLAN (Decompose)
        task_graph = self.planner.decompose_task(main_task)
        
        # 2. ROUTE (Assign)
        assignments = self.router.route_task_graph(task_graph)
        
        print(f"🚀 [ORCHESTRATION COMPLETE]: Task '{main_task}' has been distributed among the Hive Swarm.")
        return {
            "status": "ORCHESTRATED",
            "task_graph": task_graph,
            "assignments": assignments,
            "agent_count": len(task_graph)
        }
