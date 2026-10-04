# Round 2 report — the encoding walker judges a class opener and a shadowing local

Ran by: specseal:warden on claude-opus-5-5
Target SHA: 69273b86 (PR #782, branch `fix/762-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local`)
Base: `release/v0.18.2` at 94d7b2e0
Kind: the verifying round. Its target is round 1's fix range
`88434e82..ad9ecb24` (02518dd6, 746bd406, ad9ecb24) plus the record commit
69273b86. Round 1's record says `Loses a record or crashes: no`, so the floor
was met and this round is the run's one reopening.

## Summary

All four of round 1's findings are closed by the fix commits, and the three
`survivors.md` exemptions are true. The smith's correction to round 1's class
table holds as far as it goes: `ResourceHandle.open` does open locale text,
and a class call to it is reported.

The correction stops one step short. `ResourceHandle` and `ResourceContainer`
do not define `read_text`, but both inherit `Traversable.read_text`. Called on
either class, that method reads in the locale, and the walker passes it. The
fix pass wrote a new completeness claim into J1 and into the comment over
`UNBOUND_RECEIVERS`, and these two classes make that claim false. Round 1's
class enumeration read only the methods each class defines in its own body,
so it never saw an inherited method. That is 🟡 1.

The `Traversable` fix also flips one shape from passing to reported:
`Traversable.open(t, "r", "utf-8")`. The method is abstract and opens nothing
when called on the class, so this is ⬜ 2. The same `OPEN_METHODS` rows that
🟡 1's fix needs also close it.

## What the account claimed, and what I found

- **Commit 02518dd6's message**: *"ossaudiodev is excused, a class-called
  Traversable.read_text is shifted, OPEN_METHODS is held to
  UNBOUND_RECEIVERS, and the rebinding limit names every scope."* All four
  hold (executed, below).
- **The `UNBOUND_RECEIVERS` comment** at
  `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:172`
  says *these are the ones whose method, called on the class, reads text in the
  locale*. **Ledger row J1** says *`UNBOUND_RECEIVERS` holds every public
  standard-library class whose `open`, `read_text` or `write_text`, called on
  the class, reads text in the locale*. Both are false for
  `importlib.resources.simple.ResourceHandle` and `ResourceContainer`, and for
  their `importlib.simple` spellings (🟡 1).
- **The smith's note**: *`ResourceHandle.open` opens locale text in text mode,
  but a class call is reported.* Confirmed by execution:
  `ResourceHandle.open(h)`, `(h, "r")`, `(h, mode="r")` and `(h, "r", None)`
  are each reported, and `(h, "r", "utf-8")` correctly passes. Round 1's
  report row at `rounds/round-1-report.md:97` (*"no: they raise, or open
  bytes"*) is wrong for `ResourceHandle.open`, and it is wrong for the inherited
  `read_text` of both classes (⬜ 4, a correction to the paperwork).
- **The orchestrator's narrow run**: *140 passed*. Reproduced in the clone at
  69273b86: 140 passed.

## Findings

### 🟡 1 — `ResourceHandle.read_text(h)` and `ResourceContainer.read_text(c)` called on the class read the locale and pass, and J1 says no such class is left

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:178`

**What I found (executed).** I enumerated every public standard-library class
on 3.12.11, 3.13.9 and 3.14.3 that has `open`, `read_text` or `write_text`,
with inherited methods included this time. Two classes outside
`UNBOUND_RECEIVERS` inherit a method that reads text:
`importlib.resources.simple.ResourceHandle.read_text` and
`importlib.resources.simple.ResourceContainer.read_text`. Both come from
`importlib.resources.abc.Traversable`. Every other inherited method was
already covered: the pathlib subclasses are in the list, `zipfile.PyZipFile`
inherits a `ZipFile.open` that reads bytes, and the `webbrowser` and `urllib`
openers involve no text file.

On all three interpreters, `Traversable.read_text(self, encoding=None)` does
`self.open(encoding=encoding)` (read from its source and executed).
`ResourceContainer.read_text(x)` called on the class called `x.open(encoding=None)`
on all three. `ResourceHandle.open(mode='r', *args, **kwargs)` hands `args` and
`kwargs` to `io.TextIOWrapper`, so `None` ends in the locale. `importlib.simple`
re-exports both classes on 3.12, 3.13 and 3.14 (executed), which makes it a
second spelling, the way `importlib.abc.Traversable` is one for `Traversable`.

At the target, the walker returns no site for
`from importlib.resources.simple import ResourceHandle; ResourceHandle.read_text(h)`,
and none for the `ResourceContainer` shape either. `shift` is 0 because neither
class is in the list, so the walker reads `h` as the encoding. This is exactly
the cause behind round 1's 🟡 2.

**Why it matters.** The behaviour is pre-existing at the base, and the shapes
are as contrived as `Traversable.read_text(t)` was. `ResourceHandle` cannot
even be instantiated on 3.12 or 3.14 (executed: `TypeError`, abstract
`iterdir` and `name`). The claim is new, though. Commit 746bd406 wrote into J1
that `UNBOUND_RECEIVERS` *holds every* such class. Commit 02518dd6 wrote into
the comment that *these are the ones*. Each was built from an enumeration that
read a class's own body and never an inherited method. The release would ship
a ledger row whose completeness claim is false. That is the defect round 1
rated 🟡 in two findings, and the reason is the same: an enumeration had a
blind spot, and the record did not say so.

**Fix (paste-ready below, executed in the clone).** Add the four spellings to
`UNBOUND_RECEIVERS`. Give `ResourceHandle` an `OPEN_METHODS` row of `(0, 1)`
for both spellings. Without that row, adding it to the list moves the shifted
`<expr>` encoding slot to position 3, and `ResourceHandle.open(h, "r", "utf-8")`
then flips from correctly passing to reported (executed). Plant two `UNNAMED`
cases and one `NAMED` case, then correct the comment, J1 and the changelog
line. With the fix the module ran 144 passed. With the four list rows removed,
both new `UNNAMED` cases were red (no site). With the `OPEN_METHODS` rows
removed, both new `NAMED` cases were red. The clone was reverted afterwards.

A narrower answer is possible: keep the code and narrow J1 and the comment to
*a class that defines the method in its own body*. That leaves an under-report
which the record would then state, and the module's own rule is that a call
the walk does not know is a row to add.

### ⬜ 2 — the `Traversable` fix turns `Traversable.open(t, "r", "utf-8")` from passing to reported

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:235`

Executed at the base and at the target. With `Traversable` in
`UNBOUND_RECEIVERS` and no `OPEN_METHODS` row, a class call to `.open` uses
`<expr>`'s `(0, 2)` shifted to `(1, 3)`. `Traversable.open(mode='r', *args)`
takes its encoding at `args[0]`, the slot `zipfile.Path` has, so a positional
encoding after the mode is missed. The shape passed at the base, by accident:
unshifted slot 2 held it. It is reported at the target.

The release ships no reading defect from this. `Traversable.open` is abstract
and its body is only a docstring (read on 3.12 and 3.14), so called on the
class it opens nothing. It is an over-report on a call nobody writes. The
`OPEN_METHODS` rows in 🟡 1's fix close it, along with the `NAMED` case that
is red without them (executed).

### ⬜ 3 — the list of modules that do not import on macOS names nine, and the construction failed on fourteen

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:143`

The comment over `NOT_A_FILE_OPENER`, and J1 in the same words, say that each
module that does not import on macOS was read in its documentation. They then
name nine modules. On 3.12 the construction also failed on five Windows-only
submodules: asyncio.windows_events, asyncio.windows_utils, encodings.mbcs,
encodings.oem and multiprocessing.popen_spawn_win32 (executed). None of the
five carries a module-level `open` (executed: a search of each source file).
So the set is right, and only the sentence is incomplete. Round 1's report
mentioned *Windows-only submodules* without naming them.

### ⬜ 4 — round 1's class table calls `ResourceHandle` a class that raises or opens bytes (correction)

`seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-1-report.md:97`

This is paperwork and does not count toward `Needs a fix`. The row
*`MultiplexedPath`, `ResourceContainer`, `ResourceHandle` — no: they raise,
or open bytes* is wrong twice. `ResourceHandle.open` opens text in the locale
(the smith's note, confirmed). Both `ResourceHandle` and `ResourceContainer`
inherit `Traversable.read_text` (🟡 1). Only `MultiplexedPath` overrides
`read_text` to raise. The report is a committed record, so the orchestrator
decides whether the correction goes into it or into this round's record.

## Round 1's findings, each checked against the fix

- **Finding 1 (`ossaudiodev`): closed.** `ossaudiodev` is in
  `NOT_A_FILE_OPENER` at :167. Its `NAMED` case is at :852 and passes at the
  target. The same shape is reported at the base (executed; the base has no
  row, so the case is red there). The docstring list (:35), the comment
  (:143–147), the changelog bullet and J1 now say how the modules that do not
  import were settled. Of those wordings, only ⬜ 3's omission remains.
- **Finding 2 (`Traversable`): closed for `Traversable`.** Both spellings are
  in the list (:184–185). Both `UNNAMED` cases (:759, :763) are reported at
  the target and give no site at the base (executed). The
  `from importlib.resources import abc` spelling is reported too. `importlib.abc.Traversable`
  is absent on 3.14 and present on 3.12 and 3.13 (executed), as the comment
  says. J1 got narrower in one place: *a method called on a class that list
  holds*. It also gained a claim the fix did not earn, which is 🟡 1.
- **Finding 3 (S3 and `OPEN_METHODS`): closed.** The assertion at :952 is red
  with a foreign `OPEN_METHODS` row
  (`importlib.metadata.PathDistribution`), executed. It passes at the target,
  whose rows are `<expr>` and `zipfile.Path`.
- **Finding 4 (the rebinding sentence): closed.** The docstring at :66–70 now
  names any binding in any scope. Executed at the target: an assignment, a
  loop variable and a parameter rebinding an imported `wave` each give no
  site, which is what the sentence states. J1's note says the same.

## The three `survivors.md` exemptions

All three are true. `survivor-check --range 88434e82..ad9ecb24 --exempt
<survivors.md>` passes with three exempt survivors. Without `--exempt` it exits
1 (executed). Each quote is where the file says it is, and each grounds cell
holds:

- **`spec.md:73`** is the frame's C1 describing the defect at the base. The
  defect it names is closed for every class the list holds.
- **The docstring of `methods_of_unbound_receivers` (:928)** describes the
  filter at :935 exactly.
- **The failure message at :960** names what its own assertion checks. The new
  `OPEN_METHODS` assertion has its own message at :954.

Stop rules: J1's anchors resolve at the target with 13 ok and 0 drifted
(`evidence-check --strict --ledger` on the fragment, executed).
`unverified-check` reads `overview.md` as 1 closed (the ✅ row) and 1 open
(the sealer's), executed.

## Regression tests to plant

In `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`:

- in `UNNAMED`: `"ResourceHandle.read_text unbound, inherited from Traversable"`
  and `"ResourceContainer.read_text unbound, the importlib.simple spelling"`
  (🟡 1);
- in `NAMED`: `"ResourceHandle.open unbound, encoding after the mode"` (🟡 1)
  and `"Traversable.open unbound, encoding after the mode"` (⬜ 2).

Each was seen red as stated under 🟡 1.

## Facts for the evidence ledger

- J1's claim cell, once 🟡 1 is fixed: `UNBOUND_RECEIVERS` holds every public
  standard-library class whose `open`, `read_text` or `write_text`, defined or
  inherited, reads text in the locale when called on the class. Its evidence
  cell should say the enumeration was rerun with inherited methods in round 2
  of review. That run found `ResourceHandle` and `ResourceContainer` through
  `Traversable.read_text`, and no other class.
- `importlib.simple` re-exports `ResourceHandle` and `ResourceContainer` on
  3.12 to 3.14. `importlib.abc.Traversable` exists on 3.12 and 3.13 and not on
  3.14.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a class-called `ResourceHandle.read_text(h)` or `ResourceContainer.read_text(c)` reads the locale through the inherited `Traversable.read_text` and passes; J1 and the `UNBOUND_RECEIVERS` comment, both written by round 1's fixes, say the list holds every such class | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:178` | open | executed: the inherited-method enumeration on 3.12.11, 3.13.9 and 3.14.3 finds exactly these two; no site at the base or the target; `ResourceContainer.read_text(x)` calls `x.open(encoding=None)`; `importlib.simple` re-exports both; the proposed fix ran 144 passed and its cases were red without its rows |
| ⬜ 2 | adding `Traversable` to `UNBOUND_RECEIVERS` without an `OPEN_METHODS` row turns `Traversable.open(t, "r", "utf-8")` from passing to reported | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:235` | open | executed: passes at the base, reported at the target; read: the class-called method is abstract with a docstring-only body, so it is an over-report on a call that opens nothing; closed by 🟡 1's fix |
| ⬜ 3 | the comment over `NOT_A_FILE_OPENER` and J1 name nine modules that do not import on macOS; five Windows-only submodules also failed and are not named | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:143` | open | executed: the 3.12 failed-import list holds fourteen names; a search of the five sources finds no module-level `open`, so the set is right and only the sentence is incomplete |
| ⬜ 4 | correction: round 1's class table says `ResourceHandle` and `ResourceContainer` raise or open bytes | `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-1-report.md:97` | open | paperwork, not counted toward Needs a fix; executed: `ResourceHandle.open` hands `None` on to `io.TextIOWrapper`, and both classes inherit `Traversable.read_text` |
| 🟢 | round 1's finding 1 is closed — `ossaudiodev` excused, with its case and the three records' wording | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:167` | confirmed | executed: reported at the base, no site at the target; the `NAMED` case at :852 passes; read: docstring, comment, changelog and J1 say how the modules that do not import were settled |
| 🟢 | round 1's finding 2 is closed — a class-called `Traversable.read_text` is shifted, in both spellings, with two cases | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:184` | confirmed | executed: three spellings reported at the target, none at the base; `importlib.abc.Traversable` present on 3.12 and 3.13, absent on 3.14 as the comment says |
| 🟢 | round 1's finding 3 is closed — S3 holds every `OPEN_METHODS` key to `UNBOUND_RECEIVERS` | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:952` | confirmed | executed: red with a foreign `OPEN_METHODS` row, green at the target |
| 🟢 | round 1's finding 4 is closed — the rebinding limit names any binding in any scope | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:66` | confirmed | executed: assignment, loop variable and parameter rebinding an imported `wave` each give no site at the target, as the sentence states |
| 🟢 | the three `survivors.md` exemptions are each true | `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/survivors.md` | confirmed | executed: `survivor-check` over the fix range passes with the file and exits 1 without it; read: each quote at its coordinate, each grounds cell holds |
| 🟢 | the smith's correction: `ResourceHandle.open` opens locale text, and a class call to it is reported | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:235` | confirmed | executed: four unnamed class-call shapes reported, the named one passes; read: its body wraps the stream in `io.TextIOWrapper(stream, *args, **kwargs)`; incomplete, see 🟡 1 and ⬜ 4 |
| carried | round 1's C1, C2 and C3 confirmations | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:349` | confirmed | carried from round 1 as the prompt asked, not re-derived; the fixes touched `UNBOUND_RECEIVERS` and `NOT_A_FILE_OPENER`, and the module's own C1 and C3 cases pass at the target (executed, 140 passed) |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 and ⬜ 2

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

### ⬜ 3

```text
# The comment over NOT_A_FILE_OPENER, its last three lines, become:
# does not was read in its documentation instead: `dbm.gnu`, `nt` and
# `ossaudiodev` carry an `open`; `nis`, `spwd`, `msilib`, `msvcrt`, `winreg`,
# `winsound` and five Windows-only submodules of `asyncio`, `encodings` and
# `multiprocessing` carry none.
# J1's evidence cell takes the same addition.
```

Needs a fix: yes — 🟡 1 (a class-called `ResourceHandle.read_text` or
`ResourceContainer.read_text` passes, and J1 and the comment say no such class
is left)
Loses a record or crashes: no

## Proof block

Files opened in the clone at 69273b86, or in the tree under review:

- `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`:
  lines 1–460 and 860–970 read whole, the rest through the fix diff and
  searches
- `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-1.md`
- the same directory's `rounds/round-1-report.md` (lines 40–150, plus a
  search), `survivors.md` and `overview.md` (lines 15–35)
- the fix range's diff of `changelog.md`, `overview.md`, `round-1.md`,
  `survivors.md`, the ledger fragment and the test module
- `bin/survivor-check`, plus the `--help` of `evidence-check` and
  `unverified-check`
- CPython source of `importlib.resources.abc` (`Traversable.open`,
  `Traversable.read_text`) and `importlib.resources.simple`
  (`ResourceHandle.open`), through inspect on 3.12.11 and 3.14.3
- the five Windows-only submodule sources, searched only

Leavings: the clone, the base extract and the probe files all sit under
`<scratchpad>/1791119068-…/round-2/` and are removed at handover.
