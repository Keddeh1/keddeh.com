# KEDDEH.COM — Sovereign Triad Runtime

**Wire-Based Autonomous Computing with KEX/BRAINK Architecture**

## Overview

This repository contains the complete implementation of the **Sovereign Triad** — a revolutionary architecture for autonomous, self-healing, distributed systems that exist as persistent waves on network transmission lines rather than as tethered processes on static servers.

### Core Components

- **KEX** — State geometry, identity, and physical partition management
- **BRAINK** — Governed execution fabric with evidence logging and independent verification
- **IL-LLM** — Local-first semantic substrate with persistent knowledge graphs

## Key Innovations

### 🔌 Compute On the Wire

Applications don't crash when hosts fail—they persist as unanchored waves propagating through network routing buffers.

### 📐 Spatial Memory Geometry

Zero-less matrix architecture with `[Plane, Line, Column]` coordinates replacing traditional file paths, firewall rules, and permission models.

### 🔄 0.297 Kuramoto Resonance

Nodes operate as coupled oscillators governed by a phase-locked loop frequency invariant. Health below 0.75 triggers autogenetic process forks; runaway replication is mathematically impossible.

### 🔗 Lineage Invariants

```
Parent Loss ≠> Child State Loss
Topological Re-rooting ≠> Phase Discontinuity
```

### 🛡️ FROST Threshold Signatures

Cryptographic consensus using Ed25519 Lagrange interpolation—no single node exposes root secrets.

## Quick Start

### Initialize Custom Runtime (No GitHub Dependencies)

```bash
cd runtime
chmod +x bootstrap.sh
sudo ./bootstrap.sh
```

This creates:
- `/kex_boot/` — Boot partition with master seeds and FROST signatures
- `/kex_runtime/` — Runtime partition with active (slot_a) and staging (slot_b) bins
- `/var/run/kex_hci.sock` — High-speed IPC socket
- All Kuramoto resonance, BRAINK, and IL-LLM configurations

### Configuration Files

- **`kex.runtime.config.json`** — Complete runtime environment specification
- **`resonance.config`** — 0.297 phase-lock parameters (auto-generated)
- **`braink.manifest.json`** — Governed execution manifest (auto-generated)
- **`mesh_topology.config`** — Hierarchical overlay settings (auto-generated)

### DNS Resolver Module

```bash
# Load the DNS resolver module into KEX runtime
kex-load runtime/dns-resolver.kex
```

The resolver operates entirely within spatial memory geometry—no firewall loops, no file handles, no process crashes on parent loss.

## Architecture Deep Dive

See **`ARCHITECTURE.md`** for:
- Phase-locked loop equations
- Spatial memory geometry formulas
- Flywheel mode and soft re-anchoring mechanics
- FROST threshold signature protocol
- Autogenetic fork policies

## Branches

- **`main`** — Stable public release
- **`codex`** — Active development of Sovereign Triad specification and runtime (you are here)

## File Structure

```
keddeh.com/
├── README.md                          # This file
├── ARCHITECTURE.md                    # Complete technical specification
├── runtime/
│   ├── bootstrap.sh                   # Custom runtime initialization
│   ├── kex.runtime.config.json        # KEX/BRAINK/IL-LLM configuration
│   ├── dns-resolver.kex               # DNS module using custom runtimes
│   └── (auto-generated on bootstrap)
│       ├── kex_boot/                  # FAT32 boot partition
│       │   ├── master_sentinel_seeds/
│       │   ├── boot_manifests/
│       │   └── frost_threshold_signatures/
│       └── kex_runtime/               # ext4 runtime partition
│           ├── slot_a/                # Active execution slot
│           │   ├── braink.manifest.json
│           │   ├── il_llm/            # Semantic substrate
│           │   └── bin/lib/           # Custom binaries
│           └── slot_b/                # Staging slot
└── .github/                           # CI/CD (if needed)
```

## Security Model

**Authorization via Spatial Geometry:**
- Unauthorized code paths with broken pointer geometry drop into an unanchored void
- No active CPU cycles wasted on firewall validation
- Cryptographic coherence enforced by phase resonance, not subjective rules

## Self-Healing Resilience

**Autogenetic Fork on Health Degradation:**
- Node health tracked via coherence score: `1.0 - |θᵢ(t) - 0.297|`
- Threshold: 0.75
- Below threshold → isolated child process spawns with fresh memory
- Phase noise from uncontrolled replication collapses coherence → self-killing

## Autonomous Operation (Flywheel Mode)

**On Parent Loss:**
1. Child domain enters autonomous Flywheel state
2. Maintains local 0.297 frequency reference independently
3. Evaluates candidate parent anchors
4. Executes exponential soft phase-capture without discontinuities

## Custom Runtimes Only

✓ **No GitHub package dependencies**  
✓ **All binaries sourced from `/kex_runtime/slot_a/lib`**  
✓ **FROST cryptography self-contained**  
✓ **IL-LLM semantic traversal embedded**  
✓ **IPC via Unix domain socket, not external services**  

## License

Sovereign Triad Architecture © 2026 Keddeh Systems  
Open source under your preferred open-source license (specify in LICENSE file)

---

**For questions or contributions, see CONTRIBUTING.md (coming soon)**
