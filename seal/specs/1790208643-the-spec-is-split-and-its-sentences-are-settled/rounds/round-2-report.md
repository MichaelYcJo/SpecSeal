# Round 2 report — the spec is split and its sentences are settled

Verifying round. Target SHA `5e00373f`, base `release/v0.15.1` at
`06f10aaa`. The surface is round 1's fix range `28baec83..091bcde8`:
`577676b2` (the orchestrator's `CLAUDE.md` halves of findings 2 and 4, and
row C8 re-stamped), `b271a9d8` (the smith's fixes and record corrections) and
`091bcde8` (two `survivors.md` exemptions). The fix range creates no unit, and
round 1's `New units` row reads `none`, so nothing in it is judged as new code.
Reviewed in a `git clone --no-local` at the target under the session
scratchpad. Nothing was written in the worktree except this file.

Coordinates carried from round 1's record and report without re-deriving
them: where each rule sits in the four carriers, the `blocks more` statement
at `docs/review-chain-spec.md:447`, and the three ledger rows of round 1's
finding 11. Every verdict below is re-derived.

## What the account claimed, and what the code does

- **The halves rule gives the hash to neither side where both edited, in all
  three carriers (claimed; confirmed, read and executed).**
  `docs/the-evidence-ledger.md:118`, `CONTRIBUTING.md:258` and
  `CLAUDE.md:169` each say *to neither side where both did*, and each says
  the row is re-read against every edit the merged unit carries. The owner's
  paragraph now sits below the marker check, so *Nothing downstream can see
  that* (`:100`) again follows the #424 paragraph it points at.
- **The edit arm corrects a falsified claim in place before re-stamping
  (claimed; confirmed, read).** The owner (`docs/the-evidence-ledger.md:47`)
  and `CLAUDE.md:138` state it as one sentence. `CONTRIBUTING.md:223` states
  it as a third answer bullet, which round 1's report gave no block for. That
  bullet says: *the code still stands and your edit made the claim false —
  correct the claim in place first, with a `Corrected <date>` note, then run
  `--reverify`*. It agrees with the owner: correct first, then re-stamp. It
  also keeps the section's *about the claim rather than the code* framing,
  and the paragraph after it now reads *All three … none is an append*.
- **Both needles and the case are green (claimed; confirmed, executed).**
  The module is `52 passed` at the target. With *the side that edited the
  anchored unit* deleted from one carrier at a time, the result is: from
  `CLAUDE.md`, `test_a8_both_rule_documents_say_what_to_do_at_the_conflict`
  red; from `CONTRIBUTING.md`, the same case red; from the owner,
  `test_the_policy_document_owns_the_exception_and_the_halves` red. Every
  file was restored from kept bytes and checked by sha256. **The clauses the
  fixes added are held by nothing, though.** That is finding 1 below.
- **The fix-range sweep reported two sentences (claimed; found three,
  executed).** `bin/survivor-check --range 28baec83..091bcde8 --exempt
  <survivors.md>` exits 1 at `091bcde8`. It excuses the two
  `blocks more` sentences and still names
  `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/spec.md:137`,
  which keeps *exactly one side*. Over the pull request's own range
  (`06f10aaa...HEAD`) the sweep exits 0, because `spec.md` is added by the
  branch, so CI cannot see this survivor. That is finding 3.
- **The two exemptions (claimed grounds; confirmed, read).** In
  `skills/code-review/scripts/chain_check.py:2394`, *this file* is the
  checker itself. Its claim that every other refusal fails closed on what it
  cannot read agrees with the checker's own comments. The verdict vocabulary
  counts an unrecognised word as open (`:383`), and `Written late` judges an
  unreadable row as though the row were absent (`:373`). The one leniency is
  `NEEDS_FROM`'s pre-cutoff print (`:661`), which is a grandfather cutoff and
  not a tolerant read. Neither sentence copies the dangling *this document's
  default*. Each names a different referent that does hold the direction, so
  exempting them is right in kind. The test module's *this file*
  (`tests/test_a_record_precedes_the_fixes_it_commissions.py:765`) is weaker,
  because a test module is itself a file. Its module docstring opens by
  naming `chain_check.py`, and the grounds rest on that. I accept them.
- **The remaining fixes (claimed; confirmed, read).**
  `docs/commit-review-gate-spec.md:340` sends the rows to the record document.
  It sends the floor, `Needs a fix`, the reopening and *when the record was
  written* to the run document, which holds §*When the record was written —
  before the fixes it commissioned* (`docs/review-chain-spec.md:630`).
  `skills/verify/SKILL.md:80` describes a runner that starts pytest as a
  child, not the reader's own `bin/test`.
  `tests/test_a_record_says_what_ran_it.py:439` no longer contradicts itself,
  no line is over 100 columns, and ruff check and format both exit 0.
  `skills/evidence-check/SKILL.md:316` separates the code a row cites from
  what it claims. The three ledger Claim cells of round 1's finding 11 name
  `docs/round-record-spec.md`, each with a `Corrected 2026-09-24` note. The
  `CLAUDE.md` exemption row is gone, and `overview.md` says the paste landed.
  `plan.md:7` ends at *spawned.*, and the generator's `chain_check` pass
  printed no approval-line notice over this report. `overview.md` names #568
  for the three doubled-notes rows. Row C8 carries a dated re-read for
  `577676b2`, and E1 and E2 carry one each.

## Do the four carriers state one rule?

I read `docs/the-evidence-ledger.md`, `CONTRIBUTING.md`, `CLAUDE.md` and
`skills/evidence-check/SKILL.md` side by side.

- **The edit arm.** The owner, `CONTRIBUTING.md` and `CLAUDE.md` state one
  rule in three wordings: a removal takes the row out and writes the new
  claim into the fragment; an edit is re-read; a claim that still holds is
  re-stamped; a claim the edit made false is corrected in place with a
  `Corrected <date>` note, then re-stamped. None of these is an append. The
  skill's sentence (`:316`) is the exception as `correction-check` needs it,
  and it has one more disjunct than the other three: *or makes what the row
  claims false*, which covers a claim falsified with no drift. That disjunct
  was the skill's before this branch (the base reads *a branch that falsifies
  what an existing shared-ledger row claims*). It is the case
  `seal/follow-up.md`'s row about code a branch ADDED asks about, and
  `questions.md` Q3 leaves that row to the owner. So the skill is wider than
  the owner there on purpose, and the answer is Q3's rather than this round's.
