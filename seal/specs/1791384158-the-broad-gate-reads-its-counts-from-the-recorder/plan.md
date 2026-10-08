# Implementation Plan: the broad gate reads its counts and the stop reason from its recorder, and the stamp's dead scale dial is retired (#869, #852, #853)

<!-- seal/specs/1791384158-the-broad-gate-reads-its-counts-from-the-recorder/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

Six phases. The first three are one chain: the recorder writes two more
facts and one more outcome, the gate's reader and words read them, and the
counts on the panel, on the failure form and on the release seal come from
that reader. The fourth retires the scale and makes a malformed chart a
refusal; it touches the same two files and is independent of the chain. The
fifth and sixth close the records. Every phase ends with a narrow run of the
modules it touched; the broad gate is the sealer's.

## Technical context

The coordinates are `spec.md` §*Read by this frame*. What the chosen
approach rests on, and what breaks it in six months:

- **The category is pytest's, obtained the way the terminal reporter obtains
  it.** The recorder calls the teststatus hook from its own
  `pytest_runtest_logreport` with `report` and `config`, as
  `_pytest/terminal.py` :625–636 does. What breaks it: a pytest that changes
  the hook's signature or its `firstresult` contract. The hook has carried
  `(report, config)` since pytest 3 and the recorder reads only names it has
  had since 6.1, which Q-M1 holds to the three builds #849 measured on.
- **The stop is read off the session and the keyboard-interrupt hook, not
  the exit code.** `session.shouldfail` and `session.shouldstop` are the
  session's own attributes; their setters refuse to unset them
  (`_pytest/main.py` :646–676), so a value seen at session end is the value
  that stopped the run. What breaks it: a stop a plugin raises as its own
  exception type rather than through the flags or `pytest.exit()` — that one
  reaches `wrap_session`'s `except BaseException` as exit 3 and the exit net
  still catches it. The one stop neither sees is named (`spec.md` Scope 2).
- **The counts refuse an unread line.** A keyed record is the recorder's
  own file; a line in it that is not a JSON object was written by something
  else or cut by a death the `end` line already shows. What breaks it: a
  row whose test deliberately writes well-formed lines into the keyed record
  — rule 3's named limit, unchanged.
- **The release seal loads the gate's module by path.** `release_seal.py`
  already loads three tree modules that way (`readers`), and `broad_gate.py`
  at import runs its interpreter floor (3.12; the `seal` job runs 3.12) and
  nothing else. What breaks it: a `broad_gate.py` that grows an import-time
  side effect; the release job then says `no seal` with the reason and exits
  0, which is its contract.
- **The scale's retirement leaves one window, in this repository.** The
  installed hook's `read_values` of 0.20.0 refuses a file with no `scale`
  and leaves it pending; the owner's plugin update ends the window and the
  next `Stop` draws the file. What breaks it: nothing — the file is never
  lost, and `bin/seal-stamp --from` draws it on demand.
- **`load` refuses what it cannot import.** The exception's own sentence is
  what the person reads, so `CHART_MALFORMED` reaches them with the path.
  What breaks it: an exception whose `str()` is empty; the refusal then
  names the path and the exception's type, which is still a sentence.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. The recorder writes pytest's own category per report; the gate counts lines | A plugin's category outside pytest's list is printed after the list in first-seen order, which a reader may not expect | **chosen.** One judgment, pytest's, imported by calling its hook; the gate copies no rule |
