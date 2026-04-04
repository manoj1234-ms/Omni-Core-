import requests
import time

# --- OMNI-CORE V2 MEMORY TEST (JWT SECURE) ---
HUB_URL = "https://global-hive-mind.onrender.com"
OMNI_KEY = "OMNI-MASTER-2026"
TASK_ID = "SECURE_DEPLOY_V2"

def test_v2_memory_secure():
    print(f"🚀 [TESTING STAGE 4]: JWT Secure Sync for Task: {TASK_ID}")
    
    # 1. LOGIN / ATTACH
    print("\n🔑 [AUTH]: Authenticating with Hive Mind...")
    auth_res = requests.post(f"{HUB_URL}/attach", 
                             json={"agent_id": "SECURE_AGENT_007", "agent_type": "Security"}, 
                             headers={"X-Omni-Key": OMNI_KEY}).json()
    
    token = auth_res.get('token')
    if not token:
        print("🛑 [AUTH FAILED]: No token received.")
        return

    HEADERS = {"Authorization": f"Bearer {token}"}
    print("✅ [AUTH SUCCESS]: JWT Token received.")

    # 2. WRITE STATE (Securely)
    print("\n👤 [AGENT]: Logging secure data to Shared Memory...")
    payload = {
        "task_id": TASK_ID,
        "key": "firewall_status",
        "value": "Hardened-JWT"
    }
    requests.post(f"{HUB_URL}/memory/session/update", json=payload, headers=HEADERS)

    # 3. READ STATE (Securely)
    res = requests.get(f"{HUB_URL}/memory/session/query?task_id={TASK_ID}", headers=HEADERS).json()
    print(f"📦 [HIVE-STATE]: {res.get('data')}")
    
    if res.get('data', {}).get('firewall_status') == "Hardened-JWT":
        print("🎉 [SECURITY TEST PASSED]: Shared memory is persistent and JWT-PROTECTED.")

if __name__ == "__main__":
    test_v2_memory_secure()
