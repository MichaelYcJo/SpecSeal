# Implementation Plan: every record has one home, and a released ledger file never changes

<!-- seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/plan.md
     The decisions D1–D8, the scenarios S1–S15 and the classes are in spec.md;
     this file says in what order they are built and how each phase is shown. -->

Approved 2026-10-03 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

From the release this ships in, a branch writes one ledger file of its own: its fragment. A re-read or a correction of a released row becomes a citing row in that fragment.

- `evidence-check` reads a released row together with the rows that cite it. A coordinate is OK when any reading recorded its current hash, and a correction supersedes the row it cites.
- `--reverify --into` writes the citing rows.
- `correction-check` refuses a changed released file for work cut after the rule, and reports a dropped correction.
- The fold stops being able to write an old file.

Then the rules move. The ledger and fragment rules each get one home, every other carrier becomes a link, and a layout document indexes where every kind of record lives.

## Technical context

**What this builds on.** These are units opened at 233f0455. The full list is in spec.md §*Data & interfaces*.

- **`evidence_check.py#check_text` classifies coordinate occurrences, not rows.** It deduplicates on `(coordinate, hash)` per file, so phase 1 has to introduce a row view first. The reader already has `#ledger_table_rows` and `#grounds_cells`.
- **The citation needs no new grammar.** `ANCHOR_RE` already accepts `path#"major">"minor"@hash`. `#text_regions` gives a markdown heading its section, and `#minor_region` → `#literal_statements` narrows to the one line holding the literal.
- **`#reverify` splices hashes in place across every ledger it reads.** Phase 2 adds the second writer beside it, without rewriting it.
- **`correction_check.py` already lists the three addresses at each revision** (`#ledger_listing`), so the freeze arm reuses that listing. Its row identity (`#rows`, `#standing`) reads a first cell and an anchor set, and a `Corrected ·` row is identified by its citation, which never changes.
- **`fold_ledger.py#split` and its helpers** (`#release_sections`, `#body_rows`, `#rewrite_self_anchors`) are removed whole. `#insert` keeps the join.
- **`hooks/config.py#config_rows` is the one reader of `seal/config.md`.**

**Constraints.**

- `tests/test_a_row_points_by_content.py#test_the_checker_asks_git_for_nothing` holds `evidence-check` to no git call. The config row is a file read.
- The release files are not edited by this branch (S12).
- Fixtures use `example.com` and `/Users/x/` only (`tests/test_no_real_identifiers.py`).
- Probes and cases that commit drive git from Python (contract §8).

**What breaks in six months, for the chosen approach.**

1. **A family grows one row per re-read.** A popular row such as `agents/smith.md#"## Phases"` carries rows from many releases, so it collects a citing row at every release that edits that unit. That is growth by one line per reading, where today's cost is one conflict per pair of branches. When it matters, a later work item can write a `Corrected ·` row that restates the claim and starts a clean family. Nothing has to change in the checker for that.
2. **Cutoff exemptions outlive their branches.** A work item below the cutoff that is reopened in some later release would still be read under the old rule. The cutoff can be lowered to `0` at any time once no such branch is open (spec D5).
3. **Pre-rule in-place edits drift a citation.** If somebody hand-edits a released row in place under an exemption, a citation to it drifts. That is loud, not silent, and the repair is one in-place re-stamp in a fragment.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Citing rows in the fragment, a family union, released files frozen, a config cutoff** | Families grow one row per reading; a stale exemption; a pre-rule in-place edit drifts a citation (above) | **chosen** |
| Re-read keyed by coordinate (`X@old → X@new`), no row identity | One re-read vouches for every row citing X, including rows nobody opened. That widens the defect the `seal/follow-up.md` row about unread re-stamps already reports | rejected |
| The newest re-read of a row wins, by date or by position | Two parallel branches re-read one row on the same day, and nothing orders them across a squash. A whole-row snapshot also drops the other side's coordinate, so two branches touching different units of one row always leave it DRIFTED | rejected |
| A row id (`0.15.1#N1`) as the citation, as the issue sketches it | `0.15.1.md` has two different `N1` rows (lines 26 and 100 at 233f0455), and 325 of 1,084 rows carry no label at all | rejected |
| Migrating the 37 release files into topic files under `seal/ledger/` | Rewrites every file #647, #716 and #718 re-stamp, so all three conflict at their squash. It also breaks every content citation into a moved file | rejected |
| No fold: fragments stay one per work item forever | The best size unit, but it removes the boundary *a fragment present means not shipped*, which `settle`, `unverified-check` and `chain-check` read. That rework does not fit under the cap | rejected for this work. D8 leaves the size question answered by the section |
| A merge driver for ledger files | It would need to understand what a row claims. #424 rejected it for that reason, and nothing has changed | rejected |
| Enforcing the freeze from the first pull request after landing, with no cutoff | Turns #647, #716 and #718 red at their own pull requests for edits that were correct when they were cut | rejected |
| Grandfathering by whether the merge base contains the rule | Each sibling merges the release branch in when another squashes first, which moves its merge base past the rule and loses the exemption mid-run | rejected |
| Making the freeze universal for every repository using the plugin | Changes what `--reverify` does in every installed repository, and nobody there has `--into`'s fragment convention. Opt-in by the config row changes nothing for them | rejected |

