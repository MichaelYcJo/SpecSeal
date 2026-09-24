# 1790260564-a-moved-file-counts-as-written — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | cb7b8d10 |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#564, the gathered reading's three assumptions, built first because it
touches the read boundary and the fragment reader inside `corrected` that
phase 2 builds on. `read_blobs` normalises `\r\n` to `\n`. One region helper
sits behind `blank_released` and `only_released`, and after a version heading
only a version heading or `^##\s+\[?unreleased\b` (case-insensitive) changes
the region. The fragment reader in `corrected` reads the paths
`a_gathered_fragment` accepts in `tracked(root, a)`. The module docstring's
released-section paragraph and `blank_released`'s docstring lose *up to the
next `## ` heading*. Ledger rows C1, H1, C2 and the others `evidence-check`
names are re-read, and corrected where false. G7, G8 and G10 seen red at
`c52e8350`, G9 red by mutation, G10 asserting the committed blob. The spawn
added: `questions.md` Q1 is built on its default, so `gather_changelog.py`
and `publish_release_note.py` are left alone (filed as #586).

## What this phase found

- **The frame holds.** Every coordinate `plan.md` §*Technical context* names
  was where it said, and the three probes went red at `c52e8350` exactly as
  #564 recorded: G7, G8 and G10 each exit 0 with `against 2 sentence(s)`.
- **Reading `tracked(root, a)` from `corrected` is a new path list, and the
  module's own case said so.**
  `test_every_path_list_this_module_derives_from_git_is_filtered_or_named`
  went red: `tracked` was declared filtered by its ONLY caller, `corpus`. The
  plan names the extra `ls-tree` but not this case. It is reclassified rather
  than worked around: `tracked` now maps each caller to the filter it
  applies (`corpus` → `records_a_past_state`, `corrected` →
  `a_gathered_fragment`), and the set of callers is still checked against
  the source, so a third unfiltered caller is still red. Ledger row S2
  (`seal/releases/0.11.2.md`) said *its only caller* and is corrected in
  place.
- **The listing is lazy.** `tracked(root, a)` runs only when the tip's
  `CHANGELOG.md` has a marker, so a repository with no gathered fragments
  pays no extra `git` process.
- **`SECTION_HEADING` is gone**, not kept unused: its comment said *Any `## `
  heading, which is where a section ends*, which is the rule this phase
  replaces. `UNRELEASED_HEADING` and `released_lines` replace it.
- **The unused spelling survives in one released changelog entry.**
  `CHANGELOG.md` line 37 (0.15.1) still says *up to the next `## ` heading*.
  It is a released entry, which is not rewritten, and the sweep blanks it.
- **Gate items** (`CONTRIBUTING.md` §*What a change to a gate must carry*):
  - *Test seen red:* G7, G8 and G10 at `c52e8350` (exit 0, where 1 is owed).
    G9 is green there and red with the `Unreleased` arm deleted from
    `released_lines`, the file restored from a copy afterwards.
  - *Failure direction:* the sweep holds more and writes less, so it reports
    more. The ⬜6 rule also takes a fragment's post-heading text out of the
    pool, so it reports less *there*; that text is released, and nobody may
    correct a survivor inside it. A wrong deny costs a red run and a
    `survivors.md` row; a wrong allow costs a round.
  - *Prompt budget:* zero. The sweep prints and exits.
  - *Platform:* CRLF is the platform surface. G10 sets `core.autocrlf=false`
    in its fixture and asserts the committed blob holds `\r\n` after the
    marker, so a runner whose git converts line endings cannot turn it into
    an LF case (§13). CHANGELOG.md is written in binary mode so Python's
    text-mode newline translation on Windows cannot double the `\r`. Only
    macOS was run here; the three-OS matrix in `test.yml` is the rest.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `SECTION_HEADING` and its comment (*any `## ` heading is where a section ends*) | `released_lines` and `UNRELEASED_HEADING`, which state the replacing rule; ledger row G8 in `seal/ledger/1790260564-a-moved-file-counts-as-written.md` |
| the one-path spelling `seal/specs/{item}/changelog.md` in `corrected` | the reader now asks `a_gathered_fragment`; ledger rows G7 and H1 (corrected) |
