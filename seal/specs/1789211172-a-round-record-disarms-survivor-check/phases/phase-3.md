# 1789211172-a-round-record-disarms-survivor-check — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `<filled by the sweep that closes the build, the way `f2c1f52` filled #361's five>` |
| Ran by | `specseal:smith` on `unknown` — the spawn prompt named no model, and this template reserves the value for the spawning session rather than letting a segment source it from its own idea of what it is |

## What this phase was asked

A case that finds every path list this module derives from git and asserts
each one is filtered or named with grounds; `whole_range`'s is the one named
exception, with the ownership argument in the message. Seen red two ways, each
restored and the tree left clean: the filter removed from `corrected`, and a
new unfiltered path-list call added to the module.

## What this phase found

**The enumeration is measured rather than declared, and the difference is the
whole point.** `spec.md` enumerates the class by construction and that
enumeration lives in prose; this case walks the module's own AST for it. The
declared classification and the measured set are compared, so the case is red
whenever they disagree — which is the state the module was in for five
releases, with the docstring asserting a class the code did not hold.

**The walk looks for the path-listing WORDS, not for the `git` helper.** A
call is a path list when any of `--name-only`, `ls-files` or `ls-tree` appears
among the string constants anywhere inside it, whichever function is being
called. That is wider than the two forms the module uses today, so a fourth
site written as a direct `subprocess.run(["git", …])` is found too. The
plan's own failure scenario for this phase was a refactor renaming the `git`
helper turning the case red for no defect; keying on the subcommand words
rather than on the helper's name removes that scenario rather than accepting
it.

**Three buckets, because the three call sites are protected three different
ways** and collapsing them would make the case pass for the wrong reason:

| Function | Bucket | Checked how |
|---|---|---|
| `corrected` | filters its own list | its body names `records_a_past_round` |
| `tracked` | filtered by its only caller | `corpus` names the predicate, **and** `corpus` is the only caller of `tracked` in the module |
| `whole_range` | the named exception | its body does **not** name the predicate, and both the grounds and the function still rest on `foreign` |

The second row's *only caller* half is what keeps the bucket honest. A second
caller of `tracked` that did not filter would be a fourth unfiltered path list
reached through a third, and the set-equality assertion alone would not see it
because `tracked` would still be accounted for.

The third row's `foreign` half is the same idea for grounds rather than for
code. The argument for leaving `whole_range` unfiltered is that filtering
could turn a legitimate declaration into `foreign` — refused and printed
rather than silently dropped. If that mechanism leaves the function, the
grounds are an argument about code that is gone, and the case says so instead
of continuing to excuse an unfiltered list.

**Seen red two ways, restored from bytes kept in the mutating script:**

| Mutation | Exit | What it said |
|---|---|---|
| the filter removed from `corrected` | 1 | ``corrected derives a path list and no longer applies `records_a_past_round` `` |
| a fourth unfiltered path-list call (`since`) added | 1 | ``the module derives a path list from git in ['corrected', 'since', 'tracked', 'whole_range'] and this case accounts for ['corrected', 'tracked', 'whole_range']. Classify the difference ['since']`` |

The second message is also the proof that the case is not vacuous: it names
the three functions the walk actually found, so the set it compares against is
a measurement and not a restatement of the constant above it.

The module compared byte-identical to the original after both, and
`tests/__pycache__` was cleared between them.

**A formatter hook removed an import the Edit tool had just written.** `import
ast` at module scope was stripped by the `PostToolUse` hook because nothing
used it yet, and the `Edit` call reported success — contract §9's argument for
an edit that can fail, arriving from the other direction: the edit landed and
was then undone by a tool downstream of it. `git status` was what caught it,
not the edit's own result. The import is in place now that the helpers below
use it; the sequence worth remembering is write the user first, the import
second.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase adds one case and three helpers, and edits nothing | none |
