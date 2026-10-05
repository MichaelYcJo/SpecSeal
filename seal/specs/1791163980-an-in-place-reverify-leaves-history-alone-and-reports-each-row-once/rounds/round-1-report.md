# Round 1 report — an in-place `--reverify` leaves history alone and reports each row once

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 0667af2e |
| Base | `release/v0.18.3` at a3aa139a |
| Pull request | #801 (draft) |
| Ran by | specseal:warden on claude-opus-5-5 |

## What this round was asked, and what it found

Spec compliance first, against `spec.md` D1–D5, then quality. The overview's
divergences were judged on their grounds, and the 31 released-row verdicts and
the changelog fragment were read against the code at the target.

D2, D3, D4 and D5 hold. D1 holds for every shape the spec's Class 1 table
names. Two shapes outside that table break it, and both are in units this
branch created:

- A coordinate the family holds that has no one place, on a row the run dates
  for another coordinate. The run leaves it silently (🟡 1).
- A coordinate the family holds that names a ledger line the run itself
  rewrites. Here the judgment made before the walk is wrong (🟡 2).

The ledger home's new sentence on reason (ii) names two ways the run leaves a
coordinate. It leaves one in more ways than that, including the case S12
pins (🟡 3). The rest is paperwork and cost.

The smith's account was read in full: `overview.md`, `phases/phase-1.md` to
`phases/phase-3.md`, `questions.md` and the fragment's rows A1–A6. Each claim
used below was checked against the code at the target. Where the account and
the code disagree, the finding says so.

## Findings from execution

### 🟡 1 — a held coordinate with no one place, on a row the run dates, is left with no line and no BROKEN part

`skills/evidence-check/scripts/evidence_check.py:3344-3347`. The guard
`if holds and current_hash(...) is None: continue` runs before the row's
dating is known. It skips the coordinate on every row. Phase 1's own rider
rule says the date makes the row the newest reading of every coordinate on
it. So on a dated row this coordinate becomes the family's newest reading, at
a hash neither place holds, and nothing in the run's output says so.

**Probe p1 (executed).** A, dated 2026-02-01, carries `handler` at h1 and
`other`. B, dated 2026-03-01, holds `handler` through one of its two places.
`other` drifts with no reading holding it. The run is
`--reverify --checked 2026-04-01 .`, with the freeze and without it.

