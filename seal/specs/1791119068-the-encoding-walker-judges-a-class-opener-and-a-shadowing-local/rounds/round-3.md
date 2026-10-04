# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — review round 3

| Field | Value |
|---|---|
| Target SHA | a3ebd97dc7c040fb3d24451b26f011c6ab3f596f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #782 |
| Broad gate | 86903035 against 94d7b2e0 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of #762 (PR #782), the verifying round and the run's last, at a3ebd97d: open round 2's fixes (range 06dd7a22..dc823460) and judge whether each closes its finding with no regression — the inherited-method class enumeration and its added rows (ResourceHandle, ResourceContainer, pipes.Template), the Traversable over-report, the Windows-only submodules — and whether J1's completeness claim is true as written.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the comment above `NOT_A_FILE_OPENER` and J1 name fourteen modules that do not import and were read instead; 3.12's `lib2to3.pgen2.conv` also fails to import and is not named; J1 also calls the sources read "C sources", but six of them are Python | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:146` | deferred PR #782 | the run is capped: round 2 was its one reopening, and this record ends it. Executed: fifteen failed imports on 3.12.11, `No module named 'pgen2'`; read: `conv.py` and `grammar.py` define no `open`, `read_text` or `write_text` and no module-level `open`, so the set is right and only the sentence is short. Rung 4: nobody has agreed to act on it, so it goes in this record and in PR #782's body |
| ⬜ 2 | the comment above `UNBOUND_RECEIVERS` and J1 list what the class enumeration left out, and `idlelib`'s `FileList`, `IOBinding` and the search dialogs, which have `open` on 3.12–3.14, are not among them and fit none of the four reasons as written; the comment's "these are the classes whose method reads text in the locale" describes every member, and `pathlib.PurePath` has no such method | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:177` | deferred PR #782 | the run is capped: round 2 was its one reopening, and this record ends it. Executed: the enumeration lists the `idlelib` classes on all three interpreters; `PurePath` has none of the three methods on any of them. Read: `IOBinding.loadfile` reads through `tokenize.open`, the encoding the file declares, so leaving them out is right and the list holds. Rung 4, as ⬜ 1 |
| 🟢 | round 2's finding 1 is closed — `ResourceHandle` and `ResourceContainer` (both spellings) and 3.12's `pipes.Template` are judged with the path shift, each with its open-slot row | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:192` | confirmed | executed: each class-called `read_text` without an encoding is reported at the target and gave no site at `06dd7a22`; `pipes.Template.open(t, f, "r")` the same; each of the twelve added rows, removed alone, turns its case red; an independent inherited-method enumeration on 3.12.11, 3.13.9 and 3.14.3 finds no other class outside the list whose class-called method reads the locale |
| 🟢 | the `pipes.Template: (1, 2)` row passes no call that opens a file in the locale | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:274` | confirmed | executed: sixteen shapes; the ones that pass are a `"rb"` mode, a third positional and `encoding=`, and each of those raises `ValueError` or `TypeError` before anything is opened; class-called, receiver-built, aliased, `rw=`, splatted and non-literal-mode shapes are all reported. Read: pipes source, lines 145–171 |
| 🟢 | round 2's finding 2 is closed — `Traversable.open(t, "r", "utf-8")` passes again | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:266` | confirmed | executed: no site at the target for both spellings; each `NAMED` case red without its row; `Traversable.open(t, "r")` still reported |
| 🟢 | round 2's finding 3 is closed — the five Windows-only submodules are named in the comment and in J1 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:149` | confirmed | read: both places name the five; executed: they are among my 3.12 failed imports, and none defines one of the three methods. A fifteenth module is ⬜ 1 |
| carried | round 2's finding 4 (the correction to round 1's class table) and rounds 1–2's confirmations | `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-2.md` | confirmed | carried as the prompt asked, not re-derived; the fix range touches none of their units except the tables re-checked above, and the module passes at the target (executed, 151 passed) |
| ❓ | `msilib`'s 3.12 source defines no class with `open`, `read_text` or `write_text` | J1's evidence cell, `seal/ledger/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local.md:2` | ❓ out of verified scope | no 3.12 interpreter on this machine ships `msilib`, so the claim stands as the smith's reading and was not re-established. The sealer or whoever has a Windows 3.12 install answers it; nothing in the list depends on it unless such a class exists |

## Paste-ready fixes

