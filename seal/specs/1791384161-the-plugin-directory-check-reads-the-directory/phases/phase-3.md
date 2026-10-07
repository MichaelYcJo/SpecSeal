# 1791384161-the-plugin-directory-check-reads-the-directory — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | b30fd044 |
| Ran by | unknown — the spawn prompt named the agent, `smith`, and not the model |

## What this phase was asked

`plan.md` phase 3: the records. `changelog.md` in this directory, one entry
saying what the command stopped claiming and what the box now says (#858). The
ledger fragment: S9, P1c and W4 read against the new text, each expected to
hold, then written as `Re-read ·` rows by `evidence-check --reverify --into
… --checked 2026-10-08`; no row for the command. `overview.md` with `## Not
verified` naming Q2's answerer. A phase record per phase. The spawn prompt
added: Q2 goes to `overview.md` §*Not verified* with the repository owner as
answerer.

## What this phase found

**A fourth family drifted.** After c4990707, `evidence-check` named rows in
three families the plan listed and one it did not: O2
(`seal/releases/0.18.1.md:368`), which anchors `docs/branch-and-release.md`
§*Work accumulates on a release branch* — the section the third-reader
paragraph sits in. Its claim is about the merge method's home there, and the
merge table and its rule sentences are untouched, so it holds. P1c anchors
the same section, which the plan's coordinates (`Cutting a release` only) did
not show.

**The fragment's file name is the full directory name.** The spawn prompt named
`seal/ledger/1791384161.md`. `.github/scripts/fold_ledger.py`'s fragment
reader takes the section heading from the file's base name, and every released
section heading carries the full name (`seal/releases/0.20.0.md`'s `### 1791270161-the-broad-gate-…`),
so the fragment is
`seal/ledger/1791384161-the-plugin-directory-check-reads-the-directory.md`.

**The writer's notes were generic, and each row now says what was read.**
`--reverify --into` wrote *re-read against the code at the hashes in this
row*. Each row's last cell now names what changed in its anchors and why the
claim still holds; S9's own executed check reproduces (`grep -c "on the tag"
docs/release-checklist.md` prints 0, exit 1), and W4's two cited cases ran
green (2 passed).

**The three documentation facts were opened by the build, not only the
frame.** `claude.com/docs/directory/publish` and
`claude.com/docs/directory/submission-status` were fetched on 2026-10-08: a
merge to the tracked branch is scanned and published with *Updates without
resubmitting*; a Console listing *stays as it is* and is moved by Withdraw or
by email; *A plugin is installable only once its status is Published*, and
*Not live yet* is its own status. The portal's **Submissions** list is where a
plugin's status and card are, at `claude.ai/directory/manage`, and the Console
page's address is the docs' own link. So the command's docstring and the box
rest on a reading taken by the build too, and only the logged-in pages remain
unverified (`overview.md`).

**Verified by, executed.** `bin/evidence-check .` exit 0, 0 drifted;
`bin/evidence-check --strict .` exit 0. `bin/test -q -p no:cacheprovider` over
`tests/test_the_ledger_fragments_fold_at_release.py`,
`tests/test_a_record_states_what_the_tree_has.py`,
`tests/test_a_question_says_who_can_answer_it.py`,
`tests/test_no_real_identifiers.py` and `tests/test_docs_line_wrap.py`: exit
0, 222 passed. `bin/unverified-check` over the overview: 2 open, 0
unreadable, exit 0. `bin/fold-check`: exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
