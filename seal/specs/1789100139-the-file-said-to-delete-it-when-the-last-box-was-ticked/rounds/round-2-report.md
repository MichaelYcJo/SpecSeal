# round 2 — review report

| | |
|---|---|
| Target | the diff of round 1's fixes, `bfe8cdb..17a4737` — not the branch |
| Review at | `86d8e41f5a97680651bdb8c9d8327012dbccacd3` — adds only `round-2-asked.md` on top of the target |
| Base | `origin/release/v0.11.1` = `5646717` |
| Ran by | `specseal:warden on Opus 5` |
| Worked in | a `git clone --no-local` at the review SHA, under the session scratchpad, removed after this report |

## What this round found, in the order one thing caused the next

Round 1's complaint was one habit stated nine ways: **a number written into a
record without the measurement that produces it**. The fix pass closed that
habit where it mattered most and repeated it where it did not.

Where it closed, it closed hard. Finding 4 asked for the module set to be
named instead of counted; `overview.md` now names thirteen modules with a
count each, and all thirteen counts reproduce exactly, each exit 0, 447
together. That is the strongest closure in the round, and it is what makes the
rest legible.

Where it repeated, it repeated in the corrections themselves. Finding 5's
replacement figure is attributed to a commit where it does not hold; finding
9's replacement figure holds at no commit at all; and the file finding 5
edited gained a new heading whose count its own table contradicts. None of the
three reaches a gate — every check is green at the review SHA — so all three
are corrections rather than fixes.

```
① round 1: a count with no measurement behind it
       ↓ closed properly
② finding 4 — thirteen modules named, every count reproduces
       ↓ same habit, in the corrections
③ finding 5's "32 at 62c22ca" is 35 at 62c22ca
④ finding 9's "467 single" is 473 at every commit
⑤ survivors.md's new heading says five rows over six
       ↓ and separately
⑥ finding 3's deferral reached none of the three places that carry one
```

---

## The seven that are closed, re-derived rather than inherited

**Finding 1 is closed, and the §15 probe reproduces exactly as claimed.**
`bin/test -q tests/test_routing_is_recorded.py` at the review SHA is 31
passed, exit 0. With `hooks/routing.py` mutated so an absent `Planning` row
reads as `framer`, the new assertion goes red, exit 1, and names exactly one
offender — `1788177600-the-tree-that-arrives-without-its-history/routing.md`,
one distinct path and no other. The parser was restored from bytes kept before
the mutation, `git status --porcelain` came back empty, and the module was
green again afterwards. The claim that the restore came from kept bytes rather
than from HEAD is a claim I can only make about my own probe, which was
written that way; for the fix pass's own probe it stays the fix pass's word.

**Finding 1's stated limit holds, and it holds under either reading of the
mutation.** The load-bearing half — that the case's `Implementation` arm is
unexercised by the tree — is confirmed: with the `Implementation` default
mutated to `smith`, this case alone is exit 0. What the number depends on is
which mutation you mean.

- Absent row reads as `smith` — `found.get(IMPLEMENTATION, BY_SMITH)` — gives
  **2 failed, 29 passed, exit 1**.
- Absent *or unreadable* answer reads as `smith` — the `else BY_SMITH` arm of
  the returned dict — gives **3 failed, 28 passed, exit 1**, the third being
  `test_an_unreadable_third_axis_reads_as_unanswered_not_as_no_declaration`.

The record says three, which is true of the second mutation. I am not calling
that a defect; I am recording that the figure is mutation-dependent and the
record does not say which mutation it was. The limit itself is sound either
way.

**Finding 2 is closed and the smith's correction of my predecessor's text was
right.** The paragraph at `skills/implement/orchestration.md:23` now scopes
itself to *the three sections #292 moved*, and *The order below is the
exception* points at `## Orchestrator: the order inside a ticket` at line 34,
which is below it. Round 1's paste-ready text said *above* and would have been
wrong.

