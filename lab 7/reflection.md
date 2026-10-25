# Reflection - coverage vs mutation score

## The numbers

Lab 6 reported the same 45% total coverage for the AI-only, manual-only and
combined suites. Coverage could not tell the two suites apart.

Lab 7 shows a real difference:

| Suite | Lab 6 coverage (total) | Lab 7 target mutation score |
|-------|------------------------|-----------------------------|
| AI-only | 45% | 80.0% |
| Manual-only | 45% | 100.0% |
| Combined | 45% | 100.0% |

The 20-point mutation gap with zero coverage gap is the main lesson: line
coverage says the code ran, not that the test checked the result. The AI suite
executed the same `format_task_report` lines as the manual suite but asserted
only "returns a string" and "contains the title". That was enough to run the
code, but not enough to notice a changed prefix, a changed separator, or a
changed newline join. The manual suite's exact-string assertions killed all
three mutants.

This matches the Lab 6 assertion counts: the AI suite had 9 assertions across
8 tests, while the manual suite had 19 across 10 tests. More assertions are
not automatically better, but assertions that pin the output contract are.

## What the gap tells me about test quality

1. **Coverage is necessary but not sufficient.** A line can be 100% covered
   and still be wrong in production because no test asserts the right result.
2. **Mutation score measures the oracle, not just execution.** It asks whether
   the test suite would fail if the code changed behaviour. That is closer to
   the question we actually care about.
3. **Weak assertions create false confidence.** The AI report tests passed
   while the report format could be visibly wrong. A green suite is only as
   meaningful as its assertions.
4. **Scope matters when reading mutation scores.** The all-mutant score is
   low (26-40%) because most mutants are in functions Lab 6 never targeted.
   That is missing coverage, not necessarily weak assertions. The fair
   comparison is the 15 mutants inside the three target functions.
5. **The two techniques are complementary.** Coverage finds unexecuted code;
   mutation testing finds under-asserted code. Running both gives a much more
   honest picture than either alone.

## Did the AI suite have any value?

Yes. It found the `format_task_report` crash in Lab 6 (two tests failed), and
it killed all `find_task_by_title` and `remove_task` mutants. It is a useful
first draft and crash finder. The manual suite was stronger on exact output
contracts, which is exactly where the AI suite left survivors. The best suite
is the combination: broad execution plus precise assertions.
