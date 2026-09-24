# Implementation Plan: the fold checks run only as this repository's tests

Approved 2026-09-24 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned. The wrap item is #583.

## Summary

Move the two checks out of `tests/` into a shipped script,
`skills/settle/scripts/fold_check.py`, reachable as `fold-check`. The
repository's values reach it as three `seal/config.md` rows. The two test
modules stay, under the same names, as this repository's pins over the
shipped script. Beside that, `settle`'s `first_cell` learns the whole class
of container syntax that can stand before a row's first pipe. The wrap test
skips exactly the `Enforced by:` lines the shipped reader reads.

## Technical context

- **What moves, and from where.**
  `tests/test_a_folded_statement_names_what_enforces_it.py#statements`,
  `#bound`, `#target_problem`, `#shape_problems`, `#HEADING`,
  `#BOLD_OPENING`, `#ENFORCED`, `#NOTHING`; and
  `tests/test_a_document_has_room_for_the_next_fold.py#markers`,
  `#marker_digest`, `#documents`, `#ceiling_problems`. Both modules already
  load `skills/verify/scripts/unverified_check.py` by path for `live_lines`
  and `FOLD_MARKER`; the shipped script does the same.
- **How a command reads a config row.**
  `skills/verify/scripts/broad_gate.py#broad_command` loads
  `hooks/config.py` by path and walks `config_rows`, and `#seal_home`
  resolves the root at either place. Copy the shape, not the code: a second
  table walk is what `hooks/config.py`'s docstring forbids, and a second
  root resolver is a copy `agent-contract` §16 already names.
- **How a command ships.** `bin/settle` and `bin/settle.cmd` are the pair to
  model. `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`
  requires the pair, the `.cmd` twin and the executable bit for any script a
  shipped document names. `settle.py`'s comment block over `AnchoredRow`
  (read, not run) says every shipped script carries the interpreter-floor
  guard copied from `round_record.py#below_floor` and compiles under 3.9;
  `tests/test_a_script_says_which_interpreter_it_needs.py` pins the number.
- **`first_cell`** is `skills/settle/scripts/settle.py#first_cell`. Its only
  caller is `#anchored_rows`. The parallel #487 chain edits `#open_rows` in
  the same file and merges the release branch in after this one squashes.
- **The wrap skip** is `tests/test_docs_line_wrap.py#prose_lines`. Its
  marker skip is spelled from the reader's own constant, and its comment
  says why: a skip wider than the reader leaves unwrapped lines nobody
  checks.

