# Implementation Plan: a ledger row that will not parse is counted

<!-- seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-25 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

A ledger coordinate that `ANCHOR_RE` and `OLD_COORD_RE` both refuse is in no
finding list today, so it is counted nowhere and the total reads clean. This
plan gives it a verdict of its own, `MALFORMED`, graded like `OLD-FORMAT`:
named, counted on every totals line even at zero, exit 2 under either
reading, a `LEFT` line from `--reverify`, and a block from the commit
advisor. It first repairs the five rows in this repository that are skipped
right now, so the arm lands on a tree it passes. #322 needs no code: it was
fixed in `97e29b7a`, and the pull request closes it with the grounds in
`spec.md` item 9.

## Technical context

All coordinates read at `ca2afdb9`.

- `skills/evidence-check/scripts/evidence_check.py#check_ledger`: calls
  `check_text(unquoted(text), …)` and then `old_format_rows(text)`. The new
  function is called third, the same way.
- `evidence_check.py#old_format_rows`: the model to copy. It reads table
  rows only, through `unquoted`, and blanks new-format anchors before it
  scans.
- `evidence_check.py#main`: `totals` holds five keys, and the per-ledger and
  `total:` lines are f-strings that print `old-format` at zero on purpose.
- `evidence_check.py#exit_code`: `OLD-FORMAT` returns 2 first. The case in
  `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` builds a
  `zero` dict with the five keys, so indexing `totals["MALFORMED"]` there
  raises until that dict gains the key. Update the case; do not reach for
  `.get` to dodge it.
- `evidence_check.py#reverify`: walks `ANCHOR_RE` over `unquoted(text)` and
  prints `LEFT` for an unreadable ledger, returning 1.
- `evidence_check.py#unescape`: already turns `\"` into `"`, which is what
  makes escaping the repair for four of the five live rows.
- `hooks/evidence-advisor.py#failing_rows` and `#main`: a two-verdict filter
  and one printed block per verdict.
- The comment above `VENDORED_FENCE_RE` explains why `evidence_check.py`
  must load alone (`evidence-ci` vendors it into `tools/`). The cell splitter
  follows the same constraint.

