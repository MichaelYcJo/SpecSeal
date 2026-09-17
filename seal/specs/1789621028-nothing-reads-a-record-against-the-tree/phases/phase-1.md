# 1789621028-nothing-reads-a-record-against-the-tree — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 73025104 |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

Close #426 in `tests/test_chain_hooks_hardening.py`, inside
`test_the_questions_are_collected_before_the_work_not_during_it`: the sweep
records the read's byte length and asserts it equals `os.path.getsize` of the
file it read, so the assertion has no number in it to be wrong. Not a bigger
threshold and not an exact byte count as a literal — the ticket refuses both
by name. Acceptance is the module green untouched and exit 1 under each of
`f.read(10)`, `f.read(2000)` and the loop's iterable replaced by `()`, each
mutation applied alone and reverted, plus one ordinary reword of a definition
staying green.

## What this phase found

**The frame left the module red, and phase 1's stated acceptance could not be
taken as written.** `plan.md`'s Phases row 1 asks for
`bin/test tests/test_chain_hooks_hardening.py` *exit 0 untouched*. Executed at
`5adaffef`, the frame's own commit: **exit 1**, on
`test_every_spec_directory_that_reached_the_ladder_has_an_overview`, naming
this work item. Writing `spec.md` and `plan.md` is what puts a directory on
the SDD ladder, and that case demands the closing memo the builder owns — so
the claim was true of the tree the framer read and false of the tree the
framer left. Opening `overview.md` is the answer and it was due at the first
divergence anyway; it rides this phase's commit, and the divergence row is in
the memo.

**The byte comparison is what makes the middle mutation visible, and the
numbers say why.** `f.read(2000)` reads 2000 *characters*; the sweep reported
2006, 2024, 2007, 2018 and 2020 bytes for the five definitions, because these
files carry emoji and em-dashes. Both sides of the new assertion are byte
counts — `len(body.encode("utf-8"))` against `os.path.getsize` — so the
comparison holds across that encoding rather than being defeated by it. A
character-length reading would have compared 2000 against a byte size and
still gone red here, but only by accident of the mismatch.

**The mutation battery, executed 2026-09-17.** Exit codes read directly from
`subprocess.run().returncode`, never through a pipe (§1); each mutation
applied alone to bytes kept in the driver and restored from those bytes, never
from HEAD (`agents/smith.md` §Boundaries); `tests/__pycache__` cleared between
runs.

| Run | Exit | What it printed |
|---|---|---|
| Baseline, fix in place | **0** | 51 passed |
| `f.read(10)` | **1** | `the sweep read a definition it did not read in full: [('agents/framer.md', 10), …]` |
| `f.read(2000)` | **1** | `… [('agents/framer.md', 2006), ('agents/scribe.md', 2024), …]` |
| `for path in ():` | **1** | the sweep-walked-every-definition assertion — `Right contains 5 more items, first extra item: 'agents/framer.md'` |
| A sentence added to `agents/scribe.md` (control) | **0** | 51 passed |
| Restored | **0** | 51 passed |

The third mutation is caught by the assertion above the new one rather than by
the new one, which is correct and worth stating: an emptied loop is an empty
`read` list, and `all(...)` over nothing is true. The case that names the
defect is the list-equality assertion, and the two together are what close the
three mutations the ticket measured.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The `1000` byte floor and the comment claiming it pinned wholeness | Nothing needs to own it — the claim it made was false, and the assertion that replaces it makes the true claim at the same line |
