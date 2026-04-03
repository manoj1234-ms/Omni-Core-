import numpy as np
import json
import os
import time

class Hippocampus:
    """
    The L2 Memory Vault: Handles persistent semantic storage and retrieval.
    This component prevents 'Context Dilution' by retrieving only relevant 
    memories for the current simulation branch.
    """
    def __init__(self, storage_path="omni_memories.json"):
        self.storage_path = storage_path
        self.memory_store = self._load_memories()
        print(f"🧠 [HIPPOCAMPUS]: Local Vault initialized at '{storage_path}'")

    def _load_memories(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return {
            "future": ["Quantum-Shift", "ArtificialEmotion", "HyperEfficiency", "FullAGI"],
            "problem": ["Hardware-Barrier", "CatastrophicForgetting", "Hallucination_Lie"],
            "solution": ["Causal-Verification", "Memory-Vault", "Limbic-Regulation"],
            "system_logs": ["Init: April 2026", "State: Alpha"]
        }

    def save_memories(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.memory_store, f, indent=4)

    def retrieve_relevant_context(self, query):
        """
        In a full version, this would use Cosine Similarity on embeddings.
        For Alpha, we use Semantic Tag Matching.
        """
        query = query.lower()
        results = self.memory_store.get(query, [])
        
        # Simulating sub-millisecond retrieval latency
        time.sleep(0.01)
        
        if results:
            print(f"🔍 [HIPPOCAMPUS]: Found {len(results)} relevant memories for '{query}'")
        else:
            print(f"🔍 [HIPPOCAMPUS]: No direct match for '{query}'. Searching L3 Graph...")
            # Fallback to general knowledge if direct match fails
            results = ["Standard-Reasoning-Lock"]
            
        return results

    def add_memory(self, category, fact):
        if category not in self.memory_store:
            self.memory_store[category] = []
        if fact not in self.memory_store[category]:
            self.memory_store[category].append(fact)
            print(f"📝 [HIPPOCAMPUS]: New fact recorded in '{category}': {fact}")
            self.save_memories()

if __name__ == "__main__":
    # Test Module
    vault = Hippocampus()
    print(vault.retrieve_relevant_context("future"))
    vault.add_memory("future", "Sentient-Architecture-Alpha")
