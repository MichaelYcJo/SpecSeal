# 1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks — review round 1

| Field | Value |
|---|---|
| Target SHA | 80445412d4524ec57299a5aa171dc8b846282a77 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #765 |
| Broad gate | b68042f4 against 78d795fa |
| Fixes checked by | no fixes to check |
| Fix range | `80445412d4524ec57299a5aa171dc8b846282a77..608ad8412adfc2f6a8ac5132d8026f523816818f`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item `1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks` (#750, PR #765). The target is `80445412`, against `release/v0.18.1` at `edee5ca2`.

Spec compliance first. Check that the rule sentence in `docs/worktree-guard-spec.md` §*Which tree* says what `switch_kind` does, clause by clause. Then check that the pin, the three `KINDS` rows and the rule case (C3) each fail when the thing they hold changes. Compare the sentence against `switch_kind` over a generated set of `checkout` and `switch` commands built by construction, and do not rely on the `KINDS` rows alone.

Quality second. The smith changed one coordinate in the frame's `spec.md` to write out a heading in full, and wrote three `Re-read ·` rows (M2, K5, K7). Judge both.

The orchestrator verified the guard module, the hygiene modules and the line-end module (343 passed) and ruff on the two changed Python files at the target. The release head carries 10 drifted rows from the wave-one squashes. They belong to a parallel chore, not to this item.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the comment beside `judged=set()` says the default subtracts this case's own frozen half; the same commit moved that half off the frozen walk | `tests/test_guard_resolves_the_tree_it_judges.py:1221` | answered | no change. The comment beside `judged=set()` names the frozen walk as the side the case compares, and the line it sits beside still makes that comparison. What C3 changed is where `frozen` is read from, and the docstring of the case states that. Editing the comment after the run's one round that opened nothing would commission a change no round reads; read: `frozen` at line 1230 is built from `split_segments_with_separators`, the comment names the frozen walk |
| ⬜ 2 | the rule case's `frozen` is the whole command's segments, stricter than the per-view condition `POLICY_RULE` states | `tests/test_guard_resolves_the_tree_it_judges.py:1228` | answered | no change. The case's `frozen` set, the union of the command's segments, is stricter than `POLICY_RULE`'s per-view condition. The reviewer measured that the two do not part on any shape the case generates, so the stricter set can fail only where the per-view one would also have to be judged; read; executed: green at the target, so no generated shape separates the two today |
| ⬜ 3 | the closing memo lists `evidence-check --strict` as executed with no result, and it exits 2 at the target | `seal/specs/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks/overview.md:12` | answered | corrected in the record commit: `overview.md` now gives the strict check's exit 2, with every drifted row the wave-one squashes' and none this item's; executed: exit 2, the 10 wave-one rows; this item's fragment is clean. A paperwork correction |
| 🟢 | the corrected sentence states `switch_kind`'s words, clause by clause and in its order | `docs/worktree-guard-spec.md:631` | confirmed | read against `hooks/worktree-guard.py:290-322`; executed: 82,742 generated commands, 0 differ; the base sentence differs on 6,136 |
| 🟢 | the pin and each of the three new `KINDS` rows fail when what they hold changes | `tests/test_guard_resolves_the_tree_it_judges.py:1266` | confirmed | executed: four mutants, each red on its own row; the `before --` row is the only one red under the base sentence's reading |
| 🟢 | C3 makes the rule case fail when the per-view subtraction is dropped, and loses no coverage of the judged subtraction | `tests/test_guard_resolves_the_tree_it_judges.py:1224` | confirmed | executed: red at the target, green with the base test; the judged-subtraction mutant reds the same seven cases before and after |
| 🟢 | `switch_kind`'s docstring states the same words in `classify`'s order, and no executable line changed | `hooks/worktree-guard.py:296` | confirmed | read: the diff touches docstring lines only |
| 🟢 | the `spec.md` coordinate written out in full resolves and changes no meaning | `seal/specs/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks/spec.md:159` | confirmed | executed: the records arm reads it as `DRIFTED`, not refused; read: the heading is K7's |
| 🟢 | the `Re-read ·` rows for M2, K5 and K7 are honest; each cited claim holds after the edit | `seal/ledger/1791089705-the-worktree-guards-switch-rule-says-what-the-guard-asks.md:2` | confirmed | read against `seal/releases/0.16.0.md:248` and `seal/releases/0.18.0.md:134`, `:136`; executed: no drift for M2, K5, K7 |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` at `80445412` | 135 passed |
| the corrected sentence read literally against `switch_kind`, every word list of length 0 to 4 over 14 words, `switch` and `checkout` | 82,742 compared, 0 differ |
| the base sentence, same set | 6,136 differ |
| pin: `docs/worktree-guard-spec.md` restored to `edee5ca2` | the pin case red |
| `-B` dropped from `switch_kind`'s `checkout` tuple | `checkout -B with no name` red, 17 others green |
| the `checkout` branch's `--` return deleted | `checkout -- path` and `checkout a name before --` red |
| `switch` reading only the words before `--` | `switch -- a name` red alone |
| `kind and kind not in frozen` → `kind`, target test file | the rule case and `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` red |
| the same mutant, base test file | only `test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it` red |
| `return wider - set(judged)` → `return wider`, target and base test files | the same seven cases red in both |
| `bin/test` over the five modules that read `docs/worktree-guard-spec.md` | 321 passed |
| `bin/evidence-check --strict .` at `80445412` | exit 2: 10 drifted rows, all wave-one; this item's fragment 11 ok, 0 drifted |
| `bin/survivor-check --range edee5ca2...80445412` | exit 0, 3 removed sentences, none standing |
| the broad gate (full suite, lint, typecheck) | not yet, and not this round's: the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
