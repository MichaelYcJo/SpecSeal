# 1788912166-red-for-following-the-documents-green-for-ignoring-one — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | <filled at the phase's commit> |
| Ran by | unknown — the spawn prompt named no runner, and the value is the spawning session's rather than a value this segment decides about itself |

## What this phase was asked

#295 — the `Broad gate` cell is read at a ready pull request, behind the
eighth cutoff. `not yet` and a SHA older than the record's own `Target SHA`
each fail with their own sentence. Verified by five cases: `not yet` fails, a
premature SHA fails, a settled SHA passes, draft plus `not yet` passes, and an
id below the cutoff is untouched.

The cutoff was handed over as the safety property of the whole change and not
as an option: every round record ever written defaults to `Broad gate: not
yet`, so an arm reading the cell without one fails every work item in flight,
including one whose rounds were running in another checkout while this was
built.

## What a change to a gate must carry

- **A test seen red.** Eleven cases were run against the unfixed script and
  all eleven failed, the first of them with
  `AttributeError: module has no attribute 'BROAD_GATE'` — the constant did
  not exist, because nothing had ever read the cell. Two of the eleven are
  worth naming separately: `test_a_work_item_one_second_below_the_cutoff_is_
  not_failed_for_it` and `test_a_broad_gate_cell_nobody_can_parse_is_reported_
  rather_than_failed` were red on their **print** assertion while already
  exiting 0, which is the shape that says the fixture record passes every
  other arm and the missing behaviour is the reporting rather than the
  verdict. Then **fourteen mutations across both scripts, all killed** (the
  sweep is listed under *What this phase found*).
- **A stated failure direction.** The gate **blocks more**, and this is the
  only arm of the three that does. It is a new refusal with nothing
  grandfathered into it beyond the cutoff, so its blast radius is exactly the
  work items opened on or after `GATE_FROM`. A wrong deny here costs a CI red
  and a re-run of the suite; a wrong allow ships a branch nobody ran the suite
  over, which is what the row exists to prevent. The direction is chosen on
  that asymmetry, and the cutoff is what keeps the deny from firing on history
  nobody can repair.
- **A prompt budget: zero.** No interactive path, no hook, no question. The
  arm reads a table cell and calls `git merge-base --is-ancestor`.
- **Platform honesty.** No process inspection. `git rev-parse` and `git
  merge-base` through the existing `resolves_to` and `is_ancestor` helpers,
  both already used by this file on every run, on every platform CI runs on.

## What this phase found

**The near-miss the spec warned about is real and it is one word wide.**
`round_record.py#bound_line` says *"`chain_check.py` enforces that at the
broad gate"*, which reads as *chain_check reads the Broad gate cell* and means
*chain_check enforces the reopening bound, and the moment it does so is the
broad gate*. That sentence was left untouched: it is correct about a different
thing, and the fact that it now reads as true for a second reason does not
make it a claim about this arm.

**Three states, not two, and the third is what the cutoff is really for.** The
plan named `not yet` and a premature SHA. Building it surfaced two more shapes
that had to be decided rather than discovered later:

- **An absent row.** Judged as the same state as `not yet` — the cell names no
  run — and it FAILS. The spec is silent on it, and the reasoning is that
  `round_record.py new` writes this row on every record it generates, so above
  the cutoff an absent row cannot arise honestly; reading it as *nothing to
  check* would make deleting one line the way past the whole arm. This is a
  judgment beyond the spec's letter and it is flagged as such: it is the one
  decision in this phase a reviewer should weigh rather than check.
- **A cell nobody can parse.** Reported, never failed, which is `questions.md`
  assumption 3 taken literally. A real record in this tree reads `due after
  this record — see the row below`.

**Equal is not premature, and `merge-base --is-ancestor X X` exits 0.** So an
arm resting on ancestry alone fails the exactly-correct case: the round
reviewed a commit and the gate ran at that commit. The resolved oids are
compared before the ancestry call, which is also the thing that makes an
abbreviated cell and a full-length `Target SHA` comparable at all. The
mutation that removes the equality guard turns
`test_a_broad_gate_at_the_very_commit_the_round_reviewed_passes` red.

**The `Broad gate` label moved from the writer to the reader.** It was defined
in `round_record.py` under a comment reading *"Field labels the checker has no
constant for, because it never reads them"* — true when it was written, and
false from this phase on. Two copies would drift silently in the direction
that matters: rename the row in the writer alone and it keeps writing a row
the reader no longer finds, which this arm reads as *no run was named*. The
case that pins it asserts the quoted literal appears **once** in
`chain_check.py` and **never** in `round_record.py`; an `is` comparison cannot
say this, because the two scripts load each other as separate module objects
and `"Broad gate"` is not an identifier, so it is not interned.

**The class this arm broke, enumerated rather than patched where it was
reported.** The first boundary run came back 43 failed / 1129 passed across
two modules, and the cause was one fixture work-item id above the cutoff
(`1799000000`) whose hand-built records carry no `Broad gate` row. Enumerated
statically over every `specs/<id>` in `tests/`: **thirteen distinct fixture
ids, exactly one of them above `GATE_FROM`, in six modules**. All six record
builders now carry `| Broad gate | {sha} against base |`, where the gate SHA
is the commit the round reviewed — equal, so not premature, and it is the
honest value for a record that has settled. Those six modules are 388 passed
after the change. Fixing only the two the report named would have left the
other four red for whoever ran them next, which is contract §12 exactly.

**The mutation sweep, and both files restored from kept bytes.** Fourteen
mutations, all killed; the script asserts each pattern matched exactly once
and one of them did not, at a two-space indentation difference, which is §9's
*an edit must be able to fail* catching a mutation that would otherwise have
been recorded as killed while never having been applied. Restoration is from
bytes held in memory and verified byte-for-byte afterwards, never
`git checkout --`, which would have taken every uncommitted fix in the file
with it.

**What the next phase inherits.** This branch's own work item id IS
`GATE_FROM`, and the cutoff is `>=`. So this pull request is the first one the
arm applies to: its last round record must carry a real broad-gate SHA before
it goes ready, or the check fails its own branch. That is correct and
intended, and it is the one operational consequence phase 4 has to name where
somebody will read it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `round_record.py`'s definitions of `BROAD_GATE` and `GATE_NOT_YET` | `chain_check.py`, which now reads the cell; the writer imports both from there, and `test_the_broad_gate_label_has_one_spelling_both_scripts_read` refuses a second copy |
| the comment *"Field labels the checker has no constant for, because it never reads them"* | replaced in place by the sentence saying the checker now reads this one, and why the definition moved rather than being copied |
