# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — review round 1

| Field | Value |
|---|---|
| Target SHA | c9d5114ef366c4190f6887b379a499cff0df8d93 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 696 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a row printed at its bar is named under it), 🟡 2 (a measurement attributed to the wrong release in a shipped definition and changelog), 🟡 3 (the per-call bound contradicts §10's requirements read) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 targets `c9d5114e` and the diff `cd24f516..c9d5114e`, the whole build. It was asked to check stage 1 against `spec.md` and the approved plan, then to attack five things:
1. The grade in `session_cost.py`: a row exactly at its bar, an unknown kind, a resumed agent's slices, a segment with no call, the `--json` rows' `kind` and `bar`, and every existing output unchanged where no grade applies.
2. The cross-pin between the script's constants and the protocol's table, in both directions.
3. `agents/framer.md` §*How a frame opens*: bounded rather than forbidden batching, §10 cited, consistent with the warden's 1.89, and the 1.4 bar's band coordinates.
4. The ledger's 22 re-stamped rows and the two corrected in place.
5. The class: every other place stating that the script cannot tell kinds apart, a universal 1.2 bar, or the prohibition.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the grade compares the unrounded ratio and prints it rounded, so a row shown at 1.80 is named under the 1.8 bar | `skills/verify/scripts/session_cost.py:2507` | open | executed probe: 79/44 and 67/48 print `1.80 … bar of 1.8` and `1.40 … bar of 1.4`; S7's fixtures are exact fractions and never exercised it |
| 🟡 2 | *the 0.12.2 framers … read 1.48–1.64* gives 0.12.2 a 0.12.1 reading and leaves out 0.12.2's stalled 1.56 and 1.80 | `agents/framer.md:188` | open | #456 opened: 1.48 sits under its 0.12.1 section, 1.64 under #423's comment, 1.56 and 1.80 under #424's; also in the changelog fragment line 5 and the test docstring line 293 |
| 🟡 3 | the about-six bound on one call has no exception for the files the handoff names, which §10 says go out in one call | `agents/framer.md:175` | open | `skills/agent-contract/SKILL.md:246` read; the bullet cites §10 as the rule it applies |
| ⬜ 4 | *which `agents/framer.md` no longer does* reads as if the definition once held the opening reads back | `docs/review-handoff-protocol.md:633` | open | the prohibition lived in no file, per spec §Grounding and the definition case's own docstring |
| ⬜ 5 | the counts sentence lists *a segment that made no call* among rows with no bar; a no-call smith is counted exempt and a no-call warden carries bar 1.8 | `skills/verify/scripts/session_cost.py:2536` | open | read: exemption keys on kind, not on numbers; counts are right, the sentence is not |
| ⬜ 6 | the docstring says a program reading `--json` can tell exempt from unknown through `SEGMENT_BARS`, which is not in the reading | `skills/verify/scripts/session_cost.py:2360` | open | read; the two `kind` keys sit on different objects and are not confusable by path, and I7 fixed both keys' shape |
| ⬜ 7 | the cross-pin loops over two named kinds, so an entry added to either table alone passes | `tests/test_the_handoff_before_round_one.py:550` | open | executed: a `scribe` entry with a bar and no protocol row left the case green; a value moved on the protocol side alone turned it red |
| 🟢 | the ledger stays true at the target, and both in-place corrections say something true | `seal/releases/0.4.0.md`, `seal/releases/0.15.7.md` | confirmed | unscoped `evidence-check .` exit 0, 3179 ok, 0 drifted; correction and re-read notes read against the diff |
| 🟢 | Q1's reading reproduces: the frame's segment is 50 calls at 4.17 tools per turn, graded against 1.4 | `seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/phases/phase-4.md` | confirmed | executed `--json` over the run's transcript at the target; the largest batch of 11 was not re-derived |
| 🟢 | the class holds no other carrier of *cannot tell kinds apart*, a universal 1.2 bar, or the prohibition | README.md, README.ko.md, `skills/`, `docs/`, `templates/`, `agents/` | confirmed | read, by search over each |

## Paste-ready fixes

```python
    graded = [row for row in rows if row["bar"] is not None and row["numbers"]]
    # The ratio is printed to two places, in the table above and on the line
    # below, so the grade compares the figure a reader sees: a row printed at
    # 1.80 meets a bar of 1.8. Unrounded, 79 calls over 44 turns (1.7955)
    # printed `1.80 tools per turn against the reviewing bar of 1.8`.
    under = [
        row
        for row in graded
        if round(row["numbers"]["tools_per_turn"], 2) < row["bar"]
    ]
```
```python
def test_a_row_printed_at_its_bar_meets_it(tmp_path):
    """79 calls over 44 turns is 1.7955 and 67 over 48 is 1.3958: the table
    prints both as 1.80 and 1.40, so a line naming either under 1.8 or 1.4
    contradicts the row above it."""
    out = segment_report(
        graded_run(
            tmp_path,
            [
                ("specseal:warden", [2] * 35 + [1] * 9),
                ("specseal:framer", [2] * 19 + [1] * 29),
            ],
        )
    )
    assert grade_lines(out) == [], out
    assert "every graded row meets its kind's bar" in " ".join(out.split()), out
```
```python
        if row["bar"] is not None
        and round(row["numbers"]["tools_per_turn"], 2) < row["bar"]
```
```
Nothing here limits how many reads go out together below that bound. Every
framer that read 1.00–1.12 since 0.12.3 was a spawn whose prompt held its
opening reads back, and the framers of 0.12.1 and 0.12.2 that finished,
never told that, read 1.48–1.64.
```
```
  framer reading since sat at 1.00–1.12 tools per turn; the
  0.12.1 and 0.12.2 framers that finished, never told, read 1.48–1.64. The
  rule was in no file, which
```
```
    burst; the 0.12.1 and 0.12.2 framers that finished, never told, read
    1.48-1.64. Writing that
```
```
- **Bound the size of one call, not the reading.** §10 is the rule you are
  applying: what one coordinate names goes out together, and the files your
  spawn prompt names are one such call whatever their number. The bound is
  on each call of the wide reading after that — about six reads or ranges —
  and never the whole reading list of the section above sent as the opening
  call. Six is a default and not a measured limit; the 0.15.1 framers sent
  2.3–3.1 tools per turn and all of them finished (#548), and #640 is where
  the number can be overturned.
```
```python
    assert "whatever their number" in section, (
        "the bound reaches the files the handoff names, which §10 says go out "
        "in one call"
    )
```
```
... every framer reading under the bar since 0.12.3, at 1.00–1.12, was a spawn whose prompt held its opening reads back, which `agents/framer.md` §*How a frame opens* now replaces with a bound on one call (#640) |
```
```python
        "this ratio. A row with no bar — a kind not listed, a row no spawn\n  "
        "named — is ungraded, and so is a graded kind's segment that made no "
        "call."
```
```python
    """A segment's kind and bar, as the two keys every segment row carries.

    `kind` is `""` where no spawn named the row, and `bar` is None for an
    exempt kind and for a kind the table does not know alike. The page tells
    those two apart through `SEGMENT_BARS`; a program holding only `--json`
    cannot, because the table is this script's and not the reading's."""
```
```python
    entries = re.findall(r'^    "(\w+)": \("(\w+)", ([\d.]+|None)\),$', script, re.M)
    rows = dict(
        re.findall(r"^\| (\w+) \| tools per turn \*\*≥ ([\d.]+)\*\* \|", protocol, re.M)
    )
    graded = {segment: bar for _, segment, bar in entries if bar != "None"}
    assert graded == rows, (
        f"`SEGMENT_BARS` grades {graded} and the protocol's table states {rows} "
        "-- add, move or remove both or neither"
    )
```

## Executed probes

| What was run | Result |
|---|---|
| a probe `test_tmp_*` in the clone's `tests/`, warden 79/44 and framer 67/48 through `graded_run` and `segment_report` | exit 1: both rows named at `1.80` and `1.40` against bars of 1.8 and 1.4; probe deleted |
| `bin/test` over nine modules (test_session_cost, test_the_handoff_before_round_one, test_a_segment_feeds_the_flow_log, test_a_moved_rule_leaves_its_definition, test_docs_line_wrap, test_one_word_one_meaning, test_no_real_identifiers, test_the_rules_have_one_owner, test_a_merge_cannot_silently_drop_a_correction) | exit 0, 552 passed |
| `bin/test tests/test_chain_hooks_hardening.py -k questions_are_collected` | 1 passed |
| `bin/evidence-check .`, unscoped | exit 0; 3179 ok, 0 drifted, 0 broken |
| cross-pin with the protocol's framing value moved to 1.5 alone | exit 1, `grades a framer row against 1.4 and the protocol's framing bar is 1.5`; reverted |
| cross-pin with a `scribe` entry and bar added to `SEGMENT_BARS` alone | exit 0, the gap ⬜ 7 names; reverted, clone tree clean |
| `session_cost.py --json` over the run's transcript (`/Users/x/.claude/projects/-Users-x-Documents-GitHub-SpecSeal/b5ffa967-bd00-4976-b4ed-5a1751a5b58e.jsonl`) | exit 0; `Frame #640 batching segments` 50 calls, 4.17, kind `framer`, bar 1.4 |
| the largest batch of 11 in one turn | not run by this round, carried from `phases/phase-4.md` |
| `survivor-check --range cd24f516..HEAD` | not run by this round, carried from `phases/phase-4.md` |
| broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