| | base a3aa139a | target 0667af2e |
|---|---|---|
| `left` line for A's `handler` | `src/service.py#handler  2 places, none holding the recorded content — left` | none |
| family `LEFT` line, no freeze | the `--ledger` remedy (#792's defect) | *does not hold the code*, with no remedy and nothing above it to explain |
| MOVES | BROKEN part for A's `handler` (read: `pending.append(..., None)` in the `len(places) != 1` branch) | none: `continue` precedes `pending` (read, and executed in p5) |
| A after the run | dated `2026-02-01 · 2026-04-01`, `handler` still at h1 | the same bytes |
| `--strict` after | exit 2, BROKEN `handler` | exit 2, BROKEN `handler` |

The ledger ends the same at the base and at the target. What the target loses
is the line saying why `--strict` now reads A's `handler` BROKEN, and the
pact-change part for that BROKEN. Two consequences follow:

- Phase 2's Q3 answer says a family with neither reason needs a ledger the
  run cannot read. This shape also reaches the *neither* clause, from a ledger
  the run writes.
- Two of the phase-3 verdicts hold only once this is fixed. `seal/releases/0.4.0.md:59`
  says *never answers a flagged row with silence*. `seal/releases/0.18.2.md:129`
  (C1) says a record row is appended *per such row with a BROKEN coordinate*.
  In this shape the run flags A's row and says nothing, and it appends no
  BROKEN row. See ⬜ 4.

Fragment row A1 says *a held one whose reading no longer resolves to one place
is left with no line*. That is true only where the run does not date the row.

**Why it matters.** The `left` line is the only thing in the run's output that
explains a BROKEN coordinate the run's own date created. Without it, a person
sees a no-remedy `LEFT` line under the freeze-free arm and nothing at all under
the freeze, and a signatory gets no record of the BROKEN.

The fix in the fence below was applied in the clone (p5). With it the probe
prints `src/service.py#handler  its row is dated by this run, and no one place
holds it — left`, the family line takes the (ii) clause, and MOVES gets the
BROKEN part. The undated shape stays silent, and the two-place case phase 1
planted still passes.

### 🟡 2 — a held coordinate naming a ledger line the run rewrites is left at a hash the run made stale

`skills/evidence-check/scripts/evidence_check.py:3343`. `left_alone`'s premise
is in its docstring at `evidence_check.py:3062`, and the spec states it too (D1,
*Why it is judged before the walk*): *a walk writes ledger lines and no code,
so no coordinate's grading moves during the run*. `family_view` grades every
coordinate on a member's line except its citation, so it grades a
non-citation coordinate naming a ledger line as a code coordinate. #791 built
exactly that shape: `test_a_ledger_coordinate_restamped_on_two_walks_is_one_move`.

For such a coordinate the premise is false. The line it names is one the walk
re-stamps. Spec Class 1's *Coordinate kind* axis lists the citation and the
rename, and not this kind.

**Probe p2 (executed), no freeze.** R1 in `0.1.0.md` carries `handler`. Q in
`0.2.0.md` carries one coordinate, which names R1's line. It is not a citation.
Fragment B re-reads Q, dated 2026-02-01, carrying that coordinate at the same
hash, so the family holds it. `handler` is then edited, and the run is
`--reverify --checked 2026-03-01 .`.

| | base a3aa139a | target 0667af2e |
|---|---|---|
| R1 | re-stamped and dated | re-stamped and dated |
| Q's and B's coordinate naming R1's line | re-stamped, both rows dated | left at the old hash, because it is judged held and deferred |
| `--reverify` exit | 0 | 1, `LEFT seal/releases/0.2.0.md:5 Q · beside R1 — still DRIFTED: the newest reading of … does not hold the code` |
| `--strict` after | exit 0 | exit 2, DRIFTED on Q and B |

This is a regression from the base to a red `--strict`, and it comes with a
`LEFT` line naming no remedy. A second run clears it: on that run nothing
holds the coordinate, so it is re-stamped. This repository carries no row of
this shape today. I counted 9 non-citation coordinates under `seal/` across
every ledger, and all of them name lines that are not table rows
(`seal/README.md`, `seal/config.md`, `seal/ledger.md`'s header blockquote),
which no walk rewrites. The shape is one the suite already builds, and §12
asks for the class.

The fix in the fence below was applied in the clone (p5). It treats a
coordinate naming a file this run may rewrite as not held. With it, p2 exits 0
and `--strict` exits 0, as at the base. A run narrowed away from the rewritten
file still judges the coordinate held, which is right, because nothing moves
its line.

## Findings from reading

### 🟡 3 — the ledger home defines "left the coordinate itself" as two shapes, and the case S12 pins is neither

`docs/the-evidence-ledger.md:186-189`: *Where the run left the coordinate
itself, its claim quoting text the run rewrote or its row left whole for want
of a date cell, the line says so*. Written as an appositive, it reads as the
definition of the (ii) clause.

The run leaves a coordinate on every `left` reason:

- path escapes the repository;
- not in any known checkout;
- the file could not be read;
- no one place holds it;
- the anchored statement is gone from code the person edited.

`a_correction_whose_statement_is_gone`, the tree behind S10's second shape and
S12, is the last of these. Its `"x * 2"` is gone because the code changed, not
because the run rewrote anything. A person who reads that `LEFT` line and
looks the clause up finds a condition their case does not meet. The behaviour
is right, and the sentence states a narrower condition than the code uses.
Pinned in `test_the_documents_say_each_outcome_is_printed_once`.

### ⬜ 4 — two `Re-read ·` verdicts rest on 🟡 1

`seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md`,
the rows citing `seal/releases/0.4.0.md` *"never writes onto"* and
`seal/releases/0.18.2.md` *"Corrected · C1 ·"*. Each says the cited claim
holds. At the target each is false in p1's shape (see 🟡 1), and each is true
once 🟡 1's fix lands.

The fix moves `reverify`'s hash, so the fix pass's `--reverify --into` run
re-dates both rows. The phase-3 table's grounds for 0.4.0:59 (*a coordinate
its family holds is not flagged by `--strict`, so leaving it silently
contradicts no verdict*) is wrong for a dated row and needs that qualifier.
This is a correction to the run's paperwork.

### ⬜ 5 — the in-place and frozen arms now build the family view twice

`skills/evidence-check/scripts/evidence_check.py:3221-3230`. `reverify` now
calls `family_view` over every ledger the repository carries before its first
walk. `main` then calls it again, through `released_drift` in the unfrozen arm
and through `reverify_into` in the frozen arm.

Measured over this repository's 42 ledgers (p4): one `family_view` pass takes
7.46 s, so every `--reverify` here pays about that much more wall-clock time.
It is inside the plan, so F1's no-window claim is unaffected. Nothing ships
wrong. If it is ever wanted, the second pass could share the first's scan
cache, since no walk writes code. No fix is asked for this round.

## Divergences in `overview.md`, and the questions the prompt named

**1. A held coordinate rides a row the run dates.** Confirmed as the rule that
keeps `--strict` at the base's verdict. Two narrower rules exist:

- Ride only where `--checked` is later than the held coordinate's newest date.
  At an equal or earlier date the row does not become the newest reading, and
  a tie is a union.
- Do not date the row at all. That breaks R1 at `seal/releases/0.16.0.md:57`.

The narrower one changes only coordinates on a row whose date already claims
the whole row was read, so it buys nothing #785 asked for.

Does the rider rule re-open #785 for any shape? One shape re-stamps and
re-dates an outranked reading: a row dated only because its citation moved.
Probe p3, no freeze: R1 carries `handler` and `other`, outranked A and holding
B re-read `handler`, and `other` drifts. R1 is re-stamped, A's and B's
citations move, and A is dated and its `handler` rides from h1 to h2. That is
byte-identical to the base, and `--strict` exits 0. It is inside spec §*Out*,
because R1's family is drifted on `other`, and the `--checked` paragraph
covers a row whose citation hash moves. No shape outside a drifted family
re-opens #785, with one exception: 🟡 1's dated row is where the rule and
the guard beside it disagree.

**2. A held coordinate with two places prints nothing and is left.**
Confirmed where the row is not dated. On a row the run dates it is 🟡 1.

**3. Class 2's "last non-`unchanged` walk" built as "the last walk left it".**
Confirmed. The spec contradicts itself here. Class 2's rule prints a line for
*left, unchanged*, and S9 forbids that line. `walked_move`'s #791 rule and
`owed_moves` side with S9. `test_every_walk_sequence_prints_what_the_file_holds`
asserts the printed line and the BROKEN part as one decision over all 36
sequences, and `walked_outcome` hands through only the walk's own line, so the
two cannot drift apart (read).

**4. Reason (i) judged on the newest reading only.** Confirmed. The view
`why_still_drifted` reads is `released_drift`'s, taken against the open plan,
so *newest* includes the dates the run itself added. I enumerated the cases:

- An older reading outside the narrowing, under a newest one the run wrote and
  left, is (ii). A run without `--ledger` would re-stamp the older one to no
  effect.
- A newest reading outside the narrowing is (i), which is true.
- A tie of one reading in the run and one outside is a union, so it is not
  owed.
- A newest reading the run dated and re-stamped holds, so it is not owed.

I found no shape where newest-only names a remedy that cannot clear the
family.

**Class 1 by construction.** The axes are narrowed or unnarrowed, the walk on
which a coordinate is left or cleared, outranked or newest, and frozen or
unfrozen. The coordinate kind is a fifth axis.

- **Outranked.** Left alone in all four combinations of narrowing and freeze
  (S1, S2 both narrowings, S3). The released member under the freeze is not
  walked.
- **Newest and holding.** The hash is unchanged, so nothing moves.
- **Newest, tied with a holder.** Left alone (S3).
- **Walk on which it is left or cleared.** A held coordinate produces no
  outcome on any walk except where it rides. A rider on walk k is spliced on
  walk k, joins MOVES on walk k, and reads unchanged on later walks (read).
  The shape that fails is a held coordinate with no place on a dated row
  (🟡 1).
- **Coordinate kind.** A citation is outside the judgment (planted). A rename
  is outside: held implies a reading resolves. A non-citation ledger
  coordinate is 🟡 2.
- **Frozen or unfrozen.** p1 ran both.

**The 31 released-row verdicts.** I read every claim against the target. The
drifted units are:

| Unit | Rows citing it |
|---|---|
| `reverify` | 19 |
| `main` | 8 |
| the home's §*A released row is read again* | 7 |
| the skill's re-verify section | 2 |
| `RE_READ_SENTENCES` | 1 |
| the usage snippet | 1 |
| two test units | 2 |

I read every claim that names what this branch changed: dating, naming, `left`
lines, the narrowed `LEFT` line, MOVES and the pact record, and the dated-note
sentence.

28 of the 30 `Re-read ·` verdicts hold as the phase-3 table says. Notes on
three of them:

- 0.18.1:417 says *re-stamps in place as before*. That compares the in-place
  arm with the freeze, as phase 3 says.
- 0.18.1:418's exit-0 equivalence is not broken by p1 or p2, because both exit
  1.
- 0.18.2:87 (E4) holds vacuously for a ledger coordinate 🟡 2 leaves
  unmoved.

The other two, 0.4.0:59 and 0.18.2:129, hold only after 🟡 1 (⬜ 4).

**The `Corrected ·` over `seal/releases/0.18.2.md:91`.** Confirmed:

- The released claim ended *although without the freeze the ledger home says a
  released row is re-stamped in place with a dated note*, which D4 made false.
- The new claim's three code facts are true at the target. `reverify_into`
  writes `Re-read <checked> by work item` into Notes (`evidence_check.py:4195`).
  `reverify` splices only `dated_cell`. The home's sentence now reads *adding
  the date of the reading to its `Checked` cell*.
- 0.18.2:91 is itself a `Corrected ·` row. A correction of it supersedes its
  family, and the 0.18.0 row it corrected stays superseded. `corrected_by`
  drops a superseded correcting row, so no double-correction is reported.

`bin/evidence-check --strict .` exits 0 at the target, which is consistent
with this (executed, see *Executed probes*).

**`changelog.md`.** It says what ships at the target. Bullet 1 states the rider
and the narrowed exit-0 change, bullet 2 the fold, bullet 3 the per-coordinate
remedy, and bullet 4 #781. After 🟡 1's fix, bullet 1's *is named on no line*
stays true, because the rider sentence follows it.

**D4 (#781).** Confirmed. The owner's decision is recorded in `spec.md`
§*Grounding* and `questions.md`, and the writer is unchanged. The sentence and
`RE_READ_SENTENCES` changed together, and the needle
`test_the_ledger_rules_have_one_home` reads is intact.

## Regression tests to plant

Destination: `tests/test_a_released_row_is_read_again_in_a_fragment.py`,
after the case for the two-place held coordinate that phase 1 planted. I saw
both cases red at the target and green with the two fixes below applied to the
clone (p5). The fix pass shows them red again before committing them (§15).

```python
def test_a_held_coordinate_with_two_places_on_a_row_the_run_dates_is_left_and_named(
    repo,
):
    """#785, the rider rule meeting the resolution guard. B holds `handler`
    through one of its two places; A carries it at an older hash and also
    `other`, which drifted with no reading holding it. The run dates A for
    `other`, which makes A the newest reading of `handler`, and A's hash is
    in neither place: the run names it `left` and hands MOVES a BROKEN part,
    as for any coordinate no one place holds. Red at 0667af2e."""
    o0 = unit_hash(repo, "src/service.py", "other")
    h0 = at_version(repo, 1)
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h0}` | read | 2026-01-01 | |"
        ],
    )
    h1 = at_version(repo, 2)
    a = fragment(
        repo,
        [re_read_of(r, h1, "2026-02-01", extra=f", `src/service.py#other@{o0}`")],
        name=A_ITEM,
    )
    places, _ = ec.resolve_unit("src/service.py", "handler", TWICE)
    x, y = places[0]
    held = ec.content_hash(ec.gfm_lines(TWICE)[x - 1 : y])
    b = fragment(repo, [re_read_of(r, held, "2026-03-01")], name=B_ITEM)
    (repo / "src" / "service.py").write_text(
        TWICE.replace("x * 2", "x * 3"), encoding="utf-8"
    )
    frozen(repo, "0")
    moves = []
    ec.reverify([str(a), str(b)], str(repo), {}, None, "2026-04-01", moves)
    assert ("src/service.py#handler", h1, None) in [m[2:] for m in moves], moves
    fix = run(["--reverify", "--checked", "2026-04-01", "."], repo)
    said = [
        line
        for line in fix.stdout.splitlines()
        if line.startswith("  src/service.py#handler  ") and line.endswith("left")
    ]
    assert len(said) == 1, fix.stdout


