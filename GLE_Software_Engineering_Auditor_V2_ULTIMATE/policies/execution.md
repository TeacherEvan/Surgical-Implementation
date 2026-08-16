# Execution Policy

## Safe by default
- read files
- search repository
- create planning artifacts
- run non-destructive tests
- static analysis
- local build

## Approval required
- deletion outside explicitly approved scope
- destructive database migrations
- production deployment
- credential rotation
- permission changes
- external account actions
- irreversible operations

## Principle
The agent must know what a command is expected to do before executing it.
