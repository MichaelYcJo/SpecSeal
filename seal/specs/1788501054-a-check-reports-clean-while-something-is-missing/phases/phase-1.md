# 1788501054-a-check-reports-clean-while-something-is-missing — phase 1

<!-- seal/specs/1788501054-a-check-reports-clean-while-something-is-missing/phases/phase-1.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | a942058 |
| Ran by | specseal:smith on opus |

## What this phase was asked

Build phase 1 only, of the four-phase table in `plan.md`: make
`docs/review-handoff-protocol.md` and `skills/code-review/SKILL.md` name the
two forms of `evidence-check` and what each is for — the unscoped read that
says what a branch broke, the scoped `--ledger` write that keeps `--reverify`
off a row somebody else owns — with cases pinning both sentences, seen red
with the prose stashed.

Coordinates given rather than searched for:

- `docs/review-handoff-protocol.md:385`, *"the runner incantation"*, in the
  list of what the handoff carries. It does not distinguish a command's forms.
- The measurement the requirement is bought with: one work item's three review
  rounds and two fix passes all ran the scoped form and all reported ok, and
  the broad gate's unscoped run found fifteen drifted rows and one broken
  claim.

The `Ran by` value is the one the spawn prompt handed over and nothing more —
`specseal:smith`, `model: opus`. The previous work item's phase records are
the mixed case `docs/review-chain-spec.md` describes, where the version detail
after the model came from the segment rather than from the prompt; this row
carries only what was given.

## What this phase found

**The draft number had to move, and the requirement count with it.** The
protocol's Status section is what a conformance reader opens, and
`tests/test_the_handoff_before_round_one.py` already refuses a title and a
Status that name different drafts. The sentence above the bullets says how
many requirements follow, so a fourth bullet under *Three requirements* is the
list counting one thing and the reader counting another —
`test_the_requirement_count_moved_with_the_requirement` refuses both
directions of that, the count alone and the old sentence surviving beside it.

**The obvious repair for #153 is the defect the narrowing was adopted to
fix.** Read quickly, the ticket says *stop narrowing*, and that puts
`--reverify` back onto `seal/ledger.md`'s S8 — a row whose claim is false and
whose repair belongs to the repository owner. So both documents state the
write's purpose beside the read's, and the skill says outright not to answer
this by deleting the narrowing. `test_the_review_skill_refuses_the_repair_that_looks_obvious`
is what keeps that sentence in the file.

**The guidance cannot reach the session this trap was sprung on.** The
orchestrator that handed three rounds the scoped form wrote the guidance it
would have had to read. That is Q1 in `questions.md`, settled by evidence
rather than preference, and it is why phase 2 exists at all: a session that
narrows on its own initiative is told by the tool or by nobody. Both documents
say the tool announces its own narrowing, so phase 2's line is now something
two shipped documents assert — it cannot be dropped silently.

**Two test files, not one.** The prose cases and the execution cases were
written together and split before the commit, because a phase-1 commit
carrying phase 2's red cases does not stand on its own. The split is also the
convention the sibling suites already use
(`tests/test_a_record_says_what_ran_it.py` names its own prose siblings), and
each file's docstring points at the other.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
