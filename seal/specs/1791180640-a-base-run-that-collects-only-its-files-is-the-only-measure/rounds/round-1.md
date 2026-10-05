# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — review round 1

| Field | Value |
|---|---|
| Target SHA | cdb578958f9a8be5c92e6389903b3627db367767 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #814 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `165a6ca85e9e8ac72232163e9d42db24fe8ff809..36e5fb46f7a3d5565491a23ef51fe326331fa5fe`, 5 commits |
| Contract changes | none |
| New units | COMPANY (depth 1); RAN_RE (depth 1); PRE_EXISTING (depth 1); TEARDOWN_FAILS (depth 1); test_a_file_the_base_fails_only_alone_is_not_called_failing_on_base_too (depth 1); BOX (depth 1); BOXED (depth 1); test_a_first_runner_without_the_gates_environment_costs_the_word (depth 1) |
| Needs a fix | yes — 🔴 1 (a file the base fails only alone reads failing on base too) and 🔴 2 (a first runner without the gate's environment hands the measurement to the next runner) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Spec compliance first against `spec.md` (a solo base run per failing candidate, read for counts only; a collect-only proof pass of the whole row before the permissive word; `MULTI_RUNNER` from the trailer count; multi-file groups giving only `new`), then quality: every code path to `failing on base too`, enumerated and attacked (the proof pass's parse across pytest versions and plugins, the row's shape, the solo run against the proof); the phase-2 corpus sampled at the target, a3aa139a and fb698f90; the overview's three divergences; the stricter rows rule 3 names; the seal.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A file the base passes beside the other failing files and fails alone (sibling `sys.path`, sibling state, a session teardown error) reads `failing on base too`; a3aa139a gave `new` | `skills/verify/scripts/broad_gate.py:2291` | **fixed** `fd98c2c8` | fixed at fd98c2c8; executed: layouts A, A2, B through three gates' `compare_at_base`; four regression cases red at cdb57895; regression against a3aa139a |
| 🔴 2 | A first runner without the gate's environment (container-style) is passed over, the host runner after it measures, and its proof sees one trailer: `failing on base too` where a3aa139a gave `new`; rule 3's "as they were before" is false for it | `skills/verify/scripts/broad_gate.py:2008` | **fixed** `fd98c2c8` | fixed at fd98c2c8; executed: layout C (emulated box) through three gates; regression against a3aa139a |
| ⬜ 3 | Rule 3's `pytest -q tests` example reads `new?` only under pytest 9; 8.1–8.3 collect only the handed file and the word is measured | `templates/config.md:333` | **fixed** `fd98c2c8` | fixed at fd98c2c8; executed: proof reader over 8.1.1, 8.3.5, 9.1.1 |
| ⬜ 4 | PR body says no exception outside S3–S5; phase 2 records two and this round adds more | PR #814 body | answered | corrected at 3742b12c: `overview.md` and `phases/phase-2.md` say the only exception left is the S3–S5 shape; the pull request body is corrected by the orchestrator; read; the orchestrator owns the body |
| ❓ | Two `failing on base too` gains outside the S3–S5 shape (warnings-only group; interrupted group's `test_two`) | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4752` | ❓ out of verified scope | each is true for the file alone and the first is the row's own truth; whether the acceptance rule admits them is the orchestrator's call against the owner's rule; the strict variant of fix 1 reverts both (measured: 3 failed, 498 passed) |
| 🟢 | The proof reader: one trailer, names, sum, errors, colour, deselection, `-n 2` | `skills/verify/scripts/broad_gate.py:1979` | confirmed | executed across pytest 8.1.1, 8.3.5, 9.1.1, 13 shapes each |
| 🟢 | The planted corpus leaks nothing and matches phase 2's table | `tests/test_the_seal_is_taken_once_by_the_sealer.py:5814` | confirmed | executed: 53 of 55 parameters, 64 file words, at a3aa139a, fb698f90, cdb57895 |
| 🟢 | A green run is unchanged; this repository's row hands pytest only the file | `skills/verify/scripts/broad_gate.py:3434` | confirmed | read: no hunk in `gate`; `.github/scripts/run_tests.py:644` uses `argv or ["tests"]`; S18 carried |

## Paste-ready fixes

```diff
@@ -1929,6 +1929,28 @@
     "collected-at-base-{n}.txt), so the gate cannot tell which runner the "
     "failure is from. A row earns the measured word by running pytest once"
 )
+# Formatted with the number of the file's run alone. A file of a group of
+# several that the base fails alone, where the group's run at the base failed
+# fewer tests than its files fail one by one: some file fails alone and not
+# beside the others (a module another one puts on `sys.path`, state another
+# one sets, a session fixture's error pytest gives the last test of each
+# session), and a count does not say which.
+COMPANY = (
+    f"{NOT_MEASURED}: the base fails this file run alone, but the run of the "
+    "failing files together at the base failed fewer tests than they fail one "
+    "by one (kept as suite-at-base-<k>.txt and suite-at-base-<k>-{n}.txt), so "
+    "the failure alone may not be the base's failure in the row"
+)
+# pytest's outcome line, for a session that RAN tests: `1 passed in 0.01s`,
+# `== 1 failed, 2 passed in 0.12s ==`. Under the proof pass no session that
+# received `PYTEST_ADDOPTS` runs a test, so this line is a runner started
+# without the gate's environment (`tox`, `env -i`, a container), and the
+# trailer count cannot see it.
+RAN_RE = re.compile(
+    r"^=*[ ]*\d+ [a-z]+(?:, \d+ [a-z]+(?: [a-z]+)?)* in \d+(?:\.\d+)?s"
+    r"(?: \(\d+:\d\d:\d\d\))?[ ]*=*$",
+    re.M,
+)


 def report_counts(data):
@@ -2005,7 +2027,7 @@
     """
     plain = COLOUR_RE.sub("", text)
     trailers = list(COLLECTED_RE.finditer(plain))
-    if len(trailers) != 1:
+    if len(trailers) != 1 or RAN_RE.search(plain):
         return MULTI_RUNNER
     alone, selected, errors = trailers[0].groups()
     collected = int(alone or selected or 0)
@@ -2227,6 +2249,9 @@
         if len(others) == 1:
             work.append((others, None))
         verdicts, number, n = {}, {}, 0
+        # A group of several that went file by file, with its report's
+        # `(tests, failing)`, and each of its files' `(tests, failing)` alone.
+        together, alone_counts = None, {}
         for group, proving_at in work:
             if proving_at is not None:
                 (path,) = group
@@ -2288,9 +2313,11 @@
                 if tests and not failing and code == 0:
                     verdicts.update({f: NEW for f in group})
                 else:
+                    together = (group, tests, failing)
                     work += [([f], None) for f in group]
                 continue
             (path,) = group
+            alone_counts[path] = (tests, failing)
             if failing:
                 work.append((group, prefix))
             elif (code == 0 and tests) or (
@@ -2299,6 +2326,23 @@
                 verdicts[path] = NEW
             else:
                 verdicts[path] = NOT_ENDED.format(code=code, kept=f"{name}.txt")
+        # A run alone measures the file without the others, and the branch ran
+        # it beside them. Where the group ran every test its files hold alone
+        # and still failed fewer than they fail one by one, some failure alone
+        # is not the base's failure beside the others, and no count says
+        # whose: every word the group's files earned alone falls back to
+        # `new?`. A group that ran fewer tests (stopped, interrupted, handed a
+        # path it lacks) ran some file in no company, and says nothing.
+        if together is not None:
+            group, tests, failing = together
+            counts = [alone_counts.get(f) for f in group]
+            if None in counts or (
+                tests >= sum(t for t, _ in counts)
+                and failing < sum(x for _, x in counts)
+            ):
+                for f in group:
+                    if verdicts[f] == ON_BASE:
+                        verdicts[f] = COMPANY.format(n=number[f])
         return {f: verdicts[f] for f in files}
     finally:
         subprocess.run(
```
```text
Replace:
  Two limits still read a word the gate did not measure. **A second runner the proof run does not reach, or reaches without the gate's environment** — one started by `tox`, `nox`, `env -i` or a container, one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq` — leaves the row read as one with a single runner, so a file a later runner named can read `failing on base too` from the measuring runner's directory.

With:
  A runner started without the gate's environment — by `tox`, `nox`, `env -i` or a container — runs its tests during the proof run, and the outcome line it prints counts as a second session, so the file reads `new?`, whichever runner comes first. A file the base fails alone, from a group of failing files that ran every test together at the base and failed fewer than they fail one by one, reads `new?` too: some file there fails alone and not beside the others, and no count says which. Two limits still read a word the gate did not measure. **A second runner the proof run does not reach, or that prints nothing it can read** — one behind `\|\|`, one behind a part that exits non-zero under collection alone, one at `-qqqq`, one started without the gate's environment at `-qq` or quieter — leaves the row read as one with a single runner, so a file a later runner named can read `failing on base too` from the measuring runner's directory.
```

## Executed probes

| What was run | Result |
|---|---|
| Narrow module run in the clone at cdb57895, the five modules the prompt names | 716 passed, 1 skipped, exit 0 |
| `bin/evidence-check --strict .` in the clone at cdb57895 | exit 0 |
| Layouts A, A2, B, C plus two controls (normal; S3–S5 inner run under `-rN -s`) through a3aa139a, fb698f90, cdb57895 and the patched gate | A/A2 `test_b`, B `test_a`, C `test_two`: target `failing on base too`, a3aa139a `new`; patched gate `new?` for all four; controls unchanged across gates except S3–S5's accepted `new` → `failing on base too` |
| Planted corpus, 53 of 55 parameters (N3's symlink pair skipped), three gates | 64 file words; no target `failing on base too` where a3aa139a was stricter |
| Proof reader over real collect-only output, pytest 8.1.1 / 8.3.5 / 9.1.1 × 13 shapes | as expected everywhere; `-qqqq` → `MULTI_RUNNER`; error under `-rN` → beyond; `tests tests/test_two.py` proven under 8.x (pytest collected only the file) |
| Patched gate against the gate's three modules | 597 passed, 1 skipped |
| Strict variant of the patch (no `tests >=` guard) against two modules | 3 failed (the two ❓ gains, two params of one), 498 passed |
| The four regression cases above | red at cdb57895 (4 failed on the permissive word), green with the patch (4 passed) |
| Broad gate: the full suite, lint and typecheck after the rounds | not yet — not run by this round; the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
