# Implementation Plan: survivors.md silences what it quotes

<!-- seal/specs/1790174139-survivors-md-silences-what-it-quotes/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-23 by the orchestrating session, on the owner's `automation` answer, when `smith` was spawned.

## Summary

Three phases, each closing one or two tickets, in the order of harm. Phase 1
takes the exemption file out of the sweep on both sides — the range's path
list and the corpus — which is both halves of one defect (#507 the range,
#308 the corpus) and the reason 29 of 36 rows on three pull requests were
never consulted. Phase 2 puts phase records in the same class (#460). Phase 3
gives a deeper exemption file its owner (#304). Phase 4 is the records: the
ledger re-stamp, the fragments, the follow-up rows, the closing memo, and the
branch's own sweep, which is the first real run of the fix on a range that
writes an exemption file.

The mechanism is the one the module already has. `records_a_past_round` is a
predicate on a path's shape, applied in `corrected` (the range) and `corpus`
(the pool); this work widens the class it names and touches nothing else in
the arithmetic. `wanted`, `carriers`, `weights`, `score` and `report` are not
edited.

## Technical context

- `skills/code-review/scripts/survivor_check.py#records_a_past_round` — the
  predicate, matched on `rounds` inside `specs` in the path's parts.
- `#corrected` — builds `paths` from `git diff --name-only`, filters by the
  predicate, then by `retired_directories`; returns `gone` (removed
  sentences) and `written` (n-grams of added sentences). `#wanted` returns
  `keep - written`. This is the range half: a committed `survivors.md` is in
  `paths`, its rows are added sentences, their n-grams are the survivors'.
- `#corpus` — `tracked(root, rev)` filtered by the predicate. This is the
  corpus half: the file is one more carrier of each quoted phrase, and
  `#weights` is `log2(F / df) / log2(F)`.
- `#OWNER_DIR` — `(?:^|.*/)(seal/specs/[^/]+)/[^/]+$`; `#whole_range` reads
  the owner off the exemption file's path and, where there is one, asks
  whether the range touches that directory. No owner, no question.
- `#WORK_ITEM_DIR` — `^((?:seal/)?specs/[^/]+)/`, used by
  `retired_directories`; anchored at the start, reads a prefix, so a deeper
  path matches it. Not a hole.
- The module docstring §*What is excluded, by construction rather than by
  list*, pinned by
  `tests/test_a_corrected_sentence_survives_elsewhere.py#test_the_docstring_names_both_sides_of_the_round_record_exclusion`,
  which requires `**A record of a past round.**` to be the first exclusion
  stated and that paragraph to name `pool`, `range` and `both sides`.
- `tests/…#test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
  — `PREDICATE = "records_a_past_round"`, `FILTERS_ITS_OWN_LIST = {"corrected"}`,
  `FILTERED_BY_ITS_ONLY_CALLER = {"tracked": "corpus"}`,
  `NAMED_EXCEPTION = {"whole_range": …}`. A new predicate name changes
  `PREDICATE` and nothing else; a second call site in either function goes
  red until classified.
- The fixture pattern: `build(repo, {path: text}, message)` and
  `run("--range", …, "--root", str(repo))`, with `RECORD`, `FOUND`,
  `REPAIRED` constants; lines 547–640 of the test module are the two cases
  phase 1 and phase 2 mirror.
- `.github/workflows/hygiene.yml` step *wording this branch removed is not
  still standing elsewhere*: passes every `seal/specs/*/survivors.md` as
  `--exempt` over `origin/<base>...HEAD` on a pull request into a release
  branch. Unchanged.
- The three real ranges and today's numbers: `spec.md` §*The measured state*.

**Failure scenario of the chosen approach, six months out.** A fourth kind
of file appears under a work item directory that quotes wording in order to
record it — a `corrections.md`, a per-phase `survivors.md` — and is not in the
predicate. It silences what it quotes exactly as `survivors.md` did, and
nothing measures it until a round notices a row that never prints. The
mitigation in this work is the class stated in one predicate with one
docstring paragraph per member, so the next member is one arm and one
paragraph rather than a rediscovery; what it cannot do is see the fourth kind
coming. The per-path-list test already refuses a new call site; nothing
refuses a new file kind, and this plan does not pretend otherwise.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Exclude `survivors.md` from the corpus only (#308's original one-liner) | Measured by #308's second comment: 0.758 → 0.757, one thousandth of a point, because the range half subtracts the phrase before the weight matters. The row stays silenced | Refused |
| Exclude it from the range only (#371's original shape) | Measured by #361's round 3 at `3673e46`: three survivors printed as `exempt` and two still reported, both of them the file's own quote cells; and the file still dilutes every phrase it quotes | Refused |
| Both sides, by the path's shape, in the predicate `corrected` and `corpus` already apply | A file kind outside the predicate is still silent (above). The per-path-list test keeps a new call site from escaping the predicate | **Chosen** |
| Read the exemption rows before `wanted` and add their quotes back to the search set | Turns the exemption file into an input of the search instead of a judgment on its result; a row's quote would then decide what is looked for, and a row with a wrong quote would search for the wrong thing. It also leaves the corpus half untouched | Refused |
| Exclude `seal/specs/` wholesale | `changelog.md`, `overview.md`, `spec.md` and the ledger fragment are live statements; #423's pass found one false fact standing in three of them (#460 §*Not this*) | Refused |
| Exclude only the quoted original inside a correction marker in a phase record (#460's narrower answer) | Needs a marker syntax and a parser the repository does not have; does nothing about the dilution half; a phase record's `## What this phase was asked` quotes without any marker | Refused |
| Leave phase records in and pay an exemption row per quoting record now that rows work | Each row is the escape used for the thing the docstring says it is not for, and the record still dilutes every phrase it quotes. #460 measured two of four places in one pass being this | Refused |
| Refuse an ownerless declaration outright with a new printed state | Closes #304 but also breaks the documented hand-run case, a file outside any work item directory; and the deeper file is not ownerless once the prefix is read at any depth | Refused |
| Widen `OWNER_DIR`'s tail so the owner is read at any depth beneath `seal/specs/<id>/` | A file outside `seal/specs/` keeps the old reach, as documented and by design | **Chosen** |
| Take #366 here as a fourth phase | Adds `round_record.py`, work item A's file, to this branch's surface while A is being built in parallel, for a ticket that is not about the survivor sweep | Refused; `questions.md` Q1 |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The exemption file is out of the sweep on both sides** (#507, #308). The predicate names `survivors.md` directly under a `specs/<id>/` directory; `corrected` and `corpus` apply it; the docstring gains its paragraph; `PREDICATE` follows the name. Cases S1, S2, S3, S4, S9 (first extension), S10, each seen red first. The `seal/follow-up.md` row for the range half is deleted. The S5 table is executed over the three real ranges and written into `phases/phase-1.md` beside today's numbers | The new cases red at `cdc8d182` and green after, `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py` with the count read directly; S5's three runs with `--exempt`, without, and with the file deleted in a probe, exit codes read directly; the changelog fragment entry | af5c4044 |
| 2 | **A phase record is a record** (#460). The predicate names `phases/` under a `specs/<id>/` directory; cases S6 (three), S9 (second extension); the docstring paragraph; the `seal/follow-up.md` row for what this gives up, the repository owner named. S5 re-executed, because the three items' phase records leave the pool | The three cases red first; the module's case count read directly; S5's numbers written into `phases/phase-2.md` beside phase 1's | |
| 3 | **A deeper exemption file has an owner** (#304). `OWNER_DIR`'s tail; case S7 (deeper, and the layout position unchanged); S8's enumeration of every path-reading regular expression written into `phases/phase-3.md` | S7 red first; the module's case count; the enumeration read | |
| 4 | **The records.** `evidence-check --reverify .` over the drifted rows named in `spec.md` §*Data & interfaces*; the ledger fragment's new rows; `overview.md` with its `## Not verified` table; `questions.md` Q2–Q4 filled by the measurements phases 1–3 made; the branch's own sweep (S12) and its `survivors.md` if the sweep reports the folded docstring copies in `docs/review-chain-spec.md` | `bin/evidence-check --strict .` exit 0; `bin/survivor-check --range origin/release/v0.15.0...HEAD --exempt <this item>/survivors.md` exit 0 with every `exempt` line naming a row; `bin/unverified-check --baseline origin/release/v0.15.0 seal/specs/` exit 0; every exit code read directly, never through a pipe | |

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

### What each phase carries, per `CONTRIBUTING.md` §*What a change to a gate must carry*

| Phase | Test seen red | Failure direction | Prompt budget | Platform honesty |
|---|---|---|---|---|
| 1 | S1 at exit 0 with no `exempt` line; S2 at a halved score naming the weaker phrase; S3 with two different reports; S4 naming the file as a source | The gate **finds more**: survivors that were silenced are reported and then excused by name. Every open branch of 0.15.0 that carries a `survivors.md` may see new reports at its next CI run, which is the milestone's stated reason this lands before #526. The wrong deny is a printed line naming a row that already exists; the wrong allow is what is there today | zero | a path shape read from `git` output, which uses `/` |
| 2 | S6's three cases | The gate **finds less** in one place: a phase record carrying old wording is no longer reported, and the #423 phase-4 shape with it. Cheaper because every measured instance (#460: two of two) was the record doing its job, and the excused alternative dilutes the survivors that matter. Named in `seal/follow-up.md` | zero | same |
| 3 | S7 with the deeper file excusing a range it does not own | The gate **refuses more**: a declaration one directory deeper is asked the ownership question and printed `not yours` when it fails. The wrong refusal is one printed line; the wrong allow is a silent whole-range excuse | zero | a path pattern; `--exempt` paths may be absolute, and the pattern is not anchored at the start for that reason |

### Overlaps with work items A and C

Work item A (`fix/503-…`, `round_record.py`, `chain_check.py`, the review
record) and C (`fix/536-…`, the release scripts) are being framed or built
in parallel. Measured 2026-09-23 by `git diff --stat` against
`release/v0.15.0`: A's branch holds `routing.md` alone and C's holds its SDD
set, so neither has touched a file this item touches yet. The files where a
collision is possible by what each item is about:

- `seal/ledger.md` — all three re-stamp rows with `--reverify`. Hunk by hunk,
  both sides read, never `--ours` or `--theirs`.
- `seal/follow-up.md` — this item deletes one row and adds one; A or C may do
  the same. Text-level, resolvable by reading.
- `docs/review-chain-spec.md` — this item does not touch it; A may.
- `skills/code-review/scripts/round_record.py` — this item does not touch it
  unless Q1 is answered *here*, which is why the default is *A*.

## Operational impact

No migration, no new dependency, no environment variable, no change to the
command line or to `hygiene.yml`. **One compatibility note for every branch
already open against `release/v0.15.0`:** once this lands, a `survivors.md`
committed on such a branch stops silencing what it quotes, so the branch's
next CI run may report survivors it did not see before — each of which is
then either excused by a row it already has (printed as `exempt`) or is a
real report. That is the gate finding what it was supposed to find, and the
milestone orders this item before #526 for exactly that reason.
