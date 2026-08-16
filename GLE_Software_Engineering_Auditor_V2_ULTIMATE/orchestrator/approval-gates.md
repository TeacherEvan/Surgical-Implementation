# Approval Gates

## AUTO
- read repository
- search repository
- create/update planning artifacts
- run non-destructive tests
- run static analysis

## REVIEW
- broad refactors
- security-sensitive changes
- dependency upgrades with meaningful risk

## APPROVAL_REQUIRED
- delete important data/files
- destructive database migration
- production deployment
- credential rotation
- permission changes
- external account changes
- irreversible operations

## BLOCKED
Any operation prohibited by the host/user policy.
