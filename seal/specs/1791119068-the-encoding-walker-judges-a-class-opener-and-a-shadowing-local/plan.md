# Implementation Plan: the encoding walker judges a class opener and a shadowing local (#762)

<!-- seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

## Summary

Close round 3's two yellows of #741 for their classes, not their instances,
and its three notes as sentences or set entries: a method opener called on
its class is judged with the path shift (C1), a bare name no import binds is
never excused (C2), every standard-library module whose `open` takes no
locale encoding is excused when imported (C3), and the docstrings name exactly
what the code excuses. One module changes:
`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`.
`spec.md` holds the classes, the decisions and the acceptance.

## Technical context

Read 2026-10-04 at the base `94d7b2e0`, where the module is byte-identical to
round 3's target `42db9639` (`git diff 42db9639 HEAD` on it is empty):

- `judge`'s first test is `if target in OPENERS: return judge_opener(call, target)`.
  `OPENERS` holds four function rows, `<expr>.open`, and the method row
  `zipfile.Path.open`. The `.open` branch at the end of `judge` computes the
  shift from `UNBOUND_RECEIVERS`, asks `owner`, and looks up
  `f"{made_by}.open"` in `OPENERS`. That lookup is the only reader the method
  row needs.
- `judge_opener(call, opener, shift)` reads `OPENERS[opener]` for the
  positions and derives the reported kind from the opener's name. Whatever
  shape the split takes, the kinds `zipfile.Path.open()` and `<expr>.open()`
  stay as they are: `UNNAMED` pins them.
- `owner`'s bare-name branch (`isinstance(receiver, ast.Name) and receiver.id
  not in bound`) is the whole of C2. Without it, `dotted` returns
  `bound.get(name)`, which is None for an unimported name, and the `.open`
  branch falls to `<expr>.open`.
- `NOT_A_FILE_OPENER` is the set C3 extends. Its comment says *receivers that
  open no text file*; `tokenize` opens text in a fixed encoding, so the
  comment widens to *take no locale encoding*.
- `test_each_unnamed_shape_is_reported` and `test_what_the_walk_cannot_prove_counts_as_unnamed`
  assert the qualname `<module>`; a case whose site sits in a function needs
  its own assertion.
- `tests/test_a_shrunken_corpus_declines_to_judge.py` names this module's
  `tracked_python` and `entry_points` only, neither of which changes.

**What breaks in six months.** A new opener method is added — say a class's
`.open` whose encoding sits somewhere unusual — and whoever adds it puts the
row where the function openers are. S3's test is what names it at that
moment; without S3, the separation in D1 is a convention and the class reopens
the way 🟡 1 did.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| C1: round 3's paste-ready guard, `target in OPENERS and target != "zipfile.Path.open"` | The next method row reopens the class under a new name; §12 measured exactly that shape three times in one work item | refused |
| C1: a generic guard at the top of `judge` — skip any key whose class part is in `UNBOUND_RECEIVERS` | Closes the class, but leaves method rows and function rows in one table whose two kinds of key are read by two different branches; a reader adding a row cannot tell which branch will read it | refused |
| C1: method positions in a table of their own, read only by the `.open` branch; the top of `judge` reads function openers only; S3 asserts no function-opener key is a method of an `UNBOUND_RECEIVERS` class | A split costs one more table to read; `judge_opener` takes positions and a kind rather than a key. Accepted: it makes the class unreachable rather than excepted | **chosen** |
| C2: round 3's paste-ready fix — keep the bare-name excuse for `os` and `webbrowser` | A spelling list that K2 refuses, kept to reproduce a behaviour round 2's reviewer called acceptable to lose; and C3's `posix`, `nt`, `tokenize`, `aifc`, `sunau` raise the question of whether they join it | refused, unless M1 finds a tree instance |
| C2: delete the bare-name branch | `def f(os): os.open(p, 0)` is reported; an over-report for a shape the tree does not have, with an `ALLOWED` row as its repair | **chosen** |
| ⬜ 3: trace `/` and `.joinpath` from a `zipfile.Path(...)` receiver in `owner` | Two new branches for an over-report whose repair (`encoding=` keyword) already passes; new surface for the review to find under-reports in | refused; a docstring sentence instead |
| ⬜ 4: add `dbm.gnu`, `dbm.ndbm`, `dbm.sqlite3` only, as round 3 listed | Leaves `aifc`, `sunau`, `tokenize`, `posix`, `nt` over-reported, found the next time somebody reads; round 3's list was read, not constructed | refused; C3's construction instead |
| Edit #741's `spec.md:86` (⬜ 5) | Rewrites a shipped record; `settle` already folds the newest work item where two disagree | refused (spec D5) |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | C1. Method positions move out of the table the top of `judge` reads; S1's three `UNNAMED` spellings, S3's structural test, and S2's existing `NAMED` case now passing for the right reason | Each new case run red at the base before the fix (S1: no site; S3: names `zipfile.Path.open`); S2 shown red by deleting `"utf-8"` after the fix; then `bin/test` on the module green | 7227d29f |
| 2 | C2 and C3. The bare-name branch of `owner` deleted; C3's modules added to `NOT_A_FILE_OPENER` after re-running the construction on 3.12 (M2); S4, S5, S6, S7 cases; the `NAMED` case for `def f(os)` moved | Each new case run red at the base (S4, S5: no site; S6: reported); S7 run at the base and labelled pin or regression case by the result; `bin/test` on the module green, the repository case included (M1) | |
| 3 | The docstrings (module, `owner`, the comment over `NOT_A_FILE_OPENER`) name exactly what is excused, with ⬜ 3's sentence and D4's shape in *What no row can hold*; `changelog.md`; the ledger fragment with E1's `Re-read ·` row and one new row for C1–C3 | Read against the code (S8); `evidence-check --reverify --into seal/ledger/<id>.md` names E1 and nothing else, then `bin/evidence-check .` shows 0 drifted and 0 broken; `tests/test_no_real_identifiers.py` and ruff on the module | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

What a phase discovers while it is being built, and needs the next phase to
know, goes in `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes. Re-read this column
after any rebase.

## Operational impact

None for a deployer: no migration, no environment variable, no dependency.
What changes is a contributor's verdict. A branch that adds
`zipfile.Path.open(q, "r")`, or `.open()` on a local named after a module,
fails every CI leg where it passed; a branch that imports one of C3's modules
and calls its `open` passes where it failed. No file in the tree changes
verdict (spec §*Grounding*, last row — read; S9 executes it).
