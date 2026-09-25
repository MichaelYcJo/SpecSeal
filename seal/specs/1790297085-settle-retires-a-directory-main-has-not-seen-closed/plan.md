# Implementation Plan: settle refuses a retirement the release's base has not seen closed; a missing sibling exits 2; the gatherer refuses a fragment's own `## ` line

<!-- seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/plan.md
The approval line is written by the orchestrating session when it spawns
`smith`; the framer leaves it out on purpose. -->

Approved 2026-09-25 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

Three instrument fixes, one phase each, smallest first. Phase 1 makes three
loaders refuse a missing sibling at exit 2 with a sentence, and discharges the
`# RIDER:` that asked for it. Phase 2 makes `settle --retire` ask the rule
arm's predicate of the merge base of `--released-at` and `HEAD` as well as of
the tree, so a closure that has reached the release branch and not `main` no
longer lets its directory go in the same release. Phase 3 makes the changelog
gatherer refuse a fragment carrying a line that starts `## `.

`chain_check.py` is not edited by any phase (`spec.md` §Scope item 1 has the
measurement), so the merge with work item A after it squashes touches no
file this work item edits.

## Technical context

**Phase 1 — the loaders.**
- `skills/settle/scripts/fold_check.py#load` takes `(path, name, purpose)`
  and raises `SystemExit(<sentence>)` (exit 1). Its callers: `#reader` and
  the `hooks/optin.py` load (grep `load(` in the file).
- `skills/settle/scripts/settle.py#load` takes `(path, name)` with one
  sentence for every file ("it is where the fold record is read from"),
  which is false for `OPTIN`. Give it `fold_check.py`'s `purpose` parameter;
  its callers are `open_rows`, `survey`, `retire` (all `READER`) and `main`
  (`OPTIN`).
- `skills/code-review/scripts/round_record.py#load` and the `# RIDER:` above
  it. `chain = load(CHAIN, "specseal_chain_check")` must stay a module-level
  assignment after the floor guard —
  `tests/test_a_script_says_which_interpreter_it_needs.py#test_the_guard_precedes_every_other_module_level_act`
  reads the AST for exactly that. Rewrite the module docstring's exit
  paragraph, which today says "a sibling script that will not load is 1" and
  argues why; it becomes 2, under the *input was unusable, nothing read,
  nothing written* clause.
- The shape to copy is `.github/scripts/rider_check.py#load_checker`:
  `os.path.isfile` first, the sentence to stderr, `raise SystemExit(2)`.
  Keep the `spec is None` branch at 2 as well.
- Stale sentences the fix makes false, corrected in the same phase:
  `settle.py#load`'s docstring (*the rider … is still waiting for somebody
  to fix*), the docstring of
  `tests/test_settle_reads_before_it_removes.py#test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback`,
  and `.github/scripts/rider_check.py#load_checker`'s docstring (*That shape
  is `round_record.py`'s own open rider*).
- Cases that change: the settle case above asserts on `str(raised.value)`,
  which becomes `2`; it moves to `capsys` or a subprocess.
  `tests/test_a_folded_statement_names_what_enforces_it.py#test_a_script_copied_on_its_own_says_which_sibling_it_misses`
  asserts `!= 0`; tighten to `== 2`.
