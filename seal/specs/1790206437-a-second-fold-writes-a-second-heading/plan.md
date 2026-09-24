# Implementation Plan: a second fold writes a second heading

<!-- seal/specs/1790206437-a-second-fold-writes-a-second-heading/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-24 by the orchestrating session on the owner's `automation` answer, when `smith` was spawned.

## Summary

Five phases, in the order the risk is retired. Phase 1 repairs the measured
instance in `seal/ledger.md` and plants the real-tree case that is red before
it, because a hygiene case red on every pull request is the one thing this
branch must not leave for the next. Phase 2 makes the fold join a section it
already heads, keeps the first date, and gives `--check` the refusal, each
case red first. Phase 3 brings the two `round_record.py` sentences to the rule
`same_run` implements and pins the written one. Phase 4 writes the reviewing
convention #366's second half comes down to, in the three places the
reviewer copies from, pinned. Phase 5 is the verify phase: the fragment rows,
the changelog fragment, `overview.md`, the survivor sweep over the range, and
the ledger checker — the broad gate is the sealer's.

## Technical context

**`.github/scripts/fold_ledger.py`** (read whole, 2026-09-24 at `9f846733`).
`section(version, date, entries)` builds `## <version> — <date>` first and
one marked `###` block per fragment; `append(ledger_text, block)` puts it
below everything; `main` computes `date = args.date or <today UTC>` and calls
both. The only re-run guard is `folded()`, which refuses a fragment whose
marker already stands in the file. `--check` reads fragments left, open
evidence-todo rows, and counts `MARKER_LINE_RE` — nothing reads `## ` lines.
Every printed path goes through `under()` and the `/`-joined constants
(round 1's Windows finding of `1788326734`); the new arm prints no path.

**`.github/scripts/gather_changelog.py`** is the mirror, and #289's fix there
is the template for phase 2: `heading_re`, `section_heading`,
`existing_date`, `insert`'s two arms, and `main`'s `found`/`heading`/`date`
lines. One difference matters: the gatherer inserts a new section at the
top and the fold appends at the bottom, so the fold's existing section is
normally the last `## ` in the file — `insert` still walks to the next `## `
so a heading appended later (S4) does not break it.

**`seal/ledger.md`** at `9f846733`: lines 1763–1766 are `''`,
`'## 0.9.3 — 2026-09-08'`, `''`, the marker for `1788890000`. Deleting 1764
and 1765 leaves one blank line between `1788873640`'s last row and the
marker, which is the shape every other work item boundary in the file has.
The rows the second fold wrote (`1788890000`'s) are byte-identical either
side, so `evidence-check` totals do not move.

**`tests/test_the_ledger_fragments_fold_at_release.py`**: the `tree` fixture
writes the ledger head, two fragments and a drained evidence-todo; `fold()`
asserts the heading and a marker landed; `run(*args, root=)` drives the
script; `ledger(tree)` and `fragments_left(tree)` read the state. A second
fold case writes a third fragment after `fold(tree)` and runs
`run("--version", "0.4.0", "--date", "2026-09-16", root=tree)` — the
gatherer's case is the pattern, name for name.

**`tests/test_release_hygiene.py`**: `duplicated_version_headings(text)`
already reads any text; `read_text("CHANGELOG.md")` is how the real-tree
case opens a file. The ledger case is the changelog case with the path
changed and the message naming the ledger.

**`skills/code-review/scripts/round_record.py`** (`:347-402` and
`:4263-4290` read): `kept_broad_gate` and `same_run` are the rule;
`new_broad_gate_file` writes the comment as one string literal; `seal`
calls it when `seal_home` returns no round (a `straight to the PR`
declaration). The seal module's `run_seal(repo, value)`, `declaration(review=)`,
`write`, `commit`, `ITEM`, `GATE_FILE` build the direct-home state in three
lines (`test_seal_writes_a_file_where_no_round_record_exists` is the model).

**`tests/test_the_report_standard_is_one_in_three_places.py`**: `CARRIERS`
holds the four files the worked row is pinned in; `WARDEN` the one file some
sentences are pinned in alone; `flat(*parts)` collapses whitespace. The
convention sentence is pinned across the three reviewer-facing carriers
(`CARRIERS[:3]`, by name, not by slice), and a new constant holds the
sentence so the three files and the case cannot drift apart.

**The ledger rows this work moves** (S15): in §0.4.0 of `seal/ledger.md`,
the rows anchored on `.github/scripts/fold_ledger.py`'s `section` and `main`
(lines 297, 302, 303, 311, 312 at `9f846733`) and on `append` if `append`
changes; in §0.15.0, A9 on `skills/code-review/scripts/round_record.py`'s
`kept_broad_gate`. The stamps those rows carry are the ledger's and are not
repeated here: `evidence-check`'s records arm reads a short path beside a
hash as a file it cannot find, once the work item has a fragment. Each claim
still holds after the edit and is re-read, given a dated note and re-stamped
with `evidence-check --reverify .`; none is re-pointed or removed. Work items
A and B of this milestone also re-stamp rows in this file; a conflict is
resolved hunk by hunk with both sides read (`CLAUDE.md`).

**What breaks in six months.** The fold and the gather now carry the same
three helpers under the same names in two scripts, and an edit to one is
not an edit to the other. That is the cost accepted here: the two scripts
are already siblings by design (`fold_ledger.py`'s docstring says so), a
shared module under `.github/scripts/` is mechanism a patch release does
not add, and #547 rewrites the fold's placement next, at which point the
helpers diverge on purpose. The other failure is the convention sentence
going stale in one carrier, which S13's pin turns into a red case rather
than a fourth disagreement.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#540 · refuse a second fold outright** (*version already folded*, exit 1) | The red-release shape has no path but a hand edit; the doubled `0.9.3` in the tree is what that path produces | rejected — join, as the gatherer does |
| **#540 · the refusal in `tests/test_release_hygiene.py` alone**, the exact #289 mirror | #540 and #547 both say `--check` is where the refusal belongs; a release pull request is where a doubled heading is written and `--check` is the arm that runs there | rejected in favour of both — one reader in the script, one real-tree case in the suite |
| **#540 · the refusal in `--check` alone** | The suite runs on every pull request and locally; `--check` runs only for a pull request into `main`, so the branch that adds the refusal would not itself be refused | rejected in favour of both |
| **#540 · leave the doubled `0.9.3` for #547's restructure** | S2's case is red on every pull request until D lands, or is not planted, and a case that passes over the defect it is for is a counterfeit | rejected — phase 1 |
| **#540 · repair by moving `1788890000`'s section under the first heading** | The sections are adjacent; a move is a larger hunk for the same result | rejected — delete two lines |
| **#540 · a shared `.github/scripts/_sections.py` for the three helpers** | Mechanism a patch release does not add; a new module to import from two scripts whose tests drive them by `subprocess` | rejected — mirrored helpers, named the same |
| **#540 · edit the `date = args.date or …` line to `existing or args.date or …`** as the gatherer did | `1790173209`'s `survivors.md` quotes that line; the sweep over this range would report the gatherer's line as a survivor of the removed one, the idiom class step A (#543) is fixing in parallel | rejected — decide the kept date beside the line; Q4 measures the sweep anyway |
| **#542 · pin the comment through `GATE_CARRIERS` over `round_record.py`'s source** | Pins the source rather than the written file the two rounds asked for; changes A11's *eight documents* count | rejected — a seal-module case over the written `broad-gate.md` |
| **#542 · leave the comment unpinned and say so at `GATE_CARRIERS`** (the ticket's second option) | `agent-contract` §14: text a tool writes for a person is pinned in the commit that changes it; `1790174138`'s plan promised a red test rather than a stale sentence, and the ninth carrier is the stale sentence it did not catch | rejected |
| **#366 · a finer `depth_two`** mapping each added unit to what it asserts | A gate change with a heuristic (names referenced, not what is asserted), the four answers and a false-positive argument; the milestone says no design | not here — Q1, the owner, 0.16.0 if wanted |
| **#366 · say it in `depth_two`'s refusal message** | The refusal arrives at `close`, after the report is written; the smith cannot split a finding, and rewording a refusal line is a gate change the spec reserves to the owner | rejected |
| **#366 · the sentence in `templates/sdd-round.md` too** | The template's comment is the record's shape, not the reviewer's rule for writing a `Location`; the reviewer copies the table from the two files the report-standard module names | rejected — three carriers |
| **#366 · defer the whole ticket again** | The ticket has been open since 0.11.x with its cheaper answer written in it; the three cases shipped; the milestone lists it as a sentence | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified. The
row is the whole task; there is no prompt per phase (`agents/framer.md`).
Each phase closes with `phases/phase-N.md` from `templates/sdd-phase.md`,
the ledger rows drafted during the phase written in one pass, a commit, and
`python3 skills/evidence-check/scripts/evidence_check.py --strict .` read
directly (§1).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The measured instance.** `tests/test_release_hygiene.py#test_no_version_heads_two_sections_of_this_ledger` planted beside the changelog case, run first against the tree as it stands and its red output copied into the phase record (`0.9.3 twice, at lines [1673, 1764]`); then `seal/ledger.md` lines 1764–1765 removed (S1); `evidence-check` totals before and after; `fold_ledger.py --check` exit 0 with the same count | `bin/test tests/test_release_hygiene.py -q`, exit read directly; the totals line of `evidence-check` before and after S1, equal; `git diff --stat` on the ledger reads two deletions | d08c671a |
| 2 | **The fold joins.** `section_heading`, `insert`, `doubled_versions` (NAME NOT IN TREE until this phase adds it) in `fold_ledger.py`; `main`'s kept date, dry-run heading, `(appended into the existing section)` message and the `--check` refusal; the module docstring; one sentence in `docs/release-checklist.md` §2. Cases S3–S8 in the fold module, each seen red first (S8's real-tree red against `git show 9f846733:seal/ledger.md` in a scratch root). Rows F1, F2 drafted; §0.4.0's `section`/`main`/`append` rows re-read and re-stamped | `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_the_changelog_is_gathered_at_release.py tests/test_release_hygiene.py -q`; `uvx ruff check` and `uvx ruff format --check` over the script and the test module; `fold_ledger.py --dry-run --version 0.15.1` over this tree prints a fresh heading (no 0.15.1 section exists) | deade859 |
| 3 | **The two sentences, and the class.** `new_broad_gate_file`'s last sentence and `kept_broad_gate`'s count sentence take the round-3 report's blocks verbatim; `test_the_written_broad_gate_file_says_a_same_run_re_seal_replaces_its_entry` (NAME NOT IN TREE until this phase adds it) in the seal module, red first on both halves; the two further carriers `spec.md` S11b names read against the template's clause and reworded where they state the replaced rule, the judgment per carrier in the phase record; A9 re-read with a dated note; A11 corrected in place (Q3); rows B1, B2 drafted | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_broad_gate_cell_keeps_every_run.py -q` and `bin/test tests/test_the_fixes_close_the_record.py -k broad_gate -q`; ruff over `round_record.py` and the test module | 171feacf |
| 4 | **The convention.** One sentence in `agents/warden.md`, `skills/code-review/SKILL.md` §*Findings format* and `docs/review-chain-spec.md` §*The depth in `New units`*, held in one constant and pinned by `test_every_carrier_tells_the_reviewer_to_split_a_finding_that_sits_at_two_depths` (NAME NOT IN TREE until this phase adds it), red with the sentence deleted from any carrier; row D1 drafted | `bin/test tests/test_the_report_standard_is_one_in_three_places.py tests/test_docs_line_wrap.py tests/test_the_record_is_held_to_the_floor_and_the_depth.py -q`; `git diff --stat` shows no `.py` under `skills/code-review/scripts/` in this phase | dea6f051 |
| 5 | **Verify.** The fragment `seal/ledger/1790206437-….md` written in one pass from the drafted rows; `changelog.md` (three entries); `overview.md` opened with the divergences met and `## Not verified` naming the sealer for the broad gate; `survivor-check --range origin/release/v0.15.1...HEAD` with a `survivors.md` row for anything reported (Q4); `evidence-check --strict .` exit 0; `git diff --stat` against the base read against S14's list | executed, each exit read directly; the hand-back carries the module runs, the red-first evidence per case, and the suite labelled `unverified — the sealer` | |

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

- **A release's fold is re-runnable.** After this ships, running
  `fold_ledger.py --version X.Y.Z` a second time for a version the ledger
  already heads joins that section and keeps its date, and `--check` refuses
  a ledger that heads a version twice. The release checklist's §2 says so
  beside the gather's sentence.
- **`seal/ledger.md` changes shape by two lines** (one `0.9.3` heading and a
  blank), and every row is byte-identical. A parallel branch re-stamping rows
  in §0.9.3 merges without a conflict unless its hunk touches lines 1763–1766.
- **Every `broad-gate.md` written from now on carries the corrected
  comment.** The eleven already committed keep the old sentence; they are
  records of the runs that wrote them and are not rewritten (the survivor
  sweep leaves records out on both sides).
- **#547 rebases onto this branch.** What it inherits in `fold_ledger.py` is
  three additions with the gatherer's names and an unchanged date line.
- No migration, no new dependency, no new environment variable, no change to
  any workflow file. Python floor stays 3.12.
