# 1790835051 — review round 1 report

Ran by `specseal:warden on claude-opus-5-5`, at `6a93a5520f628e445ba277177bbbe62c3e3999f4`
(the merge of `release/v0.17.0` @ `821e592d` onto the build's tip `3eacc85f`),
in a `git clone --no-local` of the repository checked out at that SHA. The
worktree was only read, and the one file written in it is this report.

## In one view

```
seal --check stops at the six `raise` sites of seal() + seal_home's      (the spec's seven)
        |
        +-- but three more refusals sit BELOW its return, inside callees:
        |     field_index (0 or 2 `Broad gate` rows) · cell (a pipe or newline)
        |     · write_record -> hiders_close (a comment the record never closes)
        |
        v
preflight: PREFLIGHT PASSED, exit 0  ->  sealer: suite runs, then seal exits 2   (🟡 1, executed)
```

Everything else the round was asked holds. The ask is placed after the arms
and does not stop on an arm's failure. It reads the exit code off the
subprocess. Its three skip paths each print their line, and the five
divergences in `overview.md` are each right. Three ⬜ are about records and
wording.

## 🟡 1 — `seal --check` passes three refusals that `seal` raises on its write path

`skills/code-review/scripts/round_record.py:4579`.

**What is wrong.** The `--check` return stands before `kept_broad_gate`. The
three calls after it each raise `Refused`, and `--check` never reaches any of them:

- `field_index(reader, lines, BROAD_GATE)` at `round_record.py:4595` refuses a
  last record with no `| Broad gate |` row, or with two.
- `cell(BROAD_GATE, value)` refuses a value carrying a pipe or a newline. The
  value includes the run the cell already holds, read back through the reader.
- `write_record` calls `hiders_close` first, which refuses a record that ends
  inside an HTML comment it never closes.

The spec counted seven refusals: the six `raise` sites of `seal()` and
`seal_home`'s. That is the count of the `raise` statements in the function's
body. It is not the count of refusals on the write path. Contract §12 asks for
the class, and these three are members of it.

**Why it matters.** It is the exact cost this work item exists to remove. The
probe ran each shape at the target:

| Shape of the last record | `seal --check` | `--preflight` | the sealer's full run |
|---|---|---|---|
| `Broad gate` row deleted | exit 0, `checked … raises no refusal` | exit 0, `PREFLIGHT PASSED` | suite ran, then exit 2, `has 0 \| Broad gate \| … \| rows` |
| `Broad gate` row twice | exit 0 | exit 0 | suite ran, then exit 2, `has 2 … rows` |
| a comment left open at the end | exit 0 | exit 0 | suite ran, then exit 2, `never closed` |

The preflight chain arm does not catch any of these either. It judges a draft,
and `chain_check.broad_gate` returns before it reads the cell when `strict` is
false.

**Which of the branch's own claims this makes false.** Four are read as of the
target:

- `seal`'s docstring at `round_record.py:4428` says the seven *are raised in the
  same order*, which is fine. But the code comment at `round_record.py:4576` says
  *Nothing below this return may raise … and a case reads this function's body
  to hold that*.
- The case it names,
  `tests/test_the_seal_is_taken_once_by_the_sealer.py#test_the_check_returns_after_the_last_refusal_and_before_the_write`,
  walks only the `ast.Raise` nodes written in `seal`'s own body. A refusal
  raised by a callee is invisible to it, so the case passes over all three.
  This is item 4's *passes for the wrong reason*: the case pins *no `raise`
  statement below the return*, and the comment reads it as *nothing below the
  return refuses*.
- `skills/code-review/orchestration.md:553` tells the orchestrator the
  preflight asks *every refusal the sealer's write would raise*.
- Ledger row R3 states the position the case pins, and the fix moves it.

**How likely this is.** `round_record.py new` writes one `Broad gate` row and
closes every comment it writes. All three shapes come from a hand edit of a
record, or a merge that keeps both sides of the row. `chain_check` names
deleting the row as an edit it was built to close (the comment beside the
absent-row branch of `broad_gate`), so the shape is anticipated rather than
hypothetical. It does not lose a record or crash. The sealer refuses with
nothing written. What is lost is one suite.

**The fix** composes the record above the return and writes it below, so the
three callees are asked under `--check` in the order `seal` asks them. The diff
under *Paste-ready fixes* was applied in the round's clone and run (see
*Executed probes*). The three new cases and the reworked position case were
each red against the target and green with the fix. 43 selected cases of the
sealer module passed with the fix in place, covering every `seal` and
preflight case. `ruff check` and `ruff format --check` passed on both files.

