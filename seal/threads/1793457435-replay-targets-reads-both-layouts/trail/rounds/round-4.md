# Review round 4: 1793457435-replay-targets-reads-both-layouts

```seal
target: a2b71208, fixes 54ec5a37..a2b71208
```

This verifying round reads the diff of the fixes, 54ec5a37..a2b71208. The range holds four commits. 11d1ea61 adds a row to `frame/plan.md` *Judgments of the run*: the run goes on past round 3 for one fix pass and this round, and stops here. 9237e34b is the fix. It gives each generator one `CASE_NAME` form and a `NAMED` line, reads a `--case` name only where `CASE_NAME.fullmatch` accepts it, answers any other name with `NAMED`, and removes `a.count = len(a.case)` from both `main`s. It also rewrites the docstrings, the changelog sentence, three cases and `gaps.md`. 3035c0fd appends the close block to round 3's finding 1. a2b71208 is the orchestrator's fold of `frame/design.md` *Scope* item 4. The units read are `CASE_NAME` and `NAMED` in both scripts, `replay_targets.py#say_unanswered`, `#not_written` and `#main`, `seed_defects.py#say_unanswered` and `#main`, the three changed cases, the changelog sentence, the new `gaps.md` row, the new plan row and the folded *Scope* item 4. The diff changes paths outside `docs/` and `seal/` (`evals/`, `tests/`), but `seal/parity.md` is not declared (executed: `ls seal/parity.md`), so no `original:` line is owed. The record is in English, since `seal/config.md` has no `Record language` row.

Carried from round 3 and not re-established: `bin/seal layout --pairs` names no pair holding `test_seed_defects.py` or `test_replay_targets.py`, and no new test function was added, only assertions inside three existing cases. Scenario 4's clone run over v0.27.0 and v0.26.0 was not run again. Every verdict below was reached this round.

Axes walked over the fix diff. Inputs: a name in each form, a bare seeded name, a full SHA, a bare replay name, `replay-<epoch>` with no round, `replay-<epoch>-r01`, a written name given twice and an unanswered name given twice. Response shape: the stderr lines, their order beside the empty-read line, and stdout under `--list`. Error paths: the exit of a `--case` run, with and without `--list`, where every name is answered, where one is not, and where no commit read holds a round 1 record. The change's own axis is whether `CASE_NAME` accepts every name the generator itself writes, so that no case it can write is refused when named. Authorization, concurrency and security have no surface here: the scripts are maintainer tools and hold no gate.

The crafter's enumeration, read against both `main`s at a2b71208 (read: `evals/scripts/seed_defects.py:436-501`, `evals/scripts/replay_targets.py:987-1054`). The close lists nine paths in `seed_defects.py#main` and eight in `replay_targets.py#main`. Each path in the code is on the list: the tag widening under `if a.case`, the digits or epochs handed to `targets`, the comparison in `targets` and `records#wanted`, `--list`'s answered set, the write path's `chosen`, the removed count, `say_unanswered`, the empty-read line and the exit. The method, taking each `main` apart into every place a name is read, is one of contract rule 12's three, so the list of paths is whole. Finding 1 is one input on path (7) that the fix's own new sentence names and that path (7) was not read for. The orchestrator has decided that any further finding on this mechanism is deferred to an issue, so each finding below is written to be acted on from this record alone.

## Findings

### 1. An unanswered `--case` name given twice is named twice on stderr, against the new sentence that a name given twice is one name

```seal
severity: should
location: `evals/scripts/replay_targets.py:960-967`, `evals/scripts/seed_defects.py:386-406`, `evals/scripts/replay_targets.py:50-53`, `evals/scripts/seed_defects.py:47-53`, `tests/evals/test_replay_targets.py:800-829`, `tests/evals/test_seed_defects.py:409-484`
evidence: executed `.venv/bin/python -m pytest -p no:xdist -p no:cacheprovider -q -s tests/evals/test_tmp_round4_probe.py -k twice`
regression: round-3#1
```

