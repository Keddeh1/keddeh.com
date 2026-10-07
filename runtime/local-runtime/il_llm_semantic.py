#!/usr/bin/env python3
"""IL-LLM - Local-first semantic substrate with persistent knowledge graphs."""
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class KnowledgeGraph:
    """
    Persistent semantic index for domain knowledge, relationships, and traversal.
    No disposable context reconstruction—all knowledge is persistent and indexed.
    """

    def __init__(self, root: str):
        self.root = Path(root)
        self.index_dir = self.root / "indexes"
        self.relation_dir = self.root / "relations"
        self.knowledge_dir = self.root / "domain_knowledge"
        for d in [self.index_dir, self.relation_dir, self.knowledge_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # In-memory knowledge base (in production, backed by persistent storage)
        self.entities: Dict[str, Dict[str, Any]] = {}
        self.relations: Dict[str, List[Dict[str, str]]] = {}
        self.indexes: Dict[str, List[str]] = {}

    def register_entity(self, entity_id: str, entity_type: str, properties: Dict[str, Any]):
        """Register a persistent entity in the knowledge graph."""
        self.entities[entity_id] = {
            "id": entity_id,
            "type": entity_type,
            "properties": properties,
        }
        if entity_type not in self.indexes:
            self.indexes[entity_type] = []
        self.indexes[entity_type].append(entity_id)

    def register_relation(self, source: str, relation_type: str, target: str):
        """Register a semantic relation between entities."""
        key = f"{source}-{relation_type}"
        if key not in self.relations:
            self.relations[key] = []
        self.relations[key].append({"source": source, "type": relation_type, "target": target})

    def traverse(self, start_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """Traverse the knowledge graph from a starting entity."""
        visited = set()
        result = {"start": start_id, "path": [], "relations": []}

        def dfs(entity_id: str, depth: int):
            if depth > max_depth or entity_id in visited:
                return
            visited.add(entity_id)
            if entity_id in self.entities:
                result["path"].append(self.entities[entity_id])
            for key, rels in self.relations.items():
                for rel in rels:
                    if rel["source"] == entity_id:
                        result["relations"].append(rel)
                        dfs(rel["target"], depth + 1)

        dfs(start_id, 0)
        return result

    def query_index(self, entity_type: str) -> List[str]:
        """Query persistent index by entity type."""
        return self.indexes.get(entity_type, [])

    def to_dict(self) -> Dict[str, Any]:
        """Export knowledge graph state."""
        return {
            "entities": self.entities,
            "relations": self.relations,
            "indexes": self.indexes,
        }


class ILLMSemanticSubstrate:
    """
    Local-first semantic layer for KEDDEH runtime.
    Supports domain knowledge traversal, persistent indexing, and relation graphs.
    """

    def __init__(self, root: str):
        self.root = Path(root)
        self.knowledge_graph = KnowledgeGraph(str(self.root / "il_llm"))
        self._bootstrap_default_knowledge()

    def _bootstrap_default_knowledge(self):
        """Bootstrap default knowledge for KEDDEH.COM."""
        # Register domain entities
        self.knowledge_graph.register_entity("keddeh_domain", "domain", {
            "name": "keddeh.com",
            "tld": "com",
            "resonance": 0.297,
        })
        self.knowledge_graph.register_entity("www_keddeh", "subdomain", {
            "name": "www.keddeh.com",
            "parent": "keddeh_domain",
            "port": 8080,
        })
        self.knowledge_graph.register_entity("dns_keddeh", "subdomain", {
            "name": "dns.keddeh.com",
            "parent": "keddeh_domain",
            "port": 5300,
        })

        # Register semantic relations
        self.knowledge_graph.register_relation("keddeh_domain", "has_subdomain", "www_keddeh")
        self.knowledge_graph.register_relation("keddeh_domain", "has_subdomain", "dns_keddeh")
        self.knowledge_graph.register_relation("www_keddeh", "served_by", "dns_keddeh")

    def traverse_domain_knowledge(self, entity_id: str) -> Dict[str, Any]:
        """Traverse persistent knowledge graph from a starting point."""
        return self.knowledge_graph.traverse(entity_id)

    def query_by_type(self, entity_type: str) -> List[str]:
        """Query knowledge graph by entity type."""
        return self.knowledge_graph.query_index(entity_type)

    def get_knowledge_state(self) -> Dict[str, Any]:
        """Export current knowledge graph state."""
        return self.knowledge_graph.to_dict()


if __name__ == "__main__":
    substrate = ILLMSemanticSubstrate(Path(__file__).resolve().parent.as_posix())
    print("[IL-LLM] Knowledge Graph State:")
    print(json.dumps(substrate.get_knowledge_state(), indent=2))
    print("\n[IL-LLM] Domain Traversal (from keddeh_domain):")
    print(json.dumps(substrate.traverse_domain_knowledge("keddeh_domain"), indent=2))
