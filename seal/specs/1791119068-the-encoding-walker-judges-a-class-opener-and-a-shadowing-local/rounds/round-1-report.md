# Round 1 report — the encoding walker judges a class opener and a shadowing local (#762)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 90e64515 |
| Base | `release/v0.18.2` at 94d7b2e0 |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at 90e64515, in the session scratchpad |

## Summary

Spec compliance holds for what the spec asked. C1's split is real, S1 is red
at the base and green at the target (executed), and S3 reads all five tables
`judge` tests `target in` (executed). Deleting the bare-name branch removes
excuses only, so it introduces no new under-report (read, then executed on
three shapes). Each of the eight names added to `NOT_A_FILE_OPENER` takes no
locale encoding: six by import and source, `dbm.gnu` and `nt` by the standard
library's documentation.

Two classes the work claims to have enumerated are each one member short.

- **C3 by construction ran on macOS only.** A module that does not import there
  was dropped without a word. `ossaudiodev` is in the 3.12 standard library
  (Linux and FreeBSD), carries a module-level `open`, and is not in the set.
  The comment, the changelog and J1 each say the set is every such module.
- **C1's cause has a second route.** A method called on its class is shifted
  only when its class is in `UNBOUND_RECEIVERS`, a hand list.
  `importlib.resources.abc.Traversable.read_text(t)` reads the locale and
  passes, at the base and at the target. S3's filter is bounded by the same
  list, so it cannot see this. `OPEN_METHODS` keys are not checked against that
  list either: I added a row for a class outside it, and S3 stayed green while
  the class-called call was judged unshifted.

Two smaller items: D4's sentence names the narrower-scope case of a rebound
import only, and the same under-report also happens in the same scope and from
a sibling scope.

The prompt said the module ran at 142 passed at the target. I ran it in the
clone at 90e64515 and got **137 passed**, which is what the phase-2 and
phase-3 records say. I could not reproduce 142.

## Findings

### 🟡 1 — `ossaudiodev` is missing from C3, and three records say the set is complete

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:144`

**What was claimed.** Spec C3 says the set was built *by construction … every
importable standard-library module and submodule carrying a callable `open`*.
Phase 2's M2 says *nothing else carries a module-level `open`*. Ledger row J1
says *found no module beyond the set*. The comment over `NOT_A_FILE_OPENER`
says *every standard-library module with a module-level `open` that no other
table holds, enumerated over every importable module on 3.12 to 3.14*. The
changelog says *the list is every standard-library module with a module-level
`open`, enumerated on 3.12 to 3.14 rather than read*.

**What I found (executed).** I re-ran the construction on 3.12.11, 3.13.9 and
3.14.3 and also listed every name that failed to import. On 3.12 these failed:
`dbm.gnu`, `nt`, `ossaudiodev`, `nis`, `spwd`, `msilib`, `msvcrt`, `winreg`,
`winsound`, plus Windows-only submodules. Phase 2 accounted for `dbm.gnu` and
`nt` and was silent about the rest. Of the rest, only `ossaudiodev` has a
module-level `open`. Its 3.12 documentation (read) gives
`ossaudiodev.open([device, ]mode)`, which opens an audio device. It is
deprecated since 3.11 and removed in 3.13, and it exists on Linux and FreeBSD,
so it is present on the ubuntu leg at the suite's 3.12 floor.

**Why it matters.** `import ossaudiodev; ossaudiodev.open("w")` is reported as
`<expr>.open()` (executed). The repair the failure message names, adding
`encoding="utf-8"`, raises a `TypeError` against that C function, so the only
way out is an `ALLOWED` row for a call that opens no text. The larger cost is
the claim. The release ships a changelog line, a code comment and a ledger
row that each state the set is complete, and the construction behind them
could not see a module that only imports off macOS. This is the blind spot
phase 2 named for two modules and did not apply to the rest of the
failed-import list.

**Fix.** Add the name and a `NAMED` case. Then write the claims so they say how
the modules that do not import locally were settled. The fix was executed in
the clone: the module ran 139 passed with this fix and 🟡 2's, and the new
`NAMED` case is red with the row removed.

### 🟡 2 — `Traversable.read_text(t)` called on its class reads the locale and passes

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:166`

**The class, by construction (executed).** I enumerated every public
standard-library class that defines `open`, `read_text` or `write_text` as an
instance method, on 3.12 to 3.14. Those are the method names `judge` shifts on
a class call. The candidates outside `UNBOUND_RECEIVERS` were checked one by
one:

| Class | Opens a file in the locale? |
|---|---|
| `importlib.resources.abc.Traversable` (and its 3.12–3.13 alias `importlib.abc.Traversable`) | **yes**: `read_text(self, encoding=None)` calls `self.open(encoding=encoding)`, and a `pathlib` traversable passes `None` on to the locale |
| `importlib.metadata.PackagePath`, `PathDistribution` | no: both read UTF-8 |
| `MultiplexedPath`, `ResourceContainer`, `ResourceHandle` | no: they raise, or open bytes |
| `imaplib`, `telnetlib`, `urllib.request`, `webbrowser`, `tkinter.tix`, `zipfile.ZipFile` | no file text |
| `pipes.Template.open` (3.12) | locale, but the class call is reported (its path is read as a non-literal mode) |
| pathlib's private _local Path, zipfile's private _path Path | private spellings, left out |

