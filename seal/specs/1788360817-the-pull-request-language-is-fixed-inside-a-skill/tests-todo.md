# regression tests to plant — prescribed by round 1, planted by the implementer

All in `tests/test_the_pull_request_language_is_the_repositorys.py` unless a row says otherwise.

| # | What it asserts | Grounds | Status |
|---|---|---|---|
| 1 | a `seal/config.md` holding the template's default row leaves the mirror case green, and a non-English row is what the case reads instead of the file's absence | round 1 🟡 5: today the file turns it red whatever the row says | ⬜ |
| 2 | the skill says an empty value and an unreadable file land on English, beside the two absences it already names | round 1 🟡 3 | ⬜ |
| 3 | a row of a different table ends the table rather than being skipped: `| a | b | c |` between two two-cell rows leaves the row after it out | round 1 🟡 6 | ⬜ |
| 4 | every file under `templates/` is named by at least one document that is not a line-width list — a shipped template with no consumer is unreachable | round 1 🟡 1, and the check is worth having for the whole directory rather than this one file | ⬜ |
