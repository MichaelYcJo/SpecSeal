# 1790683267-a-rider-read-ends-where-the-hasher-cuts — review round 1

| Field | Value |
|---|---|
| Target SHA | 0abe93a712a4d1d492407b4b20f69633a63f4763 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #683 — https://github.com/MichaelYcJo/SpecSeal/pull/683 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 over the build range `f7b7d247..0abe93a7` at HEAD `0abe93a7`, against `346b4af7`. Spec compliance first, then quality. The pushes:
- the class and not the two shapes, both ways, by the reviewer's own reader-against-hasher differential;
- whether anything depended on the removed text path and on `gfm_places`' second value;
- whether the `-->` rule the frame left out of scope is a defect, and whose;
- the interpreter floor;
- whether the ledger rows the build wrote, re-read or corrected are true.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `comment_blocks`' docstring says a mid-line marker piece is a rider exactly where its GFM line opens a comment; a line continuing an HTML comment an earlier block left open is read too | `.github/scripts/rider_check.py:307` | open | executed: the continuation probe reads the piece after the break as a rider at HEAD, and the hasher cuts that line; the behaviour is right, the sentence is narrower |
| ⬜ 2 | G13's first clause, this item's `Re-read` note on G13 ("holds as written") and P5-1's #682 correction ("nowhere else") state the same narrower rule | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md` G13; `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md` P5-1 | open | a correction to paperwork, outside `Needs a fix`; the same counterexample as ⬜ 1, at HEAD and at the base; K1 states the exact rule |
| ⬜ 3 | `region_lines`' "No TEXT" comment explains an argument `comment_blocks` no longer takes | `.github/scripts/rider_check.py:476` | open | read; S2 already takes this item's `Re-read` note, so a re-stamp is the whole cost |
| ⬜ 4 | the rider's oracle case drives `quoted_lines(lines, text)`, which no shipped caller uses; the reader's GFM-lines path has no oracle case | `tests/test_the_hooks_hide_what_a_renderer_hides.py:753` | open | executed: the reader's path through the same oracle and corpus, 6,066 documents, 5,183 with a break, never leaves both readings |
| ⬜ 5 | `Rider.where` prints the `str.splitlines` piece number, which runs ahead of the GFM line below one of the eight characters | `.github/scripts/rider_check.py:374` | open | read; older than #664 and outside this item's class; see Deferred |
| 🟢 | K1 holds: every piece of every rider read lies in one block the hasher returns, and every marker piece in a cut block starts exactly one rider | `.github/scripts/rider_check.py:377` | confirmed | executed: 120,000 generated texts, 0 at HEAD against 20,154 at the base; end to end on 6,971 texts, 0 drifted after `reverify` at HEAD against 8 at the base |
| 🟢 | nothing changes for a text without the eight characters | `.github/scripts/rider_check.py:377` | confirmed | executed: 64,482 generated texts and the 25 tree files, identical riders; `inferred_anchor` identical on 43,145 riders; the tree reads `18 ok · 0 drifted · 0 broken` with either script |
| 🟢 | the removed text path and the second value of `gfm_places` had no other reader | `.github/scripts/rider_check.py:236` | confirmed | read: every call site in the tree; executed: the three rider modules pass |
| 🟢 | the `-->` rule is not a defect in the rider reading, and not this item's class | `.github/scripts/rider_check.py:341` | confirmed | executed: BROKEN with a space at both versions and with U+2028 at HEAD, and the CommonMark parser shows the stamp line as paragraph text; the reader and the hasher share the rule |
| 🟢 | the shipped script stays on the interpreter floor | `.github/scripts/rider_check.py:410` | confirmed | executed: the floor case and ruff; read: no `zip(`, `pairwise` or `.UTC` |
| 🟢 | the new cases were seen red at the base reader | `tests/test_every_reader_ends_a_line_where_gfm_does.py:1024` | confirmed | executed: 32 red against the base `rider_check.py`, the two shapes under all eight characters in both cases; the rider-to-block-end mutant turns 8 red |
| 🟢 | K1, K2, S2, S3 and R1-1 are true at HEAD, and the checks agree | `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md` | confirmed | executed: `evidence-check --strict` exit 0, `correction-check` exit 0, `survivor-check` exit 0 with the exemptions; G13 and P5-1 are true apart from ⬜ 2 |

## Paste-ready fixes

