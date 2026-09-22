# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — overview

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

📋 implement applied
· spec:     `seal/specs/1790039346-…/{routing,spec,plan,questions}.md` in full;
            `seal/specs/1790027178-…/rounds/round-3-report.md` and the
            parent's `overview.md`, `changelog.md` and `phases/phase-1.md`;
            `CLAUDE.md` §*a change writes fragments, never the shared file*
            and §*The goal a design is chosen against*; `CONTRIBUTING.md`
            §*House rules* (the re-read rule); `seal/config.md`;
            `seal/follow-up.md` in full; `skills/agent-contract/SKILL.md`;
            `templates/sdd-phase.md` and `templates/sdd-overview.md`
· evidence: `seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`,
            rows R1, R2, R6, R7, R9 and R10; S1 and S3 re-read in
            `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`
· verified: **executed** — the two modules each phase touched, per phase, and
            `tests/test_chain_hooks.py` with
            `tests/test_a_script_says_which_interpreter_it_needs.py` at phase
            3; every new case red against `3cdfd8ad` or under a named mutation
            before it was committed; five mutations applied alone and restored
            from a byte copy; `bin/settle` at the tip; `ruff check` and
            `ruff format --check` over the four Python files; the reader
            imported and exercised on `/usr/bin/python3` 3.9.6;
            `evidence-check --reverify` over the two fragments and
            `evidence-check --strict .`. **read** — A10, the four docstrings.
            **unverified** — the two rows below

## Why this work exists

**This work item ran five review rounds and the fifth was the last the chain
allows, so the fix below has no reviewing round after it.** That is a real
gap rather than a formality: every earlier round found a defect the previous
fix pass believed it had closed, four of them removing a work item's
directory at exit 0, and the reader that catches that class is the one this
pass rewrote. What stands in a round's place is named in §*Not verified* —
which claims rest on this session's own execution and nothing else.

Round 3 of #458's chain found the rule *a line stops being live two ways*
given to the fold reader in full and to `settle`'s ledger reader by half, and
found that the obvious way to carry the other half over loses three real
sections of `seal/ledger.md`. This gives the rule one owner —
`unverified_check.py#live_lines`, ONE scan carrying fence, comment and
code-span state together — and makes both readers ask it, closing the five findings that
round deferred.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A2's fixture shape | Spec A2: *a commented-out draft holding a marker and a coordinate row · Then the draft's coordinate is attributed to no work item*. Built with the row after the marker, the row landed in `gamma`, the section that was open | The draft's row sits BEFORE its marker; a second row after the marker is pinned as landing in the open section, with the reason in the case | HTML comments do not nest, so the marker's own `-->` closes the draft and the row after it is live again. That is `comment_scan`'s rule, pinned at `seal/ledger.md:80` and by the c-3 shape in the comment-shape family; the frame refused touching that scanner, and the spec's *Then* is true of a row the comment actually encloses |
| The frame's own coordinates | `spec.md:30` cites the parent's S1 and S3 anchors with the file's basename alone — `unverified_check.py` and `settle.py`, no directory — and `evidence-check --strict .` reports both BROKEN, *file not found — same name at skills/verify/scripts/…* | Left as written and handed back | `spec.md` is the framer's file and not on the builder's list (`agents/smith.md`, §6). The repair is the two full paths; the eleven NOT-IN-TREE reports from the same run, for names the frame used before they existed, closed themselves when phase 3 landed them |
| The equal-length span rule has a case | `plan.md` names no case for `blank_code_spans` itself; the loose regex is recorded as acceptable | A parametrised case of five shapes, two red under the loose regex | A property the plan chose over an alternative it kept acceptable is exactly the property the next simplification takes back silently; a case is cheaper than the round that would find it (NAME NOT IN TREE) |
| The fold gate's failure direction | `spec.md` G3 and `plan.md` §*Operational impact*: *fewer lines live … rather than a directory removed with nothing absorbing it* | The direction runs both ways, and the narrowing's half is the other one | Round 2's finding 1, executed: a `docs/` draft quoting the closing delimiter above a marker took `settle --retire` from exit 1 *nothing to retire* to exit 0 with the directory removed. A span the predicate spares cannot hold an opener, so the only delimiter it can restore is a closing one and a closing one can only end a comment sooner — liveness is monotonically non-decreasing. The behaviour is kept and `c-8` is the pin; what was owed is the disclosure. **Corrected again 2026-09-22 after round 3's finding 2**: this row used to ground the direction on *what the HTML rule says*, and that is false — no state-free pass can be the interleaved reading of comments and code spans, and round 3's finding 1 was the residue. The pass stops at a span's first closing delimiter and prefers to park rather than to read live; fuzzed over 40,000 documents, 0 lines live where the reading parks and 132 parked where it reads live. `blank_code_spans`'s docstring carries the contract. `plan.md` is corrected here; **`spec.md` G3 is the framer's file and is named in the hand-back for the orchestrator**. **Superseded 2026-09-22 by round 4's fix pass**: the stateless pass this row argues about is gone, and with it the expensive-against-cheap trade and both figures. `live_lines` is one scan carrying all three states, so there is no approximation left to state a direction for — what replaces the trade is agreement with an independently written character-level reading, in the tree as `test_the_scan_agrees_with_a_character_level_reading`. The row is kept because it records what was decided at rounds 2 and 3 (NAME NOT IN TREE) |

## The dry run — A8, Q1

