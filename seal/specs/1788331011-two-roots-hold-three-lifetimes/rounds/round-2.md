# 1788331011-two-roots-hold-three-lifetimes — review round 2

<!-- seal/specs/1788331011-two-roots-hold-three-lifetimes/rounds/round-2.md — the
verifying round on round 1's fix diff (3591a00..77632d1), written by the
review orchestrator right after the report was verified. It opened round 1's
nine `fixed` verdicts and the `New units` row as a finding surface, and
executed the inherited ❓ b. -->

| Field | Value |
|---|---|
| Target SHA | a99fd65 (the fix diff is 3591a00..77632d1; a99fd65 is round-1's record edit only) |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | `hooks/root-migrate.py#dirty` (returns True when `git ls-files` cannot answer; two more git calls) → `main`; `hooks/root-migrate.py#old_items` (the `isdir` filter restored, same return shape) → `moves`, `main`; `hooks/root-migrate.py#main` (the symlink refusal before the units are counted, one new output sentence) → `hooks/dispatch.py#GROUPS`, the spec's refusal table; `hooks/root-migrate.py#git_mv` (`cannot create` names `dirname(dst)`) → `move`, `run_moves`, `tests/test_the_root_migrates_itself.py#test_a_file_named_seal_stops_with_a_line_not_an_exception`; `tests/test_the_root_migrates_itself.py#by_hand_block` (a second parameter `text=None`, two assertions) → `test_the_readmes_by_hand_sequence_yields_the_hooks_tracked_set`, `test_by_hand_block_fails_loudly_when_the_block_leaves_its_section`; `tests/test_the_root_migrates_itself.py#HEADINGS` (the Korean value is the full heading) → `by_hand_block` |
| New units | code: none; tests: `tests/test_the_root_migrates_itself.py#test_a_symlinked_specseal_is_refused_not_half_moved`, `#test_when_git_ls_files_cannot_answer_the_move_is_refused_as_dirty`, `#test_an_item_shaped_tracked_file_under_specs_stays_and_is_named`, `#test_by_hand_block_fails_loudly_when_the_block_leaves_its_section` (planted at 9f400d0) |
| Needs a fix | no |

- [ ] Pass

<!-- The reviewer's answer is `no`: 🟡 A is answerable with grounds (a rare
tree, and the by-hand sequence is in the README). The orchestrator chose to
fix it anyway, because a stamped half-move with no ledger is the class 🔴 1
was, and the fix is four lines and one test; 🟢 B–E ride in the same pass.
That makes this round a finding round, so it consumes the cap and round-3
verifies its fixes. -->

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1-1 | round-1 🔴 1 (ignored file under `.specseal/` stops the move for good) | `hooks/root-migrate.py#tracked_names`, `#entries`, `#moves` | closed | planted test executed red against 4516166's hook (`stopped at .specseal/.DS_Store: fatal: not under version control`), green at a99fd65; the second start is silent and `.specseal/` keeps only `.DS_Store` — pinned |
| 🟡 1-2 | round-1 🟡 2 (`seal` as a file, and a `repoint()` failure, escape `main()`) | `#git_mv`, `#main` | closed | both planted tests executed red against 4516166 (`FileExistsError`, `OSError` out of `main()`), green now; the re-point failure prints the `--reverify` line and stamps nothing |
| 🟡 1-3 | round-1 🟡 3 (destination already holding the file promises a continuation) | `#move`, `#taken` | closed | planted test executed red against 4516166 (`destination exists … The next session start continues.`), green now; the spec's refusal-table sentence and the code agree to the letter |
| 🟡 1-4 | round-1 🟡 4 (a row citing a foreign `specs/` entry is re-pointed) | `#repoint_path` | closed | planted test executed red against 4516166 (`4 ledger rows re-pointed`), green now; totals equal pinned |
| 🟡 1-5 | round-1 🟡 5 (the staged commit is refused in-session and nobody says so) | `README.md` §"Coming up from 0.3.x", `README.ko.md` same, `changelog.md` | closed | the waiver line present in all three — read; docs-only fix, P10 not re-run |
| 🟡 1-6 | round-1 🟡 6 (the mark fragment's row still said `.specseal/`) | `seal/ledger/1788310269-the-implementer-leaves-a-mark.md` row 2 | closed | claim says `seal/`, anchor and hash unchanged; `evidence_check.py --strict .` 217 ok · 0 drifted · 0 broken executed |
| 🟢 1-7 | round-1 🟢 7 (S1 / S10 wording) | `spec.md` S1, S10 | closed | read |
| 🟢 1-8 | round-1 🟢 8 (by-hand block ended with `evidence-check .`) | `README.md`, `README.ko.md` by-hand block | closed | planted test executed red against 3591a00's READMEs (`1 ok · 3 broken`), green now |
| 🟢 1-9 | round-1 🟢 9 (`.specseal/map/` holding only ignored files stays) | `#move` | closed | pinned by 🔴 1's test |
| 🟢 1-10 | round-1 🟢 10 (Q1–Q8 defaults) | `questions.md` | deferred to the PR body | no PR yet |
| ❓ 1-a | round-1 ❓ a (Windows porcelain / pathspec) | `#dirty` | out of verified scope | CI's windows leg on the PR |
| 🟡 A | a symlinked `.specseal/` is skipped without a word: git tracks the link as one blob, so `tracked_names` returns nothing for the home, the work items move, the marker is stamped, and `seal/ledger.md` never appears — the checker then finds no ledger. round-1's reading ("fails like 🔴 1") was wrong: it does not fail, it half-moves and reports success | `hooks/root-migrate.py#moves` (the home units), `#main` (the stamp) | fixed — 9f400d0 (code, tests, spec) and bc11b81 (the records) | executed on a fixture (round-1 ❓ b) |
| 🟢 B | "when git cannot answer, the dirty test refuses" is not enforced by code: all-git-down is silence (`optin.repo_root` returns None first); `ls-files`-only-down moves from the directory listing and 🔴 1's shape returns | `#entries`, `#dirty`, `spec.md` step 4, the fragment's 🔴 1 row | fixed — 9f400d0 (code, tests, spec) and bc11b81 (the records) | executed with a patched `git()` (a contrived state) |
| 🟢 C | `old_items` lost the `isdir` filter; an item-shaped tracked FILE under `specs/` moves as a work item, against §"Which entries of `specs/` are SpecSeal's" | `#old_items` | fixed — 9f400d0 (code, tests, spec) and bc11b81 (the records) | executed |
| 🟢 D | a file at a directory's destination reports `cannot create seal/` naming the wrong parent | `#git_mv` | fixed — 9f400d0 (code, tests, spec) and bc11b81 (the records) | executed |
| 🟢 E | `by_hand_block` takes the section to end of file; a lost block would run the next bash block in the README under `shell=True` | `tests/test_the_root_migrates_itself.py#by_hand_block`, `#HEADINGS` | fixed — 9f400d0 (code, tests, spec) and bc11b81 (the records) | executed on an edited copy |
| 🟢 F | a relative-symlinked `specs/<id>` dangles after the move, rows re-pointed, stamped — the same by hand; git's own behaviour | `#move` | record only | executed |
| ❓ G | case-insensitive filesystems | `#tracked_names` | out of verified scope | reading only: git's exact names are compared; CI's macOS/Windows legs measure it |

Contract changes of round 1 walked: every call site round-1's row named was opened and no site outside the row exists (`grep` over `hooks tests skills`; the five other files naming `root-migrate` are comments and docstrings). The `old_items` row's "same shape" hid the filter change 🟢 C names.

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_the_root_migrates_itself.py -n auto` at a99fd65 | 29 passed |
| the six planted tests against 4516166's `root-migrate.py` | 5 failed as round-1 recorded; the by-hand test passed (it pins the README, not the hook) |
| the by-hand test against 3591a00's READMEs | 2 failed: `1 ok · 3 broken` |
| `evidence_check.py --strict .`; the fragment alone | 217 ok · 0 drifted · 0 broken; 57 ok |
| `uvx ruff check` / `format --check` on the two changed `.py` | clean |
| P7 `dispatch.py session-start`, HOME redirected | message delivered, marker written, `.specseal/` gone, `specs/notes` stays |
| `tracked_names`: a space in a name, nested entries, a staged-new file | all listed; staged-new refused by `dirty()`, moved after commit |
| `git()` patched so only `ls-files` fails, `.DS_Store` present | `dirty()` False; `stopped at .specseal/.DS_Store` |
| `subprocess.run` raising everywhere | silence — `optin.repo_root` returns None first |
| `.specseal/map/` with `seal/ledger` a file | `cannot create seal/: … '…/seal/ledger'`, non-resumable, not stamped |
| `.specseal/map.md` with `seal/ledger.md/` a directory | the `taken` line, not stamped |
| a tracked file `specs/1788000001-a-file.md` | moved, "2 work items" |
| `.specseal` → symlink to a tracked directory | home skipped, item moved, `0 rows`, stamped, checker finds no ledger |
| `specs/<id>` → relative symlink | link moved and dangling, `2 broken`, stamped |
| `by_hand_block` on both READMEs; a copy with the block removed | 8 lines each; `IndexError` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/root-migrate.py#moves`, `#main` | the home units and the stamp — where 🟡 A's refusal lands |
| round-1 | `hooks/root-migrate.py#dirty` | where 🟢 B's two lines land; ❓ a's Windows question lives here too |
| round-1 | `tests/test_the_root_migrates_itself.py#by_hand_block` | 🟢 E; also the README-pin whose red state round-2 reproduced |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟢 1-10 the eight defaults of questions.md | the PR body, at opening | the orchestrator |
| ❓ 1-a Windows porcelain / pathspec | CI's windows leg on the PR | CI |
| ❓ G case-insensitive filesystems | CI's macOS / Windows legs on the PR; not written to `seal/follow-up.md` — reading gives no failure shape to name | CI |
| 🟢 F a symlinked `specs/<id>` dangles after the move | this record only; git's own behaviour, the same by hand | nobody — recorded |