**Findings 6 and 7 are closed.** The two ledger notes are no longer identical
— 6514 characters at `seal/ledger.md:1366` against 339 at `:1367` — and R3's
note now records its own re-anchoring from `@08730484` to `@98c5bec1`.
`seal/ledger.md:1646`'s first reason is in the past tense with the `#351`
clause added, word for word as round 1 proposed.

**Finding 8 is closed, and the second attempt held.** `plan.md`'s phase table
parses to contiguous data rows `1 2 3 4 5 6` with no blank line between rows 5
and 6, and the two prose paragraphs follow the completed table.
`overview.md:95` reads *The six divergences above*.

**Finding 9's loaded half is closed.** Doubled `Checked` cells went from 3 to
0. Three Notes cells moved from the run-on form to the sentence-break form —
`[a-zA-Z] **Re-read` falls 57 → 54 and `. **Re-read` rises 163 → 166, which is
the same three. `docs/issues-and-milestones.md` is re-wrapped and
`test_docs_line_wrap` is 23 passed, exit 0.

**Finding 4 is the one that closed hardest.** Every one of the thirteen counts
reproduces, run one module at a time, exit 0 each:

| Module | Claimed | Measured |
|---|---|---|
| `test_the_rules_have_one_owner` | 45 | 45 |
| `test_release_hygiene` | 32 | 32 |
| `test_docs_line_wrap` | 23 | 23 |
| `test_a_corrected_sentence_survives_elsewhere` | 43 | 43 |
| `test_one_word_one_meaning` | 13 | 13 |
| `test_no_document_names_the_old_roots` | 11 | 11 |
| `test_no_real_identifiers` | 2 | 2 |
| `test_unverified_rows_close` | 86 | 86 |
| `test_a_section_marked_for_one_role_reaches_only_that_role` | 9 | 9 |
| `test_a_record_states_what_the_tree_has` | 58 | 58 |
| `test_a_rider_reaches_its_file` | 29 | 29 |
| `test_routing_is_recorded` | 31 | 31 |
| `test_the_seal_is_taken_once_by_the_sealer` | 65 | 65 |

447 passed over the thirteen together, exit 0. The internal arithmetic checks
out too: the first nine sum to 264 and the first eleven to 351, which is why
neither earlier figure could be reproduced.

---

## The corrections this round opens

Each of the four below sits under `seal/specs/`. Per `docs/review-chain-spec.md`
§*The last round verifies, and what it verifies is a diff*, a finding located
in a record is a correction — it owes no fix pass and no reader, it is
corrected in the closing commit, and `Needs a fix` does not count it. Each
closes `answered — corrected at <sha>` in that commit.

### ⬜ 10. Finding 5's replacement figure belongs to a different commit

`seal/specs/…/rounds/round-2-fixes.md:20` · `rounds/round-1.md:88`

The fix table says *Measured at `62c22ca`: `every survivor is excused by a row
above (32)`, exit 0, and the reported places split 29 records to 3 loaded
files*. **Executed**, with the exemption row's own range spec
(`origin/release/v0.11.1...HEAD`) so the range row actually matches, exit codes
read directly:

| Commit | Excused | Records | Loaded files |
|---|---|---|---|
| `90f2f9d` | 32 | 29 | 3 |
| `ae2d0ac` — round 1's target | 32 | 29 | 3 |
| `62c22ca` — where the fix table says it measured | **35** | **30** | **5** |
| `a3b4fc3` | 36 | 31 | 5 |
| `17a4737` — the end of the fix range | 36 | 31 | 5 |

So `32` and the `29 + 3` split are round 1's numbers at round 1's target, and
the fix table attributes them to its own commit, where they are `35` and
`30 + 5`. This is round 1's finding 4 in its own correction: a figure carried
across a measurement point rather than re-taken at it.

Nothing is broken by it. `overview.md`'s `· verified` line says *32 places, all
32 excused* about a run the builder made at `90f2f9d`, and at `90f2f9d` that
is exactly right — an executed claim is about its moment, and that one is
honest. What is wrong is only the fix table's attribution.

