# Implementation Plan: nothing reads a record against the tree

<!-- seal/specs/1789621028-nothing-reads-a-record-against-the-tree/plan.md — HOW, in phases.
This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-17 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

A round record is written once and the tree keeps moving. `spec.md` settles
what #344 left open: **the authoritative statement of a fix range moves out of
the fixes file's prose and into the record, written by the generator that
already resolves it, and read back at the pull request by the one checker
allowed to ask git.** #426 and #427 are then fixed into a tree that has a
reader in it, rather than at their own coordinates.

Six phases, each a vertical slice that ends runnable. The order is cheapest
and most independent first, so the run has a green boundary before it reaches
the phase that can grow.

## Technical context

Everything below was opened at its coordinate on 2026-09-17. Nothing in this
section came from a ticket body without being checked.

**#426.** `tests/test_chain_hooks_hardening.py`, function
`test_the_questions_are_collected_before_the_work_not_during_it` at `:1026`.
The sweep appends `(relative, len(body))` at `:1133`; the floor is
`assert all(size > 1000 for _, size in read)` at `:1150`, under a comment at
`:1147` claiming it pins that each file arrived whole. `agents/*.md` is five
files and the smallest, `agents/scribe.md`, is 3764 bytes. The measured fix is
in `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-3-report.md:273`
and `:283` — byte length on both sides, so the comparison survives the emoji
and em-dashes these files carry.

**#427.** `skills/code-review/scripts/round_record.py`, `close`'s row loop at
`:3752-3772`. `old` is the reviewer's grounds; the three branches build
`grounds` for `fixed`, `answered` and `deferred`; the write at `:3771` is
`grounds + (f"; {old}" if old else "")`. The refusal at `:3692` that looks like
it would catch a re-close reads only the **Verdict** cell, so a record whose
Verdicts were restored to `open` and whose Grounds were not passes straight
through it. The proposed guard is at
`.../1789540097-…/rounds/round-3-report.md:292` and the round says it is
**unmeasured**.

**#344.** `parse_range` at `round_record.py:2737` resolves both ends through
`chain.resolves_to` and refuses only an unparseable or unresolvable ref — so
`HEAD` is accepted today. `close` already resolves each `fixed` commit and
refuses one outside the range (`:3707-3717`), which is the shape the new
refusal copies. The record's field table is `templates/sdd-round.md:33-45`;
the field precedent is `chain_check.py:500-501` (`CONTRACT`, `NEW_UNITS`) with
`docs/review-chain-spec.md:854` §*The fix surface* documenting it and
`SURFACE_FROM` at `chain_check.py:520` governing it. Nine cutoffs of that shape
already exist, `STRICT_FROM` at `:480` holding the reasoning for all of them.

**The five places, re-located.** Two of #344's bullets do not resolve as
written, which is the ticket demonstrating its own class:

| #344 says | The tree at 2026-09-17 |
|---|---|
| `rounds/round-3-fixes.md:3` says `ce0f9fe..HEAD` | It says `` `ce0f9fe..ce0f9fe`, empty `` — and only one commit, `393da643`, has ever touched the file, so it has never said otherwise. The **moving** range is one file over, at `rounds/round-2-fixes.md:3`: `` `de7d693..HEAD`, four commits at the time of writing `` |
| *round 2's table pinned its range for exactly this reason* | Round **1**'s did — `` `e972b5f..b8aa637`, seven commits ``. Round 2's is the one that moves |
| `rounds/round-3.md:28` understates a hand-edit | `:28` is finding 3's verdict row. The hand-edit disclosure is inside the single-paragraph `## What this phase was asked` at `:19` — *`round-1.md`'s cell repaired by hand from the report with an HTML comment beside it* |
| `rounds/round-2.md:32` points at `tests/test_broad_gate_rule.py:281` | Holds. `:279-280` are the module constants `COUNT_WORD` and `ASSIGNS_THE_GATE`; the failure message the row names begins at `:319` |
| `survivors.md:5` describes sixteen places; `overview.md:6` records 15 exempt | Both lines say what the ticket says. Whether the re-run still reports three is Q3 — the range `origin/release/v0.10.0...HEAD` no longer means what it meant |
| A verdict attributes a fix to a commit carrying half of it | **No coordinate given.** Q2 locates it before anything is written |

**The corpus, measured.** 223 committed round records with a Verdicts table ·
39 fix-table files, 11 stating a range in their first eight lines in eleven
different spellings, two of them naming `HEAD` · **zero** surviving doubled
close-prefixes across every `seal/specs/*/rounds/*.md`. The two lines that
match a crude search for one are prose in
`1789445605-…/rounds/round-2.md:53` describing #414's rendering, not an
instance.

