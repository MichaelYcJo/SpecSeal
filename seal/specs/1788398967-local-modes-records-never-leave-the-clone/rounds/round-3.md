# 1788398967-local-modes-records-never-leave-the-clone — review round 3

<!-- The verifying round for round 2's fixes (target: the diff ee97c8c..ca96676).
It closed four of six, found one that had not closed for the case that opened
it, and opened a 🔴 on the export — the half neither earlier round had read.
The bound stays five while a 🔴 is open, and round 4 verifies these fixes.
Written by the review orchestrator, which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | ca96676 (the fix diff from ee97c8c); 1f908fb is round 2's record and carries no code |
| PR | none yet |
| Broad gate | not yet — a 🔴 was open |
| Fixes checked by | round-4 |
| Contract changes | `write_zip` → `export`; `unused` → `export`; `unsafe` → `import_`; `blocked_path` → `import_`; `import_` → `main`; `write_members` → `import_`, `tests/test_the_records_can_be_carried_out_and_in.py`; `read_manifest`'s docstring → none, prose only |
| New units | `blocked_path`, `MEMBER_COUNT_LIMIT`, the `refused` list, and nine test cases |
| Needs a fix | yes — 🔴 1 (`seal export` writes every record outside the clone through a link at `<stem>.zip.partial`, exit 0), 🟡 2 (`unused` kept `exists`), 🟡 3 (a name the zip needs as a directory and the root holds as a file crashes mid-write), 🟡 4 and 🟡 5 (a corrupt manifest, an encrypted member and an unknown compression method each reach the console as a traceback), 🟡 6 (round 2's 🟡 2 did not close for the case it measured), 🟡 7 (the reorder is covered by no case), 🟡 8 (neither bound counts members), 🟡 9 (a record the write turns down is dropped in silence), 🟡 10 (three documented claims the code does not support) |

- [ ] Pass

The escape has now been closed three times: the record's own name, the name a
collision falls back to, and the name the export writes through. Each fix was
aimed at the coordinate the finding named. The class — *every path this
command writes to* — is what round 3's prompt handed the reviewer, and it is
what found the third one.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r2 🔴 1 | the `.incoming` fallback link | `skills/implement/scripts/seal.py#place` | answered — reproduced | reviewer executed the escape at ca96676: exit 0, the copy at `ledger.incoming-2.md` inside the root, nothing outside. Both layers pin — reverting `lexists` reddens the fallback case, reverting `O_EXCL` reddens the write pin |
| r2 🟡 2 | the limits after `read_manifest` | `skills/implement/scripts/seal.py#import_` | **did not close** — this round's 🟡 6, fixed at d420708 | reviewer executed the same 400 MB manifest round 2 measured: 419,430,384 declared is under `ARCHIVE_LIMIT` 536,870,912, and `unsafe` exempted the manifest from `MEMBER_LIMIT`, so it imported at **exit 0** having grown 422 MB. The reorder bounded a 4 GB manifest and left the measured one alone |
| r2 🟡 3 | `ARCHIVE_LIMIT` uncovered | `tests/test_the_records_can_be_carried_out_and_in.py` | answered — reproduced | reviewer removed the check: exactly one case reddens |
| r2 🟡 4 | a bad CRC met mid-write | `skills/implement/scripts/seal.py#import_` | answered for a record's checksum; the manifest's is this round's 🟡 4 | reviewer removed `testzip`: the corrupt-member case reddens. Then flipped a byte in the manifest's data and got `BadZipFile` out of `read_manifest`, whose docstring says it never raises |
| r2 🟡 5 | the S8 label | `seal/ledger/1788398967-…md` | answered — and the same defect one row down is this round's 🟡 10 | reviewer read both clauses |
| r2 🟡 6 | the archive total in no README | `README.md`, `README.ko.md`, `spec.md` | answered for that refusal; the 🔴's own behaviour is this round's 🟡 10 | reviewer read all three against what executes |
| 🔴 1 | `write_zip` builds `<path>.partial` and hands the string to `zipfile.ZipFile(..., "w")`, which opens with a plain `open()` and follows a link. The name is fully predictable — `seal-<repo>-<date>.zip.partial`, beside the clone, where the default export writes. A broken link there put the manifest and both records outside the clone at exit 0, printing `wrote <path>` for what was the link. `--output` takes the same path | `skills/implement/scripts/seal.py:328-330` | fixed at d420708 — `O_EXCL`, the flag the import already writes with | reviewer executed it; orchestrator reproduced it independently, clean, then with the fix: exit 1 naming the `.partial` name, nothing outside. The planted case reddens when the flag is reverted. The reviewer also checked the export cannot *read* outside the root — `root_files` excludes link files, prunes linked directories, and `os.walk` does not follow links |
| 🟡 2 | `unused` kept `exists` where `place` moved to `lexists`, and its docstring claimed both went through it — the sentence that would have sent the fix's author here describes a pairing that does not exist. A broken link at the zip's name read as free and `os.replace` removed it | `skills/implement/scripts/seal.py:304`, `:311` | fixed at d420708 — `lexists`, and the docstring says which chain is whose and why the wrong sentence cost a fix | reviewer executed it. The case asserts the link survives and the zip takes the next name |
| 🟡 3 | `os.makedirs(exist_ok=True)` raises `FileExistsError` when the name exists and is not a directory, and it sits outside the try the corrupt-member fix added. A zip holding `seal/a` and `seal/a/b.md` left two records on disk, lost the one after them, and printed a traceback. The root's own contents raise it too, so a check over the zip's names alone is not enough | `skills/implement/scripts/seal.py:865` | fixed at d420708 — `blocked_path`, at the altitude of `linked_path` | reviewer executed both sides; orchestrator planted a case for each, and reverting the check reddens both |
| 🟡 4 | `read_manifest`'s docstring opens "Never raises for a bad archive" and catches three types; `archive.read` also raises `BadZipFile` on a bad checksum, and `testzip` runs twenty-five lines later | `skills/implement/scripts/seal.py:624` against `:778` | fixed at d420708 by the reorder, and the docstring now says what it does and does not catch | reviewer executed it: traceback, root empty |
| 🟡 5 | `except zipfile.BadZipFile` around `testzip` is unreachable — CPython's `testzip` catches that type itself and returns the member's name. What leaves it is an encrypted member (`RuntimeError`) and an unknown compression method (`NotImplementedError`), both tracebacks | `skills/implement/scripts/seal.py:778-780` | fixed at d420708 — all three named, `BadZipFile` kept as the guard that would still be right if `testzip` stopped swallowing it | reviewer read `inspect.getsource(zipfile.ZipFile.testzip)` on 3.13.9 and executed both shapes |
| 🟡 6 | round 2's 🟡 2 did not close for the case round 2 measured, and both the comment and the ledger row said it had | `skills/implement/scripts/seal.py:740-744` | fixed at d420708 — the manifest is bounded like every other member, once `unsafe` runs before `read_manifest` | reviewer executed the 400 MB manifest at ca96676: exit 0, 422 MB. Orchestrator's case reddens when the manifest's size bound is removed |
| 🟡 7 | the reorder is the one unit in ca96676 no case covers — moving the sum back below `read_manifest` reddens nothing | `skills/implement/scripts/seal.py:744` | fixed at d420708 — two cases pin the order, one on the manifest's data and one on the compression method | reviewer ran eleven mutations, one at a time: ten redden exactly one case each, the reorder reddens nothing. Orchestrator reproduced with the new cases in place: reverting the order reddens both |
| 🟡 8 | both bounds count bytes and neither counts members. A member declaring zero bytes passes the member bound and adds nothing to the total: a 31.5 MB zip of 300,000 empty members imported at exit 0, writing 300,002 files in 34.5 s | `skills/implement/scripts/seal.py:110-111` | fixed at d420708 — `MEMBER_COUNT_LIMIT`, 20,000 | reviewer executed it. Orchestrator's case is one member over the bound, and reddens when the check is disabled |
| 🟡 9 | a record `O_EXCL` turns down is skipped in silence, and the report reads `0 files added` — which a person reads as an empty zip. The round-2 pin asserted the silence as correct | `skills/implement/scripts/seal.py:875` | fixed at d420708 — named in the report, and the pin now asserts the name comes back | reviewer read. Reverting the report reddens the pin |
| 🟡 10 | three claims the fix commit added that the code does not support: the ledger's "both bounds are read before the manifest" (only the total was), its `S17` label where the clause is `S17b`, and the fail-direction table plus both READMEs describing a link in the destination as refused where S19d says the copy lands past it | `seal/ledger/…md:52-53`, `spec.md:177`, `README.md`, `README.ko.md` | fixed at d420708 | reviewer read each against what executes. The third is round 2's 🟡 6 one row over — the commit added rows for the total and the checksum and none for its own 🔴's behaviour |
| 🟢 11 | `overview.md` records 51 cases where the file collects 66 | `overview.md:19-20` | pass — no action | reviewer read: the rounds' records carry the current number, which is where a reader looks |
| 🟢 12 | every file under a work item is read twice per export | — | pass — no action | reviewer read: the single-walk invariant is worth more than the second read |

## Every unit this fix pass added was mutation-tested

Round 2 added `O_EXCL` and found it pinned by nothing. This pass ran the check
on itself before handing over: eight mutations, one at a time.

| Reverted | Reddened |
|---|---|
| the export's `O_EXCL` | `test_a_link_at_the_partial_name_refuses_the_export` |
| `unused`'s `lexists` | `test_a_broken_link_at_the_zips_own_name_is_not_a_free_name` |
| `blocked_path` | `test_a_member_under_a_member_refuses_the_zip`, `test_a_file_the_root_already_holds_blocks_a_member_under_it` |
| the manifest's size bound | `test_a_manifest_larger_than_a_record_refuses_the_zip` |
| `MEMBER_COUNT_LIMIT` | `test_a_zip_of_more_members_than_a_root_holds_refuses_it` |
| the wider `except` | `test_a_member_this_build_cannot_decompress_refuses_the_zip` |
| the order (manifest read before the data) | `test_the_data_is_read_before_the_manifest_is`, and the compression-method case |
| naming what the write turned down | `test_the_write_itself_refuses_a_name_that_became_a_link` |

Each reddens its own case and no other.

## Executed probes

| What was run | Result |
|---|---|
| reviewer: round 2's 🔴 at ca96676 | exit 0, the copy inside the root, nothing outside — closed |
| reviewer: a broken link at `<stem>.zip.partial` | **the whole zip written outside the clone at exit 0** — 🔴 1 |
| reviewer: a broken link at `<stem>.zip` | silently replaced by `os.replace` — 🟡 2 |
| reviewer: whether the export can read outside the root | it cannot — links excluded, linked directories pruned, `os.walk` does not follow |
| reviewer: `seal/a` with `seal/a/b.md` | `FileExistsError`, two records on disk, one lost — 🟡 3 |
| reviewer: a bad CRC on `manifest.json` | `BadZipFile` out of `read_manifest` — 🟡 4 |
| reviewer: an encrypted member; compression method 99 | `RuntimeError`; `NotImplementedError` — 🟡 5 |
| reviewer: the 400 MB manifest round 2 measured | exit 0, 422 MB grown, the record imported — 🟡 6 |
| reviewer: 300,000 zero-byte members | exit 0, 300,002 files, 34.5 s — 🟡 8 |
| reviewer: `inspect.getsource(zipfile.ZipFile.testzip)` on 3.13.9 | it catches `BadZipFile` itself |
| reviewer: eleven mutations against ca96676 | ten redden one case each; the reorder reddens nothing — 🟡 7 |
| reviewer: `evidence_check --strict` on this fragment | 33 ok · 0 drifted · 0 broken |
| orchestrator: the `.partial` escape, clean, before and after the fix | the zip outside the clone at exit 0; then exit 1 naming the `.partial` name, nothing outside |
| orchestrator after the fixes: the three touched test files | 142 passed |
| orchestrator: eight mutations, one per unit this pass added | each reddens its own case and no other |
| orchestrator: `evidence_check.py --strict .` | 400 ok · 0 drifted · 0 broken |
| orchestrator: `ruff check` and `ruff format --check` on the two changed Python files | clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–2 | `skills/implement/scripts/seal.py#linked_path`, `#place`, `#write_members` | the import's write path, now changed in every round |
| round 3 | `#write_zip`, `#unused`, `#blocked_path`, `#import_`'s order | the export's write path and the import's check order, both opened for the first time |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A root that is itself a symbolic link | `overview.md` §Not verified | the repository owner |
| Whether 32 MB, 512 MB and 20,000 are the right numbers | `overview.md` §Not verified | the repository owner, at the first root that meets one |
| `evidence_check.py` drops a row with a non-hex hash silently | issue #97, with the reviewer's note that it belongs earlier than 0.6.0 | the repository owner |
| The reminder reading `1 work items changed` at N=1 | `questions.md` Q1, and the pull request body | the repository owner |
| A handoff fact from the orchestrator carries no verification label | issue #89, on 0.6.0 | the repository owner |
