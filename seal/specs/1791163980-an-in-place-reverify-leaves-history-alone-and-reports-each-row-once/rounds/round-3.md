# 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once — review round 3

| Field | Value |
|---|---|
| Target SHA | 7f4672a3e155b98d65c23385914f67ba70803dd3 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #801 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a regression against the base: a held coordinate whose only place is unsure is left BROKEN on a dated row where the base re-pointed it, and `--strict` goes red where the base was clean); 🟡 2 (pre-existing at the base: a claim tie is BROKEN to the check and silent to `reverify`, fixed at both sites or deferred whole) |
| Loses a record or crashes | no — nothing written is lost and nothing crashes; 🟡 1 writes a BROKEN pact-change part a second run contradicts, and 🟡 2 omits one, both in narrow shapes |

- [ ] Pass

## What this round was asked

The verifying round over round 2's fixes (930078de..4d510880), and the last round this item gets: rounds 1–2's verdicts inherited and checked (round 2's p6 and round 1's p1 and p2 re-run at the target, the base and the earlier targets); the `unplaced` loop judged by construction over what a held coordinate's places can hold × dated or undated × freeze, against the check's verdict and `left_because`'s wording; the `still` call c4c6a73e removed as equivalent; A1, the re-read 0.4.0:59 and 0.18.2:129 claims, and `changelog.md` against the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a held coordinate whose only place is one the declaration rule is unsure of, on a row the run dates, is named `left` and handed a BROKEN part where the base re-pointed it onto its one provable destination; `--strict` after exits 2 where the base exits 0, and the loop's line drops `, and no destination is provable` | `skills/evidence-check/scripts/evidence_check.py:3599` | open | C10 executed at a3aa139a, fceff8ce and the target; a regression against the base since phase 1; the fix and its case executed in the clone, red at the target and green with the fix, 693 passed in the three narrow modules |
| 🟡 2 | a claim coordinate whose minor content two or more places hold is BROKEN to the check and silent to both `reverify` paths; on a dated held row the run's own date turns the family BROKEN with no line | `skills/evidence-check/scripts/evidence_check.py:3382` | open | S1 and C4 executed at a3aa139a, fceff8ce and the target; pre-existing at the base in the ordinary path, which the loop copies; fceff8ce named the dated cell and round 2's fix silenced it again; the fix executed in the clone, 906 passed in four modules |
| ⬜ 3 | an unsure place with a claim that does not hold the row's hash is left with a BROKEN part, where the check reads it DRIFTED | `skills/evidence-check/scripts/evidence_check.py:3394` | deferred a new issue against `reverify`'s unsure-place rule | C8 executed, identical at the base; the round-6 never-write rule against `classify`'s round-8 DRIFTED; a design question, not this item's |
| ⬜ 4 | the loop's comment, the overview's grounds, spec D1, A1 and the `0.4.0.md:59` re-read say a place holding the recorded content is OK to the check, or that every flagged row gets a line, which a claim tie contradicts | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | open | a correction to the run's paperwork; follows 🟡 1 and 🟡 2 |
| 🟢 | round 2's blocking finding is closed — a held two-place coordinate one place holds is silent on a dated row | `skills/evidence-check/scripts/evidence_check.py:3609` | confirmed | p6 re-run at four SHAs, both variants, both freeze arms; the planted cases red with 930078de's script and green at the target |
| 🟢 | the `still` call removed in c4c6a73e was equivalent | `skills/evidence-check/scripts/evidence_check.py:3613` | confirmed | read: one key takes one branch on every walk; executed: the target and a copy with the call restored identical in 49 cell-arms |
| 🟢 | round 2's white 2 was answered at 4d510880 | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | confirmed | A1's qualifier, the re-stamp at the current `reverify` hash and the phase-3 grounds read; the remainder is ⬜ 4 |
| carried | round 2's white 3, the walk-order shape | `skills/evidence-check/scripts/evidence_check.py:3080` | deferred #806 | already deferred in round 2; #806 is open; this range does not touch `cited_first` |
| 🟢 | round 1's yellow 1 is closed — a held coordinate no place holds, on a dated row, is named in the check's terms | `skills/evidence-check/scripts/evidence_check.py:3617` | confirmed | p1 re-run at four SHAs, both freeze arms |
| 🟢 | round 1's yellow 2 is closed — a held ledger-line coordinate is re-stamped as at the base | `skills/evidence-check/scripts/evidence_check.py:3358` | confirmed | p2 re-run unnarrowed at four SHAs |
| carried | round 1's yellow 3 and white 5 | `docs/the-evidence-ledger.md:189` | confirmed | this range touches neither the sentence nor the family view |
| 🟢 | `0.18.2.md:129` (C1) holds of what `reverify` calls BROKEN | `seal/releases/0.18.2.md:129` | confirmed | read in every probe cell; where `reverify` and the check differ the record follows `reverify`, which is 🟡 1, 🟡 2 and ⬜ 3 |
| 🟢 | `changelog.md` says what ships at the target, but for *as any such coordinate is* in C10 | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md` | confirmed | each bullet read against the code; exact once 🟡 1 lands |
| ❓ | the full suite, the repository lint and the typecheck at the target | the branch | ❓ out of verified scope | not this round's to run; the sealer answers it, after the fixes this round names land or are deferred |

## Paste-ready fixes

```python
            why = left_because(places, resurrected)
            if resurrected and m.group("claim") is None:
                # An unsure place with no claim is no place, and the ordinary
                # path heals it onto the one destination that reconstructs
                # the recorded hash; so does this (round 3).
                raw_path, locator = m.group("path"), m.group("locator")
                hashes, _, _ = content_matches(
                    home, at, locator, m.group("hash"), scan_cache.setdefault(home, {})
                )
                if len(hashes) == 1:
                    path, name, (a, b) = hashes[0]
                    target = body if path == at else read(os.path.join(home, path))
                    new_raw = (
                        raw_path
                        if path == at
                        else (raw_path[: len(raw_path) - len(at)] + path)
                    )
                    shown = f"#{name}" if path == at else f"{path}#{name}"
                    new_hash = content_hash(gfm_lines(target)[a - 1 : b])
                    if new_hash != m.group("hash"):
                        pending.append(
                            (offset, coordinate_of(m), m.group("hash"), new_hash)
                        )
                    else:
                        still(key, new_hash)
                    kept.append(
                        (
                            m.start("path"),
                            m.end("hash"),
                            new_raw
                            + text[m.end("path") : m.start("locator")]
                            + name
                            + text[m.end("locator") : m.start("hash")]
                            + new_hash,
                            (
                                key,
                                f"  {raw_path}#{locator} -> {shown}  "
                                "(identical content)",
                            ),
                        )
                    )
                    continue
                why += ", and no destination is provable"
            walked(key, m.group("hash"), None, f"  {coordinate_of(m)}  {why} — left")
            pending.append((offset, coordinate_of(m), m.group("hash"), None))
