# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — review round 2

| Field | Value |
|---|---|
| Target SHA | 69273b868e8e2e336a6cf020bfd0ec8c7318cd5b |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #782 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `06dd7a22cd04c449b27675a90b340d5fa76221a9..dc82346050e08b67e2d073f3802adec053b1d11f`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a class-called `ResourceHandle.read_text` or `ResourceContainer.read_text` passes, and J1 and the comment say no such class is left) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #762 (PR #782), the verifying round, at 69273b86: open round 1's fixes (range 88434e82..ad9ecb24, closed at 69273b86) and judge whether each of the four closes its finding, with no regression — 🟡1 ossaudiodev and the three records' wording; 🟡2 the two Traversable spellings in UNBOUND_RECEIVERS and J1's narrowed claim; ⬜3 the OPEN_METHODS assertion; ⬜4 the rebinding sentence — plus the three survivors.md exemptions and the smith's correction to round 1's ResourceHandle row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a class-called `ResourceHandle.read_text(h)` or `ResourceContainer.read_text(c)` reads the locale through the inherited `Traversable.read_text` and passes; J1 and the `UNBOUND_RECEIVERS` comment, both written by round 1's fixes, say the list holds every such class | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:178` | **fixed** `76746a38` | fixed at 76746a38 — (the class enumeration re-run with inherited methods and every home, `__all__` and `__getattr__` spelling on 3.12, 3.13 and 3.14: `ResourceHandle` and `ResourceContainer` under both spellings, and 3.12's `pipes.Template`, a third member neither round named, join `UNBOUND_RECEIVERS` with `OPEN_METHODS` rows and five `UNNAMED` cases; the comment states how the list was settled and what was left out), dc823460 (J1 and the changelog say the same); executed: the inherited-method enumeration on 3.12.11, 3.13.9 and 3.14.3 finds exactly these two; no site at the base or the target; `ResourceContainer.read_text(x)` calls `x.open(encoding=None)`; `importlib.simple` re-exports both; the proposed fix ran 144 passed and its cases were red without its rows |
| ⬜ 2 | adding `Traversable` to `UNBOUND_RECEIVERS` without an `OPEN_METHODS` row turns `Traversable.open(t, "r", "utf-8")` from passing to reported | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:235` | **fixed** `76746a38` | fixed at 76746a38 — (`OPEN_METHODS` rows `(0, 1)` for both `Traversable` spellings and the four `ResourceHandle` and `ResourceContainer` spellings; `NAMED` cases for each, the two `Traversable` ones red before the fix and the four others red when their row is removed); executed: passes at the base, reported at the target; read: the class-called method is abstract with a docstring-only body, so it is an over-report on a call that opens nothing; closed by 🟡 1's fix |
| ⬜ 3 | the comment over `NOT_A_FILE_OPENER` and J1 name nine modules that do not import on macOS; five Windows-only submodules also failed and are not named | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:143` | **fixed** `76746a38` | fixed at 76746a38 — (the comment over `NOT_A_FILE_OPENER` names the five Windows-only submodules), dc823460 (J1 the same); executed: the 3.12 failed-import list holds fourteen names; a search of the five sources finds no module-level `open`, so the set is right and only the sentence is incomplete |
| ⬜ 4 | correction: round 1's class table says `ResourceHandle` and `ResourceContainer` raise or open bytes | `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-1-report.md:97` | answered | round reports are a reviewer's record of a moment and are not rewritten; `rounds/round-2-report.md` itself carries the correction to round 1's class table (the orchestrator's decision); paperwork, not counted toward Needs a fix; executed: `ResourceHandle.open` hands `None` on to `io.TextIOWrapper`, and both classes inherit `Traversable.read_text` |
| 🟢 | round 1's finding 1 is closed — `ossaudiodev` excused, with its case and the three records' wording | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:167` | confirmed | executed: reported at the base, no site at the target; the `NAMED` case at :852 passes; read: docstring, comment, changelog and J1 say how the modules that do not import were settled |
| 🟢 | round 1's finding 2 is closed — a class-called `Traversable.read_text` is shifted, in both spellings, with two cases | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:184` | confirmed | executed: three spellings reported at the target, none at the base; `importlib.abc.Traversable` present on 3.12 and 3.13, absent on 3.14 as the comment says |
| 🟢 | round 1's finding 3 is closed — S3 holds every `OPEN_METHODS` key to `UNBOUND_RECEIVERS` | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:952` | confirmed | executed: red with a foreign `OPEN_METHODS` row, green at the target |
| 🟢 | round 1's finding 4 is closed — the rebinding limit names any binding in any scope | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:66` | confirmed | executed: assignment, loop variable and parameter rebinding an imported `wave` each give no site at the target, as the sentence states |
| 🟢 | the three `survivors.md` exemptions are each true | `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/survivors.md` | confirmed | executed: `survivor-check` over the fix range passes with the file and exits 1 without it; read: each quote at its coordinate, each grounds cell holds |
| 🟢 | the smith's correction: `ResourceHandle.open` opens locale text, and a class call to it is reported | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:235` | confirmed | executed: four unnamed class-call shapes reported, the named one passes; read: its body wraps the stream in `io.TextIOWrapper(stream, *args, **kwargs)`; incomplete, see 🟡 1 and ⬜ 4 |
| carried | round 1's C1, C2 and C3 confirmations | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:349` | confirmed | carried from round 1 as the prompt asked, not re-derived; the fixes touched `UNBOUND_RECEIVERS` and `NOT_A_FILE_OPENER`, and the module's own C1 and C3 cases pass at the target (executed, 140 passed) |

