# 1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once — review round 1

| Field | Value |
|---|---|
| Target SHA | 0667af2eba55dbb6553256fb6de85ac75de0c13c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #801 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a held coordinate with no place on a row the run dates is left silently, with no BROKEN part), 🟡 2 (a held coordinate naming a ledger line the run rewrites is left stale, so `--strict` goes red where the base was clean), 🟡 3 (the ledger home's definition of the (ii) case) |
| Loses a record or crashes | no — nothing written is lost and nothing crashes; 🟡 1 leaves out one pact-change BROKEN row the base wrote, in a narrow shape, which is a missing write rather than a lost record |

- [ ] Pass

## What this round was asked

Spec compliance first against `spec.md` D1–D5 (the once-before-the-walk judgment of held and superseded coordinates; each coordinate's `left` outcome printed once after the walks; the `LEFT` remedy by reason; #781's sentence, the owner's decision; the records), then quality: the overview's four divergences on their grounds; Class 1 enumerated by construction (narrowing × walk × outranked/newest × freeze); the 30 `Re-read ·` verdicts and the `Corrected ·` over `seal/releases/0.18.2.md:91`; whether `changelog.md` says what ships at the target.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a held coordinate with no one place, on a row the run dates, is left with no `left` line and no BROKEN part, and the family line names no remedy | `skills/evidence-check/scripts/evidence_check.py:3344` | open | p1 executed at the target and the base, with the freeze and without it; MOVES read, and executed with the fix in p5 |
| 🟡 2 | a held coordinate naming a ledger line the run rewrites is left at a stale hash: `--reverify` exits 1 and `--strict` exits 2, where the base exits 0 and 0 | `skills/evidence-check/scripts/evidence_check.py:3343` | open | p2 executed at the target and the base; the premise is at `evidence_check.py:3062` and in spec D1 |
| 🟡 3 | the ledger home defines the (ii) case as two shapes, and S12's tree (a statement gone from edited code) is neither | `docs/the-evidence-ledger.md:186` | open | read against every `left` reason in `reverify` and against the S12 tree |
| ⬜ 4 | two `Re-read ·` verdicts (0.4.0:59, 0.18.2:129) hold only once 🟡 1 is fixed, and the phase-3 grounds for 0.4.0:59 need the dated-row qualifier | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | open | a correction to the run's paperwork; follows 🟡 1 |
| ⬜ 5 | `family_view` now runs twice per in-place or frozen `--reverify` | `skills/evidence-check/scripts/evidence_check.py:3221` | open | p4: 7.46 s per pass over 42 ledgers; nothing ships wrong |
| 🟢 | divergence 1: a held coordinate rides a row the run dates | `skills/evidence-check/scripts/evidence_check.py:3563` | confirmed | keeps `--strict` at the base; the narrower date-compare rule buys nothing #785 asked for; p3, the rider through a moved citation, is byte-identical to the base and inside spec §Out |
| 🟢 | divergence 2: a held two-place coordinate on a row the run does not date is left silently | `skills/evidence-check/scripts/evidence_check.py:3344` | confirmed | the family's newest reading still holds; the dated-row half is 🟡 1 |
| 🟢 | divergence 3: a `left` line exactly where the last walk left the coordinate | `skills/evidence-check/scripts/evidence_check.py:3037` | confirmed | spec Class 2 contradicts S9; `walked_move` and `owed_moves` side with S9; the 36-sequence case asserts line and BROKEN together |
| 🟢 | divergence 4: reason (i) read off the newest readings | `skills/evidence-check/scripts/evidence_check.py:3957` | confirmed | enumerated four shapes; the view is the open plan's, so the run's own dates count |
| 🟢 | D4 (#781): the home names the `Checked` date, the writer unchanged, the pin follows | `docs/the-evidence-ledger.md:174` | confirmed | the diff read, and the owner's decision found in `spec.md` and `questions.md` |
| 🟢 | the `Corrected ·` over `seal/releases/0.18.2.md:91` | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | confirmed | the released claim is false after D4; the new claim's three facts read true at the target |
| 🟢 | 28 of the 30 `Re-read ·` verdicts | `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md` | confirmed | every claim read against the target; the other two are ⬜ 4 |
| 🟢 | `changelog.md` says what ships at the target | `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md` | confirmed | each bullet read against the code |
| ❓ | the full suite, the repository lint and the typecheck at the target | the branch | ❓ out of verified scope | not this round's to run; the sealer answers it, after the rounds settle |

## Paste-ready fixes

```python
    # The files this run may rewrite. A coordinate naming a line of one is
    # graded against a line the walk can move, so the judgment made before
    # the first walk does not hold for it (#785).
    writes = {planned_key(p) for p in ledgers}
```
```python
                at, rel_ = place(root, maps, default_repo, m.group("path"))
                holds = spot[1] in held_at.get((ident, spot[0]), ()) and (
                    at is None or planned_key(os.path.join(at, rel_)) not in writes
                )
```
```python
    Judged once, never live: a walk writes ledger lines and no code, so no
    code coordinate's grading moves during the run, and only a date the run
    adds could reorder a family's readings mid-walk. A coordinate naming a
    line of a ledger the run writes is the exception, and `reverify` never
    judges it held."""
```
```python
        deferred, held_edits, unheld = set(), [], []
```
```python
                if holds and current_hash(m, root, maps, default_repo) is None:
                    # A newest reading resolves it, so this reading of it is
                    # history, unless the run dates its row (below).
                    unheld.append((m.start(), key, m))
                    continue
```
```python
        # A held coordinate with no one place, on a row the run dates: the
        # date makes that row its newest reading, so it is left as any
        # coordinate no one place holds is, named and handed to MOVES.
        for offset, key, m in unheld:
            if bisect.bisect_right(starts, offset) in joined:
                walked(
                    key,
                    m.group("hash"),
                    None,
                    f"  {coordinate_of(m)}  its row is dated by this run, and no "
                    "one place holds it — left",
                )
                pending.append((offset, coordinate_of(m), m.group("hash"), None))
```
```python
    One with no one place to re-stamp on such a row is left and named, as
    any such coordinate is.
```
```markdown
coordinate itself, on a `left` line or by leaving its row whole for want of
a date cell, the line says so and points at the line naming why, and a run
over every ledger names such a family too. Where neither is found it names
no remedy.
```
```python
            "Where the run left the coordinate itself, on a `left` line or by "
            "leaving its row whole for want of a date cell, the line says so and "
            "points at the line naming why, and a run over every ledger names "
            "such a family too.",
```

## Executed probes

| What was run | Result |
|---|---|
| p1: a held coordinate with two places on a row dated for `other`, `--reverify --checked`, with the freeze and without it, at the target and the base | target: no `left` line for `handler`, and with no freeze the family line names no remedy; base: `2 places, none holding the recorded content — left`; the same bytes at both; `--strict` after exits 2 at both |
| p2: a held non-citation coordinate naming R1's line, R1 re-stamped in place, no freeze, at the target and the base | target: `--reverify` exits 1 with a no-remedy family line, and `--strict` after exits 2; base: exits 0, and `--strict` after exits 0 |
| p3: the rider through a moved citation, no freeze, at the target and the base | byte-identical output and ledger at both; `--strict` after exits 0 |
| p4: one `family_view` pass over this repository's ledgers | 7.46 s over 42 ledgers |
| p5: the 🟡 1 and 🟡 2 fixes applied in the clone; p1, p2, and the two cases under *Regression tests to plant*; then `bin/test -q` on the three narrow modules | p1 prints the `left` line and the (ii) clause; p2 exits 0 and `--strict` exits 0; both cases green with the fixes and red with them reverted; the three modules: 687 passed |
| the three narrow modules at the target, unpatched | not run by this round: the orchestrator's run (749 with the hygiene modules) is the record |
| `bin/evidence-check --strict .` in the worktree at the target, with this report on disk | exit 0; no name in this report is reported NOT-IN-TREE |
| the full suite, the lint and the typecheck (the broad gate) | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