## ⬜ 2 — 35 re-stamped ledger rows carry no note saying #702 re-read them

`seal/releases/0.16.0.md` and the other fourteen files of `8e9528c`.

**What is wrong.** `CLAUDE.md` §*Repo rule — a change writes fragments, never
the shared file* says *"an edit drifts the row, which is re-read against that
edit and re-stamped there with a dated note"*. In `048ab6f..3eacc85f`, 47 added
ledger lines outside this item's fragment change only a hash and, where the date
cell did not already end in it, append `· 2026-10-01`. None of them names #702
or 1790835051. #638 and #666 each left a `Re-read 2026-10-01 by work item …`
note on the same rows earlier the same day. Because of that, a row #702 re-read
reads exactly like a row it never touched.

**Why it is ⬜.** Every claim was read as still holding, `evidence-check` is
clean, and nothing in the release behaves differently. What is missing is the
row recording who did the reading. `overview.md` already says it: *35 rows in 15
files re-read … none corrected*.

## ⬜ 3 — The ask reads declarations from the disk, and the chain arm reads them from HEAD

`skills/verify/scripts/broad_gate.py:2861`.

`hooks/routing.py#item_dir` walks `declarations(root)`, which is the working
tree, untracked files included.
`skills/code-review/scripts/chain_check.py#declared_for_this_branch` reads
`tracked_declarations` at HEAD (and `GITHUB_HEAD_REF` first). The gate's comment
and the module docstring call the ask's key *the key the commit gate and the
chain arm read*. That is true of the commit gate and not of the chain arm.

Here is where the two disagree (read, not executed). An uncommitted second
`routing.md` naming the same branch makes `item_dir` return `""`. The ask is
then skipped with `PREFLIGHT_NOT_ASKED`, while the chain arm sees one tracked
declaration and passes. Whatever `seal` would refuse then reaches the sealer.
The skip prints its line, so this is said rather than silent. It is also the
same direction `routing.for_branch` takes at the commit. The finding is about
the sentence. Either the comment says *the key the commit gate reads, from the
working tree*, or the ask reads tracked declarations. The first matches what
`seal` itself reads, which is the working tree.

## ⬜ 4 — The ask's stderr line calls a record a work item, and the skip line misdescribes two declarations

`skills/verify/scripts/broad_gate.py:2770` and `:2776`, read.

- Where `seal --check` passed, `home` is the record path
  (`broad_gate.py:2975`). The line reads `asked … of
  seal/specs/<id>/rounds/round-2.md, the work item declared for `feature``, and
  the appositive calls a record a work item.
- For a `straight to the PR` item, `sealed_record` returns the `broad-gate.md`
  home. That file does not exist before the sealer writes it, so the line names
  a file the reader cannot open. No preflight case covers the direct home. Only
  the subcommand's S2 case does.
- `PREFLIGHT_NOT_ASKED` ends *so there is no record here for a sealer to seal*.
  For two declarations, the problem is not that no record exists. It is that
  there is no single answer.

Each is a sentence that reads badly while the behaviour stays right, which is
why it is ⬜.

## What the prompt asked, answered

1. **The class.** The seven refusals the spec names are asked in `seal`'s
   order with `seal`'s sentences (S1 cases, read and run by the orchestrator).
   Three more are not asked (🟡 1, executed). No path under `--check` writes,
   runs `run_check`, or prints `round-record: sealed`: the return precedes
   `write_record`, and `CHECKED` and `CHECKED_NO_ROUND` both begin
   `round-record: checked` (read). The post-write `chain_check --worktree` is
   excluded by the spec's §Out, and it is judged as a draft, the same as the
   preflight's chain arm. So it adds no refusal the arm does not already ask,
   apart from the `--worktree` against HEAD difference that #638 already owns.
