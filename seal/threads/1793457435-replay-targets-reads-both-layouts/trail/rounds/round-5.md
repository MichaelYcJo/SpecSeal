# Review round 5: 1793457435-replay-targets-reads-both-layouts

```seal
target: 780a3df7, fixes f6e8dbe2..780a3df7
```

This verifying round reads the diff of the fixes, f6e8dbe2..780a3df7. The range holds two commits, and both touch the work item's records alone (executed: `git diff a2b71208..HEAD --name-only` names `changelog.md`, `frame/design.md` and `trail/rounds/round-4.md` under the work item, and nothing else). a88fe334 rewrites the last sentence of `frame/design.md` *Scope* item 4 and the changelog sentence on a name given twice. 780a3df7 appends round 4's two close blocks: finding 1 `deferred #1228`, finding 2 `fixed a88fe334`. No code changed after round 4's target a2b71208, so the code read below is the code round 4 read. The diff changes no path outside `docs/` and `seal/`, and `seal/parity.md` is not declared (executed: `ls seal/parity.md`), so no `original:` line is owed. The record is in English, since `seal/config.md` has no `Record language` row.

Carried from round 4 and not re-established: the coordinates of both generators' `main` and `say_unanswered` (`evals/scripts/seed_defects.py:386-406`, `:436-501`; `evals/scripts/replay_targets.py:960-967`, `:987-1054`), and the names of the cases that pin the `--case` answers. Every verdict below was reached this round, against the code as it stands at 780a3df7.

Axes walked over the fix diff. Error paths: every place either `main` returns 1 under `--case`, including the `SystemExit` raises a failed git call or an unusable truths file makes, which the new frame sentence does not claim to exclude. Response shape: the stderr lines of a name given twice, written and unanswered, under `--list` and under `--out`. The change's own axes are whether the deferral's home can be acted on without this record, and whether each rewritten sentence states what the code does, before this release and now. Inputs, authorization, query scope, concurrency and security have no surface in a diff of records alone.

## Findings

No finding this round.

## Confirmations

```seal
confirms: round-4#2
```
What holds: `frame/design.md:25` now ends *Scope* item 4 with "A `--case` run no longer compares the number of cases written with the number of names given: it exits 1 where a name is unanswered, and `seed_defects.py` also where no commit it read holds a round 1 record", round 4's text word for word (read: the a88fe334 diff). The code matches each clause. Neither `main` compares `len(chosen)` with the names under `--case`: `seed_defects.py:499-500` returns `1 if unanswered else 0` where `a.list or a.case`, and `replay_targets.py:1026` and `:1052-1053` do the same. The only count comparison left is the `--count` path's `len(chosen) == a.count` (read: `evals/scripts/seed_defects.py:501`, `evals/scripts/replay_targets.py:1054`). `seed_defects.py:491-498` returns 1 where `held` is false, before it looks at the names, which is the second clause. `replay_targets.py` under `--case` has no such return: a run that reads no record leaves every name in form unanswered, so it exits 1 by the first clause (read: `evals/scripts/replay_targets.py:1004-1006`, `:970-983`). The sentence no longer says "only", so the `SystemExit` paths (`evals/scripts/replay_targets.py:185`, `:242`, `:247`, `:894` and the truths-file raises at `:719-776`), which also end a run with status 1, do not contradict it. The earlier sentence of the item on `seed_defects.py`'s empty-read line, `gaps.md` *Not done* and both `main` docstrings agree with the new sentence. No other sentence in the work item's frame, plan, phases or `gaps.md` states the old "exits 1 only" (executed: `git grep -n -i 'exits 1 only\|only where a name'` over the work item, `evals/`, `tests/` and `docs/`, no hit outside the round records). a88fe334 touches `frame/design.md`, a path finding 2's `location:` names.

```seal
confirms: none
```
What matched: the deferral of round 4's finding 1 names a home that can be acted on. #1228 is open, in the milestone "backlog: review chain & agents" (executed: `gh issue view 1228`). Its body gives the symptom, the two `say_unanswered` lines at #1150's head (`replay_targets.py:963`, `seed_defects.py:394`), the two module docstrings that say "A name given twice is one name", and a done-when: each generator names an unanswered name once, and each test module holds a case that gives one name twice and counts one line. That is enough to fix it from the issue alone, since the fix is one line in each `say_unanswered`. The close says #1228 "carries" round 4's paste-ready fix. The issue in fact points to `trail/rounds/round-4.md` finding 1 for it, and `skills/settle/SKILL.md` removes that directory once the work item ships; git history keeps it. The issue names the module docstrings but not the two test docstrings that repeat the sentence (`tests/evals/test_replay_targets.py:807-809`, `tests/evals/test_seed_defects.py:425-427`). Round 4's `location:` names both test ranges, and the done-when's new case lands in the same two functions. The finding stands deferred to #1228 and is not written up again here.

