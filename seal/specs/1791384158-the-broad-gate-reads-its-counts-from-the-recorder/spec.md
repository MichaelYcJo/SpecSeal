# Feature Specification: the broad gate reads its counts and the stop reason from its recorder, and the stamp's dead scale dial is retired (#869, #852, #853)

<!-- seal/specs/1791384158-the-broad-gate-reads-its-counts-from-the-recorder/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three asks, one build, because they share one record and one reader. #869
is #834's inventory applied to the broad gate: four readings still go round
the recorder 0.20.0 gave it, and two of them decide what a person reads on
the stamp and on the failure form. #852 is the one of those four that
needs the recorder to write one more fact, so the inventory said to settle it
here. #853 is a dial on the same stamp that no longer turns anything, left in
place by #832 because retiring it was out of that item's scope, and its only
remaining reader is the refusal of itself.

Every claim below is `read`, at the coordinate it names, at 5623d728
(0.20.0 as shipped, the tip of `release/v0.21.0`) and in the built
environment's pytest 9.1.1 with pytest-xdist 3.8.0. Nothing was executed by
this frame; the rows of `questions.md` marked *a measurement* are the
smith's first act in the phase that needs them.

**The defect, in one sentence.** The record the row's own pytest writes
already holds every outcome, and the gate still reads pytest's printed
summary line for the panel's counts, counts the lines it could not read in
a field nothing reads, cannot tell a session `pytest.exit()` or `-x` stopped
from one that ran to its end, and ends in a traceback rather than a refusal
when the chart file beside the stamp is malformed.

**The direction, from #834.** Prefer the input that is owned or observed
and refuse what is not recognised, over reading one more shape of text.
Name what the change removes. Import a judgment that already has a reader
rather than copying it. The recorder's record is the gate's own format
(owned); what pytest hands a plugin through its hooks is observed; pytest's
printed line is neither, and it goes.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #834's inventory, part 5 (`inventory/5-verify-bin-ci.md` on `origin/chore/834-every-reader-and-record-is-inventoried`): rows 21, 22, 26, 49, 118 and §*Observations* | The grounds. Row 26 classes the panel's counts as a guess; row 21 says `skipped` is counted and never read; row 22 names the two stops that pass as ended; row 49 says `when`, `nodeid` and the rest are written and never read, so the record can carry more than the gate reads; row 118 says `read_chart` raises at import and `load` lets it through. Each was re-read in the code before this frame rested on it (§*Read by this frame*) |
| #869, §*What this asks* | The panel and the failure form read their counts from the recorder, and so does the release seal where it can; a line the recorder cannot read is counted where a reader sees it or refused; a malformed mark file is a refusal |
| #852, body and its comment of 2026-10-07 | Settle whether the stop reason is observed or the limit stays named. **Settled: observed**, from pytest's own hooks and the session's own flags, never from output (§*Scope* 2). The comment's two corrections to `RAN_TO_ITS_END`'s comment are carried into its rewrite (S11) |
| #853, §*What this asks* | Retire the band, `--scale`, the ladder's scale rung and the values file's `scale` field; keep the one-per-`Stop` budget rule. **Retired, all four** (§*Scope* 5). The `scale` a values file written by 0.20.0 carries is read as nothing |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between a count a person compares by hand against `suite.txt` and one the record gives, the record. Between a traceback a person reads and an exit 2 that names the file, the refusal. Nothing here asks anybody anything |
| `templates/config.md` §*Choosing a value — the criterion*, rule 3 | The one home of what the comparison cannot measure. Its two sentences on the stops that pass as ended are removed and replaced by one on what the record now observes (§*What this frame removes*); the pins in `tests/test_the_seal_is_taken_once_by_the_sealer.py` move with it, in the same commit (contract §14) |
| `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare against the base*, the **New?** bullet | Says the same thing as rule 3 in the reader's words, and its clause on the exits a stopped session shows moves with rule 3's |
| `docs/the-broad-gate.md` §*Where the stamp is drawn*, the #717 paragraph | Describes the ladder as *its file's own scale, then 0.90, the one rung with a disc since #832*. Scope 5 ends the scale, so the sentence is corrected in the commit that retires it — `docs/the-broad-gate.md` §*A document that its own work item's fixes disproved is corrected in the same work item* is the rule, and its `Enforced by:` line is kept |
| `docs/the-broad-gate.md` §*One act, one owner* | The sealer judges nothing and hands the words on. The words `new`, `failing on base too` and `new?` are unchanged; two new reasons join the `new?` family and the sealer passes them on unedited as it does the others |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from` | 57 released rows anchor `templates/config.md#"## Broad gate"` and drift when rule 3 moves; they are re-read into this item's fragment with `evidence-check --reverify --into`, and the rows this work makes false are `Corrected ·` rows there (S15 lists them) |
| `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/plan.md` §*Alternatives considered*, the row *Retire `--scale` and the band now that the disc has one size* | *out of scope; a work item of its own if anyone wants it*. This is that work item, and #853 is the owner wanting it |
| `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md`, the owner's decision 6 | The panel's `suite` row is `suite ✓ <n> passed · <m> skipped`. The counts the record gives take that row's shape; the owner's layout names test outcomes and neither warnings nor deselected items, which is why the recorder records neither (§*Scope* 1) |
| `seal/specs/1791327652-a-base-session-that-died-part-way-is-not-read-as-finished/spec.md` §*Grounding* (quoting `CONTRIBUTING.md` §*What a change to a gate must carry*) | The direction every failure of the mechanism falls on: a measurement the gate cannot vouch for reads `new?`, never `new`. A record with a line the reader cannot parse is such a measurement (§*Scope* 3) |
| `seal/specs/1791270161-the-broad-gate-reads-a-record-its-pytest-plugin-wrote/questions.md` Q1 and Q2 | Both stand as built, (a). Nothing here reopens the five-row table, the loading route or the unit of the word |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Each class below is enumerated from the code (`grep` over the tree, named per scope item); every sentence a person reads is pinned in the commit that changes it; every new case is seen red at 5623d728 or with its sentence deleted, and the phase record says how |

