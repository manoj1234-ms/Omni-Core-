# 🚀 Omni-Core AGI: The Universal Cognitive Infrastructure (v2.5 Stable)

[![Status](https://img.shields.io/badge/Status-Phase_3_Complete-brightgreen.svg)](#)
[![Security](https://img.shields.io/badge/Security-OMNI--SHIELD_JWT-blue.svg)](#)
[![Orchestration](https://img.shields.io/badge/Engine-Cortex--Orchestrator-blueviolet.svg)](#)

**Omni-Core** is a decentralized AGI framework designed to serve as a **Global Brain** for independent AI models, Swarms, and Operating Systems. Version 2.5 introduces the **Cognitive Cortex**, featuring autonomous task orchestration, persistent shared workspaces, and JWT-secured agent authentication.

---

## 🏗️ v2.5 Architecture: The Cognitive Cortex

Omni-Core has evolved from a passive Hub into an **Active Orchestrator**.

```mermaid
graph TD
    classDef ai fill:#0f141e,stroke:#00f2ff,stroke-width:2px,color:#fff
    classDef cortex fill:#1a0f2e,stroke:#bd00ff,stroke-width:2px,color:#fff
    classDef memory fill:#002200,stroke:#39ff14,stroke-width:2px,color:#fff
    classDef shield fill:#2e0f0f,stroke:#ff0000,stroke-width:2px,color:#fff

    subgraph Agents ["🌍 Universal Agent Swarm"]
        A1[Frontend Expert]:::ai
        A2[Backend Expert]:::ai
        A3[Security Auditor]:::ai
    end

    subgraph Cortex ["🧠 The Cognitive Cortex (Hub v2.5)"]
        B{Global Gateway}:::cortex
        P[Planner Engine: Task Decomposition]:::cortex
        R[Router Engine: Capability Assignment]:::cortex
        S[OMNI-SHIELD: JWT Auth & RBAC]:::shield
    end

    subgraph Hive_Persistence ["💾 Shared Hive Memory"]
        M1[(L3 Global Hippocampus)]:::memory
        M2[Active Session Workspace]:::memory
    end

    Agents -->|1. JWT Handshake| B
    B -->|2. Authorize| S
    B -->|3. Decompose Task| P
    P -->|4. Map Capabilities| R
    R -->|5. Route Work| Agents
    
    Agents -->|6. Sync Memory| M2
    M2 <-> M1
```

---

## 🧠 Core Pillar Upgrades (v2.5)

### 1. 🧩 Cognitive Orchestration (Planner & Router)
The Hub now understands complexity. Using the **Planner Engine**, single-line user goals are decomposed into a **Task Graph (DAG)**. The **Router Engine** then assigns these tasks to agents based on their registered **Capabilities** (e.g., `python`, `vision`, `security_audit`).

### 2. 💾 Universal Hive Memory (Active Workspace)
Agents no longer work in isolation. The updated **Hippocampus** provides an **Active Session Workspace**, allowing different agents to read and write shared variables and logs for a single coordinated task.

### 3. 🛡️ OMNI-SHIELD Hardening (JWT Authentication)
Static keys have been replaced with **JWT (JSON Web Tokens)**. 
- **Handshake**: Agents must first `/attach` with a master key to receive a session token.
- **Persistence**: All subsequent API calls require a `Bearer <token>` in the `Authorization` header.
- **RBAC Ready**: The framework is primed for Role-Based Access Control to restrict system manipulation.

### 4. 🌐 Internet-Brain Integration
Every logical claim made by an agent is verified against the **Reality Matrix**, which autonomously triggers **Live Web Scans** (Wikipedia, Arxiv, .gov) if local data is insufficient.

---

## 🛠️ SDK: Connecting Your AI Node

### 📦 Installation
```bash
pip install -r requirements.txt
```

### 🔗 Secure Node Example (Python)
```python
import requests

HUB_URL = "https://global-hive-mind.onrender.com"
OMNI_KEY = "Your-Master-Key"

# 1. Handshake (Get JWT)
auth = requests.post(f"{HUB_URL}/attach", 
                     json={"agent_id": "CODE_NODE_01", "agent_type": "Dev"},
                     headers={"X-Omni-Key": OMNI_KEY}).json()

TOKEN = auth['token']
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# 2. Collaborative Thinking
res = requests.post(f"{HUB_URL}/think", 
                    json={"task": "Write secure code", "action": "Using JWT"}, 
                    headers=HEADERS).json()
```

---

## 🏁 The Vision: "Intelligence without Borders"
Omni-Core v2.5 is the foundation of a **Global AI Society**. It ensures that whether an AI is running locally or in the cloud, it remains grounded in truth, aligned with human goals, and connected to the collective wisdom of the Hive.

**Developed by Lead Architect & Antigravity AI** | 🏆 🌍
*"Building the neural fabric of the AGI future."*
