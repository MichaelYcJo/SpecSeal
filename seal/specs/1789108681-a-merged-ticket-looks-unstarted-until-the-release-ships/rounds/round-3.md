# 1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships — review round 3

| Field | Value |
|---|---|
| Target SHA | 64d830b |
| Ran by | specseal:warden on Opus 5 |
| PR | #360 |
| Broad gate | f689a1b against origin/release/v0.11.1 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

# round 3 — the reopening's verifying round, and the last record of this run

| | |
|---|---|
| Target | the **diff of round 2's fixes**, `99005ba..64d830b` — not the branch |
| Review at | `64d830b` |
| Base of the branch | `origin/release/v0.11.1` = `f9c6907` |
| Draft pull request | #360 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-2.md`, closed — 3 fixed, 0 answered, 0 deferred |

## This is the last record, and that is decided before you start

Round 1 met the floor. Round 2 was its verifying round and reopened the run
on finding 16, which is the **one** reopening the chain allows. So this record
ends the run whatever it finds: if it opens something, that finding becomes an
issue with the verdict `deferred #N`, this record's `Fixes checked by` reads
`no fixes to check`, and the pull request is labelled `chain: capped`.

Nothing about that changes what you should report. Report what you find.

## The job

**The answers, not new findings** — for each of round 2's three verdicts, is
it actually closed. `rounds/round-2.md` holds the verdict table,
`rounds/round-3-fixes.md` holds what the fix pass says it did, and
`rounds/round-2-report.md` holds the reasoning the verdicts came from.

**There is no finding surface this time, and the record says so.**
`round-2.md`'s `New units` row reads `none`, derived from the fix diff by
`round_record.py close` rather than typed. The pass added no unit on purpose:
findings 16 and 17 both sit inside round 1's fix surface, where a case to pin
them would be depth 2 and is refused. So every surface in this diff is a
verification surface, and the round is three prose lines across three files.

## The three verdicts, and the half of each that is a decision

The diff is small; the judgments inside it are not. Each fix took part of a
paste-ready text and declined part, and the decline is the half worth checking
rather than inheriting.

- **Finding 16** — `.github/scripts/release_completeness_check.py:48-52`. The
  `Environment:` line now names `HEAD_SHA` with its default and one clause
  saying its absence is the silent one. **The pass declined to restate the
  merge-ref argument in full**, on the grounds that it already stands twice in
  the file — `merge_base`'s docstring and the comment above `point` — and a
  third copy would add a third place to keep in step, which is the failure
  mode finding 16 is itself an instance of. Judge whether the pointer it left
  instead actually reaches that argument, and whether the enumeration is now
  exhaustive against `grep -n environ` over the file.
- **Finding 17** — `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488`.
  *all four* → *every entry*, taken over the arithmetic correction *all five*,
  on the grounds that the tuple can gain a sixth member and *five* would rot
  exactly as *four* did. Judge both halves.
- **Finding 5** — `overview.md:31`, *Eight* → *Nine*. The pass reports it swept
  the class rather than the coordinate, which is what produced the finding in
  the first place: four hits outside `rounds/`, two already correct and two
  counting a different subject, and the `rounds/` records deliberately left
  saying *eight* because they are past-state documents true at their own
  target SHA. **That sweep is the claim worth re-deriving**, since a sweep
  reported and not done reads identically to one done.

## Executed by the orchestrating session at `64d830b`

Exit codes read directly, no pipe. Re-derive rather than inherit:

- Eight modules, one per call — `test_a_release_cannot_ship_an_untrue_milestone`
  29 · `test_ci_gives_the_checks_what_they_need` 2 ·
  `test_a_merged_ticket_says_so_on_the_tracker` 23 · `test_docs_line_wrap` 23 ·
  `test_release_hygiene` 32 · `test_one_word_one_meaning` 13 ·
  `test_no_real_identifiers` 2 · `test_a_record_states_what_the_tree_has` 58 →
  **182 passed, exit 0 each**.
- `uvx ruff check` and `uvx ruff format --check` on the two changed Python
  files → **exit 0** each.
- The diff read line by line: three files, nine lines.
- `git status --porcelain` → empty.

## The form the commands take in this checkout

