# Round 2 report — warden (verifying)

| Field | Value |
|---|---|
| Work item | 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file (#640, draft PR #696) |
| Target SHA | 618dc68f5435bf8116f6295b0c08160461bcc5d9 |
| Diff | the fix range `0340a8bd..fe122afe` (one commit), plus `618dc68f`, which only closes round 1's record |
| Clone | a `git clone --no-local` under the session scratchpad, `<scratchpad>/1790815612/round-2/clone`, removed at the end of the round |
| Ran by | specseal:warden on Opus 5.5 |

This is the verifying round. Its target is the fix commit, and its job is
whether each of round 1's seven verdicts is actually closed, with its class.
Round 1's report and record were read for coordinates; every verdict below is
re-derived at the target. The fix commit's message and the ledger notes were
read as claims and checked against the code.

One new unit was named in round 1's record,
`test_a_row_printed_at_its_bar_meets_it` (depth 1). It was judged as code.

## Round 1's findings, one by one

### Finding 1 — the coordinate is closed, the class is not

`report_grades` now compares `round(tools_per_turn, 2)` against the bar
(`skills/verify/scripts/session_cost.py:2511`). The table and the grade line
both print with `.2f`, and Python's `round` and `.2f` round the same binary
value the same way, so the compared figure is the printed one.

Executed: with the `round` removed, the new unit goes red with both rows named
at `1.80` and `1.40`. At the target it is green.

The class is the same comparison anywhere a ratio is compared unrounded and
printed rounded beside the verdict. One more instance exists, in `report`'s
plain reading. That is 🟡 8 below.

### Finding 2 — closed

`agents/framer.md:189-192` now gives 0.12.1 and 0.12.2 together, at
1.48–1.80, with the two stalled readings named. I opened #456 for the four
figures. The 1.48 framer sits under the *0.12.1* section. The 1.64 framer is
in the #423 comment, and the stalled 1.56 and 1.80 are in the #424 comment,
both of the 0.12.2 run. The #468 comment, the third 0.12.2 work item, has no
framer. So the four readings are all the framers of those two releases.

The band sentence now says *that finished*, which keeps 0.12.2's stalled 1.80
out of 1.46–1.79. The changelog fragment and the test docstring carry the same
correction. The protocol's framing row gained *that finished* as well.

Executed: the opening case is red against the pre-fix `agents/framer.md`.

The frame records `spec.md:65-67`, `questions.md:27` and `plan.md:111` still
carry 1.48–1.64. Round 1 called correcting them optional, and they ship
nowhere.

### Finding 3 — closed

The bound now reads: the files the spawn prompt names are one call *whatever
their number*, and the six-read bound applies to each call of the wide reading
after that (`agents/framer.md:175-182`). That matches §10 at
`skills/agent-contract/SKILL.md:246`. The skeleton-first bullet above it is
not contradicted, because the opening call is the handoff's own files and the
wide reading comes after.

The changelog fragment and the ledger fragment's P1 row say the same. No other
shipping carrier of *about six* exists. A search over the tree found only the
frame records and this work item's fragments.

Executed: the case is red against the pre-fix definition, on *whatever their
number*.

### Finding 4 — closed

The framing row's Grounds now say the section *now replaces* the hold-back
with a bound on one call (`docs/review-handoff-protocol.md:633`). The case
refuses the old clause.

Executed: red against the pre-fix protocol.

### Finding 5 — closed

The counts sentence now says a row with no bar is ungraded, *and so is a
graded kind's segment that made no call* (`session_cost.py:2540`). That is
true of a no-call warden, and it no longer claims anything about a no-call
smith.

Executed: with the old sentence restored, the no-paired-call case is red.

### Finding 6 — closed (read)

The `segment_kind` docstring now says a program holding only `--json` cannot
tell exempt from unknown (`session_cost.py:2358-2361`). No document outside the
script carries the old claim. I searched `docs/`, `agents/`, both READMEs and
`skills/verify/SKILL.md`.

### Finding 7 — closed

The cross-pin now compares the whole of both tables
(`tests/test_the_handoff_before_round_one.py:584-595`). The script regex
matches all three `SEGMENT_BARS` entries, and the `>= 3` guard catches a
change to that dict's shape.

Executed, both directions:
- a `scribe` entry with a bar added to `SEGMENT_BARS` alone turns it red;
- a `scribing` row added to the protocol's table alone turns it red.

Both were reverted.

### The new unit — correct, and red on its defect

`test_a_row_printed_at_its_bar_meets_it` (`tests/test_session_cost.py:3271`)
builds 79 calls over 44 turns (1.7955) and 67 over 48 (1.3958). It asserts the
table prints `1.80` and `1.40`, and that no grade line appears. The two table
regexes hold the fixture at the boundary. If the fixture drifts off it, they
go red rather than letting the case pass for the wrong reason.

Executed: red against the unrounded comparison, green at the target.

`test_every_json_row_carries_its_kind_and_bar` stays green under that mutant,
because its fixtures do not sit at a boundary. It is a consistency check and
not this defect's pin, so that is not a gap.

### The four other-ledger re-stamps — true

I read each note against the fix diff to the protocol, whose only change in
the anchored section is the framing row's Grounds cell.

- `seal/ledger.md` row 97: *only the `framing` row's Grounds cell changed again*. True.
- `seal/releases/0.4.0.md` row 114: *that case now compares the whole of both tables*. The case is `test_the_scripts_bars_are_the_protocols`, named one sentence earlier, so the antecedent holds. True.
- `seal/releases/0.8.2.md` row 42: *the paragraphs this claim is about are untouched*. True.
- `seal/releases/0.15.7.md` row 41: *the `verifying` row is untouched*. True.

Executed: unscoped `evidence-check .` exits 0, with 3180 ok, 0 drifted and 0
broken.

## A finding this round opened

### 🟡 8 — the plain reading's batching advisory prints 1.20 under a threshold of 1.2

`report` compares the unrounded `tools_per_turn` with 1.2
(`skills/verify/scripts/session_cost.py:2102`). The batching line under it
prints the ratio with `.2f`. The `nothing obvious` line at `:2134` uses the
same unrounded value.

Executed: 241 calls over 201 turns (1.199) print:

```
  batching           1.20 tools per turn — 241 calls over 201 turns that sent one, in this transcript alone; most turns send a single call, and each turn costs 9s of model time on top of the command
```

and no `nothing obvious` line. The protocol states the advisory as *below 1.2*
(`docs/review-handoff-protocol.md:644`). So a reader sees 1.20 flagged by a
rule that says below 1.2. This is the same defect 🟡 1 named, in the reading
that existed before this work item.

The code is not this branch's. The class is, because contract §12 says the fix
for 🟡 1 is owed to every instance of the same cause. The fix commit closed
only the instance in `report_grades`.

The smith can answer with grounds instead. S10 holds the plain reading
unchanged, and the defect predates this work item. In that case it is a
deferral, and the owner opens the issue. The rounding does not move S10's own
assertion, because a 1.00 transcript still prints the advisory. The fix is
fenced below.

### ⬜ 9 — the fix left three lines unwrapped

- `skills/verify/scripts/session_cost.py:2500` runs to 120 columns inside the `report_grades` docstring. Ruff passes, because E501 is not selected.
- `agents/framer.md:180`, *call. Six is a default and not a*, and `:198`, *#456). It is a*, are ragged ends left by the edit. `tests/test_docs_line_wrap.py` is green.

None of these changes behaviour or a fact.

## Regression tests to plant

- `tests/test_session_cost.py`, beside `test_the_report_stops_claiming_one_at_a_time_above_a_ratio_of_one`: a plain reading printed at 1.20 is not flagged (🟡 8). Use 40 two-call turns and 161 one-call turns: no `batching` line, and `nothing obvious` present. Seen red at `618dc68f` by this round's probe, on its first half. The case is fenced under 🟡 8.

## Facts for the evidence ledger

- #456 records exactly four framer readings over 0.12.1 and 0.12.2: 1.48 (0.12.1), 1.64 (#423), and the stalled 1.56 and 1.80 (#424). #468 has none. Opened by this round on 2026-10-01. The P1 row's correction note rests on it.
- If 🟡 8 is fixed, the plain reading's comparison needs a row of its own in this work item's fragment. No existing row anchors the `report` function's advisory.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1 is closed at its coordinate — the grade compares the ratio rounded to the two places it is printed to | `skills/verify/scripts/session_cost.py:2511` | confirmed | executed: the new unit red with the round removed, green at the target; the class's other instance is finding 8 |
| 🟢 | round 1's finding 2 is closed — 0.12.1 and 0.12.2 read 1.48–1.80, two finished and two stalled, and the band says *that finished* | `agents/framer.md:189` | confirmed | #456 opened: 1.48 under 0.12.1, 1.64 under #423, 1.56 and 1.80 under #424, no framer under #468; the opening case red against the pre-fix file |
| 🟢 | round 1's finding 3 is closed — the files the spawn prompt names are one call whatever their number, and the bound is on each later call | `agents/framer.md:175` | confirmed | read against `skills/agent-contract/SKILL.md:246`; the case red against the pre-fix file; no other shipping carrier |
| 🟢 | round 1's finding 4 is closed — the framing row says the section now replaces the hold-back | `docs/review-handoff-protocol.md:633` | confirmed | executed: the protocol case red against the pre-fix protocol |
| 🟢 | round 1's finding 5 is closed — the counts sentence puts a no-call segment of a graded kind among the ungraded and claims nothing of a no-call smith | `skills/verify/scripts/session_cost.py:2540` | confirmed | executed: the no-paired-call case red with the old sentence restored |
| 🟢 | round 1's finding 6 is closed — the docstring says `--json` alone cannot tell exempt from unknown | `skills/verify/scripts/session_cost.py:2358` | confirmed | read; no carrier of the old claim in `docs/`, `agents/`, either README or `skills/verify/SKILL.md` |
| 🟢 | round 1's finding 7 is closed — the cross-pin compares both whole tables | `tests/test_the_handoff_before_round_one.py:584` | confirmed | executed: an entry added to `SEGMENT_BARS` alone, and a row added to the protocol alone, each turn it red |
| 🟢 | the new unit pins its defect — the table regexes hold the fixture at the boundary and the grade assertion goes red unrounded | `tests/test_session_cost.py:3271` | confirmed | executed: red against the unrounded comparison, green at the target |
| 🟢 | the four other-ledger re-stamp notes are true | `seal/ledger.md`, `seal/releases/0.4.0.md`, `seal/releases/0.8.2.md`, `seal/releases/0.15.7.md` | confirmed | read against the protocol diff, whose one change in the section is the framing Grounds cell; unscoped `evidence-check .` exit 0, 3180 ok, 0 drifted |
| 🟡 8 | the plain reading compares the unrounded ratio with 1.2 and prints it rounded, so 1.199 prints `batching 1.20 tools per turn` and drops `nothing obvious` — finding 1's class, left standing | `skills/verify/scripts/session_cost.py:2102` | open | executed: 241 calls over 201 turns; the protocol states the advisory as below 1.2 at `docs/review-handoff-protocol.md:644`; may be answered with grounds (S10, predates the work item) as a deferral the owner opens |
| ⬜ 9 | one docstring line runs to 120 columns and two prose lines end ragged after the fix's edit | `skills/verify/scripts/session_cost.py:2500` | open | read; ruff and the line-wrap case are green, and nothing changes in behaviour or fact; also `agents/framer.md:180` and `:198` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over eight modules (test_session_cost, test_the_handoff_before_round_one, test_a_segment_feeds_the_flow_log, test_docs_line_wrap, test_no_real_identifiers, test_one_word_one_meaning, test_a_merge_cannot_silently_drop_a_correction, test_a_moved_rule_leaves_its_definition) at the target | exit 0, 493 passed |
| `bin/evidence-check .`, unscoped, at the target | exit 0; 3180 ok, 0 drifted, 0 broken |
| `ruff check` and `ruff format --check` over the three changed Python files | exit 0 and exit 0 |
| `round` removed from the comparison in `report_grades`, with a `scribe` entry and bar added to `SEGMENT_BARS` | exit 1: the new unit names both rows at `1.80` and `1.40`; the cross-pin names `scribing` on the script side alone; reverted |
| a `scribing` row added to the protocol's bars table, with finding 5's old sentence restored | exit 1: the cross-pin names `scribing` on the protocol side alone; the no-paired-call case red; reverted |
| `agents/framer.md` and `docs/review-handoff-protocol.md` checked out at `0340a8bd` | exit 1: the opening case on *whatever their number*, the protocol case on the old clause; restored |
| a `test_tmp_*` probe: a plain reading of 40 two-call and 161 one-call turns (1.199) | exit 1: `batching 1.20 tools per turn`, no `nothing obvious`; probe deleted |
| `gh issue view 456 --comments` | the four framer readings and their releases, as above |
| broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Paste-ready fixes

### 🟡 8

`skills/verify/scripts/session_cost.py`, in `report`, replacing the two
comparisons with 1.2:

```python
    # Compared at the two places the ratio is printed to, as `report_grades`
    # does: unrounded, 241 calls over 201 turns (1.199) printed `batching
    # 1.20 tools per turn` under an advisory the protocol states as below 1.2,
    # and the `nothing obvious` line went missing beside it.
    shown = round(data["tools_per_turn"], 2)
    if shown < 1.2:
```

```python
    if same <= 0 and shown >= 1.2:
        print("  nothing obvious — the command time is the command's own cost")
```

`tests/test_session_cost.py`, after
`test_the_report_stops_claiming_one_at_a_time_above_a_ratio_of_one`:

```python
def test_a_plain_reading_printed_at_the_advisory_is_not_flagged(tmp_path):
    """241 calls over 201 turns is 1.199, which prints as 1.20. The advisory
    sits below 1.2, so a batching line printing 1.20 contradicts the rule that
    printed it, and the `nothing obvious` line went missing beside it."""
    lines = []
    for i in range(40):
        lines += [
            message(
                i * 10,
                [use(f"d{i}a", f"ls a{i}"), use(f"d{i}b", f"ls b{i}")],
                message_id=f"md{i}",
            ),
            result(i * 10 + 1, f"d{i}a"),
            result(i * 10 + 2, f"d{i}b"),
        ]
    for i in range(161):
        second = 400 + i * 10
        lines += [
            message(second, [use(f"s{i}", f"cat f{i}")], message_id=f"ms{i}"),
            result(second + 1, f"s{i}"),
        ]
    path = tmp_path / "p.jsonl"
    path.write_text("\n".join(lines) + "\n")
    out = run([str(path)]).stdout
    assert "batching" not in out, out
    assert "nothing obvious" in out, out
```

### ⬜ 9

`skills/verify/scripts/session_cost.py`, the `report_grades` docstring
paragraph, re-wrapped:

```python
    **A line per row under its bar, and the counts always.** At the bar is
    meeting it, and the ratio compared is the one printed, to two places, in
    the table above and on the line: compared unrounded, 79 calls over 44
    turns (1.7955) printed `1.80 tools per turn against the reviewing bar of
    1.8`, a line contradicting the row above it (round 1's 🟡 1). Every
    count prints even when nothing is under, which is `report_segments`' own
    rule: a grade that silently matched nothing reads exactly like a run
    whose rows all met their bars. Exempt and ungraded are counted apart,
    because one is the protocol's judgment and the other is a kind nobody has
    measured a band for.
```

Needs a fix: yes — 🟡 8 (the plain reading's batching advisory prints 1.20
under a threshold of 1.2, finding 1's class left standing), unless the smith
answers it with grounds as a deferral the owner opens
Loses a record or crashes: no

The broad gate has not come due: 🟡 8 is open. If it is answered with grounds
rather than fixed, nothing else is open, and what comes due is the sealer's
spawn.

## Proof block

Files opened at `618dc68f` in the clone:
- the work item's rounds: `rounds/round-1.md`, `rounds/round-1-report.md`;
- the fix commit `fe122afe` in full, by diff and by word diff over the ledger files;
- `skills/verify/scripts/session_cost.py` (2060–2145, 2348–2364, 2480–2560), `agents/framer.md` (the fix hunks and 175–198), `docs/review-handoff-protocol.md` (632–644 by search), `skills/agent-contract/SKILL.md` §10 as received;
- `tests/test_session_cost.py` (1–135 by search, 293–330, the new unit and the changed cases by diff), `tests/test_the_handoff_before_round_one.py` (the changed cases by diff);
- `seal/ledger.md` row 97, `seal/releases/0.4.0.md` row 114, `seal/releases/0.8.2.md` row 42, `seal/releases/0.15.7.md` row 41, and the work item's ledger fragment by word diff;
- `spec.md` S10 by search, and `pyproject.toml` for the ruff selection;
- the tracker: issue #456 with its comments.
