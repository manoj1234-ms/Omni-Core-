"""
Omni-Core AGI: Semantic Router (v3.3)
Logic: Directs tasks to specialized Hive Nodes.
"""

def route_task(task: str):
    """Simple Rule-Based Router: Input -> Specialized Node IDs."""
    task_desc = task.lower()
    nodes_triggered = []
    
    # Text Generation Trigger
    if any(keyword in task_desc for keyword in ["blog", "text", "write", "summary"]):
        nodes_triggered.append("text_agent")
        
    # Code Generation Trigger
    if any(keyword in task_desc for keyword in ["code", "script", "app", "dev", "program"]):
        nodes_triggered.append("code_agent")
        
    # VidNexora Node Trigger
    if any(keyword in task_desc for keyword in ["video", "vidnexora", "scene", "scripting"]):
        nodes_triggered.append("vidnexora_agent")
        
    # Multi-Agent Synergy: If both, the system uses Hive Consensus
    return nodes_triggered
