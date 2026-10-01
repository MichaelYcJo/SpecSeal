# Round 1 report — warden

| Field | Value |
|---|---|
| Work item | 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file (#640, draft PR #696) |
| Target SHA | c9d5114ef366c4190f6887b379a499cff0df8d93 |
| Base | `release/v0.17.0` at cd24f516 |
| Diff | cd24f516..c9d5114e, 29 files |
| Clone | a `git clone --no-local` under the session scratchpad, `<scratchpad>/1790815612/round-1/clone` |
| Ran by | specseal:warden on Opus 5.5 |

No earlier round exists, so nothing was inherited. The implementer's account
(the spawn prompt's facts, `phases/phase-4.md`, the ledger notes) was read in
full and treated as claims; what each claim met when opened is below.

## Stage 1 — spec compliance

Read against `spec.md` I1–I11 and S1–S15 and `plan.md`'s four phases.

- **I1, S1 (read).** `agents/framer.md` §*How a frame opens* comes right after §*What you read, and how widely*. It carries the skeleton-first bullet, the per-call bound and the ranged read. It cites §10 by number. No sentence forbids parallel reads, and the case that asserts the prohibition absent covers the whole file. One conflict with §10 itself is 🟡 3.
- **I2, S2 (read; band opened on the tracker).** The definition says 1.4 and promises no saving. I opened the band's coordinates: #370 holds the 0.11.2 framer at 1.46, #376 and #385 hold the three 0.11.3 framers at 1.59–1.79, and #456 holds the 0.12.1 framer at 1.48 and the 0.12.2 framer at 1.64. So *1.46–1.79 over 0.11.2–0.12.2* is true, counting only framers that finished. The sentence beside it is not: it gives 1.48–1.64 as *the 0.12.2 framers*. That is 🟡 2.
- **I3, I4, S3 (executed).** The protocol has the `framing` row and the three old rows are unchanged. The tying paragraph keeps the sentence the 1.2 cross-pin reads and narrows *cannot tell* to the plain reading. It also says `--segments` applies the bars by kind. Its tests are green. One clause in the framing row's Grounds is ⬜ 4.
- **I5, S4–S10 (executed).** The block sits between the table and the §6 block. It prints a line for each row under its bar, the three counts on every page, the exemption, and the three caveats. The exit code is 0. The plain reading and `--spawns` show no grade. One defect is 🟡 1: the comparison uses the unrounded ratio, but the line prints it rounded.
- **I6, S12 (executed, both directions probed).** `SEGMENT_BARS` uses the basename as its key. Moving the protocol's framing value alone turns the cross-pin red; the build had shown the script-side direction already. Adding a kind to one side only does not turn it red. That gap is ⬜ 7.
- **I7, S11 (executed).** Every segment row in `--json` carries `kind` and `bar`, in both branches of `measure_segments`, and every earlier key is still there. The `kind` question the orchestrator raised is judged in ⬜ 6.
- **I8, S13 (executed).** `skills/verify/SKILL.md` step 1 and both READMEs carry the new clause, and their case is green.
- **I9 (executed, narrow).** Nine modules: 552 passed. That covers the three edited modules plus the moved-rule, line-wrap, one-word, real-identifier, one-owner and merge-correction modules. The chain-hooks batching case: 1 passed. The claim that every case was seen red first is carried from the phase records. I did not reproduce it.
- **I10, S14 (executed).** Unscoped `evidence-check .` exited 0: 3179 ok, 0 drifted, 0 broken. I read both in-place corrections, and each now says something true. The 0.4.0 bars row names the fourth kind, and its note says the old *cannot tell segment kinds apart* now holds for the plain reading only. The 0.15.7 A2 row now says `kind` and `bar` differ between the two routes, as `agent` does. The twenty `Re-read 2026-10-01` notes each name the edit made inside their unit. I checked those against the diff, and none claims a sentence the diff changed.
- **I11, S15 (executed).** `--json` over the run's transcript at the target reproduces the frame's row: `Frame #640 batching segments`, 50 calls, 4.17 tools per turn. I did not re-derive the largest batch of 11, because `--json` does not carry a per-turn maximum. It is carried from `phases/phase-4.md`.

## Stage 2 — quality

### 🟡 1 — a row printed exactly at its bar is named as under it

`skills/verify/scripts/session_cost.py:2507` compares the unrounded
`tools_per_turn` against the bar. The table above it and the grade line both
print that ratio with two decimals. A warden at 79 calls over 44 turns
(1.7955) shows **1.80** in the table, and the grade line under it reads:

```
    specseal:warden  1.80 tools per turn against the reviewing bar of 1.8
    specseal:framer  1.40 tools per turn against the framing bar of 1.4
```

This was executed with a probe built from the module's own `graded_run`. The
framer row is 67 calls over 48 turns (1.3958). Both counts are ordinary sizes
for a segment. The line contradicts itself, and it is the line a person posts
to the flow log, so somebody will act on a round that met its bar. The
build's at-the-bar case (S7) uses 9/5 and 7/5, which are exact, so the gap
between printed and compared precision was never exercised.

The fix compares the figure the page prints. `--json` keeps the unrounded
ratio, so the S11 case should compute *under* the same way.

### 🟡 2 — "the 0.12.2 framers read 1.48–1.64" names the wrong release for 1.48

`agents/framer.md:188` says *the 0.12.2 framers, never told that, read
1.48–1.64*. #456 has the 1.48 framer under its opening section, *0.12.1 — one
session, 0.11.4's tail through 0.12.1's tag*. The 1.64 framer sits in the
comment for #423, the first work item of 0.12.2. The 0.12.2 run's other two
framers are the stalled ones, at 1.56 and 1.80 (the #424 comment). So
0.12.2's framers read 1.56–1.80, and 1.48–1.64 spans two releases. The
argument still holds, because no framer without the prohibition read near
1.00. But a shipped definition and a shipped changelog entry state a
measurement that no source records.

Same-class carriers, enumerated per §12:
- shipping: `agents/framer.md:188` and the changelog fragment, line 5;
- prose: the docstring of the opening case in `tests/test_the_handoff_before_round_one.py`, line 293;
- frame records: `spec.md:67`, `questions.md:27` and `plan.md:85`. The plan's line is where the error started (*the 0.12.2 framers — 1.48 and 1.64*). These are records, so correcting them is optional.

The protocol's framing row is not a carrier, because it states the band over
0.11.2–0.12.2 only.

### 🟡 3 — the per-call bound conflicts with §10's requirements read

`agents/framer.md:175-181` bounds one call at *about six reads or ranges*,
with no exception. Contract §10, which the bullet cites as the rule it
applies, says at `skills/agent-contract/SKILL.md:246`: *What has no excuse is
the requirements read, where every file the handoff names can be opened in
one call.* Give a framer a spawn prompt naming eight files, and the
definition says six while the contract says all eight in one call. The
section was meant to apply §10 without contradicting it. The anti-stall
grounds (#456's stall on an opening burst) concern the wide reading list of
the section above, not the handful of files a handoff names. The fix is to
carve the handoff's own files out of the bound. The smith may instead justify
the bound on the requirements read as well, with grounds.

### ⬜ 4 — "which `agents/framer.md` no longer does" says the definition once held reads back

`docs/review-handoff-protocol.md:633`, the framing row's Grounds. The
prohibition lived in spawn prompts and in no file (spec §Grounding; the
definition's own case says so). *No longer does* reads as if
`agents/framer.md` used to carry it. The behaviour and the numbers are right,
so this is ⬜. A proposed wording is fenced below.

### ⬜ 5 — the page says a segment that made no call is ungraded, and a smith's is counted exempt

`skills/verify/scripts/session_cost.py:2536`. The counts sentence lists *a
segment that made no call* among the rows *with no bar*. A no-call smith row
lands in `exempt`, because exemption is read from the kind, while a no-call
warden row is ungraded and still carries `bar` 1.8 in `--json`. The counts
are right; the sentence describing them is not.

### ⬜ 6 — `kind` in `--json`: two meanings, and the docstring's claim about telling exempt from unknown

The orchestrator asked whether a consumer can confuse `spawns.rows[*].kind`
(`head`, `tail` or `cycle`) with a segment row's `kind` (an agent basename).
I judge that one reading cannot. The two are on different objects, a program
reaches each by its path, and G3's note records the choice. The real
weakness is a different one. The segment `kind` is the agent's basename
(`warden`), while the page and the protocol call the kind `reviewing`. And
`bar` is null for an exempt kind and an unknown one alike. The docstring of
`segment_kind`, at `skills/verify/scripts/session_cost.py:2360`, says *a
program reading `--json` can do the same* (tell the two apart through
`SEGMENT_BARS`). A program that has only the JSON cannot: the table is in the
script, not the reading. Spec I7 fixed both keys' shape, so this is ⬜ and
the docstring is what to correct. A third key is the owner's call, not this
round's.

### ⬜ 7 — the cross-pin holds two named kinds, not the table

`tests/test_the_handoff_before_round_one.py:550` loops over a fixed pair. I
added a `scribe` entry with a bar to `SEGMENT_BARS`, with no protocol row,
and the case stayed green (executed, reverted). By reading, the same is true
of a protocol row added with no constant. The docstring says *either moving
alone turns it red*. That is true of a value moving and not of an entry
being added. Optional; the fence below makes the loop read both tables.

### Checked and clean

- **Resumed slices (read and executed).** Each slice is graded on its own numbers, and the label carries `N/of`. A small second slice can be named, which the small-round caveat covers.
- **Unknown `subagent_type` (executed).** It prints as ungraded and the JSON gives `bar` null (`scribe` in S8). `spawn_labels` guarantees a non-empty string or an absent field, so `rsplit` cannot meet a non-string.
- **Segment with no call (executed).** It is ungraded.
- **Pages without a grade (executed).** `--segments` gains only the block. Nothing above it and no number moves (S10's cases). The plain reading's `< 1.2` line and `--spawns` are unchanged.
- **The class, contract §12 (read, by search over README.md, README.ko.md, `skills/`, `docs/`, `templates/`, `agents/` and CONTRIBUTING.md).**
  - *Cannot tell kinds apart*: no other carrier.
  - *1.2 as a batching bar*: only the protocol's tying sentence and the script.
  - *The prohibition*: no carrier.
  - `docs/measuring-a-run.md` points at the protocol's section rather than restating a bar. `docs/the-agent-set.md` states no number.
  - `skills/verify/SKILL.md:647`'s *three segment kinds came to have bands* is history about how the bands arose, so it stays true.
- **Consistency with the warden's number (read).** The framer's 1.4 sits beside the warden's 1.89 and the protocol's 1.8 without contradicting either.

## Regression tests to plant

- `tests/test_session_cost.py`: a row printed at its bar meets it (🟡 1). Use 79 calls over 44 turns for the warden and 67 over 48 for the framer: no grade line, and `every graded row meets its kind's bar`. Seen red at c9d5114e by this round's probe. The case is fenced under 🟡 1.
- `tests/test_the_handoff_before_round_one.py`, the opening case: after 🟡 3's fix, assert that the handoff's own files are outside the bound, for example the phrase `whatever their number`.

## Facts for the evidence ledger

- G1's claim *exactly at the bar is meeting it* should read *a row printed at its bar meets it* once 🟡 1's fix lands. The anchor on `report_grades` will drift and must be re-read.
- P2's claim, the 1.46–1.79 band over 0.11.2–0.12.2, was opened against #370, #376, #385 and #456 by this round on 2026-10-01 and holds, counting framers that finished.

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

## Paste-ready fixes

### 🟡 1

`skills/verify/scripts/session_cost.py`, in `report_grades`:

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

`tests/test_session_cost.py`, beside the at-the-bar case:

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

And in `test_every_json_row_carries_its_kind_and_bar`, the comprehension that
computes `under`:

```python
        if row["bar"] is not None
        and round(row["numbers"]["tools_per_turn"], 2) < row["bar"]
```

### 🟡 2

`agents/framer.md`, the paragraph after the three bullets (re-wrap to 88):

```
Nothing here limits how many reads go out together below that bound. Every
framer that read 1.00–1.12 since 0.12.3 was a spawn whose prompt held its
opening reads back, and the framers of 0.12.1 and 0.12.2 that finished,
never told that, read 1.48–1.64.
```

The changelog fragment, line 4–5:

```
  framer reading since sat at 1.00–1.12 tools per turn; the
  0.12.1 and 0.12.2 framers that finished, never told, read 1.48–1.64. The
  rule was in no file, which
```

The test docstring in `tests/test_the_handoff_before_round_one.py`, line 293:

```
    burst; the 0.12.1 and 0.12.2 framers that finished, never told, read
    1.48-1.64. Writing that
```

### 🟡 3

`agents/framer.md`, the second bullet of §*How a frame opens*:

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

The opening case, after the `about six reads or ranges` assertion:

```python
    assert "whatever their number" in section, (
        "the bound reaches the files the handoff names, which §10 says go out "
        "in one call"
    )
```

### ⬜ 4

```
... every framer reading under the bar since 0.12.3, at 1.00–1.12, was a spawn whose prompt held its opening reads back, which `agents/framer.md` §*How a frame opens* now replaces with a bound on one call (#640) |
```

### ⬜ 5

```python
        "this ratio. A row with no bar — a kind not listed, a row no spawn\n  "
        "named — is ungraded, and so is a graded kind's segment that made no "
        "call."
```

### ⬜ 6

```python
    """A segment's kind and bar, as the two keys every segment row carries.

    `kind` is `""` where no spawn named the row, and `bar` is None for an
    exempt kind and for a kind the table does not know alike. The page tells
    those two apart through `SEGMENT_BARS`; a program holding only `--json`
    cannot, because the table is this script's and not the reading's."""
```

### ⬜ 7

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

Needs a fix: yes — 🟡 1 (a row printed at its bar is named under it), 🟡 2 (a
measurement attributed to the wrong release in a shipped definition and
changelog), 🟡 3 (the per-call bound contradicts §10's requirements read)
Loses a record or crashes: no

The broad gate has not come due: three 🟡 are open, so a fix pass and a
verifying round come before the sealer's spawn.

## Proof block

Files opened at c9d5114e in the clone:
- the work item's records: `spec.md`, `plan.md`, `questions.md`, `phases/phase-4.md`, `changelog.md`;
- the code and its documents: `skills/verify/scripts/session_cost.py` (lines 850–995, 1634–1860, 2018–2146, 2327–2730, 3036–3200), `agents/framer.md` (100–196), `docs/review-handoff-protocol.md` (the bars section by diff), `skills/verify/SKILL.md` (592–656), `docs/measuring-a-run.md` (1–30);
- the tests: `tests/test_session_cost.py`, `tests/test_the_handoff_before_round_one.py` and `tests/test_a_segment_feeds_the_flow_log.py` by diff;
- the ledger: `seal/releases/0.4.0.md` and `seal/releases/0.15.7.md` by word diff, the re-read notes of every other changed ledger by word diff, and `seal/ledger/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file.md`;
- the tracker: issues #370, #376, #385, #456, #478 and #548.
