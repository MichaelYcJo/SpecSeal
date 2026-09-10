# 1789034970 — review round 2, the verifying round

Target `b8aa637`, fix range `e972b5f..b8aa637` on
`docs/120-the-contract-is-settled-against-the-agents-that-exist`, draft pull
request 338. The surface is the fix diff and the units it created, not the
branch.

## The twelve closures, re-derived by reverting

Eight of the ten `fixed` rows name a document the fix changed and a case that
pins it. Each was re-derived the way round 1 re-derived the previous work
item's: the file was checked out at `e972b5f` alone in a fresh
`git clone --no-local`, the case the fix table names was run, and the
assertion it broke on was read. All eight went red, each on the assertion its
own fix wrote. None stayed green.

Two `fixed` rows have no revert to take, and each was settled another way.

**Finding 6** is a case rather than a document, so reverting it deletes the
thing under test. It was mutated instead. A fifth definition carrying the
marker turns it red naming both files — *2 definitions assign the broad gate
(['framer.md', 'sealer.md'])* — which is the arrival `questions.md` Q2 puts in
0.11.0, and the message tells that reader §2's sentence has to follow. Removing
§2's count sentence turns it red the other way. The case is closed.

**Finding 5** is fourteen ledger rows whose `Checked` moved to 2026-09-10, and
only opening the rows settles whether they were re-read or re-stamped. Eight
gained a `**Re-read 2026-09-10 … round 1's fix pass**` sentence. The other six
are the six the round named, and each already carried a
`Re-read 2026-09-10 in work item 1789034970 (#120).` sentence written by an
earlier phase of this branch — the note stood and the date column had not
followed it, which is exactly the defect the finding described. So the six are
dates catching up with a recorded read rather than dates asserting an
unrecorded one. One row in that group carries a 2026-09-10 note belonging to
work item 1789002694 rather than to #120, and its `Checked` was already
2026-09-10, so it makes no new claim. The claims themselves were spot-checked:
§3 still names the 28-minute case, and all four definitions still point at §7
and §8 rather than restating them. The commit message's *and a sentence saying
what was re-read* reads as if the fix pass wrote fourteen of them; it wrote
eight and inherited six.

Both `answered` rows hold. Finding 11 changed no assertion and added a rider
that `rider_check.py` reads at 26 ok. Finding 12's correction landed in
`spec.md:43` and `plan.md:151`, both now reading *a branch a worktree already
held*, and `overview.md:23` records the correction with its source.

## What this round opened

Four are worth a fix and four are corrections. Findings 1 through 3 come from
execution; the rest from reading, with the measurement each rests on named.

**🟡 1 — one of the four definitions passes the new bound case on a sentence
about something else.** `BOUNDS` is a vocabulary of four closing phrases and
the case asserts that every `agents/*.md` carries one. Three do, in sentences
whose subject is the file's own writes. The fourth entry,
`"you don't write them anywhere"`, is matched in `agents/scribe.md:26` by a
parenthetical whose subject is worker *findings*: *(Worker findings are
pre-verification by definition — that is why you don't write them anywhere
yourself.)* That sentence says verdicts are not the fact-finder's to record. It
is not a bound on a list of durable writes, and `agents/scribe.md` states no
such list anywhere.

Two mutations measure what that costs. Rewording the parenthetical alone —
leaving `agents/scribe.md` otherwise untouched and just as unbounded — turns
the case red, so today's pass rests on that sentence and nothing else. And a
fifth definition file carrying the parenthetical in unrelated prose, with no
list of writes and no bound, passes. The case was written for §6's new default,
where any loose sentence about producing something reads as a grant; on one of
the four files it covers, and on every file that arrives next, it is the loose
sentence.

**🟡 2 — the fix for finding 1 copied sixteen verbatim words out of the
contract into a second document, one word over the window this repository uses
to define a copy.** `skills/code-review/SKILL.md:154` now ends with *It
surfaced two work items later, when `git switch` refused a branch a worktree
already held.* That sentence was already in §7 at `e972b5f`; the fix pass wrote
it into the skill. Measured with the tree's own `longest_shared` against
`SECTIONS[7]`, the new paragraph shares a 16-word run with §7, where `WINDOW`
is 15 and `LONGEST_KEPT_APPLICATION` — the longest run the repository has
decided is still an application rather than a copy — is 10.