**What I found (executed).** In this work's C1 class, `Traversable` is the one
member that under-reports. `from importlib.resources.abc import Traversable;
Traversable.read_text(t)` returns no site at the base and at the target.
`shift` is 0 because the class is not in `UNBOUND_RECEIVERS`, so
`names_encoding(call, 0)` reads `t` as the encoding.
`Traversable.open(t, "r", -1)` also passes, because the unshifted encoding slot
2 holds the buffering argument.

**Why it matters.** Its cause is the cause of #741's 🟡 1, which this work
closes: a method called on its class is judged without the shift. J1 states
that cause as fixed in general (*a method called on its class is judged with
the path shift*), and the changelog repeats it. The work enumerated C1 over
`OPENERS` keys only. The other source of the same defect is that
`UNBOUND_RECEIVERS` is incomplete, and nothing enumerated it.

This is pre-existing at the base, and nothing in the tree has the shape. If
the smith answers it with grounds as a deferral, J1's claim should then be
narrowed to the classes `UNBOUND_RECEIVERS` lists.

**Fix.** Add both spellings to `UNBOUND_RECEIVERS` and plant one `UNNAMED`
case. Executed in the clone: the case is red with the two rows removed and
green with them.

### ⬜ 3 — S3 is bounded by the same hand list, and `OPEN_METHODS` keys are not checked against it

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:914`

S3 does reach the class the spec drew. `tables_matched_by_dotted_name` returns
`ALWAYS_UNNAMED`, `BINARY_BY_DEFAULT`, `OPENERS`, `TEXT_ALWAYS` and
`TEXT_UNLESS_BINARY` (executed), so a method row of an `UNBOUND_RECEIVERS`
class in any of the five is named. Its fixture makes the filter fail when the
filter is wrong.

Two gaps stay open, and both come from S3 deciding what a method is by
`UNBOUND_RECEIVERS` membership.

- **A method row for a class outside the list is not named.** I added
  `importlib.resources.abc.Traversable.open` to `OPENERS`, and
  `methods_of_unbound_receivers` returned `[]` (executed).
- **D1's claim covers the top of `judge` only.** D1 says *a method row added
  later cannot be reached by the top-of-`judge` lookup*, which is true. But
  `OPEN_METHODS` is now a second place a method's positions live, and its shift
  still depends on `UNBOUND_RECEIVERS`. I added
  `OPEN_METHODS["importlib.resources.abc.Traversable"] = (0, 1)`, and
  `Traversable.open(t, "r")` returned no site: `"r"` was read as the encoding,
  which is exactly #741's 🟡 1 shape. S3 stayed green (executed).

No tree instance exists, so the release ships no defect from this. The cheap
guard is one assertion: every `OPEN_METHODS` key except `<expr>` is in
`UNBOUND_RECEIVERS`. Executed in the clone: red with a foreign row, green
without one.

### ⬜ 4 — D4's sentence names a narrower scope, but any rebinding of an imported name is excused

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:66`

The docstring says the under-report is *a name an import binds that a narrower
scope rebinds*. `bindings` is file-wide, so the same excuse also applies to
these shapes, each returning no site (executed):

- the same scope: `import wave` then `wave = make(p)` then `wave.open()`;
- a module-level loop: `import shelve` then `for shelve in d: shelve.open("w")`;
- a sibling scope: `def a(): import wave` and `def b(): wave = make(p); return wave.open()`.

The behaviour is the one D4 put out of scope. Only the sentence is narrower
than the code.

## Answers to what the round was asked

- **Does S3 reach the class?** It reaches every dotted-name table, but only for
  methods of the five `UNBOUND_RECEIVERS` classes (⬜ 3). The class of
  class-called methods judged unshifted is wider than that list (🟡 2).
- **Does deleting the bare-name branch leave an unstated under-report?** The
  deletion itself leaves none. With the branch gone, `owner` returns None for
  an unbound name, which is not in `NOT_A_FILE_OPENER` and falls to `<expr>`.
  So the change only turns excuses into reports, and `owner` has one caller
  (read). The remaining under-report in that area is the import-bound name,
  which the docstring states too narrowly (⬜ 4).
- **Do the eight added names take no locale encoding?**
  - `dbm.ndbm`, `dbm.sqlite3`, `dbm.gnu`: key-value stores with no encoding
    parameter. The documentation (read) says keys and values are stored as
    bytes, and a `str` is converted with the default encoding, which is UTF-8
    and not the locale.
  - `aifc`, `sunau`: binary audio.
  - `tokenize.open`: opens bytes and wraps them in the encoding
    the tokenize module's encoding detection returns, UTF-8 by default. Source read on 3.12.
  - `posix.open`, `nt.open`: the implementation of `os.open`, which returns a
    file descriptor. The documentation says `os` imports one of the two by
    platform (read).

  All eight hold.

