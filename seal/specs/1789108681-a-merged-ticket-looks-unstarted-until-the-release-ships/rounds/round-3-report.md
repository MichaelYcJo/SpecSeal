# round 3 — the reopening's verifying round

Target: the diff of round 2's fixes, `99005ba..64d830b`, read at `64d830b`.
Three files, nine lines. Reviewed in a `git clone --no-local` of this
repository at that SHA, in the session scratchpad, deleted before this report
was written.

Round 2's three verdicts are all closed. The prose that replaced finding 16's
defect carries a new one, and it is the only thing this round opened that is
not paperwork.

## What round 2's three fixes actually did

**Finding 16 is closed, and both halves of its decline hold.**

The enumeration is exhaustive. `grep -n environ` over
`.github/scripts/release_completeness_check.py` returns four reads —
`HEAD_BRANCH:254`, `REPO:263`, `BASE:264`, `HEAD_SHA:269` — and the
`Environment:` line at `:48-52` now names all four, `HEAD_SHA` with its
default. Carried from round 2 rather than re-derived: that a reader takes this
line as exhaustive, because the sibling script carries the same kind of line.

The pointer reaches the argument. The new clause says *`merge_base` below
carries what falling back to `HEAD` costs on a `pull_request` event*, and
`merge_base`'s docstring at `:82-101` is where that argument stands: the merge
ref, `HEAD` already containing `origin/main`, `git merge-base` answering the
base tip, and the collapse to the spelling `questions.md` Q8 rejected. The
decline to restate it is right on its own grounds — a third copy is the
failure mode the finding is an instance of.

The class the decline named also holds. Two scripts in `.github/scripts/`
carry an `Environment:` line, and the sibling's five `os.environ` reads are
documented across two places: four on the line at `:48` and `DRY_RUN` in its
own paragraph at `:44-46`. Round 2's phrase *lists all four of its own* is
loose — the sibling reads five — but the same grounds name the fifth and its
home, so the sweep covered it.

**Finding 17 is closed, and the decline of the arithmetic correction holds.**

The docstring at `:488` now says *every entry*. The loop at `:493` iterates
`("GH_TOKEN", "HEAD_BRANCH", "HEAD_SHA", "BASE", "REPO")`, and the step's
`env:` block at `.github/workflows/hygiene.yml:270-281` holds exactly those
five keys and no sixth. So *every entry* is true of the loop today and stays
true when the block grows, which is the ground the pass gave for declining
*all five*.

**Finding 5 is closed, and the sweep was done rather than reported.**

`overview.md:31` reads *Nine modules were run narrowly instead*, and nine is
the right figure: executed, 121 cases over the six document modules and 54
over the three the build touched, exit 0 each, 175 in total, which is exactly
what `overview.md:9` claims after round 1's fixes. Re-derived per module
rather than inherited.

The class sweep is real. Running the pass's own command over the work item
excluding `rounds/` returns the hits it names, each judged correctly:
`overview.md:9` already right, `overview.md:31` the fix, `questions.md:17` and
`plan.md:81` counting open milestone issues rather than modules, and
`phases/phase-5.md:31` counting ledger rows in agreement with `overview.md:9`.
The `rounds/` records keep their *eight*, which is right — they are past-state
documents true at their own target SHA.

## What this round opened

### 🟡 Finding 18 — the docstring says one input fails silently; two do

`.github/scripts/release_completeness_check.py:50-51` states that `HEAD_SHA`
*is the one entry whose absence is silent rather than loud*. That partitions
the four inputs into one silent and three loud, and the partition does not
hold: losing `HEAD_BRANCH` also leaves the step green.

Measured, by running the script with one input removed at a time:

| Input removed | Exit | What the run does |
|---|---|---|
| `REPO` | 1 | `KeyError: 'REPO'` — loud, as the docstring says |
| `HEAD_SHA` | 0 | the range collapses, nothing printed about it |
| `HEAD_BRANCH` | 0 | prints `'' is not a release/vX.Y.Z branch — nothing to judge`, judges nothing, step green |