### ⬜ 11. Withdrawing the bullet is what put the place back in the reported set

`seal/specs/…/survivors.md:16`, `:17`, `:33`, `:42`

Round 1 withdrew the
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` bullet on the
grounds that the check does not report that line. It does report it — from
`62c22ca` onward, which is the commit that withdrew the bullet.

The mechanism is the one the fix table names itself, #308's quote-dependence:
an exemption quote joins the written side and leaves the search set. While the
bullet stood, its quote was what removed the sentence at `:602` from the set
the check searches. Round 1 measured the absence that the bullet's own presence
created, and concluded the bullet was wrong about a place that was only
invisible because the bullet was there. Measured at `62c22ca` with no
exemption file, the loaded-file places are five, and `:602` is among them.

The gate is unaffected: at the review SHA the range row excuses all 36,
`every survivor is excused by a row above (36)`, exit 0. What is wrong is the
prose. `survivors.md:16` still says *The 32 were opened rather than waved
through, and the three that are not records are named here*, `:17` says *29 of
the 32*, and `:42` says *All 32 reported places were opened; the three outside
the records are listed above* — where the tree those sentences are committed
in reports 36, of which 5 are loaded files and two of those five are named
nowhere in the three bullets.

The withdrawal itself was still the right act. The bullet described a
docstring the file does not carry, which is true independently of the counting.

### ⬜ 12. The heading added by the fix pass counts five rows over a table of six

`seal/specs/…/survivors.md:44`

The heading reads `## Round 1's fix range — five per-survivor rows` and the
table beneath it has six. `a3b4fc3` added the sixth row and left the heading
alone. This is finding 8's class — a count in a record that the table under it
contradicts — reappearing in the same pass that closed finding 8.

Two nearby sentences are not defects and should be left alone. `:46` says
*`bfe8cdb..62c22ca` reported five places*, which is **executed and true**: that
range reports exactly five, and they are the table's first five rows. `:50`
says *Two of the five*, which is about those five places rather than about the
rows. Only the heading counts rows, and only the heading is wrong.

### ⬜ 13. Finding 9's corrected count reproduces at no commit either

`seal/specs/…/rounds/round-2-fixes.md:24` · `rounds/round-1.md:92`

Round 1 wrote *468 written with single spaces*; the fix pass corrected it to
*3 doubled against 467 single*. Counting date cells as whole table cells gives
473 single and 3 doubled at `ae2d0ac`, and 473 and 3 at `bfe8cdb` — so neither
468 nor 467 is the number at any commit in the range, and the correction moved
from one unreproducible figure to another.

The measurement that matters is sound: doubled cells go 3 → 0 at `17a4737`,
and 473 + 3 = 476 single afterwards, which is the three re-padded cells
arriving in the single-spaced population. The denominator is decoration and
nothing reads it. It is worth correcting only because it is the third figure
in this run written without the command that produces it.

### ⬜ 14. The deferred decision reached none of the three places that carry one

`seal/specs/…/questions.md` · `overview.md:61` · `rounds/round-1.md:86`

Round 1's finding 3 — whether `spec.md` may narrow issue #351's `Done when` —
was deferred to the repository owner, correctly. Where it went is the problem.
`docs/review-chain-spec.md`'s leftover table sends *a decision only a person
can make* to `seal/specs/<item>/questions.md`, *and named in the PR body*. It
is in none of these:

- **`questions.md`** — no row. Q2 is a different question, about who makes the
  tracker writes.
- **`overview.md`'s `## Not verified`** — three open rows, none of them this;
  `bin/unverified-check` is exit 0 and does not see it.
- **`seal/follow-up.md`** — nothing for `#351`, and that file's own opening
  sends a coordinate-tied item to a `# RIDER:` instead.

