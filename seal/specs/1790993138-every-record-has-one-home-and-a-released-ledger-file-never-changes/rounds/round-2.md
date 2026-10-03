# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — review round 2

| Field | Value |
|---|---|
| Target SHA | 30369bde53b1c9d2ceb52ad5374f86003bfdff2a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 736 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 10 (the home, the changelog and a comment state a guarantee the per-coordinate rule does not give), 🟡 11 (a folded double correction cannot be cleared), 🟡 12 (a narrowed `--reverify` names nothing owed while the family reads DRIFTED) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 is a verifying round. It targets `30369bde` over round 1's fix range `f50f5f05..b726c91b`. It was asked:
- whether each of round 1's fixes holds, with 🟡 2 checked as built to the orchestrator's rule (newest `Checked` date per coordinate, ties a union);
- whether the units the fixes created are correct: the date selection with missing or malformed dates, `released_drift` following the family, the double-correction notice, the `CITATION` regex, the full-cell fallback, and the new cases;
- whether 🟡 2 holds against S6, S7 and the release fold, and what the second lander re-stamps after the sibling merges;
- whether M2 still reads 1,083 rows with 0 misreads;
- whether the ledger corrections and re-stamps hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding is closed — `--into` slices the line the match was made on | `skills/evidence-check/scripts/evidence_check.py:3267` | confirmed | closed at `d971ba27`; executed: its case red at `f50f5f05`, green at HEAD |
| 🟢 | round 1's finding 2 is closed — only the newest-dated readings of a coordinate count, ties a union, as the orchestrator decided | `skills/evidence-check/scripts/evidence_check.py:2428` | confirmed | closed at `c7ec3c23`, `1f8f001a`, `752a50a3`; executed: P1 red at `f50f5f05`; the tie case red with the tie removed |
| 🟢 | round 1's finding 3 is closed — the repair says the correction carries every coordinate | `skills/evidence-check/scripts/evidence_check.py:3285` | confirmed | closed at `01082c4f`; executed: its case red at `f50f5f05` |
| 🟢 | round 1's finding 4 is closed — two corrections of one fragment-stage row are named | `skills/evidence-check/scripts/evidence_check.py:2400` | confirmed | closed at `c730be61`; executed: red at `f50f5f05`; the folded case is new finding 11 |
| 🟢 | round 1's finding 5 is closed — a closing-pipe citation is keyed by the citation | `skills/evidence-check/scripts/correction_check.py:579` | confirmed | closed at `fe6b06f6`; executed: both cases red at `f50f5f05`; M2 1,083 rows, 0 misread; 12 of 12 tree rows keyed right |
| 🟢 | round 1's finding 6 is closed — row 25 is a `Corrected ·` row whose claim holds | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:25` | confirmed | answered at `5604b390`; read against `check_text` and `family_view`; no other row cites the 0.4.0 row |
| 🟢 | round 1's finding 7 is closed — the §3 drift row names `--into` and the second fold | `docs/release-checklist.md:199` | confirmed | closed at `f4b1d18e`; executed: its case red at `f50f5f05`; read against `fold_ledger.py` and the freeze |
| 🟢 | round 1's finding 8 is closed — REMOVED-not-re-pointed is qualified for the freeze | `docs/the-evidence-ledger.md:37` | confirmed | closed at `2f01c24b`; read |
| 🟢 | round 1's finding 9 is closed — the whole-cell fallback names R1 in round 1's shape | `skills/evidence-check/scripts/evidence_check.py:2186` | confirmed | closed at `c4b06aae`; executed: its case red at `f50f5f05`; the comment is new finding 14 |
| 🟡 10 | the home, the changelog and the code comment say no pair of hashes nobody read together is accepted; S6 and a same-day tie accept one | `docs/the-evidence-ledger.md:111`, `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/changelog.md:20`, `skills/evidence-check/scripts/evidence_check.py:2004` | open | executed: (h2, o2) from two rows reads 6 OK, exit 0; the tie reads 8 OK, exit 0 |
| 🟡 11 | once two corrections of one row have folded, the notice cannot be cleared: a third correction retiring one leaves both named | `skills/evidence-check/scripts/evidence_check.py:2404` | open | executed: exit 2 before and after the retiring row; exit 0 with the fix in the clone |
| 🟡 12 | `--reverify` narrowed with `--ledger` to a released file reports nothing owed while the family reads DRIFTED | `skills/evidence-check/scripts/evidence_check.py:3195` | open | executed: `0 written · 0 left`, exit 0, strict exit 2 after; with the fix 1 written, strict exit 0 |
| ⬜ 13 | a `Checked` date the calendar does not have outranks every later reading | `skills/evidence-check/scripts/evidence_check.py:2435` | open | executed: `2026-13-45` outranks the `--into` row it reported written |
| ⬜ 14 | the whole-cell fallback's comment claims a line-start property the substring match does not test | `skills/evidence-check/scripts/evidence_check.py:2186` | open | executed: R2 with a cell equal to R1's first cell, `citation_for` → None |
| ⬜ 15 | the test module's docstring still states the plain union | `tests/test_a_released_row_is_read_again_in_a_fragment.py:16` | open | read |

