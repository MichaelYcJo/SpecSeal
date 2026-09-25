# 1790297086-the-broad-gate-says-what-ci-says — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 190f4796 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#499. Phase 4 had these parts:

- The no-workflow case asserts on `` `release` ``, `gate.WORKFLOW` and every
  `PARTITION` step name, and its strip list goes.
- M2 is measured before the edit and after it. The module runs from a
  scratch copy of the tree under a directory whose name holds `release`.
  It is a copy, never a worktree left behind.
- The red direction: `coverage_line` forced to return a line, and the case
  goes red.
- The changelog fragment is closed, and `overview.md` is written.

## What this phase found

- **M2 is green before the edit.** The case passed from a copy of 73f8fded
  under `release-m2/`, with the copy's own virtualenv (1 passed).
  1404b3a7 (#549) had already cut `sys.executable` and the gate's realpath
  out of the stream, and those were the two paths through which a
  `release` directory reached it. The edit was made anyway, as `questions.md`
  M2's default said. The strip list was a list of echoed paths kept by hand,
  and the next echoed path would have reopened it.
- **Forcing `coverage_line` alone does not reach a run with no workflow.**
  `gate` calls it only when a workflow was read. So the red direction forced
  both the call and a line from it. That is what "a gate that prints the line
  unconditionally" means. It went red on `` `release` ``, and again with the
  line naming only the workflow's path. A step name printed alone went red
  too, so each needle class is held.
- **Two ledger rows cite this case, and they drifted differently.**
  `0.12.2.md` G7 anchors on it, drifted, and was re-read and re-stamped.
  `0.15.1.md` G2 names it in prose only. Its note was re-read and it still
  holds.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the strip list (`str(tmp_path)`, the gate's realpath, `sys.executable`) and the bare-word `release` search in the no-workflow case | the same case, as assertions on the names of the release job |
