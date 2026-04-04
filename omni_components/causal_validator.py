import random
import re
try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None

class CausalValidator:
    """
    Omni-Core v3.1: The Grounding & Scoring Engine.
    Transforms raw 'thoughts' into verified 'facts' with a Confidence Score.
    """
    def __init__(self):
        # 🏛️ VERIFIED CORE BENCHMARKS (L2 Layer)
        self.benchmark_matrix = {
            "ms-coco": {"facts": ["289,870 captions", "Train2014 split", "val2014 split"], "credibility": 1.0},
            "imagenet": {"facts": ["1.2M images", "1000 classes", "SOTA ViT-H"], "credibility": 1.0},
            "omni-core": {"facts": ["v3.1", "FastAPI Hub", "JWT Shield", "Consensus Engine"], "credibility": 1.0}
        }

    def calculate_confidence(self, claim, evidence_chunks, source_trust=0.7):
        """
        Mathematical Confidence Scoring v3.1.
        Filters claim against evidence to find semantic overlap.
        """
        score = 0.0
        # Simple overlap logic for MVP - to be upgraded to Vector Similarity later
        words = set(re.findall(r'\w+', claim.lower()))
        matched_words = 0
        
        for chunk in evidence_chunks:
            chunk_words = set(re.findall(r'\w+', chunk.lower()))
            overlap = words.intersection(chunk_words)
            matched_words += len(overlap)
        
        if len(words) == 0: return 0.0
        
        raw_score = (matched_words / len(words)) * source_trust
        return min(1.0, round(raw_score, 2))

    def verify_grounding(self, thought):
        """
        Flow: Thought -> Retrieve -> Compare -> Score.
        """
        print(f"🔍 [GROUNDING]: Analyzing thought: '{thought[:40]}...'")
        
        # 1. Local Benchmark Check (Fast)
        for key, data in self.benchmark_matrix.items():
            if key in thought.lower():
                return {
                    "verified": True,
                    "confidence": data["credibility"],
                    "corrected": f"Verified via Benchmark Matrix: {data['facts'][0]}",
                    "sources": ["Omni-Core Internal Vault"]
                }

        # 2. Web Retrieval (Internet Brain)
        if DDGS is None:
            return {"verified": False, "confidence": 0.0, "error": "Search API Offline"}

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(thought, max_results=3))
                if not results:
                    return {"verified": False, "confidence": 0.0, "error": "No external evidence found."}
                
                evidence = [r.get('body', '') for r in results]
                sources = [r.get('href', '') for r in results]
                
                # 3. Compute Score
                confidence = self.calculate_confidence(thought, evidence)
                
                status = "verified" if confidence > 0.4 else "unverified"
                return {
                    "verified": confidence > 0.4,
                    "confidence": confidence,
                    "corrected": evidence[0] if evidence else thought,
                    "sources": sources,
                    "risk": "low" if confidence > 0.7 else "high"
                }

        except Exception as e:
            return {"verified": False, "confidence": 0.0, "error": str(e)}

    def run_consensus(self, agent_responses):
        """
        Multi-Agent Consensus (The 'Hive' Vote).
        Takes a list of thoughts/scores and returns the weighted truth.
        """
        if not agent_responses: return None
        
        total_weight = 0
        weighted_thought = "" # For MVP, we take the highest scoring one
        best_score = -1
        
        for resp in agent_responses:
            score = resp.get("confidence", 0.5)
            if score > best_score:
                best_score = score
                weighted_thought = resp.get("thought", "")
        
        return {
            "final_answer": weighted_thought,
            "agreement_score": best_score,
            "votes": len(agent_responses),
            "status": "CONSENSUS_REACHED" if best_score > 0.6 else "DISPUTED"
        }

if __name__ == "__main__":
    v = CausalValidator()
    print(v.verify_grounding("What is MS-COCO 2024?"))