```seal
confirms: none
```
What matched: the changelog sentence a88fe334 wrote, "A run no longer exits 1 for a name given twice whose case it wrote, which it used to do saying nothing; an unanswered name given twice is still named twice (#1228)", is true of the code. At the merge base afa9dd76 both `main`s set `a.count = len(a.case)` under `--case` and returned `0 if len(chosen) == a.count else 1`, with no stderr line for a name (read: `git show afa9dd76:evals/scripts/replay_targets.py` lines 829-847, `afa9dd76:evals/scripts/seed_defects.py` lines 396-414). So a written name given twice exited 1 and said nothing. At 780a3df7 the existing cases give a written name twice under `--out` and assert exit 0 with an empty stderr (read: `tests/evals/test_replay_targets.py:827-829`, `tests/evals/test_seed_defects.py:465-466`). `bin/test` ran them and they passed (executed). The probe gave each generator one unanswered name twice under `--out`. Each named it twice on stderr and exited 1, and `seed_defects.py` with `seeded-<kept> --case seeded-<kept>` under `--out` wrote the case once, exited 0 and printed nothing on stderr (executed). Under `--list` the same `say_unanswered` reads the names as given (read: `evals/scripts/replay_targets.py:963`, `:1026`, `evals/scripts/seed_defects.py:394`, `:490`). Round 4's probe ran that path at the same code. The word "still" can be read as "as the last release did", and the last release named no name at all. Read beside the sentences before it, which say the naming is new, it reads as "this release does not fix it yet". No act turns on that word, so it is no finding.

```seal
confirms: none
```
What matched: the suite's label. `gaps.md` labels the full suite, the lint and the format check at the work item's head as not verified, and names the orchestrator's `seal gate` as the answerer. Neither commit in the range claims a broad run, so the label is honest. This round leaves nothing open. Round 4's finding 1 is deferred to #1228, and finding 2's close holds. What comes due is the orchestrator's broad run, `seal gate`, and the sealer's spawn after it.

## Not judged

| What | Location | Who answers |
|---|---|---|
| The full suite, the repository-wide lint and the format check at 780a3df7 | `seal/config.md` *Broad gate* | the orchestrator, by `seal gate` now that the rounds settle |
| Scenario 5's byte-for-byte regeneration of the eight committed cases after 9237e34b, carried from round 4 | `frame/design.md` *User scenarios* row 5 | the sealer, as `gaps.md` names it |
| Scenario 4's clone run over v0.27.0 and v0.26.0, carried from round 3 | `frame/design.md` *User scenarios* row 4 | the sealer, as `gaps.md` names it |
| Round 3's ten `seal mutate` mutants, carried from round 4, read and not re-run | `seal/threads/1793457435-replay-targets-reads-both-layouts/trail/rounds/round-3.md` close of finding 1 | the sealer, when it samples the crafters' claims |
| Q1 and Q2, carried from round 1 | `frame/questions.md` | the orchestrator's measurement, and the owner for Q2 |
| A round whose `target:` names a release branch deleted since, still left out | `evals/scripts/replay_targets.py#targets` | #1224, out of scope by the frame |

## Probes

| Command | Result |
|---|---|
| `git diff a2b71208..HEAD --name-only` in the branch worktree | three paths, all under `seal/threads/1793457435-replay-targets-reads-both-layouts/`: no code changed after round 4's target |
| `bin/test -q tests/evals/test_replay_targets.py tests/evals/test_seed_defects.py -k names_each_named_case` in the branch worktree at 780a3df7 | exit 0, 3 passed: the written name given twice exits 0 with an empty stderr in both generators |
| `bin/test -p no:xdist -p no:cacheprovider -q -s tests/evals/test_tmp_round5_probe.py` in the branch worktree; one file reusing `tagged_repo`, `shipped_item` and `commit_everything_as_e`, run once | exit 0, 2 passed. Under `--out`, `replay_targets.py --case replay-1-r1 --case replay-1-r1` exited 1 and named the name twice, and `seed_defects.py --case seeded-<kept> --case seeded-12345678 --case seeded-12345678` exited 1 and named `seeded-12345678` twice. `seed_defects.py --out` with a written name given twice wrote it once, exited 0, stderr empty. The `--list` lines the probe printed were taken by the next `readouterr` and not shown, so this probe settles nothing under `--list` |
| `git grep -n -i 'exits 1 only\|only where a name\|given twice'` over the work item outside its rounds, `evals/`, `tests/` and `docs/` | no "exits 1 only" left; "given twice is one name" stands in the two module docstrings and the two test docstrings round 4's finding 1 names, deferred to #1228 |
| `gh issue view 1228 --json number,title,state,body,labels,assignees,milestone,comments` | open, milestone "backlog: review chain & agents", no assignee, body with symptom, coordinates and a done-when |
| `ls seal/parity.md` | no such file |

The probe file and its bytecode were removed before hand-back, and nothing it made is left in the worktree.