- **The halves rule.** The owner, `CONTRIBUTING.md` and `CLAUDE.md` state
  one rule. The notes are a union. The hash belongs to the editing side, and
  to neither side where both edited. `evidence-check` runs after the
  resolution, and the row is re-read against every edit. The skill carries no
  halves paragraph. Its `correction-check` section says what that command
  cannot see and stops there, as it did at the base. The spec's carrier list
  for #509 (`spec.md:137`) is the owner and the two guides, so the skill is
  not a missing fourth carrier.
- One thing I considered and did not raise. The owner's halves paragraph ends
  *before it is re-stamped*, which read alone gives one outcome, the shape of
  round 1's finding 3. It is not that defect. Where the unit survives the
  merge, both surviving outcomes of the edit arm end in a re-stamp:
  corrected-then-re-stamped, or re-stamped. The edit arm stated 70 lines
  above governs which one applies.

## Findings — from execution

### ⬜ 1 — the clauses round 1's fixes added are held by no case, and the owner's third outcome can be deleted with the suite green

`tests/test_a_merge_cannot_silently_drop_a_correction.py:711`. I deleted each
added clause from each carrier in turn, and the module stayed `52 passed`
every time. The clauses were *and to neither side where both did* (three
carriers), *re-read against every edit the merged unit carries* (three),
`CLAUDE.md`'s *corrected in place … where the edit made it false*,
`CONTRIBUTING.md`'s third bullet, and the owner's *one the edit made false is
corrected there first*. No module under `tests/` names any of them.

Round 1's §*Regression tests to plant* named this needle, and agent contract
§14 asks for the pin in the same commit. It did not land, and the fix pass's
records do not say why. The comment above the needles (`:722`) also still
says *the checker says which after the fact*, which is the *which side*
wording the fix removed.

