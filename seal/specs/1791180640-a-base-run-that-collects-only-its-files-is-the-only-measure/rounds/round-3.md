# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — review round 3

| Field | Value |
|---|---|
| Target SHA | 95422c35a34cfd19651c65e25b82a1bf512ad50c |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #814 |
| Broad gate | a7941237 against cb60859d; earlier run: d7f53926 against a3aa139a |
| Fixes checked by | no fixes to check |
| Fix range | `125bd927d1506822263aa89adfa60993a370fb8f..125bd927d1506822263aa89adfa60993a370fb8f`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a later runner that collects nothing at the base passes the proof for a silent measuring runner; a regression against a3aa139a) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round over round 2's fixes (275cd1a0..d9ce4e1a), and the last round this item gets: every path to `failing on base too` at the target, enumerated; the node-id proof attacked (lines shaped like node ids, row and ini verbosity, echoing runners, two runners receiving the option, `--co`, pytest 8.1, 8.3 and 9.1.1, xdist); the routes that never meet a group; rounds 1–2's layouts and a corpus sample at the target and a3aa139a; the texts against the code; the seal.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A later runner that collects no test at the base (no test in its directory, or every test deselected) passes the proof for a silent measuring runner: zero node ids against a zero trailer, `failing on base too` where a3aa139a read `new?` / `new`; rule 3's swallow sentence is false for it | `skills/verify/scripts/broad_gate.py:2058` | deferred #815 | #815 — the run is capped; fixed post-review on this branch, and #815 is what that fix closes; executed: swallow0 and swallow-desel end to end under pytest 8.1.2, 8.3.5 and 9.1.1 at both gates; regression against a3aa139a; the fix executed with the narrow run; two cases red at 95422c35 |
| ⬜ 2 | `overview.md` says no exception to "no new permissive word" is left, and the changelog fragment's swallow bullet overstates the target | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md` | deferred #815 | #815 — the records follow the post-review fix; read; falsified by 🟡 1; a correction to the run's paperwork |
| ⬜ 3 | The `COMPANY` reason says the group's run "failed" where it collected no test (exit 5) | `skills/verify/scripts/broad_gate.py:1953` | deferred #815 | #815 — the reason's sentence follows the post-review fix; the word stays `new?`; executed: two-empty reads `COMPANY` at 95422c35 and `new?` at a3aa139a; not a regression, not permissive |
| 🟢 | round 2's blocking finding is closed — a count another file makes up no longer keeps the word | `skills/verify/scripts/broad_gate.py:2364` | confirmed | executed: cancel, cancel2, outweigh, flaky2 read `COMPANY` for every file; read: no file of a failed group reaches the proof |
| 🟢 | round 2's 🟡 2 is closed for its layout — swallow reads `MULTI_RUNNER` | `skills/verify/scripts/broad_gate.py:2058` | confirmed | executed at 95422c35; the class's remainder is 🟡 1 |
| 🟢 | round 2's 🟡 3 is closed — the `COMPANY` reason claims no count | `skills/verify/scripts/broad_gate.py:1953` | confirmed | read; ⬜ 3 is a narrower point |
| 🟢 | round 2's ⬜ 4 is closed — rule 3 names the two routes that never meet a group | `templates/config.md:333` | confirmed | read; executed: cdsub-cancel and passing-sibling as rule 3 says, equal at a3aa139a |
| 🟢 | round 2's ⬜ 5 is closed as written | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md` | confirmed | read; ⬜ 2 is this round's remainder |
| 🟢 | The node-id proof holds across pytest 8.1.2, 8.3.5, 9.1.1, row and ini verbosity, xdist and conftest output | `skills/verify/scripts/broad_gate.py:1886` | confirmed | executed: 24 proofs read None; extra node-id-shaped lines only make it stricter |
| 🟢 | The corpus sample leaks nothing, and the reverse-direction moves are to `new` where the base passes or to `new?` | `tests/test_the_seal_is_taken_once_by_the_sealer.py:5996` | confirmed | executed: 15 layouts, 29 rows at both gates |
| 🟢 | A green run is unchanged; this repository's row measures a lone failing file and reads `new?` for a group | `skills/verify/scripts/broad_gate.py:3507` | confirmed | read (no hunk in `gate`); executed (the row through `compare_at_base` in a clone) |

