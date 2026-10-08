# 1791384156-config-rows-coordinates-and-headings-have-one-reader — round 1 fixes

Fix range `9f186d2a..105d96ea`, eight commits, written by smith on Opus 5.5
from the committed record at 9f186d2a.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 🔴 1 | fixed | c6e32946 — the doubled freeze row's case matches `seal/config.md` with `os.sep` read as `/`, as the sealer's cases do; the other new path assertions were read and build their path with `os.path.join` or name a git path |
| 🔴 2 | fixed | 105d96ea — `survivors.md` records the four places the sweep names over `origin/release/v0.21.0...HEAD`, each read; the other 29 of the round's 33 were character-class patterns that stopped being named once 0bb98893 froze `settle`'s old copy in the tests, and the file says so. `survivor-check` with the file exempting: exit 0 |
| 🟡 3 | answered | corrected at 9e508b5c: the two `Re-read ·` rows for 0.19.0's `Corrected · C1` are replaced by one `Corrected ·` row whose claim says an unreadable `config.md` is refused at exit 2 before anything is planned, carrying every coordinate the released row rests on plus `frozen_from` and `vendored_config_text` |
| 🟡 4 | fixed | 0bb98893 — S7 compares `coordinate_paths` with `settle`'s own pattern as it stood at 0.20.0, frozen in the test, over the ledgers released by 0.20.0; red under `mutation-check` with the checker's quoted locator narrowed |
| 🟡 5 | fixed | f743e6d2 — `pact_notices` reads the config through `config_at_head` (HEAD's blob decoded strictly, or `hooks/config.py#config_text` under `--worktree`), so an unreadable config is one notice naming it; `read_record` decodes a file on disk as the HEAD read does, so `--worktree` no longer raises. Red under `mutation-check` three ways |
| 🟡 6 | fixed | 6907b221 — `LOOSE_HEADING` asks `heading_level` for level 2 or 3 and decides only the wording; the heading grep reads any counted `#` run (`#\{\d`). Red under `mutation-check` with the old pattern put back |
| ⬜ 7 | fixed | 9af7b103 — `vendored_config_rows`' docstring names the second way the twin differs, a row holding a character only Python ends a line at, with the round's measurement |
| ⬜ 8 | deferred #872 | the mechanism, which lines a reader hides before it asks the heading rule, is the live-line family #872 holds; `overview.md` §*Not done* states the limit of `spec.md`'s sentence (293d3ca8) |
| ⬜ 9 | answered | `spec.md` §*Data & interfaces* ordered `pact_declaration`'s own doubled-row sentences to become the generic one's, and `docs/the-pact.md` §*How a signer names the pact* says a row written twice has no value at all; a doubled `Pact` now lists no pact, so there is no row to tell a person to merge entries into |
| ⬜ 10 | fixed | 9af7b103 — the clause reads "a label shown twice has no value at all", wrapped under the line length |
| ⬜ 11 | fixed | 9af7b103 — `markdown_lines` is memoised per distinct text (`_shown_lines`); one `--strict .` run makes 360 fence-blanking passes with it and 1,626 without, counted in-process |

The fix pass's ledger rows are K26–K28 and the re-reads its edits drifted, in
`seal/ledger/1791384156-config-rows-coordinates-and-headings-have-one-reader.md`.
`changelog.md` gained the pact notices' reading (293d3ca8).
