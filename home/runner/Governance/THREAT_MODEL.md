# Threat Model & Risk Matrix

| Threat ID | Threat Description | Mitigation Strategy | Evidence / Assurance | Residual Risk |
| :--- | :--- | :--- | :--- | :--- |
| **TM-01** | AI Hallucination / Malicious Directive | Confine outputs to `Hypothesis`; enforce `Evaluator` gate. | `sun.evidence.v1` log | Low |
| **TM-02** | FD / Environment Variable Contamination | Isolated execution bridge via `.saac_devil_runtime/jssh_bridge.sh`. | Subshell isolation | Negligible |
| **TM-03** | CI Auto-Push Infinite Loop | Enforce Read-Only CI actions (`contents: read`); zero auto-commit. | CI Integrity Audit | None |
| **TM-04** | Runtime / Policy Mutation | File-hash verification (`integrity_check.sh`) before kernel boot. | Cryptographic hash | Very Low |
| **TM-05** | RPC / Data Spoofing | Multi-node resonance checking and circuit breakers. | Resonance score | Low |
| **TM-06** | Filesystem Enumeration Probe | Active process monitoring via `scanner.sh`. | Audit Alert Log | Low |