## Paste-ready fixes

```markdown
against it. The cost is a re-read, never a question. What it buys is that a
coordinate is held to its newest reading, so a revert to content a newer
reading superseded is caught. Coordinates are still judged one at a time, as
the halves rule judges units: two branches re-reading different units of one
row leave a pair no single reading recorded, and it reads OK, because each
side read the unit it edited. A same-day pair of readings from two branches is
a union, so a revert to either reads OK.
```
```markdown
  of them recorded what the code holds now, and DRIFTED when none did. Two
  branches that edited the same unit still leave the row DRIFTED, and code
  reverted to a hash only a superseded reading recorded reads DRIFTED too.
  A `Corrected ·` row supersedes the row it cites, and a released row
  corrected by two or more rows names each of them DRIFTED until one claim
  is kept.
```
```python
# neither matches and the row is DRIFTED. The cost: content back at a hash
# only an older reading recorded reads DRIFTED, a partial revert and a whole
# one alike, and costs a re-read, never a question. Coordinates are still
# judged one at a time, so readings of two units on two rows combine into a
# pair neither row recorded (round 1, 🟡 2; round 2, 🟡 10). A `Corrected ·` row supersedes
```
```python
# skills/evidence-check/scripts/evidence_check.py, family_view
    for keys in corrected_by.values():
        # A correcting row a later `Corrected ·` row supersedes is no longer
        # a claim: that later row is the repair once both have folded, where
        # neither can be edited (round 2, 🟡 11).
        keys = [k for k in keys if k not in superseded]
        if len(keys) < 2:
            continue
```
```markdown
read them together and keep one claim. The second branch cannot cite the
first one's row before the fold, so the repair is one row merging the two.
Once both have folded, a `Corrected ·` row citing one of them retires it.
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_a_folded_double_correction_is_cleared_by_retiring_one(repo):
    """Both corrections folded, so neither can be edited: a third
    `Corrected ·` row citing one of them retires it, and the notice goes
    (round 2, 🟡 11)."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"],
    )
    cite = citation(r, "R1 · handler adds one")
    sec = "### 2000000001-a-later-item"
    c1, c2 = (
        f"| Corrected · handler adds {n} | `{cite}`, `src/service.py#handler@{h}` "
        "| read | 2026-02-01 | Corrected 2026-02-01 |"
        for n in ("two", "three")
    )
    released(repo, [c1, c2], version="0.2.0", section=sec)
    frozen(repo, "0")
    assert run(["--strict", "."], repo).returncode == 2
    retire = citation(c2, "Corrected · handler adds three", version="0.2.0", section=sec)
    fragment(
        repo,
        [
            f"| Corrected · handler adds two, as the other row says | `{retire}`, "
            f"`src/service.py#handler@{h}` | read | 2026-03-01 | Corrected 2026-03-01 |"
        ],
        name="3000000001-y",
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout
```
```python
# skills/evidence-check/scripts/evidence_check.py, released_drift
            for key, m, status, detail in graded:
                if ledger_kind(root, view.files[key[0]][0]) != "released":
                    continue
                if status == "BROKEN":
                    broken.append((where(key), coord, detail))
                    break
                # DRIFTED, or OK and outranked by a newer reading holding
                # other content: the family owes a re-read either way. That
                # newer reading may sit in a fragment LEDGERS left out, which
                # nothing re-stamped (round 2, 🟡 12).
                drifted.setdefault(top, {}).setdefault(coord, m)
                break
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_a_narrowed_into_re_reads_a_family_a_fragment_outranks(repo):
    """The newest reading sits in a fragment `--ledger` leaves out, so no
    in-place re-stamp reaches it: `--into` still owes the released row a
    re-read (round 2, 🟡 12)."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"],
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h2}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name="2000000009-z",
    )
    frozen(repo, "0")
    (repo / "src" / "service.py").write_text(SERVICE)
    assert run(["--strict", "."], repo).returncode == 2
    out = run(
        ["--reverify", "--into", INTO, "--checked", "2026-03-01",
         "--ledger", "seal/releases/0.1.0.md", "."],
        repo,
    )
    assert "1 citing row written" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 0
```
```python
# skills/evidence-check/scripts/evidence_check.py, beside date_column
def calendar_date(text):
    """Whether TEXT, a `CHECKED_RE` match, is a date the calendar has: a
    `2026-13-45` would otherwise outrank every reading after it (round 2)."""
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return True


# family_view, checked
        found = CHECKED_RE.findall(cells[column[0]]) if column else []
        return max((d for d in found if calendar_date(d)), default="")
```
```python
    # The cell whole, with both of its pipes: it names the row where no
    # other line holds that run, which covers a first cell that also ends
    # another row's last cell (round 1, ⬜ 9). The match is a substring, as
    # `cited_row` resolves it, so a cell exactly equal to another row's cell
    # still names no row.
```
```text
  S1  a coordinate is OK when one of its newest readings in R's family -- the
      members recording it with the newest `Checked` date, ties together --
      recorded what it holds
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the three touched ledger modules at HEAD | 183 passed |
| `bin/test` on the S6/S7 module, the docs line-wrap module and the one-home module at HEAD | 42 passed |
| the same three touched modules with the four source files at `f50f5f05` | 9 failed (every case the fix pass planted), 174 passed |
| the tie removed from `family_view` (first newest reading only) | the tie case red; S6 and S7 green |
| `evidence_check.py --strict .` at HEAD | 3,786 ok, 0 drifted, exit 0 |
| M2 at HEAD: `citation_for` → fragment row → `ANCHOR_RE` → `cited_row`, and `corrections()` | 1,083 rows, 0 without a citation, 0 wrong rows, 0 misread, 0 fallback of either kind |
| `corrections()` against `ANCHOR_RE` on every `Corrected ·` row in the tree | 12 of 12 keyed on the citation |
| date scan of every anchored ledger row | 1,146 rows: 0 without a date, 0 invalid, 0 after 2026-10-03 |
| sibling merges (#647, #718, #716, all three) into `30369bde`, then `--strict` and `correction-check --range` | 0 conflicts; drifted 6, 3, 0, 9; correction-check exit 0, each exempt |
| the second lander's repair in the all-three merge: `--reverify --into <this fragment> --checked 2026-10-03` | 8 hashes on 7 rows re-stamped, 0 written, 0 left; ledger 0 drifted; records arm 4 refused (#647's records name a removed unit) |
| `fold_ledger.py --version 0.18.0` at HEAD, then `--strict` | 3,786 ok, 0 drifted |
| the same fold over the all-three merge with the repair applied | 4 fragments folded; 3,991 ok, 0 drifted, exit 0 |
| P1: two rows each re-reading one unit; then a same-day tie (🟡 10) | exit 0, 6 OK; exit 0, 8 OK |
| P2: two corrections folded, then a third retiring one (🟡 11) | exit 2, exit 2; `--into` 0 written, exit 0; with the fix: exit 2, exit 0 |
| P3: a fragment's newer reading, code reverted, `--reverify` narrowed to the release file (🟡 12) | strict exit 2; `0 written · 0 left`, exit 0; strict exit 2; with the fix: 1 written, strict exit 0 |
| P4: a released row dated `2026-13-45` (⬜ 13) | `--into` 1 written, strict exit 2; with the fix: exit 0 |
| P5: R2 with a cell equal to R1's first cell (⬜ 14) | `citation_for` → None |
| the four ledger modules with the fixes for 11, 12 and 13 applied in the clone | 186 passed |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the second lander re-stamps 7 rows (6 of this fragment, 1 of #718's) and clears #647's 4 records-arm refusals of a unit this branch removed | the handoff to whichever of #647, #718 and #715 lands second | the orchestrator of the 0.18.0 run |
