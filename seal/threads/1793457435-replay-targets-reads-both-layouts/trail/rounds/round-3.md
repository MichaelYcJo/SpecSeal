# Review round 3: 1793457435-replay-targets-reads-both-layouts

```seal
target: cf10986e, fixes dd60a7a0..cf10986e
```

This verifying round reads the diff of the fixes, dd60a7a0..cf10986e. The range holds three commits. 1f96e0a5 adds a row to `frame/plan.md` *Judgments of the run* that routes round 2's regression to a fix pass. 28e10171 is the fix: it rewrites the default reason of `seed_defects.py#say_unanswered` and its docstring, the case that pins it, and the changelog sentence. cf10986e appends the close block to round 2's finding 1. The units read are `seed_defects.py#say_unanswered`, the `--case` paths of `seed_defects.py#main` that reach it, and `test_names_each_named_case_no_shipped_commit_answers_with_its_reason`. The diff changes paths outside `docs/` and `seal/` (`evals/`, `tests/`), but `seal/parity.md` is not declared (executed: `ls seal/parity.md`), so no `original:` line is owed. The record is in English, since `seal/config.md` has no `Record language` row.

Carried from round 2 and not re-established: `bin/seal layout --pairs` names no pair holding `test_seed_defects.py` or `test_replay_targets.py`. Scenario 4's run over v0.27.0 and v0.26.0 and Scenario 5's byte-for-byte regeneration were not run again. The fix changes only a line `say_unanswered` prints on stderr, and no written case file carries it (read: `evals/scripts/seed_defects.py:378-393`). Every verdict below was reached this round.

Axes walked over the fix diff: inputs (a `--case` name of eight digits, seven digits, the full SHA, a name with no shipped commit, and a name written without its `seeded-` prefix), response shape (the stderr line, its order beside the empty-read line, and stdout under `--list`), and error paths (the exit 1 of an unanswered name). The change's own axis is whether the reason states only what the run read. The fix's commit message and close block say it does. Authorization, concurrency and security have no surface here: the script is a maintainer tool and holds no gate.

## Findings

### 1. `seed_defects.py --case` says no shipped commit read has a name's digits as its first eight, for a name whose commit the run read and listed

```seal
severity: should
location: `evals/scripts/seed_defects.py:378-393`, `evals/scripts/seed_defects.py:441`, `evals/scripts/replay_targets.py:963-974`, `evals/scripts/replay_targets.py:994`, `tests/evals/test_seed_defects.py:409-470`, `seal/threads/1793457435-replay-targets-reads-both-layouts/changelog.md:7`
evidence: executed `bin/test tests/evals/test_tmp_round3_probe.py -p no:xdist -q -s`
reopens: round-2#1
```

Why it matters: the close claims that the reason now says what the run read. That holds for the inputs round 2 probed, a full SHA and seven digits. It does not hold for a name written without its `seeded-` prefix. The close and the commit message say the reason now states "all `targets` compares", and the docstring at `evals/scripts/seed_defects.py:380-382` says the same. But the run reads and answers a name in two different spellings. `main` builds the digits it reads by `name.removeprefix("seeded-")` (`:441`), so a bare name such as `6432b6d6` is read as a commit's first eight digits. `targets` keeps that commit (`:292`). The set of answered names holds `case_name(t)`, which is `seeded-6432b6d6` (`:451`, `:473`), so the bare name is never in it. `say_unanswered` then finds no `left` entry under that spelling either, and falls to the default reason.