Why ⬜ and not 🟡: every carrier is right at the target, so the release ships
no wrong sentence. What is missing is the pin that keeps the next edit from
quietly reverting one carrier. The block under §*Paste-ready fixes* was run
in the clone and then reverted. It is green at the target. It turns
`test_a8_both_rule_documents_say_what_to_do_at_the_conflict` red for each
guide's clause removed, and the owner's case red for each owner clause
removed. That includes the edit arm's third outcome, which needs its own
assertion, because the owner's halves paragraph also contains `` `Corrected
<date>` note`` (as *notes*) and a shared needle alone stayed green.

### ⬜ 3 — this item's `spec.md` still states both rules as round 1 found them, and the fix-range sweep names one (a correction)

`seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/spec.md:137`.
The #509 row says *the hash belongs to exactly one side* and *a drifted
anchor is the tool naming which side that was*. The #488 row at `:136` says
the branch *re-reads the drifted row and re-stamps it*, with one outcome.
`overview.md` §*Fed back into the spec* reads `none`. The survivor sweep over
the fix range exits 1 on `:137` with the exemptions applied, and the account
reported the sweep as naming two places. `settle` later folds what is still
true out of `spec.md` into `docs/`, so these two rows are the ones a retiring
session would have to catch. It is a record, so it is a correction and not
counted by `Needs a fix`. Two ways to fix it: correct both rows with a dated
note and add a line under §*Fed back into the spec*, or add a `survivors.md`
row with the grounds that the frame records what was asked.

### ⬜ 4 — rows E1 and E2 label clauses no case holds as executed, and E2's note keeps *which side* (a correction)

`seal/ledger/1790208643-the-spec-is-split-and-its-sentences-are-settled.md:13`.
The fix pass reworded both Claim cells to the corrected rules. The Result
cells still say **Executed**: red with each sentence removed from the owner.
That was true of the two sentences phase 3 pinned, and it is not true of the
added clauses (finding 1). E2's Notes also still say *only the drift says
which side edited*, and where both sides edited, the drift names the row and
not a side. Once finding 1's block lands, the Result cells are true again
with a dated re-read naming the new needles. Otherwise the added clauses
should carry **Read**.

## Findings — from reading

### ⬜ 2 — the record document now names the reopening's direction as the rule the `not yet` reason is an exception to, while the checker names its own refusals

`docs/round-record-spec.md:529`. The fix for round 1's finding 6 made the
dangling *this document's `blocks more` default* read *the `blocks more`
direction `docs/review-chain-spec.md` §*The reopening* states*. The only
`blocks more` statement there (`:447`) is the reopening check's own failure
direction: a run that reopens twice is refused. That is not a default for the
fix-surface cell, and `says_not_yet`'s `allow` is a different check. The code
states the same exception about a different referent: *this file's `blocks
more` direction. Every other refusal here treats what it cannot read as the
failing case* (`chain_check.py:2394`). That is the sentence this round
accepted the exemption for. So two statements of one exception now name two
different rules. The behaviour is unaffected. The block under §*Paste-ready
fixes* names the one the code names.

## Regression tests to plant

- `tests/test_a_merge_cannot_silently_drop_a_correction.py`: the block under
  §*Paste-ready fixes* for finding 1. It was seen green at the target and red
  per carrier with each added clause removed, in the clone, and then
  reverted.

## Facts for the evidence ledger

- None new. E1 and E2 take a dated re-read once finding 1's needles land
  (finding 4).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the clauses round 1's fixes added — neither side where both did, re-read against every edit, the edit arm's corrected-in-place outcome — are held by no case in any carrier | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | open | executed: each clause deleted from each carrier, module `52 passed` every time; round 1's regression test not planted; the proposed block green at the target and red per carrier |
| ⬜ 2 | the record document names the reopening's own failure direction as the rule the unrecognised `not yet` reason is an exception to; the checker names its own refusals | `docs/round-record-spec.md:529` | open | read: `docs/review-chain-spec.md:447` is the reopening check's direction; `chain_check.py:2394` states the exception against the file's refusals |
| ⬜ 3 | this item's `spec.md` keeps *exactly one side* and a single-outcome edit arm; the fix-range sweep exits 1 on it with the exemptions applied | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/spec.md:137` | open | executed: `survivor-check --range 28baec83..091bcde8 --exempt` exit 1, one place; also `:136`; the PR range exits 0; a record, so a correction |
| ⬜ 4 | rows E1 and E2 label clauses no case holds as executed, and E2's note keeps *which side edited* | `seal/ledger/1790208643-the-spec-is-split-and-its-sentences-are-settled.md:13` | open | the Result cells describe phase 3's two needles; finding 1's probe; a record, so a correction |
| 🟢 | round 1's finding 1 is closed — the owner's halves rule gives the hash to neither side where both edited and re-reads against every edit | `docs/the-evidence-ledger.md:118` | confirmed | read; the needle it keeps turns the owner's case red when deleted, executed |
| 🟢 | round 1's finding 2 is closed — both guides carry the same halves rule | `CONTRIBUTING.md:258`, `CLAUDE.md:169` | confirmed | read; the kept needle red in `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` per guide, executed |
| 🟢 | round 1's finding 3 is closed — the owner's edit arm names both outcomes, and `CONTRIBUTING.md`'s third answer bullet agrees with it | `docs/the-evidence-ledger.md:47`, `CONTRIBUTING.md:223` | confirmed | read: correct first with a `Corrected <date>` note, then re-stamp, in both |
| 🟢 | round 1's finding 4 is closed — `CLAUDE.md`'s edit arm names the corrected-in-place outcome | `CLAUDE.md:138` | confirmed | read |
| 🟢 | round 1's finding 5 is closed — *Nothing downstream can see that* follows the #424 paragraph again | `docs/the-evidence-ledger.md:100` | confirmed | read |
| 🟢 | round 1's finding 6 is closed — the dangling *this document's default* is gone | `docs/round-record-spec.md:529` | confirmed | read; what replaced it is finding 2 of this round |
| 🟢 | round 1's findings 7 to 10 are closed — the gate pointer, the verify skill's wrapper paragraph, the docstring and the skill's *cites* | `docs/commit-review-gate-spec.md:340` | confirmed | read; also `skills/verify/SKILL.md:80`, `tests/test_a_record_says_what_ran_it.py:439` (module `52 passed`, ruff 0), `skills/evidence-check/SKILL.md:316` |
| 🟢 | round 1's findings 11, 12 and 14 are closed — the three Claim cells, the dead exemption and pending-paste rows, the approval line | `seal/ledger.md` | confirmed | read: three `Corrected 2026-09-24` notes; `survivors.md` and `overview.md`; `plan.md:7`, and the generator's check pass printed no approval notice over this report, executed |
| carried | round 1's finding 13 — which of the doubled notes is the row's | `seal/ledger.md` | deferred #568 | already deferred in round 1; `overview.md` §*Not done* names #568 |
| 🟢 | the two `survivors.md` exemptions for `chain_check.py`'s own direction | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/survivors.md` | confirmed | read: each names a referent that holds the direction; the PR-range sweep with them exits 0, executed |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py` at the target | `52 passed` |
| *the side that edited the anchored unit* deleted from `CLAUDE.md`, `CONTRIBUTING.md`, the owner in turn; module run; restored and sha256-checked | red: `test_a8_both_rule_documents_say_what_to_do_at_the_conflict`, the same, `test_the_policy_document_owns_the_exception_and_the_halves` |
| the skill's *removes or edits the code an existing ledger row cites* deleted; module run | `52 passed` (no case reads that sentence) |
| each clause round 1's fixes added deleted from each carrier (nine mutations); module run each time | `52 passed` every time (finding 1) |
| finding 1's block applied in the clone; the module at the target, then eight clause deletions; then the block reverted | green at the target; red for each guide clause and each owner clause, the owner's edit arm through its own assertion |
| `bin/test tests/test_a_record_says_what_ran_it.py`; `uvx ruff check` and `format --check` over it | `52 passed`; exit 0, exit 0 |
| `bin/survivor-check --range 06f10aaa...HEAD --exempt survivors.md` | exit 0; three exempt used |
| `bin/survivor-check --range 28baec83..091bcde8`, without and with `--exempt survivors.md` | exit 1, three places; exit 1, one place (`spec.md:137`, finding 3) |
| `bin/correction-check --range 06f10aaa...HEAD` | exit 0 |
| `git grep` over the tracked tree for the old wordings (*exactly one side*, *which side that was*, *re-stamps it there*) outside round records | this item's `spec.md` and `phases/phase-3.md`, and dated notes in C8, D1 and E2; the phase record and the notes are history, `spec.md` and E2 are findings 3 and 4 |
| `evidence_check.py --strict .` in the clone, with this report copied in | exit 0; `1868 ok · 0 drifted · 0 broken`, records arm `0 refused` |
| `bin/test tests/test_no_real_identifiers.py` with this report staged intent-to-add in the clone | `5 passed` |
| `round_record.py new` over this report in the clone; the record deleted and `round-1.md` restored after | exit 0; the tables parse; `Needs a fix` `no` and the floor `no` copied; `Pass` unticked while the four notes read `open`; no approval-line notice for `plan.md` |
| the broad gate — full suite, repository-wide lint, typecheck | not yet; this round did not run it and leaves it to the sealer |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether the skill's *or makes what the row claims false* — wider than the owner — is the rule, i.e. whether `seal/follow-up.md`'s row on code a branch ADDED is closed | already `questions.md` Q3 | the repository owner, whom Q3 names |