## Regression tests to plant

- `NAMED` gets `"ossaudiodev.open is an audio device"` (🟡 1), in this module.
- `UNNAMED` gets `"Traversable.read_text unbound"` (🟡 2), in this module.
- `test_no_method_is_matched_by_its_dotted_name` gets the
  `OPEN_METHODS`-against-`UNBOUND_RECEIVERS` assertion (⬜ 3), in this module.

## Facts for the evidence ledger

- If 🟡 1 is fixed, J1's *found no module beyond the set* should say how the
  modules that do not import on macOS were settled: `dbm.gnu`, `nt` and
  `ossaudiodev` were read from the documentation, and `nis`, `spwd`,
  `msilib`, `msvcrt`, `winreg` and `winsound` were read as having no `open`.
- If 🟡 2 is deferred instead of fixed, J1's *a method called on its class is
  judged with the path shift* is true only for the classes `UNBOUND_RECEIVERS`
  lists, and the row should say so.

## Carried, not re-established

Nothing was carried from an earlier round of this work item; this is its first
round. #741's round-3 findings were read as the spec cites them, for
coordinates only.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | C3 omits `ossaudiodev` (3.12, Linux and FreeBSD), and the comment, the changelog and J1 each call the set complete | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:144` | open | executed: on 3.12 the construction's failed-import list holds `ossaudiodev`, and `ossaudiodev.open("w")` is reported; read: its documentation gives a module-level `open` of an audio device with no encoding parameter |
| 🟡 2 | a class-called `Traversable.read_text(t)` reads the locale and passes, because `UNBOUND_RECEIVERS` does not list `Traversable`; same cause as #741's 🟡 1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:166` | open | executed: no site at the base or the target; the class enumeration on 3.12–3.14 finds `Traversable` as the only member that under-reports; pre-existing at the base |
| ⬜ 3 | S3 names methods of `UNBOUND_RECEIVERS` classes only, and no check holds `OPEN_METHODS` keys to that list | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:914` | open | executed: a foreign `OPEN_METHODS` row reproduces the unshifted judgment while S3 stays green |
| ⬜ 4 | D4's docstring sentence names a narrower scope only; the same scope and a sibling scope are excused too | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:66` | open | executed: three shapes, each with no site |
| 🟢 | C1: a class-called `zipfile.Path.open` is judged with the shift, in all three spellings, and no dotted-name table holds a method of an `UNBOUND_RECEIVERS` class | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:349` | confirmed | executed: S1 red at the base and green at the target; S3's five tables listed; read: S2 and S3 red at the base by the base's positions |
| 🟢 | C2: deleting the bare-name branch turns excuses into reports and introduces no new under-report | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:433` | confirmed | read: `owner` has one caller and None falls to `<expr>`; executed: S7's `tokenize` case is reported at the target |
| 🟢 | C3: each of the eight added names takes no locale encoding | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:144` | confirmed | executed: present and carrying `open` on the local builds; read: `tokenize.open` source, and the documentation for `dbm.gnu`, `dbm.ndbm`, `dbm.sqlite3` and `os.open` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1

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

### 🟡 2

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

### ⬜ 3

```python
# test_no_method_is_matched_by_its_dotted_name, before `methods = ...`:
    unshifted = sorted(set(OPEN_METHODS) - {"<expr>"} - UNBOUND_RECEIVERS)
    assert not unshifted, (
        f"OPEN_METHODS rows {unshifted} name a class outside UNBOUND_RECEIVERS, "
        "so the method called on its class is judged without the shift"
    )
```

### ⬜ 4

```text
# Module docstring, "What no row can hold", replace the rebinding clause with:
a handler subclass whose constructor calls `super().__init__(p)`, and a name an
import binds that anything else in the file also binds (`import wave`, then
`wave = make(p)`, a loop variable, or a parameter `def f(wave)`), because
imports are read for the whole file and not per scope, so that `.open` is
excused as the module's.
```

Needs a fix: yes — 🟡 1 (`ossaudiodev` missing from C3, and three records
call the set complete) and 🟡 2 (class-called `Traversable.read_text` passes;
fix, or defer with J1 narrowed)

Loses a record or crashes: no

## Proof block

Opened at 90e64515 in the clone: this work item's `spec.md`, `plan.md`,
`questions.md`, `overview.md`, `changelog.md`, `phases/phase-1.md`,
`phases/phase-2.md`, `phases/phase-3.md`; the ledger fragment
`seal/ledger/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local.md`;
`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`
(lines 1–640 and the diff against 94d7b2e0, which covers the rest); the same
module at 94d7b2e0; `bin/test`; `ruff.toml` (line length). Outside the tree:
`importlib/resources/abc.py` on 3.12, 3.13 and 3.14; the source of
`tokenize.open` on 3.12; the docstring of `os.open`; the Python documentation
pages for `dbm`, `ossaudiodev` (3.12) and `os`. The broad gate is `not yet`,
and the sealer answers it. Every probe file, the extracted base module, and the
clone with its `.venv` are deleted at handover.