def test_a_held_ledger_coordinate_the_run_moves_is_re_stamped(repo):
    """#785's judgment is made before the walk, on the premise that a walk
    moves no code. A coordinate naming a ledger line is the exception: Q and
    B both name R1's line, B newer and holding it, and the run re-stamps R1
    in place, which moves that line. Q and B are re-stamped with it, as
    before #785, and `--strict` reads the tree clean. Red at 0667af2e."""
    h = unit_hash(repo, "src/service.py", "handler")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
    released(repo, [r1])
    lc = citation(r1, "R1 · handler adds one")
    second = "### 1000000002-the-second-item"
    q = f"| Q · beside R1 | `{lc}` | read | 2026-01-01 | |"
    released(repo, [q], version="0.2.0", section=second)
    cq = citation(q, "Q · beside R1", version="0.2.0", section=second)
    fragment(
        repo,
        [
            f"| Re-read · Q · beside R1 | `{cq}`, `{lc}` | read | 2026-02-01 | "
            "Re-read 2026-02-01 |"
        ],
        name=B_ITEM,
    )
    assert run(["--strict", "."], repo).returncode == 0
    edit_handler(repo)
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    assert fix.returncode == 0, fix.stdout
    assert run(["--strict", "."], repo).returncode == 0
```

## Facts to feed into the evidence ledger

- Fragment row A1. Replace *a held one whose reading no longer resolves to one
  place is left with no line* with: *left with no line where the run does not
  date its row, and named `left` and handed MOVES a BROKEN part where it
  does*. Add the first case above to A1's grounds.
- A new row, or an extension of A1: a coordinate naming a line of a ledger the
  run writes is never judged held, because the walk can move that line. Its
  grounds are `reverify` and the second case above.
- The phase-3 grounds for 0.4.0:59 (⬜ 4) need the dated-row qualifier.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 and 🟡 2

The two fixes touch neighbouring lines of `reverify`. They are shown
separately, in the order to apply them.

🟡 2 — `skills/evidence-check/scripts/evidence_check.py`, before
`once, again, bound = cited_first(...)`:

```python
    # The files this run may rewrite. A coordinate naming a line of one is
    # graded against a line the walk can move, so the judgment made before
    # the first walk does not hold for it (#785).
    writes = {planned_key(p) for p in ledgers}
