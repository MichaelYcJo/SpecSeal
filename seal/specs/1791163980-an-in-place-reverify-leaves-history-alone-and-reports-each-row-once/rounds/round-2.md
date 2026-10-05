# 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once — review round 2

| Field | Value |
|---|---|
| Target SHA | fceff8ce7db5211d72f68fff0640dd7f5b928c63 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #801 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a held two-place coordinate that one place still holds is named `left` and recorded BROKEN on a row the run dates, where `--strict` reads it OK and both the base and round 1's target were silent) |
| Loses a record or crashes | no — nothing written is lost and nothing crashes; 🟡 1 adds a false BROKEN part, which in a signatory repository is a wrong pact-change row rather than a lost one |

- [ ] Pass

## What this round was asked

The verifying round over round 1's fixes (fa8a5c3c..b5dbc88c): did each fix close its finding (round 1's probes p1 and p2 re-run), did the range introduce a regression; the two new behaviours judged by construction across round 1's axes plus coordinate kind (a held coordinate with no one place on a dated row; a coordinate naming a line of a ledger the run may rewrite); the new `left`-reasons sentence against the code; A1 and the two re-reads; `changelog.md` against the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a held two-place coordinate that one place still holds is named `left` and handed MOVES a BROKEN part on a row the run dates, where `--strict` reads it OK and the base was silent; its line also describes the row differently from the check | `skills/evidence-check/scripts/evidence_check.py:3596` | open | p6 executed at the base, round 1's target and this target, with the freeze and without it, alone and beside a newer holder; the fix and its case executed in p7 and p8 |
| ⬜ 2 | A1's clause and the re-reads of `0.4.0.md:59` and `0.18.2.md:129` hold only once this round's yellow 1 is fixed | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | open | a correction to the run's paperwork; follows this round's yellow 1 |
| ⬜ 3 | a non-citation ledger coordinate whose file walks before the file holding its line is hashed before that line moves | `skills/evidence-check/scripts/evidence_check.py:3080` | deferred a new issue against `cited_first` | p10 executed at the base and the target: identical but for the remedy text; #772's class, not added by this branch |
| 🟢 | round 1's yellow 1 is closed for its shape — a held coordinate no place holds, on a dated row, is named and handed a BROKEN part | `skills/evidence-check/scripts/evidence_check.py:3596` | confirmed | p1 re-run with the freeze and without it; the planted case red at 0667af2e and green at fceff8ce; its neighbouring shape is this round's yellow 1 |
| 🟢 | round 1's yellow 2 is closed — a coordinate naming a line of a ledger the run writes is never judged held | `skills/evidence-check/scripts/evidence_check.py:3357` | confirmed | p2 re-run unnarrowed and under two narrowings; the planted case red at 0667af2e and green at fceff8ce; citation, other-checkout and frozen-arm kinds read |
| 🟢 | round 1's yellow 3 is closed — the home names every `left` reason | `docs/the-evidence-ledger.md:189` | confirmed | read against all seven `left` lines in `reverify` and against the S12 tree; the pin is present |
| 🟢 | round 1's white 4 was answered at b5dbc88c | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/phases/phase-3.md` | confirmed | both rows re-dated after the fix and the grounds qualified; the same rows rest on this round's yellow 1, which is the second row above |
| carried | round 1's white 5 — the family view built twice per run | `skills/evidence-check/scripts/evidence_check.py:3234` | confirmed | read: the fix range adds no third pass |
| 🟢 | `changelog.md` says what ships at the target | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md` | confirmed | each bullet read against the code; bullet 1's new sentence is exact once this round's yellow 1 lands and needs no edit |
| 🟢 | `overview.md`'s two new divergence rows and `spec.md` D1's inferred sentence | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | confirmed | read against the fix range |
| ❓ | the full suite, the repository lint and the typecheck at the target | the branch | ❓ out of verified scope | not this round's to run; the sealer answers it, after the rounds settle |

## Paste-ready fixes

```python
        for offset, key, m in unplaced:
            if bisect.bisect_right(starts, offset) not in joined:
                continue
            repo, rel = place(root, maps, default_repo, m.group("path"))
            body = read(os.path.join(repo, rel)) if repo is not None else None
            places, resurrected = (
                resolve_unit(rel, m.group("locator"), body)
                if body is not None
                else ([], False)
            )
            if any(
                recorded_here(rel, body, p, m.group("hash"), m.group("claim"))
                for p in places
            ):
                # One of its places holds what this row recorded, which the
                # check calls OK: the dated row is a newest reading that holds
                # it, as on a row no family holds (round 2).
                still(key, m.group("hash"))
                continue
            walked(
                key,
                m.group("hash"),
                None,
                f"  {coordinate_of(m)}  {left_because(places, resurrected)} — left",
            )
            pending.append((offset, coordinate_of(m), m.group("hash"), None))
