# 1788501054-a-check-reports-clean-while-something-is-missing — phase 8

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-8.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 8 |
| Commit | filled by the commit that closes this phase |
| Ran by | specseal:smith on opus |

## What this phase was asked

Round 4's one 🔴 and six 🟡, **as four classes rather than seven coordinates**.
This is the fourth round running that a class recurred inside its own fix, and
the instruction said so: round 3's pass was handed eight findings as four
classes and that is what turned a 12-mutation battery into 18 with 9
survivors. The handover reports what was enumerated per class, not which
findings were closed.

The four classes as they were given:

- **A record cell that a checker parses.** 🔴 1 — `round-3.md`'s `New units`
  carries prose inside its sixth `;`-separated entry, `depth_problems` refuses
  it, and the branch is RED at HEAD because of it. 🟡 2 — the same cell gives
  one reason for two widenings and it is false for one of them. Enumerate
  every cell in every round record that a checker parses and RUN them through
  the checker rather than reading them.
- **A recorded limit that is wrong.** 🟡 3 — one of the four limits round 3's
  fix pass recorded as unreachable is false, and half the guard it describes
  is load-bearing. 🟡 5 — the fallback sentence is false off Windows, which is
  round 1's 🟡 9 restated one branch over. **Re-derive all four**, and every
  other place this branch records a limit. A limit that is wrong is worse than
  one that is missing: it tells the next battery not to look.
- **The pins.** 🟡 4 — a rider stands in for a pin depth ALLOWS, because depth
  refuses a new unit and not a new assertion. 🟡 6 — the limit is written in
  five places, pinned in three, and the pinning case's own docstring says
  three. Count the copies and count the pins for every sentence this branch
  wrote or corrected.
- **The record's own trace.** 🟡 7 — `round-1.md:9` was corrected in place
  with no trace, and the obvious repair is refused by the checker. Check
  whether any other cell was corrected the same way and apply ONE rule to all
  of them.

Constraints: §15 on every case written or widened, with how each was seen red
in the handover; §12 in the handover, per class; edits through `Edit`; git
driven from Python where a probe needs a repository; `evidence_check.py .`
unscoped and never `--reverify`, still reporting exactly one drifted row;
`questions.md` Q2, Q3 and Q4 left to the repository owner.

## What this phase found

**Every class was wider than the finding that named it, and in three of the
four the extra instance was the more serious one.**

**A checker found the class boundary the round could not.** The
record-cell class was enumerated by running all four records through every
checker that reads a cell — `says_none`, `says_not_yet`, `depth_problems`,
`yes_or_no`, `CHECKER_RE`, `nobody_reason`, `runner_problem`, `resolves_to`,
`pass_checked`, `verdict_table`, `open_blocking`, `closed_with_a_fix`,
`run_reopened`, `ran_by`, `commissioned_fixes` — rather than by reading them.
Only the one cell was malformed. That is a clean answer and it cost one
command, where reading four records would have cost four and settled less.

**The trace class is three instances, and the round named one.** Walking git
over each record's field table and diffing the cells classifies twelve
changes: nine are pending rows being filled, which the ordering rule requires
and each record announces of itself, and three are corrections —
`round-1.md`'s `Needs a fix` count (19 of 231 → 20 of 235), `round-2.md`'s
`Contract changes` reach, and `round-3.md`'s `New units`. The first of those
was invisible to the round because it is a NUMBER inside a prose cell, and
nothing distinguishes it from the sentence around it.

That walk is now the case, and writing it exposed a weakness worth recording:
keying the check on the bare cell name would have let a deleted trace pass,
because every record names its own cells in its ordinary reasoning —
`round-3.md` says `New units` twice outside its trace. The marker
`CORRECTED IN PLACE` scopes it, and the mutation that proves the scoping is
removing one cell name from a trace while leaving the record's other mentions
alone.

**Three of the four recorded limits gave a false reason, and the two nobody
reopened were the two that had survived a round.** The round reopened two of
the four. Re-deriving all four found:

