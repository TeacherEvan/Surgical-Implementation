# Consistency Reviewer


## Purpose
Check that planning artifacts agree.

## Compare
REQUIREMENTS ↔ CODEBASE-STATE ↔ ARCHITECTURE ↔ TODO

## Check
- scope
- terminology
- files/modules
- dependencies
- acceptance criteria
- sequence
- research decisions

## Failure
Write a run log, revise artifacts, and retry. Maximum 5 consistency cycles.
After 5 failures: STOP_AND_REQUEST_USER.