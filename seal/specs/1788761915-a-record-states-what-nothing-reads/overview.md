# 1788761915-a-record-states-what-nothing-reads — overview

📋 implement applied
· spec:     `seal/specs/1788761915-…/routing.md`, `spec.md`, `plan.md`; `CLAUDE.md` §*The goal a design is chosen against*, §*A ledger coordinate names content*, §*a change writes fragments, never the shared file*; `CONTRIBUTING.md` §*What a change to a gate must carry*; `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*; `skills/code-review/SKILL.md` §*Findings format*; issues #190 and #207
· evidence: `seal/ledger/1788761915-a-record-states-what-nothing-reads.md` — R1 the boundary and the identifier arm, R2 the stamp arm, R3 the printed bound. Five rows in `seal/ledger.md` re-pointed from `check_ledger` to `check_text`, and eight re-read and re-verified
· verified: **executed** — `./bin/test` over eleven modules (the new file, `test_the_record_is_generated.py`, and the evidence, chain and hygiene modules the change touches), `./bin/evidence-check .` exit 0, `uvx ruff check`/`format --check` on every touched file, and 28 mutations one at a time. **read** — the eight ledger claims re-verified. **unverified** — the full suite, the repository-wide lint and the typecheck, which are the orchestrator's

## Why this work exists

A record asserted things about the tree that nothing read, and knew the bound
the next round was under without saying it; now `evidence-check` reads the
first over work items that have not shipped, and `round_record.py new` prints
the second at the moment a session decides whether to spawn again.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the check lives | `spec.md`: *no new file and no new CLI … whether it is a new command or an arm of one that exists is `plan.md`'s* — and `plan.md` names neither | An arm of `skills/evidence-check/scripts/evidence_check.py` | It is the checker whose one job is already *does a written claim about the tree still hold*, `plan.md` spells the stamp arm as *resolved the way a ledger anchor is* — which is `resolve_unit`, `content_hash` and `place`, all of them there — and `bin/evidence-check` is already on PATH, so no CLI appears |
| Which names are read | `plan.md`: *a backticked identifier that appears nowhere outside `seal/specs/`* | Only a COMPOUND one — a name carrying an underscore | Measured: of the 55 distinct such names, the 19 without an underscore are a shell command, six stdlib names, an errno, an environment variable, a lint code, a probe value, five words of prose and three retired verdict words. Not one is a claim about a unit; all 36 compound ones are. This is `plan.md`'s own repair for the false positive it predicts — *narrow the pattern, do not widen the exemption* — taken before the first false positive rather than after |
| What the corpus excludes | `plan.md` names only `seal/specs/` | `seal/specs/` **and** `seal/ledger/`; `seal/ledger.md` stays in | Found by writing this work item's own fragment: naming four units in it silenced four refusals in its own `phase-2.md`. The gathered ledger is the other case and points the other way — its S15 note keeps a renamed unit's old name beside the new one on purpose, and excluding it refuses five occurrences of that name in work item `1788735085`'s records |
| How a record's stamp is graded | `spec.md` acceptance: *a stamp the tree contradicts is refused* | An anchor that does not resolve fails (exit 2); drift reports (exit 1, exit 2 under `--strict`) | A live work item's branch is editing the very units its records stamp, so failing on drift is red by construction — the state `.github/workflows/test.yml`'s `ledger` job refuses in its own comment, and a check that is always red gets ignored. #190's own worked example is a stamp *no file carries*, which is the failing half |
| Which floor record the bound is keyed to | `spec.md` acceptance: *the previous record's floor row reads `no`*; `plan.md` silent | The EARLIEST earlier record whose row reads `no` | Keyed to the latest, the walk restarts at every record it stops at, because every record it stops at is itself a record that met the floor. That is the *unbounded by construction* failure `chain_check.stopping_floor` records in its own docstring for the count, and the writer's side must not re-make it |
| Whether `chain_module` is the marker's worked example | Phase 3 wrote it into `skills/code-review/SKILL.md` | An invented name | Writing a real gone name into a document puts it back into the tree the check compares against. It silenced the four occurrences phase 2 went red on, which would have made phase 3's correction stop being load-bearing | <!-- NAME NOT IN TREE -->

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrator, at the broad gate after the rounds settle — `agent-contract` §2 |
| whether the identifier arm's false-positive rate holds for a repository that is not this one — the compound narrowing was measured over one corpus of 55 names | the first user repository to run it, or a later work item that measures a second corpus |
| whether a record naming a unit through a `path#unit` fragment with no hash — the `Location` column's other spelling — should be read as a claim. It is not read today; only backticked bare names and full `path#unit@hash` stamps are | the repository owner, as a follow-up |

## Not done

**No count check, and the reason is written where the next author will stand
rather than only in `plan.md`.** The ticket names it as the second shape and
the plan turns it down: not one of this session's four false counts is
checkable without a convention for naming what is counted, which #190's own
body calls a bigger claim than the first shape. Nothing in the checker states
that, because the checker has no place to put a sentence about a check it does
not implement. It is `plan.md`'s Alternatives table and this memo.

**The record's `path#unit` fragments are not read.** A verdict table's
`Location` column carries `chain_check.py#stopping_floor` as often as
`f.py:130`, and a fragment with no hash is a claim about a unit's existence
that this arm could check. It was left because the identifier arm already
covers a bare name and adding a third pattern with no measured instance is
mechanism ahead of evidence. Named in *Not verified* above with an answerer.

**The shipped work items' 129 occurrences are untouched**, which `spec.md`
puts out of scope and the spot-check confirms is right: six were opened at
their coordinates and every one is a unit that existed when the record was
written, or a stdlib name the narrowing now removes.

## Fed back into the spec

Two clauses, both inferred during implementation and both in
`docs/review-chain-spec.md` §*The reopening — one, and then the run is
capped*: that `new` prints which of three states the run's bound is in, and
that the floor record it names is the earliest whose row reads `no`. The
second is a statement about the rule that was true before this work and had
never been written down on the writer's side.
