# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — review round 2

| Field | Value |
|---|---|
| Target SHA | c8d6c7858d88df8ad450bb624038a66638cded08 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #814 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (a group's count another file makes up keeps failing on base too on a regression), 🟡 2 (a measuring runner whose output never reaches the gate), 🟡 3 (the COMPANY reason is false on the no-count route) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round over round 1's fixes (165a6ca8..36e5fb46): every path to `failing on base too` at the target enumerated and attacked (the proof pass, the `COMPANY` count comparison, `RAN_RE`); round 1's layouts A, A2, B and C at the target, a3aa139a and cdb57895; the phase-2 corpus sampled, with S3–S5 words rebuilt; rule 3, the SKILL.md bullet, the reasons, the changelog and `overview.md` against the code; the seal and this repository's row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A file the base fails only alone keeps `failing on base too` when another file of its group fails more beside the others (one sibling's import-time state with two effects, or a flaky test); the sum check cannot see per file, and rule 3's "two dependencies whose counts cancel" undersells it | `skills/verify/scripts/broad_gate.py:2362` | open | executed: cancel, cancel2, outweigh, flaky2 and cancel under `-n 2` through three gates' `compare_at_base`, and cancel2 under this repository's own row in a clone; a3aa139a `new` for the regressed file each time; regression against a3aa139a; a planted case red at c8d6c785 |
| 🟡 2 | A measuring runner whose output goes to a file, followed by a runner listing only the failing file, reads `failing on base too`; rule 3 says such limits are "as they were before", and a3aa139a read `new` | `skills/verify/scripts/broad_gate.py:2035` | open | executed: the swallow layout through three gates; the proof's one session is the second runner's; regression against a3aa139a; a planted case red at c8d6c785 |
| 🟡 3 | The `COMPANY` reason says the group "failed fewer tests than they fail one by one" where it is given because a file had no count alone | `skills/verify/scripts/broad_gate.py:1938` | open | read, plus the `a-file-with-no-count-alone` parameter executed in the narrow run; not a regression (new at fd98c2c8) |
| ⬜ 4 | Rule 3 does not name the two routes that never meet a group: a file run alone from the start (the one failing file, or a `cd sub` row's candidates) and a sibling the branch passes | `templates/config.md:333` | open | executed: cdsub and passing-sibling layouts read `failing on base too` at all three gates; not a regression |
| ⬜ 5 | `overview.md` says only S3–S5 is left and that leave-one-out would see the cancel; the changelog fragment says "depend on each other both ways" | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md` | open | a correction to the run's paperwork; falsified by 🔴 1 and 🟡 2 |
| 🟢 | round 1's first blocking finding is closed for layouts A, A2, B and the no-count shape; its class's remainder is this round's 🔴 1 | `skills/verify/scripts/broad_gate.py:2359` | confirmed | executed: each reads `COMPANY` at c8d6c785, also under `-n 2` |
| 🟢 | round 1's second blocking finding is closed — a first runner without the gate's environment | `skills/verify/scripts/broad_gate.py:2035` | confirmed | executed: layout C reads `MULTI_RUNNER`; `RAN_RE` attacked on real and constructed output with no permissive gap at `-q` |
| 🟢 | round 1's ⬜ 3 is closed — rule 3's per-version example | `templates/config.md:333` | confirmed | read; pinned in the rule 3 case |
| 🟢 | round 1's ⬜ 4 is closed — the PR body's acceptance sentence is scoped to the corpus | PR #814 body | confirmed | read via `gh pr view`; ⬜ 5 is this round's remainder |
| 🟢 | round 1's ❓ is carried out — the strict variant | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4795` | confirmed | executed: the narrow run passes both changed cases |
| 🟢 | The S3–S5 shape is the base's failure | `tests/test_the_seal_is_taken_once_by_the_sealer.py:6001` | confirmed | executed: four of the 18 words rebuilt; the base fails `tests/test_err.py` by hand each time |
| 🟢 | The corpus sample leaks nothing | `tests/test_the_seal_is_taken_once_by_the_sealer.py:6001` | confirmed | executed: 15 layouts × 2 rows, 32 file words, at a3aa139a and c8d6c785 |
| 🟢 | A green run is unchanged; this repository's row measures its normal and sibling shapes right | `skills/verify/scripts/broad_gate.py:3498` | confirmed | read (no hunk in `gate`); executed (the row through `compare_at_base` in a clone) |

## Paste-ready fixes

```text
templates/config.md, rule 3 — replace:
  Two dependencies in one group whose counts cancel, one file failing only beside the others and another only alone, also leave a word standing.

With:
  **The files of a failing group are compared by counts, never one by one.** Where one file fails only alone and another fails more tests beside the others than alone, the group's count can match or pass its files' counts, and every word the files earned alone stands, a regression the base passes in the row included: one sibling's import-time state that one file needs and another trips over does it, and so does a flaky test that fails in the group's run and passes alone. 0.18.2 read such a file `new`.
```
```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ compare_at_base docstring
-    runner, also as before (this work item's `questions.md` Q1). Two
-    dependencies whose counts cancel, one file failing only beside the
-    others and another only alone, leave a group's count equal and its
-    words standing.
+    runner, also as before (this work item's `questions.md` Q1). The
+    company check compares counts and never files: where one file fails
+    only alone and another fails more beside the others than alone -- one
+    sibling's import-time state with both effects, or a flaky test that
+    fails in the group's run -- the group's count matches or passes its
+    files' counts and every word they earned alone stands (#789 round 2).
@@ the comment above the check
-        # failure in the row, and no count says whose: every word a file of
-        # the group earned alone falls back to `COMPANY`. A file with no
-        # count alone counts the same way (#789 round 1).
+        # failure in the row, and no count says whose: every word a file of
+        # the group earned alone falls back to `COMPANY`. A file with no
+        # count alone counts the same way (#789 round 1). A file that fails
+        # more beside the others makes up for one that fails only alone,
+        # and then nothing here sees it: rule 3 names it (#789 round 2).
```
```diff
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written, the sentences rule 3 must carry
+        # #789 round 2's 🔴 1.
+        "**The files of a failing group are compared by counts, never one by "
+        "one.**",
+        "one sibling's import-time state that one file needs and another trips "
+        "over does it, and so does a flaky test that fails in the group's run "
+        "and passes alone. 0.18.2 read such a file `new`.",
@@ the sentences that must be gone
+        "Two dependencies in one group whose counts cancel",
```
```text
templates/config.md, rule 3 — replace:
  **A second runner the proof run does not reach, or that prints nothing it can read** — one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq`, one started without the gate's environment at `-qq` or quieter — leaves the row read as one with a single runner, so a file another runner named can read `failing on base too` from the measuring runner's directory. And where a row runs pytest twice and the base passes the file under the runner a prefix reaches first, the file reads `new` from that runner. Both are as they were before the proof run existed.

With:
  **A runner the proof run does not reach, or that prints nothing it can read** — one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq`, one started without the gate's environment at `-qq` or quieter, one whose output goes to a file — leaves the row read as one with a single runner, so a file another runner named can read `failing on base too` from the measuring runner's directory. Where the silent runner is the one that measured and a later runner lists only the file, the proof reads the later runner's session, and the word is new: 0.18.2 read `new` there. And where a row runs pytest twice and the base passes the file under the runner a prefix reaches first, the file reads `new` from that runner, as it did before the proof run existed.
```
```diff
-        "**A second runner the proof run does not reach, or that prints "
-        "nothing it can read** — one behind `\\|\\|`, one behind a part that "
-        "exits non-zero under collection alone, one at `-qqqq`, one started "
-        "without the gate's environment at `-qq` or quieter — leaves the row "
-        "read as one with a single runner, so a file another runner named can "
-        "read `failing on base too` from the measuring runner's directory.",
+        "**A runner the proof run does not reach, or that prints nothing it "
+        "can read** — one behind `\\|\\|`, one behind a part that exits "
+        "non-zero under collection alone, one at `-qqqq`, one started without "
+        "the gate's environment at `-qq` or quieter, one whose output goes to "
+        "a file — leaves the row read as one with a single runner",
+        "Where the silent runner is the one that measured and a later runner "
+        "lists only the file, the proof reads the later runner's session, and "
+        "the word is new: 0.18.2 read `new` there.",
```
```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ -1938,6 +1938,7 @@
 COMPANY = (
     f"{NOT_MEASURED}: the base fails this file run alone, but the run of the "
     "failing files together at the base failed fewer tests than they fail one "
-    "by one (kept as suite-at-base-<k>.txt and suite-at-base-<k>-{n}.txt), so "
-    "the failure alone may not be the base's failure in the row"
+    "by one, or one of them wrote no report alone (kept as suite-at-base-<k>.txt "
+    "and suite-at-base-<k>-{n}.txt), so the failure alone may not be the base's "
+    "failure in the row"
 )
--- a/skills/verify/SKILL.md
+++ b/skills/verify/SKILL.md
@@ -508,3 +508,4 @@
   pytest more than once when the gate asked it only to collect, or the
   failing files run together at the base failed fewer tests than they fail
-  one by one. It is a
+  one by one or one of them wrote no report alone. It is a
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ test_the_unmeasured_word_says_so_and_every_reader_is_told_it
     assert gate.COMPANY.format(n=2) == (
         "new? not measured: the base fails this file run alone, but the run of "
         "the failing files together at the base failed fewer tests than they "
-        "fail one by one (kept as suite-at-base-<k>.txt and "
-        "suite-at-base-<k>-2.txt), so the failure alone may not be the base's "
-        "failure in the row"
+        "fail one by one, or one of them wrote no report alone (kept as "
+        "suite-at-base-<k>.txt and suite-at-base-<k>-2.txt), so the failure "
+        "alone may not be the base's failure in the row"
     )
@@ the SKILL.md phrases every reader is told
-        "run together at the base failed fewer tests than they fail one by one",
+        "run together at the base failed fewer tests than they fail one by one "
+        "or one of them wrote no report alone",
```
```text
templates/config.md, rule 3 — after the 🔴 1 sentence, add:
  A file that runs alone from the start meets no group to be compared with — the one failing file the base carries at the root, or every failing file of a `cd sub` row, whose paths the root's tree does not carry — and a sibling the branch passes is never run at the base, so a module or state another file gives it in the row is not seen there either, as before the proof run existed.
```
```text
overview.md, Not done — replace:
  After round 1's fix pass only one is left: the S3–S5 shape, …
With:
  After round 1's fix pass the S3–S5 shape is the one exception the corpus holds. Round 2 found two more outside it, both regressions against a3aa139a: a group whose count another file makes up (round 2's 🔴 1), and a measuring runner whose output never reaches the gate (round 2's 🟡 2).

overview.md, Not done — replace:
  A leave-one-out run, the group without each file, would see it at one more run per file the base fails alone;
With:
  A leave-one-out run does not see it either: in a two-file group the group without one file is the other file alone, and a flaky test defeats any rerun. Only a per-file answer from the group's own run would, and the report's names are the one such answer, which #812 stopped reading;

changelog.md — replace:
  One new limit is named beside them: in a group whose files depend on each other both ways, so that the counts cancel, the words stand.
With:
  One new limit is named beside them: the files of a failing group are compared by counts, so where one file fails only alone and another fails more beside the others — one sibling's import-time state, or a flaky test — the words they earned alone stand.
```

## Executed probes

| What was run | Result |
|---|---|
| The narrow module run in the clone at c8d6c785, the five modules the prompt names | 725 passed, 1 skipped, exit 0 |
| `bin/evidence-check --strict .` in the clone at c8d6c785 | exit 0 |
| Round 1's layouts A, A2, B, C and the normal control through `compare_at_base` of a3aa139a, cdb57895 and c8d6c785 (pytest 9.1.1) | A/A2: on, `new` → on, on → `COMPANY` ×2; B: `new`, on → on, on → `COMPANY` ×2; C: `new` → on → `MULTI_RUNNER`; normal: on/`new` at all three |
| cancel, cancel2, outweigh, flaky2, cancel under `-n 2` through the same gates | the regressed test_b: a3aa139a `new`, c8d6c785 `failing on base too` in each; cancel2 and flaky2 put the word on all three files |
| This repository's row (`uvx ruff check . && uvx ruff format --check . && bin/test -q`) through c8d6c785's `compare_at_base` in a clone: normal, sibling on the path, cancel2 | on/`new`; `COMPANY` ×2; `failing on base too` ×3, with the base's group run passing the regressed file (`3 failed, 1 passed`) |
| The swallow row through three gates | a3aa139a `new`; cdb57895 and c8d6c785 `failing on base too`; the proof's one session is the second runner's |
| cdsub (`cd sub` row, ini in `sub`), passing-sibling, xdist-A, xdist-B, `-x` | cdsub and passing-sibling: on at every gate (⬜ 4); xdist-A: `COMPANY` at c8d6c785; xdist-B: on at every gate, the base's truth there; `-x`: a group of one |
| S3–S5 rebuilt: Axis A's inner `tests/test_g.py`, under `-q -rN` (stderr), `-q -rN` (stdout), `-q -n 2 -rN` (stderr), and a stderr inner run under `-q -s` | `tests/test_err.py`: a3aa139a `new`, c8d6c785 `failing on base too`; by hand at the base it exits 1 (`1 failed`) |
| Corpus sample: 15 `REGRESSED` layouts × own and files-only rows, at a3aa139a and c8d6c785 | 32 file words, no leak, every target word equal to the planted table's |
| `proof_refused` at c8d6c785 on outcome-line shapes, and a real pseudo-terminal capture via `script` | `-q`, ruled and pytest-sugar lines → `MULTI_RUNNER`; uv, tox, `files checked`, `no tests ran` → proven; raw `\r\n` would be proven, and `run`'s text mode removes it before the reader |
| The two cases under *Regression tests to plant*, in the clone at c8d6c785 | 2 failed, each on the permissive word |
| Broad gate: the full suite, lint and typecheck after the rounds | not yet — not run by this round; the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:2291` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:2008` | round 1's 🔴 2 — fixed |
| round-1 | `templates/config.md:333` | round 1's ⬜ 3 — fixed |
| round-1 | PR #814 body | round 1's ⬜ 4 — answered |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4752` | round 1's ❓ — out of verified scope |
| round-1 | `skills/verify/scripts/broad_gate.py:1979` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:5814` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py:3434` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
