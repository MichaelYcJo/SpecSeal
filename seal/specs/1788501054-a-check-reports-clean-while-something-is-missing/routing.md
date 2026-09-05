# 1788501054-a-check-reports-clean-while-something-is-missing — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/153-150-a-check-reports-clean-while-something-is-missing |

Answered 2026-09-04 by the repository owner, before the first edit.

## Why this way

Two tickets, one branch. **Not for the reason #110 + #117 shared one** — apart
these do not undo each other. They are the same shape (a check reports clean
while something is missing, and the missing thing leaves no trace), they land
in the same two files, and a review chain is the expensive unit at roughly
forty to a hundred minutes.

The risk is stated rather than discovered: this release has three times seen a
branch break the rule it was adding — the floor refusing the only legal end to
a run, the roll's guard breaking its own invariant, the `Ran by` row removing
the coverage of its own grandfathering arm. **Two rules on one branch doubles
that**, and it is the first thing the rounds are told to attack.
