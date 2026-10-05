# Post-review check — 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure

| Field | Value |
|---|---|
| Target SHA | 051d9e31 |
| Base | `release/v0.18.3` at a3aa139a |
| Range checked | `904f34f5..051d9e31` (code in b1e1fca9, records in 051d9e31) |
| Pull request | #814 (draft, `chain: capped`) |
| Ran by | specseal:warden on claude-opus-5-5 |

This is a narrow verifying pass over #815's fix, not a round. The run is
capped.

## Summary

#815 is closed for the two shapes round 3 executed. swallow0 and
swallow-desel read `MULTI_RUNNER` at 051d9e31 under pytest 8.1.2, 8.3.5 and
9.1.1. At 904f34f5 both read `failing on base too`. Round 2's swallow reads
`MULTI_RUNNER` at both heads.

The fix does not over-tighten. A lone failing file, and a lone file pytest
cannot collect, still read `failing on base too` under all three versions,
plain, under `-n 2` and at `-qqq`. This repository's own row still reads
`failing on base too` for a lone pre-existing failing file, and `COMPANY` for
a group of two. Fed as text, the only session shapes whose answer changed
between 904f34f5 and 051d9e31 are the empty session and the
all-deselected one.

One instance of #815's class is still open (🟡 1). A later runner whose own
command line sets `-o verbosity_test_cases=-1` prints node ids, just as the
measuring runner does. Beside a silent measuring runner, that session passes
the proof. Executed: a3aa139a reads `new`; 904f34f5 and 051d9e31 read
`failing on base too`, under all three versions, although the base passes
the file. b1e1fca9 did not introduce it. Round 3 named it under *What it
does not close*, but no record carries it as deferred. Rule 3 and the
changelog say the node ids are ones "no other runner prints", and the
overview says no exception is left. The fix fenced below adds no code. It
names the limit in rule 3, pins that sentence, and adds it to the
`compare_at_base` docstring.

## What was asked

The four checks named in the prompt:

- #815 closed;
- no over-tightening;
- the new condition enumerated by construction;
- the texts checked against the code at 051d9e31.

The scope is narrow. The narrow run is the two named modules.

## The new condition, by construction

Read at 051d9e31, `skills/verify/scripts/broad_gate.py:2057-2079`. The
proof accepts a session only when all of these hold:

- exactly one trailer, and no outcome line;
- no `<path>: <count>` line;
- every node id names the path, and the number of node ids equals the
  trailer's count;
- every `ERROR` line names the path;
- the trailer counts at most one error, and where it counts one, an
  `ERROR` line is present;
- since b1e1fca9, at least one node id or one `ERROR` line.

So the accepted shapes are the ones below. The table also says whether each
can come from a runner other than the measuring one. Each shape was also
fed as text to both heads' `proof_refused`.

| Shape | Accepted at 904f34f5 / 051d9e31 | Can another runner produce it? |
|---|---|---|
| S1: k ≥ 1 node ids of the path, trailer k (or k selected beside deselected) | yes / yes | **Yes, in one row shape.** The row's later runner must set `-o verbosity_test_cases=-1` on its own command line, because its command line outranks `PYTEST_ADDOPTS`. It must also collect only the path. This is 🟡 1, executed. No other pytest invocation prints node ids under the proof, because the ini and `addopts` are outranked (round 3, executed). A wrapper that forwards to two pytest processes prints two trailers. |
| S2: `ERROR <path>` (or `ERROR <path> - …`), trailer `no tests collected, 1 error` | yes / yes | **Yes**, from a later runner whose own arguments hold the path and which cannot collect it at the base (swallow-err, executed). The word is then true of the row, because that runner fails the file at the base. a3aa139a gives the same word under all three versions, so this is not a regression. |
| S3: node ids of the path and one `ERROR <path>` line, trailer counting one error | yes / yes | Not seen from pytest. A module that fails to collect yields no item, and a per-function collection error names `<path>::<name>`, which the `ERROR` check refuses as `COLLECTED_BEYOND`. Read, not executed against pytest. |
| S4: an `ERROR <path>` line beside a trailer that counts no error, with or without node ids | yes / yes | No pytest session prints it, because a collection error is always counted in the trailer. Only a non-pytest part of the row or a conftest that prints exactly that line could produce it. The condition reads the `ERROR` lines rather than the trailer's error count. `if not ids and not errors` would be the stricter form, and it would still accept S2. I found no producer, so this is not a finding. |
| empty: `no tests collected`, no id, no `ERROR` | **yes** / no (`MULTI_RUNNER`) | This is #815's swallow0. |
| all deselected: `no tests collected (2 deselected)` | **yes** / no (`MULTI_RUNNER`) | This is #815's swallow-desel. |

