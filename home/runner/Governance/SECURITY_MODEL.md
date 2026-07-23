# Security & Isolation Model

## Boundary Enforcement
- **Process Boundary**: All execution streams passing to `jssh` or external scripts run inside `.saac_devil_runtime/sandbox.sh`.
- **Capability Registry**: Only actions declared inside `Capabilities/capabilities.json` are allowed execution paths.
- **Audit Trails**: Security scanning detects unauthorized filesystem traversal (`find`, `grep`, `rg` abuse) and flags alerts.
