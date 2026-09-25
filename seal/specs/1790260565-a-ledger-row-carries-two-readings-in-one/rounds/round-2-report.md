# 1790260565-a-ledger-row-carries-two-readings-in-one — review round 2 report

Verifying round. Target SHA 103b0974; the surface is round 1's fix range
`db544d4f..938edc68` (950db9ef, 938edc68), plus the one new unit round 1's
record names, `EDIT_OUTCOMES` (depth 1). Nothing outside that diff was
re-reviewed. Worked in a `--no-local` clone at the target SHA.

## What the fix pass claimed, and what the code does

**Round 1's ⬜ 1 is closed.** The fix commit claims each new needle was seen
red with its sentence deleted from a scratch copy of its carrier. I re-ran
that myself rather than taking it (executed). Each of the thirteen new
needle-carrier pairs occurs exactly once in its carrier, whitespace
collapsed, and deleting it turns exactly the right case red with that
needle named in the assertion. That is five in `CLAUDE.md`, five in
`CONTRIBUTING.md` and three in the owner, `docs/the-evidence-ledger.md`. The
owner's slice `OWNED_SENTENCES = CONFLICT_SENTENCES[-8:]` now starts at
*removes or edits code an existing* and ends at *run `evidence-check` after
the resolution*, so the two argument needles sit outside it. The owner
carries neither of them, which matches the comment's claim that it words
both its own way (executed count: 0 each).

**Round 1's ⬜ 2 is closed.** The rewritten comment at
`tests/test_release_hygiene.py:1296` makes two claims, and both hold (executed).
With the width dropped inside `ledger_overwide`, the unit case goes red
(1 failed, 2 passed). With the corpus case calling `overwide_rows` bare,
every case stays green (3 passed). The overview row at `overview.md:24` says
the same two things.

**`CLAUDE.md` was not edited in place.** No commit from the release base
f673e3b1 to the target touches it, and the fix range's diff for it is empty
(executed). The needles the fix added for `CLAUDE.md` were already in its text.

**Rows E1 and E2 (`seal/releases/0.15.1.md`) and L1 (the fragment) resolve.**
`evidence-check` over those two files reports 200 ok, 0 drifted and 0 broken.
Over the whole tree it exits 0 (executed). Each row's new note describes the
fix that happened.

### ⬜ 1 — `CONTRIBUTING.md`'s re-stamp needle holds the condition, not the act

`tests/test_a_merge_cannot_silently_drop_a_correction.py:754`. This is in the
new unit. The comment above `EDIT_OUTCOMES` says the pair pins *a claim that
still holds is re-stamped with a dated note*. For `CLAUDE.md` and the owner,
the needle holds the act: *re-stamped there with a dated note*. For
`CONTRIBUTING.md` the needle is *the claim still holds and you have re-read
it*, which is the bullet's premise. The instruction after the dash is
`evidence-check --reverify .`, which recomputes the hash and names what it
changed, and nothing holds it. With that clause deleted from
`CONTRIBUTING.md`, the guides' case stays green (executed: 1 passed). The
first fix below makes the needle cover the act as well.

This is ⬜ and not 🟡. Every document says the right thing today, and the
case holds the outcome's presence in all three carriers. What is missing is
a hold on half of one bullet.

### ⬜ 2 — Correction: E1 does not anchor the unit its new note cites

`seal/releases/0.15.1.md`, row E1. The new note says the outcomes *are held
now as well, by `EDIT_OUTCOMES`*. The row's grounds anchor
`CONFLICT_SENTENCES` and the owner's case, but not `EDIT_OUTCOMES`. The owner's
case names `EDIT_OUTCOMES` in its body, but that anchor hashes the function,
not the dictionary. So a later edit that drops a needle pair from
`EDIT_OUTCOMES` leaves E1 `ok`, and its *held now* stays written over a case
that no longer holds it. `CONFLICT_SENTENCES` is anchored in the same row for
exactly that reason. The anchor below was computed by `evidence-check
--reverify` over a scratch ledger in the clone (executed: `f810196e`).

### ⬜ 3 — Correction: E1's and E2's new notes cite a record that has no runs in it

`seal/releases/0.15.1.md`, rows E1 and E2. Each new note ends *the right case
went red (`rounds/round-1.md`)*. `rounds/round-1.md` records no deletion run
for these needles. Its ⬜ 1 grounds are round 1's needle counts, taken
before the needles existed. The runs appear only in commit 950db9ef's
message. This round's probe row reproduces all thirteen of them, so the
citation can point at this round's record, which will carry that row.

## Regression tests to plant

None needed. The ⬜ 1 fix below is a stronger needle in an existing case.
Seen red by construction: the proposed needle contains the clause whose
deletion stayed green (executed: the proposed needle is found in
`CONTRIBUTING.md`, whitespace collapsed).

## Facts for the evidence ledger

