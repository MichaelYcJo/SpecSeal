# the hooks and the rider check read fences and comments by one rule (#667, #658) — questions for the planner

<!-- seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**One row needs a person: Q1.** It blocks phase 1, and phase 1 comes first on
purpose, because the lesson of `1790635413` is that the readers were built before
anything independent could check them. Every other row is a measurement or the
work's.

## Decided from the tree, so nobody reopens them

The spawn prompt left these open. Each is answered here with the grounds a
reviewer can open.

| # | What was left open | The answer | Grounds |
|---|---|---|---|
| D1 | What reading holds for every shape the three rounds executed | Two block constructs by CommonMark's block rules (a fenced block, a line-start comment block), closed only; no inline state; an uncertain line keeps the base reading; a construct that never closes is not one | `spec.md` §*Why three rounds traded one direction for the other*: every finding traces to inline state or to an uncertain state resolved toward one side. §*The shapes*: every executed shape gets an answer no worse than the base |
| D2 | Whether the hooks need comment state at all | Yes, and only the block kind | A fence-only rule opens a fence on a fence line inside a header comment and hides the table (round 2, 🟡 2's shape). 18 of 26 committed `routing.md` files, the template and `seal/config.md` open with such a comment (`plan.md` §*Technical context*) |
| D3 | Whether a mid-line `<!--` hides anything | No; it is not modelled, and the lines it might hide keep their base reading | It cannot hide a block start (CommonMark decides blocks before inlines), so ignoring it moves no construct. All three rounds lost ground by modelling it. The residual is named in `spec.md` §*Scope* |
| D4 | What a fence or comment that never closes does | Nothing: it is not a construct. `hooks/config.py` keeps hiding the lines below an unclosed fence because its base does; the routing reader and the rider check read through | The constraint's first direction. This reverses `1790635413`'s pinned `routing.parse("```\n" + two_axis_text()) is None` and its "unclosed to the end" rider rule, and keeps its `lone` case as it pinned it rather than as round 3 proposed |
| D5 | A table wholly inside a closed fence or comment (R2, R9) | Not a declaration, not a config table | Both directions of the constraint meet there. `hooks/routing.py`'s docstring breaks the tie: "Everything here fails toward 'no declaration'", and `hooks/config.py`'s says the same of *nothing is declared*. The ask that follows is the one every non-parsing `routing.md` already gets |
| D6 | Which oracle | A CommonMark parser that shares no code or model with the walk, reading only whether a line is hidden, never table grammar | Round 3: "The oracle cannot catch this, because it is built the same way." The tree's own reference reading (`tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules`) models comments as inline raw HTML, which is the wrong model for a comment block. Which parser, and whether the suite may take one, is Q1 |
| D7 | Whether the three readers share one implementation | Yes: one stdlib-only module under `hooks/`, imported as a sibling by both hooks and loaded by path by the rider check | Hooks never import `skills/`, and nothing asks them to. Skills already load `hooks/config.py` and `hooks/routing.py` by path (`broad_gate.py`, `seal.py`, `chain_check.py`, `survivor_check.py`), so a `hooks/` module reaches every reader. `hooks/routing.py`'s docstring gives the reason against copies |
| D8 | Whether any reader is better left as it is | None of the three. The rider check's change is latent today (no markdown rider in the tree) and small, and its base fails loudly on a quoted rider, at exit 2 in CI | #667 names all three. The rider change adds one condition to one walk and removes an invented alarm, which is the direction `rider_check.py`'s own docstring refuses to accept |
| D9 | Which shapes should refuse loudly | None newly | Every ambiguous shape has the base reading available as the floor. The release scripts refuse because they write the text their own reader reads; here only `seal.py#write_row` writes, and its read-back guard already refuses |
| D10 | Whether `live_lines` and the readers #584 moved join this walk | No | They answer a question whose safe direction is the opposite one (a marker is safe parked; a hook row is safe at its base reading), and they ship in #663 |
| D11 | Whether the commit gate should name a hidden declaration | Out of scope | The generic message already exists for every non-parsing file, and no committed declaration has the shape. Named in `spec.md` §*Scope* with its answerer |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | May the test suite take `markdown-it-py`, pinned to one version, as a test-only dependency, so the oracle is a CommonMark parser that shares nothing with the walk? Why the tree cannot answer it: `CONTRIBUTING.md` §*Running the checks* states "The suite needs only `pytest`", and what CI installs from a package index on three platforms is a supply-chain choice somebody is accountable for. No document delegates it | a person — the repository owner | (a) **Yes.** `bin/test` and CI install it; an adopted `.venv` gets it the way `run_tests.py#add_xdist` gives pytest-xdist; the `CONTRIBUTING.md` sentence changes. The property test runs over the shape table AND a seeded generated corpus, which is what finds a combination nobody listed. The gates stay stdlib-only. (b) **No; vendor the CommonMark specification's examples for §4.5 and §4.6 as test data.** No new package. Each rule is exercised once and the corpus cannot be generated, so a combination of a stray opener, a fence and a comment (every round's kind of finding) is checked only where the shape table lists it. The examples' licence has not been read here and would need reading. (c) **No independent oracle.** The shape table alone, which is the arrangement that let three rounds' gaps through | none. Phase 1 waits for the answer, and phases 2 to 5 depend on phase 1 | ✅ (a), answered 2026-09-29 by the repository owner in the orchestrating session: `markdown-it-py`, pinned, as a test-only dependency |
| Q2 | Does the oracle give the *Renderer* column of `spec.md` §*The shapes* on every row, and does CommonMark decide the two block constructs as `spec.md` §*The reading* states (§4.5, §4.6 type 2, block structure before inlines)? Why the tree cannot answer it: the frame cites the specification from outside the tree and derived the column by reading it; nothing was parsed | a measurement — phase 1's helper over the shape table | (a) it agrees: build on it. (b) a row disagrees: the oracle wins over the frame's reading, `overview.md` records the divergence, and that row's *Expected* answer is re-derived by `spec.md`'s rule (never leave both readings) | (a) | ✅ (a), measured 2026-09-29 in phase 1: `markdown-it-py==4.2.0` gives the column on all 32 shapes in `tests/block_shapes.py`, and `test_the_oracle_gives_the_frames_renderer_column` holds it |
| Q3 | Do the committed files read the same at `3911a8cf` and at HEAD: every `routing.md` and the template through `routing.parse` (R10), every tracked `.md` through `config_rows` (S14), every file under `RIDER_ROOTS` through `comment_blocks` and `rider_check.py`'s exit code (K8)? Why the tree cannot answer it: it is two runs of each reader over the corpus, and the frame runs nothing | a measurement — phases 3, 4 and 5, one reader each | (a) no file differs: record the counts in each phase record and the changelog fragment. (b) a file differs: it holds a shape the table does not list; add the shape to the table with its three columns before closing the phase | (a). By `grep`: no committed `routing.md` has a fence, a mid-line opener or an unbalanced comment, and no markdown file under the rider roots carries a rider | ✅ (a), measured 2026-09-29: S14 in phase 3, 519 tracked `.md` files, 4 with config rows, 0 differ; R10 in phase 4, 27 declarations (one more since #660's merge) and the template, all parse at `3911a8cf`, 0 differ; K8 in phase 5, 241 files under the rider roots, 20 blocks, 0 differ, exit 0 with either script |
| Q4 | Can the walk call more contexts exact than `spec.md`'s minimum — a construct indented one to three spaces outside any list, HTML block types 1 to 6 modelled by their own start and end conditions, block quotes? Why the tree cannot answer it: each widening is exact only if the oracle agrees on documents that hold the context | the work — phase 2 | (a) widen one context at a time, each with the context added to the generated corpus's alphabet and property half 2 green. (b) keep the minimum | (b). Nothing in today's hook files needs a widening | ✅ (b), decided 2026-09-29 in phase 2: nothing called exact beyond the minimum, and the uncertain set widened in four places the property found (`phases/phase-2.md`; `overview.md`'s first divergence row) |
| Q5 | The new module's name and API, whether the delimiter pattern moves out of `hooks/config.py` or is read from there, and the wording of `broad-gate`'s commented-row sentence. Why the tree cannot answer it: a factoring and a sentence, decided where they are pinned | the work — phases 2 and 3 | Any shape that keeps one walk for all three readers, keeps `hooks/config.py#fence_map` and `#unfenced` for their callers, and says in `broad-gate`'s sentence that the row is inside an HTML comment, is not absent, and ran nothing | a sibling of `optin.py`; the pattern moves and `hooks/config.py` re-exports it | ✅ decided 2026-09-29. Module and API in phase 2: `hooks/blocks.py` with `walk`, `Walk.hidden(base)`, `fence_only` and the delimiter rule; the pattern moved and `hooks/config.py#FENCE` names it. The sentence in phase 3: the row is "written inside an HTML comment", "not absent and it is not in a code fence", and "Nothing ran." |
| Q6 | How this branch meets #663 and #660, which edit `unverified_check.py#fence_opener`'s docstring, `tests/test_unverified_rows_close.py`, `tests/test_a_rider_reaches_its_file.py`, `hooks/routing.py` and `seal.py`. Why the tree cannot answer it: which lands first is not known at framing time | the work — the phase that meets the conflict | Resolve hunk by hunk. `fence_opener`'s reader lists must name this walk after the merge and nothing #663 reverted; the parity cases keep holding the delimiter copy wherever it lives | merge `release/v0.16.0` in when either lands | ✅ met 2026-09-29: #660 merged clean in phase 3 (`e235453a`); #663 conflicted in `fence_opener`'s docstring alone and was resolved hunk by hunk in phase 5 (`72d03c43`), keeping its lists and rewriting its two hook-reader bullets to name the walk. #668 and work item E had not landed by the hand-back |
| Q7 | How large a generated corpus the property test can run within the suite's time, on the slowest CI leg. Why the tree cannot answer it: it is a timing | a measurement — phase 2 | Any size that finishes inside a budget the phase states; seeded, so a red is reproducible | the largest that runs in a few seconds on one core | ✅ measured 2026-09-29 in phase 2, on macOS (the slowest CI leg, Windows, is not measured here): 6,000 documents of up to 16 lines, seed 667, about a third of a second per property case; 20,000 of up to 24 lines take about 1.1 s. The number is `CORPUS_SIZE` |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