2. **The ask in the preflight.** `asked` is resolved at `broad_gate.py:2861`
   after the `--record` refusal and before anything runs. The ask comes after
   the `checks.items()` loop, so an arm's failure does not stop it.
   `run("seal", …)` keeps `seal.txt` and reads `r.returncode`. Skip paths: no
   declaration, two declarations, and a detached HEAD each print their line and
   write no `seal.txt`, and each has a case. `straight to the PR` is asked and
   answers `CHECKED_NO_ROUND`. **Refused but would seal:** none found. The ask
   hands `seal` the same `<HEAD> against <base commit>` the sealer's run hands
   it (`broad_gate.py:3010` against `:2968`), and the predicates are `seal`'s
   own. **Passed but would refuse:** 🟡 1, and ⬜ 3's untracked declaration.
3. **The divergences.** Each is right. The tail's wording is true of an
   unasked run. `(code, text)` keeps S10's case green, and the `Check` built
   from `<keep>/seal.txt` names the file `run` wrote. `PREFLIGHT_DETACHED` is
   pinned by its own case. Leaving the two-declaration exit to the chain arm is
   honest, because the case asserts that `seal` is absent instead. S5's
   `reset --soft HEAD~1` is needed because `generate` commits the record.
4. **The cases.** S3, S4 and S5 each assert `seal`'s own distinguishing
   sentence, not just exit 1, so none passes on another refusal. S5, for
   example, asserts `descends from`, which a `nobody` checker would not print.
   S6 fails with the ask dropped (no `seal.txt`) and with `--check` dropped
   (bytes move). The undeclared, two-declaration and detached cases each fail
   if the ask runs anyway. The exception is the position case (🟡 1).
5. **The records.** `bin/evidence-check .` exit 0, 3423 ok, 0 drifted, 0
   broken, 0 refused. `bin/correction-check` exit 0, no marker dropped at the
   one merge. The range was given as `821e592d...6a93a552`, because in the
   clone `origin/release/v0.17.0` is the local repository's branch at
   `cd24f516`, not today's base. The merge-resolved rows of `0.12.0.md` and
   `0.5.0.md` changed only their `templates/config.md` hashes (read). On the
   notes, see ⬜ 2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `seal --check` returns before three refusals the write path raises in callees — `field_index` (no `Broad gate` row, or two), `cell`, and `hiders_close` (a comment never closed) — so the preflight passes them and the sealer refuses them after its suite; the position case walks only `raise` statements and passes over all three | `skills/code-review/scripts/round_record.py:4579` | open | Executed: each of three shapes `seal --check` exit 0, preflight exit 0, the full gate ran the suite and exited 2; the fix was red-then-green in the clone |
| ⬜ 2 | 35 re-stamped ledger rows carry no dated note naming #702, which `CLAUDE.md` asks of a re-stamp | `seal/releases/0.16.0.md` | open | Read: 47 added lines outside the fragment, none names #702 or 1790835051 |
| ⬜ 3 | The ask's key is said to be the chain arm's, but `item_dir` reads declarations on disk and the chain arm reads them tracked at HEAD | `skills/verify/scripts/broad_gate.py:2861` | open | Read |
| ⬜ 4 | `PREFLIGHT_ASKED` calls a record a work item and names an absent `broad-gate.md` for a direct item; `PREFLIGHT_NOT_ASKED` says no record exists where there are two declarations | `skills/verify/scripts/broad_gate.py:2770` | open | Read |
| 🟢 | The ask runs after the arms, does not stop on an arm's failure, keeps `seal.txt` and reads the exit code off the subprocess | `skills/verify/scripts/broad_gate.py:2967` | confirmed | Read; S3/S4/S6 run by the orchestrator |
| 🟢 | The three skip paths and the direct home behave as the spec says, each with its line | `skills/verify/scripts/broad_gate.py:2984` | confirmed | Read, and the cases |
| 🟢 | No ask refuses a branch that would seal: the value and the predicates are the sealer's own | `skills/verify/scripts/broad_gate.py:2968` | confirmed | Read against `:3010` |
| 🟢 | The five divergences in `overview.md` are each right | `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/overview.md` | confirmed | Read |
| 🟢 | The new preflight cases fail on the defect each pins | `tests/test_the_seal_is_taken_once_by_the_sealer.py` | confirmed | Read; each asserts its own sentence |
| 🟢 | The ledger and correction checks are clean at the target, and `agents/sealer.md` is untouched | `seal/ledger/` | confirmed | Executed: `evidence-check .` exit 0, `correction-check` exit 0; `git diff e83db346 3eacc85f -- agents/sealer.md` empty |

