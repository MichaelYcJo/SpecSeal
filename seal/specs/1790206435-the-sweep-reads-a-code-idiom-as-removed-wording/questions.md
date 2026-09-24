# the sweep reads a code idiom as removed wording — questions for the planner

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**What the tickets left open and the tree answered**, listed so nobody
reopens it here; the grounds are `spec.md` §*Judgments the tree answered*,
numbered the same way.

1. Which of #543's three candidates — the reader; the other two cannot pass
   the module's founding cases.
2. The class is `.py`, by the tree's census; other file kinds are named
   under `spec.md` §*Out*.
3. A `#` comment keeps its `#`, so a comment block stays one sentence per
   line and phase 1 is subtractive.
4. A released section is read off its heading, not the file whole; a
   gathered fragment off its marker in `CHANGELOG.md` at the tip.
5. #439's *choosing is the repository owner's* — the instance the ticket
   quotes is retired with its directory, and `seal/ledger.md` R7 already
   carries the ticket's first option as a dated note beside the figure. What
   a record states once its range stops resolving is written as judgment 5.
6. An unresolved declaration is judged by the second anchor before it is
   printed; the wrong allow is empty.
7. #526's split is a move, silent by construction; Q5 below is the probe.
8. Existing `survivors.md` rows of the two classes stay, uncounted until Q3.
9. The fixture is the four squash commits on `main`, skipped when absent.

No row below is a person's. The build does not wait on this file.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | After phase 1, what do the two founding survivors score — #269's pin over `fixture/survivor-pin-left-behind` (1.89 today) and #267's R3 over `fixture/survivor-class-left-standing` (1.79 today) — and is anything beside them named? Dropping code carriers raises the weight of every phrase they held, so the scores can only move up; a new name on either range is a false positive the reader let through | a measurement — the two existing cases, and their reports read in phase 1 | Both higher or equal and nothing new named: recorded in `phases/phase-1.md`. Something new named: it is a defect of the reader, fixed in phase 1 before the case is planted | the scores are recorded, whatever they are | ✅ measured 2026-09-24 at `476af109`: 2.00 for #269's pin and 1.89 / 1.78 for #267's two rows, identical before and after; nothing new named. The 1.89 and 1.79 the question quotes were already stale (`FLOOR`'s calibration-time figures). The pin's line moves 447 → 450, the literal's own line (`phases/phase-1.md`) |
| Q2 | After phase 1, do the four real ranges of `spec.md` §*The measured state* report exactly the prose coordinates they report today, at the same places? A 5 → 1, 0 5 → 4, C 2 → 1, B 9 → 9 is the expected shape; a prose coordinate that appears or disappears is the weighting moving, which S6's ledger row measured as 1.69 → 1.79 once before and which this row exists to see | a measurement — the S6 case's own output, read in phase 1 | Unchanged: the case pins the exact set. Moved: the case pins the new set and `phases/phase-1.md` names each moved coordinate with its score before and after | the case pins what the run shows, and the record says which | ✅ moved, at one coordinate: A 5 → 1, 0 5 → 4, C 2 → 1 as expected, B 9 → **8** — `seal/ledger.md:2053` was scored at 2.47 against a docstring joined to three assert literals by code, and one literal per sentence its best source is one run at 1.00. The case pins the new set; every other coordinate stands and every score rose or held (`phases/phase-1.md`) |
| Q3 | How many `| Path | Quote | Grounds |` rows across every `seal/specs/*/survivors.md` in the tree are of the code-idiom class or the released-changelog class? #307's first *Not verified* item asks it. The rows are not edited either way (judgment 8); the count says how much of the exemption writing of the last two releases these two phases would have spared | a measurement — one read of the four files' rows against their grounds cells, in phase 2 | The count, split by class, goes in `overview.md` and the pull request body; nothing is deleted | the rows stay | ✅ read 2026-09-24 at `93acc277`: of 56 path rows in seven files, **17** code-idiom and **3** released-changelog — 20 rows, 36 per cent; three more files hold only a range row. Per file in `phases/phase-2.md`; the rows stay |
| Q4 | The shape of the changelog exclusion in code: `records_a_past_state` gains a parameter carrying the gathered set, or a sibling predicate is applied beside it in `corrected` and `corpus`; and where the released-region blank sits — a text step beside `blank_struck` keyed on the path, or inside the reader phase 1 adds. `PREDICATE` and `EXCLUSIONS` in the test module follow whichever shape lands | the work — phase 2 decides it and `phases/phase-2.md` records it | A sibling predicate keeps the anchored function untouched, so E1–E3 drift on `corrected` and `corpus` alone; a parameter with a default drifts `records_a_past_state` too | a sibling predicate and a text step beside `blank_struck` | ✅ the default, at `93acc277`: `a_gathered_fragment(path, gathered)` beside `records_a_past_state` in `corrected` and `corpus`, the set from `gathered_fragments(root, rev)` (one `read_blobs`, no path list); `blank_released` beside `blank_struck`, applied in `sentences` on the path `CHANGELOG.md`. `records_a_past_state` untouched (`phases/phase-2.md`) |
| Q5 | Does a section moved whole from one file to another — #526's shape, the split of `docs/review-chain-spec.md` — report nothing? `wanted` subtracts every n-gram the range wrote, so a pure move leaves no removed n-gram to look for; a reworded sentence in the move is a source as it should be. Read, not measured, and the milestone's grounds for putting this item first name that split as a range this sweep has to judge cleanly | a measurement — one probe in phase 3, driven from Python: a claim stated in `a.md` and quoted in `notes.md`, moved to `b.md` verbatim in one commit, then moved with one sentence reworded | Silent on the pure move and reporting `notes.md` on the reworded one: recorded in `phases/phase-3.md`, no case planted. Anything else: a finding for the fix pass and a case | the probe's result is recorded either way | ⬜ |
| Q6 | How the kept token kinds are named across interpreters — on 3.12 an f-string is FSTRING_START, FSTRING_MIDDLE and FSTRING_END and the kept one is the middle; below 3.12 it is one STRING — and what a blanked code token leaves behind to end a sentence between two literals: a `|` where the token stood, which `END` already splits on, or a blank plus a sentence-ending character. Either keeps line numbers; the choice is about what S4's case reads back | the work — phase 1 decides it and `phases/phase-1.md` records it | Read the kinds off the tokenize module by name with a fallback for the older shape; leave a `|` where each code token stood, so `segments` needs no change | as stated | ✅ as stated, at `476af109`: `PROSE_TOKENS` read off `tokenize` by name, a `|` per code token, `segments` untouched. The delimiters and `INDENT` are blanked with no `|`; `NL`, `NEWLINE`, `DEDENT` and `ENDMARKER` were measured to change nothing and are not in the set (`phases/phase-1.md`) |

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