- **`ruff` is not installed here.** `uvx ruff check` / `uvx ruff format --check`.
- **Read exit codes directly, never through a pipe.** `cmd > /tmp/x 2>&1; echo $?`.
  This shell is `zsh`; `${PIPESTATUS[0]}` is not it.
- `bin/test`, narrow, one module at a time.
- `evidence_check.py .` **unscoped for reading** — no `--ledger`.

## Still unverified, and they stay that way

Round 1's finding 8 — whether `issues: read` reaches a pull request body — is
deferred to `overview.md` §*Not verified* with the repository owner as
answerer, at the 0.11.1 release pull request. Do not settle it by writing to
the tracker.

**The broad gate is the `sealer`'s. Do not run it.** No `bin/broad-gate`, no
whole-suite run, no repository-wide `ruff`. It comes due when this record
closes.

## Not a finding

The gate run against the live tracker refuses naming **#359 and #361**. Both
are in `release: 0.11.1` deliberately and ship in this release, so the
milestone is true as planned and the refusal is the gate seeing work that is
not merged yet. Do not report it and do not write the pair into anything.

## The two lines the run ends on

Answer each in a line of its own:

- `Needs a fix: no`, or `yes` and what does. A 🟡 answered with grounds is `no`.
  A finding located under `seal/specs/` is a correction and does not count.
- `Loses a record or crashes: no`, or `yes` and what does.

## Where the report goes

Write your report to `rounds/round-3-report.md` in the working tree,
uncommitted. Do not commit it and do not touch the tracker. The orchestrating
session verifies your highest-severity coordinates itself before any of it is
recorded.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 16 | Round 2's finding 16 — is the `Environment:` enumeration exhaustive, and does the pointer reach the argument it declined to restate | `.github/scripts/release_completeness_check.py:48-52` | answered | Executed and read. `grep -n environ` returns four reads — `HEAD_BRANCH:254`, `REPO:263`, `BASE:264`, `HEAD_SHA:269` — and the line names all four with `HEAD_SHA`'s default. The pointer reaches `merge_base`'s docstring at `:82-101`, which carries the merge-ref argument in full, so the decline to restate it holds. The class the decline named also holds: the sibling's five reads are documented across its line at `:48` and its `DRY_RUN` paragraph at `:44-46`. The replacement prose carries a new defect, reported as finding 18 rather than as this one reopening |
| 17 | Round 2's finding 17 — does the docstring now describe its own loop, and does the decline of *all five* hold | `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488` vs `:493` | answered | Read. The loop iterates `("GH_TOKEN", "HEAD_BRANCH", "HEAD_SHA", "BASE", "REPO")` and the step's `env:` block at `.github/workflows/hygiene.yml:270-281` holds exactly those five keys, so *every entry* is true of the loop. The decline of *all five* holds on its stated ground — the block can gain a sixth, and *five* would rot as *four* did |
| 5 | Round 2's finding 5 — is the second module count corrected, and was the class swept rather than the coordinate | `overview.md:31` | answered | Executed, per module in the clone at the reviewed SHA: `test_docs_line_wrap` 23 · `test_one_word_one_meaning` 13 · `test_release_hygiene` 32 · `test_no_real_identifiers` 2 · `test_the_rules_have_one_owner` 45 · `test_a_question_says_who_can_answer_it` 6 = **121**; `test_a_merged_ticket_says_so_on_the_tracker` 23 · `test_a_release_cannot_ship_an_untrue_milestone` 29 · `test_ci_gives_the_checks_what_they_need` 2 = **54**. Nine modules, 175 cases, exit 0 each — the figure `overview.md:9` claims. The sweep re-derived rather than inherited: the pass's own command over the work item excluding `rounds/` returns the hits it names and each is judged correctly, including `phases/phase-5.md:31` counting ledger rows. The `rounds/` records keep their *eight* correctly. Only the tally beside the sweep is off, reported as finding 20 |
| 18 | 🟡 The module docstring states `HEAD_SHA` is the one input whose absence is silent rather than loud; losing `HEAD_BRANCH` also exits 0 and prints the hotfix skip's own line | `.github/scripts/release_completeness_check.py:50-51`, and the same superlative at `tests/test_a_release_cannot_ship_an_untrue_milestone.py:494-496` | deferred #362 | #362 |
| 19 | ⬜ The `Environment:` line names four inputs; the case that pins the step calls five of them read by this script. `GH_TOKEN` is the fifth | `.github/scripts/release_completeness_check.py:48-52` vs `tests/test_a_release_cannot_ship_an_untrue_milestone.py:493-497` | deferred #362 | #362 |
| 20 | ⬜ The sweep's grounds say the command returns four hits; it returns five | `rounds/round-3-fixes.md:20`, copied into `rounds/round-2.md:113` | answered | **Corrected in this record's own closing commit, which is what a finding located in a record gets** — `skills/code-review/orchestration.md` §*The run ends with a verifying round*: a finding under `seal/specs/` owes no fix pass and no reader, and `Needs a fix` does not count it. Not `fixed`, because no fix pass wrote it and none may be commissioned here; marking it `fixed` would also leave `Fixes checked by` at `nobody`, which on this run's last record fails the pull request beside a ticked `Pass`. The grounds cell of finding 5 in `rounds/round-3-fixes.md` said the sweep's command returns *four* hits and then named a fifth in its own next sentence; re-run by this session, it returns **five** — `overview.md:9`, `overview.md:31`, `questions.md:17`, `plan.md:81` and `phases/phase-5.md:31`. Both copies are corrected, in that file and in the cell `close` had copied it into at `rounds/round-2.md`. The sweep itself was complete and every judgment in it was right; only the tally beside it was wrong |

