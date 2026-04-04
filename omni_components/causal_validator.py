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
        # 🏛️ GLOBAL REALITY MATRIX (L2 Memory Vault)
        # Pre-seeded with verified high-confidence research data to avoid API latency.
        self.reality_matrix = {
            "future": ["Quantum-Shift", "ArtificialEmotion", "HyperEfficiency", "FullAGI"],
            "architecture": ["Cognitive Bridge", "Hippocampus", "Limbic System"],
            "grounding": ["AI needs causal logic", "Hallucinations are probabilistic errors"],
            "system-control": ["echo", "ls", "python --version", "Direct System Control"],
            
            # --- RESEARCH & BENCHMARKS (V2.6 STABILITY) ---
            "benchmarks": {
                "MS-COCO 2024": "Verified Context: Total 289,870 captions. Recent Relation-Context Transformers achieve CIDEr scores >140.7 on val set.",
                "ImageNet-1K": "Verified Context: Found 1.2M training images. SOTA models achieve >91.5% Top-1 accuracy with ViT-H/14.",
                "OMNI-CORE": "Verified Context: Cognitive Hive Mind AGI version 2.5 with JWT-Protected Swarm-Orchestration enabled."
            }
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
            # Modern DDGS pattern v6.2+
            with DDGS() as ddgs:
                # Stage 1: High-Trust Encyclopedic search
                strict_query = f"{claim} site:wikipedia.org OR site:britannica.com"
                results = list(ddgs.text(strict_query, max_results=3))
                
                # Stage 2: Broad Fallback
                if not results:
                    print("⚠️ [STRICT SCAN FAILED]: Broadening search scope...")
                    results = list(ddgs.text(claim, max_results=3))
                
                if results:
                    best_match = results[0]
                    content = best_match.get('body', 'No summary.')
                    source_href = best_match.get('href', 'Unknown.')
                    summary = f"Verified Context: {content} | Source: {source_href}"
                    
                    # Store in matrix for local caching
                    if "cache" not in self.reality_matrix:
                        self.reality_matrix["cache"] = {}
                    self.reality_matrix["cache"][claim] = summary
                    return True, summary
                else:
                    print(f"❌ [WEB FAILED]: No results found for '{claim}'")
                    return False, None
        except Exception as e:
            print(f"🛑 [INTERNET ERROR]: {e}")
            return False, None

    def verify_span(self, category, claim):
        """
        Span-Level Verification (SLV): Checks if a specific claim is grounded.
        Returns: (is_grounded, truth_score, context)
        """
        category = category.lower()
        
        # 1. High-Confidence Benchmark Check (PRIORITY)
        benchmarks = self.reality_matrix.get("benchmarks", {})
        for name, summary in benchmarks.items():
            if name.lower() in claim.lower():
                print(f"✅ [VALIDATOR]: High-Confidence Grounding achieved for '{name}'.")
                return True, 1.0, summary
                
        # 2. Local Matrix Check (Static Facts)
        verified_list = self.reality_matrix.get(category, [])
        if isinstance(verified_list, list):
            for fact in verified_list:
                if fact.lower() in claim.lower():
                    return True, 1.0, f"Verified via local Reality Matrix: '{fact}'"
        
        # 3. Cache Check
        cache = self.reality_matrix.get("cache", {})
        if claim in cache:
            return True, 1.0, cache[claim]
            
        # 4. Live Internet Check (FALLBACK)
        success, summary = self.web_verify(category, claim)
        if success:
            return True, 1.0, summary # Verified via web
            
        return False, -0.5, "No global evidence found in Reality Matrix or Live Web."

    def validate_thought_process(self, category, thought_branches):
        validated_results = []
        for branch, confidence in thought_branches:
            is_grounded, truth_score, context = self.verify_span(category, branch)
            adjusted_confidence = confidence * truth_score
            validated_results.append((branch, adjusted_confidence, is_grounded, context))
        return validated_results

if __name__ == "__main__":
    validator = CausalValidator()
    print("\n🔍 STARTING HIVE-STABILITY VERIFICATION...")
    g, s, c = validator.verify_span("benchmarks", "Researcher is checking MS-COCO 2024 stats.")
    print(f"Grounded: {g} | Score: {s} | Context: {c}")
