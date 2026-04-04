import json
import time

class PlannerEngine:
    """
    The Brain (Cortex Stage 1).
    Responsible for breaking down complex 1-line tasks into a Task Graph (DAG).
    Can be later connected to a high-reasoning LLM (like GPT-4o or Claude 3.5).
    """
    def __init__(self):
        print("🧠 [PLANNER-ENGINE]: Cognitive Decomposition Module ACTIVE.")

    def decompose_task(self, main_task):
        """
        Simulated Task Decomposition Logic.
        In a full AGI Hub, this would be an LLM call.
        """
        print(f"🧩 [PLANNER]: Decomposing complex task: '{main_task}'")
        
        # Simple Logic Keywords to simulate 'Planning'
        task_graph = []
        
        if "website" in main_task.lower() or "gateway" in main_task.lower():
            task_graph = [
                {"id": "step_1", "subtask": "Architecture Design", "required_cap": "system_design"},
                {"id": "step_2", "subtask": "Implement API Endpoints", "required_cap": "flask"},
                {"id": "step_3", "subtask": "Set up Security / JWT", "required_cap": "python"},
                {"id": "step_4", "subtask": "Final QA and Test", "required_cap": "basic_reasoning"}
            ]
        elif "train" in main_task.lower() or "model" in main_task.lower():
            task_graph = [
                {"id": "step_1", "subtask": "Dataset Preparation", "required_cap": "python"},
                {"id": "step_2", "subtask": "Define Neural Architecture", "required_cap": "system_design"},
                {"id": "step_3", "subtask": "Execute Training Loop", "required_cap": "system_design"},
                {"id": "step_4", "subtask": "Export Weights and Inference", "required_cap": "python"}
            ]
        else:
            task_graph = [
                {"id": "step_1", "subtask": "Analyze and Search Context", "required_cap": "basic_reasoning"},
                {"id": "step_2", "subtask": "Synthesize Logic Answer", "required_cap": "basic_reasoning"}
            ]
            
        return task_graph

if __name__ == "__main__":
    # 🧪 Self-Test
    planner = PlannerEngine()
    plan = planner.decompose_task("Build a secure website with flask")
    for step in plan:
        print(f" -> {step['id']}: {step['subtask']} (Needs: {step['required_cap']})")
