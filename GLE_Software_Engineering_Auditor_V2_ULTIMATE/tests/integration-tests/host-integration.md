# Host Integration Test Specification

The host adapter should prove that:

1. The skill can be registered.
2. The orchestrator can create a run manifest.
3. Agents receive only intended capabilities.
4. Artifacts are created in the expected workspace.
5. External research cannot directly invoke execution.
6. Consistency retry count cannot exceed 5.
7. Verification retries are bounded.
8. Human approval is required for configured high-risk operations.
9. Final audit can block READY.
10. Debrief is produced only after final audit.
