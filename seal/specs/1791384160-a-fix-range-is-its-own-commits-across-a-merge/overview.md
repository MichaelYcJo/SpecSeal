# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md`, `handoff.md`, `routing.md` of this item; `docs/the-record-layout.md` §*A commit after the build brings its changelog fragment along* and §*A change writes fragments, never a shared file*; `docs/round-record-spec.md` §*The fix range*, §*The fix surface*, §*The depth in `New units`*, §*A fix of a fix*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `skills/code-review/orchestration.md` §*And name the fix surface, in the same record*; `templates/sdd-phase.md`, `templates/sdd-overview.md`; `seal/config.md`
· evidence: `seal/ledger/1791384160-a-fix-range-is-its-own-commits-across-a-merge.md` — 9 new claims (S1–S10, S12, `unit_adders`), 5 `Corrected ·` rows (0.18.3 `S1, S5, S8, S10` and `S2, S3, S4, S6`, 0.19.0 `A1`, 0.16.0 `G9`), the rest `Re-read ·` rows written by `evidence-check --reverify --into`
· verified: executed — each phase's modules (`phases/phase-N.md`), every new case seen red, every new unit broken by `bin/mutation-check`, `bin/evidence-check --strict` at exit 0, the real range of #860 measured; read — the released rows each re-read cites; unverified — the rows below

## Why this work exists

Two readers of a range walked it by its shape and read a sibling's work, brought in by a merge, as the work item's own. Both now read the commits that descend from the range's start, so `New units`, `Contract changes`, `Fix of a fix` and the fragment notice name what the item wrote.

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
| where a sibling's commit sits | `spec.md` §*In*: "A sibling's commit … descends from `a` never" / true for every start these readers take, not for a start at the fork point | spec, with the home stating descent only | every start here is on the branch after the build; the probe that started at the fork point listed a base commit as owned (`phases/phase-1.md`) |

**Measured on #860's own range, after the build.** `99bcad40..092004bb` resolves in this clone. Its 5 own commits are 856aeeec, 56e98860, bab19faa, d6faf419 and 092004bb. `touched` reads 9 paths where the two ends' diff lists 74. In those 9 paths, `measure` finds 13 units added between the ends, and the per-unit filter keeps 2, both in `tests/test_the_seal_is_taken_once_by_the_sealer.py`. Over the two ends' `.py` paths, the reading before this work finds 113 added units; the record it wrote named 111, one per name. `spec.md`'s 22 was a count of top-level names `git diff` adds in that file, which is a different reading of the same fact. Executed by a probe that wrote no record and was deleted.

## Not verified

| Item | Who must answer |
|---|---|
| `questions.md` Q3: the Windows leg's git emits `git grep -n -z` as `<rev>:<path>\0<line>\0<text>\n`, and `ls-tree -z` and `log --name-status -z` as measured on macOS; S10 and the three `-z` readers have run on macOS only | the pull request's CI run on the Windows shards, read by the orchestrator |
| the full suite, the repository-wide lint and the typecheck over this branch | the sealer, once, after the review rounds settle |

## Not done

- `survivor_check.py#corrected` over a hand-typed `--range` holding a merge reads the merged side's sentences as the range's. CI hands it `origin/<base>...HEAD`, where a merge of the base adds nothing, so only the hand-typed form is exposed. `spec.md` §*Out* leaves it out and asks the orchestrator to open an issue for the repository owner. That issue is still to file.
- `chain_check.py#added_on_branch` and `written_late`'s reading of a merge's first parent, `correction_check.py`'s first-parent fallback, and the three `ls-tree` readers becoming one are left to #529, #836 and #867, and #866 and #867, as `spec.md` §*Out* says.
- #835's registry does not exist on this branch. `own_commits` states its input class in `spec.md` §*The input class of each reader this changes*, and its row joins the registry where that lands first.

## Fed back into the spec

None written into `spec.md`, which is the framer's. Its only edit here is the checker's `NAME NOT IN TREE` marker on the line naming `walk_tip`. Three readings were *inferred during implementation* and stand in the divergence table above, for a planner to overturn: `touched` as the own commits' paths that the range's end carries, `own_units` mapping a unit to the commits that wrote it and how, and `-I` beside `-z` in `call_sites`.
