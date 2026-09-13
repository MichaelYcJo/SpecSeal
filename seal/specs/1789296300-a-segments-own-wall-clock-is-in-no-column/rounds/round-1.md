# 1789296300-a-segments-own-wall-clock-is-in-no-column — review round 1

| Field | Value |
|---|---|
| Target SHA | 0436688c818b1ba4a5b9a255937cb73b9aa710d8 |
| Ran by | warden on claude-opus-5 |
| PR | 380 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | test_an_unnamed_file_that_was_resumed_is_counted_once (depth 1); test_two_coordinator_messages_in_a_row_do_not_invent_a_slice (depth 1); test_a_file_whose_first_window_is_empty_still_carries_its_tokens (depth 1); test_a_resumed_file_that_called_nothing_at_all_still_gets_its_row (depth 1); test_the_breach_line_says_which_agents_the_section_binds (depth 1) |
| Needs a fix | yes — findings 1, 2, 3 and 4. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the work item, against the whole branch: no earlier round to inherit. The work item carries #350 and #343 together, because both land on one unbuilt thing — a reader that opens a spawned segment's own transcript.

The reviewer was asked to open nine claims rather than accept them, chief among them the harness fact the whole mode rests on (the `Agent` result is written when the spawn is ACCEPTED, not when it finishes), the re-measured join tolerance, the three frame corrections measurement produced, and #343's empirical claim that 13 of 43 real runs carry a §6 finding. It was warned that an aggregate is not a coordinate (§5) and told to check what a finding actually is before trusting the 13 — which is what produced finding 3.

The orchestrator verified findings 1, 2 and 3 independently before this record was written. Finding 1 by reading `measure_segments`: the `unnamed` count at `session_cost.py:1177` sums over `rows`, which are slices, while the resumed count six lines away de-duplicates. Finding 2 by re-running the mode over every segment row of every run on this machine — **43 runs, 379 named rows, median 716 s and mean 1020 s** — which confirms the reviewer's 715/1020 and confirms that *a median of about 1,000* names the mean. Finding 3 by listing `agents/`: this repository defines `framer`, `scribe`, `sealer`, `smith` and `warden`, and `claude-preset:code-reviewer` is none of them.