## Paste-ready fixes

### 🟡 1 — compose above the return, write below it

```diff
--- a/skills/code-review/scripts/round_record.py
+++ b/skills/code-review/scripts/round_record.py
@@ -4573,14 +4573,6 @@ def seal(args):
                 "Run it again at the tree as it stands; no cell was written"
             )
 
-    # `--check` (#702): every refusal above was asked and none fired. Nothing
-    # below this return may raise — it is where the write starts — and a case
-    # reads this function's body to hold that.
-    if args.check:
-        said = CHECKED_NO_ROUND if n is None else CHECKED
-        print(said.format(path=os.path.relpath(path, root), dash=DASH))
-        return 0
-
     # ONE ENTRY PER RUN, NEWEST FIRST (#174). A run the cell already holds is
     # kept behind the new one as `earlier run`, because a second broad run --
     # after a pre-existing failure, or after the last fixes landed -- used to
@@ -4588,14 +4580,31 @@ def seal(args):
     # The newest entry alone is replaced, where it is the same commit against
     # the same base (`same_run`).
     # `kept_broad_gate` is the one path, shared with `close --broad-gate`.
+    #
+    # The record is COMPOSED here and written below the `--check` return, so
+    # the write path's own refusals are asked under `--check` too (#702):
+    # `field_index` (no `Broad gate` row, or two), `cell` (a pipe or a
+    # newline in the value) and `hiders_close` (a comment the record never
+    # closes). Each is a `Refused` raised by a callee, so no `raise` in this
+    # body shows it.
     value = kept_broad_gate(reader, rows, args.broad_gate)
     if n is None:
-        write_record(reader, path, new_broad_gate_file(item, value))
+        composed = new_broad_gate_file(item, value)
     else:
         i = field_index(reader, lines, BROAD_GATE)
         raw[i] = cell(BROAD_GATE, value)
         ending = "\n" if text.endswith("\n") else ""
-        write_record(reader, path, "\n".join(raw) + ending)
+        composed = "\n".join(raw) + ending
+    hiders_close(reader, composed, RECORD_HIDERS)
+
+    # `--check` (#702): every refusal above was asked and none fired. What
+    # follows is the write and the chain check, and neither is asked here.
+    if args.check:
+        said = CHECKED_NO_ROUND if n is None else CHECKED
+        print(said.format(path=os.path.relpath(path, root), dash=DASH))
+        return 0
+
+    write_record(reader, path, composed)
     print(
         f"round-record: sealed {os.path.relpath(path, root)} {DASH} `{BROAD_GATE}` | {value}"
     )
```

The docstring paragraph at `round_record.py:4428` then says where the return
is and what stands above it:

```text
    **`--check` asks every refusal above and writes nothing** (#702). The
    seven — the six here and `seal_home`'s — are raised in the same order
    with the same sentences, and so are the three the write path's callees
    raise: `field_index` (no `Broad gate` row, or two), `cell` (a pipe or a
    newline in the value) and `hiders_close` (a comment the record never
    closes). The record is composed above the return for that reason, and
    the return is the statement immediately before `write_record`; a case
    holds that position and a second case holds the three callees. It adds
    no `raise` site, so the count above is unchanged. The line never begins
    `round-record: sealed`, because `broad_gate.py#gate` reads that prefix
    as the cell having been written. `broad-gate --preflight` is the caller:
    it asks the sealer's own subcommand rather than restating its
    predicates, so the sealer's refusals arrive before the suite.