What survives is `rounds/round-1.md:86`, whose Verdict cell reads `deferred
the repository owner` and whose Grounds cell reads `the repository owner` —
the home written twice and the question itself nowhere. The fix pass's
explanation of the deferral is in `rounds/round-2-fixes.md:18` and stops
there, because `round_record.py`'s `fix_table` takes the home out of a
`deferred` verdict and discards the third cell. Nothing is lost from the tree;
what is lost is the reader, and the reader is the person about to write the PR
body.

---

## The two judgements this round was asked to make

**A survivor by construction may be excused by a row, and this one is.**
Finding 6's fix removed R3's duplicate note, so the sentence still standing at
`seal/ledger.md:1366` is wording the range removed — at the coordinate it was
removed from, not at the one it belongs to. The check has no way to tell a
de-duplication from a missed correction, and the two answers available are a
row or a correction. Correcting would delete the sentence the de-duplication
existed to leave in one place, which is the opposite of what the check is for.
The row is the right instrument, and its Grounds cell names the mechanism
rather than asserting an exemption. I confirmed it excuses the right place:
over `bfe8cdb..17a4737` the check reports exactly two places, `seal/ledger.md:1366`
and `hooks/routing.py:189`, and both are excused, exit 0.

One thing a reader should know, and it is not a defect: the row's Quote is the
shared sentence, so that quote now joins the written side and leaves the search
set. That is the same #308 behaviour as finding 11 above. Whether
`survivor_check.py` should recognise a removed sentence that is byte-identical
to one still standing in the same file is a question about the checker, not
about this branch, and it belongs to the repository owner.

**The `fixed` / `answered` split holds against the spec, on every one of the
nine.** The rule keys on `Location`. Findings 4, 5, 6, 7 and 8 are located
wholly under `seal/specs/` or `seal/ledger.md` and closed `answered`; findings
1 and 2 are in `tests/` and `skills/` and closed `fixed`. Finding 9's Location
spans both — three ledger cells and two lines of
`docs/issues-and-milestones.md` — and closed `fixed`, which is the right read:
the spec's sentence covers a finding whose location is in the records, and a
mixed finding has a half that genuinely commissioned a reader. Finding 3
closed `deferred`, which is neither a fix word nor an answer, and is what the
verdict is.

---

## Labels

- **Executed** — everything in `## Executed probes`, exit codes read directly
  with `; echo $?` and no pipe, in a `--no-local` clone at the review SHA. The
  clone was left clean after every mutation.
- **Read** — findings 12 and 14, the `fixed`/`answered` split, and the
  by-construction judgement's reasoning.
- **Unverified** — the broad gate. Contract §2 and §3 forbid it to this round;
  `agents/sealer.md` is the agent it is assigned to, and this report leaving
  nothing needing a fix is what makes that spawn due. Also unverified and
  carried rather than re-opened: whether the four milestone descriptions and
  two ticket comments phase 5 wrote read back as stated, which the
  orchestrating session answers.

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
| 10 | ⬜ Finding 5's replacement figure is attributed to `62c22ca`, where it is 35 and 30 + 5 rather than 32 and 29 + 3 | `seal/specs/…/rounds/round-2-fixes.md:20`, `rounds/round-1.md:88` | open | Executed at five commits with the exemption row's own range spec: 32 at `90f2f9d` and `ae2d0ac`, 35 at `62c22ca`, 36 at `a3b4fc3` and `17a4737`, exit 0 each. The 29 + 3 split holds only at the first two |
| 11 | ⬜ Withdrawing the bullet returned its place to the reported set, so the counts in `survivors.md` no longer describe the tree they are committed in | `seal/specs/…/survivors.md:16`, `:17`, `:33`, `:42` | open | Executed at `62c22ca` with no exemption file: five loaded-file places, `tests/test_the_suite_has_a_command_that_is_cheap_twice.py:602` among them. #308's quote-dependence, which the fix table names. The gate is exit 0 regardless |
| 12 | ⬜ The heading the fix pass added counts five per-survivor rows over a table of six | `seal/specs/…/survivors.md:44` | open | Read, and counted: six rows. `a3b4fc3` added the sixth and left the heading. `:46`'s *reported five places* is executed and true for the range it names |
| 13 | ⬜ Finding 9's corrected denominator reproduces at no commit | `seal/specs/…/rounds/round-2-fixes.md:24`, `rounds/round-1.md:92` | open | Executed: 473 single-spaced date cells and 3 doubled at both `ae2d0ac` and `bfe8cdb`, 476 and 0 at `17a4737`. Neither 468 nor 467 |
| 14 | ⬜ The deferred decision reached neither `questions.md`, nor `## Not verified`, nor `seal/follow-up.md` | `seal/specs/…/questions.md`, `overview.md:61`, `rounds/round-1.md:86` | open | Read, and checked in all three: no row anywhere. `bin/unverified-check` exit 0 and blind to it. The record's Grounds cell repeats the home instead of the question, because `fix_table` discards a `deferred` row's third cell |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `spec.md` §Out may narrow issue #351's `Done when`, which sends two standing rules to `docs/issues-and-milestones.md` | still only `rounds/round-1.md:86` and `rounds/round-2-fixes.md:18`; finding 14 asks for a `questions.md` row so the PR body can name it | the repository owner |