## Phases

Each phase is a vertical slice that ends green on its own narrow run. The re-reads this branch owes for its own edits are written with phase 2's tool from phase 2 on. Phase 1's drift is re-read at phase 2's end. Every new case is seen red first, and the phase record says how (contract §15).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `evidence-check` reads citing rows. Family union (D3), supersession by `Corrected ·`, the citation checked as a coordinate, and three refusals named: a citation into a fragment, a citing row without a marker, a citation whose row is gone. Docstring and `--help` say what a citing row is. Scenarios S1–S4 | a new module, e.g. `tests/test_a_released_row_is_read_again_in_a_fragment.py`, run alone; each case red against 233f0455's `evidence_check.py`; `tests/test_evidence_check.py` and `tests/test_a_row_points_by_content.py` run as the touched modules  ee6d49a5 |
| 2 | `--reverify --into <fragment> --checked <date>` (D4). The refusals under `Ledger frozen from`, the row added to `seal/config.md` and documented in `templates/config.md`, and `hooks/evidence-advisor.py`'s repair text. This branch's own drifted rows re-read into `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` with the new tool, each row read first. Scenarios S5 and S15 | the phase-1 module extended for S5, with sha256 equality of every released file; `tests/test_dispatch.py` and `tests/test_gates_do_not_fail_open.py` for the advisor; `evidence-check --strict .` exit status read directly (contract §1)  b6f1c578 |
| 3 | `correction-check`: a dropped `Corrected ·` citing row is a loss, and the freeze arm with the cutoff, the exemptions and the one-line report (D5). The box-3 cases. Scenarios S6–S10 | new cases in `tests/test_a_merge_cannot_silently_drop_a_correction.py` for S8–S10, and a two-branch module (or the phase-1 module) for S6 and S7, driven from Python; S6 red with 233f0455's in-place `--reverify`; S7 red against a newest-wins variant  fe253c4f |
| 4 | The fold and `settle` (D6). `--split` removed with its cases, `--version` older than the newest release file refused, the fold-branch fragment `seal/ledger/<unix-seconds>-fold.md`, `skills/settle/SKILL.md` §*What a fold branch owes*, `settle.py`'s per-row guidance, and `docs/release-checklist.md` §2's `--split` lines and paragraph. Scenario S11; measurement M1 | `tests/test_the_ledger_fragments_fold_at_release.py` and `tests/test_settle_reads_before_it_removes.py` run; the refusal red first; M1's probe answer recorded in the phase record | |
| 5 | `docs/the-record-layout.md` (D8). Every kind of record with its home, size target and index, the per-place index tables, the D7 cut, and F1–F4 marked as not built, each with the issue the orchestrator files. Scenario S13 | `tests/test_docs_line_wrap.py`, the `docs/` ceiling case (`tests/test_a_document_has_room_for_the_next_fold.py`) and `tests/test_both_editions_carry_the_same_folds.py` run; the warden reads it against S13 | |
| 6 | One home for the ledger and fragment rules (box 5, bounded). `docs/the-evidence-ledger.md` restated as the home: re-reads and corrections go into the fragment, families, a released file never changes, and the conflict section narrowed to a fragment two stacked branches share. Every carrier in spec §*The classes, enumerated* reduced to a link naming the home's path and section, `seal/ledger.md`'s header in one hunk (S12). The pins enumerated (W2) moved from *two copies agree* to *the home states it and the links do not restate it*, and the new one-home case. Scenario S14 | the new case red with one needle restored into `CLAUDE.md`; every adjusted test module run; `.github/scripts/claude_block.py --check` (the generated block above the house rules must not move) | |

The closing work, after phase 6, belongs to whoever builds. It is not a phase:

- `seal/specs/<id>/changelog.md`;
- the fragment's rows for D2–D6's claims;
- `overview.md` with `## Not verified`.

The broad gate is the sealer's.

This table is also where the work records how far it got. There is no separate task list: a list of tasks is mutable progress, and a stale one asserts a state that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused, and so is `done`. Both can be typed without anything having happened, and both assert a present state that nobody can check. A commit hash asserts a past state that someone can open.

**Re-read the column after any rebase**, or it names commits that resolve in one clone and nowhere else.

## Operational impact

- **This repository** gains one `seal/config.md` row (`Ledger frozen from | 1790993141`). From the release that ships this, a branch writes no released ledger file, and a re-read costs one `--reverify --into` command instead of a conflict.
- **Another repository using the plugin** sees no change unless it adds that row. The checker's new reading is inert where no citing row exists, and `--reverify` without the row behaves as it did.
- **No new dependency, no new environment variable, no migration.** `fold_ledger.py --split` disappears. It was a one-time command that already exited 1.
- **For the three sibling branches:** spec §*How a branch cut before this one stays valid*.
