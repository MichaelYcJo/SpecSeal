# 1788395377-the-release-guard-globs-one-place — review round 2

<!-- The verifying round for round 1's fixes (target: the diff 5c69b96..7607d12).
It closed all six and opened five, every one inside the fix commit rather than
in the change round 1 reviewed — that commit added three surfaces the branch
did not have, and did not re-examine them. All five are fixed at c1748e4 and
round 3 verifies them. Written by the review orchestrator, which is also this
work item's implementer. -->

| Field | Value |
|---|---|
| Target SHA | 7607d12 (the fix diff from 5c69b96); HEAD 1fb5507 at review time, record-only |
| PR | none yet |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes landed at c1748e4 and round 3, the verifying round, is what opens them; this cell is set to it when that record exists |
| Contract changes | `hooks/review-history-guard.py`'s posting reminder → the string a session reads, no unit's signature: `round-N.md` is now spelled from the work item like the two beside it; `test_the_two_todo_files_sit_where_the_release_guard_looks` → itself only — one assertion became two, so the case fails when either file leaves the work-item level rather than only when both do |
| New units | `tests/test_chain_hooks.py#test_the_posting_reminder_spells_all_three_paths_from_one_base` |
| Needs a fix | yes — 1 (the blindness sentinel became an OR and passes with every `evidence-todo.md` gone from the work-item level), 2 (the skill's new paragraph says the guard reads both todo files and it reads one), 3 (the reminder spells two of three paths from the repository root and the third from the work item), 4 (the memo's rewritten rung grounds answer one clause of the ladder's five while the same commit put the work on three others), 5 (the changelog fragment describes the move alone) |

- [ ] Pass

## What this round is really about

Round 1 reviewed four renames, one test and three record files. Its fixes
added three surfaces the branch had never had: a hook's output, a skill's
instructions, and a table in a specification. Four of the five findings below
are that commit not re-reading what it had just written — including the
sentence in which it re-justified the work item's rung.

That is the same shape #82 measured five times and it is worth one line here:
**a fix commit is a change, and the round that wrote it is not the round that
reviewed it.**

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r1 🔴 1 | the memo header CI cannot read | `overview.md` | answered — the fix is round 1's, this round reproduced its closure | reviewer executed the CI command: `16 overviews · 36 open · 15 closed · 0 unreadable`, exit 0, and read that `templates/sdd-overview.md:48` already carried the right header — a hand-typed deviation rather than a taught one |
| r1 🟡 2 | the glob one directory deep | `tests/…:327-337` | answered — reproduced | reviewer executed on built shapes: the pattern reaches one, two and three directories down and does not reach the correct location, because `**` matches zero segments |
| r1 🟡 3 | the dead `todo-*.md` pattern | same case | answered for the pattern; the guard it was traded for is this round's 1 | reviewer read |
| r1 🟡 4 | the three documents naming only `rounds/` | the hook, the spec, the skill | answered on agreement; two sentences inside the fix are this round's 2 and 3 | reviewer executed `git grep` over the whole tree: `rounds/tests-todo` has no hits, `rounds/evidence-todo` only the prose round 1 deferred |
| r1 🟡 5 | the rung justified by file count | `overview.md:4-6` | answered for the count; the sentence that replaced it is this round's 4 | reviewer read the ladder |
| r1 🟡 6 | five prose mentions of the old path | the ledger | answered — correctly deferred, not re-litigated | reviewer read |
| r1 ledger re-read | the `r3 3 / r4 2` row | `seal/ledger/1788360817-…md` | pass, and one thing the note did not cover | reviewer opened both clauses itself: clause one reads the template and nothing else, clause two is an absence test the added paragraph does not contain, 66 cases green. It also found a **second** row re-hashed on the same anchor with no re-read paragraph — checked it too, honest, but a reader could not have told |
| 1 | the sentinel became `glob(evidence-todo) + glob(tests-todo)`, so it passes when every `evidence-todo.md` has left the work-item level as long as one `tests-todo.md` remains — the exact blindness this work item closes, since `fold_ledger.py:252` globs that one filename and nothing in the tree opens the other. The assertion text still said "no evidence-todo file at all" while firing only when neither exists | `tests/test_the_set_a_work_item_always_has.py:343-345` | fixed at c1748e4 — two assertions, each with the reason its file must be there | reviewer executed a tree with only a `tests-todo.md`: passes before, and the orchestrator executed after the fix — moving every `evidence-todo.md` away turns it red |
| 2 | the skill's new paragraph said the guard reads "them", the two todo files, with the one-file glob quoted in the same parenthesis | `skills/code-review/SKILL.md:141-143` | fixed at c1748e4 — it names `evidence-todo.md` and says `tests-todo.md` keeps it company because the layout is one rule rather than two | reviewer read; `git grep` over `*.py *.yml *.sh` finds no script that opens `tests-todo.md` |
| 3 | the reminder spelled `tests-todo.md` and `evidence-todo.md` from the repository root and `round-N.md` from the work item, so a session typing the three paths it was handed gets one in the wrong place. The hook's own comment states the standard this breaks — *the path a person has to recognise and then TYPE*. Before the fix all three were work-item-relative and consistent | `hooks/review-history-guard.py:206-209` | fixed at c1748e4 — one substitution; `where` already holds the work item's `rounds/` | orchestrator executed both ways with the planted case: red against the old message, 20 passed against the new one |
| 4 | the rewritten rung grounds answer one clause of the five `skills/implement/SKILL.md:508` puts on the rung above, and the same commit put this work on three of the others: a hook's output, a skill's instructions, and text a person reads and acts on. The skill forecloses the obvious defence at `:520` with a worked example that counts files arriving in review rounds. Round 1 could not have seen it — none of the three existed at `5c69b96` | `overview.md:4-9` | fixed at c1748e4 — the verdict cannot be repaired after the fact and the grounds can: the note now records that those three went in without the plan the rung asks for, and that round 2 is what found it | reviewer executed `git diff --stat 30b538b..1fb5507` |
| 5 | the changelog fragment was written at `5c69b96` and describes the move alone, so a person updating the plugin meets a changed reminder and a changed instruction with no line to read. `gather_changelog.py` folds it at the next release, so the omission ships | `changelog.md` | fixed at c1748e4 — a second paragraph names the reminder, the spec and the skill, and why the rule is said where a session meets it | reviewer read |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the glob on built shapes at depths 0, 1, 2, 3 | reaches 1–3, does not reach 0 |
| reviewer: the sentinel with only a `tests-todo.md` present | passes before the fix |
| reviewer: the reminder rendered verbatim, before and after the proposed substitution | two bases before, one after |
| reviewer: `git grep` for `rounds/tests-todo`, `rounds/evidence-todo` across the tree, and for either name across `*.py *.yml *.sh` | only the deferred prose; no script opens `tests-todo.md` |
| reviewer: `evidence_check --strict .`, `unverified_check --baseline`, `fold_ledger --check` and `gather_changelog --check` at two revisions | 357 ok · 0 drifted; exit 0; both `--check`s byte-identical at base and head |
| reviewer: the two ledger clauses opened against the edited section | both green, 66 cases |
| orchestrator: the planted reminder case against the pre-fix message, then the fixed one | 1 failed, then 20 passed |
| orchestrator: every `evidence-todo.md` moved off the work-item level, then restored | red, then 13 passed |
| orchestrator: `evidence_check --reverify .` then `--strict .` after the skill edit | the same section re-hashed a second time; 357 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `tests/test_the_set_a_work_item_always_has.py`'s new case, `hooks/review-history-guard.py`'s posting branch | the two units this run has changed twice |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 6 of round 1 — five prose mentions of the old path, one folding into the gathered ledger at the next release | round 1's record and the pull request body | the repository owner, at the release |
| A ledger row re-hashed with no re-read note, which a reader cannot distinguish from an honest one | issue #97, which is the axis: an artifact carrying a claim nothing checks | the repository owner, at 0.6.0 |
| The guard refusing a real release with a real open row | `overview.md` §Not verified | the repository owner, at the first release that meets one |
