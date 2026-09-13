# Round 1 — a segment's own wall clock is in no column (#350, #343)

**Target SHA** `0436688c818b1ba4a5b9a255937cb73b9aa710d8`
**Base** `c7cc842b937ca36a28adfcb7e436bb9c4bece995` (`origin/release/v0.11.3`)
**Diff** `git diff c7cc842...HEAD` — 20 files, 2544 insertions, 31 deletions
**Draft pull request** #380

**Contract §6 — this round spawned no agent.** Every read, probe and run below
was taken in this session. Nothing was delegated.

**Contract §2 and §3 — the broad gate was not run and was not asked for.** The
full suite, the repository-wide lint and the typecheck are the sealer's, after
the rounds settle. What ran is four modules, one checker and four probes, each
named in the probes table.

Round 1: there is no earlier `round-N.md` in this work item's directory, so
nothing was inherited. The implementer's account — the pull request body,
`overview.md`, the phase records — was read in full and then checked against
the code. Where it is confirmed below, it is confirmed by measurement rather
than adopted.

---

## What the account claimed, and what I found when I went looking

The five headline claims were opened. Four of them hold, one is wrong in a way
that matters, and the wrong one is a number rather than the argument built on
it.

**The harness fact holds, and it is larger than stated.** I measured the
`Agent` call's own tool_use-to-tool_result interval against the same segment's
own transcript span, over every spawn the join names on this machine. The
spawn interval is a median of 2.3 seconds (n=302, 0.4 s to 26.3 s); the
segment those spawns name runs for a median of 715 seconds. So `delegated`
reads two seconds for an agent that worked twelve minutes, the result is
written on acceptance, and the whole premise of the mode is confirmed by
execution rather than by reading.

**The tolerance re-measurement reproduces exactly.** The account reports
296/349 named at 1.0 s and 301 at 2.0 s against 305 spawns. My re-measurement
today reads 302/355 at 1.0 s and 307 at 2.0 s against 311 spawns — the
population grew by six transcripts because this work item's own sessions
wrote them. Every delta the argument rests on is identical: two seconds buys
five segments in both readings, 44 transcripts are structural in both
(355−311 = 44, 349−305 = 44), and nine nameable segments are missed at 1.0 s
in both. The arithmetic is right and the conclusion follows from it.

**The flat-directory correction holds.** Zero files below depth one, across
all 355 transcripts. The frame's picture of an unnamable segment as a nested
one is dead, and the code never depended on it — `join_segments` infers
unnamed from the match failing, never from the path.

**#343's empirical claim holds, and I checked what a finding is before
trusting the count.** A finding is a segment row whose own transcript holds an
`Agent` call, which prints the `§6 — an agent spawned another agent` header. I
ran the mode over all 43 runs with a `subagents/` directory: exit 0 on every
one, and 13 carry the line. Twelve of the thirteen name a `specseal:warden` or
a `specseal:smith` — 40 `Agent` calls by wardens, 4 by smiths. The claim is
not hypothetical. The thirteenth is finding 3 below.

**The two mutation survivors are genuinely covered.** I re-applied both
mutations in a scratch copy of the tree and ran the case that is supposed to
catch each. Both cases pass against the unmutated copy and both go red under
their mutation, so contract §15 is satisfied for them — established by
execution, not by the hand-back saying so.

**What does not hold: the median.** See finding 2.

---

## My own verdict on `seal/ledger.md`

The account asks for a second opinion and names the sibling branch's answer. I
did not read that round and did not inherit it.

**Touching `seal/ledger.md` here is correct.** The rule in `CLAUDE.md` forbids
*appending* to the shared file and carves out a removal; a hash re-stamp is
neither. The rule's stated purpose is to stop a release-time conflict after
the broad gate has run, and a re-stamp is the smallest edit that avoids a
worse outcome: `evidence_check.py` returns 1 on any drifted row, the hygiene
workflow runs it, so leaving the seven rows drifted turns the check red for
every branch rather than for this one. I ran the checker on this branch and it
reads 1158 ok · 0 drifted · 0 broken, exit 0.

