# 1790076050-the-release-tail-is-three-acts-no-document-names — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `7efe496c` |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

§6 stops at neither the tag nor a sentence, and two sentences reach
`docs/branch-and-release.md`. Two boxes in `docs/release-checklist.md` §6 —
the release note exists, the directory carries the version — each with its
command; the fixed-name sentence and the outside-pin sentence beside
§*What breaks when the last row is squashed*. Verified by a case over both
documents — A5, A8.

The phase row carries a conditional: "The directory box's command exists from
phase 3, so phase 2 lands before it only if the box names the command it is
about to gain; otherwise run 3 before 2 and say so."

## What this phase found

### Which side of the conditional was taken, and why

**Phase 3 was built first.** The box names
`python3 .github/scripts/plugin_directory_check.py`, and that file was in the
tree at commit `c8983b14` before this phase wrote the box.

The alternative — a box naming a command it is about to gain — is the defect
this work item is about, written into the repair. A box naming a script
nobody wrote reads exactly like a box naming one somebody did, and the reader
who finds out is a person at a release. So
`test_each_box_names_something_that_exists` resolves every path a box names
against the tree, which is an assertion that can only be made from this order.

### §*What breaks when the last row is squashed* is a paragraph, not a heading

`spec.md` and `plan.md` both cite it with a section mark. `grep '^#'` over
`docs/branch-and-release.md` returns three headings and none of them is this;
it is a bold lead-in inside `### Work accumulates on a release branch`. That
matters twice. It is where the ledger's two anchors on this file are minor
line anchors rather than heading paths, and it is why `squash_rule()` in the
case slices from that bold lead-in to the next one rather than looking for a
heading: a sentence dropped into some other part of a 296-line document would
otherwise satisfy A8.

### The identifier sweep cannot see a file until git can

Phase 3 ran `tests/test_no_real_identifiers.py` and read `5 passed` — over a
corpus that did not contain the file it had just written. That sweep walks
`git ls-files`, so an untracked new file is outside it, and the pass was a
pass over the tree as it stood before the phase. The moment phase 3's commit
tracked the file, this phase's run reported it:

```
.github/scripts/plugin_directory_check.py:46 <the raw-content host>
```

**A narrow run of a corpus sweep is only as current as the index.** Anything
that walks `git ls-files` — and several checks here do — is measuring
committed-or-staged state, so a clean report over new work says nothing until
the work is at least staged. Both offending lines were reworded (the script's
docstring and phase 3's own record, which quoted the sweep's output verbatim
and so reproduced the violation inside the record of the repair), and this
phase's runs were made with the tree staged.

### The line-wrap limit caught the box, and the fix removed a path

`docs/release-checklist.md` is in `tests/test_docs_line_wrap.py`'s `COVERED`
list at 88 display columns. The directory box cited `questions.md` Q1 by full
path, which is 99 columns on one line and cannot be wrapped without breaking
the path. The box now says "the work item that built this box carries it as an
open question" instead. Nothing is lost that a reader of a checklist needed:
the answer does not change what the box says, which is Q1's own recorded
reason for not blocking.

### How each case was shown red (§15)

Fifteen mutations against the two documents, each removing one sentence, box
or command, with the file restored from a byte copy kept outside the tree.
`6 passed` before and after.

| Mutation | Case that went red |
|---|---|
| the release-note box removed from §6 | both note cases |
| the directory box keeps its prose and loses its command | `test_two_boxes_follow_the_tag_and_each_carries_its_command`, `test_the_directory_box_says_it_never_fails_a_release` |
| **the note box moves above the tag** | `test_two_boxes_follow_the_tag_and_each_carries_its_command` |
| the note box stops saying it confirms rather than performs | `test_the_note_box_says_it_confirms_rather_than_performs` |
| **the note box names the workflow but no command that reads its run** | the same case, **after it was strengthened; see below** |
| the directory box stops saying it never fails | `test_the_directory_box_says_it_never_fails_a_release` |
| the directory box drops the *not listed* state | the same case |
| the third-reader sentence removed | `test_an_outside_directory_is_in_the_enumeration` |
| the third reader named without what it pins | the same case |
| the pointer to the box that reads the pin dropped | the same case |
| the fixed-name sentence removed | `test_the_fixed_name_sentence_sits_beside_it` |
| the fixed-name sentence drops why it is fixed | the same case |
| the one-copy sentence dropped | the same case |

**Two mutations found nothing on the first pass**, and the two failures were
different in kind, which is worth keeping apart:

- *the boxes move above the tag* was a **bad mutation**, not a weak case: it
  edited `<merge commit>` to `<merge-commit>` and moved no box at all, so the
  suite was right to stay green. Rebuilt as an actual move — the note box cut
  from below the tag and reinserted under the heading — it reds two cases. A
  mutation that changes nothing proves nothing, and it looks identical in the
  output to a case that pins nothing.
- *the note box stops naming a command that reads the run* was a **weak
  assertion**. The box names `publish-release.yml` twice, once as the workflow
  that fires and once inside `gh run list --workflow …`, so removing the
  runnable half left the case green. Naming a workflow and giving a way to
  read its run are two things, and the second is the one a reader who finds no
  release actually needs. The case now asserts both, and the mutation reds it.

### What a gate change owes (`CONTRIBUTING.md`)

Neither deliverable is a gate — both are prose and boxes a person reads.
**Failure direction: none in CI.** The cases above are what goes red, and they
go red in the tree rather than at a release. **Prompt budget: zero** for the
documents; the two commands they name are typed by a person already working
down the checklist, and neither asks a question.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the full path to `questions.md` Q1 from the directory box, cut for the 88-column limit | the box still says an open question exists and that the answer changes nothing it instructs; the row itself is unchanged in `questions.md` |
| the literal raw-content host from `.github/scripts/plugin_directory_check.py`'s docstring and from `phases/phase-3.md`'s quoted sweep output | both now name the host by description; the facts are unchanged and `overview.md` records the class |
