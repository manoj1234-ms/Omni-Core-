class GoalTree:
    """
    The Executive Control Network (Problem 5).
    Tracks the Primary Network's actions against the Master Goal
    to eliminate Agentic Drift.
    """
    def __init__(self, master_goal="Build a sentient AGI prototype"):
        self.master_goal = master_goal
        self.sub_tasks = []
        self.drift_count = 0
        print(f"🎯 [GOAL-TREE]: Master Objective set to: '{self.master_goal}'")

    def evaluate_alignment(self, action_description):
        """
        Determines if the current action aligns with the Master Goal.
        In a full system, this would use semantic similarity (e.g., BERT/T5).
        For Alpha, we use keyword-overlap and context-matching.
        """
        action_description = action_description.lower()
        core_keywords = ["agi", "prototype", "cognitive", "memory", "logic", "emotion", "causal", "sentient", "core"]
        
        # Check alignment
        is_aligned = any(keyword in action_description for keyword in core_keywords)
        
        if is_aligned:
            print(f"✅ [GOAL-TREE]: Action '{action_description}' is ALIGNED with the Master Goal.")
            return True, 1.0 # High alignment
        else:
            self.drift_count += 1
            print(f"🛑 [GOAL-TREE ALERT]: Agentic Drift detected ({self.drift_count})! Action '{action_description}' is OUT OF SCOPE.")
            return False, 0.0 # Total drift

    def generate_corrective_intention(self):
        """
        Signals the system to return to the core goal.
        """
        print(f"🔄 [GOAL-TREE]: Generating Corrective Intention...")
        return f"Return to Objective: {self.master_goal}"

if __name__ == "__main__":
    # 🧪 Self-Test: Detecting Drift vs. Alignment
    gt = GoalTree()
    
    # 1. Aligned Action
    gt.evaluate_alignment("Building a memory-augmented logic core.")
    
    # 2. Drifting Action
    gt.evaluate_alignment("Searching the web for cute cat pictures.")
    
    # 3. Corrective Intention
    print(gt.generate_corrective_intention())
