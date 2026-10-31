# Phase 2: 1793457435-replay-targets-reads-both-layouts

## What this phase found

**The frame held where it was opened.** `round_target` and `confirmed` are the two places a record's shape is decided, as phase 1's record says. The check of 7a8899d5, which last wrote every block record at v0.27.0, has the same `chain_check.py`, `hooks/lib/fields.py` and `hooks/lib/blocks.py` as this tree (executed: `git diff 7a8899d5 HEAD --stat` over the three paths printed nothing). `Parsed`, `Round` and `Finding` keep the fields `frame/plan.md` *Technical context* relies on. One part of the frame did not hold, and the build departs from it:

- **A record in blocks is one that holds any `seal` block of a round record's kinds, not only a round block.** `frame/design.md` *Data & interfaces* says that a record whose parsed blocks hold a round block is a block record. Take a block record whose round block the parser refuses, such as a `target:` value that does not read whole. `hooks/lib/fields.py` then returns its finding and confirmation blocks and no round block. By the frame's rule that record holds no round block and no `target:` line outside a fence, so it is read as a table, and it is left out as `Target SHA (none) does not resolve`. That is the false reason scope item 5 removes. By the rule built here, the commit's check judges the record and names the refusal at line 4. `test_refuses_a_record_in_seal_blocks_the_check_refuses` breaks the round block for this reason. A mutant that restores the frame's rule went red on it (mutant 2 below). Judged against: `frame/design.md` *Scope* item 5 ("It is never read as a table record"), which the frame's detection rule would break for this record.

**The decisions this phase made, each with its grounds:**

1. **`block_round` stands beside `labelled_round` and returns the same `{"sha", "value", "findings", "confirms"}`, and one function, `judged_by`, picks between them.** `round_target` and `confirmed` each ask `judged_by` once, so the shape order is stated in one place. The two readers share `refusal`, the sentence a refused record is left out with. Judged against: `frame/plan.md` *Failure scenario of the chosen approach* ("the layout statement and the shape order are each one place").
2. **`block_round` asks the writing commit's `round_of` for the commit, the findings and the `confirms:` references, and its `round_read` for the round block's `target:` value and each finding block's `location:` value.** `round_of` alone drops each location's line numbers, because `Finding.paths` keeps only the paths, and a truth needs the line. A finding's location is taken from the finding block in the span whose heading line is the finding's `heading_line`. No line of a block is read by a pattern of `replay_targets.py`. A block record is parsed twice, once by each call, and that costs one parse per record. Judged against: `skills/core/SKILL.md` *The first value* ("it reads what a command wrote or what a real parser returns") and `frame/plan.md` A6.
3. **Scenario 4's case is built on phase 1's `two_layouts` fixture, which gains a `check` and a `rounds` parameter.** A new helper, `tree_check_files`, gives the fixture this tree's check files, which read blocks. No third builder of fixture repositories was added. The case therefore reads a record in blocks in both layouts, although no release holds a 0.22.x record in blocks. It shows that the shape is read apart from the layout. Judged against: the crafter definition's rule that a new test starts from its group.
4. **The grammar half of scope item 6.** The module docstring of `replay_targets.py` now names three shapes in the order they are decided, with the block shape first. The comment above `TARGET_LABEL` no longer says that every record a replay reads stands in labelled lines. The docstrings of `record_reader`, `target_base`, `confirmed` and `round_target` name the block shape too. In `seed_defects.py`, the module docstring says `round_target` reads any of three shapes, and `target_at` says a record in blocks is judged by its commit's check. In `tests/evals/test_replay_targets.py`, the module docstring and the `LABELLED_AT` comment were rewritten. The list came from `git grep -n -i labelled` over `evals/scripts` and `tests/evals`, and from a search over `evals`, `tests`, `evals/README.md` and `docs/the-review-record.md` for "shapes", "either shape", "labelled lines" and "Target SHA (none)" (executed). That list is a sample of rule 12's kind: a search over wordings. `docs/the-review-record.md:168` still names labelled records alone. The policy root is not edited by a pull request, and `frame/design.md` *Rule changes* carries that sentence's change for the settle.

**Seen red (contract rule 15, executed).** Both new cases were run against phase 1's reader at 6c6aca99, in a scratch worktree with the new test module copied in. `test_reads_a_round_record_in_seal_blocks_by_the_check_that_wrote_it` kept no target. `test_refuses_a_record_in_seal_blocks_the_check_refuses` got `Target SHA (none) does not resolve`.

**Mutation (executed, `seal mutate`, one batch, at 96f23815): 11 mutants, 11 red.** The mutants:

- `blocked` answers False.
- `blocked` takes the frame's round-block rule.
- `block_round` reads past a refusal.
- A location value is emptied.
- Every finding reads as fixed.
- The `target:` value is emptied.
- The `confirms:` references are emptied.
- `judged_by` drops the labelled reader.
- `confirmed` reads a block record through `labelled_round`.
- The base is read through `labelled` alone.
- `refusal` names another line.

`seed_defects.py` changed in docstrings alone, so it owes no run.

**Scenario 4 (executed).** The run used a `git clone --no-local` of 96f23815, with `refs/pull/*/head` fetched from the origin. `replay_targets.py --list` over v0.27.0 and v0.26.0 printed a line for each of 49 records. It exited 0, and stderr was empty. It kept 17 targets and left out 32. No line reads `Target SHA (none) does not resolve`. By shape, read with this tree's `blocked` and `labelled`:

| Shape | Kept | No next round | No fixed finding confirmed | Target line names no base that resolves |
|---|---|---|---|---|
| blocks, 10 | 1 | 3 | 0 | 6 |
| labelled, 39 | 16 | 8 | 6 | 9 |

The kept block record is `1793443708-settle-keeps-a-gaps-file-anywhere` r2, with 1 truth. The 16 labelled targets are the 16 that phase 1's run kept. Of the 10 block records, 6 now fall under the reason `frame/design.md` *Scope* leaves out of scope: a `target:` naming a release branch that has since been deleted. That class now holds 15 records over these two tags. `frame/design.md` gives 10 for it, from the framing probe. The issue the orchestrator files for it should take this run's count.

**Scenario 5 (executed).** In the same clone at 96f23815, and in a worktree of it at a92c358b, the eight committed proofer cases were regenerated with `--case`. All four runs exited 0. `diff -r` of the two output directories printed nothing.

**The phase-boundary set (executed, one `bin/test` command, at 96f23815): 634 passed.** It ran phase 1's set again: the two modules of the *Verified by* cell, whose `test_census` cases run `tests/censuses.py`'s readers over each script, and every module that imports or names a path this phase changed. That is the list `git grep -l` gives for `replay_targets`, `seed_defects` and `evals/scripts` under `tests`, with `tests/test_conftest.py` and `tests/hooks/test_launch.py`.
