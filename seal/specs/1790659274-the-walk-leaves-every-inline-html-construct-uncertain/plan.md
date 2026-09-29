# Implementation Plan: the walk leaves every inline HTML construct uncertain (#673)

<!-- seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

The oracle first learns to see every kind of inline raw HTML. The walk then
calls uncertain every piece, and every later paragraph line, that starts
inside one. Last, the rider case gets back the half that asked the hasher its
own question. The round 3 report's drafts are the starting point for the
first two phases. This plan adds four things to them: the H4, H6 and H7 rows
and the single-quote row of H5, the renames, the nested read for pieces, and
the template's sentence.

## Technical context

- `hooks/blocks.py#leaves_open` (comment only), `#walk` (its `pending` state),
  `#walk_text` (its `inside` check). They are read at `3fc0c5bd`, which is
  byte-identical to the reviewed `8b1492aa` under `hooks/`, `tests/`,
  `.github/`, `skills/` and `templates/`.
- `tests/commonmark_oracle.py#_comment_lines` and `#_starts_in_a_comment`,
  and the `html_inline` wrapper `#_recording_html_inline`, which records
  offsets for every `html_inline` token already. Only the filters change.
- `tests/test_the_hooks_hide_what_a_renderer_hides.py#FOUND`, `#ALPHABET`
  (not touched) and `#test_the_walk_is_exact_somewhere`'s one-third floor.
- `tests/test_the_mode_question_is_asked_once.py#test_a_piece_inside_an_inline_comment_is_no_config_row`,
  which the new config case sits beside.
- `tests/test_a_rider_reaches_its_file.py#test_a_break_commonmark_does_not_honour_quotes_no_rider`.
  Its old region half is `8b1492aa^`'s, shown by `git show 8b1492aa`:
  `region_lines(CHECKER, "doc.md", '"# doc"', text)` and
  `not any("RIDER:" in line for line in kept)`.
- markdown-it-py 4.2.0's `common/html_re.py`, the source of the class table in
  `spec.md`.

**What breaks in six months.** A seventh kind of inline raw HTML is not
coming, because the list is closed in CommonMark §6.6. The live risks are
these three:

- **The floor.** Every sticky line is one the walk stops claiming. A later
  work item that adds openers to `ALPHABET` meets the floor, as rounds 2 and
  3 of F did. `FOUND` is where a shape goes, and `ALPHABET`'s comment already
  says why.
- **The parser moves.** A new markdown-it-py that tightens `\s` inside a tag
  to CommonMark's whitespace would stop forming H6 and H7 across the five
  control-character breaks. The oracle would then say "shown" there, and the
  walk is still uncertain, so nothing goes red. The pinned version is what
  keeps the `FOUND` rows meaning what they say.
- **Q1 answered "widen".** The link-attribute family then needs its own walk
  rule and an oracle that reads link and image attributes. Nothing here
  forecloses that.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| One left-to-right predicate for all six kinds, the comment included, replacing `leaves_open` | Exact where the two predicates overlap (`<? <!-- ?>`), but it changes `leaves_open`, which carries F's P2-1 anchor and the pending state's `-->` handling, for no claimed line anybody has measured | rejected: two predicates, OR-ed. Their union only over-reports, which errs toward uncertain |