- E1 should anchor `tests/test_a_merge_cannot_silently_drop_a_correction.py#EDIT_OUTCOMES@69099dff` (⬜ 2). Corrected by the orchestrator: this round's ⬜ 1 fix (d7320980) changed the unit after the report was written, so the hash is the final unit's, the one E1 carries since 135efd8a.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `CONTRIBUTING.md`'s re-stamp needle in `EDIT_OUTCOMES` holds the bullet's premise, and the act (`evidence-check --reverify .`) can be deleted with every case green | `tests/test_a_merge_cannot_silently_drop_a_correction.py:754` | open | Executed: clause deleted from `CONTRIBUTING.md` in the clone, guides' case 1 passed |
| ⬜ 2 | Correction: E1's note cites `EDIT_OUTCOMES` as what holds the outcomes, and the row does not anchor it | `seal/releases/0.15.1.md` | open | Read. The owner's case anchor hashes the function, not the dictionary; `CONFLICT_SENTENCES` is anchored for this reason. Hash `f810196e` computed by `--reverify` on a scratch ledger (executed) |
| ⬜ 3 | Correction: E1's and E2's new notes cite `rounds/round-1.md` for red runs it does not record | `seal/releases/0.15.1.md` | open | Read. `round-1.md` carries no deletion run; the runs appear only in commit 950db9ef's message |
| 🟢 | round 1's ⬜ 1 is closed — the union clause, the edit rule's other two outcomes and the guides' two arguments are held by needles | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | confirmed | Executed: each of 13 needle-carrier pairs occurs once; each deletion red in the right case, needle named |
| 🟢 | round 1's ⬜ 2 is closed — the unit case's comment names what goes red and what does not | `tests/test_release_hygiene.py:1296` | confirmed | Executed: width dropped inside `ledger_overwide` → 1 failed; corpus calling `overwide_rows` bare → 3 passed |
| 🟢 | round 1's ⬜ 3 is answered — none of the four shapes is in a ledger file, and the two deferred shapes have homes | `tests/test_release_hygiene.py:1255` | confirmed | Carried: the fix range touches neither `overwide_rows` nor any ledger file's table shape, so round 1's executed count still stands |
| 🟢 | round 1's ⬜ 4 is answered — the plan's approval line stands alone | `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5` | confirmed | Read: the second sentence is on line 6 at the target |
| 🟢 | `CLAUDE.md` was not edited in place | `CLAUDE.md` | confirmed | Executed: no commit in f673e3b1..103b0974 touches it; empty fix-range diff |
| 🟢 | E1, E2 and L1 re-read and re-stamped, and every anchor resolves | `seal/releases/0.15.1.md`, `seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md` | confirmed | Executed: `evidence-check` 200 ok, 0 drifted, 0 broken over the two files; whole tree exit 0 |

## Paste-ready fixes

### ⬜ 1

```python
    "CONTRIBUTING.md": (
        "the claim still holds and you have re-read it — run "
        "`evidence-check --reverify .`",
        "remove the row and write the new claim into your own fragment",
    ),
```

### ⬜ 2

E1's Code grounds cell, with the new anchor appended:

```
`docs/the-evidence-ledger.md#"## A row is a content anchor, and it names no commit"@c69d1fb2`, `CONTRIBUTING.md#"## House rules"@c1fd7d64`, `tests/test_a_merge_cannot_silently_drop_a_correction.py#CONFLICT_SENTENCES@4e5f6382`, `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_policy_document_owns_the_exception_and_the_halves@b5565675`, `tests/test_a_merge_cannot_silently_drop_a_correction.py#EDIT_OUTCOMES@f810196e`
```

If ⬜ 1's fix goes in first, the hash changes. Run `evidence-check --reverify`
after both.

### ⬜ 3

In both E1's and E2's last note, replace the parenthesis:

```
the right case went red (commit 950db9ef's message; reproduced by round 2's reviewer, `rounds/round-2.md`)
```

## Executed probes

| What was run | Result |
|---|---|
| A probe named with the test_tmp prefix, run once in the clone and deleted: whitespace-collapsed counts of the 13 new needle-carrier pairs, then each deleted from its carrier in turn, running the guides' case and the owner's case | each count 1; each deletion 1 failed, 1 passed, with that needle named; the carrier restored each time |
| The same probe: the act `evidence-check --reverify .`, which recomputes the hash and names what it changed, deleted from `CONTRIBUTING.md` with the premise kept | 1 passed: this is ⬜ 1 |
| The same probe: the proposed ⬜ 1 needle searched in `CONTRIBUTING.md`, whitespace collapsed | found |
| The same probe: `ledger_overwide` returns `overwide_rows(text)` without the width | 1 failed, 2 passed |
| The same probe: the corpus case calls `overwide_rows` instead of `ledger_overwide` | 3 passed |
| Argument needle counts in `docs/the-evidence-ledger.md` | 0 and 0 |
| `git log f673e3b1..103b0974 -- CLAUDE.md` and `git diff db544d4f..103b0974 -- CLAUDE.md` | no commit, empty diff |
| `bin/evidence-check --ledger seal/releases/0.15.1.md --ledger` the fragment | 200 ok, 0 drifted, 0 broken, exit 0 |
| `bin/evidence-check .` | exit 0 |
| `bin/evidence-check --reverify` over a scratch ledger with one `EDIT_OUTCOMES` row, deleted after | `EDIT_OUTCOMES@f810196e` |
| `bin/correction-check --range db544d4f...103b0974` | exit 0 |
| `bin/test -q -p no:xdist tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_release_hygiene.py tests/test_no_real_identifiers.py` | 108 passed, exit 0 |
| The broad gate: full suite, lint and format over the finished branch | not yet: it has not been run, and it is the sealer's |

Nothing this round needs a fix. With it, the broad gate comes due: the
sealer's spawn, once the orchestrator has settled the three notes.

Needs a fix: no

Loses a record or crashes: no

## Proof block

Opened in the clone at 103b0974:
`tests/test_a_merge_cannot_silently_drop_a_correction.py` (690–830),
`tests/test_release_hygiene.py` (1200–1330), `CONTRIBUTING.md` (217–232),
`docs/the-evidence-ledger.md` (49–59), `bin/test` (head),
`seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/rounds/round-1.md`,
`seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md` (1–8),
the fix diff `db544d4f..938edc68` and the close diff `938edc68..103b0974`.
`CLAUDE.md` was read through the tests and the system context, not opened as a
file.