**Can the new condition refuse the measuring runner's own valid session?**
Only where the proof's collect-only run and the run alone collect
differently. The run alone counted at least one failing or erroring
testcase. Under the same arguments and `--collect-only`, a test the run
alone ran is collected again and gives a node id. A file pytest could not
collect gives `ERROR <path>`. A setup or teardown error belongs to a
collected test. Skips and xfails are collected tests. `-m`, `-k` and
`--deselect` select the same tests in both runs. A conftest that fails at
startup prints no trailer and was already `MULTI_RUNNER`. A row that passes
`-rN`, or `-r` without `E`, prints no `ERROR` line and was already
`COLLECTED_BEYOND` at line 2072, before the new condition (the overview
names this). I found no shape that b1e1fca9 newly refuses for the measuring
runner, and the executed lone layouts all prove. Read for the classes;
executed for the layouts below.

## Findings — from execution

### 🟡 1 — a later runner that sets `verbosity_test_cases` itself passes the proof for a silent measuring runner

Location: `templates/config.md:333` (rule 3) and
`skills/verify/scripts/broad_gate.py:2077` (`proof_refused`).

- **Regression against a3aa139a:** yes.
- **Regression against 904f34f5:** no. b1e1fca9 neither made nor touched it.

**What happens.** The row is
`python -m pytest -q -p no:cacheprovider tests/unit > unit.log; python -m pytest -q -p no:cacheprovider -o verbosity_test_cases=-1 tests/integration`.
At the base, tests/unit holds a pre-existing failure and the integration
test passes. The branch makes the integration test fail. The run alone
fails, because it collected tests/unit's failing test as well. In the proof,
the measuring runner's output goes to unit.log. The later runner's own `-o`
outranks `PYTEST_ADDOPTS`, so it prints `tests/integration/test_i.py::test_i`
and `1 test collected`. That is S1, and the proof accepts it.

The result, executed end to end through each head's gate under pytest
8.1.2, 8.3.5 and 9.1.1:

| Gate | Word |
|---|---|
| a3aa139a | `new` |
| 904f34f5 | `failing on base too` |
| 051d9e31 | `failing on base too` |

The base passes the file under both runners.

**Why it matters.** This is #815's class: another runner's session passes
for the measuring runner's. It is the instance round 3 named under *What it
does not close*. It was not put in the round 3 record's `Deferred` table,
and no shipped text names it. Rule 3 says the measuring runner "lists node
ids no other runner prints". The `compare_at_base` docstring says what the
proof does not reach "is named in `templates/config.md` rule 3 rather than
claimed". The changelog says "Two limits are unchanged and named in rule 3".
All three are false for this row, and the word they hide is the permissive
one.

**Ordinary or contrived.** Contrived. The row has to write the very option
the gate hands its measuring runner, on a later runner, with the measuring
runner's output sent to a file. I do not know of a CI row that sets
`verbosity_test_cases` on the command line. That is why the fix below only
names the limit. Telling the two runners apart in code would need a mark
only the measuring runner prints, and that is a design question for the
owner rather than a fix this pass commissions. If the smith answers with
grounds instead, the grounds are the rarity of the row. The text still has
to stop saying the node ids are unique, because a person reads rule 3 to
decide whether to trust the word.

## Findings — from reading

### ⬜ 2 — the paperwork still says no exception is left

Locations:

- `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md:33`
  says "After #815's fix there is none".
- `changelog.md:25` in the same directory says "it lists node ids no other
  runner prints".
- `changelog.md:86` says "Two limits are unchanged and named in rule 3".

🟡 1 makes all three false at 051d9e31. These are corrections to the run's
paperwork under `seal/specs/`, so they are outside `Needs a fix`. The text
is fenced below.

### ⬜ 3 — one changelog sentence still says a group's run "failed"

Location: `changelog.md:76-77`, in the same directory: "A file of a run of
several that failed names that run."

