# Round 2 report — an in-place `--reverify` leaves history alone and reports each row once

| Field | Value |
|---|---|
| Round | 2 (verifying round 1's fixes) |
| Target SHA | fceff8ce |
| Fix range checked | fa8a5c3c..b5dbc88c, 3 commits |
| Base | `release/v0.18.3` at a3aa139a |
| Pull request | #801 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

## What this round was asked, and what it found

The target is round 1's fix range. For each verdict round 1 closed, the
question is whether it is actually closed, and whether the fix range
introduced a regression. The two new behaviours are judged by construction
across round 1's axes plus coordinate kind.

Round 1's three yellow findings are closed for the shapes they named:

- p1 now prints a `left` line and hands MOVES a BROKEN part, with the freeze
  and without it.
- p2 exits 0 and `--strict` exits 0, as at the base.
- The ledger home's sentence names every `left` reason the code prints.

The fix for round 1's yellow 1 opened a neighbouring shape that neither the
base nor round 1's target had (🟡 1 below). A held coordinate whose unit has
two places, one of which holds what the row recorded, is now named `left`
and handed a BROKEN pact-change part on a row the run dates. `--strict`
reads that coordinate OK before and after the run. Two paperwork items
follow from it (⬜ 2). One walk-order shape surfaced while checking the
narrowed run. It is identical at the base and outside this item, so it is
deferred (⬜ 3).

The smith's account was read in full: the fix-range commit messages, the
extended A1 row, the corrected phase-3 grounds, the new rows in
`overview.md`, the sentence fed back into `spec.md`, and the changelog. Each
claim used below was checked against the code at the target.

## Findings from execution

### 🟡 1 — a held two-place coordinate that one place still holds is named `left` and recorded BROKEN on a row the run dates

`skills/evidence-check/scripts/evidence_check.py:3596-3605`, the loop over
`unplaced` that round 1's yellow 1 fix added.

The guard at `evidence_check.py:3362` sends a held coordinate to `unplaced`
whenever `current_hash` is None. `current_hash` is None for any unit with
more than one place, whether or not one of those places holds the recorded
content. On a dated row the new loop then names the coordinate `left` and
appends a BROKEN part, and it never asks what the ordinary path asks at
`evidence_check.py:3381`: does one of the places hold what this row
recorded? There `recorded_here` answers yes, and the coordinate is
`still` — silent and not recorded, because the check calls it OK. The base
and round 1's target both stayed silent for this coordinate. The target
does not.

**Probe p6 (executed).** A, dated 2026-02-01, records `handler` at the hash
of the first of its two places, and records `other`. `other` then drifts.
Two variants were run: A alone, and A beside a newer B holding the same
hash. Each was run with the freeze and without it, through
`--reverify --checked 2026-04-01 .`, at the base, round 1's target and this
target. MOVES was read from the same run in-process.

| | base a3aa139a | round 1 0667af2e | target fceff8ce |
|---|---|---|---|
| line for `handler` | none | none | `its row is dated by this run, and no one place holds it — left` |
| MOVES for `handler` | none | none | `('src/service.py#handler', 'd06d1b56', None)`, a BROKEN part |
| `--reverify` exit | 0 | 0 | 0 |
| `--strict` after | 0 | 0 | 0 |

The same holds in all four variants. So the run says the coordinate has no
place holding it, and `--strict` says it is OK. The printed reason is false,
because one place does hold it.

**Why it matters.** The MOVES part goes to `record_pact_changes`. In a
signatory repository whose row cites a pact clause, that writes a BROKEN row
into `seal/pact-changes/<item>.md`, a permanent record, for a coordinate the
check never flagged (read: `record_pact_changes` keeps every part whose two
hashes differ, and `(d06d1b56, None)` differs). The `left` line also
contradicts the check's verdict. `left_because`'s own docstring rules that
out: *the two commands must never describe one row differently*. This is
also the shape `seal/releases/0.4.0.md:59` promises never happens (⬜ 2).

The new line's wording is a second, smaller instance of the same rule. For
the shape round 1 named, the check says
`locator is ambiguous — 2 places … (none holds the recorded content)`, the
base's `left` line said `2 places, none holding the recorded content`, and
the target says `its row is dated by this run, and no one place holds it`.
The fix below uses `left_because`, which closes both instances.

**The fix (applied in the clone, p7 and p8).** In the `unplaced` loop, ask
`recorded_here` of each place before naming the coordinate. Read it as
unchanged where one place holds the recorded content, and otherwise name it
with `left_because`'s reason. With the fix:

- the false-BROKEN shape is silent and records nothing;
- round 1's p1 shape still prints a `left` line (now `2 places, none
  holding the recorded content — left`) and still hands MOVES the BROKEN
  part;
- the three narrow modules pass (691), and the new case below is red at the
  target and green with the fix.

### Round 1's findings, re-checked at the target

**Round 1's yellow 1 — closed for its shape** (p1 re-run, executed). With
the freeze and without it, A's `handler` at h1 (held in neither place) on a
row dated for `other` now prints a `left` line and hands MOVES
`('src/service.py#handler', '96c68feb', None)`. Without the freeze, the
family line reads *this run left src/service.py#handler where it stands, and
the line naming it above says why*. That is the (ii) remedy where round 1's
target gave none. `--strict` after exits 2 with BROKEN `handler`, as at the
base. The ledger bytes match the base. The planted case
`test_a_held_coordinate_with_two_places_on_a_dated_row_is_left_and_named` is
red at 0667af2e and green at fceff8ce (executed).

**Round 1's yellow 2 — closed** (p2 re-run, executed). Unnarrowed:
`--reverify` exits 0, R1, Q and B are re-stamped and dated, and `--strict`
after exits 0. That is byte-for-byte the base's output, where round 1's
target exited 1 and then 2. The planted case
`test_a_held_ledger_coordinate_the_run_moves_is_re_stamped` is red at
0667af2e and green at fceff8ce (executed).

**Round 1's yellow 3 — closed** (read). The sentence at
`docs/the-evidence-ledger.md:189-191` names four reasons. The code prints
seven `left` lines in `reverify`, and each maps onto one of them:

| Code (`evidence_check.py`) | The sentence |
|---|---|
| `:3374` path escapes the repository | a path outside the repository |
| `:3415` not in any known checkout | … or any known checkout |
| `:3484` the file could not be read | a file the run could not read |
| `:3475`, `:3498` `left_because`: no place, N places, an unsure place | no one place holding the unit |
| `:3603` the new dated-row line | no one place holding the unit |
| `:3513` the anchored statement is gone | a quoted statement its file no longer has |

The row left whole for want of a date cell is named by the sentence before
it. The S12 tree (`a_correction_whose_statement_is_gone`) is now covered,
and the pin *the home: every left reason* is present.

**Round 1's white 4 — answered at b5dbc88c** (read). Both re-reads were
re-dated after the fix, and the phase-3 grounds for `0.4.0.md:59` and
`0.18.2.md:129` carry the dated-row qualifier. The same two rows now rest on
this round's yellow 1 (⬜ 2).

**Round 1's white 5 — carried** (read). The fix range adds one `place` call
per held, non-citation coordinate and one set built once per run. No third
`family_view` pass was added.

### The two new behaviours, by construction

**(1) A held coordinate with no one place, on a row the run dates.** The
axes are dated or undated, freeze or no freeze, the walk it is met on, and
what the places hold.

- **Undated row.** Silent, as round 1 confirmed. p1's control and the
  planted case's undated arm are green.
- **Dated, no place holds the recorded content.** Named and BROKEN, with
  the freeze and without it (p1).
- **Dated, one place holds the recorded content.** Named and BROKEN at the
  target, wrongly (🟡 1).
- **A file walked twice** (read). `unplaced` is rebuilt each walk. A row
  first dated on walk k is named on walk k, and a later walk that dates
  nothing on that row leaves the outcome as walk k left it. That matches
  A3's fold.
- **Superseded family.** It returns before `unplaced` (`:3353`), so it is
  untouched.

**(2) A coordinate naming a line of a ledger the run may rewrite is never
judged held.** `writes` is `planned_key` over the run's own `ledgers`
(`:3240`). The judgment is at `:3357-3359`.

- **Unnarrowed** (p2). Re-stamped as at the base.
- **Narrowed so the named file is left out** (p2, `--ledger` naming B only).
  The coordinate is judged held and left. Nothing moves its line, and the
  output is identical at the base, round 1's target and this target.
- **Narrowed so both files are walked** (p2, R1 and B). The output is the
  same at all three SHAs except the remedy text. B's coordinate is left
  stale because B is walked before R1's file. That is walk order, not this
  judgment (⬜ 3).
- **A citation.** It is excluded from the judgment (`:3352`), as before.
- **A coordinate in another checkout** (read). `place` returns the mapped
  or `--default-repo` checkout, so the joined path is in `writes` only where
  the run itself writes that file. That is exactly when its line can move.
- **The frozen arm** (read). `main` hands `reverify` the fragments only
  (`:5861`). A fragment coordinate naming a released line is judged held,
  and nothing writes that line in that arm.
- **Identity rule** (read). `writes` keys on `planned_key`, as `read` keys
  the plan. A symlinked or case-variant spelling of a ledger path misses
  both. The base misses it the same way, because `read` would hash the
  on-disk line, so this is not a regression.
- **In this repository** (p11, executed). One non-citation ledger
  coordinate sits in a family, on `seal/ledger.md`'s header, with one
  reading. The exception rewrites no outranked reading here today.

### Changelog, A1, the overview and the spec

- **`changelog.md`** says what ships at the target, with one gap. *Where no
  one place holds it, it is named `left` and recorded BROKEN* is narrower
  than the target's code, which does so where one place does hold it. Once
  🟡 1 lands the sentence is exact, so it needs no edit.
- **A1** (read against the code). Every clause is true of the target's
  code. The clause *named `left` and handed MOVES a BROKEN part where it
  does* becomes wrong once 🟡 1 lands, unless it takes *unless one of its
  places holds what the row recorded* (⬜ 2).
- **`overview.md`'s two new rows and the `spec.md` D1 sentence** describe
  the fix range accurately.

## Findings from reading

### ⬜ 2 — A1's clause and two re-reads rest on 🟡 1

`seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md`,
row A1 and the `Re-read ·` rows citing `seal/releases/0.4.0.md` *"never
writes onto"* and `seal/releases/0.18.2.md` *"Corrected · C1 ·"*.

At the target, p6's shape makes `0.4.0.md:59` false. Its claim is that the
command *never contradicts the check's verdict*, and here `reverify` names
`left` a coordinate the check reads OK. The shape also writes a C1 record
row for a coordinate that is not BROKEN. Both hold again once 🟡 1 lands.
The fix moves `reverify`'s hash, so the fix pass's `--reverify --into`
re-dates every row citing it. The phase-3 grounds for those two rows and
A1's clause need the qualifier. This is a correction to the run's paperwork,
not a fix.

### ⬜ 3 — a non-citation ledger coordinate is hashed before the line it names moves, when its file walks first (deferred)

`skills/evidence-check/scripts/evidence_check.py:3080`. `cited_first`
orders the walks by citations only. A non-citation coordinate naming a line
of a ledger the run re-stamps is therefore hashed against the line before
it moves whenever its own file is walked first.

**Probe p10 (executed), unnarrowed.** B re-reads R1, and B also carries a
coordinate naming Q's line in `0.2.0.md`. Then `handler` and `other` both
change. One `--reverify` leaves B's coordinate stale: exit 1, and `--strict`
exits 2. A second run clears it.

The behaviour is identical at the base and at the target. Only the remedy
text differs. The base said *run it without `--ledger`* on an unnarrowed
run, which was #792's defect. The target names no remedy, which is D3's
*neither* case.

This is #772's class and not #785's. This branch did not add it, and round
1's yellow 2 fix restores the base's behaviour for this kind of coordinate,
walk order included.

## Regression tests to plant

Destination: `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
after `test_a_held_coordinate_with_two_places_on_a_dated_row_is_left_and_named`.
The case is in the 🟡 1 fence under *Paste-ready fixes*. I saw it red at
fceff8ce (the `left` line in the output) and green with the fix applied in
the clone (p7). The fix pass shows it red again before committing it (§15).

## Facts to feed into the evidence ledger

- A1, the clause on a held coordinate with no one place: *… and named
  `left` and handed MOVES a BROKEN part where it does, unless one of its
  places holds what the row recorded, which reads as unchanged and records
  nothing*. Add the new case to A1's grounds.
- The phase-3 grounds for `0.4.0.md:59` and `0.18.2.md:129`: at fceff8ce a
  held two-place coordinate that one place holds was named `left` and
  recorded BROKEN on a dated row. Since round 2's fix it is not, and the row
  was re-read after that fix.

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

### p6 at fceff8ce, A alone, no freeze

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a non-citation ledger coordinate whose file walks before the line it names moves is left stale by one run (⬜ 3) | a new issue against `cited_first`'s walk order, #772's class | the orchestrator, who files it in the 0.18.3 triage; the evidence-check maintainer answers it |

## Paste-ready fixes

### 🟡 1

`skills/evidence-check/scripts/evidence_check.py`, `reverify`, replacing the
body of the `for offset, key, m in unplaced:` loop (`:3596-3605`):

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

The case, in `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
after `test_a_held_coordinate_with_two_places_on_a_dated_row_is_left_and_named`:

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

Needs a fix: yes — 🟡 1 (a held two-place coordinate that one place still holds is named `left` and recorded BROKEN on a row the run dates, where `--strict` reads it OK and both the base and round 1's target were silent)
Loses a record or crashes: no — nothing written is lost and nothing crashes; 🟡 1 adds a false BROKEN part, which in a signatory repository is a wrong pact-change row rather than a lost one

The broad gate is not yet due: this round leaves 🟡 1 open, and a fix
commissioned here is this item's one reopening.

## Proof block

Ran by specseal:warden on claude-opus-5-5, in a `git clone --no-local` of
the worktree at fceff8ce under this round's scratchpad directory. The base's
and round 1's `evidence_check.py` sat beside the target's in that clone as
probe copies. The probe file and the copies carried the agent contract's
probe prefix, ran once, and were removed with the clone before handover.

Files opened:

- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/rounds/round-1.md`
  and `rounds/round-1-report.md`
- the diff fa8a5c3c..b5dbc88c of `skills/evidence-check/scripts/evidence_check.py`,
  `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
  `docs/the-evidence-ledger.md`, the work item's ledger fragment,
  `changelog.md`, `overview.md`, `phases/phase-3.md` and `spec.md`
- `skills/evidence-check/scripts/evidence_check.py` at the target:
  `left_alone`, `reverify` (whole), `current_hash`, `place`, `planned_key`,
  `read`, `file_identity`, `coordinate_of`, `left_because`, `recorded_here`,
  `family_view`'s grading, `record_pact_changes`' head, and `main`'s two
  `--reverify` arms
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: its helpers
  and the two planted cases
- `seal/releases/0.4.0.md:59` and `seal/releases/0.18.2.md:129`
- `bin/test`