**What breaks in six months.** The new record field is the thing to watch. A
field a generator writes and a checker reads is only as good as its cutoff: if
the cutoff is set too low, every shipped record fails the next pull request,
and if the arm is written to fail on absence rather than to print below the
cutoff, the same thing happens on the first work item that skips `close`. The
nine cutoffs already in `chain_check.py` are the pattern to copy exactly, and
the phase's own acceptance runs the checker over the 223 records in the tree.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Content anchors in a record's `Location` cell** — #344's first option | 223 records and ~90 work items re-anchored by people who did not write them; the round template prescribes `path:line` and `tests/test_a_record_states_what_the_tree_has.py:508` exists to stop the records arm reading that cell as a coordinate. A half-done migration leaves two conventions and a checker that trusts neither | **refused** — Q1 puts it to the owner as its own work item |
| **Widen `evidence_check`'s records arm** — #344's second option | That checker calls git for nothing, stated as a bar in its own test module: *No fixture here runs git, and no fixture here may*. A range is a claim about commits, so the arm would have to break the rule that makes the checker cheap | **refused** — the reader goes in `chain_check`, which already asks git |
| **Parse the fixes file's own `Range` header and refuse a moving end there** | Measured: 11 of 39 files, eleven spellings, no two alike. A parser over that is a guess that fails open on the 28 files with no header at all | **refused**, and the measurement is the grounds |
| **Refuse a moving `--range` and stop there, with no field** | It prevents the next instance and leaves the record with nothing a reader can check. The range would still live only in prose, in the twelfth spelling | **refused** — half the fix |
| **Write the field and skip the `--range` refusal** | `close` would faithfully record the range it was given, and `HEAD` resolves, so the field would pin a commit nobody meant. Pinning the wrong thing precisely is worse than not pinning it | **refused** — both halves or neither |
| **A rule in a document and no checker** | This is the state that produced all five places. #344's own bullets 1 and 4 point at lines that no longer hold what they name | **refused** |
| **Fix #426 and #427 at their coordinates, leave #344 open** | The milestone's own ordering argument: the reader that would have caught all five is never built | **refused** |
| **Raise #426's 1000-byte floor** | Moves the silent range instead of closing it, and the next reader cannot tell which number is right. The ticket refuses it by name | **refused** |
| **Correct the five places and build nothing** | #344 says none of the five ships a defect. A correction with no mechanism behind it buys one true record and the sixth place | **refused** — it is phase 5, not the work item |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#426 — the wholeness guard compares against each file's own size.** The sweep records the read's byte length and asserts it equals `os.path.getsize` of the file it read. No number in the assertion | `bin/test tests/test_chain_hooks_hardening.py` exit 0 untouched; exit 1 under each of `f.read(10)`, `f.read(2000)` and the loop's iterable replaced by `()`, each mutation applied alone and reverted. Plus one ordinary reword of a definition, exit 0, reverted | 73025104 |
| 2 | **#427 write half — `close` refuses to prefix a `Grounds` cell it has already prefixed.** Ahead of the write at `:3771`, for all three verdict words, naming the finding and saying to restore the Grounds cell as well. Nothing is written to disk when it fires | Three cases, one per verdict word, each seen red with the guard deleted; the #427 reproduction — a planted record whose Verdict cells alone were reopened — refused, and the byte-identical doubled row reproduced with the guard removed. Exits read directly, never through a pipe | 34730974 |
| 3 | **#427 read half — `chain_check` names a record whose `Grounds` cell carries its own close-prefix twice.** The arm that makes a standing duplicate visible instead of leaving it to two commits and a reader | A planted record at exit 1, naming the file, the finding number and the repeated text; this repository's 223 committed records at exit 0. The phase **discloses** that the tree holds zero instances today, so the green run is not reported as a catch | 558226a2 |
| 4 | **#344 — the range is pinned where it is written and read where it is used.** `close --range` refuses an end that is not a commit somebody can open; `close` writes the resolved range and its commit count into the record; `templates/sdd-round.md` and `docs/review-chain-spec.md` document the field; `chain_check` re-reads it behind a cutoff of the `STRICT_FROM` shape | `close --range <a>..HEAD` refused and no cell written; `close --range <a>..<b>` writing a count that equals `git rev-list --count <a>..<b>`; a planted record whose count disagrees with the tree at exit 1; the 223 records in the tree printing, not failing, below the cutoff. Probes driven from Python (§8), all deleted | 24e62b36 |
| 5 | **#344's five places — re-located against the tree, then corrected.** Q2 and Q3 are answered here. Where a bullet's premise does not hold today, the record says what was found instead rather than being edited to match the ticket. An HTML comment beside each correction says what it was read against and when | Read-only; nothing is executed except Q3's re-measurement. Each corrected line quoted in `overview.md` beside what it was read against, and the two bullets that do not resolve recorded as such | |
| 6 | **Close-out.** `seal/specs/<id>/changelog.md`, `seal/ledger/<id>.md` written in one pass from the rows kept since phase 1, `overview.md` closed, `seal/follow-up.md` left alone with the enumeration recorded | `bin/evidence-check .` exit 0 with the new rows resolving; the modules this branch touched, run narrowly. **The broad gate is not run here** — `agent-contract` §2 leaves the full suite, the repository-wide lint and the typecheck to the sealer, after the rounds settle | |

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`.

## Operational impact

- **No migration, no env var, no dependency.** Every change is inside this
  repository's own checkers, tests, templates and records.
- **Three new refusals**, and `CONTRIBUTING.md` §*What a change to a gate must
  carry* asks the pull request to answer for each: the test seen red, the
  failure direction, and the prompt budget. The direction is the same for all
  three — each blocks more and allows nothing new — and the **prompt budget is
  zero**: all three fire inside a generator or a checker a session is already
  running, none puts a question in front of a person, and none reaches a
  `PreToolUse` hook.
- **The record gains a field**, so a work item begun after the cutoff and
  reviewed by a session on an older plugin version would write a record without
  it. That is what the cutoff is for, and the phase's acceptance runs the
  checker over every record already in the tree.
- **A backward compatibility break in `close`'s argument contract**: a caller
  passing `--range <a>..HEAD` stops working. That is the fix, and the refusal
  says what to write instead.
