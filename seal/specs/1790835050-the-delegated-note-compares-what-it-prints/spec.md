# Feature Specification: the delegated note compares what it prints

<!-- seal/specs/1790835050-the-delegated-note-compares-what-it-prints/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Ticket #701, release 0.17.0. `session-cost --spawns` prints a note when no
spawn's `delegated` interval reaches a minute — *`delegated` never reaches a
minute here — Ns at most* — and decides whether to print it on the raw
value, `delegated_max < 60` (`skills/verify/scripts/session_cost.py:2219`),
while the column beside it prints the same value through `minutes`, to one
decimal place of minutes (`:1970-1971`, `:2251`). A spawn paired in 59.6 s
therefore prints `1.0m` in the column and, beneath it, a sentence saying the
column never reaches a minute. The band where the two disagree is about
57 s to 60 s.

It is the third instance of one cause. #640's round 1 🟡 1 found it in
`report_grades` and round 2 🟡 8 in `report`'s batching advisory, and both
were fixed by comparing the ratio rounded to the two places it prints
(`session_cost.py:2102-2109`, `:2503-2507`, `:2519`). Round 3 found this one
on a duration, outside every unit that run created, and deferred it with a
paste-ready fix and case
(`seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/rounds/round-3-report.md`
§*Paste-ready fixes*, 🟡 10). This work applies that fix, pins it, and
records the class sweep the ticket's second box asks for.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §12 *A defect belongs to a class — enumerate the class* | The ticket's second box is this rule applied: every comparison in `session_cost.py` of a value against a threshold it prints rounded is checked in the same change. The sweep is §*The class, swept* below; the build re-reads it and the changelog fragment states its result, naming the one same-shape site left alone and why |
| `skills/agent-contract/SKILL.md` §14 *A fix that changes what a person sees documents it and pins it* and §15 *A new case is not planted until it has been seen red* | The note is a line a person reads and acts on. The case is planted in `tests/test_session_cost.py`, its 59.6 s half seen red at the base, and the phase record says how (plan phase 1) |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file*, the paragraph *Appended is the word, and a removal is not one — nor is an edit* | The fix edits `report_spawns`, which seven ledger rows anchor at `session_cost.py#report_spawns@15595f59` (`seal/releases/0.9.5.md` lines 11, 13, 14, 16, 45, 46; `seal/releases/0.11.3.md` line 50). An edit drifts a row, which is re-read against the edit and re-stamped there with a dated note. None of the seven claims becomes false (§*Data & interfaces*); row 13's note, which says *the `delegated_max < 60` block and its sentence are untouched*, is the one whose text the edit makes stale and it gets a `Re-read 2026-10-01` note saying what moved. New rows go to `seal/ledger/1790835050-the-delegated-note-compares-what-it-prints.md`, the changelog entry to this directory's `changelog.md` |
| #640's S10 ruling — `seal/specs/1790815612-…/spec.md` S10 *nothing else moves* and `plan.md` §*Technical context*, *the three comparability lines gain nothing (#377's and #642's lines exist because a NUMBER moved; here none does)* | The same ruling holds here. No number on any page moves and `--json` carries the raw `delegated_s` untouched, so no comparability line is added to the page; the changelog fragment names the band in which the note's presence moves, as #640's did for [1.195, 1.2) |
| `docs/measuring-a-run.md` §*An orchestrator measured by its whole session is measured by its children* | *The delegated interval is excluded from the orchestrator's model time and reported as its own number.* What the number IS does not move: the fix touches the sentence printed about the column, never the column or `measure_cycles` |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Not a gate: `session_cost.py` refuses nothing and exits 0 before and after. Stated so a reviewer does not look for the four items |

## Scope

**In.**

1. **The decision follows the column.** `report_spawns` prints the note only
   when the value the `delegated` column prints is under a minute:
   `round(delegated_max / 60, 1) < 1.0`, beside a comment naming the cause
   and #701, in the shape of the two comments #640 left at `:2102-2108` and
   `:2503-2507`. The note's own wording and its `.0f` seconds figure are
   unchanged.
2. **A case, seen red first.** In `tests/test_session_cost.py`, beside
   `test_a_delegated_column_of_seconds_says_which_of_two_things_it_is`
   (`:2608`): a spawn paired in 59.6 s prints `1.0m` in the column and no
   *never reaches a minute* note; a spawn paired in 57.0 s prints `0.9m` and
   the note with *57s at most*. The first half is red at the base; the second
   is the band's floor and is shown red with the comparison mutated (plan
   phase 1 says how).
3. **The ledger kept true.** The seven drifted rows are re-read against the
   edit and re-stamped by `evidence-check --reverify --checked 2026-10-01`,
   row 13 of `seal/releases/0.9.5.md` with a `Re-read 2026-10-01` note on
   what moved; the fragment gains the new claim; `evidence-check` exits 0 at
   the tip.
