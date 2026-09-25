# 1790297085-settle-retires-a-directory-main-has-not-seen-closed — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | cac3341f |
| Ran by | unknown — the spawn prompt named no value; the orchestrator fills this row |

## What this phase was asked

#602. `settle` asks the rule arm's predicate of the merge base of
`--released-at` and `HEAD` as well as of the tree. A directory closed on the
branch and open at the base is kept at exit 1, under its own heading naming
the base and the rows open there; the report never lists it under *retired
by the rule*. No merge base is exit 2 in both arms. `SKILL.md`,
`docs/the-evidence-ledger.md`, both READMEs and the module docstring say so.
Spec S4–S8 as cases, S4 and S5 seen red first; `./bin/settle` on this
repository read, not `--retire`. Answer `questions.md` Q2 where the phase
meets it. The marker arm is not changed.

## What this phase found

- **The frame holds.** `unverified_check.py#merge_base`, `#base_label` and
  `#commit_of` are what the plan named, and `retired_by_rule(root, base, …)`
  answers the base without a change to the reader.
- **A survey with no base carries no classification at all.** `survey`
  returns `{"base": None, "base_label": None}` the moment `merge_base`
  answers None, before any directory is classified, because the predicate
  asked of `None` is asked of the working tree — the one answer this phase
  removes. `main` refuses that dict at exit 2. `retire` refuses it too, at 2
  and with a line on its own output, so a caller that skips `main` cannot
  reach `shutil.rmtree` with the tree's answer alone; that guard has its own
  case, `test_the_retirement_refuses_a_survey_with_no_base`.
- **The tree is asked first, so the old state keeps its heading.** A
  directory with a row open on disk stays under *kept by the rule*, whose
  remedy is to close the row. Only one that passes the tree and fails the
  base takes the new heading, *kept until the closure reaches <base>*, whose
  remedy is to merge the closure there. `write_rule_kept` gained a `base`
  argument for the new heading's lines, and for a directory absent at the
  base, which prints why rather than no reason.
- **The report's summary line names the base.** `no spec.md: N to retire by
  the rule, N kept by it, N kept until the closure reaches <base>`. The pinned
  substring `0 to retire by the rule` is unchanged.
- **Q2's answer: no.** None of the 111 cases that stood before this phase
  expected a directory retired while its closure sat only in the working
  tree. `moment()` commits every overview it writes, and the fixture runs at
  `HEAD`, so the base holds the closure in every one of them. All 111 are
  green unchanged. Written into `questions.md`.
- **`./bin/settle` on this repository**, read and not `--retire`, at
  `4f77ecdc`: exit 0; `no spec.md: 3 to retire by the rule, 0 kept by it,
  0 kept until the closure reaches origin/main`. The three are the
  directories #597 kept in 0.15.3; their closures reached `main` with that
  release, so the base now agrees with the tree.
- **Seen red (§15).** Against the code at `ee3afefc`, with only the cases
  added: S4 and S5 red with the directory removed and exit 0; S7 red with the
  directory listed under *retired by the rule*; S8 red at exit 0 (report) and
  1 (`--retire`); the heading pin red on the missing constant; S6, the
  counter-case, green. After the change the module is 118 passed.
  Mutations at `4f77ecdc`, each restored from the bytes read before it and
  each red: `survey` asking the tree where it asks the base (1),
  `retire` doing the same (2), `retire` not counting the directories it kept
  there (2), the report omitting the heading (1), `main`'s refusal off (2),
  `survey` walking on with no base (2), the rows' text dropped from the kept
  lines (5), the heading's remedy dropped (1), `RULE_KEPT_HEADING` losing
  *to the branch the release merges to* (1), and one deletion each of the
  skill's paragraph, the policy's sentence and the clause in each README (1
  each). `retire`'s own no-base guard off turned its case red at `cac3341f`.
- **Verified by (executed, 2026-09-25):** 53 test modules in one `bin/test`
  call — every one that names `settle.py`, `skills/settle`,
  `the-evidence-ledger` or a README, and every one that globs `docs/` or
  lists the tree. 2536 passed, 8 skipped, 2 failed: this work item had no
  `overview.md` yet, which a spec directory owes, and `phase-1.md` quoted
  the bare anchor it was describing, which the records check resolves. Both
  are fixed in `4f77ecdc`, and those two modules with
  `tests/test_unverified_rows_close.py` re-ran at 293 passed. After the
  last edit, the settle module with `test_docs_line_wrap.py`,
  `test_a_folded_statement_names_what_enforces_it.py`,
  `test_a_document_has_room_for_the_next_fold.py` and
  `test_both_editions_carry_the_same_folds.py`: 225 passed; the settle
  module alone after `cac3341f`: 120 passed. `ruff check` and
  `ruff format --check` clean on both changed Python files.
- **Ledger.** Six rows anchor units this phase edited, and each was re-read
  against the edit and re-stamped in its own file:
  `seal/releases/0.13.0.md` S4 (`#retire`), R1 and R2 (`#main`), and
  `seal/releases/0.14.0.md` G3 (`#retire`), D3 (`#survey`, `#retire`,
  `#RULE_KEPT_HEADING`) and G7 (`#main`). D3's claim named two headings and
  there are three, so it was corrected in place with a
  `Corrected 2026-09-25` note; the other five hold and gained a
  `Re-read 2026-09-25` note. New claims are M2 and M3 in the fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
