# 🚀 Implementation Plan: Omni-Core AGI Hive Mind v2 (The Cognitive Cortex)

This plan outlines the structural evolution of Omni-Core from a centralized API Hub into a **Multi-Agent Cognitive Orchestrator**. The goal is to create a dynamic "Hive Mind" where specialized agents collaborate synchronously, guided by a shared memory layer and a centralized planning engine.

---

## 🏗️ v2 Architecture Overview
V2 introduces a **Cortex Logic** layer between the Gateway and the Agents. This layer handles task decomposition, agent assignment (Routing), and collective learning.

### Key Components:
- **Planner Engine (Brain):** Breaks complex 1-line tasks into actionable sub-tasks (Task Graphs).
- **Router Engine:** Assigns sub-tasks to the best-fit agent based on registered `capabilities`.
- **Agent Registry:** A dynamic database of agent "Manifests" (Identity, Roles, Trust Scores).
- **Shared Memory (Hippocampus v2):** Vector-based session persistence + Collective Knowledge.
- **Goal Tree v2:** Monitors sub-task alignment in real-time.

---

## 📅 Roadmap: Phase 3 (The Evolution)

### Stage 1: The Identity Protocol (Registry & Manifests) — [CURRENT FOCUS]
- **Goal**: Transition from `agent_id` strings to full JSON manifests.
- **Tasks**:
  - Update `GlobalOmniCore.attach_agent` to accept a `Manifest` {Type, Capabilities, TrustScore}.
  - Store manifests in a persistent local/cloud registry.
  - Implement basic Capability filtering (e.g., "Find me a node that can 'code'").

### Stage 2: Orchestration & Routing (The Planner Shell)
- **Goal**: Enable the Gateway to intelligently route tasks.
- **Tasks**:
  - Implement `PlannerEngine.py`: Initial LLM-based logic to split "Build X" into "Step 1, Step 2, Step 3".
  - Implement `RouterEngine.py`: Logic to assign Step 1 to Node A and Step 2 to Node B.
  - Upgrade `/think` to handle "Delegation" signals.

### Stage 3: Universal Hive Memory (Context Persistence)
- **Goal**: Allow agents to share "Working Memory" across sessions.
- **Tasks**:
  - Upgrade `Hippocampus.py` to support `active_session_state`.
  - Implement a "Read/Write" protocol for shared workspace files via the `OSHook`.
  - Integrate Vector embeddings (FAISS/Pinecone) for semantic search within the Hive.

### Stage 4: Enterprise Security & Global Scale (Omni-Shield JWT)
- **Goal**: Hardening the cloud nexus for multi-user deployment.
- **Tasks**:
  - Replace static `OMNI_KEY` with **JWT-based Authentication**.
  - Implement Role-Based Access Control (RBAC): (e.g., Planner roles can write, Observer roles can only read).
  - Add Rate-Limiting and DDOS protection via Global Gateway middleware.

---

## 🏁 Immediate Action Items (Next 24 Hours)

1.  **Refactor `GlobalOmniCore`**: Update the internal agent storage structure to handle Capability Manifests.
2.  **New API Endpoints**: Introduce `/agents/register` and `/tasks/create` in `global_gateway.py`.
3.  **Simulation Run**: Launch a swarm where an "Architect" agent sends a multi-step task, and the "Router" assigns it to a "Coder" agent autonomously.

---

> [!IMPORTANT]
> **Status**: Ready for implementation. 🦾
> Omni-Core is moving from a passive "Hub" to an active **AGI Orchestrator**.

---
*Developed by Lead Architect & Antigravity AI*