The probe reused the module's `shipped_item` fixture and ran `main(["--list", "--case", <the shipped commit's first eight digits>])` at HEAD. Stdout listed the commit: `6432b6d6 a.py:40 'return b != 2' -> 'return b == 2'  46 lines`. Stderr said `seed_defects: 6432b6d6 not written: no shipped commit read has 6432b6d6 as its first eight digits`, and the run exited 1. Without `--list` and with `--out`, it wrote nothing, gave the same line and exited 1. So the run tells a person that it read no commit with those digits, in the same output that lists one. Before 28e10171 the line said `no release shipped a commit that begins with 6432b6d6`, which is just as false (read: the old default reason in round 2's diff). So the fix commit did not introduce this. It left the class of round 2's finding standing: a reason that states something about the run which the run's own read contradicts. Contract rule 12 asks for the class: the fix pass enumerated the old wording with `git grep`, not the inputs that reach the default reason.

The sibling has the same asymmetry (read, not executed). `replay_targets.py#main` reads work items by `name.removeprefix("replay-")` (`evals/scripts/replay_targets.py:994`). `not_written` matches `left` only under the prefixed `case_name`. For a bare `1791382684-r2` whose round 2 was read and kept, it would answer `no round 2 record of its work item was read` (`:970-973`). `frame/design.md` *Scope* item 4 asks the two generators to answer a name alike, so the fix covers both.

The fix keeps the interface the crafter kept (a case is named `seeded-<commit[:8]>`, `evals/scripts/seed_defects.py:33`, `:43`). It reads only the names in that form, and it says of any other name that it is not a case's name:

```python
# evals/scripts/seed_defects.py#main
    prefixes = (
        {n.removeprefix("seeded-") for n in a.case if n.startswith("seeded-")}
        if a.case
        else None
    )


# evals/scripts/seed_defects.py
def say_unanswered(names, answered, left):
    """Say on stderr each of `--case` NAMES that ANSWERED does not hold,
    with why it was not written: that a case is named `seeded-` and a
    commit's first eight digits, for a name not in that form; else the
    reason its commit was left out with among LEFT; else that no shipped
    commit read has the name's digits as its first eight, which is all
    `targets` compares; how many there were. The line is
    `replay_targets.py#say_unanswered`'s."""
    unanswered = [name for name in names if name not in answered]
    for name in unanswered:
        if not name.startswith("seeded-"):
            why = "a case is named seeded-<a shipped commit's first eight digits>"
        else:
            why = next(
                (w for commit, w in left if case_name({"commit": commit}) == name),
                "no shipped commit read has "
                + name.removeprefix("seeded-")
                + " as its first eight digits",
            )
        print(f"seed_defects: {name} not written: {why}", file=sys.stderr)
    return len(unanswered)


# evals/scripts/replay_targets.py#main
    if a.case:
        items = {
            name.removeprefix("replay-").rsplit("-r", 1)[0]
            for name in a.case
            if name.startswith("replay-")
        }


# evals/scripts/replay_targets.py#not_written, as its first lines
    if not name.startswith("replay-"):
        return "a case is named replay-<the work item's epoch>-r<the round>"
```

A name not in the form leaves `prefixes` or `items` empty where it is the only name, so the run reads nothing. `seed_defects.py` then adds its empty-read line after the name, which is true, since no commit was read. In `test_names_each_named_case_no_shipped_commit_answers_with_its_reason`, after `empty` is defined (`tests/evals/test_seed_defects.py:461`), add a run of the kept commit's bare digits, seen red against cf10986e:

```python
        bare = kept.removeprefix("seeded-")
        assert case(bare) == 1
        assert capsys.readouterr().err == (
            f"seed_defects: {bare} not written: a case is named "
            "seeded-<a shipped commit's first eight digits>\n" + empty
        )
```

`tests/evals/test_replay_targets.py#test_names_each_named_case_no_listed_line_answers_with_its_reason` gains the matching run of a listed case's name without `replay-`. The changelog's `seed_defects.py` sentence (`changelog.md:7`) ends "or that no shipped commit read has the name's digits as its first eight, or, for a name not in a case's form, what a case is named", and its `replay_targets.py` sentence gains the same clause.

