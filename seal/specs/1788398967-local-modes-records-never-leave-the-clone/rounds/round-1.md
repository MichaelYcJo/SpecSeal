# 1788398967-local-modes-records-never-leave-the-clone — review round 1

<!-- The first round on #81's implementation (target: 016dacd against
e9aa6e9). It opened a 🔴 that put a record outside the root at exit 0, so the
bound is five rather than three while it is open, and round 2 verifies the
fixes. Written by the review orchestrator, which did not implement this work
item — the smith did. -->

| Field | Value |
|---|---|
| Target SHA | 016dacd (the whole branch from e9aa6e9); 21 files, +2459/−21 |
| PR | none yet |
| Broad gate | not yet — a 🔴 was open |
| Fixes checked by | round-2 |
| Contract changes | `linked_directory` renamed `linked_path` → `import_`; `destination_root` → `import_`; `git` → `manifest_of`, `import_`; `unsafe` → `import_`; `import_` → `main` |
| New units | `MEMBER_LIMIT`, `ARCHIVE_LIMIT`, and four test cases |
| Needs a fix | yes — 🔴 1 (a symbolic link named for the record, broken, takes it outside the root at exit 0), 🟡 2 (both roots present is refused only with `--into`, against four documents), 🟡 3 (an unborn branch records `"HEAD"` as the SHA), 🟡 4 (the NUL check cannot fire), 🟡 5 (a member is read whole with no bound) |

- [ ] Pass

