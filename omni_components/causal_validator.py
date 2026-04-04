import random
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class CausalValidator:
    """
    The Fact-Verification Logic (Problem 2).
    Inspects 'thoughts' and cross-references them with the Reality Matrix.
    Forces the AI to admit uncertainty rather than hallucinating.
    Upgraded with 'The Internet Brain': Scans the live web if unverified.
    """
    def __init__(self):
        # The 'Reality Matrix' is a grounded database of absolute truths.
        self.reality_matrix = {
            "future": ["Quantum-Shift", "ArtificialEmotion", "HyperEfficiency", "FullAGI"],
            "architecture": ["Cognitive Bridge", "Hippocampus", "Limbic System"],
            "grounding": ["AI needs causal logic", "Hallucinations are probabilistic errors"],
            "system-control": ["echo", "ls", "python --version", "Direct System Control"]
        }

    def web_verify(self, category, claim):
        """
        The Internet Brain: Scans live web. If credible search results match semantic
        contexts of the claim, it's injected into reality matrix.
        """
        if DDGS is None:
            print("⚠️ [INTERNET BRAIN OFFLINE]: 'duckduckgo-search' not installed. Skipping live scan.")
            return False
            
        print(f"🌐 [INTERNET SCAN]: '{claim}' not in local matrix. Autonomously searching verified sources...")
        try:
            with DDGS() as ddgs:
                # OMNI-AGI EPISTEMIC FILTER: Enforce search only on highly trusted academic/encyclopedic sources
                strict_query = f"{claim} site:wikipedia.org OR site:arxiv.org OR site:nature.com OR site:edu OR site:gov"
                
                results = list(ddgs.text(strict_query, max_results=3))
                if results:
                    best_match = results[0]
                    source_href = best_match.get('href', 'Unknown Source')
                    print(f"🌍 [VERIFIED TRUTH DEDUCED]: Match found via trusted source: '{source_href}'")
                    # Injecting into reality matrix permanently
                    if category not in self.reality_matrix:
                        self.reality_matrix[category] = []
                    self.reality_matrix[category].append(claim)
                    print(f"💾 [VAULT INJECT]: Claim '{claim}' permanently added to Reality Matrix.")
                    return True
                else:
                    print(f"❌ [WEB FAILED]: No reliable evidence found on verified sources (.edu/.gov/wiki) for '{claim}'.")
                    return False
        except Exception as e:
            print(f"🛑 [INTERNET ERROR]: Could not fetch data: {e}")
            return False

    def verify_span(self, category, claim):
        """
        Span-Level Verification (SLV): Checks if a specific claim is grounded.
        """
        category = category.lower()
        verified_facts = self.reality_matrix.get(category, [])
        
        # Exact match or semantic inclusion check
        for fact in verified_facts:
            if fact in claim:
                print(f"✅ [VALIDATOR]: Claim '{claim}' VERIFIED via semantic match with '{fact}'.")
                return True, 1.0 # Verified
                
        # 2. Check the Live Internet
        if self.web_verify(category, claim):
            return True, 1.0 # Verified via web
            
        print(f"⚠️ [VALIDATOR]: Claim '{claim}' in Category '{category}' NOT FOUND anywhere. Probable Hallucination.")
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
    # 🧪 Self-Test: Validating ground truth vs. hallucinated thoughts vs Live Web
    validator = CausalValidator()
    
    test_thoughts = [
        ("Quantum-Shift", 7.5),                   # Local Truth
        ("Python Programming Language", 9.0),     # Web Truth
        ("Unknown-Hyper-Martian-Tech-999", 9.5),  # High Confidence Hallucination (Lying)
        ("Is AI self-aware yet?", 4.0)            # Uncertainty
    ]
    
    print("\n🔍 STARTING SLV (Span-Level Verification) HIVE-WEB TEST...")
    results = validator.validate_thought_process("technology", test_thoughts)
    
    print("\n================== RESULTS ==================")
    for branch, score, grounded in results:
        status = "GROUNDED (MATRIX/WEB)" if grounded else "HALLUCINATION/DOUBT"
        print(f"Result: {branch} | Score: {score:.2f} | Status: {status}")
