import threading
import time
import json
try:
    from omni_components.hippocampus import Hippocampus
    from omni_components.limbic_system import LimbicSystem
    from omni_components.causal_validator import CausalValidator
    from omni_components.goal_tree import GoalTree
except ModuleNotFoundError:
    from hippocampus import Hippocampus
    from limbic_system import LimbicSystem
    from causal_validator import CausalValidator
    from goal_tree import GoalTree

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
        print("\n🌍 [GLOBAL CORE]: System initialized. Awaiting World-AI connections...")

    def attach_agent(self, agent_id, agent_type="general"):
        with self.lock:
            self.active_agents[agent_id] = {
                "type": agent_type,
                "attached_time": time.time(),
                "shared_knowledge_count": 0
            }
        print(f"🔗 [GLOBAL CORE]: Agent '{agent_id}' ({agent_type}) ATTACHED to the Universal Hive.")

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
        is_grounded, truth_score = self.validator.verify_span("grounding", proposed_action)
        
        if is_grounded:
            # 4. LEARNING (The AI teaches the Core)
            print(f"🎓 [CENTRAL LEARNING]: Omni-Core has learned a new verified fact from '{agent_id}': {proposed_action}")
            self.hippocampus.add_memory("verified_world_logic", proposed_action)
            self.limbic.update_state(9.0) # High dopamine for successful world-synthesis
            return {"status": "SUCCESS", "message": "Grounded and Aligned. Collective status updated."}
        else:
            self.limbic.update_state(1.0) # High cortisol for global logic error
            return {"status": "WARNING", "message": "Possible Hallucination. Logic does not match Global Reality Matrix."}

# --- SIMULATING THE GLOBAL WORLD AI SYNTHESIS ---
if __name__ == "__main__":
    core = GlobalOmniCore()

    # Agent 1: Medical Assistant AI in India
    core.attach_agent("MEDICAL_AI_01", "Medical")
    
    # Agent 2: Autonomous Transport AI in Germany
    core.attach_agent("DRONE_TRANSPORT_01", "Logistics")

    # 🧬 Scenario: Medical AI learns something and then Drone AI uses that logic
    print("\n" + "="*52)
    print("STEP 1: MEDICAL AI SYNTHESIZES A NEW VERIFIED FACT")
    core.process_global_task("MEDICAL_AI_01", "Verifying patient data logic.", "AI needs causal logic")

    print("\n" + "="*52)
    print("STEP 2: DRONE AI ATTEMPTS TO PERFORM AN OUT-OF-SCOPE TASK")
    # Goal Tree will reject this 'cute cat' drift for health/safety core
    core.process_global_task("DRONE_TRANSPORT_01", "Searching for viral entertainment.", "Find cat videos")

    print("\n" + "="*52)
    print("STEP 3: DRONE AI USES THE SHARED COLLECTIVE MEMORY")
    core.process_global_task("DRONE_TRANSPORT_01", "Optimizing logic for pathfinding.", "AI needs causal logic")