**What is wrong is not the file that was touched, it is the column that was
not.** Findings 5 and 6 carry it.

---

## Findings

### 🟡 1 — `unnamed` counts slices where every sentence around it counts files

`skills/verify/scripts/session_cost.py#measure_segments`, the return dict:

```python
"unnamed": sum(1 for row in rows if not row["named"]),
```

`rows` are slices. A resumed file is several rows, so an unnamable file that
was resumed is counted once per stretch of work. That is the exact failure
`segment_slices` gives every slice the file's name to avoid — its own
docstring says *the unnamed count, which is a reading about the harness, would
climb with every resume* — undone one function later. The line six lines below
it in `report_segments` de-duplicates by transcript for the resumed count, so
the pattern was known and this one instance missed it.

**Two things a reader sees.** The header prints *N segment transcripts beside
this one* against *M segments named by nobody* in two different units, and M
can exceed the number of files. And `report_breaches` reconciles the §6 count
against `unnamed`, so a run whose counts genuinely agree prints that they do
not — sending a reader to look for a child transcript that was never missing.

**Established by execution, twice.** On a fixture with one named segment and
one unnamable file resumed into two slices, the mode reads `unnamed=2` for one
unnamable file and prints *2 segments named by nobody* under *2 segment
transcripts beside this one*. With one `Agent` call added inside the named
segment, it prints *1 `Agent` call inside a segment, against 2 segments the
parent could not name, and the two do not agree* — where the truth is one call
and one unnamable file, agreeing.

**And it is already happening.** I compared the mode's own `unnamed` against
the number of distinct unnamable transcripts over all 43 real runs on this
machine: one run reads `unnamed=3` for two unnamable files today.

Enumerating the class, since the defect is a count taken at the wrong grain:
`transcripts` is files, `spawns` is calls, `unclaimed` is spawns, the resumed
count de-duplicates by transcript, and `idle_gap_s` is genuinely per row.
`unnamed` is the only member that takes the wrong grain.

### 🟡 2 — the published median is the mean, and it is wrong by 40%

Three new locations assert that a spawned agent *runs for a median of about
1,000 seconds*: the module header of
`skills/verify/scripts/session_cost.py` (:39–40), the
`#measure_segments` docstring (:1122–1125), and — where it reaches a reader
outside the code — `changelog.md:10`, as *a median of about a thousand*.

Measured with the instrument this work item builds, over every segment row of
all 43 runs: the median span is **715 seconds** for named rows and 661 for all
rows. The **mean** is 1,020. So 1,000 is the mean wearing the word median.

The figure is inherited — it comes from #145 and still stands at
`#spawn_cycles` (:691) and in that work item's records, which stay as written.
What this branch did was carry it into three new places, one of them a release
note, while the one instrument able to check it was being built in the same
diff. Contract §5 is the rule: an aggregate is not a coordinate, the number
can be checked while the claim cannot. The discipline was applied to the other
inherited aggregate in this diff — the tolerance was re-measured for Q3 — and
not to this one.

