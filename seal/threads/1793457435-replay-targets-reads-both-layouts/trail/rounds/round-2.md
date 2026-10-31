# Review round 2: 1793457435-replay-targets-reads-both-layouts

```seal
target: 46155dda, fixes 47fa757b..46155dda
```

This verifying round reads the diff of the fixes, 47fa757b..46155dda. That covers round 1's fix pass (32584024, 027be610, the close blocks at d0c12be5), the orchestrator's fold of `frame/design.md` *Scope* items 4 and 5 and its row of `frame/plan.md` *Judgments of the run* (8d45edfb), and the build of the grown item 4 (31da1258, db1d502b, 46155dda). The units read are `replay_targets.py#blocked`, `replay_targets.py#say_unanswered` and the `--list` branch of `replay_targets.py#main`, `seed_defects.py#say_unanswered` and the reworked `seed_defects.py#main`, and the three test cases the range adds or rewrites. The diff edits no path outside `evals/`, `tests/` and this work item's records (executed: `git diff --stat 47fa757b..46155dda`), so no `original:` line is owed, and `seal/parity.md` is not declared. The record is in English, since `seal/config.md` has no `Record language` row.

Carried from round 1 and not re-established: a `seal` opener stands at a release tag only in v0.27.0's 10 round records, and each of them parses (round 1's `git grep` over the release tags). Fetching the origin's `refs/pull/*/head` into a scratch clone is what lets the reviewed commits resolve, as round 1's probes did it. Every verdict below was reached this round.

Axes walked over the fix diff: inputs (`--case` with and without `--list`, a name that is read, left out or never read, and a name whose digits are not exactly eight), exclusions and boundaries (a record whose every `seal` block is refused, a refusal that names no `seal` opener, an empty read), response shape (each stderr line, its order beside the empty-read line, and the exit code), and error paths (each new exit 1). The change's own axis is that the two generators answer one name alike. The design asks for that in scope item 4. Authorization, concurrency and security have no surface here: both scripts are maintainer tools, and neither holds a gate.

## Findings

### 1. `seed_defects.py --case` tells a person that no release shipped a commit the release did ship, where the name's digits are not exactly eight

```seal
severity: should
location: `evals/scripts/seed_defects.py:378-391`, `tests/evals/test_seed_defects.py:428-432`, `seal/threads/1793457435-replay-targets-reads-both-layouts/changelog.md:7`
evidence: executed `bin/test tests/evals/test_tmp_round2_probe.py -p no:xdist -q -s`
regression: round-1#1
```

Why it matters: the unit is `seed_defects.py#say_unanswered`, which 31da1258 added. `frame/design.md` *Scope* item 4, grown at 8d45edfb by the row of `frame/plan.md` *Judgments of the run* that folds this unit into round 1's finding 1, asks that `--case` name each name no shipped commit answers, as `replay_targets.py` does. The fix gives that name a reason about the releases, "no release shipped a commit that begins with" the name's digits (`evals/scripts/seed_defects.py:387-388`). The run never reads the releases that way. It reads only the commits whose first eight digits equal a name's digits, at `seed_defects.py:292` (`commit[:8] not in prefixes`). So the defect comes from the fix's wording and not from the frame.

The probe named one shipped commit three ways over the module's `shipped_item` fixture, with `--list --case`. With its first eight digits, the run listed the commit and exited 0. With its full 40-digit SHA, it printed `seeded-<sha> not written: no release shipped a commit that begins with <sha>` and exited 1. It did the same with its first seven digits. In both cases the commit was the one release v1.1.0 shipped. A person who pastes a full SHA is told that the release never shipped it. `replay_targets.py#not_written` gives the comparable name the reason "no record of its work item was read". That sentence is about what the run read, so it stays true. The changelog fragment (`changelog.md:7`) repeats the false sentence, and `tests/evals/test_seed_defects.py:430` pins it.

The fix makes the reason say what the run read. That is the only thing the run knows (contract rule 14: the test that pins the line changes in the same commit):