```

and in the anchor loop, replacing
`holds = spot[1] in held_at.get((ident, spot[0]), ())`:

```python
                at, rel_ = place(root, maps, default_repo, m.group("path"))
                holds = spot[1] in held_at.get((ident, spot[0]), ()) and (
                    at is None or planned_key(os.path.join(at, rel_)) not in writes
                )
```

and in `left_alone`'s docstring, the last paragraph:

```python
    Judged once, never live: a walk writes ledger lines and no code, so no
    code coordinate's grading moves during the run, and only a date the run
    adds could reorder a family's readings mid-walk. A coordinate naming a
    line of a ledger the run writes is the exception, and `reverify` never
    judges it held."""
```

🟡 1 — the same function. `deferred, held_edits = set(), []` becomes:

```python
        deferred, held_edits, unheld = set(), [], []
```

the guard after `holds` becomes:

```python
                if holds and current_hash(m, root, maps, default_repo) is None:
                    # A newest reading resolves it, so this reading of it is
                    # history, unless the run dates its row (below).
                    unheld.append((m.start(), key, m))
                    continue
```

and between the `for number, row_edits in sorted(by_row.items()):` loop and
`for offset, _coord, old, new in pending:`:

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

`reverify`'s docstring, the #785 paragraph, after *a held one is re-stamped
as well: the date makes that row the newest reading of each coordinate on
it.*:

```python
    One with no one place to re-stamp on such a row is left and named, as
    any such coordinate is.
```

### 🟡 3

`docs/the-evidence-ledger.md`, the *Without the row* paragraph:

```markdown
coordinate itself, on a `left` line or by leaving its row whole for want of
a date cell, the line says so and points at the line naming why, and a run
over every ledger names such a family too. Where neither is found it names
no remedy.
```

and its pin in
`tests/test_a_released_row_is_read_again_in_a_fragment.py`,
`test_the_documents_say_each_outcome_is_printed_once`:

```python
            "Where the run left the coordinate itself, on a `left` line or by "
            "leaving its row whole for want of a date cell, the line says so and "
            "points at the line naming why, and a run over every ledger names "
            "such a family too.",
```

Re-wrap the paragraph to the 88-column rule and re-run the paste module. A
15-word run shared with another file is the check most likely to refuse new
wording.

Needs a fix: yes — 🟡 1 (a held coordinate with no place on a row the run dates is left silently, with no BROKEN part), 🟡 2 (a held coordinate naming a ledger line the run rewrites is left stale, so `--strict` goes red where the base was clean), 🟡 3 (the ledger home's definition of the (ii) case)
Loses a record or crashes: no — nothing written is lost and nothing crashes; 🟡 1 leaves out one pact-change BROKEN row the base wrote, in a narrow shape, which is a missing write rather than a lost record

The broad gate is not yet due: this round leaves three 🟡 open.

## Proof block

Ran by specseal:warden on claude-opus-5-5, in a `git clone --no-local` at
0667af2e and a second at a3aa139a, both under this round's scratchpad
directory and removed before handover. The probe files carried the
agent contract's probe prefix, ran once, and were deleted.

Files opened:

- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/spec.md`
- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/overview.md`
- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/questions.md`
- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/changelog.md`
- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/survivors.md`
- `seal/specs/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once/phases/phase-1.md`,
  `phases/phase-2.md` and `phases/phase-3.md`
- `seal/ledger/1791163980-an-in-place-reverify-leaves-history-alone-and-reports-each-row-once.md`
- `skills/evidence-check/scripts/evidence_check.py`: `family_view`,
  `reading_date`, `walked_move`, `owed_moves`, `walked_outcome`, `left_alone`,
  `cited_first`, `reverify`, `current_hash`, `citations_left`,
  `released_drift`, `why_still_drifted`, `still_drifted_line`, the in-place
  and frozen arms of `main`, `coordinate_of` and `planned_key`
- the diff a3aa139a..0667af2e of `skills/evidence-check/SKILL.md`,
  `docs/the-evidence-ledger.md`,
  `tests/test_a_merge_cannot_silently_drop_a_correction.py` and
  `tests/test_a_released_row_is_read_again_in_a_fragment.py`
- in `seal/releases/`, the claim cells of the 31 rows named in
  `phases/phase-3.md`
- `bin/test`
