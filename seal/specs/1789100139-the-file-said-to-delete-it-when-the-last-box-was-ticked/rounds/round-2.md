# 1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked — review round 2

| Field | Value |
|---|---|
| Target SHA | 17a4737d1c565e6ed1474b46fc6c58f698e20b08 |
| Ran by | specseal:warden on Opus 5 |
| PR | #358 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

# round 2 — the verifying round's paragraph

| | |
|---|---|
| Target | the **diff of round 1's fixes**, `bfe8cdb..17a4737` — not the branch |
| Review at | `17a4737d1c565e6ed1474b46fc6c58f698e20b08` |
| Base of the branch | `origin/release/v0.11.1` = `5646717` |
| Draft pull request | #358 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-1.md`, closed — 3 fixed, 5 answered, 1 deferred |

## The job, and what it is not

**The answers, not new findings.** For each of round 1's nine verdicts, is it
actually closed. `round-1.md`'s `New units` row reads `none`, so there is no
new-unit surface in this diff to treat as a finding surface — the whole target
is a verification surface.

`round-1.md`'s `Needs a fix` named findings 1 and 2. Five more were answered as
corrections and one is deferred to the repository owner.

## What the fix pass says it did, to be checked rather than inherited

`rounds/round-2-fixes.md` is the table `close` applied, with its own
`## Verification of this pass`. Four claims in it are worth opening because
each is the kind that reads true and can be false:

- **Finding 1's §15 probe.** The new assertion is claimed red under a mutated
  `hooks/routing.py` — an absent `Planning` row reading as `framer` — naming
  `1788177600-the-tree-that-arrives-without-its-history/routing.md`. The
  parser is claimed restored from bytes kept before the mutation rather than
  from HEAD. Re-derive the probe.
- **Finding 1's stated limit.** The case's `Implementation` arm is claimed
  unexercised by the tree, because 0 of 73 declarations omit that row: the
  claim is that mutating the default to `smith` leaves this case green and
  three fixture cases in the same module red. A limit stated in a docstring is
  a claim like any other.
- **Finding 8's second attempt.** The first move of phase 6's row is claimed
  to have left a blank line that broke the table the same way the prose did,
  and to have been caught by parsing the table back. Check that the table in
  `plan.md` now parses to contiguous rows 1 through 6.
- **Finding 5's arithmetic.** 32 is claimed to split 29 records to 3 loaded
  files, and the withdrawn bullet's place is claimed absent from the reported
  set. Both are countable.

Two things the pass reports finding on its own, beyond what round 1 asked:

- Two more instances of finding 9's class in `plan.md`'s phase 1 and 2 Status
  cells, and a correction to round 1's own figure — 467 single-space `Checked`
  cells rather than 468.
- A §12 survivor at `seal/ledger.md:1366` that it calls a survivor **by
  construction**: finding 6's fix deleted a duplicate, so the original now
  reads as wording the range removed. It was given a sixth `survivors.md` row.
  Whether a by-construction survivor may be excused by a row rather than
  corrected is a judgement this round makes.

## Executed by the orchestrating session at `17a4737`

Exit codes read directly, no pipe:

- `bin/test -q tests/test_routing_is_recorded.py
  tests/test_waiver_decided_at_start.py` → **48 passed, exit 0**. The case
  round 1 found red is green.
- `git status --porcelain` → empty.

## Unverified

The broad gate. It is the `sealer`'s spawn, and it comes due when this round
closes the run — not before, and not yours.

## The commands, in the form to use

`bin/test`, narrow, one module at a time. `bin/evidence-check --strict` —
never narrowed to this work item's fragment.
`bin/survivor-check --range bfe8cdb..17a4737 --exempt
seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/survivors.md`
if you want to see the §12 surface for yourself.

## The line the run ends on

