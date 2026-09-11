# 1789081272-the-writer-of-the-contract-is-not-its-executor — phase 4

| Field | Value |
|---|---|
| Phase | 4 · 4b |
| Commit | `553afb1` — the phase is `6c0f5fc` (the axis), `cb00b24` (the mark), `e0c2554` (the cross-file pin strengthened), `d950e8b` (the ledger re-reads) and `553afb1` (these records and the survivor correction) |
| Ran by | smith on Opus 5 (1M context) |

## What this phase was asked

Two rows of `plan.md`, built together because the second is the first's reader.

**Phase 4 — the fourth axis.** `templates/sdd-routing.md` gains a `Planning`
row, `framer` · `the session`, on exactly the terms the `Implementation` row
already has: OPTIONAL, absent reads as *not answered*, an answer outside the
vocabulary reads as unanswered rather than as *this file is not a declaration*,
and the answer is written WITHOUT backticks. `hooks/routing.py` gains the
constants `spec.md` §*Data & interfaces* names and a `planning` key in
`parse()`'s return, on the third axis's terms and for the reason that module's
own docstring gives: nothing decides a commit on it, so a typo there must not
take the whole declaration down and re-ask the review question on branches
whose answer is committed. `table_rows()` needs no change — its docstring
already promised unknown labels are left in *so a reader that does not
recognise a label cannot gain a third axis later*, and this is the fourth
arriving on that promise. `skills/implement/orchestration.md` gains the row as
a **record, not a fourth checkbox**, with #88 cited rather than re-argued.

**Phase 4b — the mark.** `questions.md` Q1 was answered `a mark` against this
frame's own default, by the repository owner on 2026-09-11: a session can
declare `framer` and frame the work itself exactly as it can declare `smith`
and build it. The mark is a **second constant inside `hooks/implementer.py`**,
never a second module beside it — `plan.md`'s Alternatives table records the
rejection and the grounds, contract §11 and §16 each recording a rule that sat
in two definitions in near-identical words while a third carried none. `write`,
`stands` and `is_smith` each generalise; `git_dir` does not change at all, and
`is_smith` was the one to look hardest at, because its docstring's reason for
`rsplit(":", 1)[-1]` over a substring test has to survive whatever shape it
takes for two agents. `hooks/implementer-mark.py` writes for either agent;
`hooks/implementer-notice.py` prints for either axis whose declared agent left
no mark, **once per repository per session, naming both axes in one line when
both are unfulfilled, never one line per axis** (S14). Both files keep failing
toward *no mark*, so a dead gate produces a line somebody reads.

Four cases were named — S8, S9, S13, S14 — with the vocabulary parsed out of
`templates/sdd-routing.md` so the template and the constants cannot drift, each
shown red first, each mutation-tested one at a time, and the cross-file pin
broken from both sides.

## What this phase found

**The drawing holds, and the one place it does not is a constant nobody
reads.** `spec.md` §*Data & interfaces* names four module constants and lists
`BY_SESSION_PLANNING = BY_SESSION  # the same string, one vocabulary`;
`plan.md`'s phase 4 row names three — `PLANNING`, `BY_FRAMER`,
`PLANNING_ANSWERS`. Three were written, and the divergence is deliberate. What
the fourth constant exists to say is that the planning axis's session answer is
not a different string, and `PLANNING_ANSWERS = (BY_FRAMER, BY_SESSION)` says
it by USING that string rather than by naming it twice. An alias is the exact
shape `hooks/implementer.py`'s own docstring refuses one storey down — two
spellings of one thing — and it is what a later edit turns into
`BY_SESSION_PLANNING = "the session"` without anything going red. The comment
beside `BY_FRAMER` carries the sentence the constant would have carried.
`overview.md` holds the divergence row.

**The three handed-over facts hold, and two of them changed what was
written.**

- `templates/sdd-routing.md`'s `Answered <date> by <who>, before the first
  edit.` line is untouched, and the `Planning` row sits in the table above it
  with its own comment paragraph. The cross-file pin phase 3 built was green
  before this phase and after it.
- The orchestration edit lands in `## Orchestrator: how the work is routed`,
  not in Bootstrap, and no ledger row anchors on the routing section —
  `grep` finds zero rows citing that heading. Bootstrap's `8d418684` never
  moved. What DID shake was eleven rows anchored on the implementer units,
  plus one BROKEN, and that is phase 4b's doing rather than phase 4's.
- `survivors.md` already carried phase 2's and phase 3's rows, and phase 3's
  own note about which half of its anchoring the checker enforces is what made
  this phase's five rows quick to write.

