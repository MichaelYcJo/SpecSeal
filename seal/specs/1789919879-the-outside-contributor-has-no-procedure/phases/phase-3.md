# 1789919879-the-outside-contributor-has-no-procedure — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | a968cc7c |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`.github/PULL_REQUEST_TEMPLATE.md`, carrying the base-branch fact in its own
words plus a short checklist, and pointing at the section phase 1 wrote. Q3
decided it is contributor-shaped and short. Q5 decides whether it joins
`tests/test_docs_line_wrap.py`'s `COVERED`, and this record says which way and
why.

## What this phase found

**Q5: it joins `COVERED`, and for a reason stronger than the rule that decided
it.** The rule is the file's own — a document wrapped from its first line goes
in at birth rather than waiting for a sweep — and the template was written
wrapped, widest line 77 columns against a limit of 88. The stronger reason is
that nearly all of this file is HTML comments, which `prose_lines()` does not
skip, and the box a contributor reads them in is GitHub's plain description
editor, which wraps nothing for them. Elsewhere the limit tidies a source
nobody reads unwrapped; here an unwrapped line is a line the reader actually
meets running off the edge.

**The guidance is HTML comments, and the headings are content.** Comments are
what a contributor reads while writing, and they are invisible in the posted
pull request — which answers Q3's stated risk directly. The risk was that
maintainers delete the template every time; a maintainer has nothing to delete
here, because nothing they leave in place renders.

**The moment is right, which is not obvious and is why it is recorded.** The
base-branch warning is useful only if it arrives before the base is chosen. On
GitHub's compare page the base dropdown and the description box are on the
same screen, so a contributor reading this template has the dropdown in view —
the template says *the dropdown to the left of this box* rather than naming a
page. It also names the Edit button, because the contributor who most needs
this has already opened against `main`.

**A3 is satisfied without a second hop.** The base-branch fact, why `main` is
refused, and which edit is the wrong one are all in the template itself.
`CONTRIBUTING.md` is cited after them, not in place of them.

**The identifier scan did not see the file until it was staged, and the first
run said so by saying nothing.** `tracked_text_files()` reads `git ls-files`,
so the first `bin/test tests/test_no_real_identifiers.py -q` — 5 passed — was
a run over a set that did not include the new file. A green run on a file
nobody opened is the failure mode this repository's whole evidence discipline
exists to catch, and it appeared here inside one phase. `git add` first, then
the run: 5 passed, over a set `git ls-files` now lists the template in.

**Both new pins were mutated, since a parametrized entry that never fails is
an entry that proves nothing.** Restored from bytes kept in the scratchpad,
never from HEAD; `cmp` identical afterwards.

| Mutation | Result |
|---|---|
| unmutated (`-k PULL_REQUEST` in `test_docs_line_wrap`) | 1 passed |
| a 150-column line appended to the template | **1 failed** |
| a real domain added to the template (`test_no_real_identifiers`) | **1 failed**, 4 passed |
| restored, both modules | 1 passed / 5 passed |

**No new test module.** `spec.md` S5 budgets two pins for this work item, and
both are spent — phase 1's section pin and phase 2's message pin. The template
is covered by two checks it joined rather than by a third written for it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — one new file and one line added to `COVERED` | none |
