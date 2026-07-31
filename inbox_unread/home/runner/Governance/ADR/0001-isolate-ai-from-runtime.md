# ADR 0001: Separation of Probabilistic AI from Deterministic Runtime

* **Status**: Accepted
* **Date**: 2026-07-24
* **Deciders**: LuciFeR0x0systeM (Sovereign Architect)

## Context
Generative AI models are non-deterministic. Allowing AI to directly invoke system calls or modify runtime policies introduces execution instability and safety hazards.

## Decision
We enforce a strict physical boundary:
- AI operates exclusively inside `Intelligence/`.
- AI generates `Hypothesis` items only.
- `Runtime/Policy` evaluates hypotheses strictly via deterministic logic or human approval.
