import requests
import time

HUB_URL = "https://global-hive-mind.onrender.com"
HEADERS = {"X-Omni-Key": "OMNI-MASTER-2026"}
AGENT_ID = "TEST_OS_AGENT"

def test_os_autonomy():
    print("🚀 [TESTING OS AUTONOMY]: Connecting to Hive...")
    
    # 1. ATTACH
    r0 = requests.post(f"{HUB_URL}/attach", json={"agent_id": AGENT_ID}, headers=HEADERS)
    print(f"Attach Status: {r0.status_code}")
    
    # 2. SAFE EXECUTE
    print("\n📦 Test 1: Safe Command (echo)")
    r1 = requests.post(f"{HUB_URL}/execute", json={
        "agent_id": AGENT_ID,
        "command": "echo 'Testing OS Autonomy... SUCCESS'"
    }, headers=HEADERS)
    print(f"Execute Status: {r1.status_code}")
    try:
        print(f"Result: {r1.json()}")
    except:
        print(f"Failed Decode: {r1.text[:200]}")

    # 3. FORBIDDEN EXECUTE
    print("\n🛑 Test 2: Dangerous Command (rm -rf)")
    r2 = requests.post(f"{HUB_URL}/execute", json={
        "agent_id": AGENT_ID,
        "command": "rm -rf /"
    }, headers=HEADERS)
    print(f"Forbidden Status: {r2.status_code}")
    try:
        print(f"Result: {r2.json()}")
    except:
        print(f"Failed Decode: {r2.text[:200]}")

    # 4. AUTONOMOUS WRITE
    print("\n📝 Test 3: Autonomous File Write")
    r3 = requests.post(f"{HUB_URL}/write", json={
        "filename": "omni_test_file.txt",
        "content": "This file was written autonomously by Omni-Core AGI."
    }, headers=HEADERS)
    print(f"Write Status: {r3.status_code}")
    try:
        print(f"Result: {r3.json()}")
    except:
        print(f"Failed Decode: {r3.text[:200]}")

if __name__ == "__main__":
    test_os_autonomy()