```seal
verdict: fixed 9237e34b
answer: The finding holds, and the fix answers the decision in `frame/plan.md` *Judgments of the run*'s newest row, not the paste-ready text: a name is read as a case only in the form the module docstring gives, and any other name is answered with that form. Method: the list of inputs was built from each generator's `main`, as every path by which a `--case` name is read, matched, counted, answered or named, and not from the old wording. In `seed_defects.py#main` they are (1) the presence of a name, which widens the tags to every release and reads no name; (2) `prefixes`, the digits each name hands `targets`; (3) `targets`' `commit[:8] in prefixes`; (4) `--list`'s `answered`, the case names of the kept and left commits; (5) the write path's `chosen`, the kept targets whose case name `--case` holds; (6) the write path's `a.count = len(a.case)`, which the exit compared with `chosen`; (7) `say_unanswered`, which matched a name against `left` by case name and else named its digits; (8) the empty-read line after the names; (9) the exit. In `replay_targets.py#main` they are (1) the tags; (2) `items`, the epochs; (3) `records`' `wanted`; (4) `--list`'s `listed` and its exit; (5) `chosen`; (6) `a.count = len(a.case)`; (7) `say_unanswered` through `not_written`, which matched `left` by case name and else parsed an epoch and a round by `removeprefix` and `rpartition("-r")`; (8) the exit. Two paths were wrong in both generators. Paths (2) and (7) read a name of any form, so a bare name, a full SHA, seven digits, or `replay-<epoch>` with no round was read and then given a false reason. Path (6) counted a repeated name, so a run that wrote every named case exited 1 and said nothing; that path predates this work, at the base. Each module now states a case's name once, `CASE_NAME` (`seeded-[0-9a-f]{8}`, and `replay-<digits>-r<round from 1>`), with `NAMED` as the line for any other name. Path (2) reads only names that `CASE_NAME.fullmatch` accepts, and path (7) answers any other name with `NAMED` before it matches `left`. Path (6) is gone, and a `--case` run exits 1 exactly when it named an unanswered name. Paths (1), (3), (4), (5) and (8) see only what (2) passes or compare by `case_name`, so they did not change. The off-form spellings are an unbounded domain. `fullmatch` decides all of them, and the cases pin a sample: a bare seeded name, a full SHA, a bare replay name, and `replay-<epoch>` with no round. The paste-ready fix's `startswith("seeded-")` would still read `seeded-<full sha>` as a case, against the decision, so the form is the regex, and the line names lower-case hex. `test_names_each_named_case_no_shipped_commit_answers_with_its_reason` now expects the form for the full SHA and the bare name beside a listed commit, the form and the empty-read line for a bare name alone, and exit 0 for a name given twice. `test_names_each_named_case_no_listed_line_answers_with_its_reason` gains the two off-form replay names, and `test_names_each_named_case_it_did_not_write_with_its_reason` gains a written name given twice. The new assertions were run against 11d1ea61's scripts and failed at the first new assertion of each case (executed). Each unit was then broken by `seal mutate` at 9237e34b, ten mutants in all: each regex widened, the old reading of `prefixes` and `items` restored, `NAMED` swapped for the old reason, and the old count restored. All ten went red (executed). The changelog sentence and the module and `main` docstrings of both generators were rewritten in the same commit. `git grep` for `removeprefix("seeded-")`, `removeprefix("replay-")`, `len(a.case)` and `as its first eight` finds only the new code, its case and the changelog. Two statements stand: `frame/design.md` *Scope* item 4 lists the reasons without the form's, and that file is not the crafter's to write; `trail/phases/phase-1.md` item 4 records what phase 1 built.
```

## Confirmations

```seal
confirms: none
```
What matched: the instances round 2's finding named now get a true reason (executed: the round's probe). For the shipped commit named by its full SHA, `--list --case` exited 1 with `no shipped commit read has <40 digits> as its first eight digits`, and the `--out` run gave the same line. For its first seven digits, it gave the matching line and then the empty-read line, which is true, since `targets` read no commit (`evals/scripts/seed_defects.py:292`). This match is why round 2's finding is reopened by finding 1 and not wholly unanswered: the close holds for these inputs and not for the class.

```seal
confirms: none
```
What matched: the crafter's label on the new full-SHA assertion. It reported that the assertion was not seen red on its own. This round ran that assertion alone against 1f96e0a5's `seed_defects.py`, which the probe compiled from `git show` (executed). It failed: the old script said `no release shipped a commit that begins with <sha>`. At HEAD the same assertion passed. So the assertion pins the fix (contract rule 15), and the crafter's label was honest. Read against its group, the assertion covers what the eight-digit `seeded-12345678` run does not: that the reason quotes the name's digits whole, and that a full SHA is not accepted as a name.

```seal
confirms: none
```
What matched: the fix rewrote every statement of the old reason in the same commit (contract rule 19). `git grep -n "no release shipped"` outside the round records found nothing (executed). The docstring, the case's expected line and docstring, and the changelog sentence each carry the new wording. `bin/test tests/evals/test_seed_defects.py tests/evals/test_replay_targets.py -q` passed, 44 tests (executed).

```seal
confirms: none
```
What matched: the crafter's reason for not widening the input to full or seven-digit names. The module docstring gives a case's name as `seeded-<the squash commit's first 8 hex>` and `seeded-<commit[:8]>` (`evals/scripts/seed_defects.py:33`, `:43`, read). *Scope* item 4 asks only that a name no shipped commit answers be named with its reason. Round 2's paste-ready fix asked for the reason and not for a wider input. The choice holds, and finding 1's fix keeps it.

