# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — review round 1

| Field | Value |
|---|---|
| Target SHA | 90e645150ab5752923a5d6749267e77cd88cd18a |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #782 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `88434e8218fb90110946f9b76d15505fc0da45e5..ad9ecb24fa1b73707854c0d8145505ab25d55060`, 3 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (`ossaudiodev` missing from C3, and three records call the set complete) and 🟡 2 (class-called `Traversable.read_text` passes; fix, or defer with J1 narrowed) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #762 (PR #782), at 90e64515 against `release/v0.18.2` (94d7b2e0): spec compliance first against `spec.md` (C1 the method-opener split and its structural test, C2 the deleted bare-name branch, C3 the standard-library modules re-enumerated by construction), then quality. Judge whether the S3 structural test reaches the class (a method key in any table `judge` matches by name), whether deleting the bare-name branch leaves any under-report the docstring does not state, and whether the eight added `NOT_A_FILE_OPENER` names (two of them, `dbm.gnu` and `nt`, absent from every local build) are each a module whose `open` takes no locale encoding.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | C3 omits `ossaudiodev` (3.12, Linux and FreeBSD), and the comment, the changelog and J1 each call the set complete | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:144` | **fixed** `02518dd6` | fixed at 02518dd6 — (`ossaudiodev` in `NOT_A_FILE_OPENER`, its `NAMED` case, and the comment and docstring list saying how modules that do not import on macOS were settled), 746bd406 (changelog and J1 say the same); executed: on 3.12 the construction's failed-import list holds `ossaudiodev`, and `ossaudiodev.open("w")` is reported; read: its documentation gives a module-level `open` of an audio device with no encoding parameter |
| 🟡 2 | a class-called `Traversable.read_text(t)` reads the locale and passes, because `UNBOUND_RECEIVERS` does not list `Traversable`; same cause as #741's 🟡 1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:166` | **fixed** `02518dd6` | fixed at 02518dd6 — (`importlib.resources.abc.Traversable` and `importlib.abc.Traversable` in `UNBOUND_RECEIVERS`, two `UNNAMED` cases), 746bd406 (J1 states the shift for the classes the list holds, and how the list was settled); executed: no site at the base or the target; the class enumeration on 3.12–3.14 finds `Traversable` as the only member that under-reports; pre-existing at the base |
| ⬜ 3 | S3 names methods of `UNBOUND_RECEIVERS` classes only, and no check holds `OPEN_METHODS` keys to that list | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:914` | **fixed** `02518dd6` | fixed at 02518dd6 — (S3 asserts every `OPEN_METHODS` key but `<expr>` is in `UNBOUND_RECEIVERS`); executed: a foreign `OPEN_METHODS` row reproduces the unshifted judgment while S3 stays green |
| ⬜ 4 | D4's docstring sentence names a narrower scope only; the same scope and a sibling scope are excused too | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:66` | **fixed** `02518dd6` | fixed at 02518dd6 — (the docstring's rebinding limit names any binding in any scope), 746bd406 (J1's note matches); executed: three shapes, each with no site |
| 🟢 | C1: a class-called `zipfile.Path.open` is judged with the shift, in all three spellings, and no dotted-name table holds a method of an `UNBOUND_RECEIVERS` class | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:349` | confirmed | executed: S1 red at the base and green at the target; S3's five tables listed; read: S2 and S3 red at the base by the base's positions |
| 🟢 | C2: deleting the bare-name branch turns excuses into reports and introduces no new under-report | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:433` | confirmed | read: `owner` has one caller and None falls to `<expr>`; executed: S7's `tokenize` case is reported at the target |
| 🟢 | C3: each of the eight added names takes no locale encoding | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:144` | confirmed | executed: present and carrying `open` on the local builds; read: `tokenize.open` source, and the documentation for `dbm.gnu`, `dbm.ndbm`, `dbm.sqlite3` and `os.open` |

## Paste-ready fixes

```python
# NOT_A_FILE_OPENER, after "nt":
    "nt",
    # 3.12 on Linux and FreeBSD only, removed in 3.13: an audio device.
    "ossaudiodev",
    "PIL.Image",

