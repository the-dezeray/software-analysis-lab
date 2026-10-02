# Lab 4 - Requirements Traceability Matrix (my version)

| Requirement ID | Requirement Description | Test Case ID(s) | Test Level | Status |
|----------------|-------------------------|------------------|------------|--------|
| FR-01 | Add task with title (default priority 1, not done) | TC-01 | Unit | Pass |
| FR-02 | Mark task done by ID (True/False) | TC-02 | Unit | Pass |
| FR-03 | List all pending tasks | TC-03, TC-04 | Unit, Integration | Fail (TC-03 fails; TC-04 not run) |
| FR-04 | Average priority; 0 when empty | TC-05, TC-06 | Unit | Fail (TC-05 fails; TC-06 not run) |
| FR-05 | Find first task by title / None | TC-07 | Unit | Not run |
| FR-06 | Remove task by ID | TC-08 | Unit | Not run |
| FR-07 | 20% discount for premium; validate price 0-10000 + bool flag | TC-09, TC-10 | Unit | Partial (TC-09 pass; TC-10 fail on invalid inputs) |

Coverage: 7/7 requirements have at least one test case. 3/7 fully passing, 2 failing with known defects (DEF-01, DEF-02), 1 partial, 2 not yet automated.
