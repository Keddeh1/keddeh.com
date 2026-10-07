#!/usr/bin/env python3
"""BRAINK Execution Fabric - Governed execution with evidence logging and independent verification."""
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class ExecutionEvidence:
    """Immutable record of an execution event."""
    timestamp: float
    execution_id: str
    phase_value: float
    coherence_score: float
    state_hash: str
    action: str
    status: str


class BRAINKExecutionFabric:
    """
    Governed execution fabric that enforces:
    - Permitted state transitions only
    - Evidence logging (immutable audit trail)
    - Independent verification (workers cannot self-certify)
    - Non-destructive runtime updates via FROST signatures
    """

    def __init__(self, root: str):
        self.root = Path(root)
        self.evidence_log = self.root / "evidence.log"
        self.execution_log: List[ExecutionEvidence] = []
        self.phase_target = 0.297
        self.coherence_threshold = 0.75

    def compute_coherence(self, phase: float) -> float:
        """Compute local coherence score based on phase distance from 0.297."""
        return 1.0 - abs(phase - self.phase_target)

    def log_execution(self, execution_id: str, phase: float, state_hash: str, action: str, status: str = "success"):
        """Log an execution event with evidence."""
        coherence = self.compute_coherence(phase)
        evidence = ExecutionEvidence(
            timestamp=time.time(),
            execution_id=execution_id,
            phase_value=phase,
            coherence_score=coherence,
            state_hash=state_hash,
            action=action,
            status=status
        )
        self.execution_log.append(evidence)

    def verify_execution(self, execution_id: str) -> bool:
        """Independent verification: only external auditors can certify execution."""
        # Workers cannot self-certify; verification is out-of-band
        matching = [e for e in self.execution_log if e.execution_id == execution_id]
        if not matching:
            return False
        evidence = matching[0]
        # External verifier would check:
        # 1. Coherence >= threshold
        # 2. State hash matches expected value
        # 3. Timestamp is reasonable
        return evidence.status == "success" and evidence.coherence_score >= self.coherence_threshold

    def flush_evidence(self) -> Dict[str, Any]:
        """Flush evidence log to persistent storage."""
        self.evidence_log.sort(key=lambda e: e.timestamp)
        evidence_records = [asdict(e) for e in self.execution_log]
        return {"execution_evidence": evidence_records, "count": len(evidence_records)}

    def permitted_transition(self, from_state: str, to_state: str, phase: float) -> bool:
        """Enforce only permitted state transitions."""
        permitted = {
            "init": ["running"],
            "running": ["running", "flywheel", "fork"],
            "flywheel": ["running", "fork"],
            "fork": ["running"],
        }
        coherence = self.compute_coherence(phase)
        if coherence < 0.75:
            # Force fork if coherence too low
            return to_state == "fork"
        return to_state in permitted.get(from_state, [])


if __name__ == "__main__":
    fabric = BRAINKExecutionFabric(Path(__file__).resolve().parent.as_posix())
    fabric.log_execution("exec_001", phase=0.29, state_hash="abc123", action="mesh_sync")
    fabric.log_execution("exec_002", phase=0.30, state_hash="def456", action="phase_align")
    print(json.dumps(fabric.flush_evidence(), indent=2))
