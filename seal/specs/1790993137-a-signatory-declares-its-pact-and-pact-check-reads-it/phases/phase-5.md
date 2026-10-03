# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 6900d78f |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 5, `pact-check`: `skills/evidence-check/scripts/pact_check.py`,
`bin/pact-check` and `bin/pact-check.cmd` copied from `bin/correction-check`.
It reads the pact and its signatories, the map and the siblings, each
signatory's rows and anchors, and grades with the history classification and
the exit codes of `spec.md` items 8-9. A `## pact-check` section in
`skills/evidence-check/SKILL.md`, and a row in both editions of the README
cheat sheet. Verified by S3 and S8-S12 in a new `tests/test_pact_check.py`
over two temporary repositories (clause v1 then v2 committed, v3 on a side
branch), with `HOME` pointed at a temporary directory holding the map, and
S14 through `tests/test_a_document_that_names_a_script_says_how_to_reach_it.py`.
`questions.md` Q12 is this phase's.

## What this phase found

**The frame holds for this phase.** The code is in two commits:
`135c0a8c` (the script, its wrapper pair and 15 cases, committed before the
mutation loop) and `6900d78f` (the skill section, both cheat sheets, two
cases the loop asked for, and the classification entries).

**Decisions settled while writing it.**

- A checkout named by the map is trusted only where its origin normalises to
  the signatory's; otherwise it is a signatory not found, naming what the map
  points at. A sibling is taken only where exactly one has that origin, and
  two are named and not chosen between, which is what *nothing is guessed*
  comes to with linked worktrees side by side.
- A signatory with no `seal/` root, or whose `config.md` names no `Pact` row
  for this repository's origin, is `ONE-SIDED`, exit 2. A `config.md` that is
  there and will not read is `UNREADABLE`, exit 2; an absent one is read as
  no rows, and so reaches `ONE-SIDED`.
- An unreadable map is `REFUSED`, exit 2, because read as empty it would
  report every signatory it names as not found.
- Anchors are read outside closed fences (`evidence_check.py#unquoted`), and
  only those naming this pact; a signatory of two pacts cites the other one
  too.
- "Another ref" is every branch, remote-tracking branch and tag HEAD does not
  hold, and the named ref is the first such ref holding the version, sorted.
- Findings print as `<STATUS> <signatory> <file>:<line> <anchor> — <what to
  do>`; each read signatory gets a `READ` line carrying its `Pact notify`
  value, which is how the value is printed from the first day.

**The mutation loop asked for two cases and removed one unit.** Seventeen
breaks, one at a time: thirteen red at once. The map's origin check and the
fence rule survived, and a case each was added
(`test_a_map_line_naming_a_checkout_of_another_repository_is_not_trusted`,
`test_an_anchor_quoted_in_a_closed_fence_is_an_example_and_not_graded`), then
both went red. Two survivors are behaviour-equivalent. Leaving HEAD's commits
in the other-refs list changes no verdict, because `grade` reads HEAD's list
first; it stays, documented as saying what the list is. The local-mode
`tracked` flag changed nothing, because a pact under the git directory is a
path git never tracked and its history is empty by itself; the flag was
removed and `History`'s docstring says why the list comes back empty.

**Q12, answered.** `pact_check.py` loads `hooks/config.py`, `hooks/optin.py`
and `evidence_check.py` by path. A probe (`test_tmp_q12.py` in this
session's scratchpad, deleted after) loaded all three under CPython 3.12.2,
the interpreter floor `tests/test_a_script_says_which_interpreter_it_needs.py`
holds, and under 3.14.3: nothing printed, the tree unchanged, and only the
standard library and `hooks/blocks.py` imported, which `hooks/config.py`
already puts on `sys.path`. The `seal.py` half was phase 1's.

**Two classification lists named the new command and walk.**
`tests/test_a_reference_root_is_read_and_never_taken.py#SHIPPED` fails on a
`bin/` command nobody classified, and `pact-check` is pinned: it reads only
under each repository's root as `optin.home_at` names it. The `splitlines`
census took `pact_check.py#path_map` under the reason `config_rows` has,
because it is that walk.

**Ledger rows this phase drifted (Q13, phase 5).** One row outside this work
item, `seal/releases/0.17.0.md`'s D3 on `SHIPPED`; read against the edit, it
holds, and it carries a dated note. P6 drifted with the template's corrected
sentence about which lines name the current hash and was re-read. P10's
first spelling cited a heading holding backticks inside a single code span
and the bare wrapper path, and both were refused until respelled.

**Verified, executed.** Red: the 17 breaks above. Green: the 113 modules
naming a file this phase touched, or globbing `bin/`, the templates or the
shipped scripts, gave 5501 passed, 78 skipped and the two classification
failures above; with the entries, those two modules gave 164 passed and the
phase's module 17 passed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