## Paste-ready fixes

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ def proof_refused(text, path):  (docstring)
       - **the measuring runner's session**: no `<path>: <count>` line, which
         only a runner that took its listing from the variable prints, so the
-        one session seen is the one handed `OWN_LISTING` (#789 round 2);
-        otherwise `MULTI_RUNNER`;
+        one session seen is the one handed `OWN_LISTING` (#789 round 2), and
+        at least one node id or `ERROR` line naming `path`: the run alone
+        failed the file, so its runner collected a test of it or could not
+        collect it, and a session showing neither -- one that collected
+        nothing -- is another runner's (#789 round 3); otherwise
+        `MULTI_RUNNER`;
@@ def proof_refused(text, path):  (body, after the error checks)
     errors = int(errors or 0)
     if errors > 1 or (errors == 1 and not named):
         return COLLECTED_BEYOND
+    # The run alone failed the file, so the measuring runner collected a
+    # test of it or failed to collect it. A session showing neither is
+    # another runner's, the measuring one having printed nothing the gate
+    # sees (#789 round 3).
+    if not ids and not named:
+        return MULTI_RUNNER
     return None
```
```diff
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ the proof reader's parameters (test_the_proof_needs_one_session_listing_the_file_alone)
+    # #789 round 3's 🟡 1: a measuring runner that just failed a test of
+    # the file selects it again under the same arguments, so a session
+    # that selected nothing is another runner's.
     pytest.param(
         "collecting ... collected 2 items / 2 deselected / 0 selected\n\n"
         "================== no tests collected (2 deselected) in 0.01s "
         "==================\n",
         "tests/test_two.py",
-        None,
+        "MULTI_RUNNER",
         id="everything-deselected",
     ),
@@ after test_a_measuring_runner_whose_output_the_gate_never_sees_earns_no_word
+@pytest.mark.parametrize(
+    "second, at_base, on_feature",
+    [
+        pytest.param(
+            "tests/integration",
+            {"tests/integration/test_i.py": "HELPER = 1\n"},
+            {
+                "tests/integration/test_i.py": "HELPER = 1\n\n\n"
+                "def test_i():\n    assert False\n"
+            },
+            id="the-next-runner-collects-no-test-at-the-base",
+        ),
+        pytest.param(
+            "-m slow tests/integration",
+            {
+                "pytest.ini": "[pytest]\nmarkers =\n    slow: a slow test\n",
+                "tests/integration/test_i.py": "def test_i():\n    assert True\n",
+            },
+            {
+                "tests/integration/test_i.py": "import pytest\n\n\n"
+                "@pytest.mark.slow\ndef test_i():\n    assert False\n"
+            },
+            id="the-next-runner-deselects-every-test-at-the-base",
+        ),
+    ],
+)
+def test_a_silent_measuring_runner_beside_an_empty_session_earns_no_word(
+    tmp_path, second, at_base, on_feature
+):
+    """#789 round 3's 🟡 1. The runner that measures sends its output to a
+    file, and the runner after it collects nothing at the base, so it
+    prints no line listed by file and no node id: zero ids against a
+    trailer of zero is not the measuring runner's session."""
+    row = f"{FILES_ROW} tests/unit > unit.log; {FILES_ROW} {second}"
+    repo = base_then_feature(
+        tmp_path / "repo",
+        row,
+        {"tests/unit/test_u.py": PRE_EXISTING, **at_base},
+        on_feature,
+    )
+    out = run_gate(repo, keep=tmp_path / "out")
+    assert out.returncode == 1, f"exit {out.returncode}\n{out.stdout}\n{out.stderr}"
+    gate = gate_module()
+    path = "tests/integration/test_i.py"
+    assert verdict_of(out.stdout, path) == gate.MULTI_RUNNER.format(n=1), out.stdout
```
```text
templates/config.md, rule 3 — replace:
  so where its output goes to a file and the only session seen is a later runner's, the file reads `new?`.
With:
  so where its output goes to a file and the only session seen is a later runner's, one that collected nothing at the base included, the file reads `new?`.

tests/test_the_seal_is_taken_once_by_the_sealer.py, the rule 3 sentences — replace the pinned
  "goes to a file and the only session seen is a later runner's, the file "
  "reads `new?`."
With:
  "goes to a file and the only session seen is a later runner's, one that "
  "collected nothing at the base included, the file reads `new?`."
```
```text
overview.md, Not done — replace:
  After round 2's fix pass there is none.
With:
  After round 2's fix pass round 3 found one more, a regression against a3aa139a: a silent measuring runner beside a later runner that collects nothing at the base (no test in its directory, or every test deselected) passed the proof with zero node ids. <closed at <fix commit> by requiring a node id or an ERROR line naming the file | named in rule 3 as a limit>.

overview.md, the table row "The session the proof reads" — append to Chosen:
  , and at least one node id or `ERROR` line naming the file (round 3)

changelog.md, Changed — replace:
  - a row whose measuring runner sends its output to a file, so the only
    session the extra run shows is another runner's.
With:
  - a row whose measuring runner sends its output to a file, so the only
    session the extra run shows is another runner's, one that collected
    nothing at the base included.
```

## Executed probes

| What was run | Result |
|---|---|
| The narrow module run (the five modules the prompt names, plus a probe module holding the two cases below) in the clone at 95422c35 | 730 passed, 1 skipped, 2 failed — the two probe cases, each on `failing on base too` |
| The same with 🟡 1's fix applied in the clone | 731 passed, 1 skipped, 1 failed — the `everything-deselected` parameter, which the fix flips |
| `bin/evidence-check --strict .` | not run by this round; the orchestrator reports exit 0 at the fix head |
| Rounds 1–2's layouts (A, A2, B, C, cancel, cancel2, outweigh, flaky2, swallow) and normal / lone through the gate of a3aa139a and 95422c35, pytest 9.1.1 | 95422c35: every group file `COMPANY`; C and swallow `MULTI_RUNNER`; lone on. a3aa139a: on / `new` splits, C and swallow `new` |
| swallow0 and swallow-desel through both gates under pytest 8.1.2, 8.3.5 and 9.1.1 | a3aa139a `new?` and `new`; 95422c35 `failing on base too` in all six |
| cdsub-cancel, passing-sibling, two-empty through both gates | cdsub-cancel and passing-sibling: on at both; two-empty: a3aa139a `new?`, 95422c35 `COMPANY` |
| The proof reader on real output: 8 verbosity and ini variants × 3 pytest versions, a collection error × 3 versions × plain and `-n 2`, two conftest variants | 24 + 6 proven; conftest lines → `COLLECTED_BEYOND` |
| Corpus sample: 15 `REGRESSED` layouts, each under the rows it carries, at both gates | 29 rows; target words equal the table; the only target on is N7-files, also on at a3aa139a |
| This repository's row through 95422c35's `compare_at_base` in a second clone | lone: `failing on base too`, proof one session with the node id; group of two: `COMPANY` ×2 |
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
| round-2 | `skills/verify/scripts/broad_gate.py:2362` | round 2's 🔴 1 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2035` | round 2's 🟡 2 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:1938` | round 2's 🟡 3 — fixed |
| round-2 | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md` | round 2's ⬜ 5 — fixed |
| round-2 | `skills/verify/scripts/broad_gate.py:2359` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4795` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_the_seal_is_taken_once_by_the_sealer.py:6001` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/scripts/broad_gate.py:3498` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
