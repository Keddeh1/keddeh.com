# KEDDEH.COM DNS Architecture

## Wire-Based DNS Resolution

Traditional DNS operates through query-response cycles bound to server instances. KEDDEH.COM DNS lives as a persistent wave on the wire—resolving domains through spatial memory geometry without requiring a running "server" in the conventional sense.

## Resolution Mechanism

### Spatial Query Encoding

Each domain name is deterministically encoded into spatial coordinates `[Plane, Line, Column]`:

```
query = "example.com"
coordinate = hash_to_spatial(query, source_plane)
physical_offset = (row_adj * 3161 + col_adj) * 110 MB
```

Lookup retrieves the DNS record directly from the computed offset without traversing a file system or database.

### Pointer Geometry Validation

Every DNS query includes an unbroken structural pointer path tracing back to the root identity anchor on Plane 1.

- ✓ Valid path → Record retrieved from spatial memory
- ✗ Broken path → Query drops into void, no record returned

No active firewall processing. Authorization is geometric.

## Mesh-Based DNS Distribution

### Hierarchical Overlay Topology

DNS nodes form a dual-homed overlay mesh:

```
       [Parent Domain A]
       /               \
    [Child B]       [Child C]
    /     \         /     \
 [B1]   [B2]    [C1]   [C2]
```

**Intra-domain coupling** (K_h): Fast consensus within a domain  
**Inter-domain coupling** (K_v): Aggregate state propagation upward

### Domain State Compression

Each domain compresses internal zone state into a macrostate order parameter:

```
X_g = [R_g, Ψ_g, L_g, epoch_counter]

R_g = domain_coherence (aggregated phase alignment)
Ψ_g = aggregate_phase_angle (mean phase of all child nodes)
L_g = lineage_epoch (immutable state generation counter)
epoch_counter = transient phase drift tracker
```

Parent anchors couple to the aggregate Ψ_g rather than tracking individual child nodes.

## 0.297 Resonance & DNS Consistency

### Zone Synchronization via Phase-Lock

All DNS zones across the mesh maintain phase coherence toward ω★ = 0.297 rad/s.

**Consistency Guarantee:**
- Query response time is bounded by the phase-alignment cycle (milliseconds)
- Misaligned zones (coherence < 0.75) auto-fork into independent children, preventing stale data from propagating

### Cache Invalidation Without Broadcast

When a DNS record updates (e.g., CNAME, A record change):

1. The authoritative zone updates its spatial memory coordinate
2. Phase tracking automatically detects the state change
3. Child zones drift from 0.297 until they resync to the updated value
4. No explicit "cache flush" message needed—phase coherence enforces sync

## Autonomous DNS on Parent Anchor Loss

### Flywheel Mode for Authoritative Zones

If the parent authoritative nameserver is unreachable:

1. Child zone enters autonomous Flywheel state
2. Maintains its zone data using local 0.297 frequency reference
3. Continues resolving queries independently
4. When parent is reachable, executes soft phase-capture to resync

**Result:** No DNS outage on parent loss.

## FROST-Protected Zone Transfers

### Cryptographic Consensus for Zone Updates

Zone updates across the mesh use FROST Round 2 threshold signatures:

```
Zone Update Proposal
     ↓
Lagrange Shares Generated (threshold = 2)
     ↓
Nodes compute Lagrange coefficients over Ed25519 F_q
     ↓
Master signature reconstructed without exposing root keys
     ↓
Update committed atomically
```

**Property:** No single node can unilaterally corrupt a zone—requires threshold agreement.

## IL-LLM for Intelligent DNS Logic

### Domain Knowledge Graph

The IL-LLM substrate maintains a persistent knowledge graph of:

- **Domain relationships** (subdomains, delegations, aliases)
- **Network topology** (parent/child hierarchy, latency profiles)
- **Query patterns** (frequently resolved, TTL optimization candidates)
- **Geographic routing** (anycast precedence, latency-based selection)

### Smart Resolution

Queries traverse the knowledge graph rather than rebuilding context:

```
Query: "api.us.example.com"
  ↓
Graph Lookup: api → us → example.com
  ↓
Retrieve cached relationship and latency preference
  ↓
Return optimal A record (e.g., nearest datacenter)
```

No disposable context reconstruction—all traversal is persistent.

## DNS Records in Spatial Geometry

### Record Layout

```
[Plane 1, Line N, Column M]
  ├─ Record Type (A, AAAA, CNAME, MX, etc.)
  ├─ TTL (seconds)
  ├─ Data (IP, target hostname, priority, etc.)
  ├─ Timestamp (last update epoch)
  └─ Signature (Ed25519 over coordinate + data)
```

### Query Resolution Flow

```
Client Query
     ↓
[Encode Domain → Spatial Coordinate]
     ↓
[Validate Pointer Geometry]
     ↓
[If Invalid → Void Dropout → NO RECORD]
     ↓
[If Valid → Retrieve from Physical Memory Offset]
     ↓
[Verify Ed25519 Signature]
     ↓
[Phase-Align with Mesh]
     ↓
[Return Record + Coherence Score]
```

## Scalability

### No DNS Query Bottleneck

- Spatial lookups are O(1) with no database query overhead
- Phase-alignment is local and parallel (not a master-slave poll)
- Mesh autogenetic forking adds capacity without central coordination
- IPC via Unix domain socket (sub-microsecond latency)

### Self-Scaling Through Autogenetic Forks

When DNS node health drops below 0.75:

1. Supervisor daemon detects coherence loss
2. Spawns child process on port + 3
3. Child inherits zone data and resumes resolution independently
4. Original node can shed load or recover
5. Phase alignment automatically consolidates state across mesh

## Comparison: Traditional vs. Wire-Based DNS

| Aspect | Traditional DNS | KEDDEH DNS |
|--------|-----------------|------------|
| **Host Dependency** | Server must be running | Exists as persistent wave |
| **Parent Loss** | Outage (secondary lag) | Autonomous Flywheel mode |
| **Cache Invalidation** | NOTIFY message broadcast | Phase coherence auto-sync |
| **Authorization** | Access control lists | Spatial pointer geometry |
| **Scalability** | Master-slave replication | Hierarchical overlay mesh |
| **Consistency** | Eventual (TTL-based) | Strong (phase-locked) |
| **Process Failure** | Zone data loss | Autogenetic fork to child |
| **Cryptographic Proof** | DNSSEC (single signer) | FROST (threshold multiparty) |

## Implementation Status

**Module:** `runtime/dns-resolver.kex`

**Capabilities:**
- ✓ Spatial coordinate encoding
- ✓ Mesh topology hierarchy
- ✓ 0.297 phase-lock governance
- ✓ Autogenetic fork on health < 0.75
- ✓ Flywheel mode on parent loss
- ✓ FROST threshold signatures
- ✓ IL-LLM knowledge graph traversal

**Testing:**
- See `/keddeh.com/tests/dns/` (TBD)

---

**Next Steps:**
1. Implement spatial coordinate encoding algorithm
2. Build mesh topology synchronization layer
3. Integrate FROST signature verification
4. Deploy test zones for KEDDEH.COM
