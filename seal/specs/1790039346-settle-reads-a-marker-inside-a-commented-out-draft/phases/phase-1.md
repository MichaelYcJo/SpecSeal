# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `60d5505c` |
| Ran by | `specseal:smith` on Fable 5.1 — the agent definition names no model, the spawn passed no override, and the spawning session named its own model in the prompt |

## What this phase was asked

**The refusal path agrees with `hooks/optin.py`.** `settle.py#main` resolves
the common git directory once and hands it to `home_at(root, common)`; the
opt-out arm reads the marker with `os.path.isfile`; the module docstring says
the marker is a FILE where it names the opt-out. Findings 1 and 5 of round 3.

Verified by A1 and A7, each red against the tree at `3cdfd8ad` before the
fix was written, then `tests/test_settle_reads_before_it_removes.py` green.
Ledger rows for `main` and the two cases in this work item's fragment.

## What this phase found

**Both cases were red against the tree, as the plan predicted, and each on
the assertion the finding names.** Executed before the fix:

- A1 — a repository with no `seal/` at either place and a DIRECTORY named
  `specseal-scratch` under `.git/` was told *has opted out … Delete that file
  to turn them back on*. The assertion that fails is the one wanting *has no
  seal/specs/ at either place*.
- A7 — `git_common_dir` was called twice and `home_at` received `None`. The
  assertion that fails is `len(calls) == 1`, with two roots in the list.

After the fix the module passes, `54 passed`, exit 0 read directly; `ruff
check` and `ruff format --check` over the two files exit 0.

**How A7 counts.** The stand-in is not a rewritten `optin`: it is the real
module loaded a second time under another name, with `git_common_dir` and
`home_at` wrapped on the module object. The real `home_at` reaches
`git_common_dir` through the module global, so the counter sees the
resolver's own internal call as well as `main`'s — which is what makes the
pre-fix count two rather than one. `settle.load` is the seam, replaced only
for the `OPTIN` path; the reader path still loads the real
`unverified_check.py`.

**Nothing diverged from the spec.** The sentence added to the module
docstring names the accessor and the module whose reading it copies, so the
next reader of `settle.py`'s opt-out paragraph meets the rule where the
paragraph is, and G6 asks for no more than that.

**What phase 2 inherits.** Nothing — the phases share no surface. What phase
3 inherits is the module baseline this closed at: `54 passed` in
`tests/test_settle_reads_before_it_removes.py`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the second `git_common_dir` resolution on the refusal path | `settle.py#main`'s single `common`, handed to `home_at(root, common)` |
| `os.path.exists` as the opt-out arm's reading of the marker | `os.path.isfile`, the reading `hooks/optin.py#home_at` documents |
