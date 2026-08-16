# Failure Taxonomy

- CODE_FAILURE — implementation defect
- TEST_FAILURE — test defect
- ENVIRONMENT_FAILURE — local/CI environment issue
- DEPENDENCY_FAILURE — dependency unavailable/incompatible
- DATA_FAILURE — fixture/test data problem
- NETWORK_FAILURE — transient/unavailable network resource
- AUTHORIZATION_FAILURE — required permission/approval missing
- SECURITY_BLOCK — unsafe operation detected
- SCOPE_FAILURE — work exceeded authorized scope
- RESEARCH_CONFLICT — sources materially disagree
- UNKNOWN — insufficient evidence

Every failure should record category, evidence, impact and next action.
