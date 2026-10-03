# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — review round 3

| Field | Value |
|---|---|
| Target SHA | 089a5c77d9079bcad7031a3f32bb1217ccc3e7de |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 736 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 16 (a narrowed `--reverify` answers only for families rooted in a file it read; the home and L4 say otherwise) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 is a verifying round and the run's last, since round 2 closed on fixes and spent the one reopening. It targets `089a5c77` over round 2's fix range `4f0aacc8..c9fe12fd`. It was asked:
- whether round 2's fixes hold;
- whether the units that pass created are correct: `corrected_by`'s superseded filter, `released_drift` counting an outranked released reading, the unfrozen narrowing branch, `calendar_date`, and `literal_statements` keeping one line for a pipe-led literal;
- whether the smith's reading of 🟡 12 leaves a real hole;
- what the release endgame gives when rerun over the three siblings.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 10 is closed — every carrier says coordinates are judged one at a time and none promises an unread pair is never accepted | `docs/the-evidence-ledger.md:111` | confirmed | closed at `c5829e6e`; read: the home, the changelog, both comments, D3, `plan.md`; executed: the four text-reading modules, 214 passed |
| 🟢 | round 2's finding 11 is closed — a third `Corrected ·` row retiring one of two folded corrections clears the notice | `skills/evidence-check/scripts/evidence_check.py:2419` | confirmed | closed at `9abe7a00`; executed: its case red at `4f0aacc8`, green at HEAD; read: `root_of` files the retiring row under C2 |
| 🟢 | round 2's finding 12 is closed for a narrowing to the family root's file | `skills/evidence-check/scripts/evidence_check.py:3230` | confirmed | closed at `a2c03e94`; executed: both cases red at `4f0aacc8`, green at HEAD; a narrowing to a file holding another member is new finding 16 |
| 🟢 | round 2's finding 13 is closed — a date the calendar does not have orders nothing | `skills/evidence-check/scripts/evidence_check.py:2756` | confirmed | closed at `e2a808b7`; executed: its case red at `4f0aacc8`, green at HEAD; the message is new finding 17 |
| 🟢 | round 2's finding 14 is closed — a first cell equal to another row's cell gets a citation | `skills/evidence-check/scripts/evidence_check.py:797` | confirmed | closed at `ba837122`, as a behaviour change rather than round 2's comment; executed: its case red at `4f0aacc8`; the old and new rules disagree on 0 calls over the tree |
| 🟢 | round 2's finding 15 is closed — S1 states the newest-reading rule | `tests/test_a_released_row_is_read_again_in_a_fragment.py:16` | confirmed | closed at `43354f87`; read |
| carried | round 1's nine findings are closed, as round 2 confirmed them | `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/rounds/round-2.md:32` | confirmed | carried from round 2, not re-derived; the three that round 2's fixes touched (round 1's 2, 4 and 9) are answered by the rows above |
| 🟡 16 | a narrowed `--reverify` answers only for families whose root sits in a file it read; narrowed to a release file holding a folded member, it writes nothing and exits 0 while `--strict` over the same file reads that member DRIFTED, and the home and L4 say it names that row | `skills/evidence-check/scripts/evidence_check.py:3215`, `docs/the-evidence-ledger.md:157`, `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:4` | open | executed: freeze `--into` 0 written, exit 0; no freeze exit 0, no `LEFT`; narrowed `--strict` exit 2; with the fix, 1 written and `--strict` exit 0; in code and sentences round 2's fix pass wrote, so the branch's to fix |
| ⬜ 17 | a `Checked` cell holding a date the calendar does not have is named "the reading of no date" | `skills/evidence-check/scripts/evidence_check.py:2488` | open | executed: R dated `2026-13-45` reads "matches only the reading of no date" |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, released_drift's docstring
    """`(view, drifted, broken)` for the released files among LEDGERS.

    DRIFTED is `{row: {coordinate: match}}`, one entry per row a re-read
    owes: a released row outside every family with a drifted coordinate, and
    the root of each family that is not superseded, has a released member in
    LEDGERS, and has a coordinate none of whose newest readings holds the
    current content, where a released member's reading is drifted or is
    outranked by that newer reading. BROKEN is `[(where, coordinate,
    detail)]` for the released coordinates a re-read cannot clear, which
    take a `Corrected ·` row instead.
    """
```
```python
# skills/evidence-check/scripts/evidence_check.py, released_drift
    for top, by_coord in view.readings.items():
        # A family is the run's to answer for where any of its members sits
        # in a released file LEDGERS names, not only its root: a folded
        # re-read is a released row too (round 3, 🟡 16).
        members = {key[0] for graded in by_coord.values() for key, *_ in graded}
        if top[0] not in wanted and not members & wanted:
            continue
```
```markdown
it adds the row. Where citing rows exist anyway, a `--reverify` narrowed with
`--ledger` names, by its root row, each family a released file it read holds
a member of whose newest reading sits in a file it did not write, and exits
1, because no in-place re-stamp of the files it read can clear that family.
```
```text
L4, the clause after "without the row it re-stamps in place as before,":
and narrowed with `--ledger` it names, by its root row, each family a released file it read holds a member of whose newest reading it could not reach and exits 1; under the freeze a narrowed `--into` writes the re-read such a family owes
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_a_narrowed_into_answers_for_a_family_a_folded_member_puts_in_the_file(repo):
    """The run is narrowed to the release file holding a folded re-read of R,
    not R's own file. That member reads DRIFTED under the same narrowing, so
    `--into` owes its family a re-read (round 3, 🟡 16)."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    released(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `src/service.py#handler@{h1}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        version="0.2.0",
        section="### 1500000001-the-second-item",
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `src/service.py#handler@{h2}` "
            "| read | 2026-03-01 | Re-read 2026-03-01 |"
        ],
        name="2000000009-z",
    )
    (repo / "src" / "service.py").write_text(SERVICE)
    narrowed = ["--ledger", "seal/releases/0.2.0.md", "."]
    assert run(["--strict", *narrowed], repo).returncode == 2
    unfrozen = run(["--reverify", *narrowed], repo)
    assert unfrozen.returncode == 1, unfrozen.stdout
    assert "LEFT  seal/releases/0.1.0.md:5" in unfrozen.stdout, unfrozen.stdout
    frozen(repo, "0")
    out = run(["--reverify", "--into", INTO, "--checked", "2026-04-01", *narrowed], repo)
    assert "1 citing row written" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 0
```
```python
# skills/evidence-check/scripts/evidence_check.py, family_view's emission loop
                    detail = (
                        f"matches only the reading of "
                        f"{checked(key) or 'no date the calendar has'}; "
                        f"the newest reading of this coordinate, {newest} at "
                        f"{where(last[0])}, holds other content — re-read"
                    )
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the four ledger modules, `test_evidence_check.py`, the narrowing module and the one-home module at HEAD | 251 passed |
| the five cases round 2's fix pass planted, with `evidence_check.py` at `4f0aacc8` | 5 failed, each on its own assertion |
| old against new `literal_statements` over the tree at HEAD: `classify` on 77 claim anchors, `citation_for` on 1,146 rows, a whole `--strict` run | 0 differences, 0 disagreeing calls; strict 3,791 ok, 0 drifted, exit 0 |
| `bin/test` on the survivors, docs line-wrap, one-word and no-real-identifiers modules at HEAD | 214 passed |
| 🟡 16 family (R in 0.1.0, folded C in 0.2.0, fragment F newest, code reverted): `--strict` | exit 2, 3 drifted |
| the same, `--strict --ledger seal/releases/0.2.0.md` | exit 2, C DRIFTED |
| the same, under the freeze: `--reverify --into … --checked 2026-04-01 --ledger seal/releases/0.2.0.md` | exit 0, `0 citing rows written · 0 released rows left`; strict exit 2 after |
| the same, without the freeze: `--reverify --ledger seal/releases/0.2.0.md` | exit 0, no `LEFT`; strict exit 2 after |
| the same, without the freeze: `--reverify --ledger seal/releases/0.1.0.md` | exit 1, `LEFT seal/releases/0.1.0.md:5` |
| the same, narrowed to an unrelated fragment: `--strict`, then `--reverify` with and without the freeze | strict exit 0; reverify exit 0 both, with the narrowing notice naming the three unread ledgers |
| the same, without the freeze, unnarrowed: `--reverify --checked 2026-04-01` | exit 0, no `LEFT`; strict 5 ok, 0 drifted |
| the 🟡 16 fix applied in the clone: the two member-file runs, then the four ledger modules | freeze: 1 written, strict exit 0; no freeze: `LEFT` for the root; 146 passed |
| ⬜ 17: R dated `2026-13-45`, a newer fragment re-read, code reverted | "matches only the reading of no date" |
| sibling merges (#735, #731, #733, all three) into `089a5c77`, then `--strict` and `correction-check --range 233f0455...HEAD` | 0 conflicts; drifted 6, 3, 0, 9; records arm 4, 0, 0, 4 refused; correction-check exit 0 each |
| `bin/test` on the ledger, pact, GFM line-reader and one-home modules over the all-three merge | 458 passed |
| the second lander's re-stamp on the all-three merge: `--reverify --into <this fragment> --checked 2026-10-03` | exit 0; 8 hashes on 7 rows; 0 written, 0 left; strict 3,996 ok, 0 drifted, exit 2 (records arm 4 refused) |
| `fold_ledger.py --version 0.18.0` after the re-stamp, staged, then `--strict` and `fold_ledger.py --check` | 4 fragments folded into `seal/releases/0.18.0.md`; strict 3,996 ok, 0 drifted, exit 0, 0 refused; check exit 0 |
| the broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3198` | round 1's 🔴 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2402`, `docs/the-evidence-ledger.md:102` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3217`, `docs/the-evidence-ledger.md:121` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2374` | round 1's 🟡 4 — fixed |
| round-1 | `skills/evidence-check/scripts/correction_check.py:583` | round 1's 🟡 5 — fixed |
| round-1 | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:25` | round 1's 🟡 6 — answered |
| round-1 | `docs/release-checklist.md:199` | round 1's 🟡 7 — fixed |
| round-1 | `docs/the-evidence-ledger.md:37` | round 1's ⬜ 8 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2160` | round 1's ⬜ 9 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3267` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2428` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3285` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2400` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/correction_check.py:579` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2186` | round 2's 🟢 — confirmed |
| round-2 | `docs/the-evidence-ledger.md:111`, `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/changelog.md:20`, `skills/evidence-check/scripts/evidence_check.py:2004` | round 2's 🟡 10 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2404` | round 2's 🟡 11 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3195` | round 2's 🟡 12 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:2435` | round 2's ⬜ 13 — fixed |
| round-2 | `tests/test_a_released_row_is_read_again_in_a_fragment.py:16` | round 2's ⬜ 15 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the second lander re-stamps 8 hashes on 7 rows (6 rows of this fragment, #718's row 23), and #735's four records lines naming a unit this branch removed refuse the records arm until the fold | the handoff to whichever of #647, #718 and #715 lands second; already deferred in round 2 | the orchestrator of the 0.18.0 run |