Why it matters: the unit is `say_unanswered` in both generators, with the module docstring sentence beside it. *Scope* item 4 asks that each unanswered name be named on stderr with its reason and says nothing of a repeated name, and the plan row of 11d1ea61 asks the fix to enumerate every path a name is read by. 9237e34b wrote "A name given twice is one name." into both module docstrings and the changelog, and made it hold on the exit path alone, by removing the count. Path (7), `say_unanswered`, still iterates the names as given: `unanswered = [name for name in names if name not in answered]` (`evals/scripts/replay_targets.py:963`, `evals/scripts/seed_defects.py:394`). So the defect came from how the fix was written, not from the frame.

The probe ran each generator at a2b71208 with one unanswered name given twice. `replay_targets.py --list --case replay-1-r1 --case replay-1-r1` exited 1 and printed `replay_targets: replay-1-r1 not written: no record of its work item was read` twice. The same run with `--out` printed the same two lines. `seed_defects.py --list --case seeded-12345678 --case seeded-12345678` exited 1 and printed `seed_defects: seeded-12345678 not written: no shipped commit read has 12345678 as its first eight digits` twice, then the empty-read line. The `--out` run printed the same. The exit is right in every run. A person reading the stderr sees one name reported as two failures, and a reader of the docstring is told that cannot happen. The count `say_unanswered` returns is also 2 for one name. No caller reads the count beyond its truth (read: `evals/scripts/replay_targets.py:1026`, `:1051-1053`, `evals/scripts/seed_defects.py:490`, `:499-500`), so the count changes no exit.

The fix reads each name once, in the order given, in both generators. The written-name runs the cases already hold keep passing, since an answered name prints nothing either way.

```python
# evals/scripts/replay_targets.py#say_unanswered, and the same line in
# evals/scripts/seed_defects.py#say_unanswered
    unanswered = [name for name in dict.fromkeys(names) if name not in answered]
```

The cases gain one run each, seen red against a2b71208 (contract rule 15). In `test_names_each_named_case_it_did_not_write_with_its_reason`, after the first assertion (`tests/evals/test_replay_targets.py:814-818`):

```python
        assert rt.main(["--case", "replay-1-r1", "--case", "replay-1-r1"]) == 1
        assert capsys.readouterr().err == (
            "replay_targets: replay-1-r1 not written: no record of its work item "
            "was read\n"
        )
```

In `test_names_each_named_case_no_shipped_commit_answers_with_its_reason`, after `assert case(nothing) == 1` and its `readouterr` (`tests/evals/test_seed_defects.py:479-480`):

```python
        assert case(nothing, nothing) == 1
        assert capsys.readouterr().err == unshipped + empty
```

```seal
verdict: deferred #1228
answer: Deferred by the orchestrator's decision recorded in `frame/plan.md` *Judgments of the run* (11d1ea61): this is the fourth finding of the run on how a generator answers a `--case` name, and the run stops after round 4 rather than spend another round on a maintainer's tool that gates nothing. #1228 carries the symptom, the coordinates and this round's paste-ready fix. The changelog sentence that said a name given twice is one name now says what still happens (a88fe334); the two docstrings keep it, and #1228 names them.
```

### 2. `frame/design.md` *Scope* item 4 says a `--case` run exits 1 only where a name is unanswered, and `seed_defects.py --case` exits 1 with every name answered where no commit it read holds a round 1 record

```seal
severity: should
location: `seal/threads/1793457435-replay-targets-reads-both-layouts/frame/design.md:25`, `evals/scripts/seed_defects.py:491-500`
evidence: executed `.venv/bin/python -m pytest -p no:xdist -p no:cacheprovider -q -s tests/evals/test_tmp_round4_probe.py -k unheld`
```

