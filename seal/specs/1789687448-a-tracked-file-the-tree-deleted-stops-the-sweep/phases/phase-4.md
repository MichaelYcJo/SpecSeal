# 1789687448-a-tracked-file-the-tree-deleted-stops-the-sweep — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 073fcb26 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

The class reader: no scope in `tests/*.py` lists paths from git and opens one
from disk without a guard. Modelled on
`tests/test_a_corrected_sentence_survives_elsewhere.py#_derives_a_path_list`,
with the already-guarded helpers and the fixture-repository helpers classified
rather than exempted by name. Verified by the reader at exit 0 over the tree
and exit 1 over a planted unguarded scope, and by a vacuity assertion that it
finds the guarded helpers, seen red by emptying the corpus.

## What this phase found

**The reader found a sixth unguarded helper, and it is guarded in this
commit.** `tests/test_a_finding_id_is_a_bare_integer.py#committed_records`
lists records with `git ls-tree HEAD` and takes their CONTENT from the working
tree through `id_cells`, which its own docstring states as a deliberate
residual. So a record committed and then deleted from disk was listed and
opened from nowhere, and the two population measurements that consume it ended
at it. `spec.md`'s reach table has five helpers because it enumerated by
grepping `git ls-files`; this one lists with `ls-tree`, which is the shape
`LISTS_PATHS` is deliberately kept wide enough to catch. §12 asks for the
class rather than the coordinate, so it takes the same `on_disk` pair and its
three call sites unpack it.

**The reader classifies itself, and that is not an oversight.**
`suite_modules` lists the modules it is about to parse, so a module listed and
not on disk would end the enumeration at it — this case reporting *no
offender* because it read almost nothing. It applies `on_disk` like the rest
and is declared in the same table.

**Twenty-five scopes, six tables.** The reader asks *which scope DERIVES a
path list*, because that is where the repair went and because the consumer
that opens can be in another function or another module — measured: every one
of the twenty-five scopes has `open=False` when the walk looks for an `open`
call inside the deriving scope itself.

| Table | Scopes | How the reader checks it |
|---|---|---|
| `APPLIES_THE_SHARED_GUARD` | 7 | the scope must mention `on_disk` |
| `GUARDS_ITS_OWN_LIST` | 1 | the scope must mention `isfile` |
| `OPENED_ONLY_BEHIND` | 2 | the named consumer must still carry an `except OSError` |
| `CONTENT_FROM_GIT` | 3 | grounds a reader weighs |
| `OPENS_NOTHING` | 2 | grounds a reader weighs |
| `LISTS_A_FIXTURE` | 11 | grounds a reader weighs |

**A mechanical guard test had to be narrowed to the shared name.** A first
draft read `on_disk`, `isfile` or `exists` anywhere in the scope as a guard,
and two fixture cases came back guarded because they happened to call
`os.path.exists` in an assertion. So the only guard read from the code is
`on_disk`, plus the one predicate `tracked_python` was already using, named
per scope. Everything else is declared with grounds, which is the model's own
shape.

**What the reader cannot see, stated rather than left to be found.** A listing
word built from a variable, and a scope that hands its list to a helper in
another module which then opens it. The vacuity assertion is what keeps it
from passing on a read that found nothing.

**A `SyntaxWarning` this reader does not add.**
`tests/test_a_row_points_by_content.py:763` carries an escape python does not
know, and parsing it raises a warning. It predates this branch — executed with
this work stashed, `bin/test -q tests/test_a_new_returnable_value_is_a_contract_change.py`
emits it at exit 0 — so the reader catches it at its own `ast.parse` instead
of becoming a second source, rather than filtering it globally. The warning
itself is out of scope and named in `overview.md` §*Not done*.

**§15, how each case was shown red.**

| Mutation | What went red |
|---|---|
| a module planted in `tests/` with an unguarded `git ls-files` scope, tracked with `git add -N` | `test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard`. Exit 1, 1 failed 12 passed |
| `suite_modules` returning `[]` — the corpus emptied | the reader's own case and `test_the_reader_finds_the_helpers_this_work_guarded`. Exit 1, 2 failed 11 passed |
| `test_release_hygiene.py#tracked` returning `listed, []` — one helper's guard removed | `test_no_scope_in_the_suite_lists_paths_from_git_without_a_guard`, at the `_mentions` assertion. Exit 1, 1 failed 12 passed |

Three further cases pin what the reader must not lose: a planted scope is
named, a second call in one scope counts twice, and a list built at import
time is a scope of its own. The nine modules the class touches are **284
passed** at exit 0, read from `$?`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `committed_records` returning a bare list | It returns the `on_disk` pair. Its three call sites unpack it in the same commit; no other module imports it |
| none other | none |