```
```python
LEFT_BEHIND = (
    "func main() {\n    return handler(1)\n}\n\nfunc other(x) {\n    return x * 2\n}\n"
)


def test_a_held_coordinate_with_an_unsure_place_on_a_dated_row_heals_to_its_destination(
    repo, capsys
):
    """Round 3. B holds `handler` in `src/lib.go` through the one place the
    declaration rule is unsure of, the call a move left behind; A records the
    unit itself, which now lives in `src/moved.go`, and carries `other`,
    which drifted. Dated for `other`, A becomes the newest reading of
    `handler`, and the run heals it onto the one destination that
    reconstructs A's hash, as it heals any such coordinate: `--strict` reads
    the tree clean. Red at 7f4672a3, which named it `left` and handed MOVES a
    BROKEN part."""
    lib, dest = "src/lib.go", "src/moved.go"
    (repo / "src" / "lib.go").write_text(LEFT_BEHIND, encoding="utf-8")
    unit = "func handler(x) {\n    y := x + 2\n    return y\n}\n"
    (repo / "src" / "moved.go").write_text(unit, encoding="utf-8")
    places, unsure = ec.resolve_unit(lib, "handler", LEFT_BEHIND)
    assert unsure and len(places) == 1, places
    x, y = places[0]
    held = ec.content_hash(ec.gfm_lines(LEFT_BEHIND)[x - 1 : y])
    a_at = unit_hash(repo, dest, "handler")
    o0 = unit_hash(repo, lib, "other")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `{lib}#handler@{line_hash('    return handler(0)')}` "
            "| read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    a = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{lib}#handler@{a_at}`, "
            f"`{lib}#other@{o0}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name=A_ITEM,
    )
    b = fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `{lib}#handler@{held}` "
            "| read | 2026-03-01 | Re-read 2026-03-01 |"
        ],
        name=B_ITEM,
    )
    (repo / "src" / "lib.go").write_text(
        LEFT_BEHIND.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    moves = []
    ec.reverify([str(a), str(b)], str(repo), {}, None, "2026-04-01", moves)
    out = capsys.readouterr().out
    assert f"{lib}#handler -> {dest}#handler  (identical content)" in out, out
    assert [m for m in moves if m[3] is not None and m[4] is None] == [], moves
    assert f"`{dest}#handler@{a_at}`" in a.read_text(encoding="utf-8")
    assert run(["--strict", "."], repo).returncode == 0
```
```python
                hit = [
                    p
                    for p in places
                    if recorded_here(rel, body, p, m.group("hash"), claim)
                ]
                if hit and (len(hit) == 1 or claim is None):
```
```python
            hit = [
                p
                for p in places
                if recorded_here(at, body, p, m.group("hash"), m.group("claim"))
            ]
            if hit and (len(hit) == 1 or m.group("claim") is None):
```

## Executed probes

| What was run | Result |
|---|---|
| p6, round 2's: a held two-place coordinate one place holds, on a row dated for `other`; A alone and beside a newer holder; freeze and not; dated and undated; at a3aa139a, 0667af2e, fceff8ce, 7f4672a3 | target silent with no MOVES part in every arm; fceff8ce alone names it and hands `('src/service.py#handler', 'd06d1b56', None)`; `--strict` after 0 everywhere |
| p1, round 1's: a held coordinate neither of two places holds, dated, at the four SHAs | target: `2 places, none holding the recorded content — left`, BROKEN part `96c68feb`; `--strict` after 2 with A BROKEN at all four; 0667af2e alone silent |
| p2, round 1's: a held ledger-line coordinate, unnarrowed, at the four SHAs | target and fceff8ce exit 0 and `--strict` 0, writing the base's three files; 0667af2e exits 1 and 2 |
| the `unplaced` matrix: 13 cells × freeze and not × dated and undated, at the four SHAs and the target with `still` restored | as the table *The `unplaced` loop, cell by cell*; the target and the `still` copy identical in all 49 cell-arms |
| S1: a claim row two places hold, no family, at a3aa139a, fceff8ce, target | `--strict` 2 before and after, BROKEN ambiguous; `--reverify` exits 0 and prints nothing for `handler`, at all three |
| C10: an unsure place B holds, A's content one destination elsewhere, dated, at a3aa139a, fceff8ce, target | base re-points A to `src/moved.go#handler`, `--strict` after 0; fceff8ce and target leave A with a BROKEN part, `--strict` after 2 |
| the planted held-coordinate cases (`-k "held_coordinate or held_ledger"`, six cases) at the target and with 930078de's script | target: 6 passed; 930078de: the two round-2 cases red, 4 passed |
| 🟡 1's fix in the clone: the matrix, C10, the new case, and the three narrow modules | C10 heals, `--strict` 0; C7 takes the base's wording; 47 other cell-arms identical to the target; the new case red at the target, green with the fix; 693 passed |
| 🟡 2's fix on top, in the clone: the matrix, S1, and the three narrow modules with `tests/test_a_row_points_by_content.py` | S1 and C4 named with the BROKEN part; every other cell-arm unchanged; 906 passed |
| the three narrow modules at the target, unpatched | not run by this round: the orchestrator's run (754 with the three hygiene modules) is the record |
| `bin/evidence-check --strict .` in the worktree at the target, with this report on disk | exit 0 (see the proof block) |
| the full suite, the lint and the typecheck (the broad gate) | not yet |

```
C10 at the target, --reverify --checked 2026-04-01 .
  src/lib.go#handler  only a place the declaration rule is unsure of — left
  seal/ledger/2000000001-a.md:1  Re-read · R1 · handler adds one
--strict after: exit 2
  BROKEN   src/lib.go#handler  the declaration rule is unsure of the only place it found, and none holds the recorded content — 2-2@50d94e97; record one by hand if it is still the unit — identical content at src/moved.go#handler (moved?)

C10 at a3aa139a
  src/lib.go#handler -> src/moved.go#handler  (identical content)
--strict after: exit 0
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
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3596` | round 2's 🟡 1 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3080` | round 2's ⬜ 3 — deferred |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3357` | round 2's 🟢 — confirmed |
| round-2 | `docs/the-evidence-ledger.md:189` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/phases/phase-3.md` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3234` | round 2's carried — confirmed |
| round-2 | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| an unsure place with a claim is handed a BROKEN part where the check reads DRIFTED (⬜ 3) | a new issue against `reverify`'s unsure-place rule beside `classify`'s round-8 DRIFTED | the orchestrator files it in the 0.18.3 triage; the evidence-check maintainer decides the design |
| a non-citation ledger coordinate whose file walks first is left drifted (round 2's white 3) | #806 | already deferred in round 2; the evidence-check maintainer |