The premise this work was handed — that `extractall` is the classic
path-traversal sink — was measured false by the smith and measured false
again by the reviewer, on a third interpreter. The orchestrator's own facts
in a handoff carry no verification label today; that is recorded on issue #89.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `linked_path` walked `range(1, len(parts))`, which is every directory above a member and never the member itself. A destination link named `ledger/w1.md` whose target does not exist reads as absent to `os.path.exists`, so `place` calls the member ADDED and `open(target, "wb")` follows the link and writes outside the root. Exit 0, nothing printed. A link whose target exists is caught by the byte comparison and lands as `.incoming`, which is why only the broken one leaked. Three documents called the directory case the only way out | `skills/implement/scripts/seal.py:592` | fixed at ee97c8c | reviewer executed the escape in a clone; orchestrator reproduced it independently, clean, before and after the one-line change: a record outside the root at exit 0, then exit 1 with nothing written. The planted case reddens when the loop bound is reverted |
| 🟡 2 | the both-roots refusal sat inside `destination_root`'s `if into:` branch, so `seal import` with no flag fell through to the root in force and wrote into it. `spec.md` S11, `README.md`, `README.ko.md` and the changelog fragment all describe a refusal with no flag. The case covering S11 called the command with `--into local`, so the spelling those four documents describe never ran | `skills/implement/scripts/seal.py:657-676`, `spec.md:61` | fixed at ee97c8c — the code was made to match the four documents, and S11's case now runs all three spellings | orchestrator read the refusal's own reasoning against the flagless path: it names a dead root, and the flagless call writes into the root that is read, so the reason does not carry. The documents are the acceptance criteria and refusing writes nothing, which is the direction a stop belongs in. The case reddens when the refusal is put back inside the branch |
| 🟡 3 | `git` returned stdout without reading the exit code. `git rev-parse HEAD` on a branch with no commit exits 128 and prints `HEAD`, so the manifest recorded four letters as the export's SHA and the import printed them back as one. `spec.md:107` says the field is the SHA or empty | `skills/implement/scripts/seal.py:109-127` | fixed at ee97c8c | reviewer executed against an unborn branch, a repository with no remote, and a detached HEAD — the last two were already correct. Orchestrator's planted case reddens when the exit-code check is disabled |
| 🟡 4 | `unsafe` refuses a name holding a NUL, and `zipfile` cuts the name at the NUL before `unsafe` reads it, so the check cannot fire. The member arrives under a shortened name inside the root — the outcome the surrounding comment says the refusals exist to prevent | `skills/implement/scripts/seal.py:546-547` | fixed at ee97c8c by narrowing the claim rather than the code: the guard stays, and the comment says the sanitise happens first and what it costs | reviewer executed: `info.filename` and `info.orig_filename` are both `'seal/no'` for a member named `seal/no` NUL `t.md`. Nothing lands outside the root, so this is a claim wider than what runs rather than a defect |
| 🟡 5 | `write_members` reads each member whole and `unsafe` never looks at `info.file_size`. A 408 KB zip declaring 400 MB in one member wrote 419 MB and added as much to memory, in 0.2 s. The smith recorded this as a limit with the grounds that a record is markdown; the size is chosen by the machine that sent the zip, and both READMEs tell a person to accept one from another machine | `skills/implement/scripts/seal.py:784`, `overview.md:47` | fixed at ee97c8c — 32 MB a member, 512 MB an archive, both read before a byte is written. Whether those are the right numbers is now the open question in `overview.md` | reviewer executed the measurement; orchestrator's planted case reddens when the member check is disabled |
| ❓ 6 | a root that is itself a symbolic link puts everything outside, and the leaf fix does not reach it because the loop starts inside the root. `home_at` follows the link, so it reads as a valid root — which is also what a person who deliberately put the root elsewhere would want | `skills/implement/scripts/seal.py:592` | deferred — recorded in `overview.md` §Not verified as a question for the owner, not a pass | reviewer executed it and declined to grade it, which is the right call: the two readings differ on intent, not on behaviour |
| 🟢 7 | a member whose name holds a newline becomes a file, splitting the collision report's one line into two | `skills/implement/scripts/seal.py:548` | pass — no action | reviewer read: legal on POSIX and inside the root |
| 🟢 8 | with 1000 `.incoming` siblings taken, the message names `.` as the directory | `skills/implement/scripts/seal.py:376-378` | pass — no action | reviewer read; reaching it needs 1000 files of the same name |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `extractall` against four member shapes, CPython 3.14.4 | `..` and a leading `/` stripped, a link entry written as an ordinary file — the smith's measurement on 3.13.9 and 3.12.11 reproduced on a third interpreter |
| reviewer: export with all six session-state files planted beside the root | members are `manifest.json` and five under `seal/` — none of the six |
| reviewer: the manifest against no remote, a detached HEAD, and an unborn branch | correct, correct, and 🟡 3 |
| reviewer: import against a line-ending difference, a byte-identical file, and the same zip twice | `.incoming`, left alone, nothing written |
| reviewer: `--into shared`, `--into local` and neither, across local-only, shared-only and both | 🟡 2 |
| reviewer: nine member-name shapes, NFC and NFD, a newline, a NUL | all refused but the NUL, which is 🟡 4 |
| reviewer: shared-mode export, then running the `mv` it prints | exit 0, the mode switched, and a subsequent export wrote a zip |
| reviewer: the zip bomb | 408 KB declaring 400 MB wrote 419 MB, memory 447 to 867 MB, 0.2 s |
| reviewer: the three touched test files | 127 passed |
| orchestrator: the broken-link escape, clean, at the old loop bound and with the fix | exit 0 with a record outside the root, then exit 1 with nothing written |
| orchestrator after the fixes: the three touched test files | 130 passed |
| orchestrator: each fix reverted in turn against its planted case | four cases, four reds, each with its own message |
| orchestrator: `evidence_check.py --strict .` | 384 ok · 0 drifted · 0 broken |
| orchestrator: `ruff check` and `ruff format --check` on the two changed Python files | clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| — | none; this is the first round | — |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 6 — a root that is itself a symbolic link | `overview.md` §Not verified | the repository owner |
| Whether 32 MB and 512 MB are the right limits | `overview.md` §Not verified | the repository owner, at the first root that meets one |
| The reminder reading `1 work items changed` at N=1 | `questions.md` Q1, and the pull request body | the repository owner |
| A handoff fact from the orchestrator carries no verification label | issue #89, on 0.6.0 | the repository owner |
| `evidence_check.py` skips a row whose hash is not hex without counting or naming it | issue #97, on 0.6.0 | the repository owner |