```python
    **LINES are GFM lines, and this is the one block rule** (#682). Both
    callers hand over `gfm_lines` of the file: `region_lines` cuts the blocks
    out of the region it hashes, and `riders_in` splits the same blocks at
    every `str.splitlines` piece carrying the marker. So a marker piece
    standing mid-line after a U+2028 or a form feed is a rider exactly where
    its GFM line lies inside a block this returns -- a comment it opens, or
    an HTML comment an earlier block left open -- which is where the hasher
    cuts it. Nothing here reads pieces: a reader that walked them by a second
    statement of this rule parted from the hasher in each of #664's three
    rounds.
```
```text
**Corrected 2026-09-29 in round 1 of work item 1790683267 (#682):** "opens a comment" is narrower than the reader. A mid-line marker piece is read wherever its GFM line lies inside a block `comment_blocks` over GFM lines returns, which includes a line continuing an HTML comment an earlier block left open at a marker; K1 states the rule. This was so at `346b4af7` as well.
```
```python
    lines = checker.gfm_lines(text)  # the lines `resolve_unit` numbered (#664)
    # GFM lines, the ones `riders_in` hands `comment_blocks` too, so the blocks
    # cut here are exactly the blocks the reader reads (#682).
    blocks = comment_blocks(lines, rel)
```
```python
    blocks = riders.load_blocks()
    wrong = []
    for doc in CORPUS:
        text, lines = as_read(doc)
        hidden = set(oracle.hidden_text(text))
        new = riders.quoted_lines(lines, text)
        bad = leaves_both(new, set(), hidden, len(lines))
        # What `riders_in` runs since #682: whole GFM lines, mapped to pieces.
        quoted = riders.quoted_lines(blocks.gfm_lines(text))
        places = riders.gfm_places(blocks.gfm_lines, text)
        read = {k for k, number in enumerate(places) if number - 1 in quoted}
        bad += leaves_both(read, set(), hidden, len(lines))
        if bad:
            wrong.append((lines, bad))
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_every_reader_ends_a_line_where_gfm_does.py`, `tests/test_a_rider_reaches_its_file.py`, `tests/test_the_hooks_hide_what_a_renderer_hides.py`, `tests/test_a_script_says_which_interpreter_it_needs.py`, `tests/test_a_record_states_what_the_tree_has.py` at `0abe93a7` | 446 passed, exit 0 |
| the two new cases with the base `rider_check.py` put in place, then restored | 32 failed, 32 passed: the two #682 shapes under all eight characters, in both cases |
| the mutant `ends = [inside[-1] + 1] * len(starts)` over the three rider modules, then restored | 8 failed, all in the class case |
| a reader-against-hasher differential, generated texts in `.py`, `.yml` and `.md`, HEAD and the base loaded side by side | 120,000 texts, 55,518 with one of the eight. The hasher was the same at both in all of them. HEAD: 0 texts break the property, over 135,604 riders. Base: 20,154 texts. Without the eight, 0 of 64,482 texts differ between the two, and every difference is on a text where the base broke the property |
| the same generator end to end, `reverify` then `check` then `reverify`, in a temporary tree with raw CRLF and CR ends | 6,971 texts per version. HEAD: 0 drifted after `reverify`, 0 rewritten on the second, 0 raised. Base: 8 drifted and rewritten again |
| `inferred_anchor`, HEAD against base, on Python riders both read alike | 43,145 riders, 0 differ, 1,065 named |
| the tree's marker-carrying files, HEAD against base; `rider_check.py --root .` with each script | 25 files, 18 riders, 0 differ; `18 ok · 0 drifted · 0 broken`, exit 0 with each |
| the reader's GFM-lines quoting against the CommonMark oracle, on the oracle case's corpus | 6,066 documents, 5,183 with a break, 0 leaving both readings |
| the `-->` shapes at base and HEAD, with a space and U+2028, through `reverify` and `check`, and rendered | see the table under Push 3 |
| a marker piece after a break on a line continuing an open HTML comment | cut `[(2, 2), (3, 3)]`; HEAD reads the piece after the break as rider (4, 4) and puts the piece before it in no rider; the base read that piece into the first rider, across two blocks |
| `bin/evidence-check --strict .` | `3082 ok · 0 drifted · 0 broken`, exit 0 |
| `bin/correction-check --range 346b4af7...HEAD` | 1 merge examined, no marker dropped, exit 0 |
| `survivor_check.py --range 346b4af7...HEAD` with every `survivors.md` passed through `--exempt` | 2 exempt, exit 0; without the exemptions exit 1 on the same two places |
| `ruff check` and `ruff format --check` on the two changed Python files | clean, exit 0 |
| the broad gate: the full suite, repository-wide lint and typecheck over this branch | not yet — not run by this round. It is the sealer's, and it comes due now, since nothing here needs a fix |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 5 — a rider's printed location is a `str.splitlines` number, older than #664 | not placed: a candidate for its own issue | the orchestrator, who files it or answers that it stays as is |
| the `-->` shape's sentence "no verification stamp" when a stamp sits outside the comment (Push 3) | not placed: a message improvement, outside this item's class | the orchestrator, if the owner wants the message to name the case |