## Read by this frame, and what each reading settles

pytest 9.1.1 and pytest-xdist 3.8.0 in the built environment (`.venv` at
the repository root, `bin/test`'s). Line numbers are those builds'.

| # | What was read | What it settles |
|---|---|---|
| R1 | `_pytest/main.py#wrap_session` :317–363: `except (KeyboardInterrupt, exit.Exception)` sets the exit to `INTERRUPTED` or to the `returncode` `pytest.exit()` chose, calls `config.hook.pytest_keyboard_interrupt(excinfo=excinfo)`, and `finally` calls `pytest_sessionfinish` where `initstate >= 2` | A `pytest.exit()` in a test, whatever return code it chose, is **observed** by a plugin implementing the keyboard-interrupt hook, and the recorder's `end` line is still written after it. That is the first of #852's two limits, closed by observation rather than by exit code <!-- NAME NOT IN TREE --> |
| R2 | `_pytest/main.py#pytest_runtestloop` :397–413: after each test, `if session.shouldfail: raise session.Failed(...)`, `if session.shouldstop: raise session.Interrupted(...)`; `Session.pytest_runtest_logreport` :698–705, which `pytest_collectreport` aliases, sets `session.shouldfail = "stopping after N failures"` under `--maxfail` (`-x` is `--maxfail=1`); `Session.pytest_collectstart` :691–695 raises the same two at the next collection's start; both setters :646–676 refuse to unset | Plain `-x` and `--maxfail`, and any plugin's stop, leave `session.shouldfail` or `session.shouldstop` set on the `session` object `pytest_sessionfinish` is handed. **Observed** there, in the hook the recorder already implements. The second of #852's limits closes the same way; and #852's comment holds: a failed collection under `-x` exits 1 only where another collector starts after it (the `pytest_collectstart` raise) and 2 where it was the last (the run loop's `Interrupted` on `testsfailed`) — either way `shouldfail` is set |
| R3 | `xdist/dsession.py` :135–141, :203–211, :418–422: under `-n` the stop flag is `DSession.shouldstop`, raised as `Interrupted` (exit 2) | The xdist stop is on the controller's distributed session, not on `Session`, so the exit-code net keeps it: exit 2 is not in `RAN_TO_ITS_END`, and that stays the second reading. Nothing is lost that 0.20.0 had |
| R4 | `_pytest/hookspec.py#pytest_report_teststatus` :1068 (`firstresult`, `(report, config)` → `(category, letter, word)`); `_pytest/terminal.py#TerminalReporter.pytest_runtest_logreport` :625–636 calls `self.config.hook.pytest_report_teststatus(report=rep, config=self.config)` and counts `rep` under `category` in `self.stats`; `_build_normal_summary_stats_line` :1455–1470 prints `self.stats` in `KNOWN_TYPES` :63 order with `pluralize` :1620 (`error` and `warnings` pluralise, nothing else); `_pytest/runner.py#pytest_report_teststatus` :220–229 (`error` for a failed setup or teardown, `skipped`, else `""`), `_pytest/skipping.py` :315–321 (`xfailed`, `xpassed`) | The category pytest's summary counts a report under is the result of one hook, and the terminal reporter obtains it by calling that hook with the report and the config. A plugin can make the same call from its own `pytest_runtest_logreport`, so the recorder can write pytest's **own** category on each `test` line and the gate counts lines rather than re-deriving the rule. `deselected` and `warnings` are the two entries of `KNOWN_TYPES` no report carries <!-- NAME NOT IN TREE --> |
| R5 | `_pytest/terminal.py#TerminalReporter.pytest_collectreport` :800–804: a failed collect report is counted under `error`, a skipped one under `skipped` | A failed collection is `error` on pytest's line, and a module-level skip is one `skipped`. The recorder writes a `collect` line for both outcomes (today for `failed` only), and the gate counts them the way the terminal does |
| R6 | `skills/verify/scripts/broad_gate.py`: `COUNTS_RE` :344, `suite_counts` :2703–2730, `panel` :3054–3059, `failure_lines` :3145–3147, `NO_SUMMARY` :3193; `read_record` :1966–2040 (`record.skipped` :2010, :2015, counted BEFORE the key check at :2017), `RunRecord` :1884–1918, `RAN_TO_ITS_END` :1944–1963 and its comment, `base_word` :2169–2183, `UNENDED_AT_BASE` :2155, `UNENDED_HERE` :3181; `gate` :3484–3493 (the head record is read only inside the failure loop); `load` :356–363, `stamp_module` :367; `check_scale` call :3381, `--scale` :3770, `signal` :3721 | Every unit §*Scope* names, at the coordinate it changes. Two of the readings the inventory counted are a guess (`COUNTS_RE`, `suite_counts`) and go; `skipped` counts foreign files' lines too, which is a second defect on the same field |
| R7 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py`: `Recorder.pytest_runtest_logreport` :253–266, `pytest_collectreport` :268–281 (`if not report.failed: return`), `pytest_sessionfinish` :283–296 (`kind`, `exitstatus`, `unplaced`), the module docstring's *What it writes* | The owned format this work extends: one key on the `test` line, one on the `end` line, one more outcome on the `collect` line. The docstring is the format's one home and moves with it |
| R8 | `skills/verify/scripts/seal_stamp.py`: `SCALE_FLOOR`/`SCALE_CEILING` :185–186, `DEFAULT_SCALE` :206, `SCALE_LADDER` :250, the three refusal sentences :252–270, `check_scale` :272–288, `build(scale)` :360–379 (*`scale` is checked against the band and sizes nothing*), `compose(rows, scale)` :590–607, `stamp(rows, scale, shape)` :629–635, `admitted` :638–700 (`rungs`, `min(scale, rung)`), `read_values` :907–911 (`scale` must be a number), `main` :1013–1037 (`--scale`), `drawn_from` :1045–1064; `read_chart` :323–354, `CHART = read_chart(CHART_PATH)` :357 | Every reader of the scale, and the one place the chart is read — at import. `build` says in its own docstring that the scale sizes nothing |
| R9 | `hooks/sealer-stamp.py#drawings` :110–150 (`block = (label, rows, scale)`, `stamp(rows, scale, shape=False)`, `except Exception: continue`), `load_stamp` :96–107 (`except (Exception, SystemExit): return None`); the docstring's *One message, held under a budget* | The hook's two readers of `scale`, and its stated shape on every failure: silent, the file left pending. A values file a newer gate writes without `scale` meets an older hook's `read_values` and is left pending until the plugin updates (§*Scope* 5 names the window) |
| R10 | `.github/scripts/release_seal.py#suite_counts` :229–262 (JUnit, raises on a failed or errored suite), `seal_release` :440–444 (`SUITE_XML`), `module` :63–76 (loads a tree module once by path); `.github/workflows/publish-release.yml` :117–138 (`pytest tests/ -q -n auto --junitxml=…`, `SUITE_XML`); `docs/release-checklist.md` :352–359 (the by-hand path names `SUITE_XML`) | The second mechanism for one number, and the one step and two sentences that feed it. `module` already loads tree scripts by path, so `broad_gate.read_record` is one more such load and no new loader |
| R11 | `seal/releases/*.md`: 57 rows anchor `templates/config.md#"## Broad gate"` (counted by `grep`); the rows on units this work changes are listed under S15 with the ones its edits make false | What the close-out owes the ledger, and which rows are corrections rather than re-reads |
| R12 | `tests/`: the pins and cases named per scope item below, found by `grep` over `suite_counts`, `COUNTS_RE`, `NO_SUMMARY`, `.skipped`, `unended`, `UNENDED`, `"kind": "end"`, `scale`, `SCALE_`, `--scale`, `SCALE_LADDER`, `check_scale`, `read_values`, `read_chart`, `junit`, `SUITE_XML`; `tests/test_every_reader_ends_a_line_where_gfm_does.py` :653 registers `suite_counts` as a line reader | Which cases move, which retire, and the one registry row that goes with `suite_counts` |

## Scope

**In.**

1. **The panel's `suite` row and the failure form's suite entry read their
   counts from the head record (#869).** The recorder writes on every
   `test` line the category pytest's own summary counts the report under,
   obtained by calling the teststatus hook with the report and the config
   the way the terminal reporter does (R4); it writes a `collect` line for a
   failed AND a skipped collection, each with its `outcome` (R5). The gate
   counts the keyed sessions' lines — `test` lines by `category`, a failed
   collection as `error`, a skipped one as `skipped` — and prints what
   pytest's line would print without its clock: the categories in pytest's
   order (`failed`, `passed`, `skipped`, `xfailed`, `xpassed`, `error`),
   `error` pluralised as pytest pluralises it, any category outside that
   list after them in first-seen order, and `None` where no session
   carries the key. `deselected` and `warnings` are not recorded: neither
   is a report's category (R4), and the owner's row names test outcomes
   (decision 6). Sessions are summed, so a row running pytest twice shows
   both runs where today it shows the last summary printed. `COUNTS_RE`,
   the text form of `suite_counts` and `NO_SUMMARY` are retired; on the
   failure form, where no session carries the key, one line says no pytest
   the row ran left a record, with the three causes `NO_RECORD_CAUSES`
   already names, in place of the summary-line sentence. The head record
   is read once, after the suite arm, for every outcome of the run — today
   it is read inside the failure loop only. `agents/sealer.md`'s sentence
   on *pytest's counts, or … no pytest summary* follows.
2. **The recorder records why a session stopped, and the gate reads it
   (#852).** The recorder implements the keyboard-interrupt hook (R1) and
   remembers what it was handed — the exception's type name and, for
   `pytest.exit()`, its message and return code — and at session end reads
   `session.shouldfail` and `session.shouldstop` (R2). The `end` line gains
   `stopped`, a list that is empty where nothing stopped the session and
   otherwise holds one entry per observation, each `{"by": …, "what": …}`
   with `by` one of `interrupt`, `exit`, `failures`, `stop` and `what` the
   text pytest gave. A keyed session is `unended` where it has no `end`
   line (as today), where its `end` line's `stopped` is not empty (new), or
   where its `exitstatus` is outside `RAN_TO_ITS_END` (as today; the net for
   what no hook observes — an internal error, a usage error, xdist's
   controller stop (R3), a code a plugin chose). The two limits rule 3
   named are closed: a `pytest.exit` choosing 0, 1 or 5 and a plain `-x` or
   `--maxfail` stop each put an entry in `stopped`. One limit replaces
   them, named in the recorder's docstring and in `RAN_TO_ITS_END`'s comment
   and not in rule 3: a `pytest.exit()` raised by a `pytest_sessionfinish`
   hook that runs after the recorder's is caught by `wrap_session` after the
   `end` line is written (R1 :360–363) and is not seen. `RAN_TO_ITS_END`'s
   comment is rewritten around the new reading and carries #852's two
   corrections: the `-x` sentence states the condition under which a failed
   collection exits 1 rather than 2, and the measurement sentence names
   which exits were measured on which builds, in the words the phase's own
   measurement (Q-M1) gives.
3. **A line the recorder did not write is counted where a reader sees it,
   and the counts are refused (#869).** `RunRecord.skipped` becomes
   `unread`, counted per keyed session and only there — today the count
   runs before the key check (R6), so another run's file counts too, and
   nothing reads the sum. Where a keyed record has an unread line: the
   suite counts are `None` (the panel row reads `exit <n>`, the failure
   form prints no count), the failure form says how many lines under
   `records/` did not parse as the recorder's and were passed over, and a
   file that would read `new` from such a base record reads `new?` naming
   the count, checked after the unended reason. The verdicts the record does
   hold are kept: a `failing on base too` is not demoted. A file whose FIRST
   line does not parse is not keyed and is passed over whole, uncounted, as
   today.
4. **The release seal reads the same record through the gate's reader
   (#869).** `publish-release.yml`'s suite step hands pytest the recorder —
   the four variables `recording_env` sets, spelled out in the step, with
   `SPECSEAL_RECORD_DIR` under `$RUNNER_TEMP` and a key the step chooses —
   and no `--junitxml`. `release_seal.py` loads `broad_gate.py` through its
   own `module` loader (R10), calls `read_record` and the gate's counter,
   and takes `(passed, skipped)` from the record's counts. It refuses, in
   the words it already uses for a JUnit file, a record with no keyed
   session, an unread line, an unended session, or a `failed` or `error`
   count: a `SEALED` above a red or a short suite would be false. `SUITE_XML`
   gives way to the directory and the key; the JUnit reader goes; the
   checklist's by-hand lines name the new variables.
5. **The scale is retired (#853).** `SCALE_FLOOR`, `SCALE_CEILING`,
   `DEFAULT_SCALE`, `SCALE_LADDER`, `SCALE_REFUSED`, `SCALE_NOT_A_NUMBER`,
   `SCALE_TOO_LARGE` and `check_scale` leave `seal_stamp.py`; `build()`
   takes no argument; `compose(rows, disc)` and `stamp(rows, shape, disc)`
   take whether the disc is drawn in place of a scale; `admitted` steps a
   block from *with its disc* to *the text block alone* and keeps the
   owner's rule of 2026-10-02 whole — as many of the oldest blocks as fit
   together with their disc, and one block alone that does not fit is the
   text block with no disc; `fitted` unchanged in meaning; `read_values`
   reads `rows` and the labels and ignores a `scale` key, so a values file
   0.20.0's gate wrote draws, and so does one with no such key;
   `seal-stamp` loses `--scale` and `drawn_from` its argument;
   `broad-gate` loses `--scale`, the `check_scale` call in `gate`, and
   `signal` writes no `scale`; `hooks/sealer-stamp.py` builds `(label,
   rows)` blocks and reads no `scale`; `docs/the-broad-gate.md`'s ladder
   sentences say *with its disc, then without*; the module docstrings,
   `DISC_CELLS`'s comment and `admitted`'s docstring stop saying *at every
   scale*. The window this opens is named rather than hidden: in this
   repository alone, between merging this work and the owner's next plugin
   update, a values file the tree's gate writes meets the installed hook's
   `read_values`, which refuses it for the missing `scale` and leaves it
   pending (R9); the next `Stop` after the update draws it, and
   `bin/seal-stamp --from <path>`, which the `SEALED` line already names,
   draws it at once. Every other repository runs the installed gate and the
   installed hook together, so no window opens there.
6. **A sibling that fails to import is a refusal (#869).** `load` turns an
   exception raised while executing the sibling into `Refused` naming the
   path and carrying the exception's own sentence, so a malformed
   `seal-mark.txt` ends `broad-gate` and `broad-gate --preflight` at exit 2
   with `CHART_MALFORMED`'s sentence and nothing run — `main` loads the stamp
   before it parses arguments, so no check, no worktree and no kept output
   precede the refusal. The read stays at import: every importer fails at
   once rather than at draw time, after the checks ran, which is the shape
   `check_scale`'s NaN history warned about (R8 :274–278). The hook's
   behaviour is unchanged and already correct — `load_stamp` returns `None`
   and nothing is drawn (R9) — and `seal-stamp` on its own is out of scope
   (below).
7. **The records.** The changelog fragment (one entry per issue), this
   item's ledger fragment with its own rows, the re-reads and corrections
   S15 lists, `overview.md`, a `phases/phase-N.md` per phase.

**Out, and why.**

- The `FAILED` fallback (`failing_files`, `FAILED_RE`; inventory row 25).
  #869 does not ask for it, and where no record exists there is no observed
  source for a file name; every file it names already reads `new? not
  measured`. It stays as the labelled guess it is.
- `ledger_counts`, `ledger_total` and `LEDGER_RE` (rows 27–28): a sibling's
  own printed line, classed owned. A second reader of it is #866's family,
  not this one.
- `rounds_rows`, `deferred_home` and the `Needs a fix` reading (rows 36–38):
  #866's. This work edits `panel` beside the call and never the call
  (`plan.md` §*Seams*).
- `not_as_written` and the `cmd.exe` model (rows 15, 17): text predictions
  the inventory names and nobody has asked to replace.
- `seal-stamp` run on its own with a malformed chart: a traceback whose last
  line is `CHART_MALFORMED`'s sentence. It is the repository's developer
  tool, and making it exit 2 means moving the chart's read off import for
  every importer, which Scope 6 gives the reason against.
- `deselected` and `warnings` on the panel: not a report's category (R4),
  not in the owner's row (decision 6). Two more hooks would add them; nobody
  has asked.
- A version field on the record. The recorder and its reader ship together
  (`RECORDER_DIR` is the gate's own directory), and the release seal loads
  the same tree's `broad_gate.py`, so no reader meets a record another
  version wrote.
- The bulk of rule 3: the loading route, the `PYTHONPATH` paragraph, the
  path rule, the three kinds of report left out. This frame removes what
  #852 closes and nothing more (§*What this frame removes*); shortening the
  rest is #835's direction.
- #857, the stamp's mark: held for the owner.
- #825's Q1 and Q2 (`NOT_REACHED` on a red base; a row that replaces
  `PYTHONPATH`): stand as built.

## What this frame removes

The brief asks every 0.21.0 frame to say what it takes out. Rule 3 of
`templates/config.md` is 1,211 words and 57 released rows anchor its whole
section.

| Removed | Where | Replaced by |
|---|---|---|
| `COUNTS_RE` and the text form of `suite_counts` — pytest's printed summary read backwards for a wall clock | `broad_gate.py` :344, :2703–2730; the registry row at `tests/test_every_reader_ends_a_line_where_gfm_does.py` :653 | `suite_counts(record)` over the record's categories (Scope 1) |
| `NO_SUMMARY` — *no pytest summary in this output* | `broad_gate.py` :3193; its copy in `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` :601; `agents/sealer.md` :131–133 | one line built on `NO_RECORD_CAUSES` (Scope 1) |
| `RunRecord.skipped`, counted and never read | `broad_gate.py` :1916, :2010, :2015 | `unread`, read in three places (Scope 3) |
| rule 3's clause *as a `KeyboardInterrupt` or `pytest.exit()` in a test, a failed collection without `-x` and xdist under `-x` give*, and its sentence *Two stops are named rather than closed: … while each file's tests run together* (about 75 words) | `templates/config.md` §*Choosing a value — the criterion*, rule 3 | one clause: the `end` line says pytest stopped the session — an interrupt, `pytest.exit()`, `-x` or `--maxfail`, a plugin's stop — or shows an exit other than 0, 1 and 5 (about 30 words). Rule 3 shrinks by about 45 words; the larger cut is not this item's to make |
| the **New?** bullet's matching clause | `skills/verify/SKILL.md` :518–522 | the same clause in the reader's words |
| `RAN_TO_ITS_END`'s exit catalogue as the whole reading | `broad_gate.py` :1944–1962 | the comment says what is observed and what the exit net still catches, with #852's two corrections |
| the JUnit reader `suite_counts(path)` and `--junitxml` | `.github/scripts/release_seal.py` :229–262; `publish-release.yml` :128; `SUITE_XML` at :134 and `docs/release-checklist.md` :356–357 | the gate's reader and counter (Scope 4) |
| the scale: eight names, `check_scale`, two `--scale` flags, the values file's `scale` field, `admitted`'s `min(scale, rung)`, and the parametrised scale cases #853 counts as fifteen | `seal_stamp.py`, `broad_gate.py`, `hooks/sealer-stamp.py`, `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py`, `docs/the-broad-gate.md` | nothing. The disc has one size (Scope 5) |
| a traceback as the gate's answer to a malformed chart | `broad_gate.py#load` :356–363 | exit 2 with the sentence (Scope 6) |

## The input class of every reader this frame adds or changes

| Reader | Reads | Class | Unknown input |
|---|---|---|---|
| the recorder's `test` line `category` | the teststatus hook's first element, called with the report and the config | observed (pytest's own judgment) | written as given, `""` included; the counter ignores `""` |
| the recorder's `collect` line for a skipped collection | `report.skipped` | observed | — |
| the recorder's `end` line `stopped` | the keyboard-interrupt hook's `excinfo`; `session.shouldfail`, `session.shouldstop` at session end | observed | a flag set to a value that is not a string is written as `str()` of it |
| `read_record`'s `unended` | `stopped` non-empty, or no `end` line, or an exit outside `RAN_TO_ITS_END` | owned (the record) + observed (the exit) | a `stopped` that is not a list reads as unended (strict) |
| `read_record`'s `unread` | a line of a keyed file that is not a JSON object | owned | counted; the counts refused |
| `suite_counts(record)` | the keyed sessions' `category` and `collect` outcomes | owned | a category outside pytest's list is printed after the list; a `category` that is not a string is counted as `unread`'s neighbour: the line is kept for its path and outcome and counts under no category |
| `release_seal.py`'s suite rows | the same, through `read_record` | owned | refused: no seal, a warning, exit 0 |
| `read_values` | `rows` and the labels; `scale` ignored | owned | a file without `rows` in shape is refused as today |
| `load` | the sibling's import | observed | refused with the sibling's own sentence |

## User scenarios & acceptance *(mandatory)*

Every case is seen red first: at 5623d728, or with the sentence it pins
deleted, and the phase record says which.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 · the sealed panel's counts are the record's | Given a row whose one pytest session passes 768 tests and skips 1, and a test in it that PRINTS `999 passed in 1s`. When the gate seals. Then the `suite` row reads `✓ 768 passed · 1 skipped`, and the kept `suite.txt` is read for nothing on that row | a gate case over the panel with the printed decoy; red at 5623d728, where `COUNTS_RE` takes the decoy. The existing panel cases over `LONG_SUITE` and the `768 passed, 1 skipped` fixtures re-aimed to record fixtures (Q-W1) |
| S2 · the failure form's counts are the record's, in pytest's order | Given a failing suite of 1 failed, 767 passed, 1 error (a setup failure). When the form is built. Then its suite entry carries `1 failed, 767 passed, 1 error` after the file list, and `2 errors` where there are two | a `failure_lines` case over a record fixture; red at 5623d728 (no summary line in the fixture's text, so `NO_SUMMARY` printed) |
| S3 · no record, no count | Given a row that runs no pytest, or one whose pytest loaded no recorder. When it passes, the panel's `suite` row reads `exit 0`; when it fails, the form's suite entry ends with one line saying no pytest the row ran here left a record, naming the three causes, and `NO_SUMMARY`'s sentence appears nowhere | the cases at `tests/test_the_seal_is_taken_once_by_the_sealer.py` :5907–5929 and `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` :595–640 re-aimed; the new line pinned |
| S4 · two runners sum | Given a row that runs pytest twice, each session keyed. Then the counts are the sum of both sessions' | a `read_record` case over two keyed files; red at 5623d728 |
| S5 · the categories are pytest's | Given a run with a failed setup, an xfail, an xpass, a module-level skip and a module that cannot import. Then the counts read `1 error` for the setup, `1 xfailed`, `1 xpassed`, `1 skipped` for the module, and the import failure under `error`; no `warnings`, no `deselected` | a recorder case that runs real pytest over such a tree and reads the lines; the counter case over those lines. Q-M2 measures the whole against pytest's own printed line once |
| S6 · an unread line refuses the counts and demotes `new` | Given a keyed record with one line that is not a JSON object after its session line, and another run's file beside it with garbage in it. Then `unread` is 1, not 2; `suite_counts` is `None`; the form says `1 line under records/ did not parse as the recorder's and was passed over`; a file collected and not failing at such a base reads `new?` naming the count; a file failing there still reads `failing on base too` | `read_record`, `base_word` and `failure_lines` cases; the `RECORD_LINES` fixture at :4584 renamed; red at 5623d728 (`skipped` counts both files, nothing reads it) |
| S7 · `pytest.exit` with 0, 1 or 5 is a stop | Given a base where a test in `tests/test_two.py` calls `pytest.exit(returncode=1)` (and 0, and 5). When the branch fails a test in that file. Then the base's `end` line carries `stopped: [{"by": "exit", …}]`, the session is `unended`, and the file reads `new?` naming one session, not `new` | a recorder case per return code (the `end` line read back) and a gate case on the base word; red at 5623d728, where exit 1 passes as ended — #852's first case, measured in #849 round 2 |
| S8 · plain `-x` and `--maxfail` are stops | Given a base run without xdist under `-x`, whose order puts a failing test of `tests/test_one.py` before the rest of `tests/test_two.py`. When the branch fails a test of `tests/test_two.py`. Then `stopped` carries `{"by": "failures", "what": "stopping after 1 failures"}`, and the file reads `new?`. The same under `--maxfail=2`, and for a failed collection under `-x` in BOTH orders (exit 1 and exit 2) | recorder and gate cases; red at 5623d728 — #852's second case |
| S9 · a plugin's stop is a stop | Given `--stepwise` (which sets `session.shouldstop`). Then `stopped` carries `{"by": "stop", …}` and the session is `unended` | a recorder case; red at 5623d728 only where the exit is 1 — the case asserts the field, not the exit |
| S10 · a session that ran to its end is not unended | Given `stopped: []` and exit 0, 1 or 5. Then not `unended`. Given `stopped: []` and exit 2, 3 or 4. Then `unended` by the exit net, as today | `test_a_keyed_session_whose_end_shows_a_stop_is_counted_unended` re-aimed over both fields; the fixtures at :4813–4814, :4860, :4887 gain `stopped` |
| S11 · the sentences a person reads move together | Rule 3 carries the new clause and neither removed sentence; the **New?** bullet matches; `RAN_TO_ITS_END`'s comment says what is observed, carries the `-x` collection condition, and names each exit's builds as Q-M1 measured them; `UNENDED_AT_BASE` and `UNENDED_HERE` name the stop among the causes; the recorder's docstring documents `category`, `stopped` and the skipped `collect` line | the two rule-3 pins (`test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written`, `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`) and the sentence cases at :5028–5040 moved in the same commit; `tests/test_no_passage_is_pasted_into_a_second_file.py` green |
| S12 · the release seal's counts are the record's | Given the `seal` job's suite step run with the recorder's four variables. Then `release_seal.py` prints `suite    7069 passed, 66 skipped` from the record; given a record with a `failed` or `error` count, an unread line, an unended session or no keyed session, then `no seal: the suite's counts cannot be read: …` and `::warning::`, exit 0; `--junitxml`, `SUITE_XML` and the JUnit reader are gone from the tree, and the checklist names the variables | `tests/test_the_release_seal_is_drawn.py` :286–336 and :615–726 re-aimed to record fixtures (the `junit` helper replaced by a record-writing one); `test_the_publishing_workflow_installs_the_pins_the_runner_holds` green unchanged; `grep -rn 'junitxml\|SUITE_XML' .github docs` returns history only |
| S13 · the scale is gone and the stamp is the same | `broad-gate --scale 0.9` and `seal-stamp --scale 0.9` are refused by argparse; no name in `seal_stamp.py` matches `SCALE_`; `build()`, `stamp(rows, shape)` and the hook draw byte for byte what 5623d728 drew at 0.90 for the same rows; `admitted` steps a block from with-disc to without and the owner's one-per-`Stop` rule holds; a values file with `"scale": 0.9` draws, and one without draws; the gate's values file carries no `scale`; `docs/the-broad-gate.md`'s ladder sentences say with its disc, then without | the parametrised scale cases collapsed to one each; `test_the_ladder_steps_down_in_order_and_ends_with_no_disc` re-aimed to two rungs; `test_a_file_at_a_scale_the_band_refuses_is_left_pending`, `test_the_default_scale_is_ninety_percent_with_its_reason_beside_it`, `test_the_floor_scale_is_accepted_and_below_it_is_refused_with_a_sentence`, `test_both_commands_draw_at_the_default_scale_when_given_none` and the NaN case at :174–192 retired; a byte-for-byte case against a drawing captured at 5623d728 (Q-W3); `test_the_values_file_holds_this_runs_panel` re-aimed; `grep -rn 'scale' skills/verify hooks docs/the-broad-gate.md agents` returns nothing about the stamp |
| S14 · a malformed chart is a refusal | Given a copy of the plugin whose `seal-mark.txt` has 27 lines. When `broad-gate --base <ref>` and `broad-gate --preflight --base <ref>` run. Then exit 2, stderr holds `CHART_MALFORMED`'s sentence with the path, no `suite.txt` exists under the kept output, no worktree was added | a gate case over a copied plugin tree; red at 5623d728 (a traceback, exit 1) |
| S15 · the ledger says what moved | This item's fragment holds its own rows and, from `evidence-check --reverify --into … --checked <date>`, a re-read for each released row that drifted, and `Corrected ·` rows for the ones this work makes false: 0.10.0 S14 (the suite row from pytest's counts by wall clock), 0.15.3 A5 (`NO_SUMMARY` on the form), 0.15.7 N5 and N6 (the values file's `scale`; `--from` at its own scale), 0.18.0 C2 (the JUnit reader), 0.20.0 U1 (`unended` by `end` line and exit alone), U3 (rule 3's two stops), U4 (the no-summary line), and the 0.20.0 corrections of B1, B2, L1, L2, L3 and S2 where they say *at every scale* or name the ladder's rung; the rows on `"## Broad gate"` are re-reads | `evidence-check --strict` green; the fragment read once by the reviewer against the list here (Q-W2 says the build enumerates from the checker's own output, this list being the frame's reading) |

## Data & interfaces

**The record** (`specseal_pytest_record.py`'s docstring is the format's one
home and is rewritten with it):

- `test` line: `nodeid`, `when`, `outcome`, `path`, `wasxfail` where set,
  and `category` — the teststatus hook's first element for this report, a
  string, `""` where pytest counts the report nowhere.
- `collect` line: written for a failed and for a skipped collection;
  `outcome` is `failed` or `skipped`; `path` as today. Today's `if not
  report.failed: return` becomes a test for *failed or skipped*.
- `end` line: `exitstatus`, `unplaced`, and `stopped` — a list, empty where
  nothing stopped the session; otherwise entries `{"by": "interrupt" |
  "exit" | "failures" | "stop", "what": <str>}`: `interrupt` and `exit` from
  the keyboard-interrupt hook (`what` the exception's type name, and for
  `exit` the message and the return code pytest's `Exit` carries, as text),
  `failures` from `session.shouldfail`, `stop` from `session.shouldstop`,
  each read at session end.

**The gate** (`broad_gate.py`):

- `RunRecord`: `unread` in place of `skipped`; `counts`, a dict of category
  → count over the keyed sessions, a failed collection under `error` and a
  skipped one under `skipped`; `unended` as Scope 2 says.
- `read_record`: counts `unread` after the key check and per keyed file;
  reads `category`, the `collect` outcome and `stopped`.
- `suite_counts(record)` → the counts string in pytest's shape, or `None`
  where `record.sessions` is 0 or `record.unread` is not 0. `panel` keeps
  its `split(", ")` and `wrapped` over it.
- the head record is read once after the suite arm and handed to
  `failure_lines` and to `panel`.
- new sentences, each pinned: the no-record line for the failure form
  (built on `NO_RECORD_CAUSES`), the unread line for the form, the unread
  reason for `base_word` (checked after `UNENDED_AT_BASE`); `UNENDED_AT_BASE`
  and `UNENDED_HERE` reworded to name a stop pytest made among the causes.
- `load` wraps `exec_module` and raises `Refused` with the path and the
  exception's sentence.
- `--scale` removed; `gate` asks no `check_scale`; `signal` writes no
  `scale`; `stamp.stamp(rows, shape)`.

**The stamp** (`seal_stamp.py`): `build()`, `compose(rows, disc=True)`,
`stamp(rows, shape=False, disc=True)`, `admitted(blocks, budget)` over
`(label, rows)` blocks with two rungs, `fitted` as is, `read_values`
ignoring `scale`, `main` without `--scale`, `drawn_from(path, shape)`. The
module docstring, `DISC_CELLS`'s comment and `admitted`'s docstring stop
mentioning a scale or a rung of 0.90.

**The hook** (`hooks/sealer-stamp.py`): `(label, rows)` blocks;
`stamp(rows, shape=False)`; the docstring's budget paragraph loses its
`SCALE_LADDER` sentences.

**The release seal** (`.github/scripts/release_seal.py`,
`publish-release.yml`, `docs/release-checklist.md`): `SUITE_RECORDS` (the
directory) and `SUITE_KEY` (the key) in place of `SUITE_XML`; the step sets
`PYTHONPATH`, `PYTEST_ADDOPTS`, `SPECSEAL_RECORD_DIR` and
`SPECSEAL_RECORD_KEY`; the counts come from `read_record` and
`suite_counts(record)` loaded through `module`. <!-- NAME NOT IN TREE -->

**Documents**: `templates/config.md` rule 3 (one clause for two sentences);
`skills/verify/SKILL.md` the **New?** bullet; `docs/the-broad-gate.md`
§*Where the stamp is drawn* (the ladder sentences; `Enforced by:` kept);
`agents/sealer.md` :131–133; `docs/release-checklist.md` :352–359.

**Tests**: the cases S1–S15 name; the registry row for `suite_counts` in
`tests/test_every_reader_ends_a_line_where_gfm_does.py` removed; the
`"kind": "end"` fixtures gain `stopped`.

## Open questions → questions.md

Five rows, none a person's: two measurements the smith makes first (the
hooks and flags on pytest 6.1, 7.0 and 9.1; the counts against pytest's
own line once) and three the work answers in its phase records. The
decisions the tickets left open that the tree answered are listed at the
head of that file so nobody reopens them.

Framed 2026-10-07 by framer, before the build.