Why it matters: the fold a2b71208 ends *Scope* item 4 with "A `--case` run exits 1 only where a name is unanswered". The same item, two sentences earlier, says `seed_defects.py` exits 1 where no commit it read holds a round 1 record, and the code does that first, before it looks at the names: `if not held: ... return 1` stands above `if a.list or a.case: return 1 if unanswered else 0` (`evals/scripts/seed_defects.py:491-500`). The probe ran `seed_defects.py --list --case seeded-<the bump commit's first eight>`, over a fixture whose one named commit adds no `routing.md`. Stdout listed `<commit> left out: adds 0 work items' routing.md`, so the name is answered and stderr named no name. Stderr held only the empty-read line, and the run exited 1. The `--out` run named the commit with its left-out reason and then the empty-read line, exit 1. The code matches the earlier sentence, `gaps.md` *Not done* and both docstrings. The new sentence is the one that does not hold. A sealer or a later framer reading the frame against the tree gets two readings of one item. The frame is a document an agent judges against, so the sentence is a defect and not wording. The fix is the frame's, and the frame is the orchestrator's to write.

```markdown
A `--case` run no longer compares the number of cases written with the number of names given: it exits 1 where a name is unanswered, and `seed_defects.py` also where no commit it read holds a round 1 record (round 3's finding 1, 9237e34b).
```

This replaces the last sentence of *Scope* item 4, from "A `--case` run exits 1 only" to its end.

```seal
verdict: fixed a88fe334
answer: The orchestrator folded `frame/design.md` *Scope* item 4 with this round's text: a `--case` run exits 1 where a name is unanswered, and `seed_defects.py` also where no commit it read holds a round 1 record. The commit touches the work item's records alone.
```

## Confirmations

```seal
confirms: round-3#1
```
What holds: a name written without its prefix is no longer read as a case and given a reason the run's own read contradicts, in either generator. `CASE_NAME.fullmatch` decides it before anything is read (`evals/scripts/seed_defects.py:455-456`, `evals/scripts/replay_targets.py:1005`), and `say_unanswered` and `not_written` answer it with `NAMED` before they match `left` (`evals/scripts/seed_defects.py:396-403`, `evals/scripts/replay_targets.py:975-977`). The three changed cases were run against 11d1ea61's two scripts, put back into a scratch clone of a2b71208 by `git checkout 11d1ea61 --` (executed). All three failed: the seeded case on the bare name beside a listed commit, which got `no shipped commit read has 2d5c6fd5 as its first eight digits`; the replay written-name case on the name given twice, which exited 1; the replay listed-name case on the two off-form names. At a2b71208 `bin/test tests/evals/test_seed_defects.py tests/evals/test_replay_targets.py -q` passed, 44 tests (executed). So the cases pin the fix, and the crafter's seen-red claim holds.

```seal
confirms: none
```
What matched: `CASE_NAME` accepts every name the generators write from what they read at a release tag, so the narrower reading refuses no case either generator can write. Every round record path at every `vX.Y.Z` tag, in either layout, was put through `case_name`'s form and then `replay_targets.py#CASE_NAME` (executed: `git ls-tree` over each tag, then `re.fullmatch`). That covered 276 work items and rounds 1 to 15, and every name matched. No two of those work items share an epoch, so no two of them share a case name (executed). A work item in the working tree is named `<unix-epoch-seconds>-<slug>` (read: `skills/implement/SKILL.md:346`), which `CASE_NAME` also accepts. A seeded name is `seeded-` and a commit's first eight digits as git prints them, lower-case hex, which `seed_defects.py#CASE_NAME` accepts whole.

```seal
confirms: none
```
What matched: the `gaps.md` row for Scenario 5 after round 3's fix pass. Its executed part holds: each of the eight committed case names under `evals/behaviour/proofer/` matches its generator's `CASE_NAME` (executed: `re.fullmatch` over the directory names). Its read part holds too. For a name in the form, `{m["epoch"]}` and `{m["prefix"]}` give the same set the old `removeprefix` reading gave (read: `evals/scripts/replay_targets.py:1005`, `evals/scripts/seed_defects.py:455-456`). The write path is otherwise unchanged, apart from the exit. So the case files these runs write do not change by reading. The regeneration itself was not run this round, and the row names the sealer for it.

