# Follow-up

**What belongs here, and it is a narrow list.**

A **schedulable item in a repository with no tracker** — something a person
could plan, in a project that has nowhere else to file it. This repository has
a tracker, so it should normally hold none of those.

**Every row names a person, with no condition attached.** An answerer column
reading `repository owner, next time X is opened` is a
condition wearing a person's clothes: nobody agreed to open `X`, so nobody
answers. A row that
cannot name who answers it does not belong in this file.

**Anything tied to a coordinate is a `# RIDER:` comment at the line it is
about.** `grep -rn "RIDER:"` is the repository-wide list, and it needs no file
kept in sync. A rider is not "someone should do this" — it is *"if you open
this file, do this too"*, and its whole value is arriving at the person who
opens the file. Moving it to the coordinate is what makes `next time X is
opened` do its job instead of being written down as though a person had
promised it.

An issue is no better for that purpose. It reaches whoever browses the
tracker; nobody greps the issue list before editing a hook. And a rider has no
completion of its own — it closes when the file it rides on is next changed,
which nothing can schedule.

**What that costs.** Nothing forces a rider to be deleted, so a comment can
outlive the fix it asked for and the next reader cannot tell a live one from a
spent one. Each therefore carries **the date it was read and the content it
was read against** — `Verified <date> against <anchor>@<hash>`, where the
anchor is the ledger's own: a symbol name, a heading path, or a quoted line,
resolved in the rider's own file. `.github/scripts/rider_check.py` checks
every one and `--reverify` re-stamps them; the path the ledger writes is left
off because a rider IS the coordinate. The judgment is that a rider outliving
its fix costs a confused reader for a minute, while a rider nobody ever sees
costs the defect. **This is written down so it can be overturned**: if the
stamps go stale faster than they are read, the trade was wrong and the list
comes back.

