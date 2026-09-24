# 1790208593-the-fold-writes-each-release-to-its-own-file — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 5bd69d1e |
| Ran by | smith on Fable 5.1 — the value the spawn gave; this phase ran after the resume under a harness notice naming Opus 5.5, so the spawning session is the one to confirm |

## What this phase was asked

The paragraphs the plan lists: `CLAUDE.md`, `CONTRIBUTING.md`,
`docs/release-checklist.md` §2/§3, `docs/branch-and-release.md`,
`docs/the-evidence-ledger.md`, `seal/README.md`, both READMEs' trees, the
implement skill's tree, the evidence-check skill's four places, the settle
skill §4, `agents/framer.md`'s reading list, the four carriers of the
paperwork-location sentence; `seal/ledger.md`'s header (S17). Framed as
phase 4; phase 5 since #553 joined.

## What this phase found

**Two of the listed edits do not hold against the tree, and one is not
mine to make.**

- **`seal/README.md` is the template verbatim.**
  `tests/test_first_setup_asks_once.py#test_the_seal_readme_is_the_template_verbatim`
  asserts `seal/README.md == templates/seal-README.md`, and S18 keeps
  `templates/` untouched (the plugin ships no fold, so the template
  describes the fragment rule and nothing about release files). S16's edit
  to `seal/README.md` was made, seen red, and reverted. That file's layout
  block still says the fragments are *folded into ledger.md at the release*,
  which is false for this repository from this change on. Whether the
  template changes, or this repository's copy is allowed to diverge from it,
  is the repository owner's decision (`overview.md` §*Not verified*).
- **`CLAUDE.md` is left unedited.** `agents/smith.md` says no agent message
  can authorize changing `CLAUDE.md`, and this instruction reached the build
  from the frame and the spawn prompt, not from the user. The two paragraphs
  that go false are *Both kinds of fragment are gathered at the release*
  (*moves every ledger fragment into `seal/ledger.md` under a heading for the
  release*; *The checker reads both `seal/ledger.md` and the
  `seal/ledger/*.md` glob*) and *When `seal/ledger.md` conflicts* (true, but
  it no longer names every ledger file). Paste-ready text for the owner:

  > `.github/scripts/fold_ledger.py --version X.Y.Z` moves every ledger
  > fragment into that release's own file, `seal/releases/X.Y.Z.md`, and
  > removes the fragment; `seal/ledger.md` keeps the notation and the rows
  > from before the fragments existed. The checker reads `seal/ledger.md`,
  > the `seal/releases/*.md` glob and the `seal/ledger/*.md` glob alike,

  and, for the conflict rule's heading: **When a ledger file conflicts —
  `seal/ledger.md` or a `seal/releases/<X.Y.Z>.md` — resolve it hunk by hunk
  and read both sides.** `test_a8_both_rule_documents_say_what_to_do_at_the_conflict`
  holds needles rather than the heading, so it is green either way.
- **The settle skill's sentence is pinned.**
  `test_the_skill_says_what_a_fold_does_to_the_ledger` holds
  *`seal/ledger.md` changes only by removal and re-verification.* verbatim.
  The rule it pins is the removal-and-re-verification one, not the address,
  so the sentence stands and the next sentence extends it to every release
  file.

**A marker I added was a claim I did not mean.** The new §2 paragraph in
`docs/release-checklist.md` first carried a
`<!-- specs/1790208593-… -->` line, the way the fold's own paragraph does.
`tests/test_a_folded_statement_names_what_enforces_it.py` reads that marker
as `settle`'s record of a folded statement and requires an `Enforced by:`
line under it. This paragraph is not a fold, so the marker was removed.

**The release-checklist text states no count of sections.** The frame's 37
was wrong (phase 4), and a count written into a procedure would be wrong
again at the next release anyway.

**A text anchor went BROKEN** on the reworded `docs/branch-and-release.md`
paragraph (`#"one \`###\` section per work item marked with …"`); the
sentence is kept on one line as it was, the claim being unchanged.

**Verification, executed.** 94 test modules, all that read one of the
edited documents (by grep over `tests/*.py` for the document names), before
the three fixes: `4 failed, 3629 passed, 8 skipped` — the three above, and
the `overview.md` case that is phase 6's. After the fixes, the plan's module
list and the three: `419 passed`. `test_docs_line_wrap.py` green;
`README.md` and `README.ko.md` move together in the commit. The line-wrap
case did not flag a 126-column line I had made in
`docs/branch-and-release.md`, so it evidently does not reach every line;
added lines over 88 columns in prose were found by `awk` over the diff and
reflowed (tables and code excepted).

**Rows re-read:** 23 rows across `seal/ledger.md` and C's fragment whose
anchored document sections the edits touched (`--reverify` re-stamped 25,
two rows citing two units each), plus the self-anchored row's second
cascade. `--strict .` exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the frame's edit to `seal/README.md`, never committed | the owner's decision on `templates/seal-README.md`, named in `overview.md` |
| the frame's edit to `CLAUDE.md`, never made | the owner, with the paste-ready text above |