# NAMED, after "nt.open is os.open":
    "ossaudiodev.open is an audio device": (
        'import ossaudiodev\nossaudiodev.open("w")'
    ),
```
```text
# The comment over NOT_A_FILE_OPENER, its last two lines, becomes:
# table holds, enumerated over every importable module on 3.12 to 3.14 and,
# for a module that does not import on macOS (`dbm.gnu`, `nt`,
# `ossaudiodev`), read from its documentation (#762), with PIL's `Image`
# beside them.

# changelog.md, the third bullet: add `ossaudiodev` to the list, and replace
# "enumerated on 3.12 to 3.14 rather than read" with
# "enumerated on 3.12 to 3.14, with the modules that import only on Linux
# or Windows read from their documentation".
```
```python
# UNBOUND_RECEIVERS, after "zipfile.Path":
    "zipfile.Path",
    # `Traversable.read_text(self, encoding=None)` opens through the concrete
    # path's `open`, so `None` is the locale; called on the class, the
    # traversable is the first argument (#762).
    "importlib.resources.abc.Traversable",
    "importlib.abc.Traversable",
}

# UNNAMED, after "zipfile.Path open unbound, aliased module":
    "Traversable.read_text unbound": (
        "from importlib.resources.abc import Traversable\nTraversable.read_text(t)",
        ".read_text()",
    ),
```
```python
# test_no_method_is_matched_by_its_dotted_name, before `methods = ...`:
    unshifted = sorted(set(OPEN_METHODS) - {"<expr>"} - UNBOUND_RECEIVERS)
    assert not unshifted, (
        f"OPEN_METHODS rows {unshifted} name a class outside UNBOUND_RECEIVERS, "
        "so the method called on its class is judged without the shift"
    )
```
```text
# Module docstring, "What no row can hold", replace the rebinding clause with:
a handler subclass whose constructor calls `super().__init__(p)`, and a name an
import binds that anything else in the file also binds (`import wave`, then
`wave = make(p)`, a loop variable, or a parameter `def f(wave)`), because
imports are read for the whole file and not per scope, so that `.open` is
excused as the module's.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on this module in the clone at 90e64515 | 137 passed (the prompt said 142; not reproduced) |
| the construction (every name in the standard-library module list, every package walked) on 3.12.11, 3.13.9 and 3.14.3, listing failed imports, module-level `open`, and classes defining `open`, `read_text` or `write_text` | the module set matches the spec's C3 on importable modules; the 3.12 failed-import list holds `ossaudiodev`, a Linux-only module with `open`; `Traversable` is the one class outside `UNBOUND_RECEIVERS` whose class-called method reads the locale |
| the walker at the target and at the base (extracted) on S1, S7, three rebinding shapes, `ossaudiodev`, and three `Traversable` shapes | S1: site at the target, none at the base; rebinding shapes and `Traversable`: no site at either; `ossaudiodev`: reported at both |
| a method row for `Traversable` put into `OPENERS`, and into `OPEN_METHODS`, at the target | S3 names neither; the `OPEN_METHODS` row makes `Traversable.open(t, "r")` pass |
| the proposed fixes applied in the clone, then each removed again | 139 passed with the fixes; the `Traversable` case is red without its rows, the `ossaudiodev` case red without its row, and the new S3 assertion red with a foreign `OPEN_METHODS` row; the clone was reverted afterwards |
| the full suite, repository-wide lint, typecheck, `bin/evidence-check .` | not yet, and not this round's: the sealer's, after the rounds settle |

```
# the construction probe, run once per interpreter (3.12.11, 3.13.9, 3.14.3)
for name in sorted(sys.stdlib_module_names) minus private and SKIP:
    import it (record a failure), walk its package's submodules
    record: callable module.open; public classes whose __dict__ defines
            open / read_text / write_text as an instance method
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
