# 1790076080-every-orchestrator-rule-is-a-sentence — round 3 report

| Field | Value |
|---|---|
| Round | 3 — the verifying round for round 2's fixes, and the last record of this run |
| Target SHA | `54198d71e2dc586b3b13a3e24de31ebeb8a4848e` |
| Fix range read | `39732781bedc2db5288250acb54c063f01bbbb03..efa1f82a7d1fe0788eda28852767fd0e973ce644`, 1 commit |
| Base | `origin/release/v0.13.1` |
| Branch | `docs/330-every-orchestrator-rule-is-a-sentence` |
| Inherited | rounds 1 and 2, their verdicts taken as settled and their coordinates opened rather than re-found |

Read and executed in a `git clone --no-local` of the worktree at the target
SHA, with a `uv` virtual environment inside it. The clone, the environment and
both probe files are deleted; the worktree is clean and no sibling worktree
was opened.

Round 2's `New units` reads `none`, and the range adds no `def` and no
`class`, so there was no unreviewed finding surface. Scope held to the fix
diff. The branch was not re-read.

## What round 2 asked and what the fix answers

Round 2's one 🟡 is closed, and the three corrections it recorded are made.
Every number in the fix was re-derived here rather than taken from the fix
pass's account of it, because two of these numbers have now been wrong twice
in the same direction.

The fix went further than the paste-ready block it was given, and that was
right. The block listed five planted directions; the module has eight. Writing
it verbatim would have left the docstring short by three, in the module whose
subject is that an enumeration short of its tree is worthless.

### 🟢 The docstring's enumeration is complete, and it names its class

`tests/test_every_orchestrator_act_names_its_delivery.py`, the module
docstring.

Counted by construction off the AST rather than by reading the block. The
module has 13 test functions. Exactly 10 of them call `_tree`, and those 10
split cleanly by what they assert: 8 assert `len(found) == 1` with a substring
naming the planted defect, and 2 assert `findings(...) == []`. The docstring
says *eight planted trees carry a defect* and *two more planted trees carry no
defect*, and lists all ten by name. That is the class, exactly.

The three cases the docstring does not name are outside the class it names,
not missing from it: `test_every_orchestrator_act_names_its_delivery` is named
separately as the real-tree case, and `test_the_table_reads_the_section_that_holds_it`
and `test_both_orchestration_files_are_read` plant no tree. The block says
what it is a list **of**, which is what makes the omission readable rather
than a second short list.

**Every name in the docstring resolves.** Twelve backticked `test_` names
appear in it; eleven are functions in this module and the twelfth is
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, the
neighbour module it imports its heading reader from. Nothing in the block
points at a case that does not exist.

### 🟢 No name in the docstring is split across a line break

This is the half a reader would meet again, and it is closed by construction
rather than by care. Every `test_` name in the block sits alone on its own
line with its description indented beneath it, so no docstring line carries an
odd number of backticks and no identifier spans a break. The ordinary prose
sentence that used to hold the name is gone, which is what removed the
possibility rather than the instance.

### 🟢 The exemption sits where the arm reads it — shown by taking it away

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/rounds/round-2-report.md`
line 148, against `skills/evidence-check/scripts/evidence_check.py#claim_lines`.

`claim_lines`' docstring states the rule — a line carrying the marker is
exempt, and it exempts the **line** rather than the name. Read against the
records arm's own loop, which yields `(number, name)` from `stated_names` and
refuses any name not in `tree_names`.

**Executed, red-first.** With the marker moved back to the end of the
paragraph and the name left bare on its own line, `evidence-check` exits **2**
and names the coordinate: `round-2-report.md:148`, `1 refused`. Restored, it
exits **0** at `1451 ok / 0 drifted / 0 broken / 0 refused`. So the placement
is load-bearing and the fix is real rather than cosmetic.

One thing worth recording about that probe, because it cost a false green
first. My probe script was written **inside** the clone, and `tree_names`
reads the tree outside the records — so the probe's own text put the name into
the tree and the mutation came back exit 0. A control name invented for the
test resolved too, which is what exposed it. Re-run from outside the clone,
the refusal reproduced. A probe that mutates a tree-wide name check cannot
live in the tree it checks.

