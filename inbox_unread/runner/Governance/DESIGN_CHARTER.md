# Sun and Night Architecture Charter

> **"AI proposes. Runtime decides."**

## Core Principles
1. **Evidence Before Inference**: Every system action must originate from a verified, immutable evidence trace.
2. **Deterministic Runtime**: The execution runtime operates with 0% reliance on probabilistic AI models.
3. **Hypothesis Isolation**: AI outputs are strictly scoped to the `Intelligence/Hypothesis` layer and have no authority over `Policy` or `Guard`.
4. **Zero Mutation / Non-Contamination**: Process execution must never pollute the parent shell's Environment Variables or File Descriptors (FD).
5. **Human Approval Boundary**: AI proposals transition to Runtime Policy only through explicit, deterministic verification or human approval.