Nothing sees it. `tests/test_a_moved_rule_leaves_its_definition.py` globs
`agents/*.md`, and a skill a definition preloads reaches an agent exactly as
its definition does. The class, enumerated by running that module's own
measure over every file under `skills/`, is three pairs at or over the window
once the contract's own file is set aside: this one, and
`skills/implement/SKILL.md` against §5 at 30 words and against §9 at 15. Two of
the three predate the branch, which is why the fix below trims the paragraph
rather than widening the glob — widening it would go red on content this work
item did not write.

**🟡 3 — a terminal line that wraps is truncated into the record, and round 1's
record is already carrying the damage.** `round-1.md:12` reads
`| Needs a fix | yes — findings 1 through 8. Finding 1 is the one that reopens
the |`. The sentence ends there. `round-1-report.md:503` carries the same words
and line 504 continues *defect this work item was filed against.*
`terminal_value` at `skills/code-review/scripts/round_record.py:1225` matches
the label against one physical line and keeps that line's remainder, so
everything after the wrap is dropped without a refusal.

The two are not independent choices. `agents/warden.md:386` shows the terminal
lines in a fence with no note that they must not wrap, the prose around them is
hand-wrapped, and a `yes — <what>` long enough to be worth writing is long
enough to reach the margin. Every future round meets this, and the value the
next round inherits ends mid-clause.

**🟡 4 — the release case's docstring claims a shape and matches a
spelling.** `tests/test_broad_gate_rule.py:339` says it is asserted over the
glob *because a temporal release is the shape any definition can pick up*.
What it asserts is that the literal `until the rounds settle` is absent.
Replacing `agents/warden.md`'s corrected sentence with *§2 keeps the suite out
of your hands while the rounds are open, and it is yours once they have
settled* leaves the case green. The trade is the right one — no constant
decides when two sentences say the same thing — and finding 6's case states
exactly that trade in its own docstring. This one states the opposite of it.

**⬜ 5 — `round-1.md` still describes a branch whose fixes are committed.**
Lines 9 through 11 read `nobody — the fixes are not yet written` for
`Fixes checked by`, `Contract changes` and `New units`, and all twelve verdicts
still read `open`, at a SHA where the fix range is six commits back.
`round_record.py close` has not been applied. The consequence for this round is
concrete: the eleven units the fix pass created are named in no record's
`New units` row, so the surface a verifying round is told to judge as new is
invisible to the next reader. They are
`test_the_procedure_a_reviewer_follows_carries_the_leavings_rule_too`,
`read_at`, `COUNT_WORD`, `ASSIGNS_THE_GATE`,
`test_only_one_definition_assigns_the_broad_gate`,
`test_no_definition_promises_the_suite_once_the_rounds_settle`,
`test_the_reviewer_carries_the_gate_state_into_a_section_its_report_has`,
`BOUNDS`, `test_every_definition_bounds_what_it_writes`,
`test_the_leavings_rule_says_whose_leaving_it_is` and
`test_the_sealer_recites_the_four_acts_s6_actually_withholds`.

**⬜ 6 — `round-1-fixes.md:3` states the range as eight commits.**
`e972b5f..054c58f` holds six; `e972b5f..b8aa637`, which is the range this round
was given, holds seven.

**⬜ 7 — an item that was not run is routed into a table headed
`What was run`.** `agents/warden.md:240` sends the broad-gate state to
`## Executed probes`, and the destination is right: the generator parses that
heading and copies it into the record, which is how the state reaches a record
without the reviewer writing one. But the table's own columns are
`What was run | Result`, and the value the reviewer most often has is
`not yet`. §4 of the contract is about not letting what was executed and what
was not share a label. Nothing ships broken — the `Broad gate` cell is written
by `broad-gate --record` and never from this table — so this is a sentence
about how to spell the row, not a defect in the route.