| A2. The gate derives the category from `outcome`, `when` and `wasxfail` | A copy of `runner.py`'s and `skipping.py`'s rule that drifts when theirs does — strict xfail already turns an xpass into `failed` in pytest and would read `xpassed` here | rejected: #834's rule against a copy of a judgment that has a reader |
| A3. Keep `COUNTS_RE` as a fallback where the record has no session | Two mechanisms for one number, the guess kept alive under a condition; the decoy of S1 prints through it | rejected: where there is no record the row reads `exit <n>`, which is observed |
| B. The stop reason is observed: the keyboard-interrupt hook and the session's two flags, written on the `end` line; the exit code stays as the net | A `pytest.exit()` from a later `pytest_sessionfinish` hook is after the `end` line and unseen | **chosen.** Closes both of #852's limits with one list on a line the gate already reads; the net keeps every exit 0.20.0 refused |
| B2. The exit code alone, the two limits named (today) | The limits stay; #852 says settle it | rejected: the hooks exist on every build the recorder supports (Q-M1 measures) |
| B3. Read pytest's printed `!!! stopping after N failures !!!` or `Interrupted:` lines | A guess from text the row does not own, the kind #825 removed | rejected |
| C. An unread line refuses the counts and demotes `new`; the verdicts kept | A record with one stray line loses its panel counts for that run | **chosen.** Mirrors `unplaced` and `unended` exactly: one count, one line on the form, one `new?` reason |
| C2. A keyed record with an unread line is no record (`sessions` 0) | Every file reads `NO_RECORD`, whose sentence names three causes that are not this one | rejected: a wrong sentence with a checker's authority |
| C3. Ignore it (today) | A count nothing reads | rejected by #869 |
| D. `load` turns an import failure into `Refused` with the sibling's sentence | A sibling that raises `SystemExit` at import (the floor) is not an `Exception` and keeps its own exit, which is right | **chosen.** One change at the one loader; `main` loads the stamp before parsing, so nothing runs |
| D2. Defer `read_chart` to a cached function the gate asks before the run | Every importer fails at draw time unless each adds the ask; three call sites for one file | rejected: the import-time read is what fails fast |
| E. Retire the scale whole; `read_values` ignores `scale`; the gate writes none | The one window named in `spec.md` Scope 5, in this repository only | **chosen.** #853's ask, and `build` already says the scale sizes nothing |
| E2. Keep writing `"scale": 0.9` for one release, with a rider to remove it | The dead dial #853 retires, written on every seal for a release, and a rider somebody has to meet | rejected |
| E3. Keep the band and state why | The only reader of the band is the refusal of itself; `#832`'s plan put the retirement out of its scope, not out of reach | rejected: #853 names the cost (a reader told about a dial that changes nothing) |
| F. The release seal reads the record through the gate's reader and counter | The seal job's step has to set four variables by hand; a variable mistyped reads as no record, which is `no seal` with the reason | **chosen.** One counter for the panel and the release; the JUnit reader goes |
| F2. Keep the JUnit reader | Two mechanisms for one number, which is #869's complaint | rejected |
| F3. The release seal reads a gate run's values file | A release has no gate run; the seal is taken at the tag by CI | rejected |
| G. `warnings` and `deselected` off the panel | A row run with `-k` shows no `deselected` where pytest's line would | **chosen.** Not a report's category; the owner's row (decision 6) names passed and skipped |
| G2. Two more hooks record them | Two more readers for two numbers nobody asked for | rejected; a line in `questions.md`'s decided list says where they would go |

## Phases