### 🟢 The citation count is twelve, and the method behind it is reproducible

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` and
`phases/phase-3.md`.

Re-derived rather than read, because this number has been wrong twice. At the
target SHA, tolerating the line wraps this repository's prose uses, **12**
tracked files outside `CHANGELOG.md` and `seal/specs/` name the heading. Ten
of the twelve are reachable single-line; the two that are not are exactly the
two the record names, `.github/scripts/roll_flow_measurement_issue.py` and
`skills/commit-pr-convention/SKILL.md`. Four of the twelve are test modules
that would go red on a rename — `tests/test_a_segment_feeds_the_flow_log.py`,
`tests/test_session_cost_post.py`, `tests/test_the_chain_section_has_one_shape.py`
and `tests/test_the_handoff_before_round_one.py`. `seal/ledger.md` carries
**9** rows anchored on the heading text. Every one of those five figures is
what the record states.

The whole-tree total is stated with its tree, which is the repair that matters
here: at `39732781` I count **49** wrap-tolerant and **40** single-line, which
is exactly what `phases/phase-3.md` says. One clause of that same sentence is
wrong and is a correction below.

### 🟢 The denominator is thirteen, and nothing survived

The acts table counted mechanically off `skills/implement/orchestration.md`:
20 rows, 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its
parent's act`. Thirteen delivered. Both places round 2 named now read
thirteen, and the word *fourteen* survives nowhere in this work item's files.
`phases/phase-1.md` no longer contradicts its own tally table two lines above.

### 🟢 O7 sits below O6

`seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` now runs O1
through O7 in order, and the header comment above the table is true of it.

## What this round opened

All three are records. None changes behaviour, none commissions a fix pass,
and the run does not reopen for them.

### ⬜ · One clause of the corrected citation sentence attributes two figures to the wrong commit

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/phases/phase-3.md`
line 65 — *"the round that raised this read 48 and 37 at `73e71c1a`, four
commits earlier."*

Both halves of that clause are wrong, and the sentence's own subject is that a
count has to say what tree it was taken over.

- **48 is right at `73e71c1a`; 37 is not.** Measured over the tracked tree,
  single-line at `73e71c1a` is **39**. The figure 37 belongs to `238dbeaf`,
  the commit round 1 reviewed, which is where round 2's report put it and
  where its probe row records it as the first of `37 / 39 / 39 / 39`.
- **`39732781` is one commit after `73e71c1a`, not four.** Four is the length
  of round 2's own fix range, `238dbeaf..da35172f`, which is a different pair
  of commits.

The paragraph exists to pin a total to a tree so a reader can re-derive it.
A reader who re-derives 37 at `73e71c1a` gets 39 and concludes the whole
correction drifted, when only this clause did.

### ⬜ · The fix pass edited round 2's report past what its correction note declares

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/rounds/round-2-report.md`,
lines 145–165.

The `<!-- Corrected -->` comment the fix pass left names one change: the
marker moved onto the name's own line. Two other things changed in the same
paragraph and neither is named.

- The quotation was re-cast. It read *"`<the name>` is the case that asserts
  the real-tree check can fail at all"* and now reads *"… is the case that
  asserts the real-tree check can fail at all"*, with the name lifted out onto
  its own line. This is what the marker rule required, so it is declared in
  substance even though the note describes only the marker.
- **The word *four* was removed from the reviewer's own sentence.** It read
  *"and the four planted cases are what make it able to fail"*; it now reads
  *"and the planted cases"*. The direction is right — four was wrong, the
  module has eight — but a number was taken out of a committed reviewer's
  record with nothing saying so. Round 2's record and its report now differ
  in a word that was one of round 2's own miscounts, and only the report
  moved.

Three blank lines were left at 163–165 where markdown wants one. Cosmetic, and
in the same edit.

What this costs is small and it is the run's own recurring class: a record
corrected in the right direction, with the note covering less than the edit.

### ⬜ · `overview.md` §*Not done* says *twentieth* where it means *twenty-first*

`seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`
line 55 — *"a twentieth act written without the prefix costs nothing and is
counted by nobody."*

The table carries twenty rows for twenty acts, so an act written without the
prefix would be the twenty-first. Round 2's own deferred row states it that
way. **Pre-existing at `39732781` and outside this round's target diff**,
reported because this is the last record of the run and the sentence is one of
the two things being handed to an issue, where the off-by-one would be read as
the issue's scope.

## What was confirmed rather than opened

**The two floor cases are honestly described.** `test_a_clean_planted_tree_is_clean`
is the same tree without the defect, as the block says, and
`test_a_third_level_heading_under_an_unmarked_section_is_not_an_act` asserts
no finding over a tree that carries none. Calling the second a floor is a
slight widening of the word — it guards a false positive rather than the
planted trees' baseline — but both are green-expected cases over a planted
tree, which is what the sentence claims of them. Not a finding.