Finding 2 is the sharper one for this repository's own habits: the same diff inherited two aggregates from earlier work, re-measured the join tolerance and carried the median unchecked into three new places, one of them the release note.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `unnamed` is summed over slices, not transcripts, so a resumed unnamable file is counted once per stretch — the header mixes units and the §6 reconciliation prints a false disagreement | `skills/verify/scripts/session_cost.py#measure_segments` | **fixed** `b35ed6d` | fixed at b35ed6d — `unnamed` now counts distinct transcripts. The class was enumerated rather than the coordinate patched: `transcripts` is files, `spawns` is calls, `unclaimed` is spawns, `report_segments`' resumed count already de-duplicated, and `breaches` is per slice on purpose — `unnamed` was the only member at the wrong grain. Case red first at `unnamed: 2` for one unnamable file; Executed. Two fixtures reproduce both symptoms; one of the 43 real runs on this machine already reads `unnamed=3` for two unnamable files. Contradicts `#segment_slices`' own docstring, and the resumed count six lines away de-duplicates correctly |
| 2 | 🟡 *a median of about 1,000 seconds* is the mean; the measured median is 715 s for named rows, 661 s for all rows. Carried into three new places, one of them the release note | `skills/verify/scripts/session_cost.py` :39–40 and `#measure_segments`; `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/changelog.md:10` | **fixed** `c2eb6f8` | fixed at c2eb6f8 — the three new places now say about 700 seconds. Re-measured with the mode over every segment row of the 43 runs with a `subagents/` directory on this machine: median **716 s** over 381 named rows and 664 s over all 433, mean **1,018**. The number was kept rather than dropped — a reader deciding whether to run the mode needs the size of what they are missing — but it no longer travels without its measurement: `measure_segments` now carries what it was taken over, that the population grows, and that #145's 1,000 is the mean. `spawn_cycles` and the `DELEGATING` comment still carry #145's figure and the docstring says so; the ledger half is row 6 below; Executed with the mode itself over every segment row of all 43 runs: median 715 s, mean 1020 s. An inherited aggregate (#145) propagated without re-derivation — contract §5 — while the other inherited aggregate in the same diff was re-measured |
| 3 | 🟡 the §6 line cites the contract at agents the contract does not bind | `skills/verify/scripts/session_cost.py#report_breaches` | **fixed** `7dcbcdf` | fixed at 7dcbcdf (line and case) and `c2eb6f8` (the counts in `changelog.md` and `overview.md`). Measured independently: 43 runs, **13 carry the line**, **12 name an agent this plugin spawns** — 40 `Agent` calls by wardens, 4 by smiths, 1 by `claude-preset:code-reviewer`, which `agents/` does not define. The row is stated rather than filtered, which is the direction the two counts beside it already take; Executed. 1 of the 13 runs carrying the line names `claude-preset:code-reviewer`, which no definition here governs and whose own procedure instructs the fan-out |
| 4 | 🟡 two adjacent coordinator messages produce a call-less slice, inflating the `N/of` denominator and re-using `no paired call` for a second meaning | `skills/verify/scripts/session_cost.py#segment_slices` | **fixed** `a31398e` | fixed at a31398e, with the unpinned arm found and closed at `d0a455e`'s parent `4af3441`. Judged a fix rather than an answered row: zero occurrences in 43 runs, but the harm is to counts a reader trusts without opening the file — a `3/3` where the agent worked twice — and two adjacent coordinator messages is the shape this repository's own workflow produces. Two arms, two cases: the dropped empty window, and the file that paired no call anywhere, which still owes its single row; Executed on a fixture. Reachable and not observed: zero call-less slices across all 43 real runs |
| 5 | ⬜ seven `seal/ledger.md` rows re-stamped `b1d57f7c` → `7837c909` with `Checked` left at 2026-09-09 and 2026-09-12, for a section this branch rewrote on 2026-09-13 | `seal/ledger.md` | **fixed** `f63db1c` | fixed at f63db1c — all seven `Checked` cells at 2026-09-13. Each of the seven was re-read against the section as it now stands before its cell moved: F5's absence is untouched (the one changed hunk names no issue number and no milestone), R3's nine-row run-level table is outside that hunk, G5's title format is still in the tracker document and absent from the skill, and the four unlettered rows are about the orchestrator boundary, the between-the-rows refusal and the vocabulary case, none of which the hunk reaches. Every one already carried a dated 2026-09-13 re-read note in its Notes cell, so the reading had happened and the column contradicted it; the script that moved the cells refuses a row with no such note; Executed on the diff cell by cell, and read against `#reverify`'s RIDER, which names this exact failure from round 1 of #120 — six rows then, seven now |
| 6 | ⬜ those seven rows are anchored on a whole heading path, so rows about untouched paragraphs (F5, R3) drift with any edit to the section | `seal/ledger.md` | deferred `seal/follow-up.md` | Not `evidence-todo.md`: that file is for a fact a reviewer verified that never reached the ledger, and `CLAUDE.md` makes the release fold refuse while any has an open row — a re-anchoring chore would block 0.11.3. Not an issue either, because contract §6 withholds posting from every agent. Written at `f63db1c`, naming the repository owner and carrying both sides: `CLAUDE.md`'s condition for narrowing (*unless whole-unit hashing has been measured to drift rows on unrelated edits*) is now met by measurement, and against it, five of the seven rows belong to work items that shipped in earlier releases and would be re-anchored by somebody who did not write them |
| 7 | ⬜ every segment transcript is read five times on a `--json` run, twice for the same token figure | `skills/verify/scripts/session_cost.py#segment_slices`, `#main` | **fixed** `d76cba3` | fixed at d76cba3 — the comment measured rather than reworded. `measure_segments` takes 257ms, 698ms and 926ms over the three widest runs on this machine (18, 30 and 35 segments) against `analyse`'s 28–36ms on the same transcripts: nine to thirty-three times the reading being printed, where `measure_cycles` was half again. The gating stays as it is, on the ground `spawns` is in `--json` for; what changed is that the cost is on the page instead of borrowed from a sibling's measurement. The four reads per transcript and the token walk `main` repeats are named at the line; Read. The parallel comment for `spawns` measured its cost before admitting it to `--json`; this one asserts the same terms without measuring, and the terms differ — arithmetic in memory against file input over a tree |
| 8 | ⬜ the proof block records 98 for `tests/test_session_cost.py`; the module is 100, which is what the pull request body says | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md` | **fixed** `f63db1c` | fixed at f63db1c — and every module's count is stated rather than one. The module read 100 at the handoff and 104 at the pass's end; it reads 105 now; Executed — the module alone reads `100 passed` |
| 9 | ⬜ the naming divergence was corrected in `plan.md` in place and the nested-transcript model was left standing in `spec.md`; the divergence table does not say which convention applies | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md`, `spec.md` :132 | **fixed** `f63db1c` | fixed at f63db1c — with the proposed sentence corrected before use. It contrasted `spec.md` with `plan.md`, and `plan.md` still carries the nested-transcript model at :20, :41, :100 and :103 — so a file-kind rule is one `plan.md` itself breaks. What decides it is what the divergence IS: a name absent from the tree sends a reader to a symbol that does not exist and was corrected everywhere it appeared, while a picture of the harness that measurement killed changes no instruction anyone follows and stands where it was written, in both files; Read. Both treatments are defensible; a reader meeting them in one table cannot tell which rule produced which |

