# the roll opens the next log with no body — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     `seal/specs/1788486395-.../plan.md`, `spec.md`, `questions.md`,
            `routing.md`; `docs/issues-and-milestones.md`; issue #136;
            `.github/scripts/roll_flow_measurement_issue.py`'s docstring
· evidence: `seal/ledger/1788486395-the-roll-opens-the-next-log-with-no-body.md`
· verified: see *Not verified* below — narrow runs executed, broad gate not run

## Why this work exists

A reading that only means something across versions was being written to the
issue a release deletes, because the instruction a session follows named one
destination; and every rolling log opened by the release script was born with
an empty body and no link back to the one it replaced.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which existing cases grow | `plan.md`'s technical context and the spawn prompt both name `test_one_open_issue_closes_it_and_opens_the_next` as "the one that grows" | Three cases grew | `test_one_open_issue_after_the_retry_succeeds` and `test_close_succeeds_but_open_fails_names_both_in_the_message` both stub `open_issue` with a two-argument callable. `main` now passes the closed issue's number as a third argument, so both stubs raise `TypeError` until their signatures follow. Neither document is wrong about intent; both undercount the blast radius of a signature change |
| What phase 3's cases cover | `plan.md` phase 3 asks for "a case with the milestone call failing" and says nothing about a partial create | Four cases, and one of them pins that a failed call whose create actually landed is not retried | The ladder phase 3 introduces retries `gh issue create`. A call that fails after the mutation lands would, on retry, open a second issue — which is the exactly-one-open invariant broken from the other side, by the script whose whole purpose is to keep it. The plan's stated failure direction for phases 2 and 3 is *allows more*, and that is about the two best-effort arguments; it was never a licence for the retry to break the invariant |
| Whether the round's `issues[0]` note rode this pass | Round 1 left it as a note rather than a finding — "your call whether it rides this pass" | Taken | It is the same class as 🟡 5, which was a finding: this branch gives `flow-baseline` the same exactly-one-open invariant in prose and then honours it nowhere. `agent-contract` §12 says the fix is owed to every instance the cause produces, and fixing only the sentence would leave the script picking whichever of two `gh` listed first while the sentence it ships beside says a broken invariant is named rather than guessed at |
| Where the ledger's `--reverify` was pointed | The spawn prompt says `evidence-check --reverify` takes no row selector, so `seal/ledger.md`'s S8 hash has to be restored by hand afterwards | `--ledger` scoped the run to this work item's own fragment, and S8 was never touched | `--ledger GLOB` bypasses discovery entirely (`evidence_check.py`, *"`--ledger` bypasses this entirely"*), so the twelve anchors this branch added were stamped without any other file being opened. `45edf260` is still the hash on S8, checked by grep after the run |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Narrow runs are named in each `phases/phase-N.md`; `agent-contract` §2 puts the broad gate after the rounds settle | the orchestrator |
| `ruff` is not installed in `.venv` (`.venv/bin/ruff` absent, `command -v ruff` empty), so no formatting or lint check ran against the Python this branch changed. Every line was kept inside 88 columns by hand | the orchestrator, at the broad gate |
| That `gh issue create --milestone` on an unresolvable milestone name fails before it creates the issue rather than after. The cascade in `open_issue` is written not to depend on it — a failed attempt re-reads the open-issue list before retrying — but the ordering itself was read from `gh`'s documented behaviour, never executed | the repository owner, at the 0.9.0 roll |
| That the roll's new body renders as intended on GitHub. Every assertion about it is against the string the script passes to `gh` | the repository owner, at the 0.9.0 roll |
| ✅ `seal/ledger.md`'s one DRIFTED row, `templates/config.md#"# Repository config"` | opened, and it is row S8 (`seal/ledger.md:517`, hash `45edf260`) — already deferred to the repository owner by work item 1788472135's own overview, which says the claim is false and that re-stamping it is not the repair. Neither that file nor `seal/ledger.md` is touched by this branch (`git diff 9f22d67` on both is empty). Nothing new here, and `--ledger` scoping kept this branch's `--reverify` off it |

## Not done

**No row for the skill prose.** Phase 1 is a section of `skills/verify/SKILL.md`
and `tests/test_a_segment_feeds_the_flow_log.py` reads it sentence by sentence
— twelve cases, six of them new. A ledger row citing the section would be an
inventory of the diff rather than a claim a later change can break silently,
which is the judgment `seal/ledger/1788472135-...md` made for the same shape.
The one exception is the negative constraint, which no reader would reconstruct
from the prose because it is about what the prose does **not** say; that has a
row.

**The `flow-baseline` label is not created by anything.** A repository that
wants a durable log creates the label and applies it by hand. Automating it
would mean a session or a script writing to somebody's tracker, which is the
act #136 is explicit about refusing.

**Nothing fails on a broken `flow-baseline` invariant, and the asymmetry is
deliberate.** `flow-measurement`'s exactly-one-open rule stops a release: the
roll script exits non-zero on zero and on two. `flow-baseline`'s is stated in
the same sentence and stops nothing. Round 1 closed the half that was simply
wrong — a session now names a durable log that stopped instead of reading it
as a repository that never measured, and the roll writes a note into the
issue it opens instead of pointing at whichever of two `gh` listed first — so
a broken invariant is **said** in both places it can be seen. What still does
not happen is anything failing. Making it fail would mean deciding what a
release does about a ledger it does not otherwise touch, which is a larger
question than the one #136 asked.

**`gh issue create`'s stderr is not parsed, so which best-effort argument
failed is inferred from the rung rather than read.** A first attempt that fails
for an unrelated reason produces a second attempt whose body says the milestone
could not be set. The note is written to survive that — it names three possible
causes and asks a person to set the milestone by hand *if it still exists* —
and it never asserts the milestone is gone. Distinguishing the causes would
mean matching on a string this repository does not own.

**`docs/flow.md`'s `#110 + #117` tick left this branch.** It rode into
`5e76246` on a `git add -A`, was declared in no commit body and in no phase
record, and PR #144 already carries the same one-character change on a branch
of its own. Two open pull requests holding it is a conflict waiting at
whichever merges second. `git diff f187b39 -- docs/flow.md` is now empty.

## Fed back into the spec

None. Every clause this work acts on was already written — `spec.md`'s
grounding table, the roll script's docstring, and `docs/issues-and-milestones.md`.
