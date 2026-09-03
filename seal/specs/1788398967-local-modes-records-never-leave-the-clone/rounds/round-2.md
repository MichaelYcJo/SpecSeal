# 1788398967-local-modes-records-never-leave-the-clone — review round 2

<!-- The verifying round for round 1's fixes (target: the diff 016dacd..ee97c8c).
It closed all five and opened six, one of them a 🔴 that put a record outside
the root at exit 0 — the same escape round 1 closed, one candidate name over.
So the bound stays five while it is open, and round 3 verifies these fixes.
Written by the review orchestrator, which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | ee97c8c (the fix diff from 016dacd); 2eb3a56 is round 1's record and carries no code |
| PR | none yet |
| Broad gate | not yet — a 🔴 was open |
| Fixes checked by | round-3 |
| Contract changes | `place` reads candidates with `lexists` rather than `exists`. `write_members` opens with `O_EXCL` and counts after the write. `import_` sums the archive total before reading the manifest, and runs `testzip` before writing any record. `destination_root`'s docstring no longer claims it creates the root |
| New units | three test cases from the reviewer's report, one written to pin `O_EXCL` on its own |
| Needs a fix | yes — 🔴 1 (a record still leaves the root through the `.incoming` fallback name), 🟡 2 (both limits read after the manifest is whole in memory), 🟡 3 (`ARCHIVE_LIMIT` reddens no case), 🟡 4 (a corrupt member writes the records before it, then crashes), 🟡 5 (the ledger files the unborn-branch fact under the collision clause), 🟡 6 (the archive-total refusal is in no README and no fail-direction row) |

- [ ] Pass

Round 1's five closures were each re-derived rather than taken. All five hold.
🔴 1 below is not one of them reopening — it is the neighbouring name the
round-1 fix did not reach, which is the recursive shape issue #97 is about,
caught this time by the round rather than by a release.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r1 🔴 1 | the leaf link | `skills/implement/scripts/seal.py#linked_path` | answered — reproduced, and reverting the loop bound reproduces the escape | reviewer executed five link shapes: a broken leaf, a leaf whose target exists, a leaf to a directory, a deep leaf and a mid-directory link. All exit 1 with nothing outside the root |
| r1 🟡 2 | both roots refused however asked | `skills/implement/scripts/seal.py#destination_root` | answered — reproduced, and the direction judged right | reviewer executed all three spellings, then put the check back inside `if into:` and watched the flagless call write into the shared root at exit 0 |
| r1 🟡 3 | the unborn branch's SHA | `skills/implement/scripts/seal.py#git` | answered — reproduced, and no caller regressed | reviewer read both call sites and executed each against a repository with no remote, one with a remote, and an unborn branch: only `rev-parse HEAD` changed, `"HEAD"` to `""` |
| r1 🟡 4 | the NUL claim narrowed | `skills/implement/scripts/seal.py#unsafe` | answered — and the new wording is true | reviewer executed with the guard deleted entirely: no case reddens, which is what "inert" means. Keeping it is right — it is the line that would still be correct if `zipfile` stopped truncating |
| r1 🟡 5 | the member limit | `skills/implement/scripts/seal.py#unsafe` | answered for the member, and this round's 🟡 2 and 🟡 3 are its edges | reviewer executed a lying central directory (declared 100 against 64 MB of data returned 100 bytes) and a member declaring more than it holds (no bleed): the declared size is a sound bound on what is read |
| 🔴 1 | `place` does not write to the member's name when that name is taken — it falls back to `<stem>.incoming<ext>` and then numbered siblings, and `linked_path` never sees a fallback. A broken link there reads as absent to `os.path.exists`, so `place` returns it as a collision and `open()` follows it out of the root. Exit 0, printed as an ordinary collision. The sender chooses whether the collision happens, by sending bytes that differ. `spec.md:71` S19c already claimed "any path a member would take" | `skills/implement/scripts/seal.py:668` | fixed at ca96676 | reviewer executed the escape at ee97c8c; orchestrator reproduced it independently, clean, and then with the fix: the copy lands at `ledger.incoming-2.md` inside the root and nothing appears outside. Two layers — `lexists` on every candidate, and `O_EXCL` on the write so a name that becomes a link after the check is refused too |
| 🟡 2 | both limits are read after `read_manifest`, and `unsafe` exempts the manifest from the member limit, so a 400 MB `manifest.json` is read and decoded whole before anything refuses it. The comment claimed both are read before a byte is written, which is true of the disk and not of memory | `skills/implement/scripts/seal.py:732` against `:748` | fixed at ca96676 — the total is summed first | reviewer executed it: exit 1 with 400 MB of memory grown. Orchestrator moved the sum above the manifest read |
| 🟡 3 | `ARCHIVE_LIMIT` is the one unit round 1 added that no case covers — deleting the check reddens nothing. `spec.md` S19b is written as the archive total and its case declares 40 MB in one member | `skills/implement/scripts/seal.py:111` | fixed at ca96676 | reviewer executed all six mutations one at a time: four fixes each redden exactly one case, `ARCHIVE_LIMIT` and the NUL guard redden none. The planted case is 20 members of 31 MB, refused at 650117147 bytes |
| 🟡 4 | `archive.read` raises `BadZipFile` on a bad CRC and `import_` catches it only around the open. A corrupt second record left the first on disk and printed a traceback with no line of this command's own — a partial import, against `seal.py:527-530`'s own stance and `spec.md` S17. A zip truncated on disk was already refused | `skills/implement/scripts/seal.py:828` | fixed at ca96676 — `testzip` before the first write | reviewer executed it. Orchestrator's planted case corrupts the second of two records and reddens when `testzip` is disabled. The archive bound above it is what makes reading every member affordable |
| 🟡 5 | the ledger's unborn-branch row opens `S8`, and S8 is the collision clause. The fact belongs to S4, through the manifest table's `head` field | `seal/ledger/1788398967-…md:52` | fixed at ca96676 | reviewer read both clauses. The row's content and anchors were correct; only the label pointed at the wrong criterion |
| 🟡 6 | the archive-total refusal lived in the code and in one changelog line, and in neither README nor the fail-direction table. A person meeting it reads a message no document they were pointed at describes | `README.md:468`, `README.ko.md:464`, `spec.md:175` | fixed at ca96676 — both READMEs and the table carry it, and the checksum refusal beside it. S19d and S17b added | orchestrator read all three against what executes |
| 🟢 7 | `destination_root`'s docstring opened "Creates it when the mode is named" and it creates nothing | `skills/implement/scripts/seal.py:679` | fixed at ca96676 — one line, since the same commit rewrote the docstring below it | reviewer read |
| ❓ 8 | `evidence_check.py` drops a row whose hash is not hexadecimal without counting or naming it, so the total reads healthier for holding a broken row than for holding none. The reviewer's judgment is that this is worth more than its deferral gives it | `skills/evidence-check/scripts/evidence_check.py` | deferred — issue #97, where round 1 put it. The reviewer's severity note is carried to the pull request body | reviewer executed all three shapes: non-hex is silent at exit 0, a wrong hex hash is `1 drifted` at exit 2, a gone symbol is exit 2 |