#815's third point changed the `COMPANY` reason (`broad_gate.py:1954`), the
*New?* bullet (`skills/verify/SKILL.md:509-511`) and rule 3's group sentence
to "did not give each `new`". A group whose run collected no test reads
`COMPANY` too, so the same correction applies here. The changelog's other
group bullet ("every failing file of a run of several that fails at the
base") is in the list of rows that lost a word 0.18.2 gave. There "fails" is
the accurate case, so it stays. This is a correction under `seal/specs/`.

### ⬜ 4 — the `compare_at_base` docstring's proof paragraph names only node ids

Location: `skills/verify/scripts/broad_gate.py:2230`. It reads "one pytest
session, the measuring runner's by its node ids". The proof also accepts a
session that shows the runner by an `ERROR <path>` line, and it now refuses
an empty session. The sentence's catch-all ("anything else is
`MULTI_RUNNER` or `COLLECTED_BEYOND`") keeps the behaviour right, so this is
⬜. It is folded into 🟡 1's fenced fix, which edits the same docstring.

## Checked and holds

- **#815 closed (executed).** swallow0 and swallow-desel read
  `MULTI_RUNNER` at 051d9e31 under all three versions. At 904f34f5 they
  read `failing on base too`. At a3aa139a, swallow-desel read `new` and
  swallow0 read a3aa139a's no-summary `new?`. The kept proof at 051d9e31 for
  swallow0 holds `collected 0 items` and `no tests collected`, with no node
  id. Round 2's swallow reads `MULTI_RUNNER` at both heads and `new` at
  a3aa139a.
- **No over-tightening (executed).** Under all three versions, these read
  `failing on base too` at 051d9e31:
  - lone, plain and `-n 2`;
  - lone at `-qqq`;
  - lone-uncollectable, plain, `-n 2` and `-qqq`.

  Each kept uncollectable proof holds `ERROR tests/test_a.py` and `no tests
  collected, 1 error`. a3aa139a gives the same word, except at `-qqq`,
  where it gave its no-summary `new?`. That stricter `new?` is from before
  the work item, and the file does fail at the base.
- **This repository's row (executed).** The row is `uvx ruff check . && uvx
  ruff format --check . && bin/test -q`. It went through 051d9e31's
  `compare_at_base` in a second clone, over a base commit carrying two
  ruff-clean failing files:
  - the lone file reads `failing on base too`. Its proof shows the two ruff
    lines, one session, the node id and `1 test collected`;
  - the group of both reads `COMPANY` for each file.
- **The cases were red without the fix (executed, §15).** I removed the new
  condition in the clone. Three cases went red:
  - `everything-deselected`;
  - both parameters of
    `test_a_silent_measuring_runner_beside_an_empty_session_earns_no_word`.

  I then narrowed the condition to node ids alone. Of the
  sealer-gate module, only `an-error-naming-it` went red (1 failed, 466
  passed). The ERROR half is pinned at the unit level only, and no
  gate-level case holds it. One red case is enough to pin it, so this is not
  a finding. The clone was restored afterwards.
- **Texts against the code (read).**
  - The `COMPANY` reason (`broad_gate.py:1954-1960`) matches the group
    branch (`:2361-2365`). `COMPANY` is given whenever a group's run is not
    "tests, none failing, exit 0", and `NO_RUNNER` where no report was
    written. "Kept as suite-at-base-<k>.txt" matches the group's run name.
  - The `proof_refused` docstring (`:2037-2043`) matches its body
    (`:2074-2078`).
  - Rule 3's #815 sentence matches the code: an empty session, and the node
    id or `ERROR` line.
  - The *New?* bullet in `skills/verify/SKILL.md` matches the code.
  - The changelog's #815 bullet (`:58-60`) matches.
  - The overview's row "The session the proof reads" matches.

  The exceptions are 🟡 1 and ⬜ 2–4.
- **The ledger (read).** The R2 row gains the empty-session clause and
  re-stamps the `proof_refused` and `PROOFS` anchors. Its executed claim
  agrees with what I measured, apart from the mutation narrowed to node ids
  alone. I saw that mutation caught by one unit parameter, as the claim
  implies. `bin/evidence-check --strict .` exited 0 in the clone with this
  report staged. The orchestrator reports exit 0 over the worktree.
- **The overview's corpus claim (not re-run).** The overview says the
  corpus re-run at the head gives `failing on base too` only where a3aa139a
  gave it too. That claim covers the 46 layouts, rounds 1–3's layouts and
  the 96-run matrix. I re-ran only the eleven layouts listed under
  *Executed probes*. swallow-verb (🟡 1) is a layout outside that corpus that
  breaks the claim. The rest of the corpus is the smith's executed claim,
  and I did not open it.
- **§2 audit (read).** The broad gate is still `not yet`, and the overview
  labels the full suite, lint and typecheck `unverified`, with the sealer as
  their answerer.

## Regression tests to plant

None for 🟡 1's fix, which changes text only. The rule 3 pin below is the
case §14 asks for. To see it red, delete the new rule 3 sentence and run
`test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written`.

## Facts for the evidence ledger

- R2: the proof cannot tell the measuring runner's node ids from those of a
  later runner whose own command line sets `-o verbosity_test_cases=-1`.
  This is a third limit, permissive, and new since a3aa139a. Once rule 3
  names it, the R2 row's claim should say so.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A later runner whose own command line sets `-o verbosity_test_cases=-1` prints node ids, and beside a silent measuring runner its session passes the proof: `failing on base too` where a3aa139a read `new`, and rule 3, the docstring and the changelog say no other runner prints them | `templates/config.md:333` | open | executed: swallow-verb through three gates under pytest 8.1.2, 8.3.5 and 9.1.1; regression against a3aa139a, not against 904f34f5; named by round 3's report and carried by no record |
| ⬜ 2 | The overview says no exception is left, and the changelog says the node ids are unique and the limits are two | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/overview.md:33` | open | read; falsified by 🟡 1; a correction to the run's paperwork |
| ⬜ 3 | The changelog's reasons paragraph still says a group's run "failed" | `seal/specs/1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure/changelog.md:76` | open | read against `broad_gate.py:2361-2365`; a correction to the run's paperwork |
| ⬜ 4 | The `compare_at_base` docstring names only node ids as the measuring runner's mark | `skills/verify/scripts/broad_gate.py:2230` | open | read; behaviour right through the catch-all; folded into 🟡 1's fix |
| 🟢 | #815's blocking shapes are closed — swallow0 and swallow-desel read `MULTI_RUNNER` | `skills/verify/scripts/broad_gate.py:2077` | confirmed | executed under three pytest versions at three gates; red at 904f34f5 |
| 🟢 | No over-tightening — a lone failing file and a lone uncollectable file still prove | `skills/verify/scripts/broad_gate.py:2077` | confirmed | executed: plain, `-n 2`, `-qqq`, three versions; this repository's row, lone and group |
| 🟢 | The new condition changes only the empty and all-deselected shapes | `skills/verify/scripts/broad_gate.py:2057` | confirmed | executed: ten shapes fed to both heads' `proof_refused`; read for the measuring runner's own sessions |
| 🟢 | The `COMPANY` reason, the *New?* bullet and rule 3's #815 sentence match the code | `skills/verify/scripts/broad_gate.py:1954` | confirmed | read |
| 🟢 | The #815 cases were seen red without the fix | `tests/test_the_seal_is_taken_once_by_the_sealer.py:5616` | confirmed | executed: 3 failed with the condition removed; `an-error-naming-it` red with it narrowed to node ids |

## Executed probes

| What was run | Result |
|---|---|
| The two named modules in a clone at 051d9e31 | 563 passed, 1 skipped |
| swallow0, swallow-desel, swallow through the gates of a3aa139a, 904f34f5 and 051d9e31, under pytest 8.1.2, 8.3.5 and 9.1.1 | 051d9e31: `MULTI_RUNNER` in all nine. 904f34f5: `failing on base too` for swallow0 and swallow-desel, `MULTI_RUNNER` for swallow. a3aa139a: no-summary `new?`, `new`, `new` |
| lone, lone `-n 2`, lone `-qqq`, lone-uncollectable plain / `-n 2` / `-qqq`, same gates and versions | `failing on base too` at 904f34f5 and 051d9e31 in all 36; a3aa139a the same except its no-summary `new?` at `-qqq` |
| swallow-err (a later runner that cannot collect the file at the base), same gates and versions | `failing on base too` at all three gates, all three versions |
| swallow-verb (a later runner that sets `-o verbosity_test_cases=-1`), same gates and versions | a3aa139a `new`; 904f34f5 and 051d9e31 `failing on base too`, all three versions |
| Ten session shapes fed as text to `proof_refused` at 904f34f5 and 051d9e31 | only the empty session and the all-deselected one changed, accepted to `MULTI_RUNNER` |
| This repository's row through 051d9e31's `compare_at_base`, in a second clone over a base commit with two ruff-clean failing files | lone: `failing on base too`, proof with one session and the node id; group: `COMPANY` for both |
| The sealer-gate module with the new condition removed, then narrowed to node ids | removed: 3 failed (the #815 cases); narrowed: 1 failed, 466 passed (`an-error-naming-it`) |
| `bin/evidence-check --strict .`, then the identifier module and the one-word-one-meaning module, in the clone at 051d9e31 with this report staged | exit 0; 5 passed; 19 passed. Not re-run over the worktree; the orchestrator reports exit 0 there |
| Broad gate: the full suite, lint and typecheck after the rounds | not yet — not run by this pass; the sealer's, once the run settles |

## Paste-ready fixes

### 🟡 1 — name the third limit in rule 3, pin it, and say it in the docstring

```text
templates/config.md, rule 3 — after:
  Both are as they were before the proof run existed.
Insert:
  A third came with the proof run: a later runner whose own command line sets `-o verbosity_test_cases=-1` lists node ids as the measuring runner does, so where the measuring runner's output goes to a file and that later runner collects only the file, the file can read `failing on base too` though the base passes it. A row earns the measured word back by leaving that option to the gate.
```

```diff
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ test_the_measurement_its_cost_and_its_limits_are_told_where_the_row_is_written (the sentences rule 3 must carry)
         "And where a row runs pytest twice and the base passes the file under "
         "the runner a prefix reaches first, the file reads `new` from that "
         "runner.",
+        # #815's post-review check: node ids are not the measuring runner's
+        # alone where a later runner sets the option itself.
+        "A third came with the proof run: a later runner whose own command "
+        "line sets `-o verbosity_test_cases=-1` lists node ids as the "
+        "measuring runner does, so where the measuring runner's output goes to "
+        "a file and that later runner collects only the file, the file can "
+        "read `failing on base too` though the base passes it.",
     ):
         assert sentence in text, f"rule 3 does not carry: {sentence}"
```

```diff
--- a/skills/verify/scripts/broad_gate.py
+++ b/skills/verify/scripts/broad_gate.py
@@ def compare_at_base (docstring, **The proof pass.**)
-    output: one pytest session, the measuring runner's by its node ids,
-    listing the file and nothing else, gives `failing on base too`; a
+    output: one pytest session, the measuring runner's by its node ids or
+    by an `ERROR` line naming the file, listing the file and nothing else,
+    gives `failing on base too`; a session showing neither is another
+    runner's that collected nothing (#815), and reads `MULTI_RUNNER`; a
@@ def compare_at_base (docstring, **What it does not reach**)
     branch passes is never run at the base, so what it gives the file in the
     row is not seen there either.
+    And a later runner whose own command line sets `-o
+    verbosity_test_cases=-1` lists node ids as the measuring runner does,
+    so beside a measuring runner whose output went to a file its session
+    passes the proof; this one is new with the proof pass.
```

### ⬜ 2 — the paperwork (a correction)

```text
overview.md, Not done — replace:
  After #815's fix there is none.
With:
  After #815's fix there is one, named in rule 3: a later runner whose own command line sets `-o verbosity_test_cases=-1` lists node ids as the measuring runner does, and beside a measuring runner whose output goes to a file it passes the proof (swallow-verb: a3aa139a `new`, the head `failing on base too`, under pytest 8.1.2, 8.3.5 and 9.1.1).

changelog.md, line 25 — replace:
  file, so it lists node ids no other runner prints.
With:
  file, so it lists node ids no other runner prints unless that runner sets the option on its own command line.

changelog.md, line 86 — replace:
  Two limits are unchanged and named in rule 3.
With:
  Three limits are named in rule 3, and two of them are unchanged. The third is new: a later runner whose own command line sets `-o verbosity_test_cases=-1` lists node ids as the measuring runner does, and can give a file the base passes `failing on base too`.
```

### ⬜ 3 — the changelog's group sentence (a correction)

```text
changelog.md, lines 76-77 — replace:
  A file of a run of several that
  failed names that run.
With:
  A file of a run of several that
  did not give each `new` names that run.
```

Needs a fix: yes — 🟡 1 (rule 3, its pin and the `compare_at_base` docstring do not name a later runner that sets `-o verbosity_test_cases=-1` itself; a regression against a3aa139a in that row shape, not introduced by b1e1fca9; text-only fix)
Loses a record or crashes: no

## Proof block

Opened and read at 051d9e31:

- `skills/verify/scripts/broad_gate.py`, lines 1870-2084 and 2178-2400;
- the diff of b1e1fca9: `skills/verify/SKILL.md` (495-520),
  `templates/config.md` rule 3, and
  `tests/test_the_seal_is_taken_once_by_the_sealer.py` (30-50, 686,
  700-802, 860-960, 3960-4030, 5390-5400, 5560-5640, 6196-6300);
- the diff of 051d9e31, which is the ledger fragment's R2 row, plus
  `changelog.md`, `overview.md` (1-80) and `phases/phase-2.md`;
- `rounds/round-3-report.md` and `rounds/round-3.md` (the `Deferred` table);
- issue #815's body.

Every probe ran in a clone or a fixture under the scratchpad's work-item
directory, and that directory was removed afterwards. The base-comparison
scratch worktrees were checked as removed.
