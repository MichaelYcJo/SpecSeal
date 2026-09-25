# Feature Specification: how chain_check reads a record (#598 instances 1 and 4, #529)

<!-- seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/spec.md
Work item A of `release: 0.15.4` (milestone 46). A patch release: fixes to an
instrument, no new gate. Two of the three changes RELAX a refusal and the third
makes an existing rule hold in a shape it was already written for; none adds a
refusal. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/commit-review-gate-spec.md`, the declaration table, row `through the review chain`: *"A record this pull request does not touch keeps every requirement except reachability: its commits are expected to be gone, and the review it records was enforced at the pull request that added it"* | Instance 1. A record whose exact content the base's own history already held at that path was added by an earlier pull request. So the review it records was enforced there, and this pull request makes no new claim about where its commits are |
| `docs/review-chain-spec.md` §*When the record was written*, table row *"a record with no adding commit in `<baseline>..HEAD`"*: *"The same no claim the reachability requirement already makes for a record the pull request does not touch"* | Instance 1's class reaches `written_late` too. That arm defines its own *no claim* by pointing at the reachability arm's, so the two cannot take different answers for one record |
| `docs/review-chain-spec.md` §*When the record was written*, table row *"a record DELETED and re-added on the branch"*: *"judged on the latest add"* | #529. The rule is already written. `added_on_branch` fails to meet it once a merge sits between the two adds, and (measured in framing) under committer-date skew as well |
| `skills/code-review/orchestration.md` §*Orchestrator: the pull request opens before round 1, and a phase is re-run*: *"A check that is red for following the document beside it is a check people learn to skip"*, and the #296 paragraph that made the missing-record arm draft-aware | Instance 4 takes the shape #296 gave the missing-record arm: print in a draft, fail at ready |
| `docs/round-record-spec.md` §*`Pass` has to be checked*: the draft row, *"A draft is not a request to merge, and a review still running has to have somewhere to be"*, and the row judging an invisible state as **ready** | What the draft excuse is. The strict reading at a ready or unknown pull request is unchanged |
| `docs/round-record-spec.md` §*`Fixes checked by`*: *"The draft excuse does not reach this row. `Pass` is excused in a draft because a review still running has not reached its verdict; a record naming a checker it does not have is wrong at every stage of a run"* | The sentence this work narrows, and the grounds for narrowing it rather than overturning it (see Scope, instance 4) |
| `CLAUDE.md` §*a change writes fragments, never the shared file* and §*commit early* (ledger half) | Rows this work adds go in `seal/ledger/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge.md`. Rows it drifts in `seal/ledger.md` or `seal/releases/*.md` are re-read and re-stamped in the file they are in |
| `skills/settle/SKILL.md` §2, the standing-statement shape (bold rule, grounds, one `Enforced by:` line) | Every `docs/` statement this work edits keeps exactly one `Enforced by:` line, and the new cases join the line of the statement they pin |

## Scope

### In

**1. #529: the latest add is found across a merge and under a skewed clock.**
`chain_check.py#added_on_branch` passes `--full-history --topo-order` to its
`git log --diff-filter=A`. This makes the code meet the rule
`docs/review-chain-spec.md` already states.

Measured in framing, executed in scratch repositories built by one Python
probe (git 2.54.0, deleted afterwards):

| Shape | default | `--full-history` | `--full-history --topo-order` |
|---|---|---|---|
| S1: a side branch deletes the record and re-adds the SAME content, merged `--no-ff` (#529) | early add only | late, early | late, early |
| S1b: the same with DIFFERENT content | late, early | late, early | late, early |
| S2: the feature branch adds the record, then merges its advancing base | the add | the add | the add |
| S3: `--no-ff` merge of a side branch that added the record | the add | the add | the add |
| S3b: the side adds it, the feature branch commits a fix later in time, then merges | the add | the add | the add |
| S7: S1, with the side branch's commits dated EARLIER than the early add | early add only | **early, late** | late, early |

Two conclusions follow, and both were open before this frame:

- **Answer to #529's "not measured" clause:** in S2, S3 and S3b,
  `--full-history` does not list the merge commit as an `A`. `git log` does
  not diff a merge without `-m`, so `--diff-filter=A` never matches one.
- **`--full-history` alone is not enough.** Under date skew (S7) the date
  order puts the early add first, and `found[0]` takes it. The assumption
  *"the first line is the latest add"* rests on two things, the simplification
  and the order. `--topo-order` shows a descendant before its ancestor, and
  the late re-add descends from the early add in every delete-and-re-add
  shape. So the class has two members and both are fixed (§12).

**2. #598 instance 1: a record restored byte-for-byte from the base's
history is not this pull request's claim.** A new predicate answers one
question: does the blob `rel` holds at HEAD (in the working tree under
`--worktree`) appear at that same path in any commit reachable from the merge
base? It is answered by one `git log --full-history --find-object=<blob>
<fork> -- <rel>`. A non-empty answer means the record was restored. The
predicate names the commit it found, for the printed line.

It is asked by the two arms whose claim is about *this pull request's* add,
and by no other:

- **Reachability** (`main`, where `refs` is decided). A restored last record
  gets `refs = None`, the same *no claim* an untouched record gets. The item's
  printed line says it was **restored** from `<commit>` in the base's history.
  It does not say "not changed by this pull request", because the path IS in
  the diff. The comment already above that line warns about exactly that
  mistake.
- **`written_late`.** A restored record returns `[], []` before
  `added_on_branch` is asked. The pass is silent, like the table row it joins
  (*"no adding commit in `<baseline>..HEAD`"*). It asks this of a record the
  pull request does not touch as well, because a branch whose own record was
  squashed into the base and which then merged the base in still has that
  record's add in range, and those bytes are the base's claim now, whichever
  pull request put them there (round 1, ⬜ 4).

Everything else is still read on a restored record, just as it is on an
untouched one (`test_a_merged_record_is_still_read_for_everything_else`):
`Pass`, the verdict table, `Fixes checked by`, the fix surface, the floor,
`Ran by`, `Fix range`, the doubled grounds and the broad gate.

Measured against the real case (executed, read-only git on this clone): PR
#597's head `dc3304ac` and its fork `6256bbc8` from `release/v0.15.3`. All
four `1788395377-the-release-guard-globs-one-place/rounds/round-*.md` are `A`
in `fork...head`. Each blob matches `main`'s, and `--find-object` finds each
one in the fork's history at `a211a5d7` (added) and `c52e8350` (retired). So
the predicate turns #597's four refusals into four restorations.

Measured in the scratch repositories: content edited after the restore (S4,
blob `Y`) finds nothing, so an edited record is still the pull request's
claim. A blob that entered the base's history only through a merge's second
parent (S5) is found.

**3. #598 instance 4: `Pass` beside `nobody` on the last record prints in a
draft and fails at ready.** In `checked_by`, the one refusal for a checked
`Pass` beside `nobody — <why>` on the last record (work item at or after
`STRICT_FROM`) becomes a notice when the pull request is a draft. Every other
refusal in `checked_by` stays in force at every stage. That covers the absent
row, a self-naming or earlier `round-N`, a `round-N` git does not carry, one
that reviewed the same or an earlier commit, `no fixes to check` beside a fix,
a bare `nobody`, and a word outside the vocabulary. `strict` reaches
`checked_by` from `main` the way it already reaches `check_round` and
`broad_gate`.

The grounds for narrowing the round-record-spec sentence rather than
overturning it are these. Its reason, *"a record naming a checker it does not
have is wrong at every stage"*, is true of every refusal listed above. It is
not true of `nobody — <why>` in the window. That cell is the honest state
between `round_record.py close` ticking `Pass` and the verifying round's
record committing: no later round exists yet to name. What makes the pair
refusable is the `Pass` half, and `Pass` is exactly what a draft is excused.
Executed in framing: the GitHub timelines of #587, #588 and #595 (three of the
six PRs named) each show every round commit before `ready_for_review`. So the
window lies inside the draft, and pressing *Ready for review* re-runs the
check. `.github/workflows/hygiene.yml` lists `ready_for_review` in its
`types`.

The owner's answer to Q1 of work item `1788212517` stands: *refuse it, for
work items begun after the rule*. The refusal still fires at every ready
pull request and at every run with no readable pull-request state.
`round_record.py close`, which runs the check with no payload, is one of
those. What changes is that a draft stops painting the pull request red for
the step the orchestration document orders next.

**4. Documents and records that state the changed behaviour**, in the same
commits as the code (§14):

- `chain_check.py`: the module docstring (the *"is anything required of this
  record at all?"* paragraph, and the *"The draft excuse does NOT reach this
  row"* paragraph), plus the docstrings of `check_round`, `checked_by`,
  `added_on_branch` and `written_late`
- `docs/commit-review-gate-spec.md`: the `through the review chain` row
  (restoration)
- `docs/review-chain-spec.md` §*When the record was written*: the delete and
  re-add row (across a merge and a skewed clock, and its *what it costs*
  sentence narrowed to a restore that happens within the branch), and a new
  row for a record restored from the base's history. Also §*Two records* (the
  last-record refusal is at a ready pull request)
- `docs/round-record-spec.md` §*`Fixes checked by`*: the draft sentence
  narrowed, the `nobody — <why>` table row, and the `Enforced by:` line
- `skills/code-review/orchestration.md` §*the pull request opens before
  round 1*: the *"It is red once more …"* sentence replaced
- `tests/test_the_rules_have_one_owner.py::test_the_release_leg_is_red_again_until_the_verifying_rounds_record_commits`,
  which pins that sentence and is rewritten to pin its replacement
- the ledger fragment, the drifted rows, and the changelog fragment
  `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md`

### Out, and why

- **#598 instance 2** (`settle --retire` removes a kept directory whose
  closure has not reached `main`). Moved to #602, work item C.
- **#598 instance 3** (the survivor sweep reads a removed ledger row's cells
  as removed wording). Moved to #603, work item B.
- **`chain_check.py#load` and the `try`/`except` that calls it in `main`.**
  These belong to #590, work item C, which edits this file in parallel. A
  leaves both untouched, so the two branches meet only in `main`'s body, in
  different hunks. C merges the release branch in after A squashes (milestone
  46's order).
- **Skipping a restored work item entirely**, meaning a restored
  `routing.md` drops the item from `declarations`. The documented rule keeps
  every requirement except reachability for a record the pull request does not
  touch, so a restored item is still read for everything else. #597 went red
  on reachability alone.
- **A record deleted and restored WITHIN the branch** (its content never in
  the base's history). This is still judged on the latest add, and the refusal
  names the restoring commit. That is the documented cost of the stub shape,
  and this work leaves it alone.
- **Choosing the earliest add of the current content** instead of the latest
  add. The document states *latest add* and #529 calls the early one the
  unsafe direction. Changing that would be a design change, not a patch.
- **`unverified_check.py#wrote_a_spec`.** It already reads `--full-history`
  (#525), and it asks `-1` for existence, so order cannot change its answer.
  The enumeration (`grep` for `diff-filter`, `find-object` and `full-history`
  over `skills/ hooks/ .github/`) found `added_on_branch` as the only
  path-limited, order-sensitive history query.
- **`seal/follow-up.md` line 60** (`--worktree` reading declarations from the
  working tree). This is unrelated to how a record is read, and none of this
  work is its prerequisite.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | #529, merged side branch | Given a record first added on the branch before a fix on a parallel line, and a side branch that merges the fix, deletes the record and re-adds the same content, merged `--no-ff`, and a work item at or after `ORDER_FROM`. When `chain_check` runs, then `written_late` reads the LATE add, which descends from the fix, and fails naming it | new case in `tests/test_a_record_precedes_the_fixes_it_commissions.py`, seen red against the current `added_on_branch` |
| A2 | #529, skewed clock | Given A1's shape with the side branch's commits dated earlier than the early add. Then the same failure | new case, seen red with `--full-history` and no `--topo-order` |
| A3 | #529, common shapes unchanged | Given S2 or S3 (a branch merging its advancing base, or a `--no-ff` merge of a side branch that added the record). Then the adding commit is the real add, not the merge | the existing cases stay green; one new case for S3 if none of the existing ones builds a merge |
| B1 | Instance 1, restoration | Given a record present in the base's history, retired on the base, and restored byte-for-byte by the pull request, with a `Target SHA` nothing carries. When `chain_check` runs on a ready pull request, then the exit is 0 and the item's line says the record was restored from `<commit>` | new case in `tests/test_chain_check_at_the_pull_request.py`, seen red on the current code (it fails with *not an ancestor of*) |
| B2 | Instance 1, edited after restore | Given B1 with one byte of the record changed. Then the reachability refusal still fires | new case |
| B3 | Instance 1, still read for everything else | Given B1 with the restored last record's `Pass` beside an open 🔴. Then it fails for that | new case, beside `test_a_merged_record_is_still_read_for_everything_else` |
| B4 | Instance 1 reaches `written_late` | Given a restored record whose `fixed` verdict names a commit that resolves and that the restoring commit descends from, in a work item at or after `ORDER_FROM`. Then no *written late* refusal fires | new case in `tests/test_a_record_precedes_the_fixes_it_commissions.py`, seen red on the current code |
| C1 | Instance 4, draft | Given `STRICT_ITEM`, the last record `- [x] Pass` beside `nobody — <why>`, and a draft payload. Then the exit is 0, and a notice names the verifying round and says *Ready for review* re-runs the check and fails if the cell still says nobody | new case in `tests/test_the_last_rounds_fixes_are_checked.py`, seen red on the current code; the notice's text pinned (§14) |
| C2 | Instance 4, ready and unknown | The same record at a ready payload, and with no payload. Then the exit is 1 as today | the existing `test_pass_beside_nobody_fails_a_work_item_begun_after_the_cutoff` (no payload) plus one ready-payload case |
| C3 | Instance 4 does not widen | A draft whose record names `round-9` (absent), a bare `nobody`, or `the session`. Then the exit is 1 | the existing `test_a_draft_pull_request_is_excused_the_pass_and_not_this`, plus the draft variant of one vocabulary refusal |
| C4 | `close` still reports it | `round_record.py close` ticking `Pass` with a fix verdict still prints the refusal from the check it runs | the existing `tests/test_the_fixes_close_the_record.py::test_pass_is_ticked_when_nothing_is_open_and_the_gate_is_the_flag` stays green |
| D1 | Documents say what the check does | The sentences listed under Scope 4 carry the new behaviour, and the orchestration sentence's pin is rewritten | `tests/test_the_rules_have_one_owner.py`, `tests/test_a_folded_statement_names_what_enforces_it.py` and `tests/test_docs_line_wrap.py` narrow runs |
| D2 | Ledger true | New claims in the fragment. Drifted rows re-read and re-stamped where they are | `evidence_check.py` names no DRIFTED or BROKEN row this work caused |

## Data & interfaces

- `added_on_branch(root, base, rel)`: the signature is unchanged and its
  return set is unchanged (a SHA or None). Only which SHA comes back changes.
- A new module-level predicate, named by the builder. Suggested:
  `restored_from(root, fork, rel) -> str | None`, returning the commit found
  or None. It returns None when `fork` is None or git fails, which is the
  strict direction (no relaxation).
- `written_late(reader, root, base, rel)` gains access to the fork. Two ways
  are possible: pass it in, or have `main` pass the restored set. The builder
  chooses and lists the call sites in its phase record.
- `checked_by(..., last=False)` gains `strict` (default `True`, so every other
  caller keeps today's reading). `main` passes its `strict`.
- Printed text that changes (pinned by tests): the item line for a restored
  last record, and the draft notice for `Pass` beside `nobody`.
- Ledger coordinates this work touches. Each is DRIFTED by the edit and
  re-read, never re-pointed:
  - `seal/ledger.md`: the `chain_check.py#checked_by` rows and the
    `chain_check.py#main` row
  - `seal/releases/0.8.0.md`: `#added_on_branch@5461cc08` and
    `#written_late@1b8af05f`
  - `seal/releases/0.11.3.md`: `#written_late@1b8af05f`
  - `seal/releases/0.9.5.md`, `0.13.1.md`, `0.14.0.md` and `0.4.0.md`: the
    `#main` rows

  `evidence_check.py` is the authority on the full list (read 2026-09-25 by
  `grep`; not executed).

## Open questions → questions.md

None of them blocks the build. `questions.md` lists at its head what the tree
answered, and the rows that remain belong to the work.

Framed 2026-09-25 by framer, before the build.
