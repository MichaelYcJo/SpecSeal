# 1788398967-local-modes-records-never-leave-the-clone — review round 4

<!-- The verifying round for round 3's fixes (target: the diff ca96676..d420708).
It is the first round on this work item with no 🔴 — nothing it found leaves
the root. Seven 🟡, closed at 3f2a7b1, and round 5 verifies them. Written by
the review orchestrator, which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | d420708 (the fix diff from ca96676); 4293c2e is round 3's record and carries no code |
| PR | none yet |
| Broad gate | not yet — round 5 verifies these fixes, and the one broad run comes after it |
| Fixes checked by | round-5 |
| Contract changes | `write_zip` → `export`; `blocked_path` → `import_`; `unsafe` → `import_`; `import_` → `main` |
| New units | `fifo_or_skip` in `conftest.py`, and five test cases |
| Needs a fix | yes — 🟡 1 (the refusal removes what it refused), 🟡 2 (`isfile` is not the question `makedirs` answers), 🟡 3 (the write loop has no guard), 🟡 4 (the format message is spoken over by the name message), 🟡 5 (a clash inside the zip gets the root's remedy), 🟡 6 (the Korean README names one side of two), 🟡 7 (a line of output is in no acceptance criterion) |

- [x] Pass — no 🔴. The seven 🟡 are closed at 3f2a7b1 and round 5 checks them.

**Four rounds, four escapes, and this is the first round that found none.**
Rounds 1, 2 and 3 each ended with a record outside the root: the member's own
name, the name a collision falls back to, the name the export writes through.
Nothing this round found leaves the root. The heaviest of the seven is a
refusal that removes the file it refused — which is a defect, and is not the
class the three before it were.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r3 🔴 1 | the `.partial` escape | `skills/implement/scripts/seal.py#write_zip` | answered — reproduced; and this round's 🟡 1 is what that fix added | reviewer executed it: exit 1, nothing outside the clone, no zip. The reviewer also compared the new file-object path against the old path-based one — byte-identical zips (733 bytes), mode `0o644`, no `.partial` residue, and no leaked descriptor across fifty `FileExistsError` runs |
| r3 🟡 2 | `unused` kept `exists` | `skills/implement/scripts/seal.py#unused` | answered — reproduced | reviewer executed a second export the same day: it lands on `-2` |
| r3 🟡 3 | `makedirs` mid-write | `skills/implement/scripts/seal.py#blocked_path` | answered for a regular file; this round's 🟡 2 is the rest of the class | reviewer executed both sides of the clash: exit 1, root unchanged |
| r3 🟡 4 | a corrupt manifest | `skills/implement/scripts/seal.py#import_` | answered — reproduced | reviewer corrupted the manifest's data: a line of the command's own, exit 1 |
| r3 🟡 5 | encrypted and unknown methods | `skills/implement/scripts/seal.py#import_` | answered — reproduced, and with a real encrypted member rather than a simulated one | reviewer built one with `zip -P` and one with method 99: both exit 1 with the command's own line |
| r3 🟡 6 | the 400 MB manifest | `skills/implement/scripts/seal.py#unsafe` | answered — reproduced | reviewer ran the same measurement that opened it: exit 1, root unchanged, no memory growth |
| r3 🟡 7 | the reorder had no case | `tests/…` | answered — reproduced | reviewer reverted the order: two cases redden |
| r3 🟡 8 | no count bound | `skills/implement/scripts/seal.py#import_` | answered — reproduced | reviewer sent 20,002 members: exit 1 in 0.04 s |
| r3 🟡 9 | a dropped record was silent | `skills/implement/scripts/seal.py#write_members` | answered — reproduced with a real race | reviewer turned the name `place` chose into a link between the choice and the write: the record is named, the other two land, the counts agree |
| r3 🟡 10 | three documented claims | `spec.md`, `README*`, the ledger | answered at the three coordinates; the same class reopens as this round's 🟡 6 and 🟡 7 | reviewer read each against what runs |
| 🟡 1 | `os.open` sat inside `write_zip`'s try, so `O_EXCL`'s refusal ran the cleanup that exists to remove a half-written archive — and removed a name this call did not create. A link, a file somebody left, and a concurrent export's `.partial` in flight, which loses that export the finished zip it was about to rename. Four documents say the export refuses and none says it removes. The two planted cases disagreed on this: one asserted the link survives, the other did not | `skills/implement/scripts/seal.py:347-363` | fixed at 3f2a7b1 — the open is outside the try | reviewer executed all three shapes; orchestrator reproduced the link and the file independently, before and after: gone, then still there. The missing assertion is added to the sibling case, and a case for the plain file is planted |
| 🟡 2 | `blocked_path` asked `os.path.isfile`, and `os.makedirs(exist_ok=True)` raises on *exists and is not a directory*. `isfile` is False for a FIFO, a socket and a device node, so all three walked past the check into the crash it was added to prevent | `skills/implement/scripts/seal.py:678` | fixed at 3f2a7b1 — `lexists and not isdir`, the condition `makedirs` itself checks | reviewer executed with a FIFO: one record on disk, the rest lost, a traceback. The planted case uses a `fifo_or_skip` helper written the way `symlink_or_skip` is — the call is attempted, nothing is inferred from the platform |
| 🟡 3 | the write loop catches nothing but `FileExistsError`. Every refusal in this command runs before the first byte and this is the one that cannot: a directory in the root that cannot be written into, or a full disk, left a partial copy and a traceback | `skills/implement/scripts/seal.py:915` | fixed at 3f2a7b1 — `except OSError`, with a message saying a second run finishes the copy | reviewer executed with a read-only directory: `PermissionError`, one record lost. The message is true because this command overwrites nothing |
| 🟡 4 | the reorder put the format check after the name checks, and a later format is exactly what moves the names those checks read. A zip declaring format 2 with its records under `records/` answered "is not under `seal/`" — a malformed zip, where the truth is a build too old. `spec.md` S20 promises the format message | `skills/implement/scripts/seal.py:829` against `:867` | fixed at 3f2a7b1 by moving the names below the manifest rather than by re-reading it: the manifest's size bound moved out of `unsafe` into `import_`, which is the only reason the size had to be known first | reviewer executed both zips. The reviewer offered a second path and called the choice the implementer's; this one adds no new read of the manifest |
| 🟡 5 | `blocked_path` catches the clash from both sides and the message assumed one. A clash inside the zip told a person to rename a file that is not on their machine | `skills/implement/scripts/seal.py:906-913` | fixed at 3f2a7b1 — two remedies, chosen by whether the path is actually there | reviewer executed it against an empty root. The two planted cases now each assert their own message |
| 🟡 6 | the English README says "a name has to be a directory for the zip and is a file"; the Korean says it is a file **in the root**. The zip-only clash has no description for a reader of the Korean alone, and S19e puts both sides in the criterion | `README.ko.md:468` against `README.md:471` | fixed at 3f2a7b1 | reviewer read both sentence by sentence; nothing else disagrees |
| 🟡 7 | `refused` prints a line no acceptance criterion, fail-direction row or README describes, and the ledger row carrying it is labelled S19d — whose Then clause is about a copy landing past a link | `spec.md:72`, `seal/ledger/…md:55` | fixed at 3f2a7b1 — S19g and S17d added, three fail-direction rows added, the ledger row relabelled | reviewer read. This is round 3's S17-for-S17b one row over |
| 🟢 8 | `blocked_path` re-stats a shared prefix per member: 93 ms against `linked_path`'s 71 ms at 19,000 members | — | pass — no action | reviewer measured; the count bound is 20,000 |
| 🟢 9 | `seal.py:108` said "Both limits" where there are three; `overview.md:47` said "either" of three | — | fixed at 3f2a7b1, one word each | reviewer read |

## The mutation caught a case that passed against its own defect

`test_a_zip_whose_format_moved_the_names_says_so` asserted `"format" in out`
against a fixture named `format-2.zip`. The message prints the path, so the
assertion held under the reverted order — an empty case, planted in the same
pass that found emptiness in someone else's.

It was found by running the mutation rather than by reading the case. The
fixture is renamed and the assertion is now `"reads format 1"`.

## Every unit this fix pass added was mutation-tested

| Reverted | Reddened |
|---|---|
| the open moved back inside the try | `test_a_link_at_the_partial_name_refuses_the_export`, `test_a_file_at_the_partial_name_survives_the_refusal` |
| `lexists and not isdir` back to `isfile` | `test_a_named_pipe_where_a_directory_goes_refuses_the_zip` |
| the write loop's `except OSError` | `test_a_directory_the_copy_cannot_write_into_stops_with_a_line_of_its_own` |
| the clash's two remedies collapsed to one | `test_a_member_under_a_member_refuses_the_zip` |
| the names moved back above the format | `test_a_zip_whose_format_moved_the_names_says_so` |

Each reddens its own case and no other.

## Executed probes

| What was run | Result |
|---|---|
| reviewer: nine zip shapes against the message each gets | nine exit 1, root unchanged; one wrong message — 🟡 4 |
| reviewer: `--allow-other-repo` | exit 0, imported |
| reviewer: a link, a file, and a concurrent export's `.partial` at the temporary name | exit 1 each, and **each name removed** — 🟡 1 |
| reviewer: the new zip against one written by the old path-based call | 733 bytes each, identical; mode `0o644` |
| reviewer: a second export the same day, `--output <dir>`, `--output <file>`, a mid-write failure, 50 refusals | `-2`; into the directory; the named file; no residue; descriptors 4 to 4 |
| reviewer: a FIFO where a directory goes | `FileExistsError`, one record on disk — 🟡 2 |
| reviewer: a read-only directory in the root | `PermissionError`, one record lost — 🟡 3 |
| reviewer: a clash inside the zip alone | exit 1, and the root's remedy printed — 🟡 5 |
| reviewer: `blocked_path` false positives — a real directory entry, `seal`, `seal/`, `seal/a/`, a directory at a member's own name | none |
| reviewer: `blocked_path` cost at 19,000 members sharing a prefix | 93 ms against `linked_path`'s 71 ms |
| reviewer: a real race on the name `place` chose | the record named, the rest landed, counts agree |
| reviewer: an encrypted member built with `zip -P`; method 99 across three zip layouts | exit 1 with the command's own line; the patch hits the same count of signatures every time |
| reviewer: the eight units d420708 added, one at a time | eight redden their own case — round 3's table reproduced |
| orchestrator: the link and the file at `.partial`, before and after | removed; then left in place |
| orchestrator: a format-2 zip with moved names, before and after the reorder | the name message; then the format message |
| orchestrator after the fixes: the three touched test files | 146 passed |
| orchestrator: five mutations, one per unit this pass added | each reddens its own case and no other |
| orchestrator: `evidence_check.py --strict .` | 404 ok · 0 drifted · 0 broken |
| orchestrator: `ruff check` and `ruff format --check` on the changed files | clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–3 | `#linked_path`, `#place`, `#write_members`, `#import_`'s order | the import's write path and its check order |
| rounds 3–4 | `#write_zip`, `#unused`, `#blocked_path` | the export's write path and the clash check, both changed twice |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A root that is itself a symbolic link | `overview.md` §Not verified | the repository owner |
| Whether 32 MB, 512 MB and 20,000 are the right numbers | `overview.md` §Not verified | the repository owner, at the first root that meets one |
| Whether the export accumulating unfolded work items should be signalled | issue #101, after 0.5.0 | the repository owner |
| `evidence_check.py` drops a row with a non-hex hash silently | issue #97 | the repository owner |
| The reminder reading `1 work items changed` at N=1 | `questions.md` Q1, and the pull request body | the repository owner |
| A handoff fact from the orchestrator carries no verification label | issue #89, on 0.6.0 | the repository owner |
