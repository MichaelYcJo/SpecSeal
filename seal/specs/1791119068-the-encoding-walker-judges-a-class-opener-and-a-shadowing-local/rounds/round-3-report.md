# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — review round 3 report

- Target SHA: a3ebd97d (round 2's fix range `06dd7a22..dc823460`, closed at a3ebd97d)
- PR: #782 (draft), issue #762
- Ran by: specseal:warden on claude-opus-5-5
- Round kind: the verifying round after the one reopening. This round ends the run whatever it finds, so what it opens is reported as deferral candidates, at the severity found.

## What this round was asked

Open round 2's fixes and judge whether each closes its finding with no regression: 🟡 1 (the class enumeration re-run with inherited methods; `ResourceHandle`, `ResourceContainer` in both spellings and 3.12's `pipes.Template` added to `UNBOUND_RECEIVERS`; seven `OPEN_METHODS` rows, among them `pipes.Template: (1, 2)`), ⬜ 2 (the `Traversable.open(t, "r", "utf-8")` over-report) and ⬜ 3 (the Windows-only submodules named). Check that the `pipes.Template` position choice cannot pass a call it should report, and whether J1's completeness claim is true as written. Rounds 1 and 2's 🟢 verdicts are inherited, and only what the fixes touch is re-checked.

## What the account claimed, and what I found

The fix commits and J1 claim three things. I checked each against the code and against an enumeration of my own.

1. **The list is complete.** J1 says `UNBOUND_RECEIVERS` holds every public standard-library class, under its home module, an `__all__` re-export or a module `__getattr__` alias, whose `open`, `read_text` or `write_text`, defined or inherited, reads text in the locale when called on the class. **Executed:** I re-ran the enumeration on 3.12.11, 3.13.9 and 3.14.3, independently of the smith's script. It covered every importable stdlib module and submodule, every class in its `vars` and its `__all__`, and `inspect.getattr_static` for each of the three methods with the class in the MRO that defines it. Every class it finds falls in one of three groups: in the list; left out for a reason that holds when I read the source; or a name imported only for the module's own use. The claim is true. Every module-level `__getattr__` on the three interpreters was also read (calendar, concurrent.futures, unittest, urllib.parse, zoneinfo, types, typing, asyncio, importlib.machinery, shutil, sqlite3, ast). None serves a class that has one of the three methods, apart from `importlib.abc`'s.
2. **The account of how the list was settled names everything left out.** It does not, in two places. Neither changes the list. See ⬜ 1 and ⬜ 2.
3. **`pipes.Template: (1, 2)` cannot pass a call that should be reported.** **Executed:** sixteen `pipes.Template` shapes went through the walker at the target. The ones that pass are `"rb"` as the mode, a third positional argument, and `encoding=` as a keyword. Each of those raises before it opens anything: `Template.open` raises `ValueError` for any mode but `'r'` or `'w'`, and it takes exactly `(file, rw)`, so a third argument or a keyword is a `TypeError`. **Read:** 3.12's pipes source, lines 145–171. Every shape that opens a file without raising is reported: class-called, built in the receiver, aliased, `rw=` by keyword, splatted, or with a mode that is not a literal. The choice is sound.

### Round 2's findings

- **Round 2's finding 1 is closed.** **Executed:** `ResourceHandle.read_text(h)`, `ResourceContainer.read_text(c)` and their `importlib.simple` spellings are reported at the target. At the fix range's base they gave no site. A positional or keyword encoding passes, and `None` written out is reported. `pipes.Template.open(t, f, "r")` is reported; at the base it gave no site, with `"r"` read as the encoding. I removed each of the twelve rows round 2 added, one at a time, and ran the module each time. Every removal turned a case red. Each `UNBOUND_RECEIVERS` removal failed its `UNNAMED` case and `test_no_method_is_matched_by_its_dotted_name`. Each `OPEN_METHODS` removal failed its own `NAMED` or `UNNAMED` case. So no added row is unpinned.
- **Round 2's finding 2 is closed.** **Executed:** `Traversable.open(t, "r", "utf-8")` passes at the target, and both spellings' `NAMED` cases go red without their rows. `Traversable.open(t, "r")` is still reported, as it should be.
- **Round 2's finding 3 is closed as asked.** **Read:** the comment above `NOT_A_FILE_OPENER` and J1 now name the five Windows-only submodules. **Executed:** my 3.12 import walk failed on fifteen modules, one more than round 2's fourteen. The fifteenth is ⬜ 1.
- **Round 2's finding 4** (the correction to round 1's class table) was answered as paperwork. I carried that verdict without re-deriving it, because nothing in the fix range touches it.

### No regression

**Executed:** the module ran in the clone at a3ebd97d with 151 passed, matching the orchestrator's run. `zipfile.Path.open`, `Path.read_text`, `Path.open` on its class and the bare-receiver `p.open` / `p.read_text` judge exactly as they did at the base. The shapes that changed at all are the class-called and receiver-built forms of the new classes. Each of them moved from passing or `<expr>` to its own row's verdict, and each one I checked moved in the right direction.

