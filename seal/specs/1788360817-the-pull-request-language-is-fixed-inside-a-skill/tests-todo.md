# regression tests to plant — prescribed by round 1, planted by the implementer

All in `tests/test_the_pull_request_language_is_the_repositorys.py` unless a row says otherwise.

| # | What it asserts | Grounds | Status |
|---|---|---|---|
| 1 | a `seal/config.md` holding the template's default row leaves the mirror case green, and a non-English row is what the case reads instead of the file's absence | round 1 🟡 5: today the file turns it red whatever the row says | ✅ planted |
| 2 | the skill says an empty value and an unreadable file land on English, beside the two absences it already names | round 1 🟡 3 | ✅ planted |
| 3 | a row of a different table ends the table rather than being skipped: `| a | b | c |` between two two-cell rows leaves the row after it out | round 1 🟡 6 | ✅ planted |
| 4 | every file under `templates/` is named by at least one document that is not a line-width list — a shipped template with no consumer is unreachable | round 1 🟡 1, and the check is worth having for the whole directory rather than this one file | ✅ planted |
| 5 | a config naming a language outside `LANGUAGE_CODES` does not raise out of the mirror case | round 2 🔴 1 | ✅ planted |
| 6 | `configured_language` finds a config under `<root>/.git/seal/` as well as `<root>/seal/` | round 2 🟡 2 | ✅ planted |
| 7 | both the skill and the template resolve the mirror's home and exclude the git directory | round 2 🟡 3 | ✅ planted |
| 8 | the templates check reads only prose documents and descends into subdirectories | round 2 🟡 4 | ✅ planted |
| 9 | a separator below the rows, and a repeated `\| Item \| Value \|` header, both end the table | round 2 🟡 5 | ✅ planted |
| 10 | every committed mirror's code is one this file knows — `pr.kr.md` is caught | round 2 🟡 7 | ✅ planted |
| 11 | an untracked file under `templates/` — a `.DS_Store` — is not a template the check reports | round 3 finding 1 | ⬜ |
| 12 | `mirror_to_refuse("**Korean**")` and `mirror_to_refuse("korean")` both answer `pr.ko.md`, and `"French"` still answers `None` | round 3 finding 2 | ⬜ |
| 13 | the fields `templates/sdd-round.md` carries are the fields `skills/code-review/SKILL.md` lists — the sentence's remaining claim, pinned | round 3 finding 3 | ⬜ |