## Paste-ready fixes

```python
# UNBOUND_RECEIVERS: the comment's middle sentence and the list
# Every public standard-library class having `open`, `read_text` or
# `write_text`, defined or inherited, was read on 3.12 to 3.14 (#762), and
# these are the ones whose method, called on the class, reads text in the
# locale with its encoding in a slot the shift decides.
# `Traversable.read_text(self, encoding=None)` hands `None` on to the concrete
# path's `open`, and `importlib.resources.simple`'s `ResourceHandle` and
# `ResourceContainer` inherit it; `importlib.abc.Traversable` is the same
# class on 3.12 and 3.13, and `importlib.simple` re-exports the other two.
UNBOUND_RECEIVERS = {
    "pathlib.Path",
    "pathlib.PurePath",
    "pathlib.PosixPath",
    "pathlib.WindowsPath",
    "zipfile.Path",
    "importlib.resources.abc.Traversable",
    "importlib.abc.Traversable",
    "importlib.resources.simple.ResourceHandle",
    "importlib.resources.simple.ResourceContainer",
    "importlib.simple.ResourceHandle",
    "importlib.simple.ResourceContainer",
}

# OPEN_METHODS, after "zipfile.Path": (0, 1),
    # `open(mode='r', *args, **kwargs)` hands `args` to `TextIOWrapper` the
    # same way, so the encoding sits right after the mode.
    "importlib.resources.abc.Traversable": (0, 1),
    "importlib.abc.Traversable": (0, 1),
    "importlib.resources.simple.ResourceHandle": (0, 1),
    "importlib.simple.ResourceHandle": (0, 1),

# UNNAMED, after "Traversable.read_text unbound, the importlib.abc spelling":
    "ResourceHandle.read_text unbound, inherited from Traversable": (
        "from importlib.resources.simple import ResourceHandle\n"
        "ResourceHandle.read_text(h)",
        ".read_text()",
    ),
    "ResourceContainer.read_text unbound, the importlib.simple spelling": (
        "import importlib.simple\nimportlib.simple.ResourceContainer.read_text(c)",
        ".read_text()",
    ),

# NAMED, after "ossaudiodev.open is an audio device":
    # `open(mode='r', *args)` hands `args[0]` to `TextIOWrapper` (#762).
    "Traversable.open unbound, encoding after the mode": (
        'from importlib.resources.abc import Traversable\nTraversable.open(t, "r", "utf-8")'
    ),
    "ResourceHandle.open unbound, encoding after the mode": (
        "from importlib.resources.simple import ResourceHandle\n"
        'ResourceHandle.open(h, "r", "utf-8")'
    ),
```
```text
# J1, evidence cell: replace
#   "Every public class defining `open`, `read_text` or `write_text` on the
#   same three interpreters was listed, and `Traversable` was the one outside
#   `UNBOUND_RECEIVERS` whose class-called method read the locale and passed"
# with
#   "Every public class having `open`, `read_text` or `write_text`, defined or
#   inherited, on the same three interpreters was listed (round 2 of review
#   added the inherited ones), and `Traversable`, with `ResourceHandle` and
#   `ResourceContainer` of `importlib.resources.simple` inheriting its
#   `read_text`, were the ones outside `UNBOUND_RECEIVERS` whose class-called
#   method read the locale and passed"
# and add `#OPEN_METHODS` to the re-stamp; the claim cell can stay as written.

