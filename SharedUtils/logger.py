import datetime

def hive_log(agent_id, message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] 🛰️  [{agent_id.upper()}]: {message}")
