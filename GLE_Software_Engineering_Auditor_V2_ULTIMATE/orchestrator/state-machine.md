# Orchestrator State Machine

| State | Entry condition | Exit condition | Failure |
|---|---|---|---|
| INIT | Run created | manifest initialized | stop |
| DISCOVER | INIT complete | baseline gathered | request user if inaccessible |
| REQUIREMENTS | discovery available | acceptance criteria defined | request clarification |
| RESEARCH | requirements defined | research ledger complete | research warning |
| CODEBASE_STATE | discovery complete | baseline artifact complete | stop |
| ARCHITECT | baseline/research available | architecture complete | revise |
| PLAN | architecture complete | ≥10 meaningful objectives | revise |
| CONSISTENCY_GATE | all planning artifacts exist | reviewer PASS | replan |
| IMPLEMENT | gate PASS | objectives implemented/blocked | stop on authorization issue |
| VERIFY | implementation available | evidence complete | diagnose/fix/retry |
| SECURITY_AUDIT | implementation verified | audit complete | block if critical |
| FINAL_AUDIT | all evidence available | final status assigned | block |
| DEBRIEF | audit complete | report complete | revise |
| HANDOFF | report complete | handoff recorded | revise |
| COMPLETE | all gates passed | run closed | none |
