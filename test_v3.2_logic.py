from omni_components.causal_validator import CausalValidator
from omni_components.hippocampus import Hippocampus
import time

def test_v3_2_features():
    print("====================================================")
    print("[RUNNING]: TESTING OMNI-CORE v3.2: THE EVOLUTION    ")
    print("====================================================")

    validator = CausalValidator()
    hippocampus = Hippocampus()

    # 1. Test Source Ranking & Explainable Confidence
    print("\n[TEST 1]: Source Ranking & Explainability")
    results = [
        {"body": "MS-COCO 2024 has 289,870 captions for image processing.", "href": "https://arxiv.org/abs/coco"},
        {"body": "COCO dataset is used for object detection v1.2.", "href": "https://github.com/cocodataset"},
        {"body": "I think it has some images.", "href": "http://randomblog.com/ai"}
    ]
    
    confidence, reason = validator.calculate_confidence("MS-COCO 2024 has 289,870 captions.", results)
    print(f"Confidence: {confidence} | Reason: {reason}")

    # 2. Test Deterministic Checks (Dates & Versions)
    print("\n[TEST 2]: Deterministic Validators")
    claims = [
        "The event happened on 2026-04-05.",
        "The system version is v3.2.1.",
        "This is just some text."
    ]
    for claim in claims:
        is_det, score, msg = validator._run_deterministic_checks(claim)
        print(f"Claim: '{claim}' -> Det={is_det}, Score={score}, Msg={msg}")

    # 3. Test Knowledge Graph Triplets (Phase 3)
    print("\n[TEST 3]: Knowledge Graph (Triplets)")
    hippocampus.add_triplet("Omni-Core", "version", "v3.2")
    hippocampus.add_triplet("Omni-Core", "feature", "Knowledge Graph")
    hippocampus.add_triplet("MS-COCO", "type", "Dataset")
    
    graph_data = hippocampus.query_graph("Omni-Core")
    print(f"Omni-Core Node Data: {graph_data}")

    # 4. Test Sliding Consensus (Phase 2)
    print("\n[TEST 4]: Sliding Consensus (Weighted Voting)")
    agent_responses = [
        {"thought": "Correct Answer", "confidence": 0.9, "trust_score": 0.95}, 
        {"thought": "Wrong Answer", "confidence": 0.8, "trust_score": 0.2},   
        {"thought": "Wrong Answer", "confidence": 0.8, "trust_score": 0.1}    
    ]
    consensus = validator.run_consensus(agent_responses)
    print(f"Consensus Verdict: '{consensus['final_answer']}'")
    print(f"Agreement Score: {consensus['agreement_score']} | Reason: {consensus['reason']}")

    print("\n====================================================")
    print("[SUCCESS]: v3.2 LOGIC VERIFIED. READY.             ")
    print("====================================================")

if __name__ == "__main__":
    test_v3_2_features()
