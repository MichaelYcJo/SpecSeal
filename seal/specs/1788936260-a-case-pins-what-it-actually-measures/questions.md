# Questions: a case pins what it actually measures

Routing was not re-asked: the owner approved a recommendation naming both
tickets, the pairing and the order. What follows are the two things the
checker's shape leaves open, and neither blocks the enumeration.

## Q1 — what the checker's exit code means

**The owner's, and it is the difference between a report and a gate.**

| Answer | What it costs | What it gives up |
|---|---|---|
| **Report only, always exit 0** | nothing; it is a thing a person runs | nothing stops a change that leaves a new arm unwatched, which is the state #262 is about |
| Exit non-zero on any unwatched arm | the first run fails on nine arms nobody is fixing today, which is the *red on history nobody can fix* that `chain_check.py:127` argues makes a check people skip | — |
| **Exit non-zero when the count RISES above a recorded baseline** | one recorded number, and a number in a file is the thing #262 says rots | it is the cheapest shape that refuses a regression without failing on the backlog. `issue_claims_check.py` chose report-only on one measured occurrence; here the count is nine |

The plan builds the enumeration and the report either way. The exit rule is
one arm and can be added after the first run's number exists.

## Q2 — is nine unwatched arms a failure or a baseline

Related and separate. #262 already says two of the nine are
behaviour-preserving rather than gaps, so the checker's first report is not a
list of nine defects. Whether the other seven get cases, and in what release,
is a scheduling decision the report exists to inform.

| # | Assumption | Why it does not wait |
|---|---|---|
| 1 | The checker starts at `hooks/review-history-guard.py` alone | It is the module whose arms were counted by hand, and the only one with a measured expectation to check the walk against |
| 2 | Its enumeration refuses an AST node type it does not recognise rather than skipping it | A walk that skips silently is the failure of the thing it replaces. Refusing costs a line in the report and is the only defence the plan can name |
| 3 | The ticket's table of 33 is left as written | It was true when measured, and the file changed twice after. Correcting a shipped ticket's measurement would hide the argument the ticket makes |
