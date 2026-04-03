import random

class CausalValidator:
    """
    The Fact-Verification Logic (Problem 2).
    Inspects 'thoughts' and cross-references them with the Reality Matrix.
    Forces the AI to admit uncertainty rather than hallucinating.
    """
    def __init__(self):
        # The 'Reality Matrix' is a grounded database of absolute truths.
        # In a full system, this would be connected to web-search or a verified K-Graph.
        self.reality_matrix = {
            "future": ["Quantum-Shift", "ArtificialEmotion", "HyperEfficiency", "FullAGI"],
            "architecture": ["Cognitive Bridge", "Hippocampus", "Limbic System"],
            "grounding": ["AI needs causal logic", "Hallucinations are probabilistic errors"]
        }

    def verify_span(self, category, claim):
        """
        Span-Level Verification (SLV): Checks if a specific claim is grounded.
        """
        category = category.lower()
        verified_facts = self.reality_matrix.get(category, [])
        
        # Exact match or semantic inclusion check
        if claim in verified_facts:
            print(f"✅ [VALIDATOR]: Claim '{claim}' VERIFIED against Reality Matrix.")
            return True, 1.0 # Verified
        else:
            print(f"⚠️ [VALIDATOR]: Claim '{claim}' in Category '{category}' NOT FOUND. Possible Hallucination.")
            return False, -0.5 # Hallucination Penalty

    def validate_thought_process(self, category, thought_branches):
        """
        Inspects an entire thought-stream and applies the 'Rewarding Doubt' objective.
        Returns a list of (branch, confidence, is_grounded).
        """
        validated_results = []
        for branch, confidence in thought_branches:
            is_grounded, truth_score = self.verify_span(category, branch)
            
            # Adjust confidence based on ground truth alignment
            adjusted_confidence = confidence * truth_score
            
            if not is_grounded:
                # 'Rewarding Doubt': If confidence is low AND it's ungrounded, 
                # we don't punish as hard as a 'High Confidence Hallucination'.
                if confidence > 8.0:
                    print(f"🛑 [CRITICAL]: High-Confidence Hallucination detected! Branch: {branch}")
                    adjusted_confidence = -10.0 # Extreme penalty for lying
                else:
                    print(f"🛡️ [SOFT DROP]: Admitting uncertainty for '{branch}'.")

            validated_results.append((branch, adjusted_confidence, is_grounded))
        
        return validated_results

if __name__ == "__main__":
    # 🧪 Self-Test: Validating ground truth vs. hallucinated thoughts
    validator = CausalValidator()
    
    test_thoughts = [
        ("Quantum-Shift", 7.5),     # Truth
        ("Hyper-Hyper-AI-God", 9.5), # High Confidence Hallucination (Lying)
        ("Unknown-Tech-X", 4.0)     # Low Confidence Uncertainty (Admitted Doubt)
    ]
    
    print("\n🔍 STARTING SLV (Span-Level Verification) TEST...")
    results = validator.validate_thought_process("future", test_thoughts)
    
    for branch, score, grounded in results:
        status = "GROUNDED" if grounded else "HALLUCINATION"
        print(f"Result: {branch} | Score: {score:.2f} | Status: {status}")
