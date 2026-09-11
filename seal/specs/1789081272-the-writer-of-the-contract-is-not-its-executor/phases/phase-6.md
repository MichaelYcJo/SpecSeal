# 1789081272-the-writer-of-the-contract-is-not-its-executor — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | `226a03d` — the phase is `d478a5d` (the deferral), `af07a43` (`docs/flow.md`), `bf2811d` (the README rows), `226a03d` (the two fragments) and the commit carrying these records. `plan.md` row 6's Status is `226a03d`, the commit that closed the phase's work, the way rows 4 and 4b name theirs |
| Ran by | smith on Opus 5 (1M context) |

## What this phase was asked

The last build phase. **Phase 5 is not skipped and is not mine** — it was
deferred to #350 by the repository owner on 2026-09-11, and the instruction
was explicit that it must not be built.

Five things. `plan.md` closes honestly, with row 5's Status reading
`deferred #350` and `spec.md` §Scope item 7 recording the same where a reader
meets the promise, in the struck-through shape §Scope/Out already uses for
Q1's reversal. `docs/flow.md` gets the minimum its own rule requires and
nothing more — 0.11.0's `#84` box ticked and a row for #350 under 0.11.1 —
because every further line is one #351 deletes. The two fragments, this
repository's convention rather than the `implement` skill's default:
`seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`, with
`CHANGELOG.md` and `seal/ledger.md` left alone, and with the specific ledger
claim phase 4b left for this phase — the `Planning` axis's mark and its
notice, which phase 4b deliberately kept out of `seal/ledger.md`'s two narrow
smith-mark rows. `overview.md` closed, with four named leavings in
`## Not done`: #350, `questions.md` Q3 and Q4, the `seal/follow-up.md` row
phase 4 opened, and the re-pointed ledger anchor — the last stated rather than
re-argued, because the orchestrator hands it to round 1 as a named item. And
the README `framer` row phase 1 left in `## Not done`, to be settled either
way but not left ambiguous.

S12 was given as a hard constraint: the ticket-order step's terminal phrase
and the draft pull request's position before the rounds are both pinned, and
phase 2's `spec · plan (framer)` edit there was to be left alone.

## What this phase found

**The drawing holds, and where it is silent it is silent for a reason a
reader can check.** Row 6 delivers `docs/flow.md`, the two fragments and the
closing memo, and every one of those is what the phase built. Two things
about it are worth the record.

**Row 6's first clause was already spent, and that was known.** *Step 2 loses
`once #84 exists`* is phase 2's, by the divergence row `overview.md` has
carried since then: S11 names the flow sentence and the sealer's count
together, and row 2's Verified-by cell makes that case phase 2's, so the plan
as written could not be followed. Nothing was re-done here; the checkbox and
the section are what row 6 kept.

**Row 6's Verified-by names a check whose pass, on this branch, is exit 1.**
`fold_ledger.py --check` asks *has every fragment reached the shared file*,
and a feature branch is supposed to leave one that has not. Measured: both
gatherers read exit 0 before the fragments existed and exit 1 afterwards,
each naming exactly this work item's file. The hygiene workflow runs them
only on a pull request into `main`, where the answer has to be yes. So the row
is not wrong about the command, it is wrong about the direction of a pass —
and what actually proves a fragment is `--version 0.11.0 --dry-run`, which
built both the released changelog section and the folded ledger section and
wrote nothing, exit 0 each. `git status` was unchanged after both. The
divergence row is in `overview.md`.

**Four acts this phase takes appear in no row, and every one of them
postdates the drawing.** Row 5's `deferred #350` Status and `spec.md` §Scope
item 7's strike-through exist because the deferral was decided on 2026-09-11,
after `plan.md` was approved. The #350 row under 0.11.1 exists because
`docs/flow.md`'s own rule earns it — *a row for any ticket that work opened*.
The README row is phase 1's leaving. A frame cannot name the consequences of
a decision taken after it was written, which is the honest reading rather
than a defect in the frame.

