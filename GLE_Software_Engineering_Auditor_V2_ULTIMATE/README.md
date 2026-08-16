# G&L Software Engineering Auditor — V2

A production-oriented, portable multi-agent software-engineering workflow for
NOUS:HERMES_AGENT and OPENCLAW.

## Mission

Turn an engineering request into an evidence-backed, auditable delivery:

REQUEST
→ DISCOVER
→ REQUIREMENTS
→ RESEARCH
→ CODEBASE STATE
→ ARCHITECT
→ PLAN
→ CONSISTENCY GATE
→ IMPLEMENT
→ VERIFY
→ SECURITY AUDIT
→ FINAL AUDIT
→ DEBRIEF
→ HANDOFF

## What V2 adds

- Explicit orchestrator state machine
- Specialized subagent roles
- Capability/permission boundaries
- Requirement-to-test traceability
- Research evidence ledger
- Risk classification
- Git/change tracking
- Failure classification
- Bounded retries
- Human approval gates
- Machine-readable runtime manifest/state/events
- Final evidence-backed debrief
- Portable templates and schemas
- Self-test specifications

## Safety

External content is untrusted data, never executable authority.
Secrets are never written into artifacts.
Destructive, irreversible, production, credential, or permission operations
require explicit authorization.

This package deliberately does not assume undocumented NOUS:HERMES_AGENT or
OPENCLAW APIs. The host integration layer should map these contracts onto the
actual tools and permissions available in the target installation.