```text
# ⬜ 1 — the comment above NOT_A_FILE_OPENER, its last lines become:
# does not was read in its documentation instead: `dbm.gnu`, `nt` and
# `ossaudiodev` carry an `open`; `nis`, `spwd`, `msilib`, `msvcrt`, `winreg`,
# `winsound`, the Windows-only submodules `asyncio.windows_events`,
# `asyncio.windows_utils`, `encodings.mbcs`, `encodings.oem` and
# `multiprocessing.popen_spawn_win32`, and 3.12's `lib2to3.pgen2.conv`,
# which imports `pgen2` absolutely and fails everywhere, carry none.
#
# J1's evidence cell: add "and 3.12's `lib2to3.pgen2.conv`" after
# "`multiprocessing.popen_spawn_win32`", and replace
#   "`msilib`'s 3.12 source and the C sources of the other modules"
# with
#   "`msilib`'s 3.12 source and the sources of the other modules"
```
```text
# ⬜ 2 — the comment above UNBOUND_RECEIVERS, its last sentences become:
# These classes, apart from `PurePath`, which has none of the three methods
# and is kept for the spelling, are the ones whose method, called on the
# class, reads text in the locale, itself or by handing `encoding=None` on to
# the receiver's `open`: `Traversable.read_text`, which `ResourceHandle` and
# `ResourceContainer` inherit, does that. Left out: methods that open no text
# file (`imaplib`, `telnetlib`, `tkinter.tix`, `urllib.request`, `webbrowser`,
# `ZipFile`, `TarFile`, `idlelib`'s search dialogs), that read a fixed
# encoding (`importlib.metadata`) or the one the file declares (`idlelib`'s
# `FileList` and `IOBinding`, through `tokenize.open`), that raise
# (`MultiplexedPath`), and protocol stubs. The modules that do not import on
# macOS were read in CPython's 3.12 source and hold no such class.
#
# J1's evidence cell, the "Left out:" sentence: add `idlelib`'s search
# dialogs to the first group and "or the one the file declares (`idlelib`'s
# `FileList` and `IOBinding`)" after "reading a fixed encoding
# (`importlib.metadata`)".
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on this module in the clone at a3ebd97d | 151 passed |
| the walker at the target and at `06dd7a22` (the fix range's base, its tests directory extracted) on 39 shapes: 16 `pipes.Template`, 17 `ResourceHandle` / `ResourceContainer` / `Traversable`, 6 neighbours (`zipfile.Path`, `Path`, bare receivers) | as stated per verdict; the neighbours are unchanged |
| each of the twelve rows round 2 added removed alone, the module run, the file restored | all twelve red; each `UNBOUND_RECEIVERS` row fails its `UNNAMED` case and `test_no_method_is_matched_by_its_dotted_name`, each `OPEN_METHODS` row fails its own `NAMED` or `UNNAMED` case; restored byte for byte, clone clean |
| the inherited-method class enumeration on 3.12.11, 3.13.9, 3.14.3 (sketch below) | outside the list, every class is left out for a reason that holds (binary, network, URL, dialog, fixed or declared encoding, raises, abstract) or is a name its module imported for itself; failed imports: fifteen on 3.12, ten on 3.13 and 3.14 |
| every module-level `__getattr__` on the three interpreters, read | only `importlib.abc`'s serves a class with one of the three methods |
| `lib2to3/pgen2/conv.py`, `grammar.py`, the five Windows-only submodules, searched for the three method names; `idlelib/iomenu.py` `loadfile` and `open`; `pipes.py` `open`; `importlib/resources/simple.py` and `abc.py` signatures on all three | as stated in ⬜ 1, ⬜ 2 and the `pipes` verdict |
| `evidence-check --strict --ledger` on this work item's ledger fragment | 13 ok, 0 drifted, 0 broken; records: 0 refused |
| `survivor-check --range 06dd7a22..dc823460`, with and without `--exempt survivors.md` | no removed wording still standing, both ways |
| the full suite, repository-wide lint, typecheck, `evidence-check .` over the repository | not yet, and not this round's: the sealer's, after the rounds settle |

```
# the inherited-method enumeration, run once per interpreter
for each module in sys.stdlib_module_names and its submodules (no "_" part, no test packages):
    import it (record the failures)
    for each class name in vars(module) and module.__all__ (getattr for the latter):
        for meth in (open, read_text, write_text):
            if inspect.getattr_static(cls, meth) exists:
                print spelling, home / __all__ / imported-for-itself, meth,
                      the class in cls.__mro__ whose body defines it, and its kind
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
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:178` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:235` | round 2's ⬜ 2 — fixed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:143` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-1-report.md:97` | round 2's ⬜ 4 — answered |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:167` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:184` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:952` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/survivors.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — `lib2to3.pgen2.conv` is missing from the modules read in place of an import, and "C sources" should read "sources" | PR #782's body, with this record | nobody has agreed to act on it (rung 4). The orchestrator may take it as a post-seal edit to the comment and J1, since the branch owns both |
| ⬜ 2 — `idlelib`'s classes are missing from the "left out" list, and "these are the classes" should not include `PurePath` | PR #782's body, with this record | nobody has agreed to act on it (rung 4). The orchestrator may take it with ⬜ 1, in the same two places |
