# Independent implementation review

Review the current Git diff and the relevant surrounding code.

Do not modify any files.

First reconstruct:
- the intended behavior,
- the existing architecture,
- the invariants affected by the change.

Then verify:
- correctness,
- edge cases,
- compatibility with existing behavior,
- error handling,
- test quality and missing tests,
- unnecessary complexity,
- inconsistencies between documentation, tests, and implementation.

Run appropriate tests when useful, but do not fix failures.

Treat tests as evidence, not as proof that the implementation is correct.
Look for cases where the implementation and tests could be wrong in the
same way.

Report only actionable findings, ordered by severity.

For every finding provide:
- severity,
- file and line,
- why it is incorrect or risky,
- a concrete failure scenario,
- recommended correction.

Finish with:
- requirements apparently satisfied,
- requirements not demonstrated,
- tests you recommend adding.