# 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8bf488b1 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Bring spec D6's carriers into line, so that none still says the process
record waits for the fold:

- `docs/the-record-layout.md`: only the F3 paragraph and the one line under
  the `seal/specs/<work-item-id>/` table, because #728 and #730 edit other
  parts of it in parallel;
- `docs/release-checklist.md` §2b;
- `docs/review-handoff-protocol.md`;
- one appended *Decided when* section in `docs/one-root-by-lifetime.md` and
  its `.ko.md` edition;
- `skills/implement/SKILL.md`, `agents/framer.md`, the two docstrings in
  `survivor_check.py`, and `seal/README.md`.

Make the pins follow any test-pinned sentence. Write the changelog fragment
and the ledger fragment. Name `encoding="utf-8"` on every I/O added.

## What this phase found

**S11's grep, executed.** Every phrase spec D6 lists as stating a lifetime
was searched for again after the edits. Each one that described the process
record waiting for the fold, or staying for good, is gone from the carriers.
What the grep still finds is of four other kinds:

- the new wording itself, in the implement skill and the framer;
- the heading *Why the directory is not deleted*, whose section is about a
  deletion before the merge and is still true;
- two quotations of what `seal/README.md` once said, in the settle skill and
  module docstrings;
- *The fragment lives until the release that ships*, which is about a ledger
  fragment. `test_each_carrier_says_when_the_process_record_leaves` pins
each carrier twice, by its new wording and by the absence of the sentence it
replaced. Reverting the new wording under `mutation-check` turned each case
red. The first run left one copy of the `survivor_check.py` sentence
unwatched, because a single phrase matched both copies. Each copy now has its
own entry, and both breaks go red.

**`templates/seal-README.md` is a carrier the spec did not name.**
`tests/test_first_setup_asks_once.py` holds it byte for byte to
`seal/README.md`, so it took the same edit.

**One sentence of `docs/the-record-layout.md` is now stale, and this branch
may not edit it.** §*What is decided and not built yet* opens with *F1 is
built; the other three are not yet.* F3 is built now, and #728 and #730
build F2 and F4 in the same release. That sentence belongs to whichever of
the three lands last, so it is written into the closing memo and the
hand-back rather than edited here.

**The design record's new section follows its own convention.** Both editions
take one table with the same three rows, and `DATED_SECTIONS` in
`tests/test_settle_reads_before_it_removes.py` gained the pair, so
`test_both_editions_took_the_same_decisions` compares them. Removing the
Korean heading under `mutation-check` turned it red.

**The ledger, executed.** `evidence-check --strict .` reported 30 drifted
coordinates before the fragment was written. 29 were moved by this branch's
edits. Each of the 37 released rows citing them was read, and every claim
still holds: the edits added a filter, a flag, a section or a sentence beside
what each row describes, and changed none of it.
`evidence-check --reverify --into` then wrote the 37 `Re-read ·` rows and
stamped the eight new rows. The 30th drift,
`tests/test_a_record_precedes_the_fixes_it_commissions.py#test_the_declared_limit_names_what_escapes_with_the_words_unchanged`,
drifts at e141980a too, measured on a scratch clone. The re-read row the
tool wrote for it was taken back out, because nobody here read that row. So
`--strict` ends at 4,248 ok and 1 drifted, exit 2, and the one drift is not
this branch's.

**The checklist's wrap limit, executed.** One of this phase's edits left a
99-column line in §2b, which `tests/test_docs_line_wrap.py` caught. It was
rewrapped before the commit.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The record layout's sentence saying F3 is decided in principle and not built | the two-lifetimes paragraph that replaces it, in the same place |
| The implement skill's "closed at merge and kept" | the same tree line, which now names `settle --retire-process` |
