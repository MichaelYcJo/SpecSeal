# 1791270164-the-release-seal-is-drawn-in-curves — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 6d73664f |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md`'s phase 7 row: `git mv docs/seals assets/seals`; `candidates/` with `section-28`, `key-28` and `section-14-light-red`, each a chart `.txt`, a `.ans` and a `.png`, as `spec.md` §*Data & interfaces › The gallery* says; the README's *Candidates for #857* section saying all three stood on the parchment sheet decision 6 retired; the README out of `tests/test_docs_line_wrap.py#COVERED` unless something else needs it; a divergence row for the move.

The spawn added: the charts from the orchestrating session's `chart28-section.txt` and `chart28-key.txt`; the `.ans` files from the owner's `specseal-28-section.ans`, `specseal-28-key-big.ans` and `specseal-stamp-14.ans`, regenerated lean, with codes only on change, so a terminal prints each one whole; and the owner's look at the 28-cell stamp recorded first as accepted, with Q15 at its default (`af080e19`, `questions.md` Q16).

## What this phase found

**The § candidate's chart is refused by the loader it is meant for.** `read_chart` refuses an `M` outside the field (phase 6), and three `M` cells of `chart28-section.txt`'s line 5, at columns 12, 17 and 18, lie in the groove. The reference renderer painted the groove over them, so the owner never saw those three cells: the `.ans` shows the mark without them, and a scratch comparison of the chart with the mark's three tones in the `.ans` matched at no offset until that line was read. The archive keeps the chart as the owner's candidates were drawn from it, and the README says it is refused until the three are dropped. The key's chart is accepted and matches its `.ans` at one offset; the light-red §'s 14 × 14 grid matches its `.ans` too, and is exactly the grid 35277597's `build` marks.

**The light-red § can be drawn again from its commit, the 28-cell ones cannot.** 35277597's `stamp` over the hook test module's `FULL_ROWS` paints the same cells as the owner's `specseal-stamp-14.ans`, so the README gives that command. The two 28-cell files came from the orchestrating session's reference renderer over a sample panel, and the README says no tag draws them.

**One commit of the move and the README's new section lost git's rename.** The README grew from 70 lines to 147, past what git's rename detection pairs, so `git log --follow` would have stopped at the move. The move went in alone at `ec4aee4b`, byte for byte, with the line-wrap entry; the title and the section followed in `6d73664f`.

**The lean `.ans` files paint the same cells.** Each was parsed into cells, its caption line dropped, and written back with one SGR per change, its parts together, no reset inside a line and one at the end; a script then read the new file back and required every visible cell equal to the owner's file's. Sizes: `section-28` 11,451 to 7,742 bytes, `key-28` 10,106 to 6,956, `section-14-light-red` 3,174 to 2,954, all with the caption line gone. The three previews were drawn from the archived files by the gallery's rule (12 × 24 pixels a cell, Menlo, transparent where nothing is painted) with the worktree's Pillow, and looked at once each.

**`COVERED` lost its entry, and nothing else needed it.** The list is opt-in and only `README_PAIR` constrains it; no case enumerates `assets/`, and `tests/test_the_release_check_watches_what_ships.py` already names `assets` among the roots that stay home.

**What was run.** `git ls-files docs/seals` prints nothing and `git ls-files assets/seals` fourteen files; `cmp` of the four drawings against `git show 6d0096b0:docs/seals/<name>`, equal, and the README equal at `ec4aee4b`. `bin/test tests/test_docs_line_wrap.py tests/test_release_hygiene.py -p no:xdist`: 88 passed at the move and again with the candidates. No case was added: the gallery is documentation no code path reaches (`spec.md` S10).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/seals/` and its five files | `assets/seals/`, moved with `git mv` at `ec4aee4b` |
| `docs/seals/README.md` in `tests/test_docs_line_wrap.py#COVERED` | nowhere: `assets/` is not a place the docs checks read; the fragment re-reads the four released rows that cite `COVERED` |
