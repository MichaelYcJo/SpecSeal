# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `handoff.md`, `routing.md` of this item; `docs/the-record-layout.md` §*A commit after the build brings its changelog fragment along* and §*A change writes fragments, never a shared file*; `docs/round-record-spec.md` §*The fix range*, §*The fix surface*, §*The depth in `New units`*, §*A fix of a fix*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `skills/code-review/orchestration.md` §*And name the fix surface, in the same record*; `templates/sdd-phase.md`, `templates/sdd-overview.md`; `seal/config.md`
· evidence: `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md` — 9 new claims (S1–S10, S12, `unit_adders`), 5 `Corrected ·` rows (0.18.3 `S1, S5, S8, S10` and `S2, S3, S4, S6`, 0.19.0 `A1`, 0.16.0 `G9`), the rest `Re-read ·` rows written by `evidence-check --reverify --into`
· verified: executed — each phase's modules (`phases/phase-N.md`), every new case seen red, every new unit broken by `bin/mutation-check`, `bin/evidence-check --strict` at exit 0, the real range of #860 measured; read — the released rows each re-read cites; unverified — the rows below

## Why this work exists

Two readers of a range walked it by the shape of its merges and read another work item's commits, brought in by a merge, as this one's. Both now read exactly the commits `git log --ancestry-path --no-merges a..b` lists, so `New units`, `Contract changes`, `Fix of a fix` and the fragment notice read one list.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `own_units`' shape | `spec.md` §*Data & interfaces*: "`{(path, unit): {full, …}}`" / the code returns `{(path, unit): {full: "added" or "changed"}}` | code | `unit_adders` answers which `fixed` commit ADDED a unit, and a set of commits cannot say a later fix only changed it. With a set, the unit gains a second candidate row and the depth refusal falls back to its file-level message. `test_a_unit_one_fix_added_and_the_next_only_changed_is_the_first_fixs` pins it (`phases/phase-2.md`) |
| 0.19.0's `A1` | `spec.md` §*Data & interfaces* and `plan.md` phase 4: "a re-read of 0.19.0's `A1` row" / a `Corrected ·` row | code | the claim "lands … to a top-level unit the previous record's `Fix range` added … or changed" is false for a unit a merge brought in, and `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*: "A claim that went with its code is a `Corrected ·` row" — a `Re-read ·` row cannot restate a claim |
| 0.16.0's `G9` | not in the spec / a `Corrected ·` row | code | `G9` said `call_sites` splits `git grep -n` with `gfm_lines`; phase 3 changed that walk, which the spec did not foresee among the released rows |
| `touched`'s deletions | `spec.md` §*In*: "the union of the owned commits' changed paths, deletions left out" / the union intersected with the paths `b` carries | code | one intersection leaves out a path the range deleted and a path only a merged-in commit deleted after an own change; a status filter lets the second through as a file the heuristic read (`phases/phase-2.md`) |
| `call_sites`' flags | `spec.md` §*In*: `git grep -n -z` / `git grep -n -z -I` | code | a binary file that holds the call is one line with no NUL, which the NUL walk reads as the head of the next match; the old `:` split read it as no match (`phases/phase-3.md`) |
| the two `walk_tip` cases' names | `questions.md` Q4 default (a): "keep the shapes, rewrite the docstrings and add the new assertion" / shapes kept, names changed too | code | each name stated `walk_tip`'s premise, a mechanism that is gone (`phases/phase-1.md`) |
| the ledger fragment's name | the spawn prompt: `seal/ledger/1791384160.md` / `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md` | code | `.github/scripts/fold_ledger.py` takes the `### <id>` heading and the marker from the file name, and every fragment in history carries the full id |
| "the five text-hygiene modules the brief names" | `plan.md` phase 4 / no brief in this tree names them | the reading below | the run's brief is not on this branch or on `chore/834-every-reader-and-record-is-inventoried`. Phase 4 ran the seven modules that hold document text to its rules over the files this item changed: `test_docs_line_wrap`, `test_no_passage_is_pasted_into_a_second_file`, `test_one_word_one_meaning`, `test_no_real_identifiers`, `test_release_hygiene`, `test_a_document_has_room_for_the_next_fold`, `test_a_folded_statement_names_what_enforces_it` |
| how the rule is stated | `spec.md` §*In* before the reframe: a merged-in commit "descends from `a` never" / rounds 1–3 each found an example beside the rule false in a history its author had not built, and the run stopped at round 3 on a second fix of a fix | the reframe, phases 5–7 | `spec.md` §*Reframed after round 3*: the home states only the sentence the code runs, every history the rounds built is a case of `tests/test_a_range_owns_what_git_lists_for_it.py`, and `tests/test_the_range_rule_states_no_shape.py` keeps shape and time vocabulary out of the home and its carriers |
| shape D as two cases | `plan.md` phase 5: one case per shape, "D-branch and D-CI" / one case reading both checkouts, in the shape module and in the fragment module | code | on the branch D is a straight line every reading of a range agrees on, so neither mutation of `own_commits` turned that half red alone; read together, `--first-parent` turns the case red (`phases/phase-5.md`) |
| the guard's list | `questions.md` Q6 (a): the nine proposed words and phrases / the nine plus `descends? from \S+ never` | code | round 1's false sentence used none of the nine, and the guard's own case asserts that each round's false sentence trips the list (`phases/phase-6.md`) |