**`deferred #350` is a third value in a column whose own sentence names two,
and it satisfies the rule rather than bending it.** The rule refuses a tick
and the word `done` because both can be typed without anything having
happened; a commit hash is admitted because it asserts a past state somebody
can open. An issue number does exactly that, and `deferred #N` is already
this repository's word for it in every round record's fix table. The
paragraph under the Phases table now says so, in this work item's plan only —
`templates/sdd-plan.md` is untouched, because widening the template is a
change to every plan and this phase has no row for it.

**Phase 1's grounds for leaving the README row conflated two questions.**
Whether the *What ships* table gains a `framer` row at all does not depend on
`questions.md` Q4; only what the row's middle cell says does. The row is owed
either way — a release whose headline is a fifth agent cannot ship a table
naming four — and it is `spec.md` §Scope item 8's own class, one file further
out than the four documents that item enumerates. Written in both editions,
in chain order at the head of the table. Nothing went red: the two derived
cases read the agents table for which definition *preloads* a skill, and the
fifth row preloads nothing the first four did not, so the 5 / 11 / 7 split is
unmoved. A Q4 answered *preload* edits this one cell alongside the two skills
rows and the test constant that answer already costs.

**One advisory finding has no correct edit, and it is handed over rather than
patched.** `bin/evidence-check .`'s records arm reports
`phases/phase-1.md:131` DRIFTED. That line quotes the coordinate `COVERED`
held BEFORE phase 1's own last commit changed it, and names the new hash in
the very next sentence — which is the record doing its job. The arm reads any
`path#anchor@hash` inside a record as a live citation. Re-stamping would make
the sentence claim the old and new hashes are the same; breaking the form
would make the coordinate unopenable. It predates this phase (both files are
untouched here), CI runs the checker without `--strict` so drift is a warning,
and the ledger itself reads 1121 ok · 0 drifted · 0 broken. It is a row in
`overview.md` §*Not verified* with the repository owner as answerer, because
what it asks is whether the records arm should tolerate a superseded
coordinate quoted beside its successor — a decision about the checker.

**No case was added by this phase**, so contract §15 has nothing to bind
here. The phase writes documents and records only; no hook, no script and no
test module changed, which is also why no lint ran — there is no Python in
the diff.

**The survivor check reports nothing standing.**
`survivor-check --range efed273..226a03d` examined 849 files against the
three sentences the range removed and found no removed wording still in the
tree, so `survivors.md` gains no row. The three removals are small by
construction: §Scope item 7 and the README gap paragraph both survive as
struck-through or answered text in place, which is the shape that leaves
nothing to strand.

**Over the phase's whole range the reading is the same and the count is not.**
`survivor-check --range efed273..68b9877` — the range including this record's
own commit — examines 850 files against **twelve** removed sentences and still
reports nothing standing. The nine extra come from this record and the memo,
which reword what the earlier commits left; both readings are recorded because
a reviewer re-running the check will get the wider one, and a record naming
only the narrower count reads as a different result rather than the same one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `spec.md` §Scope item 7's promise that `session_cost.py` reports time per agent | #350, milestone 0.11.1. The sentence itself is not deleted — it is struck through with the deferral beside it, so a reader who meets the promise meets its answer in the same place. `plan.md` row 5's Status is `deferred #350` |
| `overview.md` §*Not done*'s paragraph saying the READMEs have no `framer` row | Both editions' *What ships* table, which now carry the row. The paragraph is struck through rather than deleted, and the sentence above it records why phase 1's grounds did not survive re-reading |
| `overview.md` §*Not verified*'s answerer *a later work item*, for the third routing axis's template pin | The repository owner, through the row phase 4 already opened in `seal/follow-up.md`. That file's own opening refuses a condition wearing a person's clothes, and *a later work item* is one — nobody agreed to open it, so nobody answered |
| nothing else | nothing. No code, no test, no template and no agent definition was touched by this phase |