## Paste-ready fixes

### ⬜ 1 — `tests/test_a_merge_cannot_silently_drop_a_correction.py`

Replace `:718`–`:730` (the #488 and #509 groups, the tuple's close, and
`OWNED_SENTENCES`):

```
    # #488: the exception is an edit as well as a removal, and both are the
    # one write a branch owes the file the row is in; a claim the edit made
    # false is corrected in place first, with a dated note.
    "removes or edits code an existing",
    "keeping an existing claim true",
    "`Corrected <date>` note",
    # #509: of a conflicted row only the notes are a union; the hash is the
    # side's that edited the unit and neither side's where both did, and the
    # row the checker names is re-read against every edit the merge carries.
    "the side that edited the anchored unit",
    "to neither side where both did",
    "re-read against every edit the merged unit carries",
    "run `evidence-check` after the resolution",
)

# The owner of the two rules the needles above end with. The guides carry
# them and link here; the policy document states them first (#488, #509).
OWNED_SENTENCES = CONFLICT_SENTENCES[-7:]
```

And in `test_the_policy_document_owns_the_exception_and_the_halves`, after
the `for needle in OWNED_SENTENCES` loop:

```
    # #488's third outcome, in the owner's words. The shared needle above is
    # not enough here: the halves paragraph's `Corrected <date>` notes carry it.
    assert "the edit made false is corrected there first" in text, (
        "the ledger policy does not say an edit that falsified a claim corrects it first"
    )
```