```seal
confirms: none
```
What matched: the 11d1ea61 row of `frame/plan.md` *Judgments of the run*. It says the fix decides what the mechanism reads, enumerates every path a name is read by, and answers a name of another form with the form. 9237e34b does those three things, and the enumeration's list of paths is whole (see above). Finding 1 is one input that one listed path was not read for. Finding 2 is in the fold, not in the fix.

```seal
confirms: none
```
What matched: the suite's label. `gaps.md` labels the full suite, the lint and the format check at the work item's head as not verified, and names the orchestrator's `seal gate` as the answerer. No commit in the range claims a broad run, so the label is honest. This round leaves two findings open. Under the 11d1ea61 row, they go to an issue rather than to another round. Once they have, the orchestrator's broad run is what comes due, and then the sealer's spawn.

## Not judged

| What | Location | Who answers |
|---|---|---|
| The full suite, the repository-wide lint and the format check at a2b71208 | `seal/config.md` *Broad gate* | the orchestrator, by `seal gate` once the rounds settle |
| Scenario 5's byte-for-byte regeneration of the eight committed cases after 9237e34b, not run this round (it needs the reviewed commits fetched through `refs/pull/*/head`) | `frame/design.md` *User scenarios* row 5 | the sealer, as `gaps.md` names it |
| Scenario 4's clone run over v0.27.0 and v0.26.0, carried from round 3 | `frame/design.md` *User scenarios* row 4 | the sealer, as `gaps.md` names it |
| The close's ten `seal mutate` mutants, read and not re-run; two were checked by reading against the cases (the old `items` reading caught by `said.out == ""`, the old `prefixes` reading caught by the bare name run alone with `--out`) | `seal/threads/1793457435-replay-targets-reads-both-layouts/trail/rounds/round-3.md` close of finding 1 | the sealer, when it samples the crafters' claims |
| Q1 and Q2, carried from round 1 | `frame/questions.md` | the orchestrator's measurement, and the owner for Q2 |
| A round whose `target:` names a release branch deleted since, still left out | `evals/scripts/replay_targets.py#targets` | #1224, out of scope by the frame |

## Probes

| Command | Result |
|---|---|
| `bin/test tests/evals/test_seed_defects.py tests/evals/test_replay_targets.py -q` in the branch worktree at a2b71208 | exit 0, 44 passed |
| `.venv/bin/python -m pytest -p no:xdist -p no:cacheprovider -q tests/evals/test_seed_defects.py tests/evals/test_replay_targets.py -k names_each_named_case`, using the branch worktree's virtual environment, in a `git clone --no-local` of the worktree at `<scratchpad>/1793457435-replay-targets-reads-both-layouts/round-4/clone`, checked out at a2b71208 with the two scripts put back to 11d1ea61 by `git checkout 11d1ea61 --` | 3 failed, 41 deselected: each of the three changed cases is red against the scripts before the fix |
| `.venv/bin/python -m pytest -p no:xdist -p no:cacheprovider -q -s tests/evals/test_tmp_round4_probe.py -k twice` in the same clone with the scripts back at a2b71208; one file reusing `tagged_repo`, `shipped_item` and `commit_everything_as_e`, whose output it writes past pytest's capture | 2 passed. An unanswered name given twice was named twice on stderr by both generators, under `--list` and under `--out`, exit 1 (finding 1). `replay-1792000001-r01` got `NAMED`, exit 1 |
| `.venv/bin/python -m pytest -p no:xdist -p no:cacheprovider -q -s tests/evals/test_tmp_round4_probe.py -k unheld`, the same file with a third case added | 1 passed. `seed_defects.py --case` naming only a commit left out for adding no `routing.md` answered the name and exited 1 by the empty-read line, under `--list` and under `--out` (finding 2) |
| `git ls-tree -r --name-only` over every `vX.Y.Z` tag for `seal/specs` and `seal/threads`, then each round record path through `case_name`'s form and `CASE_NAME` | 276 work items, rounds 1 to 15, no name refused, no epoch shared by two work items |
| `ls seal/parity.md` | no such file |

The probe file, the scratch clone and everything under `<scratchpad>/1793457435-replay-targets-reads-both-layouts/round-4/` were removed before hand-back.