Answer the job in a line of its own — `Needs a fix: no`, or `yes` and what
does. A 🟡 answered with grounds is `no`, so this round may report findings and
still end the run. The reopening is **one**: if this round opens something, its
own fixes get one more verifying round and a second is refused.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The branch's first commit turned `test_every_declaration_in_this_repository_still_parses` red | `tests/test_routing_is_recorded.py:487` | answered | Closed at `62c22ca`, re-derived. 31 passed exit 0 at the review SHA. §15 reproduced: with an absent `Planning` row reading as `framer`, exit 1 naming exactly one offender, `1788177600-the-tree-that-arrives-without-its-history/routing.md`; parser restored from kept bytes, tree clean, green after |
| 2 | 🟡 `orchestration.md` claims a property the moved section does not have | `skills/implement/orchestration.md:23` | answered | Closed at `62c22ca`, Read. The paragraph scopes to the three sections #292 moved; *The order below* points at the heading at line 34, below the paragraph at 23. The smith's correction of round 1's *above* was right |
| 3 | ❓ Issue #351 sends two standing rules to one document; the spec ends one and no record says the ticket was overridden | `seal/specs/…/spec.md:56` | deferred the repository owner | Still the owner's, and still unanswered. Where it went is finding 14: no row in `questions.md`, none in `## Not verified`, none in `seal/follow-up.md` |
| 4 | ⬜ The executed count names no module set, and three figures disagree | `seal/specs/…/overview.md:22`, `:54` | answered | Corrected at `62c22ca`, re-derived in full. All thirteen named counts reproduce exactly, each exit 0; 447 passed over the thirteen together, exit 0. First nine sum to 264, first eleven to 351 |
| 5 | ⬜ *33 survivors* was 32, and one named loaded-file survivor is not among them | `seal/specs/…/overview.md:26`, `survivors.md:16`, `:17`, `:38` | answered | Corrected at `62c22ca`. 33 → 32 is right and `overview.md`'s executed claim is honest at `90f2f9d`. The replacement figure's attribution and the withdrawn bullet's grounds are findings 10 and 11 |
| 6 | ⬜ R3's appended ledger note is byte-identical to R1's | `seal/ledger.md:1367` | answered | Corrected at `62c22ca`, measured. 6514 characters at `:1366` against 339 at `:1367`, not identical; R3's note records its own re-anchoring |
| 7 | ⬜ A live ledger row's first reason names a file this branch deleted | `seal/ledger.md:1646` | answered | Corrected at `62c22ca`, Read. Past tense with the #351 clause added, word for word as round 1 proposed |
| 8 | ⬜ *The five divergences above* over six rows, and phase 6's row falls outside the table | `seal/specs/…/overview.md:87`, `plan.md:81` | answered | Corrected at `62c22ca`, measured. The phase table parses to contiguous data rows `1 2 3 4 5 6`; `overview.md:95` reads *six* |
| 9 | ⬜ Three `Checked` cells doubled, three Notes cells run on, two milestone lines short | `seal/ledger.md:1366`, `:1367`, `:1953`; `docs/issues-and-milestones.md:35`, `:39` | answered | Corrected at `62c22ca`, measured. Doubled cells 3 → 0; run-on form 57 → 54 and sentence-break form 163 → 166; `test_docs_line_wrap` 23 passed exit 0. Its denominator is finding 13 |
| 10 | ⬜ Finding 5's replacement figure is attributed to `62c22ca`, where it is 35 and 30 + 5 rather than 32 and 29 + 3 | `seal/specs/…/rounds/round-2-fixes.md:20`, `rounds/round-1.md:88` | answered | Corrected. `overview.md`'s `· verified` line now says the figure is 32 **at `ae2d0ac`, the tree that line describes**, and that it reads 36 at the branch tip because the range re-resolves and the exemption file's quotes move what is searched (#308). A count with no tree beside it was the whole of round 1's finding 4, and this is that class inside its own fix |
| 11 | ⬜ Withdrawing the bullet returned its place to the reported set, so the counts in `survivors.md` no longer describe the tree they are committed in | `seal/specs/…/survivors.md:16`, `:17`, `:33`, `:42` | answered | Corrected. `survivors.md` states both figures with their trees — 32 at `ae2d0ac`, 29 records and 3 loaded files; 36 at the tip, 31 and 5 — and names the two things that move them. The withdrawn bullet's paragraph now says that withdrawing it is what returned its place to the reported set, so round 1's *not among them* was true of a tree the bullet itself had made. The withdrawal still stands: the sentence was wrong about what is written at that line |
| 12 | ⬜ The heading the fix pass added counts five per-survivor rows over a table of six | `seal/specs/…/survivors.md:44` | answered | Corrected. The heading reads *six per-survivor rows* over the six that are there |
| 13 | ⬜ Finding 9's corrected denominator reproduces at no commit | `seal/specs/…/rounds/round-2-fixes.md:24`, `rounds/round-1.md:92` | answered | No edit, and the grounds are that nothing live carries the number. `467` and `468` appear only inside `rounds/`, which are records of what a party measured at a moment. Round 2's verdict row is where the correction belongs and it names what reproduces — 473 single-spaced date cells at `ae2d0ac` and `bfe8cdb`, 476 and 0 doubled at `17a4737`; re-derived here at the tip, 476 and 0 |
| 14 | ⬜ The deferred decision reached neither `questions.md`, nor `## Not verified`, nor `seal/follow-up.md` | `seal/specs/…/questions.md`, `overview.md:61`, `rounds/round-1.md:86` | answered | Corrected, and it is the one of the five that was a gap rather than a wrong number. The deferred decision is now `questions.md` Q6, with both answers spelled out and what shipped named as the default, and a `## Not verified` row carries it so `bin/unverified-check` reports it — exit 0, the row printed as `open` against the repository owner. It stood only in `rounds/round-1.md`'s Verdict and Grounds cells, both reading *the repository owner*, because `fix_table` discards a `deferred` row's third cell |