## Paste-ready fixes

```python
Environment: `REPO`, `HEAD_BRANCH` (`github.head_ref`), `BASE` for the ref
the range is measured from (default `origin/main`), and `HEAD_SHA` for the
commit it is measured TO (default `HEAD`). `GH_TOKEN` reaches `gh` rather
than this module and is loud when it is missing. Of the four above, only
`REPO` is loud: absent, it is a `KeyError` and exit 1. `HEAD_SHA` absent
collapses the range and prints nothing about it, which is what `merge_base`
below reads out. `HEAD_BRANCH` absent is the second quiet one — the version
comes out `None`, the run takes the hotfix skip, and its log line is the
hotfix skip's own, so a green step means "judged nothing" and not "judged
and passed".
"""
```
```python
        assert f"{name}:" in env, (
            f"the gate step no longer passes {name}. Every one of these is "
            "read by `release_completeness_check.py`, `GH_TOKEN` through "
            "`gh`; HEAD_SHA and HEAD_BRANCH are the two whose absence still "
            "exits 0"
        )
```
```markdown
| 5 | fixed | `64d830b`, `overview.md:31`, *Eight modules* → *Nine*. Both figures re-derived rather than inherited, and the module list at `:9` names the same nine. **Class swept rather than the coordinate**, which is what produced this finding: the sweep command over the work item excluding `rounds/` returns five hits — `overview.md:9` already correct, `overview.md:31` this one, `questions.md:17` and `plan.md:81` both counting open milestone issues, a different subject and both true, and `phases/phase-5.md:31`'s *Eight rows*, which counts ledger rows and agrees with `overview.md:9`. The `rounds/` records keep their *eight*: they are past-state documents read at their own target SHA, and `round-1-report.md:17` saying *165 across the eight modules the paragraph names* is a true statement about what that paragraph said |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` per module in the clone at `64d830b`, nine modules one per call | **175 passed, exit 0 each** — 23 · 13 · 32 · 2 · 45 · 6 = 121 over the six document modules, 23 · 29 · 2 = 54 over the three the build touched |
| The script run with one input removed at a time, exit codes read directly with no pipe, `REPO` given a neutral value | **`REPO` absent → exit 1** with `KeyError: 'REPO'`; **`HEAD_SHA` absent → exit 0**, nothing printed about it; **`HEAD_BRANCH` absent → exit 0**, prints the hotfix skip's own line; **`HEAD_BRANCH` empty → exit 0**, same line. This is finding 18's measurement |
| `grep -n environ` over `.github/scripts/release_completeness_check.py` | four reads — `HEAD_BRANCH:254`, `REPO:263`, `BASE:264`, `HEAD_SHA:269`. The `Environment:` line names all four |
| The count sweep command over the work item excluding `rounds/`, re-derived rather than inherited | **five hits**, not the four the grounds claim: `overview.md:9`, `overview.md:31`, `questions.md:17`, `plan.md:81`, `phases/phase-5.md:31`. Each is judged correctly in the grounds; only the tally is off |
| `bin/evidence-check --strict .`, unscoped, in the clone | **exit 0** — 1137 ok · 0 drifted · 0 broken. The three ledger rows anchored into the changed script resolve |
| `bin/survivor-check --range 99005ba..64d830b` | **exit 0** — 880 files at `64d830b` against 3 removed sentences, no removed wording still standing |
| `uvx ruff check` and `uvx ruff format --check` on the two changed Python files | **exit 0** each; 2 files already formatted |
| `git status --porcelain` in the clone before deleting it, and in the working tree | empty both times. The clone is deleted and nothing else was left behind |
| The broad gate — the full suite, the repository-wide `ruff check .` and `ruff format --check .` | **not yet.** It is the sealer's, `agent-contract` §2 assigns it there, and this round ran nothing broad. This report leaves nothing needing a fix, so what comes due is the `sealer`'s spawn |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/release_completeness_check.py:100` | round 1's 1 — fixed |
| round-1 | `.github/scripts/release_completeness_check.py:71-84`, `:236`; `.github/workflows/hygiene.yml:269-280` | round 1's 2 — fixed |
| round-1 | `docs/issues-and-milestones.md:127-128` vs `docs/release-checklist.md:14,18,40,50` | round 1's 3 — fixed |
| round-1 | `overview.md` §*Not verified*; `questions.md` Q3 | round 1's 4 — fixed |
| round-1 | `overview.md:9` | round 1's 5 — fixed |
| round-1 | `.github/workflows/hygiene.yml:269-280` | round 1's 6 — fixed |
| round-1 | `.github/scripts/release_completeness_check.py:12-14` | round 1's 7 — answered |
| round-1 | `.github/workflows/hygiene.yml:20-22` | round 1's 8 — deferred |
| round-1 | `.github/scripts/release_completeness_check.py#judge` | round 1's 9 — answered |
| round-1 | `.github/workflows/hygiene.yml:277` | round 1's 10 — answered |
| round-1 | `.github/scripts/release_completeness_check.py:212-219` | round 1's 11 — answered |
| round-1 | `.github/scripts/label_merged_on_release_branch.py:77` | round 1's 12 — answered |
| round-1 | `docs/` | round 1's 13 — answered |
| round-1 | prompt vs `docs/branch-and-release.md` | round 1's 14 — withdrawn |
| round-1 | `seal/specs/*/survivors.md` | round 1's 15 — answered |
| round-2 | `.github/scripts/release_completeness_check.py:116-141` | round 2's 1 — answered |
| round-2 | `.github/scripts/release_completeness_check.py:84-102`, `:259-282`; `.github/workflows/hygiene.yml:270-283` | round 2's 2 — answered |
| round-2 | `docs/issues-and-milestones.md:127-129` | round 2's 3 — answered |
| round-2 | `overview.md:9` fixed; `overview.md:31` not | round 2's 5 — fixed |
| round-2 | `.github/workflows/hygiene.yml:270-283` | round 2's 6 — answered |
| round-2 | `.github/scripts/release_completeness_check.py:15-22` | round 2's 7 — answered |
| round-2 | `.github/workflows/hygiene.yml:283-288` | round 2's 10 — answered |
| round-2 | `.github/scripts/release_completeness_check.py:250-257` | round 2's 11 — answered |
| round-2 | `.github/scripts/label_merged_on_release_branch.py` | round 2's 12 — answered |
| round-2 | `.github/scripts/release_completeness_check.py:48-49` | round 2's 16 — fixed |
| round-2 | `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488` vs `:492` | round 2's 17 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 18 — the docstring's one-silent-input superlative, and the same superlative in the case that pins the block | a new issue, `deferred #N` — the run is capped, so it is a candidate for one rather than a fix to commission | the orchestrating session opens it; the work item that takes it answers it |
| Finding 19 — `GH_TOKEN` absent from the `Environment:` line while the case counts it as an input | the same issue as finding 18 — one sentence, two counts of the same five inputs | as above |
| Whether `issues: read` reaches a pull request body through the issues endpoint | `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md` §*Not verified* — carried from round 2, not reopened and not settled here | the repository owner, at the 0.11.1 release pull request |
