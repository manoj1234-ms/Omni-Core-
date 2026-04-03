import json
try:
    from omni_components.hippocampus import Hippocampus
    from omni_components.limbic_system import LimbicSystem
except ModuleNotFoundError:
    from hippocampus import Hippocampus
    from limbic_system import LimbicSystem

class CognitiveBridge:
    """
    The Universal AI Attachment Layer.
    Allows external AI models (like Antigravity) to communicate with the Omni-Core
    through a standardized logic-exchange interface.
    """
    def __init__(self):
        self.hippocampus = Hippocampus()
        self.limbic = LimbicSystem()

    def process_ai_input(self, agent_id, payload):
        """
        Processes a JSON payload from any attaching AI agent.
        Payload format: {
            "intent": "store" | "retrieve" | "signal_emotion",
            "data": { ... }
        }
        """
        intent = payload.get("intent")
        data = payload.get("data", {})
        
        print(f"\n🌉 [BRIDGE]: Connection from Agent '{agent_id}' | Intent: '{intent}'")

        if intent == "store":
            # Any AI can store its 'learnings' locally
            category = data.get("category", "general")
            fact = data.get("fact", "")
            self.hippocampus.add_memory(category, fact)
            return {"status": "success", "message": f"Memory stored in {category}"}

        elif intent == "retrieve":
            # Any AI can query the Omni-Core database for context
            query = data.get("query", "")
            results = self.hippocampus.retrieve_relevant_context(query)
            return {"status": "success", "results": results}

        elif intent == "signal_emotion":
            # AI reports if the current situation is stressful
            confidence = data.get("confidence", 0.5)
            self.limbic.update_state(confidence * 10) # Scaling for limbic math
            return {"status": "success", "dopamine": self.limbic.dopamine, "cortisol": self.limbic.cortisol}

        else:
            return {"status": "error", "message": "Unknown Intent"}

if __name__ == "__main__":
    # 🧪 Self-Test: Simulating an external AI (Antigravity) attaching to the Bridge
    bridge = CognitiveBridge()
    
    # 1. Antigravity stores a new learning
    learning_payload = {
        "intent": "store",
        "data": {"category": "architecture", "fact": "The Universal Cognitive Bridge is now operational."}
    }
    print(bridge.process_ai_input("ANTIGRAVITY_v1", learning_payload))

    # 2. Antigravity signals stress after a complex task
    stress_payload = {
        "intent": "signal_emotion",
        "data": {"confidence": 0.2} # Low confidence, high stress
    }
    print(bridge.process_ai_input("ANTIGRAVITY_v1", stress_payload))