## Paste-ready fixes

```markdown
## Round 1's fix range — a row per survivor
```
```markdown
Measured at `ae2d0ac` and at `90f2f9d`, the two commits round 1 could run it
at: `every survivor is excused by a row above (32)`, exit 0, and the reported
places split 29 records to 3 loaded files. The figure is range- and
quote-dependent, so it is not the figure at this pass's own commits: 35 at
`62c22ca` and 36 at `a3b4fc3`, each exit 0.
```
```markdown
**A fourth bullet stood here, and withdrawing it is what put its place back
into the reported set.** While the bullet stood, its quote joined the written
side and left the search set (#308), which is why the check did not report
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` at `ae2d0ac`.
From `62c22ca` the check does report it, and the range row below excuses it
with the rest. The bullet was withdrawn on its own merits: the docstring at
that line is about pytest-xdist being installed by the workflow rather than by
the virtualenv, not the deadlock the bullet described. Round 1 found it
(finding 5).
```
```markdown
Three doubled `Checked` cells re-padded — measured as whole table cells, 3
doubled against 473 single before and 0 against 476 after.
```
```markdown
| Q6 | Issue #351's `Done when` sends two standing rules to `docs/issues-and-milestones.md`; `spec.md` §Out ends the second instead, on the grounds that with the file gone the rule has no subject. Does that narrowing stand? | a person | **(a)** the narrowing stands and `spec.md` is the record of it · **(b)** the second rule is written into `docs/issues-and-milestones.md` after all | open | review round 1, finding 3 — the repository owner |
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q tests/test_routing_is_recorded.py` at the review SHA | 31 passed, exit 0 |
| the same, with `hooks/routing.py` mutated so an absent `Planning` row reads as `framer` | exit 1; the new assertion names exactly one offender, `1788177600-the-tree-that-arrives-without-its-history/routing.md` |
| the same, after restoring the parser from bytes kept before the mutation | 31 passed, exit 0; `git status --porcelain` empty |
| the case alone, with the `Implementation` default mutated to `smith` | exit 0 — the arm is unexercised by the tree, as the docstring states |
| the module, same mutation as `found.get(IMPLEMENTATION, BY_SMITH)` | 2 failed, 29 passed, exit 1 |
| the module, mutation widened so an unreadable answer also reads as `smith` | 3 failed, 28 passed, exit 1 — the record's figure |
| the thirteen modules `overview.md` names, one at a time | 45 · 32 · 23 · 43 · 13 · 11 · 2 · 86 · 9 · 58 · 29 · 31 · 65, exit 0 each — every claimed count reproduces |
| the same thirteen together | 447 passed, exit 0 |
| `bin/test -q tests/test_waiver_decided_at_start.py` | 17 passed, exit 0 |
| `bin/evidence-check --strict` | total 1121 ok · 0 drifted · 0 broken · 0 external · 0 old-format, exit 0 |
| `bin/survivor-check --range bfe8cdb..17a4737 --exempt …/survivors.md` | 2 places, `seal/ledger.md:1366` and `hooks/routing.py:189`, both excused, exit 0 |
| `bin/survivor-check --range bfe8cdb..62c22ca` at `62c22ca`, no exemption file | 5 places, exit 1 — the five the per-survivor table's first five rows name |
| `bin/survivor-check --range origin/release/v0.11.1...HEAD --exempt …/survivors.md` at `90f2f9d` · `ae2d0ac` | 32 excused, exit 0 each — 29 records and 3 loaded files |
| the same at `62c22ca` · `a3b4fc3` · `17a4737` | 35 · 36 · 36 excused, exit 0 each — 30 + 5, then 31 + 5 twice |
| `bin/survivor-check --range origin/release/v0.11.1...HEAD --exempt …/survivors.md` at the review SHA | `every survivor is excused by a row above (36)`, exit 0 |
| `bin/unverified-check` | exit 0; 3 open rows for this work item, each with an answerer, and none of them finding 3 |
| `bin/deferral-check` | exit 0 |
| doubled and single-spaced `Checked` cells, counted as whole table cells | `bfe8cdb` 473 single · 3 doubled; `ae2d0ac` 473 · 3; `17a4737` 476 · 0 |
| the two note forms in `seal/ledger.md`, before and after | run-on 57 → 54, sentence-break 163 → 166 |
| `plan.md`'s phase table, parsed back | contiguous data rows `1 2 3 4 5 6` |
| new top-level units in the fix diff | none — no added `def` or `class` line in any Python file of the range, which is what `round-1.md`'s `New units` row says |
| **broad gate** — the full suite, the repository-wide lint, the typecheck | **not yet.** Contract §2 and §3 forbid it to this round. It is the `sealer`'s spawn, and this report is what makes it due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_routing_is_recorded.py:487` | round 1's 1 — fixed |
| round-1 | `skills/implement/orchestration.md:23` | round 1's 2 — fixed |
| round-1 | `seal/specs/…/spec.md:56` | round 1's 3 — deferred |
| round-1 | `seal/specs/…/overview.md:22`, `:54` | round 1's 4 — answered |
| round-1 | `seal/specs/…/overview.md:26`, `survivors.md:16`, `:17`, `:38` | round 1's 5 — answered |
| round-1 | `seal/ledger.md:1367` | round 1's 6 — answered |
| round-1 | `seal/ledger.md:1646` | round 1's 7 — answered |
| round-1 | `seal/specs/…/overview.md:87`, `plan.md:81` | round 1's 8 — answered |
| round-1 | `seal/ledger.md:1366`, `:1367`, `:1953`; `docs/issues-and-milestones.md:35`, `:39` | round 1's 9 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `spec.md` §Out may narrow issue #351's `Done when`, which sends two standing rules to `docs/issues-and-milestones.md` | still only `rounds/round-1.md:86` and `rounds/round-2-fixes.md:18`; finding 14 asks for a `questions.md` row so the PR body can name it | the repository owner |
