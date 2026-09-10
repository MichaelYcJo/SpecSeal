# 1789034970-the-contract-is-settled-against-the-agents-that-exist — review round 2

| Field | Value |
|---|---|
| Target SHA | b8aa637 |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 338 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1 and 3; findings 2 and 4 can be answered with grounds, and 5 through 8 are corrections. |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of #120 at `b8aa637`, the verifying round, on `docs/120-the-contract-is-settled-against-the-agents-that-exist` against `release/v0.10.0` (`d35c874`), draft pull request #338. The fix range is `e972b5f..b8aa637`, seven commits, 21 files (+494 / −44), closing round 1's twelve findings — the fix pass reports ten `fixed` and two `answered`. The round's first job was the twelve closures, and re-deriving them meant reverting rather than reading: revert each fix alone, run the case the fix pass says pins it, and name the assertion it breaks on, because a closure whose case stays green with the fix reverted is not closed. The class to enumerate was the surface the fixes created rather than the surface round 1 read — six new or changed cases landed, two of them driven off globs (`BOUNDS` over `agents/*.md`, and the count of definitions assigning the broad gate), and a case driven off a glob and a vocabulary list can pass for the wrong reason. Four shapes offered as candidates: whether each `BOUNDS` phrase sits where it bounds a list rather than somewhere else in the file; what the count case does when the framer arrives in 0.11.0 assigning the gate, and whether its failure message tells that reader what to change; whether finding 5's fourteen dates followed a re-reading or a re-stamp, given that a rider is not a check; and whether `skills/code-review/SKILL.md`'s new paragraph is a pointer plus incident or a restatement, since the 15-word window that holds the agent definitions globs `agents/*.md` and no skill is held to it. Facts handed over as executed by the orchestrator at `b8aa637`: ten modules, 340 passed, exit 0; and three checked directly — `PROBES = "## Executed probes"` exists at `round_record.py:254`, so finding 3's redirect names a section the generator parses. Handed over as read: the fix pass's 23 modules at 767 passed, `evidence-check` 1,111 ok, `rider_check` 25 ok, `survivor-check` exit 0 over both ranges, six red demonstrations including two mutants of the count case. Handed over as unverified: the full suite, the repository-wide lint and the typecheck, the sealer's after the rounds settle. Two disclosures from this chain were handed over to weigh: round 1 spawned two `Explore` subagents against §6's *spawn no agent* and disclosed neither, and the fix pass widened its own `ruff` scope to four directories, disclosed it unprompted and refused to let it move the label. One ruling was handed over so the round need not re-derive it: §2's list is three named acts — the full suite, the repository-wide lint, the typecheck — and the plugin's own record checkers are not among them whatever `broad_gate.py` bundles into the sealer's one command, so `bin/evidence-check .` was the round's to run. A finding located in a record is a correction — ⬜ with the coordinate — and stays out of `Needs a fix`.

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

## Paste-ready fixes

```python
BOUNDS = (
    "a write not below is a write you do not make",
    "a write not named here is a write you do not make",
    "is the whole of what you may write",
    "You write nothing durable anywhere, and that is the whole of it",
)
```
```
You write nothing durable anywhere, and that is the whole of it: the report you
return is your caller's to act on, and a probe file is deleted before you hand
over.
```
```
**The file is not the whole of it.** Contract §7 is about leavings, not files:
a worktree, a branch, a checkout, a scratch clone or a virtual environment your
probe made for itself is a leaving too, and the probe is not over until every
one of them is gone. Deleting the named file and stopping there is what left a
git worktree behind through a whole review chain — the report said the probe
files were deleted, and there was nothing wrong with that sentence. §7 carries
the incident that cost this rule.
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/SKILL.md:141` | round 1's 1 — fixed |
| round-1 | `agents/warden.md:157` | round 1's 2 — fixed |
| round-1 | `agents/warden.md:238` | round 1's 3 — fixed |
| round-1 | `agents/smith.md:22` | round 1's 4 — fixed |
| round-1 | `seal/ledger.md` (L7, L8, W1 and three orchestration rows) | round 1's 5 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:64` | round 1's 6 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:174` | round 1's 7 — fixed |
| round-1 | `templates/sdd-routing.md:29` | round 1's 8 — fixed |
| round-1 | `agents/warden.md:180`, `:283` | round 1's 9 — fixed |
| round-1 | `agents/sealer.md:104` | round 1's 10 — fixed |
| round-1 | `tests/test_a_moved_rule_leaves_its_definition.py:206` | round 1's 11 — answered |
| round-1 | `spec.md:44`, `plan.md:152` | round 1's 12 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the duplication guard should reach the skills a definition preloads | Two of the three pairs over the window predate this branch, so widening the glob is a sweep and not this work item's | The owner, at the release that takes the sweep |
| Whether §2's naming survives the framer | Still `questions.md` Q2's, unchanged by this round; finding 8 above only asks that the case say which literals move with it | The owner, at 0.11.0 |
