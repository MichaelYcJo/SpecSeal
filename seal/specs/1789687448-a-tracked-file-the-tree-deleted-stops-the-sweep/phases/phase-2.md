# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c20ef824 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

The other four helpers of `spec.md`'s reach table, with phase 1's guard and
phase 1's fixture shape: `test_no_document_names_the_old_roots.py#tracked`,
`test_release_hygiene.py#tracked`,
`test_a_release_is_sized_by_a_criterion.py#tracked` and
`test_a_script_says_which_interpreter_it_needs.py#shipped_python` — seven
opening call sites closed in total with phase 1's two. Verified by one
`bin/test -q` over the four modules, one red-first case per helper, and the
vacuity assertions each module already carries read at their present values.

## What this phase found

**Every helper needed a second function beside it, and that is what the
opening call sites cost.** A case cannot drive a sweep at a fixture root
while the walk lives inside the `test_` function, so each module gained a
root-parameterised body — `offenders_under`, `timer_offenders`,
`restatements`, `above_the_floor` — and its `test_` function shrank to the
call and the refusal text. No refusal string changed. This is the
`Contract changes` line the round record owes: four new module-level names
and a `root` argument on five helpers, narrowing nothing.

**`test_release_hygiene.py#tracked` takes `*prefixes`, so its root is
keyword-only.** `tracked(*LOADED, root=root)` keeps the call shape every
existing caller had. The other three take `root` positionally.

**A fixture cannot use the value a sweep exempts.** The hygiene case first
planted `ILLUSTRATIVE_VERSION` as its timer and the sweep correctly reported
nothing — `timers_in` exempts that value by name, which is what its own case
two functions up asserts. The fixture uses `0.9.0` against
`RUNNING_IN_THE_FIXTURES`, both fixture values, for the reason that constant
already carries: a fixture that moves with the release proves nothing about
the release after.

**The corpora at this commit**, so a later reader can tell a shrunken corpus
from a small one. Measured by importing each module and calling its helper on
this checkout, with nothing missing:

| Helper | Files on disk | The vacuity assertion it carries |
|---|---|---|
| `test_no_real_identifiers.py#tracked_text_files` | 1484 | none — the module had no can-fail case at all before phase 1 |
| `test_no_document_names_the_old_roots.py#tracked` | 67 | `len(files) > 30`, plus two paths named |
| `test_release_hygiene.py#tracked(*LOADED)` | 74 | none of its own |
| `test_a_release_is_sized_by_a_criterion.py#tracked` | 175 | `test_the_sweep_can_fail`, over the owner |
| `test_a_script_says_which_interpreter_it_needs.py#shipped_python` | 43 | `assert files`, now inside `above_the_floor` |

**§15, how each case was shown red.** One mutation, `conftest.on_disk`'s
classifying line replaced by `present.append(rel)` — the code as it stood
before phase 1 — and restored from bytes the probe kept:

| Case | What it reported |
|---|---|
| `test_the_scan_survives_a_tracked_file_the_tree_deleted` | red |
| `test_the_timer_sweep_survives_a_tracked_file_the_tree_deleted` | red |
| `test_the_sweep_survives_a_tracked_file_the_tree_deleted` | red |
| `test_the_enumeration_survives_a_tracked_file_the_tree_deleted` | red |

Exit 1, 4 failed 62 passed, read from `returncode`. The five modules together
are 71 passed at exit 0 with the guard in place.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The inline corpus walk inside four `test_` functions | The four root-parameterised functions named above, in the same commit. The refusal text stayed in the `test_` function, so nothing a person reads moved |
| `shipped_python`'s `assert files, "git ls-files found no shipped python at all"` from the test body | `above_the_floor`, which is the only caller. The assertion is unchanged and now covers the fixture path too |
