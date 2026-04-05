import json
import os
import time
try:
    from supabase import create_client, Client
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    create_client = None

class Hippocampus:
    """
    The L2/L3 Memory Vault (Supabase/PostgreSQL Persistent).
    Handles LOCAL semantic L2 storage (JSON) and GLOBAL L3 collective store (Supabase).
    All AI systems globally sync their verified logic to the L3 cloud store.
    """
    def __init__(self, storage_path="omni_memories.json"):
        self.storage_path = storage_path
        self.local_store = self._load_local()
        
        # 🔵 Supabase/Postgres Connection (The L3 Global Collective)
        self.supabase_url = os.environ.get("SUPABASE_URL", "https://your-project.supabase.co")
        self.supabase_key = os.environ.get("SUPABASE_KEY", "your-service-role-key")
        self.supabase: Client = None

        if create_client and "supabase.co" in self.supabase_url:
            try:
                self.supabase = create_client(self.supabase_url, self.supabase_key)
                print("🌊 [HIPPOCAMPUS]: Cloud Nexus (Supabase/Postgres) CONNECTED. L3 Global Sync active.")
            except Exception as e:
                print(f"⚠️ [HIPPOCAMPUS]: Cloud Offline. Fallback to Local L2 only. (Error: {e})")
        
        # 🔴 Stage 3: Active Session Workspace (Collaborative Memory)
        self.active_sessions = {} # {task_id: {data: {}, logs: []}}
        self.shared_files = {} # {task_id: [filenames]}
        
        # 🔗 Phase 3: Cognitive Knowledge Graph
        self.knowledge_graph = self._load_graph() # {subject: [{relation: X, object: Y}]}
        
        print(f"🧠 [HIPPOCAMPUS]: Local Vault L2 initialized at '{storage_path}'")
        print(f"🧬 [HIPPOCAMPUS-V3]: Knowledge Graph Engine ACTIVE.")

    def update_session_workspace(self, task_id, key, value):
        """
        Shared Workspace: Agents can read/write data for a specific task.
        """
        if task_id not in self.active_sessions:
            self.active_sessions[task_id] = {"data": {}, "logs": []}
        
        self.active_sessions[task_id]["data"][key] = value
        self.active_sessions[task_id]["logs"].append(f"[{int(time.time())}] [UPDATE]: {key} set to {value}")
        print(f"📡 [SESSION-SYNC]: {task_id} updated -> {key}: {value}")

    def get_session_workspace(self, task_id):
        """
        Retrieves the current state of a task's shared workspace.
        """
        return self.active_sessions.get(task_id, {"data": {}, "logs": ["No active session found."]})

    def _load_local(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return {"verified_world_logic": ["Initial collective context active."]}

    def _load_graph(self):
        graph_path = self.storage_path.replace(".json", "_graph.json")
        if os.path.exists(graph_path):
            with open(graph_path, "r") as f:
                return json.load(f)
        return {}

    def save_local(self):
        # Save L2 Vault
        with open(self.storage_path, "w") as f:
            json.dump(self.local_store, f, indent=4)
        
        # Save Knowledge Graph
        graph_path = self.storage_path.replace(".json", "_graph.json")
        with open(graph_path, "w") as f:
            json.dump(self.knowledge_graph, f, indent=4)

    def add_triplet(self, s, r, o):
        """
        Phase 3: Adds a knowledge triplet to the graph.
        """
        if s not in self.knowledge_graph:
            self.knowledge_graph[s] = []
        
        triplet = {"relation": r, "object": o, "verified_at": time.time()}
        if triplet not in self.knowledge_graph[s]:
            self.knowledge_graph[s].append(triplet)
            print(f"🕸️ [GRAPH-SYNC]: New edge: {s} --[{r}]--> {o}")
            self.save_local()

    def query_graph(self, subject):
        """
        Phase 3: Retrieves all known relationships for a subject.
        """
        return self.knowledge_graph.get(subject, [])

    def retrieve_relevant_context(self, query):
        """
        Retrieves context from Local L2, Cloud L3 (Supabase), and Knowledge Graph.
        """
        query = query.lower()
        results = self.local_store.get(query, [])

        # 1. Knowledge Graph Retrieval (Subject-Relation-Object)
        # Look for the query as a subject in the triplet graph
        triplets = self.query_graph(query)
        for t in triplets:
            rel_fact = f"[RELATION]: {query} --({t['relation']})--> {t['object']}"
            if rel_fact not in results:
                results.append(rel_fact)

        # 2. Cloud L3 Retrieval (Supabase)
        if self.supabase:
            try:
                # Query the 'logic_memories' table in Supabase
                response = self.supabase.table("logic_memories").select("fact").eq("category", query).execute()
                cloud_facts = [r['fact'] for r in response.data]
                for fact in cloud_facts:
                    if fact not in results:
                        results.append(fact)
                print(f"📡 [GLOBAL-SYNC]: Merged {len(cloud_facts)} facts + {len(triplets)} triplets.")
            except Exception:
                pass 
                
        if not results:
            results = ["Grounding-Default-Logic"]
            
        return results

    def add_memory(self, category, fact, agent_id="SYSTEM"):
        # 1. Update Local L2
        if category not in self.local_store:
            self.local_store[category] = []
        if fact not in self.local_store[category]:
            self.local_store[category].append(fact)
            print(f"📝 [L2 CACHE]: Fact cached locally: {fact}")
            self.save_local()

        # 2. Sync to Cloud L3 (Supabase)
        if self.supabase:
            try:
                self.supabase.table("logic_memories").upsert({
                    "category": category, 
                    "fact": fact,
                    "agent_id": agent_id,
                    "created_at": "now()"
                }).execute()
                print(f"🌊 [L3 SUPABASE-SYNC]: Fact uploaded to Global Postgres Pool.")
            except Exception as e:
                print(f"🛑 [L3 ERROR]: Sync failed: {e}")

if __name__ == "__main__":
    vault = Hippocampus()
    vault.add_memory("verified_world_logic", "Universal AGI Infrastructure active.")
