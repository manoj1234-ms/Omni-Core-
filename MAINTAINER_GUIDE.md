# 🛰️ MAINTAINER GUIDE: OMNI-CORE SYSTEM LOGIC

This guide explains the underlying engineering principles of the Omni-Core AGI v3.3 framework.

## 1. The Cortex Lifecycle (`/CortexHub/orchestrator.py`)
The orchestrator acts as the **Central Executive Function**. 
- It uses the **Semantic Router** (`router.py`) to parse natural language tasks.
- It maps task keywords to specific Node IDs (e.g., "code" -> `code_node`).
- It executes asynchronous HTTP requests to parallelize the swarm.
- It synthesizes the final response with a total consensus score.

## 2. Expert Node Implementation (`/HiveNodes/`)
Each node is an independent **Microservice** built on FastAPI.
- **Independence**: Nodes can run on separate physical hardware or cloud instances.
- **Causal Output**: Every successful response from a node must contain a `causal_score`. This is used by the Hub to filter hallucinations.
- **Extensibility**: To add a new capability, simply create a new node script (e.g., `market_node.py`) and add its port to the Cortex registry.

## 3. Communication Protocols
- **Inter-node**: REST API over JSON.
- **Consensus**: Weighted average of `causal_score` from all triggered nodes.
- **Persistence**: Shared memories can be synced with the Global Hub via the `/memory` endpoints.

## 4. Troubleshooting
- **Port Conflicts**: Ensure ports `5112` through `5115` are open on your local machine.
- **Node Failures**: If the Hub reports "Node Offline", manually check the terminal logs for the specific node in `HiveNodes/`.

---
**Core Mandate**: *"Never generate a token that cannot be mathematically grounded in verified world logic."*
