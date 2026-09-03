# A language row that governs four things — plan

| Phase | What | Status |
|---|---|---|
| 1 | `templates/config.md`: rename the first row, add the second, rewrite both sections, widen the exclusion list | |
| 2 | `skills/commit-pr-convention/SKILL.md`: the row's new name, the posted report added to what it governs | |
| 3 | The record side: `skills/implement/SKILL.md`, `agents/smith.md`, `agents/warden.md`, `skills/code-review/SKILL.md` name `Record language` and the strings that stay English | |
| 4 | Both READMEs | |
| 5 | `tests/test_the_pull_request_language_is_the_repositorys.py`: the row's name throughout, and cases for the second row and for the absence of coupling | |

Phase 5 is where the work is: 37 test functions read the row's name as a
string, and the file is what pins every claim in phases 1 to 4.