## Paste-ready fixes

```python
        "unnamed": sum(1 for row in rows if not row["named"]),
```
```python
        # Over TRANSCRIPTS, never over rows. A resumed file is several rows
        # carrying one name, so counting rows makes this climb with every
        # resume -- which is the failure `segment_slices` gives every slice
        # the file's name to avoid, undone one function later. `report_breaches`
        # reconciles the §6 count against this number, so a row count makes a
        # run whose counts agree print that they do not, and sends a reader
        # looking for a child transcript that was never missing. Measured on
        # the machine this was written on: one of 43 runs already reads 3 for
        # two unnamable files. The resumed count below de-duplicates the same
        # way, which is what this line was missing rather than a new rule.
        "unnamed": len({row["transcript"] for row in rows if not row["named"]}),
```
```python
def test_an_unnamed_file_that_was_resumed_is_counted_once(tmp_path):
    """The count is a reading about the harness — how many files this run
    holds that no `Agent` call in the parent can name. A resumed file is
    several rows carrying one name, so counting rows makes the number climb
    with every resume, which is exactly what giving each slice the file's
    name exists to prevent.

    Red before the fix: `unnamed` reads 2 for one unnamable file, and the
    reconciliation below prints a disagreement that is not there."""
    main = call("a", 0, 10, "git status --short") + spawn(
        "A", 25, 625, "specseal:smith", "Build phase 1"
    )
    path = write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": [
                *worked(625, "s1"),
                *spawn("N", 700, 701, "general-purpose", "search the tree"),
            ],
            # The child of that spawn: no `Agent` call in the parent can name
            # it, and the coordinator resumed it.
            "inner/agent-deep.jsonl": [
                *worked(701, "d1"),
                coordinator_message(9000),
                *worked(9010, "d2"),
            ],
        },
    )
    segments = segments_of(path)
    assert segments["transcripts"] == 2, segments
    assert len(segments["rows"]) == 3, segments["rows"]
    assert segments["unnamed"] == 1, segments
    out = " ".join(segment_report(path).split())
    assert "1 segment named by nobody" in out, out
    # One call inside a segment against one file the parent cannot name: the
    # two agree, and the sentence that fires on a disagreement must not.
    assert "1 `Agent` call inside a segment, against 1 segment" in out, out
    assert "the two agree" in out, out
    assert "do not agree" not in out, out
```
```
agent runs for a median of about 1,000 (#350). That number is in the segment's
```
```
agent goes on working for a median of about 700 seconds (#350). That number is
in the segment's
```
```
    when the spawn is ACCEPTED; the agent then runs for a median of about
    1,000 seconds, and that interval is in none of `--spawns`' columns, in
    any row. It is in the segment's own file, and this opens it.
```
```
    when the spawn is ACCEPTED; the agent then goes on working for a median of
    about 700 seconds, and that interval is in none of `--spawns`' columns, in
    any row. It is in the segment's own file, and this opens it.

    **The 700 is this mode's own reading and it corrects an inherited one.**
    #145 published *a median of about 1,000 seconds* and `spawn_cycles` still
    carries it; measured here with this mode over every segment row of the 43
    runs on the machine it was built on, the median is 715 s for named rows
    and 661 s for all rows. 1,000 is the MEAN (1,020), which is a different
    statistic wearing the same word. Re-measure rather than carry it: an
    aggregate is not a coordinate, and this is the first instrument that could
    check it.
```
```
  seconds while the agent goes on working for a median of about a thousand.
```
```
  seconds while the agent goes on working for a median of about seven hundred.
```
```python
        print(
            "\n  §6 binds the agents this plugin spawns. A row above naming "
            "an agent from\n  somewhere else is still a spawn made inside a "
            "segment and still worth seeing,\n  but which rule it answers to "
            "is that agent's own definition's to say."
        )
```
```python
def test_the_breach_line_says_which_agents_the_section_binds(segment_that_spawned):
    """The line fires on any `Agent` call in any segment's transcript, and
    the walk cannot tell a plugin agent from one whose own procedure
    instructs the fan-out. Measured: of the runs on this machine carrying the
    line, one names an agent no definition here governs.

    Red before the fix: the report cites the section and never says who it
    reaches."""
    out = " ".join(segment_report(segment_that_spawned).split())
    assert "§6 binds the agents this plugin spawns" in out, out
    assert "that agent's own definition's to say" in out, out
```
```python
    rows = []
    for index in range(len(cuts) + 1):
        window = call_windows[index]
        rows.append(
            {
                **labels,
                "slice": index + 1,
                "slices": len(cuts) + 1,
```
```python
    # A window with no call in it is not a stretch of work. The coordinator
    # can send one message and then another before the agent acts, and the
    # empty window between them was printed as a slice the agent never worked
    # -- which also pushed every later `N/of` up by one, so the second of two
    # stretches read as `3/3`. It also re-used `no paired call`, which means a
    # whole transcript that read and thought and spent tokens, for a slice
    # that spent nothing. Reachable and not observed: zero call-less slices
    # across the 43 runs on the machine this was written on.
    #
    # The `or [0]` is the file that paired no call at all. It still owes its
    # row, for the reason `measure_segments`' docstring gives.
    kept = [i for i in range(len(cuts) + 1) if call_windows[i]] or [0]
    rows = []
    for position, index in enumerate(kept):
        window = call_windows[index]
        rows.append(
            {
                **labels,
                "slice": position + 1,
                "slices": len(kept),
```
```python
                "tokens": token_totals([transcript]) if index == 0 else None,
```
```python
                # The first KEPT slice, not window 0, which may have been
                # dropped as empty. The figure is the file's and rides one row.
                "tokens": token_totals([transcript]) if position == 0 else None,
```
```python
def test_two_coordinator_messages_in_a_row_do_not_invent_a_slice(tmp_path):
    """A cut is a marker, not a stretch of work. The coordinator can send one
    message and then another before the agent acts, and the empty window
    between them is not a slice — printing it gives the file a stretch the
    agent never worked and reports the second of two as `3/3`.

    Red before the fix: three rows, the middle one `no paired call`."""
    main = call("a", 0, 10, "git status --short") + spawn(
        "A", 25, 625, "specseal:smith", "Build phase 1"
    )
    path = write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": [
                *worked(625, "s1"),
                coordinator_message(9000),
                coordinator_message(9005),
                *worked(9010, "s2"),
            ]
        },
    )
    rows = segments_of(path)["rows"]
    assert len(rows) == 2, rows
    assert [(row["slice"], row["slices"]) for row in rows] == [(1, 2), (2, 2)], rows
    assert all(row["numbers"] for row in rows), rows
    # The file's token figure still rides one row, and it is the first kept.
    assert rows[1]["tokens"] is None, rows[1]
    out = segment_report(path)
    assert "no paired call" not in out, out
    assert "specseal:smith  2/2" in out, out
```
```
`spec.md` is left as written, because a frame document records what was true
when it was framed; `plan.md` was corrected in place for the naming divergence
because a plan is a build instruction and a name that is not in the tree sends
the next reader to a symbol that does not exist. The two divergences got
different treatments on purpose, and this sentence is why.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py tests/test_a_segment_feeds_the_flow_log.py tests/test_one_word_one_meaning.py tests/test_no_real_identifiers.py -q` | **149 passed**, exit 0. Per module: 100 · 32 · 15 · 2 |
| `evidence_check.py .` | **1158 ok · 0 drifted · 0 broken · 0 external · 0 old-format**, exit 0; record arm read this work item |
| Probe — the harness fact and the tolerance, re-measured over every run with a `subagents/` directory | 43 runs, 355 segment transcripts, 311 spawns. Named at 1.0 s: 302; at 2.0 s: 307; files below depth one: 0. Spawn interval median 2.3 s (0.4–26.3, n=302); the segment's own first-to-last stamp median 867 s. **Every delta in the account reproduces** |
| Probe — `--segments` over all 43 real runs | exit 0 on every one; **13 carry a §6 line**. 40 `Agent` calls by `specseal:warden`, 4 by `specseal:smith`, 1 by `claude-preset:code-reviewer` |
| Probe — the mode's own `unnamed` against the count of distinct unnamable transcripts, over the same 43 runs | **1 run disagrees today** (`unnamed=3`, two unnamable files). Call-less slices printed: 0 |
| Probe — contract §15, the two mutation survivors re-applied in a scratch copy of the tree | Both cases PASS unmutated and go **RED** under their mutation. The worktree was never written to |
| Probe — the published median, measured with the mode | named rows n=378, **median 715.4 s**, mean 1019.5 s; all rows n=430, median 661.1 s, mean 1020.7 s |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** Contract §2 makes it one act with one owner and this round is not it. Answerer: the sealer, spawned after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `survivor-check` has no cheat-sheet row in either README | `overview.md` §Not done | the repository owner. Correctly deferred — it is a different command, and the reviewer agrees it does not belong in this diff |
| The §6 line becoming an exit code rather than a line | `overview.md` §Not done | a later work item, choosing against the 13 readings that now exist |
| `delegated_s` keeping the meaning it was published with | #145 `questions.md` §Q4, and Q1 here, answered 2026-09-13 | the repository owner, who may revisit it now a per-segment reading exists |
| A per-slice token column | `overview.md`, divergence table row 3 | deferred by design — re-deriving it duplicates `#token_totals`' #202 rule |
| Finding 6 — re-anchoring the seven ledger rows one altitude down | `seal/follow-up.md`, written at `f63db1c` | the repository owner. Routed there rather than to `evidence-todo.md`, whose open rows make the release fold refuse, or to an issue, which contract §6 withholds from every agent |