**Nothing pins the docstring to the module.** Confirmed against the checker
rather than assumed: the records arm reads `.md` files under a live work item,
so a Python docstring is outside everything that runs. The enumeration is
correct today and nothing holds it there. This is the deferral below, and it
is mechanism a fix pass may not add.

**The orchestrating session's readings reproduce.** `evidence-check` unscoped
exits 0 at `1451 ok · 0 drifted · 0 broken · 0 refused`, and the records arm
reads 93 names with 0 refused. The narrow suite is green.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 2's 🟡 1, first half — the docstring enumerated four directions where more stand | `tests/test_every_orchestrator_act_names_its_delivery.py`, the module docstring | **answered** | Counted by construction off the AST, not read: 13 tests, exactly 10 plant a tree, 8 of those assert one named finding and 2 assert none. The block lists all ten and says what it is a list of. The fix completed the list to eight past the paste-ready block's five, which listed five where the module has eight |
| 🟢 | Round 2's 🟡 1, second half — the block named a case that is in no file | `tests/test_every_orchestrator_act_names_its_delivery.py`, the module docstring | **answered** | Twelve backticked `test_` names in the block: eleven are functions in this module, the twelfth is the neighbour module it imports from. No name is split across a line break — every name sits alone on its own line, so no docstring line carries an odd number of backticks. The shape that hid the old name is gone rather than the instance |
| 🟢 | The fourth correction the fix commissioned — the not-in-tree marker's placement | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/rounds/round-2-report.md` line 148, `skills/evidence-check/scripts/evidence_check.py#claim_lines` | confirmed | The exemption sits where the arm reads it, shown by taking it away: marker at the paragraph end gives exit 2 naming `round-2-report.md:148` with `1 refused`; as shipped, exit 0. The first attempt at this probe came back a false green because the probe file lived inside the clone and `tree_names` read the name out of it |
| 🟢 | The citation count restated with its method | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md`, `phases/phase-3.md` | confirmed | Re-derived, not read. Twelve files outside `CHANGELOG.md` and `seal/specs/`, ten single-line and the two wrap-only ones exactly as named; four test modules; nine rows in `seal/ledger.md`; 49 wrap-tolerant and 40 single-line at `39732781`. Every figure matches except one clause, below |
| 🟢 | The denominator is thirteen in the two places that read fourteen | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` line 23, `phases/phase-1.md` line 63 | confirmed | Counted the acts table myself: 20 rows, 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its parent's act`, thirteen delivered. The word *fourteen* survives nowhere in this work item's files |
| 🟢 | O7 moved below O6 | `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` | confirmed | The fragment runs O1 through O7 in order and the header comment above the table is true of it |
| ⬜ | The corrected citation sentence gives 37 for `73e71c1a`, where 37 is `238dbeaf`'s figure, and calls a one-commit distance four | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/phases/phase-3.md` line 65 | correction | Single-line at `73e71c1a` is 39; 37 is the count at `238dbeaf`, which is where round 2's own probe row puts it. `git rev-list --count` gives 1 for `73e71c1a..39732781`; four is the length of round 2's fix range, a different pair. The paragraph's own subject is pinning a total to a tree |
| ⬜ | The fix pass removed a number from round 2's committed report and its correction note covers only the marker move | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/rounds/round-2-report.md` lines 145–165 | correction | *"the four planted cases"* became *"the planted cases"*. The direction is right — the module has eight — but the `<!-- Corrected -->` comment names the marker's placement and nothing else, so the record and the report now differ in one of round 2's own miscounts with only the report moved. Three blank lines left at 163–165 |
| ⬜ | §*Not done* says a *twentieth* act where the table already carries twenty rows | `seal/specs/1790076080-every-orchestrator-rule-is-a-sentence/overview.md` line 55 | correction | An act written without the prefix would be the twenty-first, which is how round 2's deferred row states it. Pre-existing at `39732781` and outside this round's target diff; reported because this sentence is what the issue will be scoped from |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | the branch | out of scope | Contract §2 leaves the broad gate to the definition that assigns it, and this one assigns none. The sealer answers it, once, after the rounds settle. This round did not run it, and nothing in this report holds it back |

## Executed probes