The direction of the argument is untouched: 715 seconds against a 2.3-second
`delegated` is still three hundredfold. This is a wrong statistic name on a
published figure, which is the class `#analyse`'s own docstring spends a
paragraph on (#200, #202) and the class `report_segments` prints a comparable-
from line about.

**Established by execution.**

### 🟡 3 — the §6 line cites the contract at agents the contract does not bind

`skills/verify/scripts/session_cost.py#report_breaches` prints §6 at any agent
whose transcript holds an `Agent` call. §6 binds the agents this plugin
spawns; it does not govern an agent from somewhere else, and one such agent's
own procedure instructs it to fan out.

**Established by execution.** Of the 13 runs carrying the line, one names
`claude-preset:code-reviewer`, which no definition in this repository governs
and whose own review procedure tells it to run finder angles through the Agent
tool. The line reports it as a §6 breach.

The count #343's argument rests on survives — twelve of thirteen are
`specseal:*` agents. What does not survive is the line's precision, and a line
that cries a rule at an agent the rule does not reach is one a reader learns
to discount. The report already prints what it cannot tell; this is one more
thing it cannot tell, and saying so costs three lines.

### 🟡 4 — two coordinator messages in a row invent a slice the agent never worked

`#segment_slices` builds one row per window, including a window with no call
in it. Two coordinator messages arriving before the agent acts produce an
empty window between them.

**Established by execution** on a fixture: a file with two stretches of work
and two adjacent markers prints three rows —

```
  specseal:smith  1/3               0.0m      1    1.00     0s             0
  specseal:smith  2/3                           no paired call             —
  specseal:smith  3/3               0.0m      1    1.00     0s             —
```

The agent worked twice and the table says three, the second stretch is labelled
`3/3`, and the `no paired call` row means something different here from what
`#measure_segments`' docstring introduced it for — a whole transcript that read
and thought and called nothing, which spent tokens, against a slice that spent
none.

**Honest about the reach**: I checked all 43 real runs on this machine and
found zero call-less slices. This is reachable and not observed. It is ranked
last for that reason, and it is 🟡 rather than ⬜ because the mode's whole value
is that a reader can trust its counts without opening the file.

### ⬜ 5 — seven ledger rows were re-stamped and the `Checked` column was not

`seal/ledger.md`, seven rows anchored on
`skills/verify/SKILL.md#"## Measure the segment, and feed the flow log"`, hash
`b1d57f7c` → `7837c909`. Six keep `Checked` at 2026-09-09 and one at
2026-09-12. The branch rewrote that section on 2026-09-13.

`CLAUDE.md` states the rule: *re-verifying is re-reading and then running
`evidence-check --reverify`*. The pull request body says the seven rows were
re-read. If that happened, the column is where it is recorded, and it is not
recorded.

The repository already knows this failure by name. `#reverify` carries a
RIDER: *this rewrites the hash and never the `Checked` column, so the claim
that somebody re-read the code is made by a person and recorded by nobody.
Round 1 of #120 measured the gap: six rows of `seal/ledger.md` got new hashes
on one branch and all six kept dates from before the content moved — one of
them anchored on the very section that branch rewrote.* That is this branch,
with seven rows instead of six.

**Established by execution** (the diff, cell by cell) **and by reading**
(the RIDER). ⬜ because the location is the run's paperwork rather than the
tool; it is out of `Needs a fix` for that reason and not because it is small.

### ⬜ 6 — the seven rows are anchored one altitude too high

Same coordinate. The anchor is a whole heading path over a long section, so
an edit to any paragraph in it drifts every row anchored there. Two of the
seven make claims about paragraphs this branch never touched: F5 is about
which tracker states the shipped skill may name, and R3 is about the
run-level table. Both drifted anyway.

`CLAUDE.md` provides the narrowing — `path#major>minor@hash` *where a claim
needs narrowing* — and a minor anchor would have left those rows alone. This
is the class this repository's own memory already carries from 0.11.2 as *the
pinning case whose unit was one altitude too high*.

Re-anchoring seven rows is outside what this diff is about. It belongs in
`evidence-todo.md` or an issue, not in the fix pass. **Established by
reading.**

### ⬜ 7 — every segment file is read for tokens twice on any `--json` run

`#segment_slices` calls `token_totals([transcript])` per file, and `main` then
calls `token_totals([path, *subagent_transcripts(path)])` over the whole tree.
Together with `#opening_stamp`, `#load` and `#resume_cuts`, a `--json` reading
now opens each segment transcript five times, two of them for the same token
figure.

The comment above the `spawns` computation measured its cost before putting it
behind `--json` (25.5 ms against `analyse`'s 42.6 ms). The comment above
`segments` says *computed on the same terms* without measuring, and the terms
are not the same: `measure_cycles` is arithmetic on a list already in memory,
`measure_segments` is file input over the whole tree. **Established by
reading.** No behavioural defect; the plain report is untouched, which the
cases pin.

### ⬜ 8 — `overview.md` records 98 where the module is 100

`overview.md`, the proof block: `bin/test tests/test_session_cost.py -q` (98).
I ran it: 100. The pull request body says 100. The record is stale against
its own pull request.

### ⬜ 9 — two frame corrections, two different treatments, and no reason given

The naming divergence was corrected in `plan.md` in place, with the proposed
name kept behind a marker in `phases/phase-1.md`. The nested-transcript model
the measurement killed was not corrected in `spec.md`, which still carries it
in the Scope prose (:11, :111), in the acceptance table's third Given (:132)
and in the fixture row (:155), and in `plan.md` (:20, :41, :100).

Leaving `spec.md` alone is defensible — records hold what was true when they
were written, which is the boundary `test_one_word_one_meaning.py` draws for
its own sweep — and on that reading the corrected `plan.md` is the anomaly. I
am not asking for either to move. What is missing is one sentence in the
divergence table saying which convention was applied and why the two
divergences got different treatments, because the next reader meets both in
one file.

**On whether any of the three should have been a hand-back rather than a
divergence row: no.** I checked what each correction changes about what gets
built. The flat-directory finding changes why the fixture is shaped as it is
and not the fixture — `#subagent_transcripts` walks rather than lists, so both
shapes stay covered, and the nested case still ships. Q2 and Q3 were framed as
measurements to be taken inside the work, at the top of the phase that needs
them, which is what `questions.md` says they are. None of the three moved an
acceptance criterion or a scope boundary. A divergence row is the right
instrument for all three.

---

## What I checked and found clean

- **The fixtures against `tests/test_no_real_identifiers.py`.** I read every
  new fixture string myself rather than trusting the run. The transcript
  fixtures carry `./bin/test tests/test_x.py -q`, `ruff check .`,
  `cat docs/spec.md`, `git commit -m x`, `agent-smith.jsonl`,
  `inner/agent-deep.jsonl`. No host, no user path, no organisation name. The
  module passes, and it passes for the right reason.
- **Both directions in `tests/test_one_word_one_meaning.py`.** The pinned
  phrasing is asserted in the owner file and both loose spellings are asserted
  absent across the three swept files. That is the module's established shape,
  and the absence half is present. The sweep is a three-file tuple rather than
  a glob, which matches how the `seal` word is swept in the same module — the
  scope is the files that carried the loose sentence, and the case name reads
  wider than that. Not raised as a finding: the module's own convention is the
  tuple, and changing it is a sweep of its own.
- **Both READMEs moved together.** One row each, same position in the same
  cheat-sheet table, equivalent content, and the Korean edition is not a
  transliteration of the English one.
- **No existing printed line moved.** The plain report and `--spawns` are
  pinned byte-adjacent by a case that names both, and the `--json` key
  exclusion list caught the new key on the commit that added it.
- **`evidence_check.py .`** — 1158 ok · 0 drifted · 0 broken · 0 external ·
  0 old-format, exit 0, plus the record arm reading this work item.
- **Exit 0 is honest.** The mode exits 0 on all 43 real runs including the 13
  carrying a finding, which is what `spec.md` argues for and what the case
  pins.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `unnamed` is summed over slices, not transcripts, so a resumed unnamable file is counted once per stretch — the header mixes units and the §6 reconciliation prints a false disagreement | `skills/verify/scripts/session_cost.py#measure_segments` | open | Executed. Two fixtures reproduce both symptoms; one of the 43 real runs on this machine already reads `unnamed=3` for two unnamable files. Contradicts `#segment_slices`' own docstring, and the resumed count six lines away de-duplicates correctly |
| 2 | 🟡 *a median of about 1,000 seconds* is the mean; the measured median is 715 s for named rows, 661 s for all rows. Carried into three new places, one of them the release note | `skills/verify/scripts/session_cost.py` :39–40 and `#measure_segments`; `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/changelog.md:10` | open | Executed with the mode itself over every segment row of all 43 runs: median 715 s, mean 1020 s. An inherited aggregate (#145) propagated without re-derivation — contract §5 — while the other inherited aggregate in the same diff was re-measured |
| 3 | 🟡 the §6 line cites the contract at agents the contract does not bind | `skills/verify/scripts/session_cost.py#report_breaches` | open | Executed. 1 of the 13 runs carrying the line names `claude-preset:code-reviewer`, which no definition here governs and whose own procedure instructs the fan-out |
| 4 | 🟡 two adjacent coordinator messages produce a call-less slice, inflating the `N/of` denominator and re-using `no paired call` for a second meaning | `skills/verify/scripts/session_cost.py#segment_slices` | open | Executed on a fixture. Reachable and not observed: zero call-less slices across all 43 real runs |
| 5 | ⬜ seven `seal/ledger.md` rows re-stamped `b1d57f7c` → `7837c909` with `Checked` left at 2026-09-09 and 2026-09-12, for a section this branch rewrote on 2026-09-13 | `seal/ledger.md` | open | Executed on the diff cell by cell, and read against `#reverify`'s RIDER, which names this exact failure from round 1 of #120 — six rows then, seven now |
| 6 | ⬜ those seven rows are anchored on a whole heading path, so rows about untouched paragraphs (F5, R3) drift with any edit to the section | `seal/ledger.md` | open | Read. `CLAUDE.md` provides `path#major>minor@hash` for narrowing; belongs in `evidence-todo.md` rather than this fix pass |
| 7 | ⬜ every segment transcript is read five times on a `--json` run, twice for the same token figure | `skills/verify/scripts/session_cost.py#segment_slices`, `#main` | open | Read. The parallel comment for `spawns` measured its cost before admitting it to `--json`; this one asserts the same terms without measuring, and the terms differ — arithmetic in memory against file input over a tree |
| 8 | ⬜ the proof block records 98 for `tests/test_session_cost.py`; the module is 100, which is what the pull request body says | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md` | open | Executed — the module alone reads `100 passed` |
| 9 | ⬜ the naming divergence was corrected in `plan.md` in place and the nested-transcript model was left standing in `spec.md`; the divergence table does not say which convention applies | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md`, `spec.md` :132 | open | Read. Both treatments are defensible; a reader meeting them in one table cannot tell which rule produced which |

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

One note on how the probes were taken, since §7 asks for it: one probe file,
written in the scratchpad, re-written and re-run four times as each question
opened the next, and deleted before this report was written. It left no
worktree, no branch, no clone and no virtual environment. The scratch copy
used for the mutation re-check was a temporary directory that deleted itself.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `survivor-check` has no cheat-sheet row in either README | `overview.md` §Not done | the repository owner. Correctly deferred — it is a different command, and the reviewer agrees it does not belong in this diff |
| The §6 line becoming an exit code rather than a line | `overview.md` §Not done | a later work item, choosing against the 13 readings that now exist |
| `delegated_s` keeping the meaning it was published with | #145 `questions.md` §Q4, and Q1 here, answered 2026-09-13 | the repository owner, who may revisit it now a per-segment reading exists |
| A per-slice token column | `overview.md`, divergence table row 3 | deferred by design — re-deriving it duplicates `#token_totals`' #202 rule |
| Finding 6 — re-anchoring the seven ledger rows one altitude down | not yet placed | the orchestrator, to route to `evidence-todo.md` or an issue rather than to this fix pass |

## ❓ out of verified scope

| Question | Who answers it |
|---|---|
| The full suite, the repository-wide lint and the typecheck. Not run, not asked for, and not this round's to run | the sealer |
| Every harness fact here was measured on one machine's harness — the one-second opening, the flat directory, the literal marker sentence. My re-measurement is the same machine, so it confirms the arithmetic and not the portability | the repository owner, as the hand-back already states |
| Whether `#DELEGATING`'s published range *1.5–3.7 seconds across 67 spawns* should be re-stamped. It is pre-existing and outside the diff; over 302 spawns today it reads 0.4–26.3 s, median 2.3 s. Not raised as a finding for that reason | the repository owner — a ledger fact rather than a fix |

## Paste-ready fixes

**Finding 1** — `#measure_segments`, the return dict. Replace:

```python
        "unnamed": sum(1 for row in rows if not row["named"]),
```

with:

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

and plant the case, in `tests/test_session_cost.py` beside
`test_a_later_slice_inherits_the_name_from_the_files_first`:

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

**Finding 2** — three locations. In `skills/verify/scripts/session_cost.py`,
the module header, replace:

```
agent runs for a median of about 1,000 (#350). That number is in the segment's
```

with:

```
agent goes on working for a median of about 700 seconds (#350). That number is
in the segment's
```

and in `#measure_segments`' docstring, replace:

```
    when the spawn is ACCEPTED; the agent then runs for a median of about
    1,000 seconds, and that interval is in none of `--spawns`' columns, in
    any row. It is in the segment's own file, and this opens it.
```

with:

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

and in `changelog.md`, replace:

```
  seconds while the agent goes on working for a median of about a thousand.
```

with:

```
  seconds while the agent goes on working for a median of about seven hundred.
```

**Finding 3** — `#report_breaches`, after the existing §6 paragraph, add a
second `print`:

```python
        print(
            "\n  §6 binds the agents this plugin spawns. A row above naming "
            "an agent from\n  somewhere else is still a spawn made inside a "
            "segment and still worth seeing,\n  but which rule it answers to "
            "is that agent's own definition's to say."
        )
```

and pin it, beside `test_a_clean_run_prints_no_such_line`:

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

**Finding 4** — `#segment_slices`, the sliced branch. Replace:

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

with:

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

and, in the same dict, replace:

```python
                "tokens": token_totals([transcript]) if index == 0 else None,
```

with:

```python
                # The first KEPT slice, not window 0, which may have been
                # dropped as empty. The figure is the file's and rides one row.
                "tokens": token_totals([transcript]) if position == 0 else None,
```

and plant:

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

**Finding 5** — `seal/ledger.md`. Set `Checked` to `2026-09-13` on the seven
rows whose anchor moved to `@7837c909`: F5, R3, G5, and the four unlettered
rows beginning *The orchestrator's boundary is stated…*, *Assigning a call by
its start…*, *The between-the-rows refusal…* and *A case that asserts a
document clause…*. If any of the seven was re-stamped without the section
actually being re-read, re-read it first — the date is the record that
somebody did, and the fix is the reading, not the cell.

**Finding 8** — `overview.md`, the proof block: `(98)` → `(100)`.

**Finding 9** — `overview.md`, the divergence table. Add to the Grounds cell
of the *What makes a segment unnamable* row:

```
`spec.md` is left as written, because a frame document records what was true
when it was framed; `plan.md` was corrected in place for the naming divergence
because a plan is a build instruction and a name that is not in the tree sends
the next reader to a symbol that does not exist. The two divergences got
different treatments on purpose, and this sentence is why.
```

Needs a fix: yes — findings 1, 2, 3 and 4.
Loses a record or crashes: no

Nothing here leaves the root or crashes. The mode exits 0 on all 43 real runs
and on every fixture, the four changed modules are green, and no code path
found writes or drops a record. Findings 1 and 4 are counts a reader trusts,
finding 2 is a published figure carrying the wrong statistic's name, and
finding 3 is a rule cited at an agent it does not reach. Each degrades a
reading; none of them loses one.

---

## Proof block

📋 code-review applied
· read: `skills/verify/scripts/session_cost.py` (whole file),
  `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*,
  `tests/test_session_cost.py` (the diff and the fixture builders),
  `tests/test_one_word_one_meaning.py`, `tests/test_a_segment_feeds_the_flow_log.py`,
  `README.md` and `README.ko.md` (the changed rows), `seal/ledger.md` (the
  changed rows), `seal/ledger/1789296300-a-segments-own-wall-clock-is-in-no-column.md`,
  and this work item's `spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `changelog.md`, `routing.md`, `phases/phase-1.md`; plus
  `skills/evidence-check/scripts/evidence_check.py#reverify` and its exit path,
  `docs/review-handoff-protocol.md` §*After the run — the per-segment bars*,
  `tests/test_docs_line_wrap.py`, `CLAUDE.md`, and pull request #380's body
· executed: the four modules (149 passed), `evidence_check.py .` (exit 0), and
  four probe runs from one scratchpad file, deleted before this report
· unverified: the full suite, the repository-wide lint and the typecheck — the
  sealer's, after the rounds settle; and portability to a second harness — the
  repository owner's
· spawned: nothing (contract §6)