```python
def say_unanswered(names, answered, left):
    """Say on stderr each of `--case` NAMES that ANSWERED does not hold,
    with why it was not written: the reason its commit was left out with
    among LEFT, else that no shipped commit read has the name's digits as
    its first eight; how many there were. The line is
    `replay_targets.py#say_unanswered`'s."""
    unanswered = [name for name in names if name not in answered]
    for name in unanswered:
        why = next(
            (w for commit, w in left if case_name({"commit": commit}) == name),
            "no shipped commit read has "
            + name.removeprefix("seeded-")
            + " as its first eight digits",
        )
        print(f"seed_defects: {name} not written: {why}", file=sys.stderr)
    return len(unanswered)
```

In `test_names_each_named_case_no_shipped_commit_answers_with_its_reason`, `unshipped` becomes `"seed_defects: seeded-12345678 not written: no shipped commit read has 12345678 as its first eight digits\n"`. The case also gains a run of `--list --case seeded-<full sha of commits["squash"]>` that expects that sentence for the full SHA, seen red against 46155dda. The changelog's sentence ends "or that no shipped commit read has the name's digits as its first eight."

```seal
verdict: fixed 28e10171
answer: The finding holds: `targets` keeps a commit only where its first eight digits equal a name's digits, so the reason "no release shipped a commit that begins with" claimed a read the run never made. The paste-ready reason was applied. `say_unanswered` now says "no shipped commit read has <digits> as its first eight digits", and its docstring says that is all `targets` compares. The interface was kept: the module docstring gives a case's name as `seeded-<commit[:8]>`, so reading a full SHA or seven digits as a name would widen what `--case` accepts, which the frame does not ask. `test_names_each_named_case_no_shipped_commit_answers_with_its_reason` pins the new sentence, and it gains a `--list` run naming the shipped commit by its full SHA beside its eight-digit name. That run exits 1 with the new sentence for the full SHA alone. The case was seen red against 1f96e0a5's script on the old sentence (executed). `seal mutate` over the new reason went red (executed). The changelog fragment's sentence was rewritten in the same commit. `git grep` on the old wording found no other statement of it outside this record.
```

## Confirmations

```seal
confirms: round-1#1
```
What holds: `replay_targets.py --list --case` now names each name that no listed line answers, and exits 1 (`evals/scripts/replay_targets.py:1012-1015`, through `say_unanswered` at `:953-960`). A name that a kept line or a `left out:` line answers stays off stderr. Round 1's probe input, `--list --case replay-1-r1` over `tagged_repo`, now gives exit 1 and the line `replay-1-r1 not written: no record of its work item was read`. `test_names_each_named_case_no_listed_line_answers_with_its_reason` pins that line, and it passes at 46155dda (executed: `bin/test tests/evals/test_replay_targets.py tests/evals/test_seed_defects.py -q`, 44 passed). It fails against 47fa757b's scripts with `assert 0 == 1` (executed: the 46155dda test modules copied into a worktree of the clone at 47fa757b). So it was seen red against the defect, as the close claims. The write path now says its names through the same helper, and its lines and exit code are unchanged.

```seal
confirms: round-1#2
```
What holds: `blocked` (`evals/scripts/replay_targets.py:319-341`) now counts a record whose every `seal` block the parser refuses. I read `hooks/lib/fields.py#read` (`hooks/lib/fields.py:335-370`) to check what the new condition can see. A refusal that is not `COMMENT_LINE`, `UNCLOSED` or `UNSURE` comes only from `_block`, and `read` calls `_block` only for a fence whose line equals `OPENER`. `UNCLOSED` and `UNSURE` are counted only at a line equal to `OPENER`. So the condition counts exactly the records with a `seal` opener in the form's spelling, and every refusal it indexes has a line of 1 or more. `test_refuses_a_record_in_seal_blocks_the_check_refuses` pins the three refused shapes from the close, and the three shapes that stay with the other readers. It passes at 46155dda and fails against 47fa757b (executed, the same two runs). Scenario 4 was re-run at 46155dda in a scratch clone with the origin's pull refs fetched (executed: `python3 evals/scripts/replay_targets.py --list`). It exited 0 with an empty stderr and printed 50 lines: 17 kept, 15 `the target line names no base that resolves`, 12 `no next round to confirm a fix` and 6 `no fixed finding the next round confirmed`. No line read `Target SHA (none) does not resolve`. These are round 1's counts, plus one line for this work item's own round 1, which stands in the clone's working tree and has no next round. This settles the `gaps.md` row that left the Scenario 4 rerun to the sealer.