The `HEAD_BRANCH` row is why this matters. `version_of("")` returns `None`, so
the script takes the hotfix skip — and the line it prints is the hotfix skip's
own line. In a green step's log that reads as the designed behaviour, not as a
fault. A reader who deletes `HEAD_BRANCH:` from the step's `env:` block has
been told by this docstring that only one deletion is the quiet kind.

There is a reading under which the sentence is true — `HEAD_SHA` is the only
input whose absence produces no output naming it — and that reading is round
2's own wording, which the fix pass took as given. So this is answerable with
grounds rather than a defect to commission a fix for. What it is not is a
correct account of which deletions leave a green step claiming to have judged
a release.

**The class is two coordinates, not one.** The same superlative stands in the
case that pins the block, at
`tests/test_a_release_cannot_ship_an_untrue_milestone.py:494-496` — *HEAD_SHA's
absence is the only one that is silent*. That line is outside this diff, in
round 1's fix surface, but it is the same claim and `agent-contract` §12 puts
it in the same fix.

Behaviour is unaffected and both deletions are pinned: the case at `:476`
covers all five entries, and `HEAD_BRANCH` has its own case at `:470`.

### ⬜ Finding 19 — the `Environment:` line still omits `GH_TOKEN`

`.github/scripts/release_completeness_check.py:48-52`. The step passes five
variables and the case at `:476` calls all five *read by
`release_completeness_check.py`*; the `Environment:` line names four. The one
missing is `GH_TOKEN`, which the script reads through `gh` rather than through
`os.environ`.

This is not finding 16 returning. The line's frame is `os.environ` reads, the
sibling script draws the boundary the same way, and losing `GH_TOKEN` is loud
— `gh` fails and the step goes red. Left as a correction because the case and
the docstring describe the same five inputs with two different counts, and a
reader comparing them has no way to tell which boundary is meant.

### ⬜ Finding 20 — the sweep's tally says four hits; the command returns five