```seal
confirms: none
```
What matched: the 1f96e0a5 row of `frame/plan.md` *Judgments of the run*. It routes round 2's finding to a fix pass because the frame held and the defect was the reason sentence 31da1258 wrote. That matches round 2's grounds and the fix's diff, which changes no frame document.

```seal
confirms: none
```
What matched: the suite's label. `gaps.md` labels the full suite, the lint and the format check at the work item's head as not verified, and names the orchestrator's `seal gate` as the answerer. No commit in the range claims a broad run, so the label is honest.

## Not judged

| What | Location | Who answers |
|---|---|---|
| The full suite, the repository-wide lint and the format check at cf10986e | `seal/config.md` *Broad gate* | the orchestrator, by `seal gate` once the rounds settle |
| Q1: what the proofer does when the current release runs a committed 0.22.x case (carried from round 1) | `frame/questions.md` Q1 | the orchestrator's measurement after the rounds |
| Q2: whether the eight committed 0.22.x cases are replaced (carried from round 1) | `frame/questions.md` Q2 | the owner; the default (b) holds for this work |
| A round whose `target:` names a release branch deleted since, still left out | `evals/scripts/replay_targets.py#targets` | #1224, out of scope by the frame |

## Probes

| Command | Result |
|---|---|
| `bin/test tests/evals/test_tmp_round3_probe.py -p no:xdist -q -s` in the branch worktree, one file reusing `shipped_item` and compiling `seed_defects.py` at 1f96e0a5 and at HEAD from `git show` | 2 passed. At 1f96e0a5, the full-SHA name gave `no release shipped a commit that begins with <sha>`, so the new assertion alone is red there. At HEAD, the full-SHA name gave the new line with exit 1, under `--list` and under `--out`; seven digits gave the new line and the empty-read line; a bare eight-digit name listed the commit on stdout and said on stderr that no shipped commit read has those digits as its first eight, exit 1, and without `--list` wrote nothing with the same line. The file and its bytecode were deleted after the run |
| `bin/test tests/evals/test_seed_defects.py tests/evals/test_replay_targets.py -q` in the branch worktree at cf10986e | exit 0, 44 passed |
| `git grep -n "no release shipped"` outside the round records | no match |
