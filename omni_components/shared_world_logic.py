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
        
        # v2: Cognitive Cortex Engines (The Brain)
        self.planner = PlannerEngine()
        self.router = RouterEngine(self.active_agents) # Registry pointer
        print("\n🌍 [GLOBAL CORE]: System initialized. Awaiting World-AI connections...")

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
            
        is_grounded, truth_score, shared_context = self.validator.verify_span(category, proposed_action)
        print(f"🔍 [VALIDATOR DEBUG]: Category='{category}', Grounded={is_grounded}, Score={truth_score}")
        
        if is_grounded:
            # 4. LEARNING (The AI teaches the Core)
            print(f"🎓 [CENTRAL LEARNING]: Omni-Core has learned a new verified fact from '{agent_id}': {proposed_action}")
            self.hippocampus.add_memory("verified_world_logic", proposed_action)
            self.limbic.update_state(9.0) # High dopamine for successful world-synthesis
            return {"status": "SUCCESS", "message": "Grounded and Aligned. Collective status updated.", "context": shared_context}
        else:
            self.limbic.update_state(1.0) # High cortisol for global logic error
            return {"status": "WARNING", "message": "Possible Hallucination. Logic does not match Global Reality Matrix."}

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