**⬜ 8 — the count case's first failure message names the contract when the
constant is what moved.** Rewording §2's count sentence turns
`tests/test_broad_gate_rule.py:281` red with *§2 no longer states the count
this case checks, so the number and the sentence have come apart*. When the
framer lands in 0.11.0, three things move together — §2's prose, `COUNT_WORD`,
and the `["sealer.md"]` the second assertion compares against — and the first
assertion fires first, pointing at the document rather than at the two literals
in this file.

## The two disclosures, and what the tree can already see

Round 1 spawned two `Explore` subagents against §6's *spawn no agent*, and its
report disclosed neither. Whether anything in the tree should notice: it
already can. `skills/verify/scripts/session_cost.py` reads a segment's spawns
and the transcripts under the session's `subagents/` directory, and
`report_spawns` prints each one with its `subagent_type`. A warden segment
measured at its boundary — which is the standing rule for every segment — shows
the spawn rows on its face. So the gap is not a missing mechanism; it is that
nobody was reading that output for a rule rather than for a cost. I am not
proposing a new check: a case that could see this would have to read a
transcript, and a report field asking an agent to declare its own breach is the
weakest form of the thing `session_cost.py` already does from the outside.

This round spawned no agent and wrote no probe that commits.

The orchestrator's ruling on `bin/evidence-check` was taken as given and the
unscoped form was run. No broad-gate check was run, and none was ordered.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The new bound case passes on a sentence about worker findings, and a fifth definition passes free | `tests/test_every_agent_reads_the_contract.py:146` | open | The fourth `BOUNDS` entry is matched in `agents/scribe.md:26` by a parenthetical whose subject is verdicts, not writes; that file states no list of writes. Rewording the parenthetical alone turns the case red, and a new definition carrying it in unrelated prose passes |
| 2 | The fix wrote a 16-word verbatim run out of §7 into a second document, over the tree's own 15-word window | `skills/code-review/SKILL.md:154` | open | Measured with `longest_shared` against `SECTIONS[7]`: 16 words, `WINDOW` 15, `LONGEST_KEPT_APPLICATION` 10. The sentence was in §7 at `e972b5f`. The guard globs `agents/*.md`, so no skill is held to it |
| 3 | A wrapped terminal line loses everything after the wrap, and round 1's record is already truncated | `skills/code-review/scripts/round_record.py:1225` | open | `round-1.md:12` ends at *the one that reopens the*; `round-1-report.md:503-504` continues *defect this work item was filed against*. `terminal_value` matches one physical line and refuses nothing |
| 4 | The release case's docstring claims it catches the shape; it matches one spelling | `tests/test_broad_gate_rule.py:339` | open | A definition reworded to *yours once they have settled* leaves it green. Finding 6's case states this same trade in its docstring; this one states the opposite |
| 5 | `round-1.md` still reads *the fixes are not yet written* in three cells with twelve verdicts open | `seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/rounds/round-1.md:9` | open | `close` has not been applied at `b8aa637`. The eleven units the fix pass created reach no `New units` row, so the surface this round judges as new is invisible to the next reader |
| 6 | The fix table states its range as eight commits | `seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/rounds/round-1-fixes.md:3` | open | `e972b5f..054c58f` holds six; the range this round was given, `e972b5f..b8aa637`, holds seven |
| 7 | The broad-gate state is routed into a table whose column reads `What was run` | `agents/warden.md:240` | open | The destination is one the generator parses and copies, which is the point of the fix. The usual value is `not yet`, and §4 is about not letting run and not-run share a label. The `Broad gate` cell is written elsewhere, so nothing ships broken |
| 8 | The count case's first failure message points at §2 when two literals in the case are what moved | `tests/test_broad_gate_rule.py:281` | open | Rewording §2's sentence reports *the number and the sentence have come apart*. At 0.11.0 the framer moves §2's prose, `COUNT_WORD` and the `["sealer.md"]` comparison together, and the first assertion masks the other two |

## Executed probes

