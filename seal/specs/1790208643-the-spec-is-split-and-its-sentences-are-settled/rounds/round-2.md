# 1790208643-the-spec-is-split-and-its-sentences-are-settled — review round 2

| Field | Value |
|---|---|
| Target SHA | 5e00373f67d69f280e9b00e39ae10fa38d7fc1bc |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 567 |
| Broad gate | cea94f6a against 06f10aaa |
| Fixes checked by | no fixes to check |
| Fix range | `5e00373f67d69f280e9b00e39ae10fa38d7fc1bc..aa2afb71f4adc740d131c5b754435ef6904dc8bf`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round at round 1's fixes (`28baec83..091bcde8`), reviewed at 5e00373f. It asked whether each round-1 finding is closed at its coordinates, whether the four carriers of the ledger's edit and conflict rules — `docs/the-evidence-ledger.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `skills/evidence-check/SKILL.md` — now state one rule, whether `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` goes red with a needle removed from each, how the third answer `CONTRIBUTING.md` gained reads against the owner, and whether the two `survivors.md` exemptions for `chain_check.py`'s own *blocks more* direction hold. It was told that a 🟡 here spends the run's one reopening.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the clauses round 1's fixes added — neither side where both did, re-read against every edit, the edit arm's corrected-in-place outcome — are held by no case in any carrier | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | deferred #569 | #569 — a case pinning the clauses round 1 added is a fix, and this verifying round follows a round that met the floor, so it commissions none; the reviewer's executed case and probes are carried whole by #569; executed: each clause deleted from each carrier, module `52 passed` every time; round 1's regression test not planted; the proposed block green at the target and red per carrier |
| ⬜ 2 | the record document names the reopening's own failure direction as the rule the unrecognised `not yet` reason is an exception to; the checker names its own refusals | `docs/round-record-spec.md:529` | deferred #569 | #569 — the same issue: `docs/round-record-spec.md` and `chain_check.py` state the `not yet` exception against two different rules; the reviewer's paste-ready sentence is in #569; read: `docs/review-chain-spec.md:447` is the reopening check's direction; `chain_check.py:2394` states the exception against the file's refusals |
| ⬜ 3 | this item's `spec.md` keeps *exactly one side* and a single-outcome edit arm; the fix-range sweep exits 1 on it with the exemptions applied | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/spec.md:137` | answered | corrected at c1ed5f35 — `spec.md`'s #488 and #509 rows carry dated `Corrected` notes stating the rules the carriers now state, `overview.md` §Fed back into the spec names them, and the frame's #509 sentence is excused in `survivors.md` as a record of what was asked; executed: `survivor-check --range 28baec83..091bcde8 --exempt` exit 1, one place; also `:136`; the PR range exits 0; a record, so a correction |
| ⬜ 4 | rows E1 and E2 label clauses no case holds as executed, and E2's note keeps *which side edited* | `seal/ledger/1790208643-the-spec-is-split-and-its-sentences-are-settled.md:13` | answered | corrected at c1ed5f35 — fragment rows E1 and E2 mark the clauses round 1 added as read, not executed, until #569's case lands, and E2's note says the drift names the row; the Result cells describe phase 3's two needles; finding 1's probe; a record, so a correction |
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

## Paste-ready fixes

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
```
    # #488's third outcome, in the owner's words. The shared needle above is
    # not enough here: the halves paragraph's `Corrected <date>` notes carry it.
    assert "the edit made false is corrected there first" in text, (
        "the ledger policy does not say an edit that falsified a claim corrects it first"
    )
```
```
**Its direction is `allow` for a reason the checker does not recognise, and
that is a deliberate exception to the direction every other refusal in
`chain_check.py` takes, which treats what it cannot read as failing.** The
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/the-evidence-ledger.md:98` | round 1's 🟡 1 — fixed |
| round-1 | `CONTRIBUTING.md:255`, `CLAUDE.md:168` | round 1's 🟡 2 — fixed |
| round-1 | `docs/the-evidence-ledger.md:47` | round 1's 🟡 3 — fixed |
| round-1 | `CLAUDE.md:138` | round 1's 🟡 4 — fixed |
| round-1 | `docs/the-evidence-ledger.md:107` | round 1's ⬜ 5 — fixed |
| round-1 | `docs/round-record-spec.md:529` | round 1's ⬜ 6 — fixed |
| round-1 | `docs/commit-review-gate-spec.md:340` | round 1's ⬜ 7 — fixed |
| round-1 | `skills/verify/SKILL.md:80` | round 1's ⬜ 8 — fixed |
| round-1 | `tests/test_a_record_says_what_ran_it.py:439` | round 1's ⬜ 9 — fixed |
| round-1 | `skills/evidence-check/SKILL.md:316` | round 1's ⬜ 10 — fixed |
| round-1 | `seal/ledger.md:1086` | round 1's ⬜ 11 — answered |
| round-1 | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/survivors.md:16` | round 1's ⬜ 12 — answered |
| round-1 | `seal/ledger.md` | round 1's ⬜ 13 — deferred |
| round-1 | `seal/specs/1790208643-the-spec-is-split-and-its-sentences-are-settled/plan.md:7` | round 1's ⬜ 14 — answered |
| round-1 | `docs/review-chain-spec.md`, `docs/commit-review-gate-spec.md`, `docs/round-record-spec.md` | round 1's 🟢 — confirmed |
| round-1 | the three documents | round 1's 🟢 — confirmed |
| round-1 | `tests/conftest.py` | round 1's 🟢 — confirmed |
| round-1 | `docs/release-checklist.md` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| whether the skill's *or makes what the row claims false* — wider than the owner — is the rule, i.e. whether `seal/follow-up.md`'s row on code a branch ADDED is closed | already `questions.md` Q3 | the repository owner, whom Q3 names |
