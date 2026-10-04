# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | bb38ce3e |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

C2 by D2: delete the bare-name branch of `owner`, so a receiver no import
binds is judged under every spelling. C3: re-run the construction on 3.12
(M2) and add its modules to `NOT_A_FILE_OPENER`. Plant S4, S5, S6 and S7,
and move the `NAMED` case for `def f(os)` to a case asserting the site. Run
the repository case once the branch is gone (M1): a tree instance would mean
keeping round 3's two-name branch instead and recording the divergence. Every
new case seen red at the base; S7 labelled pin or regression case by its
result there.

## What this phase found

**M2: the 3.12 run matches C3, and nothing else carries a module-level
`open`.** Executed 2026-10-04 on 3.12.11, 3.13.9 and 3.14.3: every name in
sys.stdlib_module_names imported, and every package's submodules walked with
pkgutil.walk_packages, recording each module whose `open` attribute is
callable. Private modules (a leading underscore) were skipped, and so were
the ones that act on import or drag in a test tree: `antigravity`, `this`,
__phello__, `idlelib`, `turtledemo`, `test`, `lib2to3`. The three runs list
the same set as spec C3's table, with `aifc` and `sunau` on 3.12 alone,
`dbm.sqlite3` from 3.13 and `compression.*` on 3.14. `dbm.gnu` was absent on
all three local builds and `nt` exists only on Windows, so both are in the set
by reading, as the frame had them. The private _dbm and _gdbm, which `dbm.ndbm` and
`dbm.gnu` re-export, are not in the set: importing either by
its own name is a shape nothing in the tree has, and it stays judged as
`<expr>.open`.

**M1: no tree instance.** With the branch deleted, the repository case
passed with `ALLOWED` still empty, executed at this phase's commit. D2 stands
and round 3's two-name branch is not kept.

**The cases for a receiver no import binds have a table of their own.**
`UNNAMED` and `UNPROVEN` assert the qualname `<module>`, and two of S4/S5's
shapes sit in a function. `UNIMPORTED_RECEIVERS` carries
`(source, kind, qualname)` and holds S4's three shapes, S5, and S7's two, so
every case of C2 is in one place.

**Seen red (contract §15), each executed:**

| Case | At the base's walker (`94d7b2e0`'s module, extracted and imported) |
|---|---|
| S4, `wave = make(p)` then `wave.open()`; `def f(tarfile)`; `for shelve in d` | no site: red |
| S5, `def f(os): return os.open(p, 0)` | no site: red |
| S6, eight `NAMED` cases, one per added module | each reported as `<expr>.open(), mode not a literal`: red |
| S7, `dbm.gnu.open(p)` with no import | reported, as expected: **a pin**. No mutation of this work turns it red, because an attribute chain whose head no import binds resolved to nothing before and after |
| S7, `tokenize.open(p)` with no import | reported at the base: **a pin there**. It is the regression case for the combination this work avoids: with the bare-name branch restored beside the C3 set, `bin/mutation-check` shows it red |

**Mutations of this phase's units, each through `bin/mutation-check`, all
red:** the bare-name branch restored in `owner` (five cases red: S4's three,
S5, and S7's `tokenize`); each of the eight added names removed from
`NOT_A_FILE_OPENER`, one at a time, against the `NAMED` cases.

`bin/test` on the module: 137 passed (124 after phase 1, plus eight S6 cases
and six `UNIMPORTED_RECEIVERS` cases, less the moved `NAMED` case). Ruff
check and format check clean.

**Owed to phase 3.** The module docstring's K1 bullet and `owner`'s
docstring still describe the deleted branch (*a bare name no import binds,
read as itself*), and the comment over `NOT_A_FILE_OPENER` still says
*receivers that open no text file*, which `tokenize` does. Phase 3 rewrites
all three.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `owner`'s bare-name branch, which returned a name no import binds as itself | none: D2 removes the behaviour. The sentences describing it are phase 3's |
| The `NAMED` case `os.open on a name no import binds` | `UNIMPORTED_RECEIVERS`, `a parameter named os`, now asserting the site |
