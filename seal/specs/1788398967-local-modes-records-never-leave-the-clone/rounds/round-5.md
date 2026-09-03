# 1788398967-local-modes-records-never-leave-the-clone — review round 5

<!-- The verifying round for round 4's fixes (target: the diff d420708..3f2a7b1),
and the cap. It found no 🔴 and nothing the diff had broken. Two of its seven
🟡 were graded must-not-ship and are closed at 7cc4fb3; the other five are
closed too, because each was a line. There is no round 6, so the broad gate
comes next. Written by the review orchestrator, which did not implement this
work item. -->

| Field | Value |
|---|---|
| Target SHA | 3f2a7b1 (the fix diff from d420708); 80e5d08 is round 4's record and carries no code |
| PR | none yet |
| Broad gate | due after this record — see the row below, filled in at the gate's commit |
| Fixes checked by | round-6 |
| Contract changes | `normalise_remote` → `import_`; `import_` → `main` |
| New units | none — three conditions, two comments, four test cases |
| Needs a fix | no |

- [ ] Pass

Five rounds, three escapes, and the curve is unambiguous. Rounds 1, 2 and 3
each ended with a record outside the root — the member's own name, the name a
collision falls back to, the name the export writes through. Round 4 found no
escape and three crashes. Round 5 found no escape, no crash the change had
caused, and one the change had walked past.

`Needs a fix: no` and the fixes still get a reader. The chain checker
refuses a `Pass` beside `Fixes checked by: nobody`, and it is right to: a run
cannot say it passed while the fixes that closed its findings were opened by
nobody. A round that opens nothing needing a fix does not consume the cap, so
round 6 reads 7cc4fb3 and this record names it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r4 🟡 1 | the refusal removed what it refused | `skills/implement/scripts/seal.py#write_zip` | answered — reproduced | reviewer executed a file, a broken link and a directory at the temporary name: exit 1 each, each still there. Descriptors 4 to 4 across fifty refusals, and a mid-write failure still removes the partial it created |
| r4 🟡 2 | `isfile` is not `makedirs`' question | `skills/implement/scripts/seal.py#blocked_path` | answered — reproduced | reviewer executed with a FIFO: exit 1, root unchanged |
| r4 🟡 3 | the write loop had no guard | `skills/implement/scripts/seal.py#import_` | answered — reproduced, and the message's promise tested | reviewer ran the read-only directory, then ran the import twice more: 2 added, then 0 added and 3 identical. A second run does finish the copy, and the collision report is right the second time |
| r4 🟡 4 | the format spoken over by the names | `skills/implement/scripts/seal.py#import_` | answered — reproduced, and the regression the reorder risked was checked | reviewer executed a bad member name with a good format: the name message still prints, both members named |
| r4 🟡 5 | the clash's one remedy | `skills/implement/scripts/seal.py#import_` | answered — reproduced. A clash on both sides needs two runs and gives two messages, which is ❓ 8 | reviewer executed each side |
| r4 🟡 6 | the Korean README named one side | `README.ko.md` | answered — reproduced | reviewer read both sentence by sentence |
| r4 🟡 7 | `refused` had no criterion | `spec.md`, the ledger | answered — reproduced | reviewer read S19g and S17d against what runs |
| 🟡 1 | the manifest is another machine's file and `read_manifest` validates the object and its `format` and nothing else. `head` without `exported_at` raised `KeyError` at the closing line — **after every record was written**, so the person sees a traceback and exit 1 for a copy that succeeded, and the command's two closing lines never print. `head` as a number or a bool raised `TypeError` the same way; `remote` as a list or a dict raised `AttributeError` before any write | `skills/implement/scripts/seal.py:987`, `:901` | fixed at 7cc4fb3 — three conditions, no new function: `normalise_remote` reads a non-string as "", and the closing line reads both fields for their type | reviewer executed eleven manifest shapes and found five tracebacks. Orchestrator reproduced four independently, before and after. Each guard reverted alone reddens its own case: the `exported_at` guard one case, the `head` guard the two parametrised head shapes, `normalise_remote` the two remote shapes |
| 🟡 2 | `unsafe` exempts `name.rstrip("/") == MANIFEST` and the size bound matched `info.filename == MANIFEST`, so `manifest.json/` passed both at any declared size. Nothing is lost today — `write_members` skips it and `ARCHIVE_LIMIT` still caps the zip — but it is a hole in a bound, and it is `unused` and `place` again: one question, two tests, and the fix visited one of them | `skills/implement/scripts/seal.py:598` against `:842` | fixed at 7cc4fb3 — the bound matches the same pair of spellings | reviewer executed it: 400 MB declared, exit 0. Orchestrator reproduced after correcting the fixture — `writestr` recomputes `file_size`, so the declared size goes into the central directory afterwards — and the planted case does the same |
| 🟡 3 | `import_`'s order comment describes an order the code no longer runs, and it is the sentence a future fixer reads to learn where a check belongs. Round 3's 🟡 2 was a docstring exactly like it | `skills/implement/scripts/seal.py:813-815` | fixed at 7cc4fb3 | reviewer read it against the code |
| 🟡 4 | both READMEs say the import refuses **writing nothing**, and the round before added a stop that writes. The outcome is in `spec.md` S17d, in the fail directions and in the changelog, and in neither README — which assert the opposite as a general rule | `README.md:466`, `README.ko.md:463` | fixed at 7cc4fb3 — a paragraph in each, saying what happens and that a second run finishes the copy | reviewer read. This is the same class as round 2's 🟡 6, round 3's 🟡 10 and round 4's 🟡 7, and the sharpest of the four: the others omitted, this one contradicted |
| 🟡 5 | the format refusal — the whole subject of the commit under review — is described in no fail-direction row and neither README. That commit added three rows and none of them is this one | `spec.md:80`, both READMEs | fixed at 7cc4fb3 | reviewer read |
| 🟡 6 | the ledger row saying every bound is read before the manifest is decoded: the member bound lives in `unsafe`, which the same commit moved below `read_manifest`. The row's anchor was re-verified by that commit, so the coordinate was re-read and the claim above it was not | `seal/ledger/…md:61` | fixed at 7cc4fb3 | reviewer read. Round 3's 🟡 10 was this same row, wrong a first time |
| 🟡 7 | round 4's record says a comment saying "Both limits" was fixed "one word each"; `overview.md` was changed and the line in `seal.py` was not | `skills/implement/scripts/seal.py:109` | fixed at 7cc4fb3 | reviewer read the commit against the record |
| ❓ 8 | a clash present on both sides needs two runs and gives two different messages — correct at each step, confusing across them. Naming both in one message is a design call | `skills/implement/scripts/seal.py#import_` | deferred — the repository owner | reviewer executed the sequence |
| ❓ 9 | `test_a_directory_the_copy_cannot_write_into_stops_with_a_line_of_its_own` skips where `os.access` says the directory is writable, which is true for root. It runs here and on all three GitHub runners | `tests/…` | deferred — the repository owner, if this suite is ever meant to run as root | reviewer read and executed |