| What was run | Result |
|---|---|
| `pytest` over `tests/test_every_orchestrator_act_names_its_delivery.py` and `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, the module the diff edits and the module it imports from, in a clone at the target SHA | 23 passed |
| The same plus `tests/test_session_cost_post.py` | 51 passed |
| `bin/evidence-check .` unscoped, in the clone at the target SHA | exit 0 · 1451 ok · 0 drifted · 0 broken · 0 refused. Records arm: 1 work item read · 93 names read · 0 refused |
| §15 probe — the not-in-tree marker moved back to the end of the paragraph, the name left bare on its own line, run from **outside** the clone | exit 2, `NOT-IN-TREE  …/rounds/round-2-report.md:148`, `1 refused`. Restored: exit 0, `0 refused`. The placement is load-bearing |
| The same probe written inside the clone | False green — exit 0 both ways. `tree_names` read the name out of the probe file itself; a control name invented for the test resolved too, which is what exposed it |
| The module's cases classified off the AST: which call `_tree`, and what each asserts | 13 tests · 10 plant a tree · 8 assert one named finding · 2 assert none. The docstring's eight-and-two is the class exactly |
| Every backticked `test_` name in the docstring resolved against the module and the tree | 12 names · 11 functions in this module · 1 the neighbour module it imports from · 0 unresolved · 0 split across a line break |
| Files naming the flow-log heading, counted at `238dbeaf`, `73e71c1a`, `39732781` and the target SHA, single-line and wrap-tolerant | 37/47 · 39/48 · 40/49 · 40/49. Outside `CHANGELOG.md` and `seal/specs/` at the target: 12 wrap-tolerant, 10 single-line, 4 test modules, 9 rows in `seal/ledger.md` |
| The acts table counted mechanically off `skills/implement/orchestration.md` | 20 rows: 8 `check:`, 5 `command:`, 5 `still a sentence`, 2 `part of its parent's act`. Thirteen delivered |
| `git rev-list --count` for `73e71c1a..39732781`, `..efa1f82a`, `..54198d71` | 1, 2, 3. No reading gives four |
| The word *fourteen* searched across every tracked file | No occurrence in this work item's files. The remaining hits belong to other work items and to `seal/ledger.md` |
| The broad gate — the full suite, the repository-wide lint, the typecheck | not yet, and not run here. It is the sealer's, once, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Nothing pins the module docstring's enumeration to the module. It is correct at this commit and a case added next month makes it wrong silently — confirmed against the checker: the records arm reads `.md` under a live work item, so a Python docstring is outside everything that runs. A case comparing the block's names against the module's own AST would close it, and a case is mechanism a fix pass may not add | `overview.md` §*Not done*, with the two already there. I agree it belongs with them: it is the same shape — an enumeration the tree does not hold in step — and it is what round 2's 🟡 was an instance of | the repository owner, with the two beside it. It is a small case rather than a design choice, so it is the cheapest of the three to close |
| The row rule cannot reach an act addressed to the orchestrator outside the two orchestration files, which the flow-log act is | `overview.md` §*Not done*, already deferred in rounds 1 and 2, named for an issue | the repository owner — choosing between the two shapes is a person's |
| The table reads the marker and not the meaning, so an act written without the prefix is counted by nobody | `overview.md` §*Not done*, already deferred in rounds 1 and 2 | the repository owner, with the above |
| Whether a network-writing arm needs a row of its own in `CONTRIBUTING.md` (Q3) | `overview.md` §*Not verified*, shipped as default (a), already deferred in rounds 1 and 2 | the repository owner, who owns that list |

Needs a fix: no — the one 🟡 round 2 opened is closed on this round's own grounds, and all three corrections are made. The three findings above are records, they commission nothing, and the run ends here.
Loses a record or crashes: no

## Proof block

📋 code-review applied

· read: `rounds/round-1.md`, `rounds/round-2.md` and `rounds/round-2-report.md`
  of this work item · the fix diff `39732781..efa1f82a` in full and the
  closure commit `efa1f82a..54198d71` · both commit messages ·
  `tests/test_every_orchestrator_act_names_its_delivery.py` in full, docstring
  and every case · `skills/evidence-check/scripts/evidence_check.py`
  (`claim_lines`, `stated_names`, `tree_names`, the records arm's loop and its
  closing counts) · `skills/implement/orchestration.md`'s twenty rows ·
  `seal/ledger/1790076080-every-orchestrator-rule-is-a-sentence.md` ·
  `overview.md`, `phases/phase-1.md`, `phases/phase-3.md` of this work item ·
  the twelve files naming the flow-log heading, at their citations
· executed: the twelve rows of §*Executed probes* above, in a
  `git clone --no-local` at the target SHA with its own `uv` virtual
  environment. Clone, environment and both probe files deleted; the worktree
  is clean and no sibling worktree was opened
· unverified: the full suite, the repository-wide lint and the typecheck —
  the sealer's, once, after the rounds settle. This report holds nothing back
  from it