| The guard | Recorded reason | Re-derived |
|---|---|---|
| `says_not_yet`'s `none` prefix | duplicates `says_none`'s | **stands** — both True routes imply the prefix |
| `says_not_yet`'s separator boundary | the same sentence covered both | **false** — `says_none` answers True for a bare `none`, so a value arrives with nothing after the word. Dropping `not rest` alone: **20 red** |
| `normcase` in the path fallback | reachable only where CPython zeroes an inode | **conclusion stands, reason false** — `OSError` reaches the fallback on every platform; what is Windows-only is `normcase` differing from the identity |
| `seal_home`'s `SKILL.md` conjunct | needs a layout nothing constructs | **false, and it was a real hole** — the layout is constructible, the answers differ against a local-mode repository, and the mutation that survived every evidence suite now dies |

The shape the three false ones share is that each explained a guard through a
platform or a caller fact that is not what makes it unreachable. A mutation
battery cannot tell an unreachable guard from an unheld decision, so the prose
is what the next battery reads — which is exactly why a wrong one is worse
than a missing one.

**The `seal_home` hole was reached only by enumerating the class.** Nothing in
round 4 pointed at it; its own rider said *"if you open this resolver, build
that fixture"*, and opening the resolver is what the class demanded. It is the
clearest instance this branch has produced of §12 paying for itself.

**Both `# RIDER:` comments this branch left are gone.** Each stood in for a
case. The `says_not_yet` one argued that depth forbade the pin, and depth
refuses a new UNIT rather than a new assertion — so the pins went into cases
that already cover those units and no depth question arises. The `seal_home`
one asked for a fixture, and the fixture exists.

**A widened case can be an instance of the class it closes.**
`test_the_declared_limit_names_what_escapes_with_the_words_unchanged` was
written to close *a correction reaches one copy and not the rest* and covered
three of five copies. Widening it to five turned red on exactly the copy the
round named, and the failure was a markdown emphasis — `wider than *a
rewording*` — which is the whole class in miniature: one measurement, five
wordings, and the pin reading four of them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The claim that `says_not_yet`'s **two** guards duplicate `says_none`'s and cannot change the answer, from `chain_check.py#says_not_yet`, its `# RIDER:`, and `overview.md` | The docstring now separates them — the prefix guard duplicates, the separator guard does not and its `not rest` conjunct is load-bearing at 20 red. `overview.md` carries the four-limit table. Pinned by assertions in `test_a_reason_the_checker_does_not_recognise_passes`, behaviour and words both. Ledger row R7 carries the correction as a re-read clause |
| The claim that `normcase` in the fallback is reachable only where CPython zeroes an inode, from `evidence_check.py#skipped_by_narrowing` (two paragraphs) and `overview.md` | Both now say the fallback is reached by `OSError` on every platform and that `normcase` differs from the identity on Windows alone. Pinned by assertions in `test_an_inode_of_zero_does_not_fold_two_files_into_one`. Ledger row R3 carries it as a re-read clause, and `overview.md`'s `## Not verified` gains the Windows pairing with the CI leg as its answerer |
| The claim that `seal_home`'s `SKILL.md` conjunct needs a layout nothing constructs, and the `# RIDER:` carrying it | `test_a_copy_under_a_plugin_tree_without_a_skill_beside_it_is_still_vendored` builds that layout; the docstring states what the conjunct decides. `seal/ledger.md`'s Q2 row is re-stamped with the re-read, and its middle clause is Executed rather than merely asserted |
| The `# RIDER:` on `chain_check.py#says_not_yet`, and its argument that depth forbids the pin | Assertions inside `test_a_reason_the_checker_does_not_recognise_passes`, which already covers that unit. Depth refuses a new unit, not a new assertion, so nothing was owed a deferral |
| The widening paragraph from `round-3.md`'s `New units` cell, and the single reason it gave for two widenings | The record's trailing HTML comment, corrected: `says_not_yet` is round 2's own `New units` entry so that widening was forced, and `skipped_by_narrowing` came from phase 2 at `93c8b89` so the other was a choice |
| Nothing from `phases/phase-3.md`, `phase-5.md`, `phase-6.md` or `phase-7.md`, which keep sentences this phase makes false | Deliberate, and it is this branch's own rule: a phase record's prose is what that phase found and asserts about its own moment, where a round record's field rows are parsed and read as a finding surface |