Executed 2026-09-22 at `7605feb4`, `bin/settle` and nothing else, exit 0 read
with `echo $?` and not through a pipe:

```
released and unfolded: 81 work items in 37 segments, 16 ungrouped, 0 skipped
```

Unchanged from `3cdfd8ad`. Behind it: 83 distinct ids sectioned by the
fence-only reading, 80 by the naive closure, 83 by the composed rule; 787
lines not live under the naive rule and 761 under the composed one. The
framer's figures, reproduced.

**The corpus figures, re-derived at round 5's fix pass, and which reading of
them is right.** `seal/ledger.md` carries **761 not-live lines, 94 marker
occurrences and 83 unique ids**, and all 94 of its markers are live. The
eleven corpus files together carry **903** not-live lines — 761 from the
ledger and 142 from `docs/`, the fenced lines the single scan began calling
not-live at round 4, where the three-pass reader had blanked them to `""` and
called them live. So round 5's **903 is a real figure mis-attributed**: it is
the eleven-file total, not `seal/ledger.md`'s. Its 102 marker occurrences and
85 ids reproduce on no file set tried — ledger, fragments, `docs/`,
`CHANGELOG.md`, live-only or counting parked markers too. The earlier rounds'
761 / 94 / 83 for `seal/ledger.md` is the correct reading, and
`test_the_three_named_markers_are_live_in_this_repositorys_ledger` and
`test_no_section_of_this_repositorys_ledger_loses_a_coordinate` now hold both
halves of it as cases rather than as figures in a record.

## Not verified

| Item | Who must answer |
|---|---|
| the broad gate — `bin/test -q && uvx ruff check . && uvx ruff format --check .` over the whole tree. Each phase ran the modules it touched and the two that load the reader; nothing broad was run, because a broad run with an edit after it is spent rather than banked | the orchestrating session, which spawns the sealer after the review rounds settle |
| **Everything the last two fix passes claim rests on this session's own execution, because the chain's cap was spent at round 5 and round 6 was read by nobody after it.** Specifically: that the two readings and their AND behave as the seven-shape family asserts; that `_paragraph_ends_at` stops where markdown stops and nowhere else; and that the corpus figures below were re-derived rather than carried. **Round 6 found this row naming the safety fuzz as what watches the block list when the fuzz could not see it** — its oracle shared the reader's two indentation bounds, and its generator built none of the shapes the rule can be wrong about. Both are repaired and the watcher was made to fire before it was trusted: reverting each of the four block rules alone now reddens `test_the_scan_never_reads_live_what_the_format_parks`, and an indented delimiter reddens it and the seven-shape family together. What is still unwatched is a rule markdown has that neither the reader nor the oracle names, which no case can report because both would be silent on it | the orchestrating session, which says it will verify the seven shapes and the corpus, and the sealer's broad gate |
| ✅ `evidence-check --strict .` at exit 0 over this branch | closed 2026-09-22: executed at round 6's fix pass, exit 0 read directly, ledgers `1439 ok · 0 drifted · 0 broken` and the records arm `0 refused`. **This row described an exit 2 that had stopped happening and named a `spec.md:30` that now holds a different row** (round 6, finding 9); the two shorthand coordinates it was written about were corrected by the orchestrating session at `6d8ebaae`, and every later refusal this branch caused was answered in the pass that caused it |

## Not done

- ~~**No case for a code span that crosses a line break**~~ — **CLOSED, and
  the closing was completed by round 5's fix pass rather than round 4's.** Q2
  decided the multi-line limit would be a sentence rather than a case;
  round 1's finding 2 then found the sentence's stated direction false,
  because a multi-line span holding a MARKER was read as a fold record and
  the directory removed at exit 0. The door was left open on the grounds
  that closing it needs span state carried across lines, which no
  formulation of the three-pass composition could hold. The composition is
  gone: `live_lines` is one scan carrying fence, comment and code-span state
  together, so a multi-line span falls out of it. Executed — a marker
  between the two halves of a code span returns the empty set, and a
  multi-line comment answers the same way it always did. The limit, its
  stated direction and the census that softened it are all gone with the
  function that carried them.
- **The third quotation, markdown's indented code block, is answered rather
  than closed** — round 1's finding 3. A fragment showing its example row
  indented has that example counted as its own coordinate; widening
  `blank_fences` would move `readable`, `check_text`, `round_record.py` and
  the review-history guard at once — measured 2026-09-22, one such widening
  reddens `test_a_continuation_that_looks_like_an_opener_is_still_joined` in
  `tests/test_the_record_is_generated.py`, a record reader with no stake in
  this rule. **Corrected after round 2's finding 3:** this bullet used to
  name `tests/test_chain_hooks.py#reader_blanking_passes` as the refusal, and
  that case stays green under the widening — it reads the calls `readable`
  makes by name, which a widened `blank_fences` leaves unchanged. It refuses
  a pass ADDED to `readable`, a different alternative.
  `coordinates`'s docstring names the door and
  `test_an_indented_example_row_is_counted_and_the_reader_says_so` pins the
  decision, so a later widening is told what this one chose.
- **`evidence_check.py`'s own readers are untouched.** `seal/follow-up.md`'s
  two rows on that module are the same class one module over and keep their
  answerers; `live_lines` is what a fix there would reuse.
- **`.github/scripts/fold_ledger.py#demote`'s fence tracking is untouched.**
  Not shipped, and its own rider says what it misreads.

## Fed back into the spec

none — neither question stated a rule; Q2's answer landed in a docstring.