```seal
confirms: none
```
What matched: Scenario 5 after 31da1258, which the crafter's `gaps.md` row left to this round (executed). The four replay cases and the four seeded cases were regenerated with `--case` in the clone at 46155dda and in a worktree of it at a92c358b. All four runs exited 0, and `diff -r` of the two output directories printed nothing. Compared with the committed cases, only the four replay scaffolds differ, each in its `git remote add origin` line, which the frame records as read from the clone's remote.

```seal
confirms: none
```
What matched: the reworked `seed_defects.py#main` (`evals/scripts/seed_defects.py:437-485`). The write loop is unchanged, and it now runs only under `elif held`. So a run that read no round 1 record still writes nothing, as it did when it returned before the loop. Each name is said before the empty-read line. Under `--list`, a name whose commit was left out is answered by its `left out:` line, and without `--list` it is said with that reason. `test_names_each_named_case_no_shipped_commit_answers_with_its_reason` pins each of these orders, passes at 46155dda, and fails against 47fa757b with `assert 0 == 1` (executed). The `gaps.md` *Not done* paragraph is accurate on both points it makes. `replay_targets.py --case` over an empty read prints only the names, because the empty-read branch runs only without `--case` (`evals/scripts/replay_targets.py:993-1006`). `seed_defects.py` adds the empty-read line after the names (read, and pinned by the case's last two asserts).

```seal
confirms: none
```
What matched: the new cases were read against their groups. `test_names_each_named_case_no_listed_line_answers_with_its_reason` covers the `--list` branch, which the existing `test_names_each_named_case_it_did_not_write_with_its_reason` does not reach. The seeded case covers `--case` naming, which no earlier seeded case covers. `bin/seal layout --pairs` in the clone exited 0 and named no pair holding either module (executed).

```seal
confirms: none
```
What matched: the suite's label. `gaps.md` labels the full suite, the lint and the format check at the work item's head as not verified, and names the orchestrator's `seal gate` as the answerer. No commit in the range claims a broad run, so the label is honest.

## Not judged

| What | Location | Who answers |
|---|---|---|
| The full suite, the repository-wide lint and the format check at 46155dda | `seal/config.md` *Broad gate* | the orchestrator, by `seal gate` once the rounds settle |
| Q1: what the proofer does when the current release runs a committed 0.22.x case (carried from round 1) | `frame/questions.md` Q1 | the orchestrator's measurement after the rounds |
| Q2: whether the eight committed 0.22.x cases are replaced (carried from round 1) | `frame/questions.md` Q2 | the owner; the default (b) holds for this work |
| A round whose `target:` names a release branch deleted since, still left out (15 records over v0.27.0 and v0.26.0 in this round's run) | `evals/scripts/replay_targets.py#targets` | #1224, out of scope by the frame |

## Probes

| Command | Result |
|---|---|
| `bin/test tests/evals/test_replay_targets.py tests/evals/test_seed_defects.py -q` in a scratch clone at 46155dda | exit 0, 44 passed |
| The same two modules from 46155dda, copied into a worktree of the clone at 47fa757b, run with `-k` on the three cases the range adds or rewrites | exit 1, 3 failed: the `seal`-blocks case on the refusal's line, and the two `--case` cases on `assert 0 == 1` |
| `python3 evals/scripts/replay_targets.py --list` in the clone at 46155dda, with the origin's `refs/pull/*/head` fetched | exit 0, empty stderr, 50 lines: 17 kept, 33 left out, none as `Target SHA (none) does not resolve` |
| `replay_targets.py --case` for the four replay cases and `seed_defects.py --case` for the four seeded cases, in the clone at 46155dda and in a worktree of it at a92c358b, then `diff -r` of the two output directories | all four runs exit 0; the diff is empty |
| `bin/test tests/evals/test_tmp_round2_probe.py -p no:xdist -q -s` in the clone, one file reusing the module's `shipped_item`, calling `seed_defects.main(["--list", "--case", name])` with the shipped commit's first 8 digits, its first 7 and its full SHA | 8 digits: exit 0, the commit listed; 7 and 40 digits: exit 1, `no release shipped a commit that begins with` the digits, while the commit was shipped. The file was deleted after the run |
| `bin/seal layout --pairs` in the clone | exit 0; no pair names `test_replay_targets.py` or `test_seed_defects.py` |