**Failure scenario of the chosen approach, six months on.** A repository
deletes its `Fold shape from` row while tidying `seal/config.md`. The
command then checks no shape, says so in one line, and exits 0; CI stays
green. In this repository the pin fails, because it reads the row and
compares it with the evidence-ledger prose. Another repository has only the
printed line. That is the cost of an absent row meaning *not declared*,
which is what every other optional row in `templates/config.md` means. The
alternative, refusing on an absent row the way `Broad gate` does, would make
every repository that never folds fail a command it never asked for.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `settle --check`, a mode of the existing command | `settle` refuses local mode and needs a released ref (`settle.py` module docstring, exit 2's five states); a check over `docs/` needs neither and would inherit refusals that have nothing to do with it. It also puts the whole change into the file the #487 chain edits | rejected |
| Two commands, one per check | Both read the same corpus at the same moment of a fold, and two README rows describe one act | rejected |
| Flags only; the repository's values live in its tests or its CI | Every fold session retypes the values from prose. In another repository they sit in workflow YAML, where no pin can hold them against the prose that states them. `CLAUDE.md` §*The goal* prefers the design that does not stop for a person | rejected; kept as a per-run override |
| Parse the values from the policy prose, as the pin does today | The regex is this repository's sentence. Another repository's sentence does not match, and a rewording here silently turns the check off | rejected |
| **Three `seal/config.md` rows, flags override per run** | The absent-row silence above | **chosen** |
| Keep `SHAPE_CUTOFF`, `LINE_CEILING`, `OVER_CEILING` as test constants beside the rows | A third copy of each value, and a pin whose only job is holding the copies equal | rejected · NAME NOT IN TREE |
| Drop the over-ceiling listing from the command | This tree's CLI and this tree's test could disagree the day a document is listed, and the test docstring records the intent to keep the listing for the next document a fold takes past the ceiling before it can be split | rejected |
| Round 3's paste-ready `first_cell` (five single prefixes) | Misses `> - \|`, `> > \|`, `1. \|`, `>\|`. A paste-ready fix carrying a defect is how one class was closed three times (`agent-contract` §12) | rejected; the class is the fix |
| Let an `Enforced by:` line wrap and join it in the reader | 3,232 of 3,490 single `path::test` targets overflow 88 columns alone (executed 2026-09-24), so the join still needs the skip, and adds a continuation grammar to §2's *exactly one line* | rejected |
| Several `Enforced by:` lines, one target each | Contradicts §2's *exactly one line*, which the shape check counts | rejected |
| Skip every line that starts `Enforced by: ` | Wider than the reader: a line outside any statement, or a `nothing — <why>` whose reason is prose, would go unchecked | rejected; the skip asks the reader |

## Phases

Each phase leaves the tree green for the modules it names. None runs the
full suite; that is the sealer's single run after the review rounds settle.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#530.** `first_cell` drops a prefix before the first pipe when that prefix is container syntax only (`>`, `-`, `*`, `+`, `1.`, `1)`, `<!--`, in any combination, spaced or not). A prefix holding anything else is kept as today | New cases in `tests/test_settle_reads_before_it_removes.py` for `> \|`, `- \|`, `> - \|`, `> > \|`, `1. \|`, `>\|`, each seen red against today's `first_cell` (§15); the comment-opener and prose-prefix cases green before and after. That module run narrow | 2e7ed5c7 |
| 2 | **The shipped script, flag-driven.** `skills/settle/scripts/fold_check.py` holds the moved functions, `bound` and `shape_problems` taking the cutoff as a parameter, plus `enforced_lines(text)` and a CLI with `--root`, `--shape-from`, `--ceiling`, exits 0/1/2, and the floor guard. `bin/fold-check` + `.cmd`, executable. Both test modules import from it; their planted cases stay, unchanged in what they assert. The two `Enforced by:` lines in `docs/the-evidence-ledger.md` re-point to `skills/settle/scripts/fold_check.py::bound` and `::ceiling_problems`. The three release-file rows whose anchors left `tests/` are REMOVED there and written anew in `seal/ledger/1790260563-the-fold-checks-run-only-as-this-repositorys-tests.md` | Both test modules, the interpreter-floor module and `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`, narrow. `bin/fold-check --shape-from 1790154761 --ceiling 1000; echo $?` is 0 on this tree. One CLI case per exit code over a planted root. `bin/evidence-check .` shows no BROKEN row | b8d01f79 |
| 3 | **The values as rows.** `Fold shape from`, `Document line ceiling`, `Over the ceiling` read through `hooks/config.py#config_rows` from the resolved root; an absent row prints that nothing was checked for it; an unparseable value exits 2 naming the row. This repository's `seal/config.md` carries the three. The prose pin reads the rows, and the constants go. `templates/config.md` gains the section, `skills/config/SKILL.md`'s table the three rows | Planted-root cases for S4 and S5, each message pinned (§14). The prose pin seen red by editing the config value alone, then the prose alone (S10). `bin/fold-check; echo $?` is 0 with no flags. `tests/test_the_rules_have_one_owner.py` and the config-template modules that pin `templates/config.md`, narrow | 0f4c6f4d |
| 4 | **The wrap skip.** `prose_lines` skips the lines `fold_check.enforced_lines` returns, and only those | New cases for S7 (seen red against today's `prose_lines`) and S8 (green before and after, which is the point: it pins the width of the skip). `tests/test_docs_line_wrap.py`, narrow. The `seal/releases/0.13.1.md` row re-read and re-stamped | 0c18fab6 |
| 5 | **What describes it.** `skills/settle/SKILL.md` §2 and §*What a fold branch owes*; `docs/release-checklist.md` §*2b*; the cheat-sheet row in `README.md` and `README.ko.md`; the evidence-ledger sentence about what the check pins; the changelog fragment `seal/specs/<this id>/changelog.md` | `test_settle_owns_the_shape_rule` updated to the new §2 sentence and seen red against the old one; the README-pair and wrap modules; the script-reach module; `bin/evidence-check .`, with each drifted row re-read and re-stamped | |

This table is also where the work records how far it got. Status is empty,
or the commit that closed the phase. What a phase finds that the next one
needs goes to `phases/phase-N.md`, from `templates/sdd-phase.md`.

**Order.** 1 stands alone and can go first or last. 2 before 3 (3 reads
rows into the functions 2 moved). 2 before 4 (4 asks the function 2 adds).
5 last, because it describes what 2 to 4 built.

**What #565 can rely on when it stacks on this branch** is listed in
`spec.md` §*Data & interfaces*. In short: `fold-check --shape-from 0` is its
worklist, a `path::test` target needs no rewording to fit a covered
document, and lowering the cutoff is one row plus one prose sentence, held
together by the pin.

## Operational impact

- **A new command on the Bash PATH**, `fold-check`, through the plugin's
  `bin/`. Nothing calls it on its own.
- **Three optional rows** in `seal/config.md`. Absent, a repository sees no
  change in any gate or command.
- **This repository's `seal/config.md` gains three rows.** Its test suite
  now depends on them: deleting one fails the prose pin.
- No migration, no new dependency, no environment variable, no hook or
  workflow change.