Vertical slices — each phase ends with something runnable and verified.
Narrow runs name the module; the broad gate is the sealer's and no phase runs
it (contract §2). A new case is shown red before it is committed and the
phase record says how (contract §15). Ledger rows are drafted as each phase
settles them and written to `seal/ledger/1791384158-the-broad-gate-reads-its-counts-from-the-recorder.md` at the phase boundary.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The recorder writes the category, the skipped collection and the stop; the reader reads them.** First act: Q-M1 on pytest 6.1, 7.0 and 9.1 (xdist 3.8 on 9.1), through `uvx --with pytest==<v>` as #849 round 2 and #825's Q-M1 ran. Then `specseal_pytest_record.py`: the teststatus call in `pytest_runtest_logreport` writing `category`; `pytest_collectreport` writing `failed` and `skipped`; a keyboard-interrupt hook on `Recorder` remembering `excinfo`'s type name, message and return code; `pytest_sessionfinish` writing `stopped` from that and from `session.shouldfail`/`session.shouldstop`; the docstring's *What it writes* rewritten. `broad_gate.py`: `RunRecord.unread` and `counts`; `read_record` reading `category`, the `collect` outcome and `stopped`, counting `unread` per keyed file after the key check, `unended` by Scope 2's rule; `suite_counts(record)` beside the text form, which phase 3 removes. Cases: S4, S5 (recorder half), S6 (`read_record` half), S7–S10 (recorder and `read_record` halves); the `"kind": "end"` fixtures gain `stopped: []` | `bin/test tests/test_the_recorder_writes_what_its_process_ran.py`; `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -k "record or unended or RECORD_LINES"`; each new case red at 5623d728 (the recorder without the fields, the reader without the rule); `bin/mutation-check` or `bin/arm-check` red on each new arm; `phases/phase-1.md` carries Q-M1's table (build × stop × what the `end` line said) | 67cf7fb5 |
| 2 | **The gate's words and the sentences a person reads.** `base_word`: the unread reason after `UNENDED_AT_BASE`; `failure_lines`: the unread line; `UNENDED_AT_BASE` and `UNENDED_HERE` naming a stop pytest made; `RAN_TO_ITS_END`'s comment rewritten with #852's two corrections and Q-M1's words; rule 3's two sentences replaced by one clause; the **New?** bullet; the two rule-3 pins and the sentence cases moved in the same commits. Cases: S6 (gate half), S7–S8 end to end at the base (the `CRASHES_ITS_WORKER` shape of #849's S1 with `pytest.exit` and `-x` in its place), S11 | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -k "base_word or unended or unread or rule or limits"`; `bin/test tests/test_no_passage_is_pasted_into_a_second_file.py tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`; each sentence pin red with its sentence deleted | 8229c227 |
| 3 | **The counts come from the record.** `gate` reads the head record once after the suite arm and hands it to `failure_lines` and `panel`; `panel` and `failure_lines` call `suite_counts(record)`; the no-record line on the form; `COUNTS_RE`, the text `suite_counts` and `NO_SUMMARY` retired; `agents/sealer.md` :131–133; the registry row in `tests/test_every_reader_ends_a_line_where_gfm_does.py`; the copy of `NO_SUMMARY` in `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`. Cases: S1 (with the decoy), S2, S3; the cases at :1924–1933, :3493–3540, :3670–3690, :4351–4380, :5907–5929 re-aimed or retired (Q-W1) | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_gate_hands_cmd_a_path_it_can_run.py tests/test_every_reader_ends_a_line_where_gfm_does.py`; S1's decoy case red at 5623d728; `grep -rn 'COUNTS_RE\|NO_SUMMARY' skills tests agents` returns history only | 2f2590b8 |
| 4 | **The release seal reads the record.** `publish-release.yml`'s suite step sets the four variables and drops `--junitxml`; `release_seal.py` loads `broad_gate.py` through `module`, reads the record under `SUITE_RECORDS` with `SUITE_KEY`, refuses as Scope 4 says, and the JUnit `suite_counts` goes; `docs/release-checklist.md` :352–359. Cases: S12 | `bin/test tests/test_the_release_seal_is_drawn.py tests/test_a_release_publishes_its_note.py`; `DRY_RUN=1 python3 .github/scripts/release_seal.py` over a record a local `bin/test` run wrote with the four variables set (executed once by the smith, output in the phase record); the re-aimed refusal cases red at 5623d728 | 22c40aaf |
| 5 | **The scale retired, the chart refused.** `seal_stamp.py`, `broad_gate.py`, `hooks/sealer-stamp.py`, `docs/the-broad-gate.md` as `spec.md` Scope 5 lists; `load` as Scope 6. Before the first edit: capture `seal-stamp --shape` and the block form at 5623d728 over `SAMPLE_ROWS` to a fixture, for the byte-for-byte case. Cases: S13, S14; the parametrised scale cases collapsed and the five retired (Q-W3); the `read_values` tolerance pair | `bin/test tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py tests/test_the_seal_is_taken_once_by_the_sealer.py -k "stamp or disc or scale or ladder or values or chart or load"`; `bin/test tests/test_docs_line_wrap.py tests/test_a_corrected_sentence_survives_elsewhere.py`; S14's case red at 5623d728 (exit 1 and a traceback); `grep -rn 'scale' skills/verify hooks docs/the-broad-gate.md agents` clean of the stamp's | af54c461 |
| 6 | **The records close.** `changelog.md` (three entries: the counts and the refusals under #869, the stop under #852, the scale under #853); the ledger fragment's own rows for S1–S14; `evidence-check --reverify --into seal/ledger/1791384158-the-broad-gate-reads-its-counts-from-the-recorder.md --checked <date>` for the drifted released rows, and `Corrected ·` rows for the list in `spec.md` S15 (Q-W2); `overview.md` with its divergence rows and `## Not verified` (the one window of Scope 5, answered by the owner's first seal after updating the plugin); every `phases/phase-N.md` in place | `bin/evidence-check --strict .` (the ledger arm alone, narrow); `bin/test tests/test_a_record_states_what_the_tree_has.py tests/test_no_real_identifiers.py tests/test_every_reader_ends_a_line_where_gfm_does.py tests/test_one_word_one_meaning.py tests/test_a_question_says_who_can_answer_it.py`; the fragment read once against S15's list | 455c42c2 |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Seams with the sibling frames of 0.21.0

