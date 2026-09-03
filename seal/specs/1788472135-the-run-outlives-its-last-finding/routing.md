# 1788472135-the-run-outlives-its-last-finding — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/the-run-outlives-its-last-finding |

Answered 2026-09-04 by the repository owner, before the first edit.

## Why this way

#110 removes the late rounds and #117 removes what those rounds were catching,
so the branch changes the review chain's own stopping behavior — it goes
through the chain it edits. The run is unattended, which is also why the two
new record fields are enforced by `chain_check.py` rather than recorded for a
person to read: a field no check reads is only true when somebody is awake.