## What the cap bought, and what it did not

Round 5 found nothing the diff under review had broken. Its two must-fix
findings are an older defect no round had opened, and a bound's second
spelling. Its other five are documents.

Four of those five are one class — **a user-visible outcome exists and no
document a person reads describes it** — and that class has now appeared in
rounds 2, 3, 4 and 5. Once on the same ledger row twice. That is not something
a sixth round would end; it is something a checklist on the fix pass would,
and the reviewer said so. It goes to issue #89 as a candidate for the
handoff protocol: *a fix that adds an outcome a person can see adds a line to
both READMEs and a fail-direction row, in the same commit.*

## Executed probes

| What was run | Result |
|---|---|
| reviewer: 31 zip shapes through the new check order | 31 correct verdicts, 0 tracebacks, 0 unintended writes |
| reviewer: a bad member name with a good format, four spellings | the name message, both members named — the reorder's regression risk is not real |
| reviewer: the read-only directory, then two more runs | stopped part-way; 2 added; 0 added and 3 identical |
| reviewer: a collision plus the read-only directory, two runs | stopped part-way, then the collision reported correctly |
| reviewer: 11 manifest field shapes on the success path | five tracebacks — 🟡 1 |
| reviewer: a file, a broken link and a directory at the temporary name | exit 1 each, each left in place |
| reviewer: `--output` into a read-only directory, a missing parent, a 300-character name | three lines of the command's own |
| reviewer: descriptors across 50 refusals; a mid-write export failure | 4 to 4; no residue |
| reviewer: `manifest.json/` declaring 400 MB | **exit 0, imported** — 🟡 2 |
| reviewer: the reorder's cost at the bounds' maximum | 0.08 s against 0.04 s — not a finding |
| reviewer: 7 mutations, one per unit the round-4 pass changed | each reddens its own case |
| orchestrator: four manifest shapes, before and after | two traceback-after-writing, one traceback-before-writing, one exit 0 at 400 MB; then all four correct |
| orchestrator after the fixes: the three touched test files | 152 passed |
| orchestrator: four mutations, one per condition this pass changed | each reddens its own case and no other |
| orchestrator: `evidence_check.py --strict .` | 408 ok · 0 drifted · 0 broken |
| orchestrator: `ruff check` and `ruff format --check` over `skills/` and `tests/` | clean, 62 files |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–5 | `#place`, `#write_members`, `#import_`, `#write_zip`, `#unused`, `#blocked_path`, `#unsafe` | seven units, every one of them changed in at least two rounds |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 8 — a clash on both sides takes two runs | this record | the repository owner |
| ❓ 9 — the read-only-directory case skips as root | this record | the repository owner |
| A root that is itself a symbolic link | `overview.md` §Not verified | the repository owner |
| Whether 32 MB, 512 MB and 20,000 are the right numbers | `overview.md` §Not verified | the repository owner, at the first root that meets one |
| The export accumulating unfolded work items | issue #101, after 0.5.0 | the repository owner |
| `evidence_check.py` drops a row with a non-hex hash silently | issue #97 | the repository owner |
| The reminder reading `1 work items changed` at N=1 | `questions.md` Q1, and the pull request body | the repository owner |
| A handoff fact from the orchestrator carries no verification label; a fix that adds a visible outcome should document it in the same commit | issue #89, on 0.6.0 | the repository owner |
