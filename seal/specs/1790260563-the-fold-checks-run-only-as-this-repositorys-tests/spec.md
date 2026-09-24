# Feature Specification: the fold checks run only as this repository's tests

Three items, one branch: #566 (the folded-statement shape check and the
per-document line ceiling become a plugin command), #530 (`settle` labels a
blockquoted or listed anchored row by its `>` or `-`), and the wrap limit that
leaves an `Enforced by:` line no room in a covered document (no issue yet;
observed in PR #581's fold on 2026-09-24).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/settle/SKILL.md` §*2. Write one standing statement per segment* | Owns the statement shape and the placement rule. Today it says the plugin "ships no checker for the shape" and "sets no ceiling; the repository states its value and the check that holds it". This work changes the first sentence and keeps the second: the plugin now ships the checker, and still sets no value |
| `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion* | States this repository's three values in prose (cutoff `1790154761`, ceiling 1000, the empty over-ceiling list), and its two `Enforced by:` lines name `tests/…::bound` and `tests/…::ceiling_problems`, which this work moves |
| `templates/config.md` (top, and §*Broad gate*) | The one place a repository states a value a plugin command reads: `\| Item \| Value \|` rows, every absent row having a default that is what repositories got before the row existed. The new rows follow it |
| `hooks/config.py#config_rows` | The one reader of that table. A second walk is what its docstring exists to prevent, so the new command loads it by path as `broad_gate.py#broad_command` does |
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs, the one that runs unattended wins. A value a fold session has to retype from prose on every run is the one that stops |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | Changelog entry → `seal/specs/<id>/changelog.md`; ledger rows → `seal/ledger/<id>.md` |
| `CONTRIBUTING.md` §*House rules* | Both READMEs move together, so the command's row lands in `README.md` and `README.ko.md` |
| `skills/agent-contract/SKILL.md` §12 | #530 is a class (whatever container syntax stands before the first pipe), and round 3's paste-ready fix covers five single tokens of it, not the class |

## Scope

**In.**

1. **A new command, `fold-check`**, shipped as
   `skills/settle/scripts/fold_check.py` with `bin/fold-check` and
   `bin/fold-check.cmd`. It runs both checks over the top level of `docs/`:
   - the **shape check** — every statement whose marker group holds an id at
     or above the repository's cutoff opens with a bold rule sentence and
     carries exactly one `Enforced by:` line whose targets resolve;
   - the **line ceiling** — every top-level `docs/*.md` is at or under the
     repository's ceiling, or is listed as over it with its markers frozen.

   The logic is what the two test modules hold today, moved, not rewritten:
   `statements`, `bound`, `target_problem`, `shape_problems`, `markers`,
   `marker_digest`, `ceiling_problems`. Their messages are pinned as they
   stand; a changed message is a §14 change and is pinned anew.
2. **The repository's values reach the command as three `seal/config.md`
   rows**, read through `hooks/config.py#config_rows`:

   | Row | Value | Absent |
   |---|---|---|
   | `Fold shape from` | a work-item id's epoch prefix; `0` binds every statement | the shape is not checked, and the command says so |
   | `Document line ceiling` | a positive integer | no ceiling is checked, and the command says so |
   | `Over the ceiling` | `none`, or `;`-separated entries `<path> frozen at <n> markers <12-hex digest> until <home>` | no document is listed |

   Flags `--shape-from`, `--ceiling` override the rows for one run, which is
   how #565 lists every statement it still has to retrofit
   (`fold-check --shape-from 0`) without editing the config first.
   This repository's `seal/config.md` gains `Fold shape from | 1790154761`,
   `Document line ceiling | 1000` and `Over the ceiling | none`.
3. **The two test modules keep their names and become this repository's
   pins over the shipped command.** Each loads `fold_check.py`, runs it over
   this tree with the values its `seal/config.md` holds, and keeps every
   planted-tree case (now calling the shipped functions). The prose pin
   (`test_the_evidence_ledger_states_the_values_these_constants_hold`) reads
   the three values from `seal/config.md` instead of from module constants,
   so the prose, the config and the check are one set of numbers.
   `SHAPE_CUTOFF`, `LINE_CEILING`, `OVER_CEILING` and `FROZEN_IDS_DIGEST`
   stop being constants; a third copy of each value is what the pin would
   otherwise have to hold equal.
4. **The documents that describe it**: `skills/settle/SKILL.md` §2 (the
   plugin ships the checker, sets no value, and the repository states its
   values as rows) and §*What a fold branch owes* (a clean `fold-check`
   where either row is declared), `docs/release-checklist.md` §*2b* (run it
   after the prose is written and before `settle --retire`),
   `templates/config.md` (a section for the three rows),
   `skills/config/SKILL.md` §*Procedure* 1 (the row table), both READMEs
   (one cheat-sheet row), and `docs/the-evidence-ledger.md` (the two
   `Enforced by:` lines re-pointed to `skills/settle/scripts/fold_check.py`,
   and the sentence that says the check pins the constants).
5. **#530.** `skills/settle/scripts/settle.py#first_cell` drops a prefix
   before the first pipe when that prefix is container syntax only: any run
   of blockquote markers (`>`), bullet markers (`-`, `*`, `+`), ordered-list
   markers (`1.`, `1)`) and the comment opener (`<!--`), in any combination
   and with or without whitespace between them. A prefix that holds anything
   else is left as it is today.
6. **The wrap exemption.** `tests/test_docs_line_wrap.py#prose_lines` skips
   a line the shipped reader reads as a statement's `Enforced by:` line with
   targets, and nothing else. It asks `fold_check.py` which lines those are,
   rather than spelling a second pattern, the way the marker skip is spelled
   from `unverified_check.py#FOLD_MARKER`. A `nothing — <why>` line is not
   skipped: its reason is prose and can continue on the next line, which the
   shape check already allows.

**Out, and why.**

- **Either `open_rows`** (`settle.py#open_rows`,
  `.github/scripts/fold_ledger.py#open_rows`). The parallel chain for #487
  (work item `1790260566-a-row-inside-a-fence-reads-as-live`) edits both.
  `first_cell` sits in the same file, so that chain merges the release branch
  in after this one squashes.
- **The 101 statements folded before the cutoff** (#565). This work ships
  what that item runs; it adds no `Enforced by:` line to any statement.
- **Wiring `fold-check` into `broad-gate`, `settle`, or a CI workflow.** In
  this repository the two test modules already run it on every pull request
  through the suite. A second invocation adds a run, not a check. A gate
  under `hooks/` or `.github/workflows/` would also carry `CONTRIBUTING.md`
  §*What a change to a gate must carry*, which nothing here needs.
- **Letting an `Enforced by:` line wrap and joining it in the reader.**
  Measured (executed, 2026-09-24): 3,232 of the 3,490 `path::test` pairs in
  `tests/` exceed 88 columns as a single target after the 13-column prefix.
  Wrapping between targets does not fit a line that holds one, so a join
  still needs the exemption, and adds a continuation grammar to §2's
  *exactly one line* besides.
- **Any document other than the top level of `docs/`.** That is where a fold
  writes (`docs/the-evidence-ledger.md` §*The fold reads the top level of
  `docs/` and no deeper*), and both checks already read exactly that.
- **`agents/smith.md`, `agents/scribe.md`** and the other files outside
  `COVERED`. The exemption changes what a covered file may hold; it adds no
  file to the list.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | Given this repository at the branch head, when `fold-check` runs with no arguments, then it reads `Fold shape from` 1790154761 and `Document line ceiling` 1000 from `seal/config.md`, reports no problem, and exits 0, printing how many statements it read and how many the cutoff binds | executed: `bin/fold-check; echo $?` |
| S2 | Given a planted tree whose bound statement has no `Enforced by:` line, a missing target, or two lines, when `fold-check` runs, then it names each with the messages the test module pins today and exits 1 | the planted cases in `tests/test_a_folded_statement_names_what_enforces_it.py`, now calling the shipped functions, and one CLI case for the exit code |
| S3 | Given a planted `docs/` document one line over the ceiling and not listed, when `fold-check` runs, then it names the document with today's message and exits 1 | `tests/test_a_document_has_room_for_the_next_fold.py` planted cases, plus one CLI case |
| S4 | Given a root whose `config.md` has neither fold row, when `fold-check` runs, then it checks nothing, says in its output that neither value is declared and so nothing was checked, and exits 0 | a planted-root CLI case; the output line is pinned (§14) |
| S5 | Given a row whose value will not parse (a ceiling of `ten`, a cutoff with letters, an `Over the ceiling` entry out of shape), when `fold-check` runs, then it names the row and the value and exits 2 with nothing checked | planted-root CLI cases, one per row |
| S6 | Given `--shape-from 0`, when `fold-check` runs on this repository, then every statement is bound and the problems listed are exactly the statements #565 has to retrofit; exit 1 | executed on this tree; a planted case with one old statement |
| S7 | Given a COVERED document holding `Enforced by: <a target wider than 88 columns>` inside a statement, when the wrap test reads it, then the line is skipped; and the line directly after it is still prose | a case in `tests/test_docs_line_wrap.py`, seen red against today's `prose_lines` |
| S8 | Given `Enforced by: nothing — <a long reason>` wider than 88 columns, or an `Enforced by:` line outside any statement, when the wrap test reads it, then the line is still prose and is reported | a case in `tests/test_docs_line_wrap.py` |
| S9 | Given anchored ledger rows written `> \| claim \| … \|`, `- \| claim \|`, `> - \| claim \|`, `1. \| claim \|`, `<!-- \| claim \|` and `>\| claim \|`, when `settle` names them, then each is labelled `claim`; and a row whose text before the first pipe is prose keeps today's label | cases in `tests/test_settle_reads_before_it_removes.py`, each seen red against today's `first_cell` except the comment opener and the prose case, which are green before and after |
| S10 | Given the two test modules, when a value is changed in `seal/config.md` alone, or in the evidence-ledger prose alone, then the prose pin fails | the pin case, seen red by editing one side |
| S11 | Given the command's README row, then both editions carry it, and every document naming the script says how to reach it | `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py` and the README pair checks, run narrow |

## Data & interfaces

**Command.** `fold-check [--root DIR] [--shape-from ID] [--ceiling N]`.
Exit 0: nothing found, including the case where nothing is declared. Exit 1:
at least one problem, each on its own line. Exit 2: the root or a row is
unusable; nothing was checked. The root is resolved the way
`broad_gate.py` resolves it (`<repo>/seal/`, else the common git directory's
`seal/`); a repository with no root at either place has no `config.md`, and
the flags alone decide what is checked.

**Rows.** Three, added to `templates/config.md` and to
`skills/config/SKILL.md`'s row table. `Over the ceiling`'s entry shape is
fixed here because a person writes it and the command parses it:

```
docs/big.md frozen at 29 markers 0123456789ab until owner/repo#1
```

The digest is `marker_digest` of the file, printed by the command itself
when the count or the ids disagree, so a person never computes it by hand.

**Functions `fold_check.py` exposes**, which the two test modules and the
wrap test call: `statements`, `bound(ids, cutoff)`, `target_problem`,
`shape_problems(root, name, text, cutoff)`, `markers`, `marker_digest`,
`ceiling_problems(root, ceiling, over, digests)`, and
`enforced_lines(text)` — the 1-based numbers of the lines the shape reader
reads as a statement's `Enforced by:` line with targets. `bound` and
`shape_problems` take the cutoff as a parameter where today they read a
module constant.

**What #565 can rely on**, stacked on this branch:

- `fold-check --shape-from 0` lists every statement still missing the shape,
  with the same messages the bound ones get. That is its worklist.
- An `Enforced by:` line with targets may be any width in a COVERED
  document, so a `path::test` target needs no rewording to fit.
- The cutoff is one row, `Fold shape from`, and the evidence-ledger prose
  pin reads it from there. Lowering it to `0` when the retrofit is done is a
  one-row edit plus the prose sentence, and the pin fails until both agree.
- `Enforced by:` targets are checked for resolution only, never for whether
  they enforce the rule; that stays review's.

**Ledger rows this work reaches** (read 2026-09-24; `seal/ledger/` is
empty, and no row anchors `settle.py#first_cell`):

| Row | Its anchors this work moves | What `CLAUDE.md` requires |
|---|---|---|
| `seal/releases/0.14.0.md`, S1 (the shape) | `tests/test_a_folded_statement_names_what_enforces_it.py#SHAPE_CUTOFF`, `#statements`, `#HEADING`, `#BOLD_OPENING`, `#target_problem`, `#shape_problems` | the anchors go, so the row is REMOVED from that file, and the claim is written anew against `fold_check.py` in `seal/ledger/<this id>.md` |
| `seal/releases/0.14.0.md`, P1 (the ceiling) | `tests/test_a_document_has_room_for_the_next_fold.py#LINE_CEILING`, `#OVER_CEILING`, `#ceiling_problems`, `#FROZEN_IDS_DIGEST`, `#marker_digest` | the same |
| `seal/releases/0.15.1.md`, S1 (no document over the ceiling) | `#OVER_CEILING`, `#FROZEN_IDS_DIGEST`, and the prose pin case, which this work edits | the same; the new claim names the config row and the pin |
| `seal/releases/0.13.1.md` (a fold marker cannot be wrapped) | `tests/test_docs_line_wrap.py#prose_lines`, which this work edits | drifts; re-read against the edit, still true, re-stamped with a dated `Re-read` note |

Every other row the edits drift is found by `bin/evidence-check .` after
them, not by this list. `settle §2` and the evidence-ledger section are
anchored by the rows above and may be anchored by others.

**Issue to file for item 6.** No issue exists. Suggested title: *fix: an
`Enforced by:` line in a covered document has room for one short target,
because the wrap limit skips a fold marker and not the line that names what
enforces it.* Body: the measurement in §Scope *Out*, the four COVERED
documents whose `Enforced by:` lines sit at 75 to 82 columns (executed
2026-09-24: `docs/the-evidence-ledger.md` 82, 76, 75; `docs/release-checklist.md`
82, 80; `docs/the-agent-set.md` 81; `docs/the-broad-gate.md` 70), against
206, 180 and 171 in `docs/review-chain-spec.md` and
`docs/round-record-spec.md`, which are not covered. It is fixed by this work
item, so this branch's pull request is what closes the issue.

## Open questions → questions.md

Framed 2026-09-24 by framer, before the build.
