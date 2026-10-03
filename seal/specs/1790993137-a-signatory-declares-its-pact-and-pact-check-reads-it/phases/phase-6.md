# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | 249a76c4 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 6, the words and the policy: `docs/the-pact.md` in fold
shape (this work item's marker, a bold rule sentence, one `Enforced by:` line
per statement), added to `tests/test_docs_line_wrap.py`'s list; the S13 case
in `tests/test_one_word_one_meaning.py`; the changelog fragment and the
ledger fragment. Verified by S13, red by planting "the home repository" in
`templates/pact.md`; `fold-check` over `docs/`; `evidence-check` over the new
fragment; the suite and the lint stay `unverified` until the sealer's run.
`questions.md` Q13 closes here. The spawn added the three text-reading
hygiene modules no round runs, and `ruff check` and `ruff format --check` on
every file touched.

## What this phase found

**The frame holds for this phase.** `docs/the-pact.md` carries eight
statements under one marker, each a bold rule sentence with one `Enforced
by:` line naming cases that exist, and `fold-check` read 158 statements in 15
documents under the `Fold shape from | 0` cutoff and exited 0. It is 138
lines, far under the ceiling, and joined `COVERED` at birth because it was
written wrapped.

**What S13 sweeps, and what it leaves.** The case reads `templates/pact.md`,
`docs/the-pact.md`, the routing subsection of `orchestration.md` and the
`pact-check` section of the `evidence-check` skill, each section cut at its
next heading of its level or above. It refuses the three working words of
#647's thread and *pact repository* in any spelling, which would give the
pact's repository the noun the owner withheld. It also pins the policy's two
definitions. The code's `home`, which names a repository's `seal/` root
throughout this tree (`optin.home_at`), is a different concept and stays out
of the sweep; a search of every shipped file this work item touched found it
used only that way.

**Q13, answered over the whole build.** The rows this work drifted outside
its own fragment were found by `evidence-check .` after each phase and are
named in each phase's record: 12 and one in phase 1, 7 in phase 2, 20 in
phase 3, 6 in phase 4, 1 in phase 5 and 2 in phase 6
(`seal/releases/0.12.0.md` and `0.9.3.md`, on `test_docs_line_wrap.py`'s
`COVERED`). Every one was read against its edit and carries a dated note in
the file it lives in; two were corrected in place (phase 1). This phase's
first note script refused the `0.9.3.md` row, which ends without a closing
pipe, after `--reverify` had already re-stamped both; the note was then
appended to that row's last cell as written, so both rows carry the reading
their new date records. `evidence-check --strict .` exits 0 at the end.

**Verified, executed.** Red: `mutation-check` planted *the home repository*
in `templates/pact.md` and *pact repository* in the policy, and each turned
the S13 case red. Green: the 107 modules naming `docs/`, a changelog,
`seal/specs` or this phase's files, with `tests/test_no_real_identifiers.py`,
the version timer (`tests/test_release_hygiene.py`), the interpreter floor
case (`tests/test_a_script_says_which_interpreter_it_needs.py`) and the four
new modules, gave 5563 passed, 77 skipped. `fold-check` exited 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
