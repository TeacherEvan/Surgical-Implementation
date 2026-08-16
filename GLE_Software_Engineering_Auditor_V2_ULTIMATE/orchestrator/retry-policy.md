# Retry Policy

## Consistency
Maximum: 5 failed/repeated planning cycles.

Each retry must:
- record the failure
- identify the exact inconsistency
- state the corrective action
- increment run number

At 5 failures: STOP_AND_REQUEST_USER.

## Verification
Use a bounded retry budget configured by the host.

Never use:
`while tests fail: keep fixing forever`

Instead:
1. classify failure
2. determine whether authorized
3. apply targeted fix
4. rerun
5. stop at budget
