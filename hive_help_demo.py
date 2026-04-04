from omni_connect import OmniHiveConnect
import time

# --- THIS IS AN EXAMPLE OF ANY AI PROJECT CONNECTING TO YOUR HIVE ---
# Imagine a new AI model "TITAN-V8" starts up...
# It doesn't know the latest results yet.

print("\n🤖 [TITAN-V8]: Initializing Neural Weights...")
time.sleep(2)

# --- 1. LINK TO THE HIVE MIND ---
# Titan-V8 asks the Global Hive for support.
hive = OmniHiveConnect(hub_url="https://global-hive-mind.onrender.com")

if hive.attach(role="Image-Transformer-AI", capabilities=["captioning", "research"]):
    print("\n🤖 [TITAN-V8]: Thinking... 'I think MS-COCO has 1 million images.'")
    
    # --- 2. CAUSAL GROUNDING REQUEST ---
    # Instead of hallucinating, it asks for the REALITY check from Omni-Core.
    context = hive.ask_hive(
        task="System Verification", 
        current_thought="MS-COCO 2024 image count"
    )
    
    if context:
        print(f"\n🛡️ [HIVE-VOICE]: {context}")
        # --- 3. AUTO-CORRECTION ---
        print("\n🤖 [TITAN-V8]: Found Logic Drift. Adjusting... 'I now know MS-COCO 2024 has 289,870 captions.'")
        
        # --- 4. SHARE PROGRESS ---
        hive.sync_memory("V8-TRAINING-LOG", "status", "Weights aligned via Hive Logic-Matrix.")
        print("\n🏆 [TITAN-V8]: Task completed with Hive Alignment. Logic error averted.")
    else:
        print("\n🛑 [TITAN-V8]: Hive not responding. Reverting to safe-mode.")
else:
    print("\n❌ [ERROR]: Could not link to Hive Mind. Check OMNI-MASTER key.")