```

The cases. The first block goes after the S1 case. The second replaces the
head of the position case.

```diff
--- a/tests/test_the_seal_is_taken_once_by_the_sealer.py
+++ b/tests/test_the_seal_is_taken_once_by_the_sealer.py
@@ -4532,6 +4532,59 @@ def test_seal_check_refuses_what_seal_refuses_and_writes_nothing(repo, shape, sa
     assert after == before, f"`--check` wrote {path.name} under a refusal"
 
 
+def hand_edited_last(edit):
+    """A settled item whose last record `edit` rewrites and commits."""
+
+    def shape(repo):
+        _one, two = settled_item(repo)
+        two.write_text(edit(two.read_text(encoding="utf-8")), encoding="utf-8")
+        commit(repo, "the last record edited by hand")
+        return two
+
+    return shape
+
+
+def without_the_row(text):
+    return "".join(
+        line for line in text.splitlines(True) if not line.startswith("| Broad gate |")
+    )
+
+
+def with_the_row_twice(text):
+    return "".join(
+        line * (2 if line.startswith("| Broad gate |") else 1)
+        for line in text.splitlines(True)
+    )
+
+
+def with_an_open_comment(text):
+    # Spelled in two parts so no record generated from a report quoting this
+    # case carries a literal comment opener.
+    return text + "\n<" + "!-- left open by hand\n"
+
+
+@pytest.mark.parametrize(
+    "edit, said",
+    [
+        (without_the_row, "has 0 `| Broad gate | … |` rows"),
+        (with_the_row_twice, "has 2 `| Broad gate | … |` rows"),
+        (with_an_open_comment, "never closed"),
+    ],
+    ids=["no-row", "two-rows", "open-comment"],
+)
+def test_seal_check_refuses_what_the_write_path_refuses(repo, edit, said):
+    """S1's class, past the six `raise` sites: `field_index`, `cell` and
+    `hiders_close` refuse on the write path, inside callees. `--check`
+    exited 0 on each while `seal` refused it after the sealer's suite."""
+    path = hand_edited_last(edit)(repo)
+    before = read_bytes(path)
+    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base", CHECK_FLAG)
+    assert code == 2, out
+    assert said in out, out
+    assert "chain-check:" not in out, out
+    assert read_bytes(path) == before
+
+
 def settled_last(repo):
     return settled_item(repo)[1]
 
@@ -4588,15 +4641,24 @@ def test_the_check_returns_after_the_last_refusal_and_before_the_write():
     keep = [
         i
         for i, statement in enumerate(seal.body)
-        if isinstance(statement, ast.Assign)
+        if isinstance(statement, ast.Expr)
         and isinstance(statement.value, ast.Call)
-        and ast.unparse(statement.value.func) == "kept_broad_gate"
+        and ast.unparse(statement.value.func) == "write_record"
     ]
-    assert len(keep) == 1, f"`seal` calls `kept_broad_gate` {len(keep)} times"
+    assert len(keep) == 1, f"`seal` calls `write_record` {len(keep)} times"
     guard = seal.body[keep[0] - 1]
     assert isinstance(guard, ast.If) and ast.unparse(guard.test) == "args.check", (
-        "the statement before `kept_broad_gate` is not the `--check` guard"
+        "the statement before `write_record` is not the `--check` guard"
     )
+    # The callees that refuse on the write path are asked above the guard.
+    above = {
+        ast.unparse(node.func)
+        for statement in seal.body[: keep[0] - 1]
+        for node in ast.walk(statement)
+        if isinstance(node, ast.Call)
+    }
+    for callee in ("kept_broad_gate", "field_index", "cell", "hiders_close"):
+        assert callee in above, f"`{callee}` is not asked above the `--check` return"
     assert isinstance(guard.body[-1], ast.Return), "the guard does not return"
     later = [
         node
```

The position case's docstring and the code comment above it should then
say *the statement immediately before `write_record`*. The comment at
`round_record.py:4576` is replaced by the diff above. Ledger row R3's claim
becomes: *the statement immediately before the `write_record` call is the
`if args.check:` guard ending in a `return`, `kept_broad_gate`,
`field_index`, `cell` and `hiders_close` are each called above it, and no
`raise` stands after it.* `skills/code-review/orchestration.md:553` is true
as written once the fix lands.

## Executed probes

| What was run | Result |
|---|---|
| A one-run probe in the clone's `tests/`, deleted after: `settled_item`, then the last record edited three ways (row deleted, row twice, comment left open), each asked by `seal --check`, `broad-gate --preflight` and `broad-gate --record` | `seal --check` exit 0 and the preflight exit 0 on all three; the full gate ran the suite and exited 2 on all three, with `has 0 … rows`, `has 2 … rows` and `never closed`; the record unchanged by the preflight |
| The 🟡 1 fix applied in the clone; `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -k "write_path or check_returns" -p no:xdist` with `round_record.py` stashed back to the target | exit 1: the three new cases and the reworked position case failed |
| The same four with the fix in place | exit 0, 4 passed |
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -k "seal_check or check_returns or test_seal_ or preflight or with_record or seal_exit or real_seals"` with the fix in place | exit 0, 43 passed |
| `uvx ruff check` and `uvx ruff format --check` on the two files the fix touches | exit 0 both |
| `bin/evidence-check .` at the target | exit 0; 3423 ok, 0 drifted, 0 broken; records 0 refused, 0 drifted |
| `bin/correction-check --range 821e592d...6a93a552 --root .` | exit 0; 1 merge examined, no correction marker dropped |
| The broad gate (full suite, repository-wide lint, typecheck) over this branch | not yet: the sealer's, once the rounds settle |

## Regression tests to plant

The cases under *Paste-ready fixes* go in
`tests/test_the_seal_is_taken_once_by_the_sealer.py` beside
`test_seal_check_refuses_what_seal_refuses_and_writes_nothing`: the three-shape
case and the reworked position case. Each was seen red against the target and
green with the fix.

A preflight-level case for one shape (a deleted `Broad gate` row, preflight
exit 1 with `seal` named) would hold the same gap from the gate's side. The
subcommand case already pins the predicate, so the preflight case is
optional.

## Facts for the evidence ledger

- R3 is rewritten as above when the fix lands, and its anchors re-stamped.
- A new row is added: *`seal --check` refuses a last record with no `Broad gate`
  row, with two, and one ending inside a comment it never closes, exit 2 with
  the write path's own sentence, nothing written*. Its anchors are
  `round_record.py#seal`, `#field_index`, `#hiders_close` and the new case.
- If ⬜ 2 is taken up, the 35 rows get one dated note each, naming #702 and
  the unit the build drifted.

## How this round was scoped

The target was the branch against today's base (`821e592d..6a93a552`). Two
code files, two test modules, four documents and the records were read. Two
module subsets ran, and only for the fix. The two changed modules were run in
full by the orchestrator (267 passed). That count is carried from the prompt
and was not re-run here. The full suite was not run, because it is the
sealer's. Round 1 has no earlier record, so nothing was inherited.

What comes due: once 🟡 1 is answered, the verifying round reads the fix, and
the sealer's spawn follows the round that closes with nothing open.

Needs a fix: yes — 🟡 1, `seal --check` passes three refusals the write path raises in `field_index`, `cell` and `hiders_close`, which the sealer then raises after its suite

Loses a record or crashes: no

## Proof block

Files opened at `6a93a552`:
`seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md`,
`overview.md`, `changelog.md`;
`seal/ledger/1790835051-the-preflight-asks-seals-own-refusals.md`;
`seal/ledger/1790815611-the-record-arms-run-before-the-sealer-is-spawned.md`;
`seal/specs/1790815611-the-record-arms-run-before-the-sealer-is-spawned/changelog.md`;
`skills/code-review/scripts/round_record.py` (`kept_broad_gate`, `same_run`,
`write_record`, `hiders_close`, `cell`, `field_index`, `where`, `run_check`,
`seal_home`, `seal`, `main`);
`skills/verify/scripts/broad_gate.py` (`load`, `branch_name`, `Check`, `run`,
`sealed_record`, `failure_lines`, `seal_record`, `gate`, the preflight
constants);
`skills/code-review/scripts/chain_check.py` (`declared_for_this_branch`,
`tracked_declarations`, `broad_gate`, `--worktree`);
`hooks/routing.py` (`declarations`, `item_dir`);
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (fixtures, the new
cases); `tests/test_broad_gate_rule.py` (the new cases);
`skills/code-review/orchestration.md`, `skills/implement/orchestration.md`,
`skills/verify/SKILL.md` and `templates/config.md`, through the diff;
`CLAUDE.md`.