Eleven frames run in parallel on branches cut from the same tip; the brief
names the overlaps. The units this item changes, so the build can be
sequenced:

- `skills/verify/scripts/broad_gate.py`: `COUNTS_RE`, `load`, `RunRecord`,
  `read_record`, `RAN_TO_ITS_END`, `base_word`, `UNENDED_AT_BASE`,
  `suite_counts`, `panel` (the `suite` row only), `failure_lines`,
  `UNENDED_HERE`, `NO_SUMMARY`, `gate` (the head record's read; the
  `check_scale` lines; the `stamp.stamp` call), `signal`, `main`
  (`--scale`), and the module docstring's usage lines.
- `skills/verify/scripts/pytest_record/specseal_pytest_record.py`: the
  `Recorder` class and the module docstring.
- `skills/verify/scripts/seal_stamp.py`, `hooks/sealer-stamp.py`,
  `.github/scripts/release_seal.py`, `.github/workflows/publish-release.yml`.
- `templates/config.md` rule 3, `skills/verify/SKILL.md`'s **New?** bullet,
  `docs/the-broad-gate.md` §*Where the stamp is drawn*, `agents/sealer.md`,
  `docs/release-checklist.md`.

**#866 (`broad_gate.py#rounds_rows`, `deferred_home`, the `Needs a fix`
reading).** This item edits `panel`'s `suite` row and leaves the
`rounds_rows(item, record)` call and its neighbours untouched. The two touch
the same file in different units, so the second to land rebases over the
first with no judgment to re-make. Where #866 changes `panel`'s signature or
the `rounds` rows' shape, the cases this item re-aims over the panel's rows
(S1) are rebuilt on its shape, and nothing else of this item depends on it.
`panel`'s 14 and `gate`'s 62 ledger rows drift under both; whichever lands
second re-reads them.

**#836 (a ledger row's claim is the test that enforces it; the reverify
families).** Phase 6 writes about seventy re-read and correction rows with
`--reverify --into` as the checker stands. Where #836 lands first, phase 6
writes them in whatever shape #836's checker then writes, and this plan
changes nothing else.

**#835 (a reader declares its input class).** `spec.md` §*The input class of
every reader this frame adds or changes* is written in the table's columns
so #835's registry can take the rows as they are; this item removes two
`guess` readers (`COUNTS_RE`, `suite_counts` over text) and adds none.

**#867 (`seal/config.md`'s rows have one reader).** Untouched here:
`broad_command` and the row readers are not in this item's unit list.

## Operational impact

- **No new dependency.** The recorder stays stdlib-plus-pytest, 3.8 syntax,
  names pytest has had since 6.1 (Q-M1 holds the three new ones to that).
  `release_seal.py` imports one more tree module by path and no package.
- **The `seal` job's suite step changes.** Four environment variables set
  in the step, `--junitxml` gone; the pins test over the install line is
  unchanged. A mistyped variable reads as no record, and the job then says
  `no seal` with the reason and exits 0, as it does today for a JUnit file
  it cannot read. `SUITE_XML` is read nowhere after this; the checklist's
  by-hand path names `SUITE_RECORDS` and `SUITE_KEY`. <!-- NAME NOT IN TREE -->
- **A `--scale` on either command is refused by argparse** (`unrecognized
  arguments`, exit 2). Nothing in the tree types it: `agents/sealer.md`,
  the skills and both READMEs name no `--scale`, and an installed gate older
  than this change that redirects to the tree's copy hands over only what
  its caller typed.
- **One compatibility window, this repository only** (`spec.md` Scope 5):
  a values file the tree's gate writes before the owner updates the plugin
  is left pending by the installed 0.20.0 hook and drawn after the update,
  or at once with `bin/seal-stamp --from <path>`. `overview.md`'s `## Not
  verified` carries it with the owner as answerer.
- **The record grows by one key per `test` line and one per `end` line**,
  and gains a `collect` line per skipped collection; a 7,000-test run adds
  about 150 KB. Nothing reads the records but the gate and the release
  seal, and they are written under the kept output as before.
- **No migration.** A record is read by the tree that wrote it; a values
  file with or without `scale` draws.
