# `settle` reads a marker inside a commented-out draft — questions for the planner

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

<!-- seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## What the tree answered, so nobody reopens it

The spawn prompt left two judgments open and named several facts to re-check.
Every one is decided in `spec.md` or in `plan.md`'s Alternatives table with
the grounds, and each is overturnable by opening what was opened. None is a
row below.

| Settled | Answer | Where |
|---|---|---|
| Where the code-span rule lives | One owner in `skills/verify/scripts/unverified_check.py`: a span blanker beside `blank_fences` and a composed `live_lines` that `folded_items` and both loops of `settle.py#coordinates` read through | `spec.md` §*What the tree answered*, `plan.md` §*Summary* |
| Whether the obvious closure is wrong | Yes, re-measured at `3cdfd8ad`: 94 → 91 markers, three real ones lost; 94 with spans blanked first | `spec.md` §*Measured on this tree* |
| Whether the span pass goes into `comment_scan` or `readable()` | Neither. The first changes `strip_comments`'s pinned output for every record reader; the second turns `tests/test_chain_hooks.py#reader_blanking_passes` red and is #210's behaviour change to the review-history guard | `plan.md` §*Alternatives* |
| Which span rule | CommonMark's equal-length backtick strings, single-line; round 3's loose regex is recorded as acceptable and not chosen | `plan.md` §*Technical context*, departure 2 |
| Whether a correct fix changes the dry run | No: the per-section coordinate counts are identical under the composed rule, and the 761 lines it calls not live are 48 real comment blocks with 0 coordinates and 0 markers. A change is a defect | `spec.md` §*What the tree answered*, A8 |
| How many phases, in what order | Three: refusal path · single-scan pin · live-line rule, the pin before the rule so the helper is built under it | `plan.md` §*Phases* |
| Whether #487 or #488 is touched | Neither; one docstring's misattribution to #487 is corrected in passing | `spec.md` §*What the tree answered* |
| Where the parent's drifted rows are re-stamped | In the parent's own fragment, `seal/ledger/1790027178-….md` — the rows are not in `seal/ledger.md` | `spec.md` §*Data & interfaces* |
| Whether `folded_items` changes at all | Yes, to read through the same helper: `docs/` carries the quoted-opener shape at three lines today, closed on their own line by the convention and not by the reader | `plan.md` §*Technical context*, departure 1 |
| Whether A4 pins the number 94 | No — set equality with the fence-only sectioning, because the number grows at every release fold and a floor over the corpus is the shape `skills/settle/SKILL.md` §3 warns about | `plan.md` §*Alternatives* |
| Which accessor, and how wide the class is | `os.path.isfile`; three readers of the marker, one wrong; `hooks/root-migrate.py`'s `exists` reads the old marker and is outside | `spec.md` §*The class, enumerated* |

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | **Does `bin/settle` still read `81 work items in 37 segments, 16 ungrouped, 0 skipped` once phase 3 is in?** Predicted from the framer's probe: the composed rule leaves every section's coordinate count identical and parks only 48 comment blocks that carry no coordinate and no marker. The prediction is a read of a probe over the same functions, not a run of the changed command, so the build takes the measurement at the tip. | **a measurement** | one run of `bin/settle` at phase 3's tip, exit code read directly · the same line — nothing to record but the quote in `overview.md` · a different line — the span rule misreads the ledger, and the phase does not close until A3 and A4 say why | **unchanged.** A8 is the acceptance and `overview.md` carries the quote; the parent's `overview.md` §*The dry run* is the shape to copy | ✅ **executed** 2026-09-22 at `7605feb4`, phase 3's tip: `released and unfolded: 81 work items in 37 segments, 16 ungrouped, 0 skipped`, exit 0 read with `echo $?` and not through a pipe. Unchanged, as predicted; the quote is in `overview.md` §*The dry run* |
| Q2 | **Is the single-line span rule enough, stated as a limit in the docstring, or does the multi-line shape need a case?** CommonMark lets a code span cross a line break; a ledger row cannot, and no `docs/` document here has ever carried a span that opens on one line and closes on the next around a comment opener. Under the single-line rule that shape parks the lines below it until a `-->`, in the safe direction (fewer lines live). Whether that deserves a case pinning the limit, or one sentence saying it, is what building the helper will show. | **the work** | a sentence in `blank_code_spans`'s docstring naming the limit and its direction · a case that plants the multi-line shape and asserts the safe direction, so the limit is pinned rather than described · widening the rule to multi-line spans, which needs state across lines the way `blank_fences` keeps it | **the sentence.** The shape has never occurred here, the failure direction is the safe one, and a rule nobody has met is a rider's worth of text rather than a case. Phase 3 records the choice in `phases/phase-3.md` | ✅ **the sentence**, decided 2026-09-22 in phase 3 and **corrected the same day after round 1's finding 2**. `blank_code_spans`'s docstring names the single-line limit, the shape it does not blank, and the failure direction — which runs **both** ways, not one: a multi-line span holding an OPENER parks the lines below it (fewer lines live, a fold reported as a deletion, the cheaper mistake), and one holding a MARKER is read as a fold record and the directory goes at exit 0 (the expensive one). The row above, and phase 3's first answer, reasoned about the opener alone. The door is older than this work and stays open; what the docstring now carries is an accurate limit plus the census that says why nothing is at risk here — fourteen multi-line spans in six top-level `docs/` documents, none holding a delimiter or a marker. No case pins the multi-line shape; `phases/phase-3.md` carries the grounds (NAME NOT IN TREE) |

**`Who can answer` takes one of three values and nothing else** — a person, a
measurement, or the work. No row here is a person's, which is why the build
does not wait: the owner pressed `automation`, and nothing in the tree left a
decision that a different answer would turn into different code.

Answered rows feed back into `docs/` (policy clause or open-questions section)
before this directory's work merges — here that is nothing, because neither
row states a rule; Q2's answer lands in a docstring.
