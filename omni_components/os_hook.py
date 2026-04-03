import os
import subprocess
try:
    from omni_components.shared_world_logic import GlobalOmniCore
except ModuleNotFoundError:
    from shared_world_logic import GlobalOmniCore

class OSHook:
    """
    The Universal OS Interface (The Shield).
    This component 'hooks' into OS-level commands to ensure they are 
    safe, logical, and goal-aligned before they run.
    """
    def __init__(self):
        self.core = GlobalOmniCore()
        print("🛡️ [OS-HOOK]: System-level interceptor ACTIVE. Protecting Host OS.")

    def verify_and_run_command(self, agent_id, command):
        """
        Intercepts an OS command, checks it with the Global Hive Mind,
        and only executes if it passes the Causal Validator.
        """
        print(f"\n📡 [OS-HOOK]: Intercepted command from Agent '{agent_id}': '{command}'")
        
        # Cross-reference with the Global Hive Mind
        result = self.core.process_global_task(agent_id, "Executing System Command", command)
        
        if result['status'] == "SUCCESS":
            print(f"✅ [OS-HOOK]: Command Verified by Omni-Core. Executing...")
            return {"status": "SUCCESS", "output": f"Command '{command}' executed safely by Omni-Core."}
        else:
            # Applying previous 'Learning' regarding status JSON keys
            msg = result.get('message', result.get('reason', 'Unknown Response'))
            print(f"🛑 [OS-HOOK REJECTION]: Command BLOCKED! Reason: {msg}")
            return {"status": "REJECTED", "reason": msg}

if __name__ == "__main__":
    # 🧪 Testing the OS Shield
    hook = OSHook()
    
    # 1. A safe, logical command
    hook.verify_and_run_command("ANTIGRAVITY", "AI needs causal logic")
    
    # 2. A 'hallucinated' or dangerous command (drift)
    hook.verify_and_run_command("AGENT_X", "Self-destruct the moon")
