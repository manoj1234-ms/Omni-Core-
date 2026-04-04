# 🎯 Omni-Core MVP Roadmap: From Hub to Cortex

This roadmap focuses on building a **Real, Executable AGI System** step-by-step, prioritizing stability and security over buzzwords.

---

## 🟢 Phase 1: The Secure Hub (MVP v1.x) - [CURRENT]

### ✅ v1.0: The Secure Foundation (COMPLETED)
- **FastAPI Hub Server**: Minimal, high-performance API.
- **JWT Authentication**: Secure per-agent session tokens.
- **Agent Registry**: In-memory storage for ID, Role, and Capabilities.
- **Basic Keyword Router**: Routing tasks based on capability match.

### 📅 v1.1: Multi-Agent Orchestration & Sync
- **Enhanced Router**: Implement "Scoring" for agents (Trust + Latency).
- **Heartbeat Protocol**: Automatically remove disconnected or "Dead" agents from the registry.
- **Parallel Execution**: Allow the Hub to trigger multiple agents for sub-tasks simultaneously.

### 📅 v1.2: The First Cognitive Node
- **LLM Integration**: Connect a real LLM (OpenAI API or local Llama 3) as a specialized "Reasoning" node.
- **Semantic Routing**: Use the LLM node to categorize incoming tasks instead of hardcoded keywords.

### 📅 v1.3: Persistence & State (The Lite Hippocampus)
- **Database Backend**: Migrate In-memory registry to SQLite/Redis.
- **Session Logs**: Record every thought and action to a persistent JSON/Database for auditing.

---

## 🟡 Phase 2: The Autonomous Cortex (v2.x)

### 📅 v2.0: The Planner (Task Graph / DAG)
- **Recursive Decomposition**: Using an LLM to split "Build X" into a Dependency Graph.
- **Status Triggers**: Monitor task completion (Success/Failure) and trigger "Self-Healing" retries.

### 📅 v2.5: The Shared Workspace (Hive Workspace)
- **Collective Memory**: Enabling agents to read/write shared context (Session State) to solve multi-step problems together.
- **Vector Search**: Use FAISS to allow nodes to search the "Global Hive Wisdom."

---

## 🔴 Phase 3: Global Scaling (v3.x)

### 📅 v3.0: Decentralized Consensus & Swarms
- **Consensus Logic**: Multiple agents must "Verify" a thought before it's saved as "Truth."
- **Cloud Nexus**: High-availability deployment on Kubernetes/Render with Global Persistence.

---

## 🏁 Immediate Next Step: v1.1 (Monitoring & Better Routing)
**Goal**: Ensure the Hive stays "Alive" and distributes tasks based on trust and speed.

---
*Authored by Lead Architect & Antigravity AI*