One shape now reports a call that cannot open anything. `ResourceContainer.open(c, "r")` is reported, though `ResourceContainer.open` raises `IsADirectoryError` on every call. It was reported at the base too, as `<expr>.open()` with a mode that was not a literal, so this is not a regression. No real code calls `open` on a container, and the comment above the row says the method raises. I recorded no finding for it.

### ⬜ 1 — a fifteenth module does not import, and the list of modules read in its place omits it

`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:146` (the comment above `NOT_A_FILE_OPENER`) and J1's evidence cell (`seal/ledger/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local.md:2`) both describe how the modules that do not import on macOS were settled. Each one was read in its documentation instead, and fourteen are named. On 3.12, `lib2to3.pgen2.conv` also fails to import, on every platform, because of its `from pgen2 import grammar`. It is not named.

**Executed:** the failed-import list on 3.12.11 has fifteen names, and the import error is `ModuleNotFoundError: No module named 'pgen2'`. **Read:** `conv.py` has no module-level `open`, and its one class, `Converter`, defines no `open`, `read_text` or `write_text`; neither does `pgen2/grammar.py`. So the set and the class list are both right, and only the sentence is incomplete.

J1's next sentence has a second inaccuracy: *"`msilib`'s 3.12 source and the C sources of the other modules that do not import on macOS define no such method"*. Five of those modules are Windows-only submodules, and `conv` is also Python, so they have Python sources rather than C ones. **Read:** a search of all six Python sources finds no `def open`, `def read_text` or `def write_text`.

Why it is ⬜: no behaviour and no fact about the list is wrong. The cost lands on the next person who re-runs the walk. They count fifteen failures against fourteen names and have to work out which side is short, which is how round 2's ⬜ 3 started.

### ⬜ 2 — the comment's "left out" list leaves out `idlelib`, and its "these are" sentence does not fit `PurePath`

The comment above `UNBOUND_RECEIVERS` is at `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py:177`. Its last sentence lists what the enumeration left out, and J1 repeats it: methods that open no text file (`imaplib`, `telnetlib`, `tkinter.tix`, `urllib.request`, `webbrowser`, `ZipFile`, `TarFile`), methods that read a fixed encoding, methods that raise, and protocol stubs.

**Executed:** on all three interpreters the enumeration also finds `open` on these `idlelib` classes:
- `idlelib.filelist.FileList`, and `idlelib.pyshell.PyShellFileList` through it;
- `idlelib.iomenu.IOBinding`;
- `idlelib.searchbase.SearchDialogBase`, and the search, replace and grep dialogs that inherit or override its `open`.

None of these appears in the list. **Read:** the dialogs' `open` shows a window, so they fit "open no text file". But `FileList.open` and `IOBinding.open` do open and read a text file, through `IOBinding.loadfile`, which uses `tokenize.open` (`idlelib/iomenu.py:126`). That is the encoding the file declares, with a prompt to the user as the fallback (`:141`). It is not the locale, so leaving them out is right. The reason fits none of the four categories as written, though. It is the reason the `NOT_A_FILE_OPENER` comment gives for `tokenize`.

The same comment says *"These are the classes whose method, called on the class, reads text in the locale"*. `pathlib.PurePath` has been in the list since before this work item, and on 3.12–3.14 it has none of the three methods. The list is a safe superset. The sentence describes every member, though, and one member does not fit it.

Why it is ⬜: the main claim, that every class whose method reads the locale is in the list, holds on my enumeration. What is incomplete is the account of the classes left out and why.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — `lib2to3.pgen2.conv` is missing from the modules read in place of an import, and "C sources" should read "sources" | PR #782's body, with this record | nobody has agreed to act on it (rung 4). The orchestrator may take it as a post-seal edit to the comment and J1, since the branch owns both |
| ⬜ 2 — `idlelib`'s classes are missing from the "left out" list, and "these are the classes" should not include `PurePath` | PR #782's body, with this record | nobody has agreed to act on it (rung 4). The orchestrator may take it with ⬜ 1, in the same two places |

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

Needs a fix: no
Loses a record or crashes: no

The gate has come due: this report leaves nothing open that needs a fix, so what comes next is the sealer's spawn.

## Proof block

- Files opened: `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` (lines 1–560 at the target, the fix diff, and the base's `UNBOUND_RECEIVERS`), `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-2.md`, `seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/rounds/round-2-report.md`, the fix range's diff of `seal/ledger/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local.md` and `changelog.md`, `docs/review-chain-spec.md` (the ladder and the deferred vocabulary), the `DEFERRED` vocabulary in `skills/code-review/scripts/chain_check.py`, `bin/test`. From the interpreters: `idlelib/iomenu.py`, `pipes.py`, `lib2to3/pgen2/conv.py`, and `importlib/resources/simple.py` and `abc.py` on all three versions.
- Clone and probes: under the session scratchpad at `1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/round-3/`, removed before handover.
- Ran by: specseal:warden on claude-opus-5-5