4. **The class, recorded.** The changelog fragment states that every other
   comparison in `session_cost.py` of a value against a threshold it prints
   rounded was checked, that two already compare the printed figure (#640),
   and that one same-shape site (`:2115`) is left because no reading of it
   contradicts the page. The build re-reads the table below rather than
   trusting it (§5), and its phase record says what it found.

**Out, and why.**

- **The note's `.0f` seconds figure.** Once the decision follows the column,
  the largest value that still prints the note is 57.0 s itself (executed by
  the framer, one arithmetic line, nothing left behind: `round(57.0 / 60, 1)`
  and `f"{57.0 / 60:.1f}"` are both `0.9`, because 57/60 in binary sits just
  under 0.95; `57.01` and `57.02` both give `1.0`), so the figure never
  prints `58s` or above beside a `0.9m` cell and cannot contradict it. The existing case pins `3s at most`; the seconds keep the
  precision the note exists for at the values it exists for.
- **`session_cost.py:2115`, `tools_per_turn <= 1.0` choosing the batching
  sentence.** Same shape — a raw comparison beside a `.2f` print — but at a
  ratio in (1.0, 1.005) the page prints `1.00` and *most turns send a single
  call*, which `1.00` does not contradict, and the raw comparison keeps that
  sentence true of the data where *one at a time* would be false by a turn.
  Checked, left, and named in the changelog fragment. Alternatives table, E.
- **The existence checks printing `minutes`: `same > 0` and `exact > 0`
  (`:2096-2100`), `outside >= 0` (`:2316`).** Zero is not a threshold a
  rounded print can contradict: `repeats 0.0m a check re-run` says a check
  was re-run, which is true at 2 s, and rounding the check would drop a real
  repeat from the page. The comment at `:2279-2283` already judged this
  shape for the refusal branch and chose to print two sums rather than a
  rounded difference.
- **Comparisons whose compared value is not printed rounded.** `idle >
  span * 0.1` (`:2057`, prints `minutes(idle)` and a share, states no
  threshold); `growth[2] > growth[0] * 1.5` (`:2136`, integers printed with
  `:,`); the 900 s gap ceiling (`:1123`, `:1586`, the gap itself unprinted);
  `distance <= JOIN_TOLERANCE_S` (`:1624`, the distance unprinted, the
  tolerance printed at `:2628`); `widest_idle_gap` at `:2672-2678` (a gap
  prints only when selected at the 900 s floor, so `15.0m` is its minimum
  print); `span_s > 0`, `run_span > 0`, `slices > 1` (sign and integer tests).
- **The three comparisons already made on the printed figure**:
  `round(data["tools_per_turn"], 2) < 1.2` (`:2109`), `>= 1.2` (`:2141`) and
  `report_grades`' `< row["bar"]` (`:2519`). #640's, closed.
- **`--json`.** `report_spawns` runs only when `args.spawns and not
  args.json` (`:3116`); `--json` prints `data` with the raw `delegated_s` and
  no note key (`:3179-3180`). Nothing there moves.
- **The `--segments` page, `measure_cycles`, the `DELEGATING` exclusion,
  `minutes` itself.** None is touched; the fix is one comparison and one
  comment inside `report_spawns`.
- **Documents.** No document states the note's threshold: `skills/verify/
  SKILL.md:683` and `:755-760` and `docs/measuring-a-run.md:31-36` describe
  the column and the ACCEPTED harness without naming 60 s, and neither README
  mentions the note. No document edit; the changelog fragment is the record.

## User scenarios & acceptance *(mandatory)*

One row per scenario — these become the review's stage-1 checklist and the
regression tests' skeleton.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a column at `1.0m` has no note under it | Given a transcript with one spawn paired in 59.6 s and one later call, when `--spawns` prints, then the `delegated` cell reads `1.0m`, the page carries no *never reaches a minute* and no *60s at most* | a case in `tests/test_session_cost.py`, red at the base |
| S2 a column at `0.9m` keeps the note | Given a spawn paired in 57.0 s, then the cell reads `0.9m` and the note prints with *57s at most* | the same case, second half; red with the fix's comparison mutated to `< 0.9` |
| S3 the quick harness still says which of two things it is | Given the existing 3 s fixture and the `orchestrator` fixture, then `test_a_delegated_column_of_seconds_says_which_of_two_things_it_is` and `test_the_delegated_wait_is_in_no_column_of_any_row` pass unchanged | the existing cases, run at the tip |
| S4 `--json` is the number it was | Given the S1 transcript through `--json`, then the spawn row's `delegated_s` is 59.6 and no key describes the note | the existing `--json` cases at the tip; one assertion on the S1 fixture if the module has no `--spawns --json` case over a sub-minute spawn |
| S5 the ledger stays true | Given the tip, then `evidence-check` exits 0, the seven rows anchored at `report_spawns` carry a 2026-10-01 re-read, row 13 of `seal/releases/0.9.5.md` says the comparison now runs on the printed minute, and the fragment holds the new row | `python3 skills/evidence-check/scripts/evidence_check.py .`, exit code read directly (contract §1) |
| S6 the class is on the record | Given this directory's `changelog.md`, then it names the band in which the note's presence moves, says every other threshold comparison in the module was checked, and names `:2115` as checked and left with the reason | read; the fragment follows `seal/specs/1790815612-…/changelog.md`'s shape |
| S7 the case was seen red | Given `phases/phase-1.md`, then it says how each half of the case was shown red before it was planted | read |

## The class, swept

Every comparison of a value against a threshold in `session_cost.py` at
`e83db346`, found by reading the module's `<`, `>`, `<=`, `>=` sites, with
whether the compared value is printed rounded beside the decision and the
verdict. The build re-reads this table; it is the framer's reading and not
evidence (contract §5).

| Site | Compares | Prints the compared value as | Contradiction a reader can see | Verdict |
|---|---|---|---|---|
| `:2219` `delegated_max < 60` | a duration against 60 s | `minutes` (`.1f` of minutes) in the column, `.0f` seconds in the note | `1.0m` beside *never reaches a minute* for 57–60 s | **fix** (in, item 1) |
| `:2109` `round(tools_per_turn, 2) < 1.2` | a ratio | `.2f` | none — compares the printed figure since #640 | closed by #640 |
| `:2141` `round(tools_per_turn, 2) >= 1.2` | a ratio | — (prints `nothing obvious`) | none | closed by #640 |
| `:2519` `round(tools_per_turn, 2) < row["bar"]` | a ratio | `.2f` | none | closed by #640 |
| `:2115` `tools_per_turn <= 1.0` | a ratio, choosing a sentence | `.2f` | none — `1.00` is consistent with either sentence | checked, left (out) |
| `:2096` `same > 0`, `:2100` `exact > 0` | a duration against zero | `minutes` | none — existence, not a threshold | left |
| `:2316` `outside >= 0` | a duration against zero | `minutes` | none — `0.0m … is BETWEEN the rows` is true at 2 s | left |
| `:2057` `idle > span * 0.1` | a share against a tenth | `minutes` and `share` `.0f%`, no threshold stated | none | left |
| `:2136` `growth[2] > growth[0] * 1.5` | integers | `:,` | none | left |
| `:1123`, `:1586` gap against 900 s | a gap | not printed | none | left |
| `:1624` `distance <= JOIN_TOLERANCE_S` | a distance against 1.0 s | distance not printed; tolerance printed `.1f` at `:2628` | none | left |
| `:2672-2678` `idle_gap_s` truthy, `widest` | gaps at or above the 900 s floor | `minutes(widest)` | none — a selected gap prints at least `15.0m` | left |
| `:2020`, `:2025`, `:2057`, `:2307` sign tests on spans; `:2652`, `:2391` `slices > 1`; `:2015` `whole > 0` | sign or integer | — | none | left |

## Data & interfaces

- **The one line that moves**: `skills/verify/scripts/session_cost.py`
  `report_spawns`, `:2219`, from `if delegated_max < 60:` to
  `if round(delegated_max / 60, 1) < 1.0:`, with its comment. `round(x, 1)`
  and `f"{x:.1f}"` are both correctly rounded from the binary value in
  CPython, so the comparison agrees with what `minutes` prints; S2 at 57.0 s
  pins the edge where a disagreement would show (`questions.md` Q1).
- **The printed page**: the note's presence moves for `delegated_max` in
  (57.0, 60) — executed at 56.9, 57.0, 57.02, 59.5, 59.6, 59.99 and 60.0,
  where `round(x / 60, 1)` and `f"{x / 60:.1f}"` agreed at every value;
  every other reading prints as it did. No number moves.
- **`--json`**: unchanged. The seven ledger claims anchored at
  `report_spawns`: none states the 60 s condition as its claim — they are
  about the empty-table arm (0.9.5 line 11), the ACCEPTED-harness disclosure
  (13), the between-the-rows figure and its refusal (14, 16, 45, 46), and
  *nothing the mode adds changes what any existing reading prints* (0.11.3
  line 50, whose claim is about the `--segments` mode's addition and holds).
  All seven drift on hash alone and are re-read, not corrected; row 13's
  free-text note is the one whose words the edit makes stale.
- **New ledger rows** in `seal/ledger/1790835050-the-delegated-note-compares-what-it-prints.md`:
  the note's decision is made on the value the column prints, anchored at
  `session_cost.py#report_spawns@<new hash>` and the case's
  `tests/test_session_cost.py#<case>@<hash>`, with how it was seen red.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided. No row there needs a person.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     `<who>` takes the two values the `Planning` row of `routing.md` takes,
     `framer` or `the session`, and a mark that disagrees with that row is
     refused at the pull request rather than guessed at. -->

Framed 2026-10-01 by framer, before the build.
