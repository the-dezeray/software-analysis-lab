# Lab 4 - Comparison: AI-generated RTM vs mine

## Where it diverged
1. Test Case IDs: AI collapsed my 10 cases into 7 (one per requirement). It dropped TC-04 (integration retest of FR-03), TC-06 (normal average), TC-10 (invalid discount inputs from Lab 3) - exactly the cases that catch the real bugs.
2. Status column is fiction: AI marked all 7 rows Pass. Actual `pytest -v` run (02/10/2026): TC-03 fails (DEF-01, off-by-one), TC-05 fails (DEF-02, ZeroDivisionError), 4 Lab-3 invalid-input cases fail. 3 of 7 requirements are not green.
3. Test levels wrong: AI labelled FR-03 and FR-05 "System" (they are unit-level function calls; only my TC-04 cross into integration via complete+list) and FR-07 "Integration" (it is a pure unit function).
4. Descriptions vague: "Search tasks", "Show average priority", "Discounts" lose the acceptance criteria (first-match/None, 0-when-empty, price 0-10000 + bool flag) that my RTM and Lab 3 tables pin down.

## Which version would I trust for an audit?
Mine. The AI draft looks tidy but is unauditable: invented TC IDs with no mapping to `tests/`, no Fail/Not-run statuses, and no link to DEF-01/DEF-02. An auditor checking FR-03 would find TC-03 failing and TC-04 missing - my RTM shows that, the AI one hides it. Same lesson as Lab 3: AI is fine for the first draft of normal cases, bad at invalid/edge cases and at reporting real verdicts. I would attach the AI draft as a working note only, never as the audit record.