**The mark's ledger row went BROKEN rather than DRIFTED, and re-pointing it
was the right act rather than the forbidden one.** `is_smith` became
`mark_for`, so `hooks/implementer.py#is_smith` names nothing. `CLAUDE.md` says
a row whose anchor a change removes is REMOVED and its new claim goes in the
fragment — and the rationale it gives is *its claim went with the code*, which
is what did not happen here. The claim is that the qualifier is dropped with
`rsplit(":", 1)` and never a substring test; it is still true, still in the
same module, and four of the row's five anchors never moved. Removing the row
would have deleted a true claim and four live coordinates to honour a rule
written for a claim that died. It is re-pointed with a 2026-09-11 re-read note
saying what happened, which is the pattern this ledger already uses when a
cited unit MOVES — `seal/ledger.md` carries six rows re-pointed that way when
the Bootstrap section changed files. The framer half is not appended: that is a
new claim, and it goes in the fragment phase 6 opens.

**A cross-file pin built the way the third axis's was cannot see the two files
drift.** `test_the_template_PARSES_into_the_FOURTH_axis_it_ships` substitutes
each constant into the template's own row and parses it back — which is
self-consistent by construction. Rename `BY_FRAMER` and the substitution
renames with it, so the case stays green while the template goes on offering a
word the parser no longer accepts. The case now also READS the two answers out
of the comment a person follows and compares them to `PLANNING_ANSWERS`, which
is red from either side. Both directions were mutated: the constant renamed
with the template untouched, and the template reworded with the constant
untouched. The third axis's own case has the same gap and was left alone —
widening it is a sweep this phase has no row for, and `seal/follow-up.md` is
where that belongs.

**The eighteen mutations were all killed, and two cases could not be shown red
by the code alone.** `test_the_commit_gate_decides_the_same_with_the_planning_row_and_without`
pins that the gate's decision does not move, which already held before the axis
existed — it was shown red by making `parse()` reject an unreadable planning
answer, which is the defect it guards. The extended
`test_every_declaration_in_this_repository_still_parses` asserts that no
committed declaration answers the fourth axis, which is its premise rather
than a behaviour; it was shown red by adding a `Planning` row to this work
item's own declaration and restoring it. Every restore in the loop was asserted
byte-identical against bytes read before the loop started, and `tests/__pycache__`
was cleared between mutations.

**The survivor check reported six places, one of them a live claim of this
phase's own.** `tests/test_the_implementer_is_recorded.py`'s module docstring
still said *nothing is said when the mark stands*, which with two axes is a
claim about the wrong grain — corrected to *about an axis whose mark stands*
rather than exempted, which is the direction the rule prefers. The five
exempted are records: two changelog copies of what 0.7.0 shipped, a past work
item's spec, a ledger section heading naming that work item, and one live
ledger row whose clause is narrower than the code and still true of it. Over
the phase's whole range, `e82403f..553afb1`, the recount leaves two of the five
reporting and excuses both; the other three rows are kept for the reason phase
2's is, that an exemption matching no candidate silences nothing and deleting
one would leave this record naming a survivor with nothing behind it.

**Three shipped documents described the mark gate as smith-only, and none of
them is pinned by anything.** `README.md`'s gate table, `docs/review-chain-spec.md`'s
hook table and its paragraph below, and the git-dir listing in
`docs/one-root-by-lifetime.md` and its Korean edition — all four now name both
axes, under §14, because a table that says what a gate fires on is text a
person reads and acts on.

**Nothing catches them being wrong, and that is measured rather than assumed.**
The four documents were put back to their pre-phase text and the ten modules
that read any of them were run: 491 passed, exit 0. So what pins the notice is
its own sentence in `tests/test_the_implementer_is_recorded.py`, and what pins
these four tables is a person opening them. The probe restored each file from
bytes read before it started and asserted the restore byte-identical.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/implementer.py#is_smith` | `hooks/implementer.py#mark_for`, one comparison over an agent-to-mark table. The docstring's reasoning went with it in full — why the qualifier is dropped with `rsplit(":", 1)[-1]` and why a substring test would read `smith-helper` as the agent — plus the sentence saying why it is one function over a table and not one predicate per agent: a second copy of the `rsplit` is a second place for it to be relaxed. `seal/ledger.md`'s row is re-pointed at the new unit with the re-read that says so |
| `hooks/implementer.py`'s single-axis `MARK` | `IMPLEMENTATION_MARK`, beside `PLANNING_MARK`. The FILE NAME under the git dir is unchanged — `specseal-implementer` is how an existing mark is found and by nothing else — and only the constant is renamed, because with two of them a bare `MARK` is the thing more than one party can have that this repository requires to be named with whose |
| `hooks/implementer-notice.py`'s inline notice sentence in `main` | `line()`, one unit above it, with `unfulfilled()` beside it deciding which axes it speaks for. The singular wording is byte-identical to what shipped, because it is what nearly every notice will say; the plural branch is new and is what S14 pins |
| `agents/*.md` — nothing | nothing. No agent definition was touched by this phase, and `agents/framer.md`'s `## When you run` is cited by the orchestration section rather than edited |
