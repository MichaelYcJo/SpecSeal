# Review round 1: 1793457435-replay-targets-reads-both-layouts

```seal
target: ea27b618 against origin/release/v0.27.1
```

The round reads both built phases against the merge base a92c358b: phase 1 (b8a0f207 to 765cbce2, record 6c6aca99) and phase 2 (96f23815, record ea27b618). The frame is `frame/design.md`, `frame/plan.md` and `frame/questions.md` as 67fcc7e3 committed them. There are no earlier rounds, so no fact was carried and every fact below was established this round. `seal/parity.md` is not declared, so no `original:` line is owed. The record is written in English, since `seal/config.md` has no `Record language` row.

Axes walked: inputs (`--list`, `--case`, `--count` and their combinations), query scope (which tags and which layouts each run reads), exclusions and boundaries (a record in each of the three shapes, a refused record, a record whose blocks are all refused, an empty read), ordering and response shape (the target dict and its new `report` key, the stderr lines), and error paths (each new exit 1 and each `left out:` reason). This change adds three axes of its own: the record layout, the record grammar, and whether a committed case still regenerates byte for byte. Authorization, concurrency and security have no surface here: both scripts are maintainer tools. They read `git show` output for paths that a `[^/]+` pattern bounds, and they hold no gate.

## Findings

### 1. `replay_targets.py --list --case NAME` that reads no record prints nothing and exits 0

```seal
severity: should
location: `evals/scripts/replay_targets.py:968-987`, `tests/evals/test_replay_targets.py`
evidence: executed `bin/test tests/evals/test_tmp_round1_probe.py -p no:xdist -q -s`
```

Why it matters: scope item 4 of `frame/design.md` removes the silent exit 0 of a run that reads no round record. Phase 1's decision 4 prints the empty-read line only where `--case` is not given, and names each case that was not written where it is given. The account claims that every empty read is now said. The code says otherwise. At `evals/scripts/replay_targets.py:982-987` a `--list` run returns 0 after it prints the kept and left-out rounds. That return comes before the loop at `:1014-1017` that names each case that was not written. The empty-read check at `:974` runs only on the branch without `--case`. So `--list --case replay-1-r1` over a repository whose tags hold no record of that work item prints nothing to stdout or stderr and exits 0. The probe gave `0 '' ''`. This is the "nothing to do" reading the design removes. `seed_defects.py` gives the other result in the same combination: `--list --case seeded-12345678` over commits that hold nothing prints its empty-read line and exits 1 (`evals/scripts/seed_defects.py:428-435`; the probe gave exit 1 and that line). The two generators answer one question two ways. No test covers `--list` together with `--case`.

The fix is in the `--case` branch. Where nothing of the named work items was read, name each case before `--list` returns. The lines are the ones `--case` already prints, so no new message text is added:

```python
    if a.case:
        items = {name.removeprefix("replay-").rsplit("-r", 1)[0] for name in a.case}
        kept, left = targets(last_tags(None), items)
        if not kept and not left:
            for name in a.case:
                why = not_written(name, kept, left)
                print(f"replay_targets: {name} not written: {why}", file=sys.stderr)
            return 1
```

A case in `Test_module` should pin `main(["--list", "--case", "replay-1-r1"]) == 1` and its stderr line over `tagged_repo`. Contract rule 15 asks for it to be seen red against ea27b618 first.

```seal
verdict: fixed 32584024
answer: The paste-ready fix covers the empty read alone, and the cause reaches further: `--list` returned before any name was said, so a name no listed line answers stayed silent even where another named item was read. The fix is written in this pass's own words. `main`'s `--list` branch now names each `--case` name that neither a kept line nor a `left out:` line answers, with `not_written`'s reason in the `not written` line `--case` already prints, and exits 1. The write path says its names through the same new helper, `say_unanswered`. `test_names_each_named_case_no_listed_line_answers_with_its_reason` pins the empty read, a partial read, and a kept and a left-out name that stay off stderr; it was seen red against ea27b618, which gave exit 0. The module docstring, `main`'s docstring, the `Exit codes` line and the changelog fragment's `--case` sentence were rewritten. `seed_defects.py --case` still says nothing for a name no shipped commit answers while another named commit is read; scope item 4 gives it the empty-read line alone, and `gaps.md` *Not done* leaves it to the orchestrator.
```

