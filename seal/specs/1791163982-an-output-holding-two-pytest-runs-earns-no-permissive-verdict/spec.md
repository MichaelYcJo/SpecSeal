# Feature Specification: an output holding two pytest runs earns no permissive verdict (#789)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

#789 and its comment, read 2026-10-05, at a3aa139a. `compare_at_base` in
`skills/verify/scripts/broad_gate.py` re-runs the failing files at the base
and reads its words off the text pytest printed. That text can hold more
than one pytest run, and three members of one ground follow from it:

1. **Two runners in the row** (`pytest -q && cd sub && pytest -q`). A file
   is asked of the first runner a prefix reaches, in that runner's
   directory. Round 1 of #761 measured `new` for a file the base fails (p1),
   `failing on base too` for a file the base never ran (p1b), and round 2
   added p1c (`new` where a same-named root file passes at the base). Rule 3
   of `templates/config.md` names the shape as a limit.
2. **An inner run on stderr under `-s`.** `run` joins stdout and then
   stderr, so the inner run's `short test summary info` rule stands after
   pytest's own, and the run's own `FAILED` line is not read. Round 3 of
   #761 measured `new` for a file the base fails, where 0.18.1 read
   `failing on base too`.
3. **A run in which pytest wrote no rule of its own** (`-rN`, `-rP` with no
   failures) **or no summary line** (`-qq`) reads a test's printed rule or
   summary as its own.

The comment warns against the issue's own proposal. Counting summaries in
the output also counts an inner pytester run's summary in captured output,
so every failing file of a suite that tests a pytest plugin would read
`new?`. Whatever decides "more than one runner" has to tell pytest's own
trailer from a test's printed one, or keep the runs apart. It must not count
lines.