### ⬜ 2 — `docs/round-record-spec.md:528`

```
**Its direction is `allow` for a reason the checker does not recognise, and
that is a deliberate exception to the direction every other refusal in
`chain_check.py` takes, which treats what it cannot read as failing.** The
```

Needs a fix: no
Loses a record or crashes: no

Nothing this round found needs a fix, so the run ends here without spending
the cap. The broad gate has come due: what comes due is the sealer's spawn.
If finding 1's block is planted, it has to land before that spawn, because an
edit after the broad run spends it.

## Proof block

Files opened: `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/rounds/round-1.md`
and `round-1-report.md`; the diff `28baec83..091bcde8`, all fifteen files;
`docs/the-evidence-ledger.md` (`:40`–`:60`, `:85`–`:135`);
`CONTRIBUTING.md` (`:200`–`:275`); `CLAUDE.md` (§*a change writes
fragments*); `skills/evidence-check/SKILL.md` (`:305`–`:360`), with the
base's `:315`–`:319`; `tests/test_a_merge_cannot_silently_drop_a_correction.py`
(`:700`–`:780`); `skills/code-review/scripts/chain_check.py` (`:370`–`:440`,
`:655`–`:668`, `:2380`–`:2405`, `:2992`–`:3004`);
`tests/test_a_record_precedes_the_fixes_it_commissions.py` (`:1`–`:12`,
`:755`–`:775`); `docs/review-chain-spec.md` (headings, `:440`–`:452`);
`docs/round-record-spec.md` (headings, `:500`–`:535`);
`docs/commit-review-gate-spec.md` (`:337`–`:343`); `skills/verify/SKILL.md`
(`:60`–`:90`); `tests/test_a_record_says_what_ran_it.py` (`:436`–`:470`);
this item's `spec.md` (`:103`–`:185`), `questions.md` (Q1–W4) and
`overview.md` §*Fed back into the spec*; `seal/follow-up.md` (the ADDED-code
row); `seal/ledger.md` rows R8, R2, A6, C8; `bin/test` (head);
`skills/code-review/SKILL.md` §*Findings format*.
