# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — review round 2

| Field | Value |
|---|---|
| Target SHA | 618dc68f5435bf8116f6295b0c08160461bcc5d9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 696 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `090edf3ba195109857f46d1f6f206c2f1e27a603..6bdf8642e7fea0a67b9eb35f82f081f626a56da1`, 1 commit |
| Contract changes | none |
| New units | test_a_plain_reading_printed_at_the_advisory_is_not_flagged (depth 1) |
| Needs a fix | yes — 🟡 8 (the plain reading's batching advisory prints 1.20 under a threshold of 1.2, finding 1's class left standing), unless the smith answers it with grounds as a deferral the owner opens |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is the verifying round. It targets `618dc68f` and verifies the fix range `0340a8bd..fe122afe`, one commit. It was asked whether each of round 1's seven `fixed` verdicts is actually closed, with its class closed too. It was also asked to review the one unit the fixes created, `test_a_row_printed_at_its_bar_meets_it`, as a finding surface, and to check the four other-ledger re-stamps the fix made.

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
| 🟡 8 | the plain reading compares the unrounded ratio with 1.2 and prints it rounded, so 1.199 prints `batching 1.20 tools per turn` and drops `nothing obvious` — finding 1's class, left standing | `skills/verify/scripts/session_cost.py:2102` | **fixed** `6bdf8642e7fea0a67b9eb35f82f081f626a56da1` | fixed at 6bdf8642e7fea0a67b9eb35f82f081f626a56da1; executed: 241 calls over 201 turns; the protocol states the advisory as below 1.2 at `docs/review-handoff-protocol.md:644`; may be answered with grounds (S10, predates the work item) as a deferral the owner opens |
| ⬜ 9 | one docstring line runs to 120 columns and two prose lines end ragged after the fix's edit | `skills/verify/scripts/session_cost.py:2500` | **fixed** `6bdf8642e7fea0a67b9eb35f82f081f626a56da1` | fixed at 6bdf8642e7fea0a67b9eb35f82f081f626a56da1; read; ruff and the line-wrap case are green, and nothing changes in behaviour or fact; also `agents/framer.md:180` and `:198` |

## Paste-ready fixes

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:2507` | round 1's 🟡 1 — fixed |
| round-1 | `agents/framer.md:188` | round 1's 🟡 2 — fixed |
| round-1 | `agents/framer.md:175` | round 1's 🟡 3 — fixed |
| round-1 | `docs/review-handoff-protocol.md:633` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:2536` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:2360` | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_the_handoff_before_round_one.py:550` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/releases/0.4.0.md`, `seal/releases/0.15.7.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/phases/phase-4.md` | round 1's 🟢 — confirmed |
| round-1 | README.md, README.ko.md, `skills/`, `docs/`, `templates/`, `agents/` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