**This frame draws the second way: the runs are kept apart by asking pytest
for its report rather than reading its text.** Every run at the base gets
`--junitxml=<path>` appended after the files, a path the gate chose. Only the
pytest process that received the gate's arguments writes that file. An inner
run started by a test gets arguments of its own, a pytester run in-process
or in a subprocess included, and none of them writes there. So the report is
pytest's own account of the one run the gate asked about, whatever a test
printed, on whichever stream, under whichever reporting flags. That settles
members 2 and 3 by construction. Member 1 is not settled by it, because a
row's first runner also receives the gate's arguments; a separate
collection-only pass counts the row's runners (Scope 4).

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `agents/sealer.md` §*Boundaries* — "`new` and `failing on base too` are the gate's words: it re-ran the failing files at the base to earn them" | The promise kept literal. A word comes only from a run the gate can show was the run it asked about |
| `README.md` "failing on base too → named as a follow-up, does not block"; `skills/verify/SKILL.md` §*The broad gate* (the three words) | `failing on base too` is the one permissive word. This work's acceptance is that no shape in the class gives it to a file the base did not fail where the row runs it. A wrong `new` is the second error and is closed the same way |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides between the issue's `new?`-for-every-file and a measurement: a measured word sends nobody to the base by hand. Where nothing can measure (two runners), `new?` is the honest word and the issue's proposal stands |
| `compare_at_base`'s docstring, "measured — never inferred"; #758's `spec.md` Scope 3 "A word is given only from a run that measured it" | The rule the new reading is held to |
| Work item `1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory`: `spec.md` Scope 1–6, `rounds/round-1-report.md` 🟡 2 (p1, p1b), `rounds/round-2-report.md` ⬜ 2 (p1c), `rounds/round-3-report.md` 🟡 1 and ⬜ 2, `overview.md` §*Not done* | What 0.18.2 built and must not be undone: the root split nominates and decides nothing, each candidate runs alone, a run that collected nothing gives `new` only to a file run alone, an inner run's lines never decide. Every one of those is kept; only the source of the reading changes from text to the report |
| `templates/config.md` §*Broad gate* §*Choosing a value — the criterion*, rule 3 | The one home of what the comparison costs a row and which rows it cannot measure. Its two-runner sentence and its `-s` sentence become false and are replaced by the behaviour's description, as the issue asks |
| `skills/implement/orchestration.md`, via `overview.md` of the 0.18.2 item, divergence row 1 | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py::test_the_one_shell_site_is_run_and_it_applies_the_rewrite` counts the `run(...)` calls in `compare_at_base`. Every run this work adds, the collection pass included, goes through the one existing call |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A case seen red, a failure direction, a prompt budget, platform honesty — answered in `plan.md` §*Operational impact* |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | Enumerate the class (below); the changed reasons and rule-3 sentences are pinned in the commit that changes them; every new case is seen red at a3aa139a |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `seal/config.md` `Ledger frozen from`; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | `seal/releases/0.18.2.md` rows D1, D2, `Corrected · B3` and `Corrected · S5` state the text reading and the two-runner limit. They become false; their corrections are `Corrected ·` rows in `seal/ledger/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict.md`, and the released file is not edited |

## The class, enumerated by construction

**The defect is one sentence: the gate read its words off text in which a
line pytest wrote for this run and a line something else wrote cannot be
told apart.** Two things put foreign lines in the text, and each was
enumerated on its own axis.

### Axis A — what a test prints (members 2 and 3, and a fourth)

Executed 2026-10-05 against pytest 9.1.1 and pytest-xdist 3.8.0 in a scratch
project: 96 runs, the product of four inner-run kinds × the base failing or
passing the outer test × twelve flag sets. The inner kinds are a subprocess
writing to the test's stdout, one writing to its stderr, pytester in-process,
and pytester in a subprocess. The flag sets are none, `-q`, `-qq`, `-q -s`,
`-q --capture=sys`, `-q -rN`, `-q -rP`, `-q -rA`, `-q -x`, `-q -n 2`,
`-q -n 2 -s` and `-q -n 2 -rN`. The inner run fails `tests/test_g.py`, which
the outer run passes. Each output was joined the way `run` joins it and read
by a3aa139a's own `measured_summary` and `verdicts_at_base`.

| Shape | a3aa139a's words | The appended report |
|---|---|---|
| inner run on stderr under `-s`, `--capture=sys`, `-n 2 -s`; base fails the outer test | outer `new`, inner file `failing on base too` (member 2) | right in every run |
| the same with the base passing everything | inner file `failing on base too` | right |
| inner run on stdout under `-s` or `--capture=sys`, base passing everything | inner file `failing on base too`. **Not in the issue:** with no failure pytest writes no rule, so the last rule is the inner one, on stdout. Keeping the streams apart, which the issue's comment proposed for member 2, would not close it | right |
| `-rN`, `-n 2 -rN`, `-rP` with an inner run in captured output (subprocess on stdout or stderr, or pytester in a subprocess) | outer `new`, inner file `failing on base too` (member 3) | right |
| `-rP`, base passing everything | inner file `failing on base too` | right |
| `-qq` | `new?`, or a word read off an inner summary (member 3) | right, because the report does not depend on verbosity |
| every other shape | right, or an honest `new?` (`-x` reads `STOPPED_EARLY` for the file it never reached, which is right) | right |

16 of the 96 runs gave a3aa139a's reading the permissive word for a file the
base passes. The appended report named exactly the outer test in all 96:
`tests.test_err` where the base failed it and nothing where it passed it,
under xdist and with pytester in-process and in a subprocess. No inner run
wrote to the path.

### Axis B — how many runners the row has (member 1)

A runner is a part of the row that is pytest and that the row reaches. The
report does not count them, because a row's first runner also receives the
gate's arguments when a prefix ends at it. Executed on a scratch row
`pytest -q && cd sub && pytest -q`, with each prefix run under
`PYTEST_ADDOPTS=--collect-only` and its own `--junitxml` appended. Prefixes 1
and 3 wrote their reports and prefix 2 (ending at `cd sub`) did not, for `&&`
and for `;` alike. Without `--collect-only`, a base whose root suite fails
stops the `&&` row at the first runner, so a real run of prefix 3 wrote
nothing. Collection alone is what reaches the second runner, and it runs no
test, so no inner run exists to confuse it.

| Runners the row reaches at the base under collection alone | Words |
|---|---|
| none — no prefix writes the report | every file `new?` (`NO_RUNNER`, reworded) |
| one | measured from the report, as Axis A |
| two or more | every file `new?` with a reason naming the parts (`MULTI_RUNNER`, new). This is the issue's proposal, decided without counting lines |

**What collection alone does not reach** (a named limit, Scope 7):

- a runner behind a part that exits non-zero at the base under collection
  alone. That covers a lint part failing at the base, an earlier runner with
  a collection error at the base (exit 2), and an earlier runner that
  collects nothing (exit 5);
- a runner joined by `||`, which runs only when the part before it fails.

In either case the comparison takes the row for a one-runner row, so member
1's words can return. Measured: `--continue-on-collection-errors` beside
`--collect-only` still exits 1, and an empty collection exits 5. No option
makes every runner exit 0 under collection. Telling "part j is not pytest"
from "part j was not reached" would take a reading of the shell this module
does not have.

### Axis C — the branch's own run (the list of files, not their words)

`failing_files` reads every `FAILED` line in the branch's output, inner runs'
included. Round 3 of #761 judged it true that this costs "an extra line and
never a seal", because a failed suite arm fails the gate whatever the words.
That stays. The branch's run is the row as written, the run CI mirrors, so
the gate cannot give it an argument of its own. **Out**, below.

## Scope

### In

1. **Every run at the base appends `--junitxml=<path>`** after the files, as
   one quoted argument (`quote`). The path is absolute, in the kept
   directory, beside the run's text, under the same stem:
   `suite-at-base-<k>.xml` or `suite-at-base-<k>-<n>.xml`. Appending to the
   row is what the comparison already does with the files. The option goes
   after them, so it overrides a `--junitxml` in the row's own arguments or
   ini `addopts`, because pytest takes the last value given.
2. **A prefix settles where its report was written** and parses. Where no
   prefix writes one, every file of the run reads `NO_RUNNER`. The text is no
   longer asked whether pytest ran. So a part that prints pytest's summary
   without running the files appended to it writes no report and reads
   `new?`. That covers a `sh -c '…'` that drops its arguments, a `make`
   target, `-p no:junitxml` and a runner that rejects the option. Today such
   a part reads `new` (rule 3's "one shape the gate cannot see through").
3. **The words are read off the report**, by a pure function of (report
   text, the files appended, the run's exit code, whether the run stopped
   early). The report's tests are placed on the appended files by the name
   pytest's report gives a test: the path written with `.` for `/` and its
   `.py` dropped, then any class names. A collection error carries the path
   in `name` with an empty `classname`. The path is relative to pytest's
   rootdir, which can sit above or below the directory the row runs pytest
   in, so the match is on dotted components and allowed in either direction.
   Measured: `cd sub` with the ini at the root gives `sub.tests.test_two`
   for the appended `tests/test_two.py`, and an ini in `sub` run from the
   root gives `tests.test_two` for `sub/tests/test_two.py`. For each file:
   - a failing or erroring test placed on this file alone → `failing on base
     too`;
   - a failing or erroring test that could be placed on this file and on
     another appended file, or on none of them → `new?` for every file it
     could be, and for every file not named, with a reason (`UNPLACED`,
     new). A failure nobody can place never lets a file read `new`;
   - otherwise, where the run stopped early (any `STOPPED_EARLY_RE` rule in
     the output, read anywhere, which can only cost a word) → `STOPPED_EARLY`;
   - otherwise → `new`.
4. **A row with more than one runner gives no measured word.** Where the
   first settled prefix *k* is not the whole row, each later prefix runs
   once more under `PYTEST_ADDOPTS` with ` --collect-only` added to whatever
   the gate's environment already carries. Nothing is appended but its own
   `--junitxml`, kept as `runners-at-base-<j>.txt` and `.xml`. Where any of
   them writes its report, every failing file reads `MULTI_RUNNER`, naming
   parts *k* and *j*, and the words already read are replaced. This happens
   once per comparison, not per file, because how many runners a row has is
   a property of the row. A row whose runner is its last part (this
   repository's, and every lint-first row) never pays it.
5. **What 0.18.2 built is kept**: the candidate split (`git cat-file -e
   HEAD:<f>` nominates and decides nothing), one group of the others and one
   solo run per candidate, the order, the `suite-at-base-<k>[-<n>].txt`
   names, `row_prefixes`, and the signature and return shape of
   `compare_at_base`. A file run alone whose report counts no test, with
   exit 4 or 5, reads `new`, as `collected_nothing` gave it. The report's
   count of tests replaces the `no tests ran` line, and the exit-code half
   stays. A run of several whose report counts no test settles the walk:
   the row's runner was reached, and one of the files is missing where it
   runs. Each of its files reads `new?` with a reason saying so
   (`NOTHING_TOGETHER`, new), where today the walk goes on and ends in
   `NO_RUNNER`.
6. **The text readers that decided words retire**: `PYTEST_SUMMARY_RE`,
   `SHORT_SUMMARY_RE`, `NOTHING_COLLECTED_RE`, `measured_summary`,
   `collected_nothing` and `verdicts_at_base` as a text reader, along with
   `ERROR_RE` where nothing else reads it. `STOPPED_EARLY_RE` stays. So do
   `FAILED_RE` and `failing_files`, which read the branch's run. Their unit
   tables in `tests/test_the_seal_is_taken_once_by_the_sealer.py` become
   tables over the report reader, covering the same shapes as reports.
   `tests/test_release_hygiene.py` names three of these constants and moves
   with them.
7. **What a person reads changes, and is documented and pinned in the same
   commit (§14):**
   - `templates/config.md` rule 3. The sentences that say the gate reads
     pytest's summary line say it asks for and reads pytest's report. The
     `-s` sentence and the "one shape the gate cannot see through" sentence
     are replaced by what is now true: a part that does not hand
     `--junitxml` on to pytest reads `new?`. The two-runner sentence is
     replaced by "a row that runs pytest in more than one part reads `new?`
     for every failing file". It also gains the collection pass's cost (one
     collection run per prefix after the runner, once, only on a failing
     gate) and the limit of Axis B, word for word as it ships.
   - `NO_RUNNER` reworded to say no part of the row wrote the report the
     gate asked pytest for, with the kept names. `MULTI_RUNNER`, `UNPLACED`
     and `NOTHING_TOGETHER` added. Each is pinned whole in
     `test_the_unmeasured_word_says_so_and_every_reader_is_told_it`, and
     `STOPPED_EARLY` is unchanged.
   - `skills/verify/SKILL.md` §*The broad gate*, the **New?** bullet: its
     reason clause names the report and the row with more than one runner.
     Its pin ("printed a line the gate reads as pytest's summary") moves to
     the new text.
   - `compare_at_base`'s docstring and the comments over the retired
     constants. The module docstring keeps "`new?` with the reason no run
     measured it", which is pinned.
   - `test_the_one_counterfeit_the_gate_cannot_see_is_named` pins a shape
     that is no longer a counterfeit. It becomes the case that the shape
     reads `new?` (S6), and its sentence pins go with the rule-3 rewrite.
   - `agents/sealer.md`, `agents/smith.md`, `README.md` and `README.ko.md`
     are not edited: the three words and their meanings do not change.
     Read at a3aa139a to confirm none names the summary line.

### Out, and why

| Left out | Why | Who answers |
|---|---|---|
| The issue's literal proposal: count pytest summaries in the output, or give every candidate `new?` | Counting lines counts inner pytester summaries (the comment's warning, measured above: every inner kind prints one). "Every candidate" misses p1b, whose permissive word comes from the group of non-candidates. Scope 4 gives every file `new?`, decided by reports rather than lines | decided here, from the tree and the probe |
| Keeping stdout and stderr apart in `run` (the comment's "code half") | The report makes the base reading independent of both streams. Splitting them would not close the stdout shape found above, and it would change the one runner every arm shares | decided here, from the probe |
| Finding each file's runner in a two-runner row, so the row can be measured | It would take a collection run per file per runner, plus a rule for a file that two runners both collect. The issue asks for no permissive word, and `new?` gives that. `plan.md` Alternatives, row E | the repository owner, if a two-runner row is ever met — a new issue |
| The runners collection alone does not reach (Axis B's limit) | No option makes pytest exit 0 under collection, and telling "not pytest" from "not reached" needs a shell reading this module lacks. Named in rule 3 | the repository owner, if met — a new issue |
| The branch's list of failing files (Axis C): an inner run's `FAILED` line adds a file, and under `-rN` on the branch it can be the only file listed | The branch's run is the row as written, which the gate must not alter. The added file's word is measured truthfully for that path, and the gate fails either way (round 3 of #761, confirmed) | decided by round 3 of #761; the repository owner if it is ever met |
| A runner that moves a `--junitxml` argument somewhere it is not read, or a wrapper that rejects unknown options | Reads `new?` (`NO_RUNNER`), the conservative direction, and rule 3 tells the row's author to pass the option on | the row's author, told in rule 3 |
| `( … )` and `{ …; }` groups, `ERROR`-only branch failures | Unchanged from #758 and #761 | as those items left them |

## User scenarios & acceptance *(mandatory)*

Every gate case lives in `tests/test_the_seal_is_taken_once_by_the_sealer.py`
and is built with its `base_then_feature`, `SUITE_ROW`, `suite_row(xdist)`,
`verdict_of` and `run_gate(repo, keep=…)`. "Seen red" means the case was run
against a3aa139a's `broad_gate.py` and failed there (§15).

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | Member 2: an inner run on stderr under `-s` | The base's failing `tests/test_err.py` runs a subprocess pytest whose output goes to fd 2 and which fails `tests/test_g.py`. The base passes `tests/test_g.py` and the branch fails both. Row `{SUITE_ROW} -s`, plain and xdist. Then `tests/test_err.py` reads exactly `failing on base too` and `tests/test_g.py` reads exactly `new` | executed — new case; seen red (a3aa139a: `new` and `failing on base too`). This is round 3's "regression test to plant with #789's fix" |
| S2 | Under `-s`, a base that passes everything, with an inner run on stdout | As S1, but the base's `tests/test_err.py` passes and the inner run writes to fd 1. Row with `-s`, and with `--capture=sys`. Then both files read exactly `new` | executed — new case; seen red (`tests/test_g.py` `failing on base too`) |
| S3 | Member 3: no rule of pytest's own | S1's base under the rows `-rN` and `-rP`, without `-s`. Then `tests/test_err.py` reads `failing on base too` and `tests/test_g.py` reads `new`; and S2's passing base under `-rP` reads `new` for both | executed — new case, parametrised; seen red |
| S4 | Member 3: no summary line | Row `{SUITE_ROW}` with `-qq`. The base passes `tests/test_two.py` and the branch fails it. Then it reads exactly `new`. Second param: S1's failing base under `-qq` reads S1's words | executed — new case; the first param is seen red (a3aa139a: `NO_RUNNER`, rule 3's "none under `-qq`"). The second holds at a3aa139a too, because the rule there is pytest's, and it is kept as the guard on the inner summary that `-qq` leaves last |
| S5 | The 0.18.2 inner-run cases keep their words | `test_what_a_test_printed_is_not_read_as_pytests_own_lines` (both params, both `UNDER`) and every other end-to-end case of the base comparison pass with their word assertions unchanged. A reason pinned whole moves only with Scope 7 | executed — those cases |
| S6 | A part that drops its arguments | Row `sh -c '{SUITE_ROW}'` (POSIX only, skipped with its reason on Windows), and a row with `-p no:junitxml`. The base fails `tests/test_two.py`. Then the file reads exactly `NO_RUNNER`, never `new` | executed — replaces `test_the_one_counterfeit_the_gate_cannot_see_is_named`; seen red (`new`) |
| S7 | Member 1: p1, p1b and p1c | Row `{SUITE_ROW} && cd sub && {SUITE_ROW}`, with round 1's p1 and p1b and round 2's p1c built as those reports describe them, plain and xdist. Then every failing file reads exactly `MULTI_RUNNER`, and `runners-at-base-<j>.txt` is kept | executed — new case, parametrised; seen red (`new`, `failing on base too`, `new`) |
| S8 | One runner first, then a part that is not pytest | Row `{SUITE_ROW} && {sys.executable} -c pass`. The base fails `tests/test_two.py` and the branch adds a failing `tests/test_three.py`. Then the words are `failing on base too` and `new`, and `runners-at-base-2.txt` is kept with no report beside it | executed — new case; seen red on the kept-file assertion only (the words hold at a3aa139a) |
| S9 | The report reader | A unit table over report texts: a function, a class method, a parametrised test, a collection error (empty `classname`), a setup error, a rootdir above and below the directory pytest runs in, a failure that matches two appended files, a failure that matches none, no test with exit 4 and with exit 5 for one file and for several, a stop marker. Each row gives its word | executed — unit rows; each mutation of the reader turns a row red: dropping the either-direction match, dropping the ambiguity rule, dropping the exit-code half |
| S10 | The cost and the limits are told where the row is written | Rule 3 carries the Scope 7 sentences. The four reasons are pinned whole. The **New?** bullet names the report and the row with more than one runner | executed — the pins, each seen red with its sentence deleted |
| S11 | This repository's own row | `uvx ruff check . && uvx ruff format --check . && bin/test -q` with a failing file at the base: `bin/test` hands `--junitxml` to pytest, so the file is measured, and no collection pass runs because the runner is the last part | executed — a probe in phase 1 (`.github/scripts/run_tests.py#main` passes its arguments through, read; whether pytest receives the option is the measurement). Not a planted case: the suite does not run `uvx` |

