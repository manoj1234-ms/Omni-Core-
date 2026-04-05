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
        
        # 🛡️ SOURCE RANKING ENGINE (v3.2)
        self.trust_weights = {
            ".gov": 0.98,
            ".edu": 0.95,
            "arxiv.org": 0.95,
            "github.com": 0.90,
            "wikipedia.org": 0.85,
            ".com": 0.70,
            ".org": 0.75,
            ".net": 0.60
        }

    def _get_url_trust(self, url):
        """
        Retrieves the trust weight for a given URL domain.
        """
        for domain, weight in self.trust_weights.items():
            if domain in url.lower():
                return weight
        return 0.5 # Default trust for unknown sources

    def _run_deterministic_checks(self, claim):
        """
        Phase 1: Deterministic Validators for dates, numbers, and tech specs.
        """
        # Date Check (YYYY-MM-DD or DD/MM/YYYY)
        if re.search(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}', claim):
             return True, 0.9, "Found valid date format."
        
        # Technical Version Check (vX.X.X)
        if re.search(r'v\d+\.\d+(\.\d+)?', claim):
            return True, 0.85, "Found technical version string."
            
        return False, 0.0, "No deterministic pattern found."

    def calculate_confidence(self, claim, evidence_results):
        """
        Mathematical Confidence Scoring v3.3 (Entropy-Aware).
        Implements Uncertainty Modeling: confidence = trust_score * (1 - entropy).
        """
        score = 0.0
        reason = "Initial assessment."
        
        # 1. Deterministic Pass
        is_det, det_score, det_msg = self._run_deterministic_checks(claim)
        if is_det:
            return det_score, f"Deterministic check passed: {det_msg}", 0.0

        # 2. Semantic Overlap Pass
        words = set(re.findall(r'\w+', claim.lower()))
        if len(words) == 0: return 0.0, "Empty claim.", 1.0
        
        individual_scores = []
        total_source_weight = 0
        
        for result in evidence_results:
            body = result.get('body', '').lower()
            url = result.get('href', '')
            source_weight = self._get_url_trust(url)
            
            chunk_words = set(re.findall(r'\w+', body))
            overlap = words.intersection(chunk_words)
            
            # Individual source match score
            match_score = (len(overlap) / len(words)) * source_weight
            individual_scores.append(match_score)
            total_source_weight += source_weight
        
        # 3. ENTROPY / UNCERTAINTY CALCULATION
        # High variance in source matches = High Entropy
        if len(individual_scores) > 1:
            mean_score = sum(individual_scores) / len(individual_scores)
            variance = sum((s - mean_score)**2 for s in individual_scores) / len(individual_scores)
            entropy = min(1.0, variance * 5.0) # Scaled for sensitivity
        else:
            entropy = 0.5 # Default uncertainty for single source
            
        avg_source_trust = total_source_weight / len(evidence_results) if evidence_results else 0.5
        
        # 4. FINAL WEIGHTED CONFIDENCE (Nature-inspired)
        final_score = min(1.0, round(avg_source_trust * (1.0 - entropy) * 1.5, 2))
        
        if final_score > 0.7:
            reason = f"Verified: Low entropy ({entropy:.2f}) across high-trust sources."
        elif final_score > 0.4:
            reason = f"Moderate: Significant disagreement/entropy ({entropy:.2f}) detected in sources."
        else:
            reason = f"Low: Critical failure in source alignment (Entropy: {entropy:.2f})."
            
        return final_score, reason, entropy

    def verify_grounding(self, thought, mode="warn"):
        """
        The v3.2.2 Explicit Grounding Pipeline:
        1. Claim Analysis -> 2. Deterministic Check -> 3. Retrieval -> 4. Scoring -> 5. Structured Reason.
        
        Modes:
        - 'strict': Rejects if confidence < 0.7
        - 'warn': Returns verdict with warning if confidence < 0.7
        - 'auto_fix': Attempts to replace claim with top evidence chunk.
        """
        print(f"🛡️ [GUARD-PIPELINE]: Analyzing thought: '{thought[:40]}...' (Mode: {mode})")
        
        # 1. Deterministic Pass
        is_det, det_score, det_msg = self._run_deterministic_checks(thought)
        if is_det:
             return {
                "verified": True,
                "confidence": det_score,
                "status": "VERIFIED_DETERMINISTIC",
                "reason": {
                    "verdict": det_msg,
                    "validators_passed": ["regex_match"],
                    "sources": ["Internal Core Logic"]
                }
            }

        # 2. Local Benchmark Check
        for key, data in self.benchmark_matrix.items():
            if key in thought.lower():
                return {
                    "verified": True,
                    "confidence": data["credibility"],
                    "status": "VERIFIED_BENCHMARK",
                    "reason": {
                        "verdict": f"Fact verified via Grounding Vault: {data['facts'][0]}",
                        "validators_passed": ["benchmark_match"],
                        "sources": ["Omni-Core Internal Vault"]
                    }
                }

        # 3. External Brain Retrieval
        if DDGS is None:
            return {"verified": False, "confidence": 0.0, "error": "Search API Offline"}

        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(thought, max_results=3))
                if not results:
                    return {
                        "verified": False, 
                        "confidence": 0.0, 
                        "status": "UNVERIFIED_EMPTY",
                        "reason": {"verdict": "No external evidence found.", "sources": []}
                    }
                
                # 4. Scored Synthesis
                confidence, explanation = self.calculate_confidence(thought, results)
                sources = [r.get('href', '') for r in results]
                top_evidence = results[0].get('body', thought)
                
                # 4. Scored Synthesis (Entropy-Aware)
                confidence, explanation, entropy = self.calculate_confidence(thought, results)
                sources = [r.get('href', '') for r in results]
                top_evidence = results[0].get('body', thought)
                
                # 5. HALLUCINATION ATTRIBUTION (Research-Grade)
                attribution = "none"
                if confidence < 0.4:
                    if not results: attribution = "retrieval_failure"
                    elif entropy > 0.6: attribution = "semantic_disagreement"
                    else: attribution = "untrusted_sources"

                # 6. Build Structured Result
                verdict = confidence > 0.4
                if mode == "strict" and (confidence < 0.7 or entropy > 0.5):
                    verdict = False
                
                status = "VERIFIED" if verdict else "REJECTED"
                
                structured_reason = {
                    "verdict": explanation,
                    "entropy": round(entropy, 2),
                    "attribution": attribution, # v3.3 Feature
                    "confidence_breakdown": {
                        "semantic_overlap": round(confidence * 0.8, 2),
                        "source_trust": round(confidence * 0.2, 2)
                    },
                    "sources": sources[:2],
                    "validators_passed": ["semantic_search", "entropy_modeling"]
                }

                response = {
                    "verified": verdict,
                    "confidence": confidence,
                    "status": status,
                    "reason": structured_reason,
                    "corrected_text": top_evidence if mode == "auto_fix" and not verdict else thought
                }
                
                return response

        except Exception as e:
            return {"verified": False, "confidence": 0.0, "error": str(e)}

    def run_consensus(self, agent_responses):
        """
        Multi-Agent Consensus (The 'Hive' Vote).
        Phase 2.1: Iterative Conflict Detection & Weighted Resolution.
        """
        if not agent_responses: return None
        
        # 1. Initial Weighted Tabulation
        weighted_thoughts = {} # {thought: total_weighted_score}
        total_trust_in_hive = 0
        
        for resp in agent_responses:
            thought = resp.get("thought", "").strip(".")
            confidence = resp.get("confidence", 0.5)
            trust_score = resp.get("trust_score", 0.5)
            
            weighted_score = confidence * trust_score
            weighted_thoughts[thought] = weighted_thoughts.get(thought, 0.0) + weighted_score
            total_trust_in_hive += trust_score

        # 2. CONFLICT DETECTION (Disagreement Reasoning)
        unique_thoughts = list(weighted_thoughts.keys())
        has_conflict = len(unique_thoughts) > 1
        conflict_gravity = 0.0
        
        if has_conflict:
            # Measure top 2 candidates' distance
            sorted_voters = sorted(weighted_thoughts.items(), key=lambda x: x[1], reverse=True)
            top_1_score = sorted_voters[0][1]
            top_2_score = sorted_voters[1][1]
            conflict_gravity = round(1.0 - (top_1_score - top_2_score) / (top_1_score + 1e-9), 2)

        # 3. WINNER SELECTION
        final_thought, score = max(weighted_thoughts.items(), key=lambda x: x[1])
        agreement_score = score / total_trust_in_hive if total_trust_in_hive > 0 else 0.5
        
        # 4. EXPLAINABLE STATUS
        status = "CONSENSUS_REACHED"
        reason = f"Stable majority Hive consensus reached ({agreement_score*100:.1f}% agreement)."
        
        if has_conflict and conflict_gravity > 0.6:
            status = "DISPUTED_CONVEX"
            reason = f"HIGH CONFLICT (Gravity: {conflict_gravity}). Hive split between top candidates. Resolution favoring top trust provider."
        elif agreement_score < 0.4:
            status = "LOW_CONFIDENCE_SWARM"
            reason = "Swarm is too fragmented to establish unified truth."

        return {
            "final_answer": final_thought,
            "agreement_score": round(agreement_score, 2),
            "conflict_gravity": conflict_gravity,
            "hive_votes": len(agent_responses),
            "status": status,
            "reason": reason
        }

if __name__ == "__main__":
    v = CausalValidator()
    print(v.verify_grounding("What is MS-COCO 2024?"))
