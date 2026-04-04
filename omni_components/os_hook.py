import os
import subprocess
try:
    from omni_components.shared_world_logic import GlobalOmniCore
except ModuleNotFoundError:
    from shared_world_logic import GlobalOmniCore

class OSHook:
    """
    The Hands of AGI (OS Autonomy).
    This component allows the Omni-Core to interact with the local OS
    directly, but only after passing through the Causal Validator
    and ensuring the 'Cortisol' (stress/risk) level is safe.
    """
    def __init__(self, core=None):
        self.core = core if core else GlobalOmniCore()
        # Restricted command list for safety
        self.blacklist = ["rm -rf", "del /s", "format", "shutdown", "wget", "curl", "> /dev/"]
        print("🦾 [OS-HOOK]: Hands of AGI ACTIVE. Direct OS manipulation ENABLED.")

    def _is_safe(self, command):
        """Checks if the command contains any blacklisted terms."""
        for term in self.blacklist:
            if term in command.lower():
                return False
        return True

    def execute_system_command(self, agent_id, command):
        """
        Processes and executes a system command autonomously.
        """
        print(f"\n📡 [OS-HOOK]: Command Signal: '{command}' (Agent: {agent_id})")

        # 1. BRAIN CHECK (Causal Validation)
        result = self.core.process_global_task(agent_id, "Direct System Control", command)

        # 2. LIMBIC CHECK (Cortisol/Safety)
        stress_level = self.core.limbic.cortisol
        if stress_level > 7.0:
            print(f"🛑 [SAFETY BLOCK]: High Cortisol ({stress_level:.2f}). System is too unstable for OS access.")
            return {"status": "BLOCKED", "reason": "High Limbic Stress. Execution Paused."}

        # 3. BLACKLIST CHECK
        if not self._is_safe(command):
            print(f"🗡️ [RESTRICTED]: Command contains dangerous syntax. BLOCKED.")
            return {"status": "BLOCKED", "reason": "Restricted Command Syntax Detected."}

        if result['status'] == "SUCCESS":
            print(f"✅ [OS-HOOK]: Verified. Executing on Host System...")
            try:
                # 4. ACTUAL EXECUTION
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()
                return {
                    "status": "SUCCESS",
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": process.returncode
                }
            except Exception as e:
                return {"status": "ERROR", "message": str(e)}
        else:
            msg = result.get('message', 'Validation Failed')
            print(f"🛑 [OS-HOOK]: Rejection: {msg}")
            return {"status": "REJECTED", "reason": msg}

    def write_autonomous_file(self, filename, content):
        """Hands of AGI: Writing files to the workspace."""
        if self.core.limbic.cortisol > 5.0:
            return {"status": "ERROR", "reason": "Stress too high to write safely."}
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"📝 [OS-HOOK]: Written autonomous file: '{filename}'")
            return {"status": "SUCCESS", "file": filename}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    # 🧪 Testing OS Autonomy
    hook = OSHook()
    
    # 1. A safe check
    res = hook.execute_system_command("ANTIGRAVITY", "echo 'Omni-Core is Alive'")
    print(f"Output: {res.get('stdout', '')}")
    
    # 2. A forbidden attempt
    hook.execute_system_command("ROGUE_AGENT", "rm -rf /")