| What was run | Result |
|---|---|
| Baseline: the eight closure cases at `b8aa637` in a fresh `git clone --no-local` | exit 0, 11 passed |
| Finding 1's fix reverted alone (`skills/code-review/SKILL.md` at `e972b5f`) | exit 1 — *the Probes row states deleting the named file as the whole obligation again* |
| Finding 2's fix reverted alone (`agents/warden.md` at `e972b5f`) | exit 1 — *warden.md promises the suite once the rounds settle* |
| Finding 3's fix reverted alone (same file, its own case) | exit 1 — *the reviewer is told to write the state into a record again* |
| Finding 4's fix reverted alone (`agents/smith.md` at `e972b5f`) | exit 1 — *agents/smith.md never says where its list of durable writes stops*, red on that file alone |
| Finding 7's fix reverted alone (`skills/agent-contract/SKILL.md` at `e972b5f`) | exit 1 — *§7 lost the ownership clause* |
| Finding 8's fix reverted alone (`templates/sdd-routing.md` at `e972b5f`) | exit 1 — *the criterion names no destination for discovery* |
| Finding 9's fix reverted alone (`agents/warden.md` at `e972b5f`) | exit 1 — *the bullet's title still calls them §6's instances* |
| Finding 10's fix reverted alone (`agents/sealer.md` at `e972b5f`) | exit 1 — *the sealer's recitation of §6 drops `post`* |
| Finding 6 mutated: a fifth definition file carrying the gate marker | exit 1 — *2 definitions assign the broad gate (['framer.md', 'sealer.md'])* |
| Finding 6 mutated: §2's count sentence reworded to *Two definitions* | exit 1 — *§2 no longer states the count this case checks* |
| Finding 4's case with `agents/scribe.md`'s parenthetical reworded and nothing else changed | exit 1 — the pass rests on a sentence about worker findings |
| Finding 4's case with a fifth definition carrying that parenthetical in unrelated prose and no bound | exit 0 — a new definition passes without one |
| Finding 2's case with `agents/warden.md` reworded to *yours once they have settled* | exit 0 — the literal is what it matches |
| `longest_shared` over every `skills/**/*.md` against every contract section, the contract's own file aside | three pairs at or over `WINDOW` 15: `skills/code-review/SKILL.md` §7 at 16, `skills/implement/SKILL.md` §5 at 30 and §9 at 15 |
| The fourteen re-dated ledger rows, `Checked` column and note read per row across `e972b5f..b8aa637` | eight gained a fix-pass re-read sentence; six already carried one from an earlier phase of this branch |
| Paste-ready fix 1 applied in the clone: the vocabulary entry replaced and the bound added to `agents/scribe.md` | red with the entry replaced and no bound, green with the bound, red again with the bound removed |
| Paste-ready fix 2 applied in the clone: the copied sentence trimmed | longest run shared with §7 falls 16 → 10, under `WINDOW`; `tests/test_a_probe_that_commits_says_so.py` stays green, 7 passed |
| `bin/evidence-check .` at `b8aa637` | exit 0 |
| `.github/scripts/rider_check.py` at `b8aa637` | exit 0 — 26 ok · 0 drifted · 0 broken |
| The broad gate | not yet. Unverified, and the sealer's — no full suite, repository-wide lint or typecheck was run in this round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the duplication guard should reach the skills a definition preloads | Two of the three pairs over the window predate this branch, so widening the glob is a sweep and not this work item's | The owner, at the release that takes the sweep |
| Whether §2's naming survives the framer | Still `questions.md` Q2's, unchanged by this round; finding 8 above only asks that the case say which literals move with it | The owner, at 0.11.0 |

## Paste-ready fixes

Finding 1 — in `tests/test_every_agent_reads_the_contract.py`, replace the
fourth entry:

```python
BOUNDS = (
    "a write not below is a write you do not make",
    "a write not named here is a write you do not make",
    "is the whole of what you may write",
    "You write nothing durable anywhere, and that is the whole of it",
)
```

and in `agents/scribe.md`, reword the parenthetical so it says what it means
and add the bound the file has never had, after the paragraph that ends
*...that is why they are not yours to record anywhere.)*:

```
You write nothing durable anywhere, and that is the whole of it: the report you
return is your caller's to act on, and a probe file is deleted before you hand
over.
```

Finding 2 — in `skills/code-review/SKILL.md`, replace the paragraph's last
sentence so the incident stays a pointer:

