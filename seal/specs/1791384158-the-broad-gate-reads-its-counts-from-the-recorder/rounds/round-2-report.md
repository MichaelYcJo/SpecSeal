# Round 2 report — 1791384158, the broad gate reads its counts from the recorder (#869, #852, #853)

- Target SHA: 1f0d610dc47d7f33413c564700d03637b78e3c72 (the clone's `git rev-parse HEAD`, executed)
- Round: 2, a verifying round. Its target is the diff of round 1's fixes,
  `4f44e5c9..96f6d42b` (43a38107, 80881f35, 6ea5686e, 96f6d42b), and the
  three record commits after it (b562cb54, 5c64f705, 1f0d610d).
- New units from round 1's record: `SCALE_FOR_OLDER_HOOKS`, judged as code.
- Nothing is carried from the earlier attempt at this round. Its scratch
  directory was still on disk (`<scratchpad>/1791384158/round-2/`). I did
  not open or use it, and this round worked in a new one.

## How the answers relate

```
round 1's five fixes        -> each closed; each guard reverted turns its pinned case red
the unplaced refusal (2)    -> can withhold a count pytest printed in full; strict side, by design
   the failure form         -> ⬜ 1  the counts line vanishes and no sentence says why
the scale constant (3)      -> reaches the one place a values file is written
   its retirement           -> ⬜ 2  only a comment, a doc sentence and the changelog promise it
the count_towards_summary   -> cannot move a count pytest prints; same test, same object
   guard (5)                -> ⬜ 3  collect reports are the half of the class it does not cover
```

All five closed verdicts hold. Nothing I found needs a fix before merge.
The three ⬜ are sentences and one unenforced promise.

## Round 1's verdicts, answered

### Blocking finding 1 is closed: the interpreter registry no longer classifies `seal_stamp.py`

Read: 43a38107 drops the one `CLASSIFIED` row and nothing else.
Executed: `bin/test tests/test_a_script_says_which_interpreter_it_needs.py`
in the clone gives 22 passed, exit 0. Executed: `gh pr checks 880` at the
target (run 37728336035, whose head SHA I confirmed through `gh api`). The
ubuntu leg and all four Windows shards pass, and so do lint, ledger,
release and both arm-check legs. The three macOS shards were still pending
when this report was written.

### Finding 2 is closed, and the refusal can withhold a count pytest printed in full

Read: `skills/verify/scripts/broad_gate.py#suite_counts` returns None
where `record.unplaced` is not 0, and
`.github/scripts/release_seal.py#suite_counts` raises after the `unended`
refusal. Executed: with each guard removed in the clone,
`test_counts_the_record_cannot_vouch_for_are_none` and the `a report with
no file of its own` case of
`test_a_record_that_cannot_vouch_for_the_counts_is_a_failure_never_a_zero`
both fail, and both pass again once the guard is restored.

The spawn asked whether the refusal can remove a legitimate count. It can,
in two ways.

- **A green run with an unplaced test.** Take a conftest that parents an
  item to a directory, or a plugin that builds a report without the path.
  pytest's line counts that test, and the record could have printed every
  other count correctly. The panel's `suite` row now reads `exit 0` with no
  tick (`broad_gate.py#panel`). The green form has no line that says why,
  because `UNPLACED` is printed only by `failure_lines`. On a tag, the
  release seal prints a `::warning::` and draws no image. The workflow
  stays green, because every step of the `seal` job is
  `continue-on-error`.
- **A pathless report whose `count_towards_summary` is false.** The
  recorder's `path_of` counts it in `unplaced` before `category_of` is
  asked, so the counts are refused although pytest never counted it. I
  know of no plugin that builds such a report.

Both cases fail on the strict side, as round 1's fix intended. A green
panel already read `exit <n>` where a record held an unread line or no
report (the overview's divergence table). Nothing I read makes either case
likely in this repository. No conftest here defines a collector
(`git grep` for the collect hooks over `conftest.py` files, executed).
The smith's account says half the suite under the recorder gave
`unplaced 0`. That is a claim I did not reproduce, and the sealer's run
answers it from its own record's `end` lines.

What the failing form shows is the one gap, ⬜ 1 below.

### Finding 3 is closed: `SCALE_FOR_OLDER_HOOKS` reaches every values file the gate writes

Read: the tree has one writer of a values file outside the tests,
`broad_gate.py#signal`, through `seal_stamp.py#write_values`
(`git grep write_values`, executed). `signal` builds one dictionary, and
`"scale": SCALE_FOR_OLDER_HOOKS` is in it. Where `item` is None, `signal`
returns before any file is written, so no path leaves the key out.
`release_seal.py` draws a PNG and writes no values file.

Read: the installed 0.20.0 `read_values` refuses only a `scale` that is a
bool or not an int or a float. 0.9 passes, and the installed hook then
draws at `values["scale"]`, which is the one rung 0.20.0 has. A file it
cannot read is skipped silently and left pending (`hooks/sealer-stamp.py`
in the 0.20.0 cache, `drawings`). So a file written without a `scale`
before 6ea5686e does not raise a message at every `Stop`. The smith says
the installed `seal_stamp.py --from` drew such a file at exit 0. I did not
run the installed copy, because the spawn keeps execution inside the clone.

Executed: with the `"scale"` line removed in the clone,
`test_the_values_file_holds_this_runs_panel` fails, and it passes once the
line is restored. Read: nothing in the tree reads the key. `git grep`
finds `"scale"` in non-test code only at that line, and the tree's
`read_values` returns it unread.

What retires the constant after 0.21 is ⬜ 2 below.

### Finding 4 is closed: `RAN_TO_ITS_END`'s comment names the `-x` case

Read: the sentence round 1 proposed is in the comment at
`broad_gate.py#RAN_TO_ITS_END`, with its round named.

### Finding 5 is closed, and the guard cannot move a count pytest prints

Read: pytest 9.1.1, the version `bin/test` installs, filters its summary
line with `getattr(x, "count_towards_summary", True)` over the reports in
`stats[key]` (pytest's terminal.py, lines 1450–1453). The recorder's
guard asks the same attribute with the same default, of the same report
object, in the same process. That holds on an xdist controller too, where
both the terminal reporter and the recorder receive the deserialized
report. A report pytest counts is therefore never `""`, and a report
pytest leaves off its line is never counted by the gate.

The failing-file lists read a line's `outcome` and not its `category`, so
a failed report pytest leaves off its line still names its file. That
agrees with pytest's exit code. Skipping the teststatus hook changes no
count either, because the hook's first result only labels the report.

Executed: with the guard removed in the clone,
`test_a_teststatus_answer_that_holds_no_word_writes_no_category` fails,
and it passes once the guard is restored.

The guard covers test reports only. Collect reports are ⬜ 3.

### Finding 6 stays deferred to #883

It was already deferred in round 1, and the overview's *Not done* names
#883. I did not reopen it.

## New findings

### ⬜ 1 · A failing suite with an unplaced test loses its counts line, and no sentence says why

Read. Since 80881f35 the failure form prints no counts where
`record.unplaced` is not 0. It does print `UNPLACED`, but that line says
only that the tests "are in no list". The branch gave `UNREAD_HERE` the
clause "and the suite's counts are not given" when it made the same
refusal for an unread line. `UNPLACED` did not get it, and
`failure_lines`' docstring still says only that `UNREAD_HERE` has already
said why no count follows. `agents/sealer.md` line 131 tells the sealer
that a failing `suite` carries its counts or a no-record line. That is now
true of neither of these two shapes.

Why it is ⬜: no number is wrong and nothing is lost. A person reading the
form sees the counts line missing and must work out the reason from
`UNPLACED`. Contract §14 asks that a fix which changes what a person sees
document the change and pin it. The pin exists:
`tests/test_the_seal_is_taken_once_by_the_sealer.py` asserts `UNPLACED`
whole, so the paste below changes that assertion too.

### ⬜ 2 · Nothing removes `SCALE_FOR_OLDER_HOOKS` after 0.21

Read. The constant's comment says to remove it "in the first release after
0.21". `docs/the-broad-gate.md` line 178 says "the first release after
0.21 stops writing it". The changelog fragment says "the release after
this one stops writing it". No case, issue or `seal/follow-up.md` row
holds any of them to it (`git grep` over `seal/`, `docs/`, `changelog/`
and `.github/`, executed). If the next minor release ships with the
constant, the docs sentence becomes false and nothing turns red.

The three wordings also disagree about a patch release. Read literally, a
0.21.1 is "the release after this one", but the comment's condition ("no
installed plugin older than #853") is met as soon as the owner runs any
0.21.x.

Why it is ⬜: 0.21.0 ships correctly. The cost is a stale sentence in a
later release. The owner's rule that a proven mechanism beats a written
one before 1.0 argues for the case below, which turns red when the release
pull request moves `plugin.json` past 0.21.

### ⬜ 3 · A collect report pytest leaves off its line is still counted

Read. pytest's filter applies to every report in `stats`, collect reports
included. The recorder's `pytest_collectreport` writes a failed or skipped
collection without asking `count_towards_summary`, and `read_record`
counts it under `COLLECT_CATEGORY`. So round 1's ⬜ 5 is closed for test
reports and not for the other half of its class (contract §12). Neither
pytest 9.1.1 nor anything in this repository sets the attribute false on a
collect report. The cheapest answer is one sentence in `category_of`'s
docstring that names the half left open. A real fix would add a field to
the `collect` line and a reader for it, which is more than the case is
worth.

## What the account claimed and what I found

| Claim (spawn prompt, fix commits, overview) | Found | How |
|---|---|---|
| suite counts are withheld, and the release seal refuses, where `unplaced` is not 0 | holds | read; executed (each guard reverted turns its case red) |
| a half-suite run had `unplaced 0` | not reproduced | the sealer's run answers it |
| `signal` writes the constant 0.9 for 0.21's cycle | holds, at the one write site | read, `git grep` executed |
| the installed `seal_stamp.py --from` drew such a file, exit 0 | consistent with the installed `read_values` | read; not run, it is outside the clone |
| `category_of` returns `""` where `count_towards_summary` is false | holds; it equals pytest's filter for test reports | read (pytest 9.1.1 source); executed (the guard reverted turns its case red) |
| "nothing in the tree reads" the scale | holds | `git grep`, executed |
| the constant's comment names the release that removes it | holds as a comment; nothing enforces it (⬜ 2) | read |

## Regression tests to plant

- `tests/test_release_hygiene.py`: the version-keyed case under ⬜ 2. It
  passes at 0.20.0 and 0.21.x and goes red once `plugin.json` passes 0.21
  with the constant still present. Show it red by setting the version to
  0.22.0 in a scratch copy before planting it (contract §15).
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: the `UNPLACED`
  assertion takes ⬜ 1's clause. It is red against the current text by
  construction.

## Facts for the evidence ledger

- pytest 9.1.1 counts a report on its summary line only where
  `getattr(report, "count_towards_summary", True)` is true, and this
  applies to collect reports as well as test reports (pytest's
  terminal.py, lines 1450–1453).
- The installed 0.20.0 `Stop` hook skips a values file it cannot read
  without saying anything, and leaves it pending.

## Not verified

| Item | Who answers |
|---|---|
| The full suite, lint and typecheck at the target | the sealer, once, after the rounds |
| Whether this repository's full suite leaves any report unplaced | the sealer's run, read off its record's `end` lines |
| The three macOS shards of CI run 37728336035 | the orchestrator, from `gh pr checks 880` before the pull request is marked ready |
| The installed `seal_stamp.py --from` on a file carrying the constant | the smith's account; outside this round's clone |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding 1 is closed — the stale interpreter-registry row is gone | `tests/test_a_script_says_which_interpreter_it_needs.py#CLASSIFIED` | confirmed | executed: the module gives 22 passed in the clone; CI at the target passes on ubuntu and all four Windows shards; macOS was pending at report time |
| 🟢 | round 1's finding 2 is closed — counts are withheld on the panel and refused on the release seal where a report had no file of its own | `skills/verify/scripts/broad_gate.py#suite_counts` | confirmed | executed: each guard reverted turns its pinned case red; read: it can withhold a count pytest printed in full (green panel `exit 0`, release warning), the strict side by design |
| 🟢 | round 1's finding 3 is closed — every values file carries the constant scale | `skills/verify/scripts/broad_gate.py#signal` | confirmed | read: one write site, one dictionary; the installed 0.20.0 `read_values` takes any non-bool number; executed: the line removed turns `test_the_values_file_holds_this_runs_panel` red |
| 🟢 | round 1's finding 4 is closed — the `-x` over-strictness is named | `skills/verify/scripts/broad_gate.py#RAN_TO_ITS_END` | confirmed | read: the comment carries the sentence |
| 🟢 | round 1's finding 5 is closed — the recorder leaves out what pytest's line leaves out | `skills/verify/scripts/pytest_record/specseal_pytest_record.py#category_of` | confirmed | read: the same filter on the same report object as pytest 9.1.1's line, so no count pytest prints moves; executed: the guard reverted turns its case red |
| carried | round 1's finding 6 — a run that `pytest.exit(returncode=0)` stopped still seals with counts | `skills/verify/scripts/broad_gate.py#panel` | deferred #883 | already deferred in round 1; the overview's *Not done* names #883 |
| ⬜ 1 | a failing suite with an unplaced test loses its counts line, and `UNPLACED` does not say so as `UNREAD_HERE` does | `skills/verify/scripts/broad_gate.py#UNPLACED` | open | read: `failure_lines` prints no counts where `unplaced` is not 0; `UNPLACED`, the docstring and `agents/sealer.md` say nothing of it |
| ⬜ 2 | nothing removes `SCALE_FOR_OLDER_HOOKS` after 0.21, and three wordings disagree about which release does | `skills/verify/scripts/broad_gate.py#SCALE_FOR_OLDER_HOOKS` | open | read: a comment, `docs/the-broad-gate.md` and the changelog fragment promise it; no case or issue holds them to it |
| ⬜ 3 | a collect report whose `count_towards_summary` is false is still counted | `skills/verify/scripts/pytest_record/specseal_pytest_record.py#pytest_collectreport` | open | read: pytest 9.1.1 filters collect reports too; no known producer sets it false |
| ❓ | the full suite at the target | the `Broad gate` row in `seal/config.md` | ❓ out of verified scope | contract §2 gives the broad run to the sealer, who answers it after the rounds |
| ❓ | the three macOS shards of CI at the target | CI run 37728336035 | ❓ out of verified scope | pending at report time; the orchestrator reads `gh pr checks 880` before marking the pull request ready |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight guard modules, in a `--no-local` clone at the target | 435 passed, exit 0 |
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py` in the clone | 22 passed, exit 0 |
| four guards reverted in the clone with the Edit tool (the `unplaced` refusal in both readers, the `"scale"` line, the `count_towards_summary` guard), then the four cases that pin them | 4 failed, 6 passed, exit 1; each failure is the case that pins the guard reverted |
| the same four cases after `git checkout` restored the guards | 10 passed, exit 0 |
| `gh pr checks 880`, and `gh api …/actions/runs/37728336035` for its head SHA | head SHA 1f0d610d; lint, ledger, release, both arm-check legs, ubuntu and all four Windows shards pass; the three macOS shards pending |
| `git grep` for `write_values`, `"scale"`, the constant and its retirement, and for collect hooks in `conftest.py` files | one write site; no reader; no retirement mechanism; no conftest collector |
| the broad gate (full suite, lint, typecheck) | not yet: the sealer's, once, after the rounds |

The clone, its virtual environment and every capture under
`<scratchpad>/1791384158/round-2-own/` were deleted before this report
was handed over.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's finding 6: a run that pytest stopped with exit 0 seals with counts | #883 (already deferred in round 1) | the owner, through #883 |

## Paste-ready fixes

### ⬜ 1

```python
# skills/verify/scripts/broad_gate.py — UNPLACED takes the clause UNREAD_HERE carries
UNPLACED = (
    "{count} of the tests and collections the row's pytest reported had no "
    "file of their own and are in no list: a test a conftest or a plugin "
    "parents to the session or to a directory, a failed collection of the "
    "whole session, or a report a plugin built without its path, so the "
    "suite's counts are not given (counted as unplaced on the end line of "
    "each record under records/)"
)
```

```text
# skills/verify/scripts/broad_gate.py, failure_lines' docstring — the last
# sentence of the `suite` paragraph
    the exit is not a count. Where a record holds lines that did not parse,
    or reports with no file of their own, `UNREAD_HERE` or `UNPLACED` has
    already said why no count follows.
```

```text
# agents/sealer.md, the "Exit 1, not sealed" bullet
  A failing `suite` also carries the counts its pytest recorded, or, where
  no pytest the row ran left a record, a line saying so and that the exit
  code is not a count of failing tests; where its record holds a line that
  did not parse, or a test with no file of its own, the line that says so
  also says the counts are not given.
```

The `UNPLACED` assertion in
`tests/test_the_seal_is_taken_once_by_the_sealer.py` takes the same
clause.

### ⬜ 2

```python
# tests/test_release_hygiene.py
def test_the_scale_written_for_older_hooks_leaves_after_its_cycle():
    """#869 round 1's 🟡 3 kept a constant `scale` in every values file for
    0.21's cycle only, so a hook older than #853 still draws it. Once
    plugin.json is past 0.21 the constant goes, with its pin in
    test_the_seal_is_taken_once_by_the_sealer.py and the sentence in
    docs/the-broad-gate.md §*Where the stamp is drawn*."""
    major, minor = (int(part) for part in version().split(".")[:2])
    if (major, minor) <= (0, 21):
        return
    gate = read_text("skills", "verify", "scripts", "broad_gate.py")
    assert "SCALE_FOR_OLDER_HOOKS" not in gate
```

```text
# changelog fragment, the Removed entry — one wording with the comment
  …refuses a file without one; the first minor release after 0.21 stops
  writing it.
```

### ⬜ 3

```text
# skills/verify/scripts/pytest_record/specseal_pytest_record.py,
# category_of's docstring — one sentence after the ⬜ 5 sentence
        A collect report is not asked: no build of pytest or plugin known
        here sets `count_towards_summary` false on one, so a failed or a
        skipped collection is always counted.
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round: `rounds/round-1.md`, `rounds/round-1-fixes.md`,
`rounds/round-1-report.md`, `overview.md`, `changelog.md` and the tail of
`survivors.md` of this work item; the diff `4f44e5c9..96f6d42b` whole; the
ledger fragment's rows changed after 96f6d42b, with anchors stripped;
`skills/verify/scripts/pytest_record/specseal_pytest_record.py` lines
1–400; `skills/verify/scripts/broad_gate.py` lines 1895–1935, 2010–2100,
2785–2815, 3040–3060, 3120–3175, 3180–3310 and the `signal` hunk;
`.github/workflows/publish-release.yml` lines 15–40 and 100–150;
`agents/sealer.md` lines 100–140; `skills/verify/SKILL.md` lines 505–535;
`tests/test_the_seal_is_taken_once_by_the_sealer.py` lines 5340–5440;
`tests/test_release_hygiene.py` lines 1–35; in the installed 0.20.0
plugin, `seal_stamp.py#read_values` and `hooks/sealer-stamp.py` lines
125–175; in the clone's pytest 9.1.1, the terminal reporter's lines
355–372 and 1380–1460, and the reports module's lines 160–178.
