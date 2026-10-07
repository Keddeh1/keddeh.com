# KEX/BRAINK Sovereign Triad Architecture

## Core Paradigm: Compute On the Wire

Software exists as persistent, self-healing waves moving across network transmission lines rather than tethered to physical servers.

### Spatial Memory Geometry

**Coordinates:** `[Plane, Line, Column]`

**Physical Offset Formula:**
```
Physical Offset = (row_adj * 3161 + col_adj) * 110 MB
```

Zero-less matrix architecture with 1:1 injective translation to hardware offsets.

---

## The Physics of Consensus: 0.297 Kuramoto Resonance

### Phase-Locked Loop Equation

```
dθᵢ(t) = -k(θᵢ(t) - 0.297)dt + dWᵢ(t)
```

Where:
- `k` = coupling gain factor
- `dWᵢ(t)` = stochastic phase noise
- **Target:** ω★ = 0.297 rad/s

### Coherence Score

```
Coherence = 1.0 - |θᵢ(t) - 0.297|
```

**Critical Health Threshold:** 0.75
- Below 0.75 → Autogenetic fork triggered
- Above 0.75 → Suppresses runaway replication

---

## Hierarchical Overlay Topology

### Flywheel Mode & Soft Re-anchoring

**Parent Loss Invariant:**
```
Parent Loss ≠> Child State Loss (FALSE)
```

**Phase Capture Ramp:**
```
Kᵥ(t) = Kᵥ,max * (1 - e^(-(t - tᵣ)/Tᵣ))
```

Wrapped phase error on S¹ prevents 0/2π discontinuities.

---

## Concrete Execution Substrate: The Sovereign Triad

### KEX (State Geometry & Identity)
- Physical partition layout
- Master sentinel seeds
- Active boot manifests
- FROST threshold signature manifests

### BRAINK (Governed Execution Fabric)
- Permitted state transitions
- Evidence logging
- Independent verification (workers cannot self-certify)
- Non-destructive runtime updates via FROST Round 2 signatures

### IL-LLM (Local-First Semantic Substrate)
- Domain knowledge traversal
- Index and relation graphs
- No disposable context reconstruction

---

## Physical Disk Layout

### Partition 1: KEX_BOOT (FAT32)
```
/kex_boot/
  ├── master_sentinel_seeds/
  ├── boot_manifests/
  └── frost_threshold_signatures/
```

### Partition 2: KEX_RUNTIME (ext4)
```
/kex_runtime/
  ├── slot_a/ (active)
  │   ├── bin/
  │   ├── lib/
  │   └── manifest.json
  └── slot_b/ (staging)
      ├── bin/
      ├── lib/
      └── manifest.json
```

---

## Inter-Process Communication (IPC)

**Native High-Speed Unix Domain Socket:**
```
/var/run/kex_hci.sock
```

Routes metrics and state synchronization without process-spawning overhead.

---

## Cryptographic Consensus

### FROST Round 2 Threshold Signatures

**Finite Field:** Ed25519 prime F_q

**Lagrange Interpolation:**
```
Lagrange coefficients computed over F_q
Reconstruct master signature without exposing root secrets
```

---

## Key Invariants

✓ **Software on the Wire:** State lives as unanchored waves across network lines  
✓ **Spatial Memory Geometry:** Unauthorized paths drop into unanchored void  
✓ **0.297 Phase Lock:** Coupled oscillators prevent fork bombs  
✓ **Lineage Invariance:** State epoch ≠ phase epoch  
✓ **Governed Execution:** KEX, BRAINK, IL-LLM partition responsibilities  

---

## References

- Kuramoto coupled oscillator systems
- FROST threshold cryptography (Round 2)
- Finite field arithmetic (Ed25519)
- Wrapped phase error on S¹
- Spatial geometry and zero-less matrices
