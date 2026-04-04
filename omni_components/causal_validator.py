import random
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class CausalValidator:
    """
    The Fact-Verification Logic (Problem 2).
    Inspects 'thoughts' and cross-references them with the Reality Matrix.
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
            print("⚠️ [INTERNET BRAIN OFFLINE]")
            return False, None
            
        print(f"🌐 [INTERNET SCAN]: '{claim}' - Scanning Global Reality Matrix...")
        try:
            # Using the recommended Context Manager pattern for DDGS v6+
            with DDGS() as ddgs:
                # 1. First attempt: Direct search for high relevance
                results = list(ddgs.text(claim, max_results=3))
                
                if results:
                    best_match = results[0]
                    content = best_match.get('body', 'No summary.')
                    source_href = best_match.get('href', 'Unknown.')
                    summary = f"Verified Context: {content} | Source: {source_href}"
                    
                    if category not in self.reality_matrix:
                        self.reality_matrix[category] = []
                    self.reality_matrix[category].append(claim)
                    return True, summary
                else:
                    print(f"❌ [WEB FAILED]: No results for '{claim}'")
                    return False, None
        except Exception as e:
            print(f"🛑 [INTERNET ERROR]: {e}")
            return False, None

    def verify_span(self, category, claim):
        """
        Returns: (is_grounded, truth_score, context)
        """
        category = category.lower()
        verified_facts = self.reality_matrix.get(category, [])
        for fact in verified_facts:
            if fact.lower() in claim.lower():
                return True, 1.0, f"Verified via Local Matrix: {fact}"
                
        success, summary = self.web_verify(category, claim)
        if success:
            return True, 1.0, summary
            
        return False, -0.5, "No global evidence found."

    def validate_thought_process(self, category, thought_branches):
        validated_results = []
        for branch, confidence in thought_branches:
            is_grounded, truth_score, context = self.verify_span(category, branch)
            adjusted_confidence = confidence * truth_score
            validated_results.append((branch, adjusted_confidence, is_grounded, context))
        return validated_results

if __name__ == "__main__":
    v = CausalValidator()
    print("\n🔍 STARTING HIVE-WEB TEST...")
    # Test with a very common topic to ensure results
    g, s, c = v.verify_span("technology", "What is Python Programming?")
    print(f"Grounded: {g} | Score: {s}")
    if c:
        print(f"Context: {c[:200]}...")
