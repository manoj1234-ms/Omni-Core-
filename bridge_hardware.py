import psutil
import requests
import time
import os

# --- BRAIN-HARDWARE SYNC BRIDGE ---
# This script connects the PC's physical state (CPU Stress) 
# directly to the Omni-Core's Limbic System (Emotional State).
# If the PC is stressed (High CPU), the AGI feels "Cortisol" rise.
# If the PC is idle, the AGI accumulates "Dopamine".

GATEWAY_URL = "http://127.0.0.1:5000"

def run_hardware_bridge():
    print("====================================================")
    print("🧠 [HARDWARE-BRIDGE]: SYNCING PHYSICAL PC TO DIGITAL BRAIN")
    print("====================================================")
    print(f"Target Gateway: {GATEWAY_URL}")
    print("Monitoring CPU Load... (Press Ctrl+C to stop)")

    # Initial system baseline
    try:
        while True:
            # 1. READ PHYSICAL STRESS
            cpu_load = psutil.cpu_percent(interval=1)
            mem_load = psutil.virtual_memory().percent
            
            # 2. CALCULATE BRAIN MODULATION
            dopamine_adj = 0.0
            cortisol_adj = 0.0

            if cpu_load > 60:
                # System is heavy (Stress)
                cortisol_adj = 0.15
                dopamine_adj = -0.05
                status = "STRESSED"
            elif cpu_load < 20:
                # System is calm (Focus/Reward)
                dopamine_adj = 0.10
                cortisol_adj = -0.05
                status = "CALM"
            else:
                # System is in equilibrium
                status = "EQUILIBRIUM"

            # 3. MODULATE BRAIN
            payload = {
                "dopamine": dopamine_adj,
                "cortisol": cortisol_adj
            }
            
            try:
                res = requests.post(f"{GATEWAY_URL}/modulate", json=payload).json()
                d_val = res.get('new_dopamine', 0)
                c_val = res.get('new_cortisol', 0)
                
                # ANSI COLORS for terminal brilliance
                color = "\033[91m" if status == "STRESSED" else "\033[92m" if status == "CALM" else "\033[94m"
                reset = "\033[0m"

                print(f"[{time.strftime('%H:%M:%S')}] CPU: {cpu_load}% | MEM: {mem_load}% | STATUS: {color}{status}{reset} | Brain D: {d_val:.2f}, C: {c_val:.2f}")
            except Exception as e:
                print(f"🛑 [BRIDGE-ERROR]: Gateway offline or broken: {e}")
                time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 [HARDWARE-BRIDGE]: Disconecting brain-hardware link. System shutting down.")

if __name__ == "__main__":
    run_hardware_bridge()