**What breaks in six months.** A repository that renames the `Code grounds`
column (to `Grounds`, say) takes that table out of the arm, and a malformed
coordinate there is silent again. The arm keys on the template's column name
because the only alternative the probe measured, scanning whole rows, refused
seven correct things in eight (see *Alternatives*). Second: an installing
repository with a malformed row, or a row whose grounds cell holds only prose,
goes red on the update that ships this. That is intended, and Q1 is where the
owner can soften it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Call it `BROKEN` | `BROKEN` means *the major unit is not there, go edit the ledger*, and its detail machinery (the destination scan, `identical content at …`) has nothing to scan for when no unit was named. `docs/the-evidence-ledger.md` reserves it for the major level, and `old_format_rows` already refused to fold the other unparseable shape into it "because the remedy differs" | rejected |
| A fourth state named `UNREADABLE`, as #299 suggests | `UNREADABLE` is already the records arm's verdict for a record or directory that could not be opened (`SKILL.md` *Verdicts*), and `check_ledger` says "ledger unreadable" for a file. One word, two meanings | rejected, and named `MALFORMED` |
| Refuse at write | The rows already in the tree stay unchecked, and five are there now. #299's table says so | rejected |
| Widen `ANCHOR_RE` | Moves the boundary and leaves the silence past it. #299's first comment | rejected |
| Scan every cell of every table row for a `#…@…` the pattern refused | Measured by the framer's probe over this repository's ledgers: 8 leftovers, 7 of them correct text (the template's notation row, path-less shorthand in Notes cells, a quoted example of the bug in a Notes cell, notation in a Clause cell). It would turn every ledger started from `templates/ledger.md` red on the template's own notation row | rejected |
| The `Code grounds` cell, rule (a) only: a leftover `#` or `@` | Misses a row whose grounds cell cites nothing at all, which the owner's second comment on #299 puts in the class ("any coordinate cell the anchor pattern rejects, whatever the reason") | rejected alone |
| **The `Code grounds` cell, rules (a) and (b)** | Measured on this repository: exactly the five live rows and nothing else. The risk is a renamed column (above) | **chosen** |
| `--reverify` heals `@0` by computing the hash | Healing means deciding what a coordinate the parser refused was meant to say. Only one of the five shapes (a well-formed path and locator with a bad hash) has a single reading, and the suite already pins the workflow that does the same thing: write `@00000000`, run `--reverify` | rejected; `--reverify` names and leaves |
| Grade like `DRIFTED`: exit 1 lenient, 2 under `--strict` | A lenient reader exits 1 and says the strict reading would refuse, so it is not silent. But `OLD-FORMAT` chose exit 2 under both, for the same silence | Q1's alternative; the default is exit 2 |
| Print and count only, exit 0 | The count moves on a green build, which is still the build #299 is about | rejected |

## Phases

Vertical slices. Each phase ends with something runnable and verified, and
each one's rows go into `seal/ledger/1790297087-a-ledger-row-that-will-not-parse-is-counted.md`
at its boundary.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The five live rows parse.** Each row in `spec.md` *The live instances* is re-read against its code; its coordinate is corrected (`\"` for the four quoted locators, a real unit in place of `<module>`), `--reverify` fills the hash, and the row takes a `Corrected <date>` note saying the coordinate never parsed (#299), which is the marker `correction-check` reads. A claim that no longer holds is corrected or taken out under `CLAUDE.md`'s rules instead. The `\"` escape is written into `templates/ledger.md`, `skills/evidence-check/SKILL.md` and the comment above `ANCHOR_RE` | `bin/evidence-check --strict .` before and after: `ok` rises by the anchors the repair made readable, and `0 drifted · 0 broken` both times. Both totals go in `phases/phase-1.md` | a77eed92 |
| 2 | **The `MALFORMED` arm.** The function beside `old_format_rows`, called from `check_ledger`; the key in `totals`, and `· N malformed` on both totals lines, printed at zero; exit 2 in `exit_code`; a `LEFT` line from `--reverify` with exit 1. The `SKILL.md` verdict row and the `--reverify` bullet. `seal/follow-up.md`'s #299 row goes | Cases S1–S10 of `spec.md` in `tests/test_a_row_points_by_content.py` and the lenient-run case file, each seen red against the phase-1 checker (§15). The modules that run the checker over a fixture repository, run at the boundary (`tests/test_a_row_points_by_content.py`, `tests/test_evidence_check.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py`, `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py`, `tests/test_gates_do_not_fail_open.py`). S12: `bin/evidence-check --strict .` over this tree reads `0 malformed`. And the arm's own answer to #299's open question: the three ledger files as they stood at `ca2afdb9` (`git show ca2afdb9:<path>`) copied into a scratch root and read with `--ledger`, which should name five `MALFORMED` rows, the framer's probe count | d78a73ad |
| 3 | **The commit advisor names them**, and the work item closes. `failing_rows` takes `MALFORMED` into its filter, its docstring says so, and `main` prints a block with the remedy. Then `seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/changelog.md` and `overview.md` | S11: a case in `tests/test_dispatch.py` beside `test_a_commit_with_a_pre_anchor_ledger_is_pointed_at_the_migrator`, and the docstring pin in `tests/test_a_row_points_by_content.py` extended to `MALFORMED`, both seen red first. `tests/test_dispatch.py` run whole at the boundary | b94697c3 |

The full suite, lint and typecheck are the sealer's, once, after the review
rounds settle (contract §2). No phase runs them.

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **A repository that installs the plugin can go red on update.** The
  plugin's `bin/evidence-check`, the commit advisor and the broad gate all
  exit 2 on a malformed row that passed before, and so does a repository's
  vendored CI copy once `/specseal:evidence-ci` re-vendors it. The output
  names each row and its remedy. The changelog fragment says this in its
  first line, because it is what an updating user meets.
- No migration, no new dependency, no new environment variable.
- **`evidence_check.py#ANCHOR_RE` and `#resolve_unit` stay as they are**:
  names, pattern, signature, return shape. Work item B (#603) loads this
  file by path and calls both, so a change to either breaks a sibling chain
  at its squash. No phase here needs to touch them. A build that finds it
  must adds a new unit beside the old one, leaves the old one in place, and
  records that here.
- The `total:` line gains a trailing field. `broad_gate.py#LEDGER_RE` reads
  only the unchanged prefix. Any outside parser anchored to the line's end
  would see the change.