**A stamp used to name a commit, and this repository's merge rule destroyed
the commits it had to name** (#239). A fix pass runs on a feature branch, a
feature branch squashes into its release branch, and the squash keeps none of
the branch's own commits — so the check failed on the RELEASE branch, where
whoever met it was never whoever caused it, and no mistake was required
anywhere. `skills/evidence-check/SKILL.md` already cited that failure as one
of the four grounds for deriving a ledger anchor from content; this is the
same repair reaching the mechanism that supplied the evidence.

A drifted rider is **the rider firing**, not a chore: it says somebody edited
the unit and did not answer the comment sitting in it, which is the arrival
this whole arrangement is for. Read it, then either do what it asks and delete
it, or re-stamp.

## Schedulable items with nowhere else to go

| Item | Who must answer |
|---|---|
| `evidence-check` ignores a ledger row whose coordinate is malformed instead of naming it. Found while writing a row during round 1's fix pass of #237: a coordinate written `path#unit@0` — a placeholder hash that is not eight hex characters — produced **no row at all**. Executed: the total stayed at 771 with the row present, `--strict` reported `0 broken`, and `--reverify` reported `0 rows re-verified`; the same row with `@00000000` was picked up and re-verified on the next run. So a typo in a hash does not drift and does not break, it removes the claim from the ledger silently, which is the one direction a checker of claims must not fail in. The fix is to count a row whose coordinate cell does not parse and name it, the way an old-format row is named; the judgment it needs is whether that counts as BROKEN or as a fourth state, since a row nobody can resolve is not a claim that drifted | the repository owner |
| Should `chain_check.py --worktree` read routing declarations from the WORKING TREE, so `round_record.py`'s own chain-check reports *declared* in local mode instead of *examined nothing*? Work item `1788817289-local-mode-from-first-setup-to-the-gate` took the notice only (#225, Q3 of its `questions.md`), and the argument is in that item's `spec.md` §*The sharp question*. It is not unsafe on the axis `read_record`'s docstring warns about — finding a declaration makes the check demand round records, so reading the working tree there is STRICTER than reading HEAD. What is against it: the local run would then assert a chain verdict CI can never reproduce, which is a second guarantee the tree has to keep true, and a declaration is committed before the first edit by rule, so an uncommitted one is not the transient state that flag was built for | the repository owner |
| Bring `agents/smith.md` and `agents/scribe.md` under `tests/test_docs_line_wrap.py`, together. `spec.md` of work item 1788433011 put this out of scope as a sweep at 148 and 160 columns. Both are now measured, with that test's own rules, at phase 4 of that item (2026-09-03, `4b85d80`): the scribe has **one** prose line over the limit (`:22`, 160 columns) and the smith **two** (`:22`, 148; `:95`, 109) — three lines in total, which is a rewrap and not a sweep. The size argument is therefore spent, and what is left is the one that decides it: adding a path to `COVERED` changes what a test guards, which `CONTRIBUTING.md` asks a separate argument for, and covering one definition and not the other reads as an oversight. So the two go in one change, with that argument | the repository owner |
| **Writing a `survivors.md` row silences its survivor a SECOND way, and that way does not rot.** An exemption row quotes the standing text, so once the commit adding the row is inside the range, `corrected` reads that quote as wording the range ADDED and `wanted` subtracts its n-grams from what is looked for at all. Executed during round 1's fix pass of #297: over `7355201..a18754c` the check reported **eleven** places before the file existed, and **one** afterwards with no `--exempt` flag passed — ten survivors went quiet through the diff rather than through the exemption. What that costs is the property the escape is built on: the quote is the anchor so an exemption *degrades to reported again* when the standing text changes, and this path has no anchor to degrade — it silences whatever the row's words match, whether or not the row still holds. The candidate fix is to leave `seal/specs/*/survivors.md` out of the ADDED side of `corrected`, the way `rounds/` is left out of the corpus by construction: an exemption file is a judgment about the range, not prose the range wrote. **What needs a person is whether that exclusion is right** — a branch may legitimately edit prose in the same commit as its exemption file, and by-construction exclusions are what this check's own docstring argues for over lists. A fix pass may not add mechanism, which is why this is a row and not a commit (`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it*). **The eleven-to-one figure is from a range no gate runs, and round 2 corrected it**: over `origin/release/v0.9.5...090bbd0`, which IS what CI runs, the check reports 41 removed sentences and **no** survivors — with the four exemption files, without `--exempt` at all, and with `survivors.md` deleted from HEAD so it cannot be on the added side. So the mechanism is real and its reach at the gate is unmeasured, which is what a person has to weigh the exclusion against | the repository owner |
| **Five more scripts die below the supported floor with a bare traceback, the way `round_record.py` did before #226.** Enumerated by construction in `seal/specs/1788789985-round-record-dies-on-python-3-9/spec.md` §*The class, enumerated by construction*, which is where the file and line of each one lives, and re-enumerated on every suite run by `tests/test_a_script_says_which_interpreter_it_needs.py#test_no_shipped_script_needs_more_than_the_floor_without_saying_so`, so this row is a decision waiting rather than a fact that can go stale. **No coordinate is repeated in this row, on purpose**: the rule above sends anything tied to one to a `# RIDER:` at the line, and `tests/test_a_rider_reaches_its_file.py#test_no_schedulable_row_carries_a_coordinate` enforces it — the first version of this row carried five and turned that case red, which is the rule catching exactly what it was written for. `gather_changelog.py` and `fold_ledger.py` use `datetime.UTC` (3.11) and are named after a literal `python3 ` in `CONTRIBUTING.md` and `docs/release-checklist.md` §3, so a release run on a 3.9 or 3.10 `python3` fails at the moment it writes the dated heading. `session_cost.py` is the same construct spelled behind `import datetime as dt`, and it ends the run report `docs/review-handoff-protocol.md` §*After a run* points at. `seal.py` is the same construct and **was not touched because another work item in this release holds that file**. `root-migrate.py` uses `zip(..., strict=True)` and is reached through `hooks/hooks.json`'s session-start dispatch, so it fails while migrating a 0.3.x layout, in a hook, where nobody is reading. The fix is fifteen lines each, copied from `skills/code-review/scripts/round_record.py#below_floor`, which was written to be copied and says so. **What needs a person is not the fix, it is whether these belong in the tracker instead**: this file's own opening says a repository with a tracker should normally hold none of these, and the handoff for #226 asked for them here | the repository owner |
| **The refusal for an unparseable `Broad gate` cell tells a person what to write, and no case pins that half.** `chain_check.py`'s new arm refuses a cell above the cutoff that carries no SHA-shaped word, and the message's second half — what a person should put there instead — is asserted nowhere. Its sibling in the same commit, the divergent-SHA notice, IS pinned on the phrase `different line of history`. A refusal is read by whoever is stopped by it, so the half that says what to do is the half that has to survive a reword. Found by round 2 of `1788912166-red-for-following-the-documents-green-for-ignoring-one`; a case is mechanism a fix pass may not add after a run has ended. **The rider clause this row first carried was wrong and is corrected here by whoever wrote it**: it named `session_cost.py`'s anchors — `#report_spawns` and `#analyse` — for a coordinate that is in `chain_check.py`, carried over from #145's round 3 without re-checking which file was being talked about, and the count was short too (four rows anchor at `#analyse` across the two ledger files, not two). Whether a `# RIDER:` at `chain_check.py`'s refusal branch drifts anything is unmeasured, and it is one `evidence-check` run to find out | the repository owner |

## Riders waiting on a file another branch holds

| Target | Who must answer |
|---|---|
