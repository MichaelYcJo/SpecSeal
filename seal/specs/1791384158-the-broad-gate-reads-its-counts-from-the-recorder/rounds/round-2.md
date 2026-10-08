# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — review round 2

| Field | Value |
|---|---|
| Target SHA | 1f0d610dc47d7f33413c564700d03637b78e3c72 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 880 |
| Broad gate | 5baae92f against d712a632 |
| Fixes checked by | no fixes to check |
| Fix range | `ba0bcc65c4c8be03296771ce128f442e8501947b..ba0bcc65c4c8be03296771ce128f442e8501947b`, 0 commits |
| Contract changes | none |
| New units | none |
| Fix of a fix | no |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Verifying round 2 of round 1's fixes: 4f44e5c9..96f6d42b plus the record commits, at 1f0d610d. A previous attempt at this round could not write its report, so nothing was carried from it; this round reviewed from the records and the code. The spawn asked for plain probes, with no installed hooks run under synthesized payloads, and no retry of a refused command. It named four things to judge. First, whether the unplaced refusal can remove a legitimate count, and what the panel then shows. Second, whether SCALE_FOR_OLDER_HOOKS reaches every values file. Third, whether ⬜ 5's early return can move a count pytest prints. Fourth, whether anything retires the constant after 0.21. It also ran the eight guard modules once. Facts arrived labelled. Read from the smith: the unplaced refusal, the half-suite measurement, the constant scale and the early return.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding 1 is closed — the stale interpreter-registry row is gone | `tests/test_a_script_says_which_interpreter_it_needs.py#CLASSIFIED` | confirmed | executed: the module gives 22 passed in the clone; CI at the target passes on ubuntu and all four Windows shards; macOS was pending at report time |
| 🟢 | round 1's finding 2 is closed — counts are withheld on the panel and refused on the release seal where a report had no file of its own | `skills/verify/scripts/broad_gate.py#suite_counts` | confirmed | executed: each guard reverted turns its pinned case red; read: it can withhold a count pytest printed in full (green panel `exit 0`, release warning), the strict side by design |
| 🟢 | round 1's finding 3 is closed — every values file carries the constant scale | `skills/verify/scripts/broad_gate.py#signal` | confirmed | read: one write site, one dictionary; the installed 0.20.0 `read_values` takes any non-bool number; executed: the line removed turns `test_the_values_file_holds_this_runs_panel` red |
| 🟢 | round 1's finding 4 is closed — the `-x` over-strictness is named | `skills/verify/scripts/broad_gate.py#RAN_TO_ITS_END` | confirmed | read: the comment carries the sentence |
| 🟢 | round 1's finding 5 is closed — the recorder leaves out what pytest's line leaves out | `skills/verify/scripts/pytest_record/specseal_pytest_record.py#category_of` | confirmed | read: the same filter on the same report object as pytest 9.1.1's line, so no count pytest prints moves; executed: the guard reverted turns its case red |
| carried | round 1's finding 6 — a run that `pytest.exit(returncode=0)` stopped still seals with counts | `skills/verify/scripts/broad_gate.py#panel` | deferred #883 | already deferred in round 1; the overview's *Not done* names #883 |
| ⬜ 1 | a failing suite with an unplaced test loses its counts line, and `UNPLACED` does not say so as `UNREAD_HERE` does | `skills/verify/scripts/broad_gate.py#UNPLACED` | answered | a note, left as it stands: the failure form already prints `UNPLACED` with the count before it would print the counts, so a reader learns why the counts line is missing; the stale docstring and `agents/sealer.md:131` sentence are prose; read: `failure_lines` prints no counts where `unplaced` is not 0; `UNPLACED`, the docstring and `agents/sealer.md` say nothing of it |
| ⬜ 2 | nothing removes `SCALE_FOR_OLDER_HOOKS` after 0.21, and three wordings disagree about which release does | `skills/verify/scripts/broad_gate.py#SCALE_FOR_OLDER_HOOKS` | deferred #885 | #885 — removing the constant belongs to the first release after 0.21; #885 names the constant, its pin, the docs sentence and the comment; read: a comment, `docs/the-broad-gate.md` and the changelog fragment promise it; no case or issue holds them to it |
| ⬜ 3 | a collect report whose `count_towards_summary` is false is still counted | `skills/verify/scripts/pytest_record/specseal_pytest_record.py#pytest_collectreport` | answered | a note, left as it stands: no known producer sets `count_towards_summary` false on a collect report; read: pytest 9.1.1 filters collect reports too; no known producer sets it false |
| ❓ | the full suite at the target | the `Broad gate` row in `seal/config.md` | ❓ out of verified scope | contract §2 gives the broad run to the sealer, who answers it after the rounds |
| ❓ | the three macOS shards of CI at the target | CI run 37728336035 | ❓ out of verified scope | pending at report time; the orchestrator reads `gh pr checks 880` before marking the pull request ready |

## Paste-ready fixes

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
```text
# skills/verify/scripts/pytest_record/specseal_pytest_record.py,
# category_of's docstring — one sentence after the ⬜ 5 sentence
        A collect report is not asked: no build of pytest or plugin known
        here sets `count_towards_summary` false on one, so a failed or a
        skipped collection is always counted.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_a_script_says_which_interpreter_it_needs.py:481` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2796` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:3817` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#RAN_TO_ITS_END` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/pytest_record/specseal_pytest_record.py#category_of` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#panel` | round 1's 🟡 6 — deferred |
| round-1 | `skills/verify/scripts/broad_gate.py#suite_counts` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/seal_stamp.py#admitted` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/release_seal.py#suite_counts` | round 1's 🟢 — confirmed |
| round-1 | the row in `seal/config.md` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's finding 6: a run that pytest stopped with exit 0 seals with counts | #883 (already deferred in round 1) | the owner, through #883 |
