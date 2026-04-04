from omni_connect import OmniHiveConnect
import time

# --- OMNI-CORE V3.1: CONSENSUS HIVE DEMO ---
# Proof that the Hive Mind can resolve conflicting thoughts into a unified truth.

HUB_URL = "https://global-hive-mind.onrender.com"
hive = OmniHiveConnect(hub_url=HUB_URL)
# PRODUCTION HUB: https://global-hive-mind.onrender.com
# LOCAL HUB: http://localhost:5112

if hive.attach(role="Hive-Orchestrator"):
    print("\n🛰️ [SWARM-MODE]: Running Consensus for 3 Virtual Agents...")
    
    # Simulate 3 agents with different thoughts on MS-COCO
    thoughts_to_vote = [
        {"agent_id": "SCOUT-1", "thought": "MS-COCO has 100k images.", "confidence": 0.4},
        {"agent_id": "ANALYST-7", "thought": "MS-COCO 2024 has 289,870 captions.", "confidence": 0.98},
        {"agent_id": "CRITIC-3", "thought": "MS-COCO is irrelevant.", "confidence": 0.15}
    ]
    
    print("\n🤝 [COORDINATING]: Sending all thoughts to the Consensus Engine...")
    result = hive.run_consensus(thoughts_to_vote)
    
    if result:
        print(f"\n🏆 [HIVE-VERDICT]: '{result.get('final_answer')}'")
        print(f"📊 [CONSENSUS SCORE]: {result.get('agreement_score')} | Votes: {result.get('votes')}")
        print(f"📡 [STATUS]: {result.get('status')}")
    else:
        print("\n🛑 [ERROR]: Consensus logic unvailable.")
