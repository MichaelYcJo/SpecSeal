# 1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local — overview

📋 implement applied
· spec:     this work item's `spec.md` (Grounding, Scope, The classes C1–C3, K1's `<expr>.open` row, Decisions D1–D6, scenarios S1–S9), `plan.md`, `questions.md`; #741's `rounds/round-3-report.md` (Findings, Paste-ready fixes); `seal/releases/0.18.1.md` row E1; `skills/evidence-check/SKILL.md` §*The records arm*
· evidence: `seal/ledger/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local.md` — `Re-read · E1` (written by `evidence-check --reverify --into`) and J1 (new)
· verified: executed — every new case at the base's walker, each unit's mutation, the 3.12–3.14 construction, the module (137 passed), ruff on the module, `bin/evidence-check .`; read — `dbm.gnu` and `nt` (see Not verified); the full suite is the sealer's

## Why this work exists

Round 3 of #741 left the encoding check passing one locale read and excusing
`.open()` on any local named after a module; after this work both are
reported, and eight standard-library `open`s that take no locale encoding stop
being reported.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which tables S3 reads | Spec S3: *the table the top of `judge` matches openers in*. Code: every table `judge` tests `target in`, collected from `judge`'s parsed source (five tables) | code | Contract §12 owes the class, and C1's own text says *the other tables the top of `judge` matches hold functions and constructors only*: a method row in any of them meets the same unshifted lookup. Reading them from `judge` keeps a table added there later inside the check |
| S3 checks its own filter | Spec silent. The test also runs its filter over a fixture holding the moved row and asserts it names exactly that row | code | After the fix no method row is left, so a weakened filter SURVIVED `bin/mutation-check`; with the fixture it is red (`phases/phase-1.md`) |
| Where S5 and S7 live | Spec S5: the case *either reads the qualname or is a test of its own*; S7: *one `UNNAMED` case for a C3 name*. Code: one table, `UNIMPORTED_RECEIVERS`, carrying a qualname, with S4's three, S5, and two S7 cases | code | S4 and S5 have shapes inside a function, which `UNNAMED` cannot assert. S7's second case, `tokenize.open(p)` with no import, is the one that goes red if the bare-name branch comes back beside the C3 set |
| What J1 cites | Spec *Data & interfaces*: *the new row cites `owner`, `judge` and `NOT_A_FILE_OPENER`*. J1 also cites `OPENERS`, `OPEN_METHODS`, the two new tests and the three case tables | code | C1's claim rests on `OPEN_METHODS` and the dotted-name test, and a coordinate missing from the row is a change nothing reports |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at this branch's head | the sealer, spawned by the orchestrator after the review rounds settle |
| ✅ That `dbm.gnu.open` and `nt.open` take no locale encoding. Neither is importable on the three local builds, so both are in the set by reading, as the frame had them | read by round 1 of review in the standard library's documentation for `dbm`, `os.open` and `ossaudiodev`, which also added `ossaudiodev` to the set by reading (`rounds/round-1-report.md`) |

## Not done

The two traces the spec put out of scope stay out, and the module docstring
now states each instead (D3, D4): a `zipfile.Path` reached by `/`,
`.joinpath` or a name is judged as `Path.open`, and a name an import binds
that a narrower scope rebinds is excused as the module. The private modules
the public `dbm` submodules re-export (_dbm, _gdbm) are not in the excused
set, so `.open` on one imported by its own name is reported; nothing in the
tree imports either.

## Fed back into the spec

none