| Follow a non-comment construct's closer onto later lines, as the comment's pending state does | A tag's closer is the first `>` outside a quoted value, so a value opened on one line and closed on the next needs quote state carried across lines. That is the kind of inline state F's frame removed on purpose ("it holds no inline state at all") | rejected: sticky to a blank line, a fence or a comment block |
| Keep `comment` and the two helper names, and say in the docstring that "comment" means any inline HTML (the round 3 draft) | A reader of `_starts_in_a_comment` believes the oracle asks about comments alone. That misreading is what let 🟡 2 stand: the oracle agreed with the walk by construction, and the name agreed with the narrow behaviour. The oracle's kind `comment` and the walk's kind `comment` (a comment block) would also mean two different things | rejected: `INLINE_HTML = "inline html"`, `_inline_html_lines`, `_starts_in_inline_html`. The cost is one dropped anchor in each of P1-2 and R1-1, which `docs/the-evidence-ledger.md` handles as "loses only the dead one" |
| The new shapes as `ALPHABET` lines | Executed by the reviewer: `test_the_walk_is_exact_somewhere` at 22,166 of 69,084, under its third; and an opener without its closer never forms inline HTML, so the lines tested nothing (61 passed with the base walk) | rejected: `FOUND` |
| The oracle's line test reads `html_inline` tokens at any depth too | A nested token's offsets are relative to the image description's own source, not the paragraph's, so the line numbers would be wrong. A line that begins inside HTML nested in a description is a whole line after a line that left HTML open, which the sticky state already calls uncertain, so no claim of the walk's depends on it | rejected for lines, taken for pieces, where the sentinel needs no offset |
| Also make a piece after `](`, `]:` or `![` uncertain (the link-attribute family) | Under the property's definition the walk is already exact there: both it and the oracle say "shown". Calling those pieces uncertain changes no answer the property checks, and it spends claimed pieces | rejected until Q1 is answered; Q1 is where it belongs |
| Leave `templates/config.md` alone because it is a template, not code | The sentence tells a person which contexts are "read as it was before", and after this work it would name one of six. §14 is that exact case | rejected: widened and pinned in phase 2 |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The oracle asks every inline HTML token (🟡 2).** `tests/commonmark_oracle.py`: the kind `inline html`; `_inline_html_lines` keeps every top-level `html_inline` token; `_starts_in_inline_html` finds the sentinel in an `html_inline` token at any depth; the module and `hidden_text` docstrings say *inline raw HTML*, and why a line is read top-level while a piece is read at any depth. `test_the_oracle_names_each_kind_it_hides` gains one row per construct in `spec.md` S1 and spells `inline html` where it spelled `comment`; `test_the_oracle_reads_the_text_not_a_readers_split` gains S2's assertions. No `FOUND` change yet. Ledger: P1-2 corrected and re-stamped, its `_comment_lines` anchor dropped with a dated note; a row in this work item's fragment for `_inline_html_lines` and `_starts_in_inline_html` | S1 and S2's new rows and assertions red with the oracle from `3fc0c5bd`, one run shown in the phase record (§15). Then `bin/test tests/test_the_hooks_hide_what_a_renderer_hides.py`, exit 0, with the base walk: the widening moves no answer on the existing corpus (Q5) | |
| 2 | **The walk calls a piece, and the paragraph after it, uncertain inside any inline HTML (🟡 1).** `hooks/blocks.py`: `INLINE_HTML`, `TAG_END`, `leaves_html_open`; `walk`'s sticky state; `walk_text`'s check asking both predicates; the module docstring's *Nothing inline is modelled* paragraph and third uncertain bullet, and `walk_text`'s docstring. `hooks/config.py#hidden_lines`' docstring. `templates/config.md` §*Broad gate*'s list of contexts read as before, and S10's pin. Cases: S3 (five openers × eight breaks), S4, S5. `FOUND`: seven documents, per `spec.md` §*The class, enumerated*'s case column. Ledger: P2-1 and R1-1 corrected and re-stamped, R1-1's `_starts_in_a_comment` anchor dropped with a dated note; rows in this work item's fragment for the new units and cases | S3 red at `3fc0c5bd` for each opener, and S4, S5 and S10 red there on their first halves; the new `FOUND` documents red with the base walk and phase 1's oracle (half 2). Then `bin/test` over the property, config, routing and rider modules, exit 0. Q2's count and Q3's corpus measurement recorded in the phase record | |
| 3 | **The rider case asks the hasher its own question again (⬜ 4).** `test_a_break_commonmark_does_not_honour_quotes_no_rider` gets back its old region half over `text` (`region_lines` keeps no `RIDER:` line), directly after the `riders_in` assertion and before `region = (`. Its docstring says the case asks the hasher twice: once on the round 1 shape (a fence run after the break) and once on the merge's shape. Ledger: R1-1's anchor on this case re-read | the old half red under a `region_lines` mutant that walks the reader's split, all eight breaks, and green at HEAD, as the reviewer showed; `bin/test tests/test_a_rider_reaches_its_file.py`, exit 0 | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/1790659274-the-walk-leaves-every-inline-html-construct-uncertain/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
**Re-read the column after any rebase**, or it names commits that resolve in
one clone and nowhere else.

## Operational impact

None to deploy: no migration, no environment variable, no new dependency (the
suite's markdown-it-py pin is unchanged), no new message, flag or exit code.
One reading changes. `seal/config.md` files in the shapes of `spec.md` S3 read
as undeclared, so `mode-gate` asks and `broad-gate` refuses there. S8 measures
that no committed file holds such a shape. The changelog fragment
(`seal/specs/1790659274-…/changelog.md`) is the builder's, and says this in a
person's words.
