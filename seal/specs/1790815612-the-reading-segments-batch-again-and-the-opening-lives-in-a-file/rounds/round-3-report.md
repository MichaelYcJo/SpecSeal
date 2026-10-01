# Round 3 report — warden (verifying, the run's last round)

| Field | Value |
|---|---|
| Work item | 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file (#640, draft PR #696) |
| Target SHA | c374404b6e2cd87f2aa55a97c16469469f40e6c8 |
| Diff | round 2's fix range `090edf3b..6bdf8642` (one commit), plus `c374404b`, which only closes round 2's record |
| Clone | a `git clone --no-local` under the session scratchpad, `<scratchpad>/1790815612/round-3/clone`, removed at the end of the round |
| Ran by | specseal:warden on Opus 5.5 |

This is the verifying round, and the run is capped: round 2 used the one
reopening. Its job is whether round 2's two closed verdicts are actually
closed, with their class. Round 2's record and report were read for
coordinates. Every verdict below is re-derived at the target. The fix
commit's message, the code comment, the ledger notes and the changelog
fragment were read as claims and checked against the code.

One new unit was named in round 2's record,
`test_a_plain_reading_printed_at_the_advisory_is_not_flagged` (depth 1). It
was judged as code.

## Round 2's findings, one by one

### Finding 8 — closed at both comparisons, and the ratio class is closed

`report` now compares `round(data["tools_per_turn"], 2)` with 1.2 in both
places: the batching advisory (`skills/verify/scripts/session_cost.py:2109`)
and the `nothing obvious` line (`:2141`). The advisory prints the ratio with
`.2f`. Python's `round(x, 2)` and `.2f` round the same binary value the same
way, so the compared figure is the printed one. Executed: 241/201 rounds to
1.2 and prints `1.20`.

The new unit pins each gate on its own. Executed: with only the advisory's
`round` removed, the case is red on `batching` appearing. With only the
`nothing obvious` gate's `round` removed, it is red on `nothing obvious`
missing. At the target it is green.

The class is closed. I enumerated every comparison in `session_cost.py` that
reads `tools_per_turn`: the two gates above, the grade at `:2519` (round 1's
finding 1, rounded), and the shape ternary at `:2115`, `<= 1.0`, unrounded.
The ternary is not an instance. It picks the sentence and prints no
threshold. `call_turns` counts only turns that sent a call, so the ratio is
1.0 exactly when every turn sent one call. A ratio in (1.0, 1.005) prints
`1.00` with *most turns send a single call*, which is true. Rounding there
would print *independent calls are going out one at a time* over a turn that
batched, which is false. So unrounded is right at that comparison.

No document carries the old unrounded comparison. The only shipping sentence
that states the advisory is `docs/review-handoff-protocol.md:644`, *below 1.2
and stays there*, and it is still true.

### The cross-pin still fails when the two values disagree

`test_the_advisory_and_the_tying_paragraph_name_one_value` now reads the
rounded comparison. Executed: with the script's threshold moved to `1.3` and
the protocol left at 1.2, it is red and names 1.3. With the comparison put
back to its unrounded form, it is red on *moved off its pattern*. So it
cannot pass silently if the comparison's shape drifts.

One limit, read only. The pattern reads the advisory's `<` comparison. The
`nothing obvious` gate's `>= 1.2` is read by no pattern, and that was also
true before the fix. The new unit holds the two gates together at 1.199,
which is the probe above. This is not a finding.

### Finding 9 — closed at its three coordinates, and the class recurs one file over

The docstring at `session_cost.py:2500` is rewrapped (widest line 77
columns). `agents/framer.md:180` and `:198` are rewrapped with nothing ragged
left in either hunk. Executed: `tests/test_docs_line_wrap.py` is green, and
`ruff check` and `ruff format --check` pass on the three changed Python files.

But the same fix commit wrote a new ragged line. In the changelog fragment's
corrected sentence, line 32 runs to 109 columns: *only for a ratio in [1.195,
1.2), and every other reading stays comparable. The protocol's bars table
gains*. That is finding 9's class. Because the file sits under `seal/specs/`,
it is reported as a correction (⬜ 11) and stays out of `Needs a fix`.

### The changelog fragment's corrected sentence is true

The old sentence said *the plain reading … unchanged*, and that clause is
gone. The new one says both the grade and the advisory compare the rounded
ratio, that a reading printed at 1.20 is no longer flagged, and that the
verdict moves only for a ratio just under 1.2. Each part matches the code
read above. *No number on the page moves* still holds, because rounding a
comparison changes no printed figure.

### The four re-stamped rows' notes are true

Each row now anchors `#report@76e36439`, and unscoped `evidence-check .`
reads it ok. Each note was read against the `report` diff, whose only
behaviour change is the two rounded gates.

- `seal/releases/0.8.3.md:126` (R2): `share`, the one-line-per-shape
  sentences and the duration guards on `same` and `exact` are untouched. The
  two edited gates are existing gates whose expressions changed, so *the nine
  gates are still nine* holds.
- `seal/releases/0.9.4.md:32` (S2): the `other`-leads note is untouched.
- `seal/releases/0.9.4.md:35` (S5): the context line and its
  `growth[0] > 0` conjunct are untouched.
- `seal/releases/0.9.5.md:47`: the negative-span sentence is untouched.

The work item's own fragment gains row R1 for the fix. Its anchors resolve
and its claim matches the code.

## Opened in this round

### 🟡 10 — the `delegated` note says a minute is never reached beside a `1.0m` cell

`skills/verify/scripts/session_cost.py:2219` compares `delegated_max < 60`
unrounded. The note prints the value with `.0f` seconds, and the column
prints it through `minutes`, which rounds to one place.

Executed with a deleted probe: one spawn whose call pairs in 59.6 s printed
the row `cycle 1  specseal:smith … 1.0m` in the `delegated` column and,
under it, *`delegated` never reaches a minute here — 60s at most*.
From about 57.0 s up to 60 s, the column reads `1.0m` while the note says a
minute is never reached. From 59.5 s, the note's own figure reads `60s`.

The cause is finding 8's: an unrounded value compared with a threshold while
the line prints it rounded. It is a duration and not a ratio, so it falls
outside the class as round 2 named it, and §12 still owes it the same fix.
It predates the work item. It came in with `93d27574` (#294) and lies
outside every unit this run created. Since the run is capped, it takes the
filing ladder.

The paste-ready fix compares at the column's own precision. The note then
prints only when the column also reads under a minute.

## Regression tests to plant

- `tests/test_session_cost.py` — for 🟡 10, beside
  `test_a_delegated_column_of_seconds_says_which_of_two_things_it_is`: one
  spawn paired in 59.6 s prints no *never reaches a minute* line. It is red
  at the target, which the probe above showed.

## Facts for the evidence ledger

None new from this round. Row R1 in the work item's fragment already
carries finding 8's fix. 🟡 10's claim belongs in whatever change fixes it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 8 is closed — both plain-reading gates compare the ratio rounded to the two places it prints | `skills/verify/scripts/session_cost.py:2109`, `:2141` | confirmed | executed: the new unit red with each `round` removed in turn, green at the target; the ratio class enumerated: the grade at `:2519` rounded, the shape ternary at `:2115` correctly unrounded |
| 🟢 | the new unit pins its defect at both gates | `tests/test_session_cost.py:315` | confirmed | executed: red on `batching` with the advisory unrounded, red on `nothing obvious` with that gate unrounded |
| 🟢 | the cross-pin still fails when the script and the protocol disagree | `tests/test_the_handoff_before_round_one.py:611` | confirmed | executed: threshold moved to 1.3, red naming 1.3; comparison unrounded, red on the pattern; the `>= 1.2` gate is read by no pattern, as before the fix |
| 🟢 | round 2's finding 9 is closed at its three coordinates | `skills/verify/scripts/session_cost.py:2500`, `agents/framer.md:180`, `:198` | confirmed | read: widths measured; executed: `tests/test_docs_line_wrap.py` green, ruff check and format check exit 0 |
| 🟢 | the four re-stamped rows' notes and the changelog's corrected sentence are true | `seal/releases/0.8.3.md:126`, `seal/releases/0.9.4.md:32`, `:35`, `seal/releases/0.9.5.md:47` | confirmed | read against the `report` diff; unscoped `evidence-check .` exit 0 |
| 🟡 10 | the `delegated` note compares the unrounded maximum with 60 and prints it rounded, so 59.6 s reads `1.0m` in the column and *never reaches a minute here — 60s at most* under it | `skills/verify/scripts/session_cost.py:2219` | open | executed: a deleted probe, one spawn paired in 59.6 s; finding 8's cause on a duration, predates the work item (`93d27574`, #294) and lies outside every unit this run created, so it takes the filing ladder |
| ⬜ 11 | the changelog fragment's corrected sentence leaves one line at 109 columns — finding 9's class, written by the commit that closed it | `seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/changelog.md:32` | open | read: widths measured; a correction to the run's paperwork, outside `Needs a fix` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_session_cost.py`, `tests/test_the_handoff_before_round_one.py`, `tests/test_docs_line_wrap.py` at the target | exit 0, 206 passed |
| `bin/evidence-check .`, unscoped, at the target | exit 0; 3182 ok, 0 drifted, 0 broken |
| `ruff check` and `ruff format --check` over the three changed Python files | exit 0 and exit 0 |
| the advisory's `round` removed, new unit and cross-pin run | exit 1 and exit 1: `batching` in the output; *moved off its pattern*; reverted |
| the `nothing obvious` gate's `round` removed, new unit run | exit 1: `nothing obvious` missing; reverted |
| the advisory's threshold moved to `1.3`, cross-pin run | exit 1: names 1.3 against the protocol's sentence; reverted |
| a probe case: one spawn paired in 59.6 s, `--spawns` | exit 1: `delegated` column `1.0m`, note *never reaches a minute here — 60s at most*; probe deleted |
| broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 10 — the `delegated` note's unrounded comparison | a candidate for the filing ladder; no home yet | the repository owner, who opens the issue or names the existing one |

## Paste-ready fixes

### 🟡 10

```python
    # Compared at what the `delegated` column prints, `minutes` to one place,
    # so the note never says a minute is not reached beside a `1.0m` cell —
    # finding 8's cause, on a duration (#640, round 3's 🟡 10).
    if round(delegated_max / 60, 1) < 1.0:
```

```python
def test_a_delegated_note_does_not_contradict_a_column_at_one_minute(tmp_path):
    """59.6 s prints `1.0m` in the `delegated` column; a note under it saying
    the column never reaches a minute contradicts the row it explains."""
    rows = spawn("A", 0, 59.6, "specseal:smith") + call("a", 80, 85, "git status")
    path = tmp_path / "band.jsonl"
    path.write_text("\n".join(rows) + "\n")
    out = run(["--spawns", str(path)]).stdout
    assert "never reaches a minute" not in out, out
```

### ⬜ 11

```
  `kind` and `bar`. Both the grade and the plain reading's batching advisory
  compare the ratio rounded to the two places they print it to, so a reading
  printed at 1.20 is no longer flagged below 1.2; the advisory's verdict moves
  only for a ratio in [1.195, 1.2), and every other reading stays comparable.
  The protocol's bars table gains the `framing` row. The first reading the
  grade took, over the run that built this change, read this frame's own
  segment at 4.17 tools per turn, 50 calls over 12 turns with a largest batch
  of 11, on a prompt without the old prohibition; one reading, and nothing
  beyond it is claimed from it.
```

Needs a fix: yes — 🟡 10 (the `delegated` note's unrounded comparison), which predates the work item and lies outside every unit the run created, so it takes the filing ladder rather than a fix on this branch
Loses a record or crashes: no

Nothing on this branch is left open for the branch to fix. Finding 8 and
finding 9 are closed, and ⬜ 11 is a paperwork correction. So the gate has
come due: what comes due is the sealer's spawn.

## Proof block

Files opened at the target in the clone:
`skills/verify/scripts/session_cost.py` (`:1155-1175`, `:1960-1972`,
`:2050-2145`, `:2205-2252`, `:2495-2560`), `tests/test_session_cost.py`
(`:60-90`, `:293-350`, `:2175-2190`, `:2590-2636`),
`tests/test_the_handoff_before_round_one.py` (`:596-620`),
`docs/review-handoff-protocol.md` (`:630-650`), `agents/framer.md`
(`:174-201`), `seal/releases/0.8.3.md:126`, `seal/releases/0.9.4.md:32`,
`:35`, `seal/releases/0.9.5.md:47`, the work item's changelog fragment
(`:15-40`) and ledger fragment (by diff), `rounds/round-2.md`, and
`rounds/round-2-report.md` (`:1-30`). Also opened:
`docs/review-chain-spec.md` (the ladder and the vocabulary of
`deferred <home>`), and the fix diff `090edf3b..6bdf8642` and `6bdf8642..c374404b`.
