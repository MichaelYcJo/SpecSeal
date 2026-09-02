# 1788331011-two-roots-hold-three-lifetimes — review round 3

<!-- seal/specs/1788331011-two-roots-hold-three-lifetimes/rounds/round-3.md — the
verifying round on round 2's fix diff (207b432..bc11b81), written by the
review orchestrator right after the report was verified. It opened round 2's
five `fixed` verdicts and the four planted tests as a finding surface. -->

| Field | Value |
|---|---|
| Target SHA | b591ba1 (the fix diff is 207b432..bc11b81; b591ba1 is round-2's record edit only) |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — the fix pass for 🟡 H had not run when this record was written; round-4 is the verifying round and sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 H (a `specs/` symbolic link half-moves under a stamp with a broken ledger; the caller may instead record it with 🟡 A's grounds, which turns this line to `no`) |

- [ ] Pass

<!-- The orchestrator's decision on 🟡 H: fix it, on the grounds already
used for round-2's 🟡 A — a stamped half-move is the class round-1's 🔴 1
was, and here the ledger is left broken rather than missing. The fix pass
is a FRESH smith spawn with the reviewer's coordinates, not a resume: the
resumed smith stands above 370k input tokens after two passes, and #89
asks what a fresh pass costs at that point. -->

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 2-A | round-2 🟡 A (a symlinked `.specseal/` half-moved under a stamp) | `hooks/root-migrate.py#main` | closed | planted test executed red against 207b432's hook (`moved 1 work item … 0 ledger rows`, stamped, `seal/` present), green at HEAD on two starts: the link line naming "Coming up from 0.3.x", `seal/` absent, not stamped |
| 🟢 2-B | round-2 🟢 B (`ls-files` down moved from the directory listing) | `#dirty` | closed | planted test executed red against 207b432 (`3 ledger rows re-pointed`), green now with the dirty line; the whole migration file 34 passed on a healthy tree, so the two extra `ls-files` calls change no result |
| 🟢 2-C | round-2 🟢 C (an item-shaped tracked file moved as a work item) | `#old_items`, `spec.md` §"Which entries of `specs/` are SpecSeal's" | closed | executed red against 207b432 (`2 work items`), green now (`left specs/1788000001-a-file.md where it is`); the spec sentence matches the code and the message |
| 🟢 2-D | round-2 🟢 D (`cannot create` named the wrong parent) | `#git_mv` | closed | the nested case executed at HEAD: `cannot create seal/ledger/: [Errno 17] …`, non-resumable, not stamped; at 207b432 the same state says `cannot create seal/:`. The existing `seal`-as-file test passes on both sides, so the nested probe is the discriminator, and the fragment's D row moves from Read to Executed |
| 🟢 2-E | round-2 🟢 E (`by_hand_block` ran to end of file) | `tests/test_the_root_migrates_itself.py#by_hand_block`, `#HEADINGS` | closed | the old helper executed on a copy with the block moved returned the wrong block's 8 lines silently, and `IndexError` on a copy with it removed; HEAD's helper raises `AssertionError` on moved, removed and heading-lost copies, and only parses — the `subprocess` lives in the README test |
| 🟢 2-F | round-2 🟢 F (a relative-symlinked `specs/<id>` dangles) | `#move` | recorded, not a fix | carried from round 2's Deferred |
| 🟡 H | `specs/` ITSELF as a symbolic link is 🟡 A on the other root: the home moves, the work item is called "not tracked as a SpecSeal work item" and left, its rows are re-pointed to `seal/specs/<id>/…` which does not exist, the marker is stamped, the next start is silent | `hooks/root-migrate.py#main` (the `.specseal` link check names `OLD_HOME` only), `#repoint_path` (re-points without asking whether the unit moved), `spec.md` refusal table (the link row names only `.specseal/`) | open — fix pass follows: refuse when `specs/` is a link holding item-shaped directories, after the unit and marker checks so a migrated repository stays silent; the line names the by-hand section; not stamped; test red-first; the refusal-table row and the order sentence widen | executed at HEAD: `moved .specseal/ into seal/ (3 ledger rows re-pointed; left specs/1788000000-a-work-item … (not tracked as a SpecSeal work item))`, stamped, checker `2 ok · 2 broken`, second start silent |
| 🟢 I | the `.specseal` link line prints at every start on a migrated repository that kept `.specseal → seal` for old tooling | `#main`, `spec.md` refusal table | record only — the spec chose "tested first, at every session start until the link is gone"; one clause in the row says the line is not a half-move | read |
| 🟢 J | `dirty()` runs `git ls-files` twice more on paths `moves()` just listed | `#dirty`, `#entries` | record only — two git processes, once per repository, old-layout path only | read |
| ❓ 2-G, ❓ 1-a, 🟢 1-10 | the deferred items | — | still deferred | CI's legs; the PR body |

New units of round 2 (four test functions) judged as code: each fails against 207b432 on its own first assertion with the hook's actual message, the symlink fixture writes only under `tmp_path`, and the helper test never touches the tracked README. Contract changes of round 2 walked with `grep` over `hooks tests skills`: no call site outside the row; one nit — `HEADINGS` is also read directly by the new test, which the `New units` row already names.

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_the_root_migrates_itself.py -n auto` at b591ba1 | 34 passed |
| the four planted tests against 207b432's `root-migrate.py` (scratch copy) | A, B, C red on their first assertion with the hook's message; D's top-level test passes on both sides |
| `.specseal/map/` with `seal/ledger` a committed file, HEAD and 207b432 | `cannot create seal/ledger/:` vs `cannot create seal/:`; both non-resumable, not stamped |
| 207b432's `by_hand_block` on moved / removed copies, both READMEs | 8 lines from the wrong block, no assertion / `IndexError` |
| HEAD's `by_hand_block` on moved / removed / heading-lost copies | `AssertionError` each, matching text |
| `specs/` → symlink to `items/`, two session starts | 🟡 H's line, stamped, `2 ok · 2 broken`, second start silent |
| `evidence_check.py --strict .`; the fragment alone | 219 ok · 0 drifted · 0 broken; 59 ok |
| `uvx ruff check` / `format --check` on the two changed `.py` | clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `hooks/root-migrate.py#main` (the link check) | where 🟡 H's second refusal lands, after the unit and marker checks |
| round-2 | `hooks/root-migrate.py#repoint_path`, `#old_items` | H's mechanism: a unit that did not move is still re-pointed |
| round-1 | `hooks/root-migrate.py#dirty` | ❓ 1-a (Windows) and 🟢 J both live here |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟢 1-10 the eight defaults of questions.md | the PR body, at opening | the orchestrator |
| ❓ 1-a Windows porcelain / pathspec | CI's windows leg on the PR | CI |
| ❓ 2-G case-insensitive filesystems | CI's macOS / Windows legs on the PR | CI |
| 🟢 I the link line on a migrated repository keeping a link | this record and one clause in the refusal-table row (the fix pass adds it) | nobody — recorded |
| 🟢 J two redundant `ls-files` | this record only; `seal/follow-up.md` is not written for two processes | nobody — recorded |
