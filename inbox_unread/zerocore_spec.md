# ZeroCore Architecture Specification (JSON-Native OS)

## 1. System Philosophy
ZeroCore is a JSON-Native Operating System Runtime. Unlike conventional applications that read JSON strictly as configuration files, ZeroCore treats JSON structured data as primitive OS objects, memory pointers, execution states, capabilities, and syscall registries.

### Core Principles
* **Registry First**: Every component exists as a schema-validated registry.
* **Schema First**: Strict schema enforcement guarantees state safety and deterministic execution.
* **Event Driven**: OS state transitions are triggered via event queues and system calls.
* **Audit First & Evidence Chain**: Every state change is recorded on an immutable event/audit chain.
* **CUI & Data Native**: Operational control uses JSSH (JSON SSH) and structural CUI.

---

## 2. Architecture Layer Map

ZeroCore System Topology
│
┌───────────────────────┴───────────────────────┐
▼                                               ▼
Layer 0: Boot & Core                            Layer 1: Kernel
(manifest, index, graph)                        (state, scheduler, recovery)
│                                               │
└───────────────────────┬───────────────────────┘
▼
Layer 2: Object System
(process, object, fd, syscall)
│
┌───────────────────────┴───────────────────────┐
▼                                               ▼
Layer 3: Registry Base                          Layer 4: Audit System
(capability, dependency, memory)                (evidence, audit chain)
│                                               │
└───────────────────────┬───────────────────────┘
▼
Layer 5: Business Engine
(30+ domain registries)
│
┌───────────────────────┴───────────────────────┐
▼                                               ▼
Layer 6: AI-Native Runtime                      Layer 7: Distributed Mesh
(cognitive engine, planner)                     (consensus, replication)
│                                               │
└───────────────────────┬───────────────────────┘
▼
Layer 8: Operational Shell
(JSSH, CLI)
---

## 3. Directory Structure Specification

```text
ZeroCore/
├── Layer0_Boot/
│   ├── boot_record.json
│   ├── runtime_manifest.json
│   └── zero_core.index.json
├── Layer1_Kernel/
│   ├── state_registry.json
│   ├── scheduler.json
│   ├── module_registry.json
│   ├── service_registry.json
│   ├── snapshot_engine.json
│   └── recovery_registry.json
├── Layer2_ObjectSystem/
│   ├── process_table.json
│   ├── object_table.json
│   ├── fd_table.json
│   └── syscall_registry.json
├── Layer3_Registry/
│   ├── capability_registry.json
│   ├── dependency_graph.json
│   └── memory_index.json
├── Layer4_Audit/
│   ├── audit_chain.json
│   └── evidence_store.json
├── Layer5_Business/
│   ├── client_registry.json
│   ├── project_registry.json
│   ├── financial/
│   │   ├── ledger.json
│   │   ├── invoice_registry.json
│   │   └── quote_registry.json
│   └── marketplace/
│       ├── listing_registry.json
│       └── escrow_registry.json
├── Layer6_AI/
│   ├── memory_index.json
│   ├── reasoner.json
│   ├── planner.json
│   ├── reflection.json
│   └── knowledge_graph.json
├── Layer7_Distributed/
│   ├── node_registry.json
│   ├── cluster_topology.json
│   ├── consensus_engine.json
│   └── transport_bridge.json
└── Layer8_Shell/
    ├── jssh_config.json
    └── cli_policy.json
4. Layer Details & Mechanics
Layer 0: Boot
 * registry.index: Root dictionary of all registered schemas and runtime pointers.
 * runtime_manifest: Boot parameters, resource allocations, and kernel limits.
 * dependency.graph: DAG (Directed Acyclic Graph) of module/registry dependencies.
Layer 1: Kernel
 * kernel_state_registry: Real-time operating system state.
 * kernel_scheduler: Task scheduling engine using JSON process priority vectors.
 * kernel_snapshot & recovery_registry: State rollback and crash recovery mechanisms.
Layer 2: Object System
 * json_process_table: Process isolation boundaries and runtime states.
 * json_object_table: In-memory structural object store.
 * json_fd_table: File descriptor equivalent for handles, streams, and IPC channels.
 * json_syscall_registry: System call interface defining deterministic operations.
Layer 3: Registry Base
 * capability_registry: Fine-grained ACL and capability token permissions.
 * agent_memory_index: Primary structural memory routing.
Layer 4: Audit
 * audit_chain: Append-only cryptographic state journal.
 * evidence_store: Non-repudiation event logs for legal/business verification.
Layer 5: Business Engine
Domain registries managing state machine lifecycles for:
 * Entities (client, user, organization)
 * Financials (invoice, ledger, quote, payment)
 * Operations (project, task, inventory, vendor)
Layer 6: AI-Native Runtime
 * planner_scheduler: AI task decomposition mapped into OS processes (json_process_table).
 * reflection_engine: Evaluates executed syscall results and auto-patches the knowledge_graph.
 * capability_learning: Dynamically proposes controlled privilege extensions for AI actions.
Layer 7: Distributed Mesh
 * consensus_registry: Raft/PBFT consensus across zero-core nodes.
 * replication_engine: High-availability audit chain and object table syncing.
Layer 8: Operational Shell
 * JSSH (JSON Secure Shell): Structural RPC stream protocol replacing legacy text shells.
 * ZeroCLI: Interactive state inspector and syscall invocation tool.
5. Security & Bug Bounty Threat Model
| Risk Level | Threat Target | Vulnerability Vector | Severity / Impact |
|---|---|---|---|
| Critical | capability_registry × json_syscall_registry | Bypass capability check using $ref pointer manipulation or type confusion in JSON schema evaluator. | Privilege Escalation / System Hijack |
| Critical | Layer 6 AI ➔ Syscall Engine | Indirect Prompt Injection leading to unexpected task execution in planner_scheduler. | Arbitrary Code/Syscall Execution |
| High | audit_chain × recovery_registry | Time-of-check to time-of-use (TOCTOU) exploits during state rollback/snapshot restoration. | Audit Bypass & History Tampering |
| High | json_fd_table | Object handle hijack or resource leakage resulting in cross-process data leakage. | Data Leakage & Context Poisoning |
| Medium | kernel_scheduler | Cyclic JSON structures or heavy validation payloads causing parser loops or OOM. | Denial of Service (DoS) |
