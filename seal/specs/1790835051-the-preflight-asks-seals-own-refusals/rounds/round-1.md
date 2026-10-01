# 1790835051-the-preflight-asks-seals-own-refusals — review round 1

| Field | Value |
|---|---|
| Target SHA | 6a93a5520f628e445ba277177bbbe62c3e3999f4 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 714 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1, `seal --check` passes three refusals the write path raises in `field_index`, `cell` and `hiders_close`, which the sealer then raises after its suite |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 targets `6a93a552`, a merge of `821e592d` onto the build's tip `3eacc85f`; the build's diff is `e83db346..3eacc85f`. It was asked to check stage 1 against `spec.md` S1–S12 and the approved plan, then quality, on five things. First, whether `seal --check` raises every refusal `seal` raises before the write, in the same order and words, and never writes or prints `round-record: sealed`. Second, the preflight's ask and its skip paths, in both directions. Third, the build's divergences from the frame. Fourth, whether each new case fails on its defect. Fifth, the re-stamped records and the merge's resolution.

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