- Who reads these exits: `skills/verify/scripts/broad_gate.py` (around the
  `seal_record` call) reads `round_record.py seal`'s code as `!= 0`, and no
  caller in `skills/`, `hooks/` or `.github/` reads `== 1` from the three
  (framer's grep, 2026-09-25). Re-grep before closing the phase.

**Phase 2 — `settle` and the base.**
- `skills/settle/scripts/settle.py#survey` classifies a released spec-less
  directory with `reader.retired_by_rule(root, None, directory)`, and
  `#retire` re-asks the same of the tree. Both gain the second question,
  `reader.retired_by_rule(root, base, directory)`, where `base` is
  `reader.merge_base(root, ref)` — the revision both CI readers use
  (`unverified_check.py#main` around `base = merge_base(root, args.baseline)`,
  `chain_check.py#main` around `fork = reader.merge_base(root, args.baseline)`).
  Name it with `reader.base_label(ref, reader.commit_of(root, ref), base)`.
- Order matters: a directory the tree already keeps (an open row on disk)
  stays under *kept by the rule* as today; only one that passes the tree and
  fails the base takes the new state. Its rows are
  `reader.open_record_rows(root, base, directory)`; where that is empty (the
  directory is absent at the base, or the base's history wrote a spec), the
  output says the rule does not hold at the base rather than printing no
  reason — the shape `write_rule_kept` already has for its empty case.
- `survey` computes the base once and carries it in the dict it returns;
  `retire` takes it from there, as it takes `released`, and asks the
  predicate itself. `tests/test_settle_reads_before_it_removes.py#run` calls
  `settle.survey(repo, "HEAD")` and `settle.retire(found, repo, out=…)`, so
  the signature of `retire` does not have to change.
- `merge_base` returning None is exit 2 in both arms, in `main`, beside the
  existing `--released-at … does not resolve` refusal.
- The report's heading constants sit at `settle.py#RULE_HEADING` and
  `#RULE_KEPT_HEADING`. `RULE_KEPT_HEADING` says "in a pull request merged
  before the one that retires the directory"; the test
  `#test_a_closed_row_is_told_to_merge_before_its_directory_goes` pins that
  substring in the report, the skill and `docs/the-evidence-ledger.md`.
  Keep the substring and add *to the branch the release merges to*, so the
  pin still holds and the sentence stops being short of the rule.
- Documents: `skills/settle/SKILL.md` §1 (*Close it in a pull request of its
  own…* — now enforced, and name the base) and its command table's
  `--released-at` line; `docs/the-evidence-ledger.md`'s rule-arm statement
  (add the new case to its `Enforced by:` line — `fold-check` reads that
  line's shape); `README.md` and `README.ko.md`'s `settle [--retire]` row,
  one clause each. `docs/one-root-by-lifetime.md`'s decision row already says
  *asked of the merge base* and becomes true; do not edit it.

**Phase 3 — the gatherer.**
- `.github/scripts/gather_changelog.py#main`, after `missing` is computed and
  before the `--version` arm writes or prints anything. The predicate is the
  one the two release readers end a section with: `line.startswith("## ")`
  (`#insert`) and `^## ` (`publish_release_note.py#section_body`). Not a
  markdown heading rule — a `## ` line inside a fence ends the section for
  both readers, so it is refused too.
- Refuse among the fragments this run would write (`missing`), not every
  fragment on disk: one already gathered is in the file, and refusing a
  release over it leaves no remedy but editing shipped prose.
- The refusal names each fragment path, the 1-based line number and the
  line, and the remedy (demote it to `###` or lower in a pull request into
  the release branch, then gather again). Exit 1, `CHANGELOG.md` untouched.
  The module docstring's exit list gains the cause.
- Documents: `docs/branch-and-release.md` §*The changelog entries arrive as
  fragments…* gets the rule and the reason (the released section ends at
  the next `## ` for the gatherer and the release note alike);
  `CONTRIBUTING.md` §*House rules*, *A change writes a fragment, never a
  shared registry*, gets one clause, because that is where a session writing
  a fragment meets the convention.

**Ledger rows whose anchored unit a phase edits** — re-read in place, a
dated `Re-read` note, `Corrected <date>` first where the edit made the claim
false (`CLAUDE.md` §*a change writes fragments*). Framer's list from a grep
on 2026-09-25; `evidence-check` after each phase is the authority:
- Phase 1: `seal/releases/0.15.3.md` G1 (`skills/settle/scripts/fold_check.py#load`).
- Phase 2: `seal/releases/0.13.0.md` S4 (`settle.py#retire`), and
  `settle.py#main` wherever cited; `seal/releases/0.14.0.md` G3
  (`#retire`) and D3 (`#survey`, `#retire`, `#RULE_KEPT_HEADING` if edited).
- Phase 3: rows citing `gather_changelog.py#main` (`seal/releases/0.13.0.md`
  S2, `seal/releases/0.15.0.md` P3) and `#fragments` if it is edited
  (`seal/releases/0.4.0.md`, `seal/releases/0.5.0.md`).
New claims go to `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md`.

**What breaks in six months.** `settle` reads `origin/main` as the clone
last fetched it. A stale ref keeps directories whose closure has in fact
reached `main` — the safe direction, since nothing is removed that CI would
refuse — and the refusal names the ref and the merge-base commit, so the
reader can see it is old and fetch. A repository whose release merges to
another branch already has to pass `--released-at`, and the same flag now
also sets the base, so there is no second value to keep in step.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #602: ask the predicate at the merge base of `--released-at` and `HEAD` | A stale `origin/main` keeps more than it must, and says which ref it read | **Chosen.** It is the revision both CI readers compare against, so `settle` and CI cannot disagree about one tree |
| #602: ask it at the tip of `--released-at` | The base moved past the fork (a hotfix merged the closure straight to `main`); `settle` retires, the release pull request's CI asks the merge base, finds the row open, and goes red — #602 again | Rejected |
| #602: a new `--base REF` flag | Two flags naming one branch invite two values; `SKILL.md` already defines `--released-at` as the branch the release merges to | Rejected |
| #602: read the pull request's base from GitHub | A fold runs before its pull request exists, and `settle` works offline | Rejected |
| #602: leave it in the skill's prose | The 0.15.3 run followed the prose on both pull requests and still cost #597 | Rejected — the state #602 was filed against |
| #590: a new exit code for *sibling missing* | A third meaning for every caller to learn, where each script's 2 already says *unusable, nothing done* | Rejected |
| #590: catch in `main`, as `chain_check.py` does | `round_record.py` loads its sibling at import, before `main` exists; #590 asks for the loaders | Rejected for the three; `chain_check.py`'s catch is left as it is |
| #586: (a) the gatherer refuses the fragment | The refusal arrives at release preparation, not at the fragment's own pull request | **Chosen by the owner** |
| #586: also refuse in `--check`, or a suite case over every fragment in the tree | Catches it earlier, and is a new gate in a release that adds none | Out — `questions.md` Q3 |
| #586: demote the line to `###` automatically | Rewrites a person's prose with nobody reading the result | Rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #590: `fold_check.py#load`, `settle.py#load` (with a per-file purpose) and `round_record.py#load` refuse a missing sibling at exit 2 with a sentence naming the path and its purpose; the `# RIDER:` on `round_record.py#load` is removed and the three sentences calling it open are corrected; one parametrized case runs each of the four scripts copied alone (`chain_check.py` included, pinning its existing 2); the two existing cases are updated; the loaders' module docstrings say 2; changelog paragraph and ledger rows written | The new case red against the pre-phase code for three scripts and green for `chain_check.py`, then green for all four (spec S1, S2); `tests/test_settle_reads_before_it_removes.py`, `tests/test_a_folded_statement_names_what_enforces_it.py`, `tests/test_a_script_says_which_interpreter_it_needs.py`, `tests/test_a_rider_reaches_its_file.py` green; S3's grep empty | 3c1be03a |
| 2 | #602: `settle` asks the rule arm's predicate of the merge base of `--released-at` and `HEAD`; a directory closed on the branch and open at the base is kept at exit 1 under its own heading naming the base and the rows open there; no merge base is exit 2; `SKILL.md`, `docs/the-evidence-ledger.md`, both READMEs and the module docstring say so; changelog paragraph and ledger rows written | Spec S4–S8 as cases in `tests/test_settle_reads_before_it_removes.py`, S4 and S5 seen red first; the module and `tests/test_a_folded_statement_names_what_enforces_it.py` green; `./bin/settle` on this repository read, not `--retire` | |
| 3 | #586: `gather_changelog.py --version` (and `--dry-run`) refuses an ungathered fragment carrying a line that starts `## `, naming the path, line number and line and the remedy, exit 1, nothing written; the docstring's exit list, `docs/branch-and-release.md` and `CONTRIBUTING.md` say so; changelog paragraph and ledger rows written | Spec S9 and S10 as cases in `tests/test_the_changelog_is_gathered_at_release.py`, S9 seen red first; that module and `tests/test_a_release_publishes_its_note.py` green; `gather_changelog.py --dry-run --version 0.15.4` on this repository read | |

The suite, lint and typecheck are not run by any phase: the sealer's broad
gate runs once after the review rounds settle (`agent-contract` §2).

## Operational impact

- No migration, no new environment variable, no new dependency.
- `settle --retire` may now keep a directory it used to remove. That is the
  point; the output says why and when it will go.
- Three shipped scripts change a documented exit code, 1 to 2, for a copy
  missing its sibling. A caller reading exit 1 as *problems found* now reads
  2 as *could not run*. Measured: no caller in this repository reads `== 1`
  from them.
- `skills/` changes, so the release that ships this moves the plugin
  version; release preparation does that, not this branch.