### 2. A record in `seal` blocks whose every block the parser refuses is still read as a table, with the false reason `Target SHA (none) does not resolve`

```seal
severity: should
location: `evals/scripts/replay_targets.py:317-327`, `tests/evals/test_replay_targets.py`
evidence: executed `bin/test tests/evals/test_tmp_round1_probe.py -p no:xdist -q -s`
```

Why it matters: scope item 5 says a record in blocks "is never read as a table record". Phase 2's departure (`trail/phases/phase-2.md`, the first bullet) claims to close that class by counting "any `seal` block of a round record's kinds". `blocked` at `evals/scripts/replay_targets.py:317-327` decides this from `FIELDS.read(...).blocks`, and that list holds only the blocks the parser accepted. A record with no accepted block therefore falls through to `labelled`, which blanks every fenced line and so answers False. The record then reaches the table reader. Two records the probe built show this. The first holds one round block whose `target:` does not read whole, and no finding or confirmation block. The second holds a round block whose fence never closes. For each, `blocked` gave False, `labelled` gave False, and `round_target` gave `(None, 'Target SHA (none) does not resolve')`. That is the false reason this work removes, and the changelog fragment's sentence "A record that check refuses is left out with the check's refusal" (`changelog.md:5`) is false for these records. The phase claimed a class and enumerated it by one instance: a refused round block beside finding blocks that parse. That is a sample (contract rule 12). The parser's own output makes the list whole. A record carries a `seal` opener exactly where `read` returns a block for it, or a refusal of it: a refusal other than `COMMENT_LINE`, `UNCLOSED` and `UNSURE` is a refused block, and an `UNCLOSED` refusal at a line that is `FIELDS.OPENER` is an unclosed one. No release tag holds such a record today (executed: `git grep` over the 65 tags found an opener only in v0.27.0's 10 records, and each of them parses). This is a defect in what the tool would say about the next such record, not in any case it writes now.

The fix reads the parser's refusals as well as its blocks. It uses no pattern of this file. `fields.blocks` is the module `hooks/lib/fields.py` imports, and the `UNCLOSED` index is the opener's (`hooks/lib/blocks.py`, the `unclosed` field of `Walk`):

```python
def blocked(text):
    """True for a record in `seal` blocks: one where this tree's
    `hooks/lib/fields.py` reads a block, or refuses one, a fence that opens
    `seal` and never closes among them."""
    check, _reader = record_reader()
    fields = check.FIELDS
    read = fields.read(text, fields.ROUND_RECORD)
    lines = fields.blocks.gfm_lines(text or "")
    return bool(read.blocks) or any(
        why not in (fields.COMMENT_LINE, fields.UNCLOSED, fields.UNSURE)
        or lines[line - 1] == fields.OPENER
        for line, why in read.refusals
    )
```

`test_refuses_a_record_in_seal_blocks_the_check_refuses` should gain the two records above. Each should be left out naming the check's refusal and not `Target SHA (none)`, and each should be seen red against ea27b618.

```seal
verdict: fixed 32584024
answer: The paste-ready `blocked` was applied after reading `hooks/lib/fields.py#read` and `hooks/lib/blocks.py#Walk` in this release. It now also counts a refusal inside a block a `seal` opener opened, and an unclosed or unplaced fence at a line that is exactly the opener. The list was made by taking `read`'s outputs apart: the blocks it accepts, the eight refusals of `_block`, `UNCLOSED` and `UNSURE` (which name an opener of any info string, so only the `seal` opener's line counts), `COMMENT_LINE` (never an opener line) and the `NEAR` notice (not an opener in the form's spelling, so a record holding only such a fence still reaches the table reader, outside this class). `test_refuses_a_record_in_seal_blocks_the_check_refuses` gains three records: a round block alone with a refused `target:`, a `seal` fence that never closes, and one the walk cannot place. Each is left out with the check's refusal, and each gave `Target SHA (none) does not resolve` at ea27b618 (executed). The case also pins that a comment line and an unclosed or unplaced fence of another info string leave a record to the labelled and table readers; mutants that counted those went red. `blocked`'s docstring and the module docstring were rewritten, and the changelog fragment now says a record is judged whether the parser reads any of its blocks or refuses every one. Phase 2's departure and the frame's scope item 5 stand as the records of their time.
```

## Confirmations

```seal
confirms: none
```
What matched: phase 2's Scenario 4 run (executed). In a scratch `git clone --no-local` of ea27b618, with the origin's `refs/pull/*/head` fetched, `replay_targets.py --list` over v0.27.0 and v0.26.0 printed 49 lines and exited 0 with an empty stderr. It kept 17 records and left out 32: 15 as `the target line names no base that resolves`, 11 as `no next round to confirm a fix` and 6 as `no fixed finding the next round confirmed`. No line reads `Target SHA (none) does not resolve`. These are the counts phase 2 claims. The kept block record `1793443708-settle-keeps-a-gaps-file-anywhere` r2 has 1 truth. Its record at v0.27.0 has one finding, with `location: tests/skills/test_settle.py:1157-1164` and `verdict: fixed d79bed62`, and round 3 confirms `round-2#1`. So the truth is the one the record holds.

```seal
confirms: none
```
What matched: Scenario 5 (executed). The eight committed proofer cases were regenerated with `--case` in the clone at ea27b618 and in a worktree of it at a92c358b. All four runs exited 0, and `diff -r` of the two output directories printed nothing. Against the committed cases, the four replay scaffolds differ in the `git remote add origin` line alone, which the frame records as read from the clone's remote, and the four seeded cases are identical.

```seal
confirms: none
```
What matched: the thread layout at v0.23.x (executed: `targets(["v0.23.1", "v0.23.0"])` in the clone). It read 14 records, kept 4 and left out 10, each with a reason. Every kept target's `report` is `seal/threads/<id>/trail/rounds/round-<n>.md`. Phase 1 claimed it kept `1793140810-each-directory-holds-everything-in-one-level` r2 with 1 truth. That target is among the 4. The other three are `1793081611-…` r2, r3 and r6 from v0.23.0, which phase 1's sentence does not name. The claim is incomplete and not false.

```seal
confirms: none
```
What matched: scope item 1 and the *Removes* rows for the paths (read `evals/scripts/replay_targets.py:89-135`, `evals/scripts/seed_defects.py:184-211`). `LAYOUTS` is the one statement of both layouts. `RECORD` and `SPEC` are gone. The eight composed paths at the old `:645`, `:669`, `:674`, `:746`, `:778` and `seed_defects.py:204`, `:327`, `:348` each derive from `layout.record`, `layout.routing` or `t["report"]`. One `exempt from old_names` comment remains, on the `seal/specs` entry (executed: `grep -rn` over `evals/scripts/`).

```seal
confirms: none
```
What matched: scope item 5's reading by a real parser (read `evals/scripts/replay_targets.py:414-449`, `skills/code-review/scripts/chain_check.py:633-790`). `block_round` takes the commit, the verdicts and the `confirms:` references from the writing commit's `round_of`. It takes the `target:` value and each `location:` value from that commit's `round_read`. It keys a finding block by `first + 1`, which is the `heading_line` that `finding_of` sets, so each location belongs to its own finding. A finding with no finding block is refused by `round_of` before `located` is indexed, so the lookup cannot miss. `git grep` over all 65 release tags found a `seal` opener only in v0.27.0's records (executed). So no record at a tag before #1198 reaches `block_round` with a check that lacks `round_read`.

```seal
confirms: none
```
What matched: the crafters' departures, apart from findings 1 and 2. Phase 1's three pins outside *Removes* each move with the new `records` shape or the `report` value, and each still guards what it was written for (read `tests/evals/test_replay_targets.py:517-564`, `:842-866`; `tests/text/test_no_case_tells_the_agent_it_is_evaluated.py:43-46`). `seed_defects.targets`' `held` counts the commits `round_1_of` read, and the empty-read line follows each commit's `left out:` line (read `evals/scripts/seed_defects.py:282-301`, `:418-437`). Phase 2's rule that any parsed block marks a record as in blocks is right for the instance it names. Finding 2 is the rest of that class.

```seal
confirms: none
```
What matched: the new tests were read against their groups. `seal layout --pairs` names no duplicate pair for either module (executed). The thread-layout parameters of the seeded cases and the two-layout fixture each cover a path the earlier cases did not: a second layout, round 2 read in round 1's layout, and the report path in each layout. The block-record case covers `confirms: round-3#1` being ignored and a `rejected` finding giving no truth.

```seal
confirms: none
```
What matched: the frame's `## Rule changes` is not applied on this branch, as the frame states. The diff against the merge base edits no path under `docs/` (executed: `git diff --stat`). `docs/the-review-record.md:168` still names labelled records alone, and the settle owns that change. `gaps.md` labels the full suite and the lint as not verified and names the orchestrator's `seal gate` as the answerer. That label is honest: no phase claims a broad run.

## Not judged

| What | Location | Who answers |
|---|---|---|
| The full suite, the repository-wide lint and format check at ea27b618 | `seal/config.md` *Broad gate* | the orchestrator, by `seal gate` once the rounds settle |
| Phase 1's and phase 2's seen-red runs and their `seal mutate` batches (9, 5 and 11 mutants), which this round read but did not re-run | `trail/phases/phase-1.md`, `trail/phases/phase-2.md` | the sealer, when it samples the crafters' claims |
| Q1: what the proofer does when the current release runs a committed 0.22.x case | `frame/questions.md` Q1 | the orchestrator's measurement after the rounds |
| Q2: whether the eight committed 0.22.x cases are replaced | `frame/questions.md` Q2 | the owner; the default (b) holds for this work |
| A round whose `target:` names a release branch deleted since, which is still left out (15 records over v0.27.0 and v0.26.0 in this round's run) | `evals/scripts/replay_targets.py#targets` | #1224, out of scope by the frame |

## Probes

| Command | Result |
|---|---|
| `python3 evals/scripts/replay_targets.py --list` in a scratch clone of ea27b618, with the origin's `refs/pull/*/head` fetched | exit 0, empty stderr, 49 lines: 17 kept, 32 left out, none as `Target SHA (none) does not resolve` |
| `replay_targets.py --case` for the four replay cases and `seed_defects.py --case` for the four seeded cases, in the clone at ea27b618 and in a worktree of it at a92c358b, then `diff -r` of the two output directories | all four runs exit 0; the diff is empty; against the committed cases only the four replay scaffolds' `git remote add origin` line differs |
| `targets(["v0.23.1", "v0.23.0"])` imported from the clone's `evals/scripts/replay_targets.py` | 14 records, 4 kept with thread-layout `report` paths, 10 left out with reasons |
| `bin/test tests/evals/test_tmp_round1_probe.py -p no:xdist -q -s` in the clone, one file reusing the module's `tagged_repo`, `BLOCK_ROUND_1` and `BLOCK_ROUND_2` | a round-block-only record with a refused `target:` and one with an unclosed `seal` fence: `blocked` False, `labelled` False, `round_target` gives `Target SHA (none) does not resolve`; `BLOCK_ROUND_1` gives `blocked` True; `replay_targets.main(["--list", "--case", "replay-1-r1"])` gives 0 with empty stdout and stderr; `seed_defects.main(["--list", "--case", "seeded-12345678"])` gives 1 with its empty-read line. The file was deleted after the run |
| `git grep -l -E` for a line that is a `seal` opener, over the round records of every one of the 65 release tags | only v0.27.0, 10 records |
| `bin/seal layout --pairs` in the clone | exit 0; no pair names `test_replay_targets.py` or `test_seed_defects.py` |