## The unit the fix added that nothing covered

`O_EXCL` reddened no case when reverted, because `lexists` already turns the
link down before the write is reached. That is the exact shape of 🟡 3, in the
commit that answers 🟡 3.

It was pinned rather than dropped: `test_the_write_itself_refuses_a_name_that_became_a_link`
hands `write_members` the name a raced check would have handed it, and asserts
nothing is written, nothing lands outside, and nothing is counted. Reverting
`O_EXCL` reddens it; so does reverting the counting order.

The layer is worth keeping because the check it backs is a check — the name is
free when `place` chooses it and can be a link by the time it is opened.

## Executed probes

| What was run | Result |
|---|---|
| reviewer: round 1's 🔴 at ee97c8c, and with the loop bound reverted | exit 1 nothing written; then exit 0 with the record outside |
| reviewer: a broken link at the `.incoming` sibling, at ee97c8c | **exit 0, the record outside the root** — 🔴 1 |
| reviewer: four more leaf-link shapes | all exit 1, nothing outside |
| reviewer: both roots, three spellings, before and after putting the check back | three refusals; then three writes |
| reviewer: `git()` against an unborn branch, no remote, and a remote, before and after | only `rev-parse HEAD` changed |
| reviewer: a 400 MB `manifest.json` | exit 1, memory grew 400 MB — 🟡 2 |
| reviewer: 20 members of 31 MB | exit 1, root unchanged |
| reviewer: a central directory declaring 100 against 64 MB of data | `read()` returned 100 bytes |
| reviewer: a wrong CRC on the second of two records | the first written, `BadZipFile` traceback, no line printed — 🟡 4 |
| reviewer: the same zip truncated on disk | exit 1, root untouched |
| reviewer: members named `seal` and `seal/` | exit 0, nothing written |
| reviewer: a root that is itself a symbolic link | exit 0, record outside — ❓ 6 of round 1, unchanged |
| reviewer: six mutations one at a time | four redden one case each; `ARCHIVE_LIMIT` and the NUL guard redden none |
| reviewer: all six rewritten or added ledger anchors, content mutated one at a time | each drifts — no dead anchor |
| reviewer: `evidence_check.py` with a non-hex, a wrong-hex, and a gone-symbol anchor | silent at exit 0; `1 drifted` at exit 2; exit 2 |
| orchestrator: the `.incoming` escape, clean, before and after the fix | exit 0 with the record outside; then the copy at `ledger.incoming-2.md` inside the root and nothing outside |
| orchestrator after the fixes: the three touched test files | 134 passed |
| orchestrator: `O_EXCL` reverted, then the counting order reverted, against the new pin | each reddens it |
| orchestrator: `testzip` and `ARCHIVE_LIMIT` disabled in turn | each reddens its own case |
| orchestrator: `evidence_check.py --strict .` | 390 ok · 0 drifted · 0 broken |
| orchestrator: `ruff check` and `ruff format --check` on the two changed Python files | clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `skills/implement/scripts/seal.py#linked_path`, `#place`, `#write_members`, `#import_` | the escape has now been closed twice in the same neighbourhood, one name apart |
| round 1 | the four cases planted then, and the three planted now | seven cases in two rounds, none of them reviewed by a round that did not also write them |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 8 — a ledger row with a non-hex hash is dropped silently | issue #97, on 0.6.0, with the reviewer's note that it belongs earlier | the repository owner |
| A root that is itself a symbolic link | `overview.md` §Not verified | the repository owner |
| Whether 32 MB and 512 MB are the right limits | `overview.md` §Not verified | the repository owner, at the first root that meets one |
| The reminder reading `1 work items changed` at N=1 | `questions.md` Q1, and the pull request body | the repository owner |
| A handoff fact from the orchestrator carries no verification label | issue #89, on 0.6.0 | the repository owner |
