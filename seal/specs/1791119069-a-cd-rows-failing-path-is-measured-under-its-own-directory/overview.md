# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — overview

## Why this work exists

A `cd` row's failing test file read `new` at the broad gate with no run at the
base, because the gate looked for it under the repository root. Now every
`new` comes from a run of the row at the base.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How many `run(...)` calls `compare_at_base` holds | `spec.md` Scope 4: "Every run, solo or not, is a `run(...)` call written in `compare_at_base`'s own body, so `test_the_one_shell_site_is_run_and_it_applies_the_rewrite` holds unchanged" / a second loop with its own `run` call turned that case red, because it counts calls | one loop over groups, one `run` call; the case unchanged | the case's own assertion, `sorted(callers) == ["compare_at_base", "gate"]`; the spec's intent is that the case holds unchanged |
| `skills/verify/SKILL.md`'s **New?** bullet | `spec.md` Scope 7: "`skills/verify/SKILL.md` … not edited: the three words and their meanings do not change" / the bullet named `suite-at-base-<k>.txt` as the files to open, and a candidate's run is kept as `suite-at-base-<k>-<n>.txt` | edited to `suite-at-base-*.txt`; the words and their meanings untouched | contract §12 and §14: the sentence a reader acts on was made false by this change |
| Three framed lines naming pytest's internals | `spec.md` line 55 and `plan.md` lines 66–67 cite `resolve_collection_argument` and `_get_node_id_with_markup`, which live in pytest's own source and not in this tree / once this work item had a ledger fragment, `evidence-check`'s records arm read it and refused the three names (exit 2), and `tests/test_a_record_states_what_the_tree_has.py#test_this_repositorys_own_records_state_nothing_the_tree_lacks` went red | each line carries ` · NAME NOT IN TREE`, the checker's own marker; no word of the frame changed | the refusal's own text: "write NAME NOT IN TREE on the line where the record means a name the tree does not have"; the same repair a builder made in work item 1790260564. The builder wrote into the framer's files here, and only this marker |
| The order of the words in the failure form | spec silent / at 94d7b2e0 the absent files came first | the order the branch's `FAILED` lines first named the files, pinned in S3[plain] | spec silent; the reader meets the files in that order one block above |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck after the rounds | the sealer, spawned by the orchestrator |
| This repository's own lint-first row (`bin/test -q` under `-n auto`) through a real failing broad gate with a branch-new module | the sealer, at its run — only if its run fails a test |
| The cases on Windows (`cmd.exe`) and Linux; the `cd sub <file>` prefix behaves differently per shell, and the kept-file assertions assume it settles nothing | CI's three-platform test job |

## Not done

The direction the root's tree never nominates (a `cd` row whose base carries
a same-named file at the root and not below the `cd`) still reads `new?`.
That is `plan.md` Alternatives row G, not taken, and `spec.md` §*Out* names it.

## Fed back into the spec

none — the rule-3 sentences are the spec's Scope 7 text, adapted ("run
alone" for "nominated").