```
```python
def test_a_held_coordinate_one_of_whose_places_holds_it_rides_a_dated_row_silently(
    repo, capsys
):
    """Round 2, yellow 1. A records `handler` at what one of its two places
    holds, and carries `other`, which drifted. Dated for `other`, A becomes
    the newest reading of `handler` at content one place holds, which the
    check calls OK: the run says nothing about `handler` and records no
    BROKEN for it, as on a row no family holds. Red at fceff8ce, which named
    it `left` and handed MOVES a BROKEN part."""
    o0 = unit_hash(repo, "src/service.py", "other")
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    places, _ = ec.resolve_unit("src/service.py", "handler", TWICE)
    x, y = places[0]
    held = ec.content_hash(ec.gfm_lines(TWICE)[x - 1 : y])
    a = fragment(
        repo,
        [re_read_of(r, held, "2026-02-01", extra=f", `src/service.py#other@{o0}`")],
        name=A_ITEM,
    )
    (repo / "src" / "service.py").write_text(
        TWICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    moves = []
    ec.reverify([str(a)], str(repo), {}, None, "2026-04-01", moves)
    out = capsys.readouterr().out
    assert "src/service.py#handler" not in out, out
    assert [m for m in moves if m[2] == "src/service.py#handler"] == [], moves
    assert run(["--strict", "."], repo).returncode == 0
```

## Executed probes

| What was run | Result |
|---|---|
| p1, round 1's: a held coordinate no place holds, on a row dated for `other`, with the freeze and without it, at the base, 0667af2e and fceff8ce | fceff8ce: a `left` line and `('src/service.py#handler', '96c68feb', None)` in MOVES at both arms, the (ii) remedy without the freeze; 0667af2e: neither; `--strict` after exits 2 at all three |
| p2, round 1's: a held non-citation coordinate naming R1's line, unnarrowed and narrowed to B and to R1 with B, at the three SHAs | unnarrowed: fceff8ce exits 0 and `--strict` 0, the base's bytes; 0667af2e exits 1 and 2. Narrowed to B: identical at all three. Narrowed to R1 with B: identical but for the remedy text (⬜ 3) |
| p6: a held two-place coordinate one place holds, on a row dated for `other`; alone and beside a newer holder; with the freeze and without it; at the three SHAs | fceff8ce: a `left` line and a BROKEN part `('src/service.py#handler', 'd06d1b56', None)` in all four variants; the base and 0667af2e: neither; `--strict` after exits 0 everywhere |
| p7: the 🟡 1 fix applied in the clone; the new case, dated and undated, against the fix and against fceff8ce | dated: green with the fix, red at fceff8ce; undated: green at both |
| p8: the three narrow modules with the 🟡 1 fix applied in the clone | 691 passed |
| p9: the two planted cases at 0667af2e and fceff8ce | 0667af2e: both red (the dated arm and the ledger-line case); fceff8ce: all three arms green |
| p10: a non-citation ledger coordinate in a file walked before the line it names moves, unnarrowed, at the base and fceff8ce | both: exit 1, `--strict` exits 2, and a second run clears it; only the remedy text differs |
| p11: non-citation ledger coordinates inside a family in this repository | one, on `seal/ledger.md`'s header, with one reading |
| the three narrow modules at the target, unpatched | not run by this round: the orchestrator's run (753 with the three hygiene modules) is the record |
| `bin/evidence-check --strict .` in the worktree at the target, with this report on disk | exit 0 (see the proof block) |
| the full suite, the lint and the typecheck (the broad gate) | not yet |

```
reverify exit 0
  src/service.py#handler  its row is dated by this run, and no one place holds it — left
  src/service.py#other  d589648e -> 7df296bc
1 row re-verified
  dated 2026-04-01 — 1 row whose hash moved, each once:
    seal/ledger/2000000001-a.md:1  Re-read · R1 · handler adds one
strict-after exit 0
MOVES for handler: [('src/service.py#handler', 'd06d1b56', None)]
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3344` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3343` | round 1's 🟡 2 — fixed |
| round-1 | `docs/the-evidence-ledger.md:186` | round 1's 🟡 3 — fixed |
| round-1 | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | round 1's ⬜ 4 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3221` | round 1's ⬜ 5 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3563` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3037` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3957` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-evidence-ledger.md:174` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md` | round 1's 🟢 — confirmed |
| round-1 | the branch | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a non-citation ledger coordinate whose file walks before the line it names moves is left stale by one run (⬜ 3) | a new issue against `cited_first`'s walk order, #772's class | the orchestrator, who files it in the 0.18.3 triage; the evidence-check maintainer answers it |
