-- OMNI-CORE v3.2: DATABASE SCHEMA (SUPABASE / POSTGRESQL)
-- This schema powers the L3 Global Collective memory and Agent Trust system.

-- 1. AGENTS TABLE: Tracking Cognitive Credit Scores
CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    role TEXT DEFAULT 'general',
    trust_score FLOAT DEFAULT 0.5,
    capabilities TEXT[], -- Array of strings
    attached_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    total_tasks_performed INTEGER DEFAULT 0,
    hallucination_count INTEGER DEFAULT 0
);

-- 2. LOGIC_MEMORIES TABLE: The L3 Global Fact Vault
CREATE TABLE IF NOT EXISTS logic_memories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category TEXT NOT NULL,
    fact TEXT NOT NULL,
    confidence FLOAT DEFAULT 1.0,
    source_url TEXT,
    agent_id TEXT REFERENCES agents(agent_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_verified BOOLEAN DEFAULT TRUE
);

-- 3. KNOWLEDGE_GRAPH TABLE: Subject-Relation-Object Triplets
CREATE TABLE IF NOT EXISTS knowledge_graph (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject TEXT NOT NULL,
    relation TEXT NOT NULL,
    object TEXT NOT NULL,
    confidence FLOAT DEFAULT 1.0,
    verified_by_agent TEXT REFERENCES agents(agent_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_verified_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. GROUNDING_LOGS: Audit trail for Explainable Confidence
CREATE TABLE IF NOT EXISTS grounding_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id TEXT REFERENCES agents(agent_id),
    thought TEXT NOT NULL,
    verdict BOOLEAN NOT NULL,
    confidence_score FLOAT NOT NULL,
    reason TEXT,
    sources TEXT[], -- Array of URLs
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- INDEXES for performance
CREATE INDEX IF NOT EXISTS idx_memories_category ON logic_memories(category);
CREATE INDEX IF NOT EXISTS idx_graph_subject ON knowledge_graph(subject);
CREATE INDEX IF NOT EXISTS idx_agents_trust ON agents(trust_score);