**Measured on #860's own range, after the build.** `99bcad40..092004bb` resolves in this clone. Its 5 own commits are 856aeeec, 56e98860, bab19faa, d6faf419 and 092004bb. `touched` reads 9 paths where the two ends' diff lists 74. In those 9 paths, `measure` finds 13 units added between the ends, and the per-unit filter keeps 2, both in `tests/test_the_seal_is_taken_once_by_the_sealer.py`. Over the two ends' `.py` paths, the reading before this work finds 113 added units; the record it wrote named 111, one per name. `spec.md`'s 22 was a count of top-level names `git diff` adds in that file, which is a different reading of the same fact. Executed by a probe that wrote no record and was deleted.

**The merge of `release/v0.21.0` after #837 squashed in as 279a580b.** Two files conflicted, and both items' behaviour stands:

- `skills/code-review/scripts/chain_check.py`: both sides added new functions at the same place, this item's `paths_of` and #837's `notes_of` and `carried_notes`. All three are kept, in that order, and no line of either side changed.
- `tests/test_the_rules_have_one_owner.py`: both items added a rule numbered 17. #837's rule, *a note closes once, at the run's end*, keeps 17, because it reached the release branch first. This item's rule is now 18, with its owner, sentence and carriers unchanged. The guard's docstring and the ledger row S12, S14, S16 now say rule 18. The phase records keep "rule 17", the number the rule had when they were written.

## Not verified

| Item | Who must answer |
|---|---|
| ✅ `questions.md` Q3: the Windows leg's git emits `git grep -n -z` as `<rev>:<path>\0<line>\0<text>\n`, and `ls-tree -z` and `log --name-status -z` as measured on macOS; S10 and the three `-z` readers have run on macOS only | round 1's record: PR #878's Windows shards ran the changed modules on git 2.55.0.windows.5 with no failure among them and no skip on S10 |
| the full suite, the repository-wide lint and the typecheck over this branch | the sealer, once, after the review rounds settle |

## Not done

- `survivor_check.py#corrected` over a hand-typed `--range` holding a merge reads the merged side's sentences as the range's. CI hands it `origin/<base>...HEAD`, where a merge of the base adds nothing, so only the hand-typed form is exposed. `spec.md` §*Out* leaves it out and asks the orchestrator to open an issue for the repository owner; round 1's record names #877 as holding that case.
- `chain_check.py#added_on_branch` and `written_late`'s reading of a merge's first parent, `correction_check.py`'s first-parent fallback, and the three `ls-tree` readers becoming one are left to #529, #836 and #867, and #866 and #867, as `spec.md` §*Out* says.
- #835's registry does not exist on this branch. `own_commits` states its input class in `spec.md` §*The input class of each reader this changes*, and its row joins the registry where that lands first.

## Fed back into the spec

None written into `spec.md`, which is the framer's. Its only edit here is the checker's `NAME NOT IN TREE` marker on the line naming `walk_tip`. Three readings were *inferred during implementation* and stand in the divergence table above, for a planner to overturn: `touched` as the own commits' paths that the range's end carries, `own_units` mapping a unit to the commits that wrote it and how, and `-I` beside `-z` in `call_sites`.
