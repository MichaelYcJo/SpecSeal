# Feature Specification: the encoding walker judges a class opener and a shadowing local (#762)

<!-- seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Why this rung

`skills/implement/SKILL.md` §3 puts work that alters *a gate's verdict* on
the top rung. The walker in
`tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py` is a
gate in that sense: `CONTRIBUTING.md` §*House rules* names it as what enforces
*Every file read or written names its encoding*, and its repository case fails
every CI leg on an unnamed call. This work changes what it reports. After it,
`zipfile.Path.open(q, "r")` fails a contributor's branch where today it
passes, and `dbm.gnu.open(p)` passes where today it fails. No file in the tree
changes verdict (read: the grep in §*Grounding*'s last row), but a future
branch's does, so this is a `spec.md` and a `plan.md`, not a scope line.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*House rules*, *Every file read or written names its encoding* | The rule the walker enforces. It names no receiver, so nothing in it changes; `test_the_rule_is_where_a_contributor_reads_it` pins its wording and stays green untouched |
| The walker's module docstring, K2 (*what the walk cannot prove counts as unnamed*) | Decides 🟡 2: a bare name no import binds is a value the walk cannot prove, so its `.open()` is judged, whatever the name is spelled |
| `seal/specs/1791076830-every-file-the-plugin-reads-or-writes-names-its-encoding/spec.md` §*The class, enumerated by construction*, K1's `<expr>.open` row (line 86) | The released contract this work narrows. It is not edited here: see §*Decisions* D5 |
| The same work item's `rounds/round-3-report.md` §*Findings* and §*Paste-ready fixes* (in the tree until the 0.18.2 release prepares; durable at `v0.18.1`) | The findings this work closes: 🟡 1, 🟡 2, ⬜ 3, ⬜ 4, ⬜ 5. Its paste-ready diffs are a starting point to re-derive, not text to paste (D6) |
| `skills/agent-contract/SKILL.md` §12 and §15 | Each defect is fixed for its class, enumerated in §*The classes*, and every new case is seen red before it is committed |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, with `seal/config.md`'s `Ledger frozen from` | Released row E1 in `seal/releases/0.18.1.md` cites `judge` by hash; its re-read is a `Re-read ·` row in this work item's fragment, never an edit to the released file |
| `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | The changelog entry is this work item's `changelog.md`; the ledger rows are `seal/ledger/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local.md` |
| `skills/settle/SKILL.md` §*2. Write one standing statement per segment*, *The newest work item wins where two say different things* | Why this spec, rather than an edit to #741's, is where the corrected K1 receiver sentence lives (D5) |
| Read 2026-10-04: a grep of every tracked `.py` for a bare `os`, `webbrowser`, `wave`, `tarfile`, `shelve` or `dbm` local, a class-called `Path.open`, `.joinpath(` on a `zipfile.Path`, `dbm.gnu`/`ndbm`/`sqlite3` and `tokenize.open`, outside the walker's own module | No hit but three `tmp_path.joinpath(...)` on pathlib, which no change here touches. So no tree verdict moves. **Read, not executed** — the repository case running green after the build is what executes it |

## Scope

**In.**

1. 🟡 1 — a method opener called on its class is judged with the path shift,
   for the whole class (§*The classes*, C1), not for one key.
2. 🟡 2 — a bare name no import binds is no longer excused at all: its
   `.open()` is judged as `<expr>.open` (D2).
3. ⬜ 4 — every standard-library module whose module-level `open` takes no
   locale encoding is excused, enumerated by construction (C3): `dbm.gnu`,
   `dbm.ndbm`, `dbm.sqlite3`, `aifc`, `sunau`, `tokenize`, `posix`, `nt`,
   beside the ten already listed.
4. ⬜ 3 — the docstring says exactly which `zipfile.Path` receivers are judged
   at `zipfile.Path.open`'s positions (a `zipfile.Path(...)` built in the
   receiver, or the class itself), and that one reached by `/`, `.joinpath` or
   a name is judged as `Path.open` and passes when `encoding=` is a keyword
   (D3).
5. ⬜ 5 and the issue's second box — the module docstring, the `owner`
   docstring and the comment over `NOT_A_FILE_OPENER` name exactly the
   receivers the code excuses; and the K1 `<expr>.open` row below, in this
   spec, is the corrected sentence #741's line 86 is superseded by (D5).
6. The regression cases (§*User scenarios*), each seen red.
7. This work item's `changelog.md` (`### Fixed`) and its ledger fragment: one
   `Re-read ·` row for E1, and one new row for the claims this work adds.

**Out, and why.**

| Left out | Why |
|---|---|
| Tracing a `zipfile.Path` through `/`, `.joinpath` or a name (⬜ 3's behaviour) | An over-report, which fails loud, and the repair the failure message already names (`encoding=` as a keyword) passes it. Tracing it is two new branches in `owner` for a shape nothing in the tree has, and the walk already declines to trace a `ZipFile` bound to a name for the same reason. The docstring says so instead (D3) |
| A local that rebinds an IMPORTED module's name in a narrower scope (`import wave` at the top, `def f(wave): wave.open()`) | `bindings` is file-wide and scope-blind by design, and the docstring's *What no row can hold* already lists name-following limits of the same kind (`f = open; f(p)`). Scope tracking is new mechanism in the walk, not a fix to `owner`. The docstring names the shape in that paragraph (D4), so the limit is stated rather than found |
| Editing #741's `spec.md` line 86 | A released work item's records are records of a moment (`docs/the-evidence-ledger.md`, `<!-- specs/1788761915-a-record-states-what-nothing-reads -->`); `settle` folds the newest work item's sentence where two disagree (D5) |
| `.open` on an arbitrary receiver that opens no file (`webbrowser.get().open(u)`, `build_opener().open(u)`) | `<expr>.open` judged as `Path.open` is #741's deliberate over-report for a walk with no types (K2). C3 enumerates modules, which the walk can prove by import; an instance it cannot |
| Any change to `CONTRIBUTING.md`, `failure`'s message or the repair text | None of them names a receiver; §14 of the contract is not engaged because no text a person reads at a red leg changes |

## The classes

Each finding names an instance; §12 of the agent contract owes the class.

**C1 — a method opener the top of `judge` can match by dotted name.** `judge`
opens with `if target in OPENERS`, and `target` is the call's dotted name. A
key of `OPENERS` that is a method of a class in `UNBOUND_RECEIVERS` is
reachable from there when the method is called on its class, and is then
judged without the shift. Enumerated by construction over `OPENERS` (read
2026-10-04): `builtins.open`, `io.open`, `codecs.open`, `os.fdopen` are
functions; `<expr>.open` is never a dotted name; `zipfile.Path.open` is the
one member. The other tables the top of `judge` matches hold functions and
constructors only. **The fix removes the class, not the member**: a method's
positions live where only the `.open` branch reads them, so a method row added
later cannot be reached by the top-of-`judge` lookup (D1).

**C2 — a receiver `owner` excuses by spelling rather than by import.** The
bare-name branch of `owner` returns a name no import binds as itself, and
`judge` then excuses it when the spelling is in `NOT_A_FILE_OPENER`. Every
bare-spelled member of that set is a member of the class: today `os`,
`webbrowser`, `tarfile`, `shelve`, `dbm`, `wave`, and after C3 also `aifc`,
`sunau`, `tokenize`, `posix`, `nt`. Removing the branch closes all of them at
once, including the ones C3 adds (D2).

**C3 — a standard-library module whose module-level `open` takes no locale
encoding.** Enumerated by construction, not by reading round 3: every
importable standard-library module and submodule carrying a callable `open`.
Executed 2026-10-04 on 3.13.5, with the presence of the version-dependent
ones checked on 3.14.3:

| Module | Already excused or tabled | Its `open` |
|---|---|---|
| `builtins`, `io`, `codecs` | `OPENERS` | the openers K1 judges |
| `gzip`, `bz2`, `lzma`, `compression.*` | `BINARY_BY_DEFAULT` | binary unless `t` |
| `os`, `webbrowser`, `tarfile`, `shelve`, `dbm`, `dbm.dumb`, `wave` | `NOT_A_FILE_OPENER` | no text |
| `dbm.ndbm`, `dbm.sqlite3` (3.13+), `dbm.gnu` (absent on both local builds; present where built with gdbm) | **added** | a key-value store, no text |
| `aifc`, `sunau` (3.12 only, the suite's floor) | **added** | binary audio, like `wave` |
| `posix`, `nt` (one per platform) | **added** | `os.open`'s implementation: a file descriptor |
| `tokenize` | **added** | text in the encoding the file declares, UTF-8 by default — never the locale's |

The build re-runs the construction on 3.12 (questions.md M2), because `aifc`
and `sunau` are present there alone, and records the result in its phase
record.

## K1's `<expr>.open` row, as it stands after this work

This row supersedes #741's `spec.md` line 86 (D5):

| Call shape | Unnamed when |
|---|---|
| `<expr>.open(...)` on any receiver except a module the file imports whose `open` takes no locale encoding (`os`, `webbrowser`, `tarfile`, `shelve`, `dbm` and its four submodules, `wave`, `aifc`, `sunau`, `tokenize`, `posix`, `nt`), PIL's `Image`, and a `ZipFile(...)` or `TarFile(...)` built in the receiver itself. A bare name no import binds is excused under no spelling | judged as `Path.open`: text mode and `encoding` neither a keyword nor the 3rd positional; the 2nd positional on a `zipfile.Path(...)` built in the receiver; every position one to the right where the method is called on its class (`Path.open(p)`, `zipfile.Path.open(p)`). A `zipfile.Path` reached by `/`, `.joinpath` or a name is judged as `Path.open` |

## Decisions

Judgments the ticket left open that the tree answered.

- **D1 — C1 is closed by separating method rows from function rows, not by
  excepting one key.** Round 3's paste-ready fix writes
  `target != "zipfile.Path.open"` into the top-of-`judge` test. That closes the
  member and leaves the class open: the next method row added to `OPENERS`
  reopens it one name later, which is the failure §12 records (one work item
  closed a single class three times, one name apart). So the `.open` method
  positions move out of the table the top of `judge` reads. The emitted kinds
  (`zipfile.Path.open()`, `<expr>.open()`) do not change, because the cases
  pin them. Alternatives are in `plan.md`.
- **D2 — the bare-name branch of `owner` goes, rather than narrowing to `os`
  and `webbrowser`.** K2 says what the walk cannot prove counts as unnamed,
  and a parameter named `os` is not proven to be the module. Round 2's
  reviewer judged the behaviour that branch existed to prevent (`def f(os):
  os.open(p, 0)` reported) *acceptable for a walk that has no types* and asked
  only that the sentence match (round-2 report, ⬜ 2). The fix pass restored
  the branch anyway, wider than asked, and that restoration is 🟡 2. Removing
  it leaves one rule with no spelling list. The cost, stated: the `NAMED` case
  `os.open on a name no import binds` becomes a reported shape, with the kind
  `<expr>.open(), mode not a literal`, and leaves `NAMED` for a case that
  asserts it is reported; nothing in the tree has that shape (§*Grounding*, last row). If the repository case meets
  one when the build runs it, the build keeps the two-name branch from round
  3's paste-ready fix instead and records the divergence (questions.md M1).
- **D3 — ⬜ 3 is a sentence, not a trace.** See §*Scope*, Out. The over-report
  has a repair the failure message already gives.
- **D4 — import shadowing in a narrower scope is stated, not traced.** See
  §*Scope*, Out. It is the one under-report left in C2's neighbourhood, and
  the docstring's *What no row can hold* is where the module already keeps
  that kind of limit.
- **D5 — #741's `spec.md` is not edited.** The issue's second box asks that
  *`spec.md`* name exactly the receivers the code excuses. The tree answers
  which: a released work item's records are records of a moment, and `settle`
  folds the newest work item's sentence where two disagree. This spec's K1
  row above is that sentence. Round 3's ⬜ 5 was a correction to #741's branch
  while it was live; that branch has shipped.
- **D6 — the paste-ready fixes are re-derived, and each case is seen red
  before it is committed.** A paste-ready fix carried a defect three times in
  an earlier run of this repository. Round 3's diffs were run green in a
  scratch clone, which shows they pass and not that they are right: its 🟡 1
  diff fixes the member and not the class (D1), and its 🟡 2 diff keeps a
  spelling list the K2 rule refuses (D2). The build reads each diff, derives
  its own, and shows every new case red against the unfixed code before
  committing it.

## User scenarios & acceptance *(mandatory)*

Every case lives in `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`
and is seen red before it is committed (contract §15). "Red" is stated per row.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 — a class-called `zipfile.Path.open` in the locale is reported | Given `import zipfile` and `zipfile.Path.open(q, "r")`, and the same through `from zipfile import Path` and `import zipfile as z`, when the walk runs, then each is reported with the kind `zipfile.Path.open()` | Three `UNNAMED` cases. Red: each returns no site at the base `94d7b2e0` (round 3 executed this at `42db9639`; the module is byte-identical at the base) |
| S2 — the existing `NAMED` case for the class-called form passes for the right reason | Given `zipfile.Path.open(q, "r", "utf-8")`, when the walk runs, then it is not reported because `"utf-8"` sits in the shifted encoding slot | Red: after the fix, deleting `"utf-8"` from that case's source makes it fail (`bin/mutation-check` on the case's source text). At the base the same deletion still passes, which is the defect |
| S3 — no method row is reachable by dotted name | Given the table the top of `judge` matches openers in, when every key is read, then none is `<class>.<method>` for a class in `UNBOUND_RECEIVERS` | One test over the table, so a method row added later fails it by name. Red: against the base's `OPENERS` it names `zipfile.Path.open` |
| S4 — a local named after a module has its `.open()` judged | Given `wave = make(p)` then `wave.open()`, and a parameter `def f(tarfile): return tarfile.open()`, and a loop `for shelve in d: shelve.open("w")`, when the walk runs, then each is reported with an `<expr>.open()` kind | `UNNAMED` (module level) or a test reading the function's qualname. Red: each returns no site at the base |
| S5 — an unimported `os` is no longer excused | Given `def f(os): return os.open(p, 0)`, when the walk runs, then it is reported as `<expr>.open(), mode not a literal` | The `NAMED` case leaves `NAMED` for a case asserting the site. `UNPROVEN` and `UNNAMED` assert the qualname `<module>`, and this shape sits in `f`, so the case either reads the qualname or is a test of its own. Red: at the base it is not reported |
| S6 — every module C3 adds is excused when imported | Given `import dbm.gnu` then `dbm.gnu.open(p)`, and the same for `dbm.ndbm`, `dbm.sqlite3`, `aifc`, `sunau`, `tokenize`, `posix`, `nt`, when the walk runs, then none is reported | `NAMED` cases. Red: each is reported at the base as `<expr>.open(), mode not a literal` |
| S7 — the same spelling with no import is still judged | Given `dbm.gnu.open(p)` with no import, when the walk runs, then it is reported | Follows from D2: an attribute chain whose head no import binds resolves to nothing. One `UNNAMED` case for a C3 name; red at the base only if the base excused it — if it is already reported at the base, it is a pin, not a regression case, and the handover says which |
| S8 — the docstrings say what the code does | Given the module docstring, `owner`'s docstring and the comment over `NOT_A_FILE_OPENER`, when read against the code, then the receivers they name are exactly the ones excused, the ⬜ 3 sentence is present, and D4's shape is in *What no row can hold* | Read by the review. No test pins docstring prose in this module, and none is added: it is not text a person reads at a red leg |
| S9 — the tree stays green | Given the whole tree, when the repository case runs, then it passes with no `ALLOWED` row added | `bin/test` on the module (narrow). The full suite is the sealer's |

## Data & interfaces

No interface changes. The module's tables, `judge` and `owner` change shape;
the kinds the walk emits do not. Ledger: E1 in `seal/releases/0.18.1.md`
cites `judge`, which moves, so its re-read is a `Re-read ·` row in this work
item's fragment (`evidence-check --reverify --into`). The new row cites
`owner`, `judge` and `NOT_A_FILE_OPENER` and claims C1, C2 and C3 as stated
above.

## Open questions → questions.md

None needs a person. Two measurements and one row for the work are in
`questions.md`, each with the default the build uses.

Framed 2026-10-04 by framer, before the build.
