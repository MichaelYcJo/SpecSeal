# 1790138190-settle-leaves-twelve-directories-with-no-way-out — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show goes here, and each part is written when it happens. -->

📋 implement applied
· spec:     pending — filled when the work item closes (phase 7)
· evidence: pending — filled when the work item closes (phase 7)
· verified: pending — filled when the work item closes (phase 7)

## Why this work exists

After two folds `settle` reported nothing left to fold while `seal/specs/`
still held twelve released directories; this gives each kind of directory a
way out and makes an empty `seal/specs/` a green state.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Phase 3's report headings | `plan.md` phase 3: *`./bin/settle` on this branch lists the ten released spec-less directories under the new heading with `1788177600` and `1788395377` named as kept* / the report prints two headings, *retired by the rule* (eight) and *kept by the rule* (two, with their four rows) | the two headings | the plan's own sentence already separates the two as listed and kept; one heading holding both would print a directory `--retire` removes beside one it refuses, which is the confusion `survey`'s docstring records round 1 fixing for the marker arm (*skipped and named* rather than *waiting to be retired*) |
| A10's reader expectation | `spec.md` A10: *a scratch clone with every directory under `seal/specs/` removed and committed · When … `unverified_check.py --baseline <parent> seal/specs/` … run · Then each exits 0* / against that removal's own parent all three CI readers exit 1, at `3103415` and at `be1579e` alike, because the removal takes four directories the rule cannot retire (three hold a `spec.md` with no marker, one has open rows) | the readers' refusal; the settled state is measured on *the next pull request*, based on the emptied commit, where every reader exits 0 | a hand removal of directories that state a rule or hold an open row is the deletion G5's readers exist to refuse, and G6 accepts only what `settle --retire` removes. The spec's own A15 already reads the fold's pull request as a retirement *at the fold's merge-base*, which a probe cannot build without first folding the three specs (O3) |
| Where the evidence-todo rule lives | `plan.md` names only the predicate as landing in `unverified_check.py` / the rule `settle.py#open_rows` held moved there too, as `todo_open_rows`, and `settle` delegates | moved | the predicate reads `evidence-todo.md`, and a second copy of the rule is the drift `plan.md` §*What breaks in six months* is written against |

## Not verified

none — every item this work defers is written when it is decided, and none
has been yet.

## Not done

nothing yet.

## Fed back into the spec

none yet.