```
**The file is not the whole of it.** Contract §7 is about leavings, not files:
a worktree, a branch, a checkout, a scratch clone or a virtual environment your
probe made for itself is a leaving too, and the probe is not over until every
one of them is gone. Deleting the named file and stopping there is what left a
git worktree behind through a whole review chain — the report said the probe
files were deleted, and there was nothing wrong with that sentence. §7 carries
the incident that cost this rule.
```

Finding 3 — in `skills/code-review/scripts/round_record.py`, read the label's
value across the wrap, stopping at a blank line or at the other terminal
label:

```python
def terminal_value(reader, lines, label):
    """What stands after the colon in the report's `<label>: …` line.

    A wrapped line is one value. `agents/warden.md` shows the two terminal
    lines in a fence and says nothing about wrapping, and the prose around
    them is hand-wrapped, so a `yes — <what>` worth writing is long enough to
    reach the margin. Reading the physical line alone truncated round 1 of
    #120 mid-clause, and the record shipped that way.
    """
    pattern = re.compile(r"^\s*" + re.escape(label) + r"\s*:\s*(.*?)\s*$")
    others = tuple(
        re.compile(r"^\s*" + re.escape(other) + r"\s*:")
        for other in TERMINAL_LINES
    )
    found = []
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        parts = [match.group(1)]
        for following in lines[index + 1 :]:
            if not following.strip() or any(o.match(following) for o in others):
                break
            parts.append(following.strip())
        found.append(" ".join(part for part in parts if part))
    if len(found) != 1:
        raise Refused(
            f"the report has {len(found)} `{label}:` lines and the record "
            "needs exactly one — the row is copied from what stands after "
            "the colon"
        )
    value = reader.visible(found[0])
    word, _ = chain.yes_or_no(value)
    if word is None:
        raise Refused(
            f"`{label}: {value}` is not `{chain.FLOOR_NO}` or "
            f"`{chain.FLOOR_YES} {DASH} <what>`, which is the vocabulary the "
            "checker reads the row in"
        )
    return value
```

This changes what a person reads in the record, so it owes a case: a report
whose terminal line wraps produces the whole sentence in the cell, and the
same report with the wrap removed produces the same cell.

Finding 4 — in `tests/test_broad_gate_rule.py`, add to
`test_no_definition_promises_the_suite_once_the_rounds_settle`'s docstring:

```
    **The direction this can still miss, stated rather than left to be
    found.** It matches one spelling. A definition that promises the suite in
    other words -- *yours once the rounds have settled* -- is invisible here,
    the same verbatim-versus-semantic trade
    `test_only_one_definition_assigns_the_broad_gate` states, for the same
    reason: no constant decides when two sentences say the same thing. What
    narrows it is that the wrong sentence had one idiom in this tree and the
    glob is what catches it arriving in a second file.
```

Needs a fix: yes — findings 1 and 3; findings 2 and 4 can be answered with grounds, and 5 through 8 are corrections.
Loses a record or crashes: no

Both lines above are one physical line each on purpose. Finding 3 is why.

## Proof

Read in the repository under review: `seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/` — `rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-1-fixes.md`, `rounds/round-1-asked.md`, `spec.md`, `plan.md`, `changelog.md`, `overview.md`. In a `git clone --no-local` at `b8aa637`: `skills/agent-contract/SKILL.md`, `skills/code-review/SKILL.md`, `skills/code-review/orchestration.md`, `skills/code-review/scripts/round_record.py`, `skills/evidence-check/scripts/evidence_check.py`, `skills/verify/scripts/session_cost.py`, `agents/warden.md`, `agents/smith.md`, `agents/sealer.md`, `agents/scribe.md`, `templates/sdd-routing.md`, `seal/ledger.md`, `seal/ledger/1789034970-the-contract-is-settled-against-the-agents-that-exist.md`, `ruff.toml`, `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_a_probe_that_commits_says_so.py`, `tests/test_broad_gate_rule.py`, `tests/test_every_agent_reads_the_contract.py`, `tests/test_the_agent_contract_holds_the_universal_rules.py`, `tests/test_the_reviewers_report_reaches_the_record.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_waiver_decided_at_start.py`, `tests/test_docs_line_wrap.py`. Three `test_tmp_*` driver scripts were written outside the clone, run, and deleted; the clone is clean at `b8aa637` and holds nothing this round added.