## Data & interfaces

- `compare_at_base(root, base, command, files, keep)`: signature and the
  `{file: word}` return unchanged.
- New: one pure reader of a report, (report text, appended files, exit code,
  stopped) → `{file: word}`, beside `STOPPED_EARLY_RE`. It parses with the
  standard library's ElementTree and accepts a `testsuites` root or a bare
  `testsuite`.
- New reasons, each opening `NOT_MEASURED`: `MULTI_RUNNER`, `UNPLACED` and
  `NOTHING_TOGETHER`. `NO_RUNNER` is reworded.
- Kept files: `suite-at-base-<k>[-<n>].txt` as today, each with its `.xml`
  beside it; `runners-at-base-<j>.txt` and `.xml` for the collection pass.
- The collection pass's environment is the gate's own with ` --collect-only`
  appended to `PYTEST_ADDOPTS`, passed through `run`'s existing `env`.
- Ledger: new rows and `Corrected ·` rows for `seal/releases/0.18.2.md` D1,
  D2, `Corrected · B3` and `Corrected · S5`, all in
  `seal/ledger/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict.md`.
  Re-reads of every other released row whose coordinate drifts go there too,
  through `evidence-check --reverify --into`.
- Changelog fragment:
  `seal/specs/1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict/changelog.md`.

## Open questions → questions.md

`questions.md` beside this file. No row waits on a person. Two are
measurements and two are the work's, each with the default the build uses.

Framed 2026-10-05 by framer, before the build.
