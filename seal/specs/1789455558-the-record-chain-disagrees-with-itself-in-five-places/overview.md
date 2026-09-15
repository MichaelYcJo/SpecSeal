# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `plan.md` (seven phases, four rules, the alternatives table) · `spec.md` A1–A12 · `questions.md` Q1–Q6 ·
            `routing.md` · `CLAUDE.md` §*a change writes fragments* §*no real identifiers* §*a thing more than one
            party can have is named with whose* §*a ledger coordinate names content* · `skills/agent-contract`
            §1 §2 §5 §9 §12 §14 §15 · `skills/implement/SKILL.md` §1–§4 · `seal/config.md` (no `Record language`
            row → English) · `seal/follow-up.md` · issues #404 #405 #406 #407 #408 #414
· evidence: six rows in `seal/ledger/1789455558-the-record-chain-disagrees-with-itself-in-five-places.md`, one per
            ticket; one row removed from `seal/ledger.md` whose claim this branch made false (below)
· verified: executed — each phase's module, the red-first mutation the plan named for each, and the four
            measurements. read — that no instructing document outside `seal/specs/` carries either changed refusal
            sentence. unverified — the broad gate, which is the sealer's

## Why this work exists

Six tickets deferred under two work items' round caps turned out to be one
subsystem saying different things about the same record in five places; this
makes the generator, the pull-request check and the two case modules that read
them agree, and removes the causes rather than the instances.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The reach's new refusal is narrower than the frame described | `plan.md` §*Operational impact*: *a `round-N+1.md` whose `## Inherited coordinates` table has been edited or truncated since `new` wrote it makes `close --round N` exit 2 where it exited 0* | A table that lost rows **and** names no row from round N at all. One that lost some rows and kept one of round N's still passes | Q3's own decision rule, run as the plan asked: any unaccounted pair narrows the predicate to `filled == 0`. The corpus produced 65 of 139, and the 2 pairs that separate the two rules are sections written **by hand** — one correct row where the round before carried three coordinates. Refusing those is the reader sent to correct a table that is not wrong, which is the failure the removed refusal was removed for. `phases/phase-2.md` carries the four-row table |
| `spec.md` A7 cannot hold as written | A7: *Given a last round whose 🟢 row's Grounds quote an earlier round's 🔴 **and whose verdict is closed** … it says nothing about that row*, verifiable as *a case … **red against the whole-row join*** | The same row reading `verified`: still refused, and no longer called a blocking finding. A second case carries the closed-verdict half as the silence it actually is | The two halves of A7 cannot both be true. The whole-row join is `BLOCKING in "".join(seen) and verdict_of(...) not in CLOSED_WORDS`, so a **closed** verdict was already silent before this change and no fixture of that shape can be red against it. What is red against the join is the same row with an unrecognised verdict — refused either way, and called a blocking finding only by the join. `phases/phase-4.md` carries the reasoning |
| The ledger cannot reach `--strict` exit 0 on this branch, and the frame assumed it could | `plan.md` phase 7: *`bin/evidence-check --strict .`, exit 0 read directly* | Exit 2, with every drifted anchor read and its claim judged; one row removed because its claim is false, and six anchors left DRIFTED for the owner's one-command re-verify | This branch changes four units of `round_record.py` and `chain_check.py` and three test units that **`seal/ledger.md` already cites**, so drift is the mechanism firing correctly rather than a defect. `--reverify` rewrites hashes across the shared file and never the `Checked` column — a gap a standing `# RIDER:` at `evidence_check.py#reverify` measured — so running it blind would record a re-read nobody did, and it would put a multi-row edit to the shared file on a branch while two others are in flight. CI runs the check **without** `--strict`, where drift is exit 1 and a warning, so nothing is broken by leaving it. Every affected claim was re-read: twelve still hold, one does not |
| One `seal/ledger.md` row's claim is false, so this branch touches the shared file after all | `plan.md` §Out and the spawn both say `seal/ledger.md` stays closed, because *nothing on this branch removes code an existing shared row cites* | The row is removed there and its superseding claim written into this work item's fragment | The premise is the thing that turned out false. The row's clause ended *…and the case that pins it asserts the whole output holds no bare `the seal`* — the assertion #406 deleted, so its second half is now untrue. `CLAUDE.md` §*a change writes fragments* states the exception in as many words: *a branch that removes code an existing `seal/ledger.md` row cites must touch that file to leave the ledger true — the row is removed there, and the new claim is written into the branch's own fragment.* One line deleted, nothing else in the file changed |

## Not verified

| Item | Who must answer |
|---|---|
| The broad gate — the full suite, the repository-wide lint and the typecheck (`seal/config.md`'s `bin/test -q && uvx ruff check . && uvx ruff format --check .`) | `agents/sealer.md`, spawned by the orchestrating session once after the review rounds settle |
| Seven `seal/ledger.md` anchors left DRIFTED by this branch's own edits — `round_record.py#close`, `#seal`, `#fix_table`, `#reach_forward`, and the test units `test_the_two_record_run_reads_back_through_chain_check`, `test_the_refusal_says_which_value_the_last_record_may_hold`, `test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one`. Every claim on them was re-read on 2026-09-15 and all still hold; what is owed is the hash refresh and a `Checked` date, which is a person's act | the repository owner, at the release that folds this fragment |
| That phase 4's repaired severity arm behaves correctly at a real pull request | this branch's own pull request — `plan.md` rule 4 names it as a risk taken on purpose rather than designed around |
| ✅ `seal/specs/1789455558-…/handoff.md:61` names `test_both_ampersand_cells_name_both_shells`, which nothing in the tree carries; the records arm of `evidence-check` refused the file for it <!-- NAME NOT IN TREE: this row is ABOUT a name the tree does not carry, so quoting it makes this document say it too. The case lives on `fix/401-402-…`, which this branch did not cut from. --> | closed 2026-09-15 in phase 7: the line carries `NAME NOT IN TREE` with the reason — the case module lives on `fix/401-402-…`, which this branch did not cut from. `evidence-check`'s records arm reports 0 refused |

## Not done

**The eleven cells already rendered wrong by #414's cause are not repaired
here.** Nine were fixed by hand at `9919b265` and two still stand in
`rounds/round-2.md` of `fix/401-402-the-broad-gate-row-runs-unchecked-and-is-never-asked-for`.
Q1 settles it: a fourth work item, cut from `release/v0.12.0` after that branch
merges, repairs both cells and carries #413 with them. Editing another branch's
records from here would collide at its merge.

**The five other readers of `chain.SEPARATORS` were read and not changed.**
Bounding #414's class is what reading them buys; changing them is a different
work item. None has the stray-punctuation shape — the reasoning is in
`phases/phase-3.md` and in Q5.

**`chain_check.py` gained no reader of `## Inherited coordinates`.** #405
established that `close`'s reach is that section's only reader, and a second
reader at the pull request arrives after the wrong cell is already committed.
`spec.md` §Out names it; if the section should also be checked there, it is a
work item with its own frame.

## Fed back into the spec

**None as clauses.** What this work established went into `questions.md`'s own
rows — Q3, Q4 and Q5 now carry measurements with their populations, dates and
readers, and Q6 carries the sentence phase 4 drafted for the reviewing round to
judge — and into the six ledger rows. `spec.md` is left as the framer wrote it,
including A7, whose two halves cannot both hold; the divergence table above is
where that is recorded rather than in an edit to the contract this work was
built against.
