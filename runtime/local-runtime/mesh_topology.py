#!/usr/bin/env python3
"""Mesh Topology Coordinator - Hierarchical overlay with phase-lock governance."""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import time


class MeshNode:
    """Individual node in the hierarchical overlay mesh."""

    def __init__(self, node_id: str, port: int, phase: float = 0.297):
        self.node_id = node_id
        self.port = port
        self.phase = phase
        self.coherence = 1.0 - abs(phase - 0.297)
        self.parent: Optional[str] = None
        self.children: List[str] = []
        self.status = "running"
        self.last_sync = time.time()

    def compute_coherence(self) -> float:
        """Recompute coherence score based on phase distance from 0.297."""
        self.coherence = 1.0 - abs(self.phase - 0.297)
        return self.coherence

    def should_fork(self) -> bool:
        """Determine if this node should trigger an autogenetic fork."""
        return self.coherence < 0.75

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "port": self.port,
            "phase": round(self.phase, 4),
            "coherence": round(self.coherence, 4),
            "status": self.status,
            "parent": self.parent,
            "children": self.children,
            "last_sync": self.last_sync,
        }


class MeshDomain:
    """Domain containing multiple nodes with intra-domain consensus."""

    def __init__(self, domain_id: str, parent_domain: Optional[str] = None):
        self.domain_id = domain_id
        self.parent_domain = parent_domain
        self.nodes: Dict[str, MeshNode] = {}
        self.domain_coherence = 1.0  # R_g
        self.aggregate_phase = 0.297  # Psi_g
        self.lineage_epoch = 0  # L_g

    def add_node(self, node: MeshNode) -> None:
        """Add a node to this domain."""
        self.nodes[node.node_id] = node
        if len(self.nodes) > 1:
            # Set first node as parent
            first_node = list(self.nodes.values())[0]
            node.parent = first_node.node_id
            first_node.children.append(node.node_id)

    def sync_intra_domain(self) -> Dict[str, float]:
        """Synchronize nodes within domain (K_h coupling)."""
        if not self.nodes:
            return {}
        phases = [node.phase for node in self.nodes.values()]
        self.aggregate_phase = sum(phases) / len(phases)
        coherences = [node.compute_coherence() for node in self.nodes.values()]
        self.domain_coherence = sum(coherences) / len(coherences)
        return {
            "aggregate_phase": self.aggregate_phase,
            "domain_coherence": self.domain_coherence,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain_id": self.domain_id,
            "parent_domain": self.parent_domain,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "domain_coherence": round(self.domain_coherence, 4),
            "aggregate_phase": round(self.aggregate_phase, 4),
            "lineage_epoch": self.lineage_epoch,
        }


class MeshTopologyCoordinator:
    """
    Hierarchical overlay mesh coordinator.
    Manages intra-domain (K_h) and inter-domain (K_v) coupling.
    Handles flywheel mode and soft phase capture on parent loss.
    """

    def __init__(self, root: str):
        self.root = Path(root)
        self.domains: Dict[str, MeshDomain] = {}
        self.phase_lock_target = 0.297
        self.coherence_threshold = 0.75
        self._bootstrap_topology()

    def _bootstrap_topology(self) -> None:
        """Bootstrap root and child domains."""
        root_domain = MeshDomain("root_domain", parent_domain=None)
        root_domain.add_node(MeshNode("root_node_0", port=8000, phase=0.297))
        self.domains["root_domain"] = root_domain

        # Child domain
        child_domain = MeshDomain("child_domain_0", parent_domain="root_domain")
        child_domain.add_node(MeshNode("child_node_0", port=8003, phase=0.296))
        child_domain.add_node(MeshNode("child_node_1", port=8004, phase=0.298))
        self.domains["child_domain_0"] = child_domain

    def get_or_create_domain(self, domain_id: str, parent: Optional[str] = None) -> MeshDomain:
        """Get existing domain or create new one."""
        if domain_id not in self.domains:
            self.domains[domain_id] = MeshDomain(domain_id, parent_domain=parent)
        return self.domains[domain_id]

    def add_node_to_domain(self, domain_id: str, node: MeshNode) -> None:
        """Add a node to a domain."""
        domain = self.get_or_create_domain(domain_id)
        domain.add_node(node)

    def sync_all_domains(self) -> Dict[str, Any]:
        """Synchronize all domains and check for fork triggers."""
        sync_report = {}
        forks_needed = []

        for domain_id, domain in self.domains.items():
            domain.sync_intra_domain()
            sync_report[domain_id] = domain.to_dict()

            # Check for fork triggers
            for node_id, node in domain.nodes.items():
                if node.should_fork():
                    forks_needed.append({
                        "domain": domain_id,
                        "node": node_id,
                        "coherence": node.coherence,
                        "action": "autogenetic_fork"
                    })

        return {"domains": sync_report, "forks_needed": forks_needed}

    def flywheel_mode(self, domain_id: str) -> Dict[str, Any]:
        """Activate autonomous flywheel mode on parent loss."""
        domain = self.domains.get(domain_id)
        if not domain:
            return {"status": "error", "reason": f"Domain {domain_id} not found"}

        domain.parent_domain = None  # Disconnect from parent
        domain.status = "flywheel"

        # Maintain local 0.297 frequency reference
        for node in domain.nodes.values():
            node.phase = self.phase_lock_target
            node.status = "flywheel"

        return {
            "status": "success",
            "domain": domain_id,
            "mode": "autonomous_flywheel",
            "local_frequency_reference": self.phase_lock_target,
        }

    def soft_phase_capture(self, domain_id: str, new_parent_phase: float, tau: float = 1.5) -> Dict[str, Any]:
        """
        Soft re-anchoring: exponential phase capture without discontinuities.
        Formula: K_v(t) = K_v_max * (1 - e^(-(t - t_r)/tau))
        """
        domain = self.domains.get(domain_id)
        if not domain:
            return {"status": "error", "reason": f"Domain {domain_id} not found"}

        import math
        capture_steps = 10
        for step in range(capture_steps):
            progress = 1.0 - math.exp(-(step / capture_steps) / tau)
            for node in domain.nodes.values():
                node.phase = (1 - progress) * node.phase + progress * new_parent_phase
                node.compute_coherence()

        domain.parent_domain = None  # Will be set to new parent
        domain.status = "running"

        return {
            "status": "success",
            "domain": domain_id,
            "action": "soft_phase_capture",
            "steps": capture_steps,
            "final_phase": domain.aggregate_phase,
            "tau": tau,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase_lock_target": self.phase_lock_target,
            "coherence_threshold": self.coherence_threshold,
            "domains": {did: d.to_dict() for did, d in self.domains.items()},
        }


if __name__ == "__main__":
    coordinator = MeshTopologyCoordinator(Path(__file__).resolve().parent.as_posix())
    print("[MESH] Initial Topology:")
    print(json.dumps(coordinator.to_dict(), indent=2))
    print("\n[MESH] Sync Report:")
    sync = coordinator.sync_all_domains()
    print(json.dumps(sync, indent=2))