## Paste-ready fixes

Finding 12 — `seal/specs/…/survivors.md:44`, the heading.

```markdown
## Round 1's fix range — a row per survivor
```

Finding 10 — `rounds/round-2-fixes.md:20`, the sentence after *33 becomes 32*.

```markdown
Measured at `ae2d0ac` and at `90f2f9d`, the two commits round 1 could run it
at: `every survivor is excused by a row above (32)`, exit 0, and the reported
places split 29 records to 3 loaded files. The figure is range- and
quote-dependent, so it is not the figure at this pass's own commits: 35 at
`62c22ca` and 36 at `a3b4fc3`, each exit 0.
```

Finding 11 — `seal/specs/…/survivors.md:33`, the withdrawn-bullet paragraph.

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

Finding 13 — `rounds/round-2-fixes.md:24`, the denominator.

```markdown
Three doubled `Checked` cells re-padded — measured as whole table cells, 3
doubled against 473 single before and 0 against 476 after.
```

Finding 14 — a new row in `seal/specs/…/questions.md`, so the PR body has
something to name.

```markdown
| Q6 | Issue #351's `Done when` sends two standing rules to `docs/issues-and-milestones.md`; `spec.md` §Out ends the second instead, on the grounds that with the file gone the rule has no subject. Does that narrowing stand? | a person | **(a)** the narrowing stands and `spec.md` is the record of it · **(b)** the second rule is written into `docs/issues-and-milestones.md` after all | open | review round 1, finding 3 — the repository owner |
```

Needs a fix: no

Loses a record or crashes: no

## Proof

Opened and read, in a `--no-local` clone at `86d8e41`:
`seal/specs/1789100139-…/` (`spec.md`, `plan.md`, `questions.md`,
`overview.md`, `survivors.md`, `changelog.md`, `routing.md`,
`rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-2-asked.md`,
`rounds/round-2-fixes.md`); the full diff `bfe8cdb..17a4737` and
`17a4737..86d8e41`; `seal/ledger.md` at lines 1363–1367, 1430, 1646 and 1953,
and the same file at `bfe8cdb` and `ae2d0ac`; `seal/follow-up.md`;
`docs/review-chain-spec.md` §*The last round verifies, and what it verifies is
a diff*; `docs/issues-and-milestones.md`; `skills/implement/orchestration.md`;
`skills/code-review/scripts/round_record.py` (`fix_table` and the header
documentation of `new` and `close`), `skills/code-review/scripts/survivor_check.py`
around `RANGE_CELL`, `skills/code-review/scripts/chain_check.py` for the
verdict vocabulary; `hooks/routing.py#parse`;
`tests/test_routing_is_recorded.py`; `bin/test`.