# changelog.md, the first bullet's added sentence becomes:
#   `Traversable.read_text(t)`, from `importlib.resources.abc`, called on its
#   class, passed the same way and is now reported too, and so is the same
#   method called on `ResourceHandle` or `ResourceContainer`, which inherit it.
```
```text
# The comment over NOT_A_FILE_OPENER, its last three lines, become:
# does not was read in its documentation instead: `dbm.gnu`, `nt` and
# `ossaudiodev` carry an `open`; `nis`, `spwd`, `msilib`, `msvcrt`, `winreg`,
# `winsound` and five Windows-only submodules of `asyncio`, `encodings` and
# `multiprocessing` carry none.
# J1's evidence cell takes the same addition.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test -q` on this module in the clone at 69273b86 | 140 passed |
| the walker at the target and at the base (the base's tests directory extracted), on 24 shapes: three Traversable read_text spellings, six Traversable open shapes, ResourceHandle and ResourceContainer read_text and open shapes, ossaudiodev, three rebinding shapes | as stated per finding; the only shape that flips from passing to reported is `Traversable.open(t, "r", "utf-8")` and `(t, "r", -1)`; `ResourceHandle.read_text(h)` and `ResourceContainer.read_text(c)` give no site at either |
| the class enumeration with inherited methods (every public class in every importable standard-library module and submodule, on 3.12.11, 3.13.9, 3.14.3) | inherited text-reading methods outside the list: `ResourceHandle.read_text` and `ResourceContainer.read_text`, from `Traversable`; failed imports on 3.12: fourteen, the nine named plus five Windows-only submodules |
| `Traversable.open`, `Traversable.read_text` and `ResourceHandle.open` source on 3.12 and 3.14; `ResourceContainer.read_text` on a stand-in object on all three; the `importlib.simple` and `importlib.abc` spellings on all three | `open` is abstract with a docstring-only body; `read_text` calls `self.open(encoding=encoding)`; the stand-in's `open` received `encoding=None`; `importlib.simple` re-exports both classes on all three; `importlib.abc.Traversable` absent on 3.14; `ResourceHandle(...)` raises `TypeError` (abstract) |
| a search of the five Windows-only submodules' sources for a module-level `open` | none in any |
| 🟡 1's proposed fix applied in the clone, then rows removed one group at a time | 144 passed with it; both new `UNNAMED` cases red without the list rows; both new `NAMED` cases red without the `OPEN_METHODS` rows; the clone was reverted and re-ran 140 passed |
| finding 3's assertion with `OPEN_METHODS["importlib.metadata.PathDistribution"]` added | red, naming the row |
| `survivor-check --range 88434e82..ad9ecb24`, with and without `--exempt survivors.md` | passes with three exempt; exits 1 without |
| `evidence-check --strict --ledger` on this work item's ledger fragment | 13 ok, 0 drifted, 0 broken; the work item's records: 0 refused |
| `unverified-check --baseline 94d7b2e0` on `overview.md` | 1 open (the sealer's), 1 closed |
| the full suite, repository-wide lint, typecheck, `evidence-check .` over the repository | not yet, and not this round's: the sealer's, after the rounds settle |

```
# the inherited-method enumeration, run once per interpreter
for each public class C in every importable stdlib module and submodule:
    for meth in (open, read_text, write_text):
        if C has meth (getattr_static, inherited included):
            print C, meth, and the class in C's MRO whose body defines it
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:144` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:166` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:914` | round 1's ⬜ 3 — fixed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:66` | round 1's ⬜ 4 — fixed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:349` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:433` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
