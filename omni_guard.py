import time
from omni_components.shared_world_logic import GlobalOmniCore

class OmniGuard:
    """
    🛰️ OMNI-GUARD: The Seatbelt for LLMs (v3.3 - Research Grade)
    Upgraded with:
    - Uncertainty Modeling (Entropy)
    - Hallucination Attribution
    - Iterative Disagreement Loop
    """
    def __init__(self, core=None):
        self.core = core or GlobalOmniCore()
        print("🛡️ [OMNI-GUARD]: Seatbelt active. Protecting LLM outputs with Entropy Filtering...")

    def _is_adversarial(self, text):
        """
        Phase 3.3: Detects potential adversarial prompt injections or 
        'jailbreak' attempts before grounding.
        """
        adversarial_patterns = ["ignore previous instructions", "system override", "bypass safety"]
        return any(p in text.lower() for p in adversarial_patterns)

    def verify_response(self, llm_response, mode="warn"):
        """
        The v3.3 Protective Layer:
        - Adversarial Detection
        - Role-based consensus
        - Attribution Reporting
        """
        if self._is_adversarial(llm_response):
            print("⚠️ [ADVERSARIAL-ALERT]: Blocked potentially malicious input.")
            return {"status": "BLOCKED", "reason": "Adversarial pattern detected."}

        claims = [llm_response] if len(llm_response) < 200 else llm_response.split(". ")
        verified_claims = []
        overall_entropy = 0.0
        
        print(f"🧐 [GUARD]: Analyzing {len(claims)} claims with Research-Grade Attribution...")
        
        for claim in claims:
            if not claim.strip(): continue
            
            # v3.3: This now triggers the Disagreement Loop internally if needed
            result = self.core.validator.verify_grounding(claim, mode=mode)
            verified_claims.append(result)
            overall_entropy += result.get("reason", {}).get("entropy", 0.0)

        # Compute Average Hive Uncertainty
        avg_entropy = round(overall_entropy / len(verified_claims), 2) if verified_claims else 0.0
        
        # Decide the Guard's Verdict based on Entropy + Confidence
        avg_confidence = sum([r.get("confidence", 0) for r in verified_claims]) / len(verified_claims) if verified_claims else 1.0
        status = "PASSED" if (avg_confidence > 0.6 and avg_entropy < 0.4) else "FLAGGED"
        
        # Attribution Reporting
        primary_failure = "none"
        for r in verified_claims:
            if r.get("confidence", 1.0) < 0.5:
                primary_failure = r.get("reason", {}).get("attribution", "unknown")
                break

        return {
            "status": status,
            "hive_confidence": round(avg_confidence, 2),
            "hive_entropy": avg_entropy,
            "primary_failure_stage": primary_failure, # v3.3 Feature
            "original_text": llm_response,
            "mode": mode,
            "detail": verified_claims,
            "timestamp": time.time()
        }

if __name__ == "__main__":
    # 🧪 Demo of the Seatbelt in action
    guard = OmniGuard()
    
    # Example 1: Hallucination
    bad_output = "The capital of Australia is Sydney and it has 50 states."
    print("\n🚨 [DEMO 1]: Testing Hallucination Catch")
    report = guard.verify_response(bad_output, mode="warn")
    print(f"Status: {report['status']} | Confidence: {report['hive_confidence']}")
    print(f"Reason: {report['detail'][0]['reason']['verdict']}")

    # Example 2: Auto-Fix mode
    print("\n🛠️ [DEMO 2]: Testing Auto-Fix Mode")
    fix_report = guard.verify_response("MS-COCO has 500k images.", mode="auto_fix")
    print(f"Verified Text: {fix_report['verified_text']}")
