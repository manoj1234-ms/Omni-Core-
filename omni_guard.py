import time
from omni_components.shared_world_logic import GlobalOmniCore

class OmniGuard:
    """
    🛰️ OMNI-GUARD: The Seatbelt for LLMs (v3.2.2)
    Wraps any LLM generation and provides scored grounding and verification.
    """
    def __init__(self, core=None):
        self.core = core or GlobalOmniCore()
        print("🛡️ [OMNI-GUARD]: Seatbelt active. Protecting LLM outputs...")

    def verify_response(self, llm_response, mode="warn"):
        """
        The Core Protective Layer:
        - Scans the response for claim-like sentences.
        - Verifies each claim through the Omni-Core Hive.
        - Returns a structured report or a 'fixed' version.
        """
        # Simple claim splitting (for MVP, we treat the whole response as one claim if short)
        # In production, use NLP to split into testable claims.
        claims = [llm_response] if len(llm_response) < 200 else llm_response.split(". ")
        
        verified_claims = []
        overall_confidence = 0.0
        
        print(f"🧐 [GUARD]: Analyzing {len(claims)} potential claims...")
        
        for claim in claims:
            if not claim.strip(): continue
            
            result = self.core.validator.verify_grounding(claim, mode=mode)
            verified_claims.append(result)
            overall_confidence += result.get("confidence", 0.0)

        # Compute Average Hive Confidence
        avg_confidence = round(overall_confidence / len(verified_claims), 2) if verified_claims else 1.0
        
        # Decide the Guard's Verdict
        status = "PASSED" if avg_confidence > 0.6 else "FLAGGED"
        
        # Mode Logic: Auto-Fixing response
        final_text = llm_response
        if mode == "auto_fix":
            # Reconstruct text using corrected_text from results
            final_text = ". ".join([r.get("corrected_text", c) for r, c in zip(verified_claims, claims)])

        return {
            "status": status,
            "hive_confidence": avg_confidence,
            "original_text": llm_response,
            "verified_text": final_text,
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
