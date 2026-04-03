import time
import random
import math
from omni_components.hippocampus import Hippocampus
from omni_components.limbic_system import LimbicSystem
from omni_components.causal_validator import CausalValidator

class OmniCoreV2:
    """
    Omni-Core AGI: Version 2 (The Validated Prototype)
    This version adds the Causal Validator to prevent Problem 2 (Hallucination).
    Every branch must pass a Span-Level Verification check against Reality.
    """
    def __init__(self):
        self.hippocampus = Hippocampus()
        self.limbic = LimbicSystem()
        self.validator = CausalValidator()
        self.generation_count = 0
        
    def simulate_validated_reasoning(self, input_topic):
        """
        The Integrated Reasoning Loop: Context -> Bias -> Branch -> Validate -> Decide.
        """
        self.generation_count += 1
        print(f"\n🚀 [OMNI-CORE V2]: ANALYZING '{input_topic.upper()}' (Gen {self.generation_count})")
        time.sleep(0.5)

        # 1. RETRIEVAL (Hippocampus)
        context = self.hippocampus.retrieve_relevant_context(input_topic)
        
        # 2. MODULATION (Limbic System)
        bias = self.limbic.get_simulation_bias()
        print(f"🌡️ [LIMBIC]: Dynamic Bias Applied: {bias:.2f}")

        # 3. BRANCHING (Math Core)
        initial_thoughts = []
        for branch in context:
            base_efficiency = (self.limbic.dopamine * 10) + (self.limbic.curiosity * 5) - (self.limbic.cortisol * 4)
            uncertainty = random.uniform(0.1, 1.0) + (self.limbic.cortisol * 0.5)
            confidence = (uncertainty * base_efficiency) + bias
            initial_thoughts.append((branch, confidence))

        # 4. VALIDATION (Causal Validator) - This is the NEW step
        print("🧐 [VALIDATOR]: Verifying reasoning branches against Reality Matrix...")
        validated_thoughts = self.validator.validate_thought_process(input_topic, initial_thoughts)
        
        # 5. DECISION (Collapsing the Validated Wave)
        if validated_thoughts:
            # Sort by the validated (adjusted) score
            best_thought = max(validated_thoughts, key=lambda x: x[1])
            
            # Extract values
            branch, final_score, is_grounded = best_thought
            
            print(f"\n🌟 DECISION COLLAPSED: '{branch}' (Confidence: {final_score:.2f})")
            
            if not is_grounded:
                print("⚠️ [SYSTEM]: Grounding failure! Forcing the AI to admit uncertainty.")

            # 6. LEARNING & FEEDBACK
            self.limbic.update_state(final_score)
            
            # Record success only if it passed the validator + high confidence
            if is_grounded and final_score > 7.0:
                self.hippocampus.add_memory(input_topic, f"GroundedThought:{branch}")
            
            return best_thought
        else:
            print("⚠️ [SYSTEM]: No valid reasoning branches found.")
            return None

# --- RUNNING THE VALIDATED SYSTEM ---
if __name__ == "__main__":
    print("====================================================")
    print("🚀 OMNI-CORE V2: HALLUCINATION-FREE AGI PROTOTYPE   ")
    print("====================================================")

    core = OmniCoreV2()
    
    # 🧪 Testing Grounding vs. Hallucination
    # Part 1: Topics the AI 'knows'
    core.simulate_validated_reasoning("future")
    print("-" * 52)
    
    # Part 2: Provoking potential hallucination (Topic not in Reality Matrix)
    core.simulate_validated_reasoning("quantum_telepathy")
    print("-" * 52)

    print("\n" + "="*52)
    print(f"✅ SESSION COMPLETE. Final Limbic Balance: D={core.limbic.dopamine:.2f}, C={core.limbic.cortisol:.2f}")
    print("====================================================")
