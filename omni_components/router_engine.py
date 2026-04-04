import random

class RouterEngine:
    """
    The Orchestrator (Cortex Stage 2).
    Responsible for assigning tasks to the best-fit agent in the Registry.
    Turns the 'Collective Hive' into a synchronized execution swarm.
    """
    def __init__(self, registry):
        self.registry = registry # Pointer to the core.active_agents
        print("🧭 [ROUTER-ENGINE]: Adaptive Task Distribution System ACTIVE.")

    def route_task_graph(self, task_graph):
        """
        Takes a Task Graph (list of steps) and assigns them to agents.
        """
        print(f"📡 [ROUTER]: Distributing {len(task_graph)} sub-tasks to agents...")
        
        assignments = []
        
        for step in task_graph:
            required_cap = step['required_cap']
            best_agent = self._find_best_agent(required_cap)
            
            assignments.append({
                "step_id": step['id'],
                "subtask": step['subtask'],
                "assigned_to": best_agent,
                "capability_used": required_cap
            })
            print(f" 🔗 [ROUTE]: Assigned '{step['subtask']}' -> Agent '{best_agent}'")
            
        return assignments

    def _find_best_agent(self, capability):
        """
        Naive Registry Search: Finds an agent with the requested capability.
        """
        eligible_agents = []
        
        for agent_id, info in self.registry.items():
            if capability in info.get('capabilities', []):
                eligible_agents.append((agent_id, info.get('trust_score', 0.5)))
                
        if eligible_agents:
            # Sort by Trust Score (Highest first) and pick
            eligible_agents.sort(key=lambda x: x[1], reverse=True)
            return eligible_agents[0][0] # Return agent_id
        else:
            # If no specialist found, return the most trusted general agent (or any agent)
            if self.registry:
                return random.choice(list(self.registry.keys()))
            else:
                return "UNASSIGNED (No Active Nodes)"
