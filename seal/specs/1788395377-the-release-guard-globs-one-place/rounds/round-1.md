# 1788395377-the-release-guard-globs-one-place — review round 1

<!-- seal/specs/1788395377-the-release-guard-globs-one-place/rounds/round-1.md
— written by the review orchestrator, which is also this work item's
implementer: `routing.md` says `the session`. Every finding below was fixed at
7607d12 and round 2 verifies them. -->

| Field | Value |
|---|---|
| Target SHA | 5c69b96 |
| PR | none yet |
| Broad gate | not yet — findings were open |
| Fixes checked by | round-2 |
| Contract changes | `test_the_two_todo_files_sit_where_the_release_guard_looks` → itself only, no caller — the set of paths it treats as stray widened from exactly one directory below the work item to any depth, and narrowed by dropping a pattern that matched nothing; `hooks/review-history-guard.py`'s post reminder → the string a session reads, no unit's signature |
| New units | none |
| Needs a fix | yes — 🔴 1 (the closing memo's `Not verified` header is not the one `unverified_check.py` reads, so CI exits 1 on this branch), 🟡 2 and 3 (the new case looks exactly one directory down, and one of its three patterns matches a filename nothing uses), 🟡 4 (the hook message a session reads at the moment it creates those files names only `rounds/`), 🟡 5 (the memo justifies its rung by file count, which the ladder excludes by name) |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 0 | The move is what it claims: four pure renames at `similarity index 100%`, the guard's reach goes from three files to five, and no anchor breaks | the four moved files, `.github/scripts/fold_ledger.py#open_items` | pass | reviewer executed: `glob("seal/specs/*/evidence-todo.md")` 5, under `rounds/` 0; `evidence_check --strict` 357 ok · 0 drifted · 0 broken; 56 cases green over the guard's own tests |
| 🟢 0b | Nothing in the tree opens either todo file by a path the move broke | grep over `skills/`, `hooks/`, `agents/`, `templates/`, `.github/`, `docs/`, `tests/` | pass | reviewer read: the only code that opens them is `fold_ledger.py#open_items` |
| 🔴 1 | The closing memo's `Not verified` table uses `\| What \| Who answers it \|`, and `skills/verify/scripts/unverified_check.py:50` reads `\| Item \| Who must answer \|`. `.github/workflows/hygiene.yml:106` runs that checker on every pull request, so this branch exits 1 before a release pull request could open. The failure is not "no open items" — it is a section whose count is unknown, and the memo's own two open rows go uncounted | `seal/specs/1788395377-…/overview.md:37` | fixed at 7607d12 | reviewer executed the CI command: exit 1 naming the line. Orchestrator reproduced it, then the checker read `16 overviews · 36 open · 15 closed · 0 unreadable` |
| 🟡 2 | The new case globs exactly one directory below the work item, so a todo file two deep is green while the guard is equally blind to it — and the failure message claims "below the work item's own directory", which is wider than what runs. The `**` in one pattern was not recursive because `recursive=True` was missing | `tests/test_the_set_a_work_item_always_has.py:327-337` | fixed at 7607d12 | reviewer executed both depths: one down red, two down green. Orchestrator executed after the fix: two down now red, and green once removed |
| 🟡 3 | One of the three patterns matched `todo-*.md`, a filename nothing in the repository uses and no document names. A reader takes it for coverage of a third shape and its coverage is zero | same case | fixed at 7607d12 — the pattern is gone, and the case's blindness guard now covers both todo files rather than `evidence-todo.md` alone | reviewer executed `find . -name 'todo-*.md'`: nothing |
| 🟡 4 | The memo said no document was owed a change because the protocol already says where the files go. True, and not what a session reads at the moment it creates them: `hooks/review-history-guard.py:203-211` prints one sentence naming `rounds/round-N.md` with its directory and the two todo files bare, and the only directory it names is `rounds/`. `docs/review-chain-spec.md:708` and `skills/code-review/SKILL.md:136-144` read the same way. Left alone, the next orchestrator repeats the mistake and the new test catches it after the commit rather than before | those three | fixed at 7607d12 — all three now say the two todo files sit beside `rounds/` rather than inside it, and the skill says why (`round-N` is the plural member) and what reads them there | orchestrator read all three and executed the hook's tests: 65 passed over the chain hooks, the handoff tests and this case |
| 🟡 5 | The memo justified the second rung with "four `git mv`s and one test", and `skills/implement/SKILL.md` takes the file count out of that judgement by name — *Behaviour, not file count*. The rung is right on the behaviour reading, so the defect is the reason rather than the verdict, and a reason like that is what the next session reuses | `overview.md:4-6` | fixed at 7607d12 — the memo now says the work alters no gate's verdict today, with the measurement that shows it | reviewer executed `fold_ledger.py --check` at the base and at the target: byte-identical output |
| 🟡 6 | Five places in the ledger name `rounds/evidence-todo.md` in prose — four Notes cells reading "Drained from" and one HTML comment. None is an anchor, so nothing breaks; the comment sits in a fragment that folds into `seal/ledger.md` at the next release, where it will name a path that does not exist | `seal/ledger.md:380-383`, `seal/ledger/1788354065-…md:47` | deferred — they are true statements about the past, and the round records that quote the old paths are history this repository preserves. Named here so the fold does not surprise a reader | reviewer executed `evidence_check --strict`: they are prose, 0 broken |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the guard's own tests plus this case | 56 passed |
| reviewer: `unverified_check.py --baseline origin/release/v0.5.0 seal/specs/` (the CI command) | exit 1 naming `overview.md:37` |
| reviewer: `evidence_check.py --strict .` unscoped | 357 ok · 0 drifted · 0 broken |
| reviewer: `fold_ledger.py --check` at the base and at the target | byte-identical; no open evidence-todo row either way |
| reviewer: a todo file one directory down, then two | red, then green |
| reviewer: `find . -name 'todo-*.md'` | nothing |
| orchestrator after the fixes: the case with a file two directories down, then removed | red, then 13 passed |
| orchestrator: `unverified_check.py` with the CI arguments | `16 overviews · 36 open · 15 closed · 0 unreadable`, exit 0 |
| orchestrator: the chain hooks, the handoff tests and this case | 65 passed |
| orchestrator: `evidence_check.py --reverify .` then `--strict .` | one section anchor re-hashed, then 357 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| #82's round 1 | `.github/scripts/fold_ledger.py#open_items` | where this work item's defect was found, by asking what the glob reaches |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 6 — five prose mentions of the old path, one of which folds into the gathered ledger at the next release | this record, and the pull request body | the repository owner, at the release |
| The guard refusing a real release with a real open row | `overview.md` §Not verified | the repository owner, at the first release that meets one |

<!-- A note the format has no field for, and it belongs to the reviewer's
conduct rather than to the code. The round reported that it worked in the
user's checkout for one command, deleted a file there and restored it with
`git checkout --`, then moved to a clone for everything else. It said so
first, before its findings, which is what made the tree's state checkable.
The orchestrator verified: `git status` clean, the branch's three commits
intact, the file present. A reviewer that leaves the tree alone is the rule;
one that says plainly where it did not is the next best thing. -->