`rounds/round-3-fixes.md:20`, and the same sentence copied into
`rounds/round-2.md:113`. The grounds state that the sweep command over the
work item excluding `rounds/` *returns four hits* and then discuss five
coordinates, `phases/phase-5.md:31` among them. The command as written returns
five. The sweep itself is complete — this is the tally beside it, not the work.
Under `seal/specs/`, so a correction to the paperwork.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 16 | Round 2's finding 16 — is the `Environment:` enumeration exhaustive, and does the pointer reach the argument it declined to restate | `.github/scripts/release_completeness_check.py:48-52` | answered | Executed and read. `grep -n environ` returns four reads — `HEAD_BRANCH:254`, `REPO:263`, `BASE:264`, `HEAD_SHA:269` — and the line names all four with `HEAD_SHA`'s default. The pointer reaches `merge_base`'s docstring at `:82-101`, which carries the merge-ref argument in full, so the decline to restate it holds. The class the decline named also holds: the sibling's five reads are documented across its line at `:48` and its `DRY_RUN` paragraph at `:44-46`. The replacement prose carries a new defect, reported as finding 18 rather than as this one reopening |
| 17 | Round 2's finding 17 — does the docstring now describe its own loop, and does the decline of *all five* hold | `tests/test_a_release_cannot_ship_an_untrue_milestone.py:488` vs `:493` | answered | Read. The loop iterates `("GH_TOKEN", "HEAD_BRANCH", "HEAD_SHA", "BASE", "REPO")` and the step's `env:` block at `.github/workflows/hygiene.yml:270-281` holds exactly those five keys, so *every entry* is true of the loop. The decline of *all five* holds on its stated ground — the block can gain a sixth, and *five* would rot as *four* did |
| 5 | Round 2's finding 5 — is the second module count corrected, and was the class swept rather than the coordinate | `overview.md:31` | answered | Executed, per module in the clone at the reviewed SHA: `test_docs_line_wrap` 23 · `test_one_word_one_meaning` 13 · `test_release_hygiene` 32 · `test_no_real_identifiers` 2 · `test_the_rules_have_one_owner` 45 · `test_a_question_says_who_can_answer_it` 6 = **121**; `test_a_merged_ticket_says_so_on_the_tracker` 23 · `test_a_release_cannot_ship_an_untrue_milestone` 29 · `test_ci_gives_the_checks_what_they_need` 2 = **54**. Nine modules, 175 cases, exit 0 each — the figure `overview.md:9` claims. The sweep re-derived rather than inherited: the pass's own command over the work item excluding `rounds/` returns the hits it names and each is judged correctly, including `phases/phase-5.md:31` counting ledger rows. The `rounds/` records keep their *eight* correctly. Only the tally beside the sweep is off, reported as finding 20 |
| 18 | 🟡 The module docstring states `HEAD_SHA` is the one input whose absence is silent rather than loud; losing `HEAD_BRANCH` also exits 0 and prints the hotfix skip's own line | `.github/scripts/release_completeness_check.py:50-51`, and the same superlative at `tests/test_a_release_cannot_ship_an_untrue_milestone.py:494-496` | open | Executed, one input removed at a time: `REPO` absent → exit 1, `KeyError: 'REPO'`; `HEAD_SHA` absent → exit 0, nothing printed about it; `HEAD_BRANCH` absent or empty → exit 0, prints `'' is not a release/vX.Y.Z branch — nothing to judge` and judges nothing. `version_of("")` returns `None`, so the run takes the hotfix skip and its log line is the hotfix skip's line, which in a green step reads as designed behaviour. Answerable with grounds — the superlative is round 2's own wording and is true of *produces no output naming it* — and behaviour is unaffected, both deletions being pinned by the cases at `:476` and `:470`. The class is two coordinates, `agent-contract` §12 |
| 19 | ⬜ The `Environment:` line names four inputs; the case that pins the step calls five of them read by this script. `GH_TOKEN` is the fifth | `.github/scripts/release_completeness_check.py:48-52` vs `tests/test_a_release_cannot_ship_an_untrue_milestone.py:493-497` | open | Read. `GH_TOKEN` reaches the script through `gh` rather than `os.environ`, the sibling script draws the same boundary, and its absence is loud — `gh` fails and the step goes red. Not finding 16 returning; the cost is that two documents count the same inputs differently with nothing saying which boundary each means |
| 20 | ⬜ The sweep's grounds say the command returns four hits; it returns five | `rounds/round-3-fixes.md:20`, copied into `rounds/round-2.md:113` | open | Executed: the pass's own command over the work item excluding `rounds/` returns five, `phases/phase-5.md:31` among them — a coordinate the same grounds go on to discuss. The sweep is complete; the tally beside it is not. Under `seal/specs/`, so a correction |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 18 — the docstring's one-silent-input superlative, and the same superlative in the case that pins the block | a new issue, `deferred #N` — the run is capped, so it is a candidate for one rather than a fix to commission | the orchestrating session opens it; the work item that takes it answers it |
| Finding 19 — `GH_TOKEN` absent from the `Environment:` line while the case counts it as an input | the same issue as finding 18 — one sentence, two counts of the same five inputs | as above |
| Whether `issues: read` reaches a pull request body through the issues endpoint | `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md` §*Not verified* — carried from round 2, not reopened and not settled here | the repository owner, at the 0.11.1 release pull request |

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

Needs a fix: no

Loses a record or crashes: no

## Proof block

Opened and read at `64d830b`, in the clone except where the path is a record:

- `.github/scripts/release_completeness_check.py` — `:1-60`, `:80-110`,
  `:245-290`
- `.github/scripts/label_merged_on_release_branch.py` — `:38-50`, and its
  `os.environ` reads
- `.github/scripts/close_issues_on_release.py` — its `os.environ` reads only
- `.github/workflows/hygiene.yml` — `:262-292`
- `tests/test_a_release_cannot_ship_an_untrue_milestone.py` — `:470-515`
- `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/overview.md`
  — `:1-35`
- `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/rounds/round-3-asked.md`
- `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/rounds/round-2.md`
- `seal/specs/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships/rounds/round-3-fixes.md`
- `git diff 99005ba..64d830b` in full, and `git log --oneline f9c6907..6612085`

Not opened: `spec.md`, `plan.md`, `questions.md`, `handoff.md`, the phase
records and `round-1.md` beyond the lines the count sweep returned. Round 1
and round 2 closed their own surfaces and this round's target is the fix diff.
