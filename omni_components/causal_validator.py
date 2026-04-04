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
        The Internet Brain: Scans live web. Returns (Success, Summary).
        """
        if DDGS is None:
            print("⚠️ [INTERNET BRAIN OFFLINE]: 'duckduckgo-search' not installed. Skipping live scan.")
            return False, None
            
        print(f"🌐 [INTERNET SCAN]: '{claim}' not in local matrix. Autonomously searching verified sources...")
        try:
            with DDGS() as ddgs:
                # OMNI-AGI EPISTEMIC FILTER: Enforce search only on highly trusted academic/encyclopedic sources
                strict_query = f"{claim} site:wikipedia.org OR site:arxiv.org OR site:nature.com OR site:edu OR site:gov"
                
                results = list(ddgs.text(strict_query, max_results=3))
                if results:
                    best_match = results[0]
                    content = best_match.get('body', 'No summary available.')
                    source_href = best_match.get('href', 'Unknown Source')
                    summary = f"Source: {source_href} | Detail: {content}"
                    
                    print(f"🌍 [VERIFIED TRUTH DEDUCED]: Match found via trusted source: '{source_href}'")
                    # Injecting into reality matrix permanently
                    if category not in self.reality_matrix:
                        self.reality_matrix[category] = []
                    self.reality_matrix[category].append(claim)
                    return True, summary
                else:
                    print(f"❌ [WEB FAILED]: No reliable evidence found on verified sources (.edu/.gov/wiki) for '{claim}'.")
                    return False, None
        except Exception as e:
            print(f"🛑 [INTERNET ERROR]: Could not fetch data: {e}")
            return False, None

    def verify_span(self, category, claim):
        """
        Span-Level Verification (SLV): Checks if a specific claim is grounded.
        Returns: (is_grounded: bool, truth_score: float, context: str)
        """
        category = category.lower()
        verified_facts = self.reality_matrix.get(category, [])
        
        # 1. Check Local Matrix
        for fact in verified_facts:
            if fact in claim:
                print(f"✅ [VALIDATOR]: Claim '{claim}' VERIFIED via semantic match with '{fact}'.")
                return True, 1.0, f"Verified via local Reality Matrix: '{fact}'"
                
        # 2. Check the Live Internet
        success, summary = self.web_verify(category, claim)
        if success:
            return True, 1.0, summary # Verified via web
            
        print(f"⚠️ [VALIDATOR]: Claim '{claim}' in Category '{category}' NOT FOUND anywhere. Probable Hallucination.")
        return False, -0.5, "No evidence found in Global Reality Matrix or Live Web."

    def validate_thought_process(self, category, thought_branches):
        """
        Inspects an entire thought-stream and applies the 'Rewarding Doubt' objective.
        Returns a list of (branch, confidence, is_grounded, context).
        """
        validated_results = []
        for branch, confidence in thought_branches:
            is_grounded, truth_score, context = self.verify_span(category, branch)
            
            # Adjust confidence based on ground truth alignment
            adjusted_confidence = confidence * truth_score
            
            if not is_grounded:
                # 'Rewarding Doubt'
                if confidence > 8.0:
                    print(f"🛑 [CRITICAL]: High-Confidence Hallucination detected! Branch: {branch}")
                    adjusted_confidence = -10.0 # Extreme penalty for lying
                else:
                    print(f"🛡️ [SOFT DROP]: Admitting uncertainty for '{branch}'.")

            validated_results.append((branch, adjusted_confidence, is_grounded, context))
        
        return validated_results

if __name__ == "__main__":
    # 🧪 Self-Test
    validator = CausalValidator()
    print("\n🔍 STARTING SLV (Span-Level Verification) HIVE-WEB TEST...")
    is_grounded, score, context = validator.verify_span("technology", "What is Python Programming?")
    print(f"Result: {is_grounded} | Score: {score} | Context: {context}")
