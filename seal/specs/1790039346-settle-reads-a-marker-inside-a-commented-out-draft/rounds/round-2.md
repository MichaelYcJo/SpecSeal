# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 2

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Target SHA | 7f2d6f1c5ccd890b15948c9aa0c0f8488f169c25 |
| Written late | no |
| Ran by | specseal:warden on Opus 5 (1M context) |
| PR | 490 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `9e61df979b8793fa3f620e4e1840a54c8aaca0b1..68a023af504e0dd14a02656952af36b9e7e94300`, 2 commits |
| Contract changes | none |
| New units | test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in (depth 1) |
| Needs a fix | yes — finding 1, an undeclared direction change on a gate that retires a directory at exit 0, and finding 2, a real section marker still lost through the span shape the predicate does not reach; finding 3 is a false ground in shipped code and needs the sentence rather than the behaviour |
| Loses a record or crashes | yes — finding 1, a work item directory removed at exit 0 with nothing having absorbed it, new at `adb5607d` and absent at `7db75512` |

- [x] Pass

## What this round was asked

The verifying round, against the diff of round 1's fixes — three commits,
`7db75512..6d8ebaae` — rather than the branch. Round 1's record read `Fixes
checked by: nobody`, and closing that is what this round is for: for each
verdict round 1 recorded as closed, is it actually closed.

Round 1's finding 1 was a regression this branch introduced into its own fix,
and its repair narrowed the rule with a predicate argument. So the round was
asked to re-derive the corpus invariant that narrowing must preserve — 761
not-live lines, 83 section ids, three named markers still live — and to try to
break the narrowed rule on five named shapes. The three verdicts round 1 closed
as `answered` were handed over as judgments to re-derive rather than accept.

The class to enumerate was round 1's three new units, all depth 1, against the
mutation that should turn each red, with the pass's count of three mutations
derived rather than carried. One of the three is green by construction, and
whether its proof-by-mutation is sound was part of the question.

Corrections handed over: a coordinate the orchestrator chased three times on
this branch and the honesty of the stamp line that ended it; the three places
`survivors.md` exempts; the multi-line-span door left open in `overview.md`
§*Not done*; and whether the fix pass's own census of the false-direction claim
reached everything.

The broad gate was withheld — the sealer's, after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The narrowing makes liveness monotonically non-decreasing, so `folded_items` gains markers and `settle --retire` removes a directory where the pre-fix reader refused; `spec.md` G3 and `plan.md` §*Operational impact* both declare the opposite direction, and no case pins the change | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed** `281308c7` | fixed at 281308c7 — for the disclosure and the pin, `68a023af` for `spec.md` §*Grounding* G3. The behaviour stays — it is faithful to the HTML rule — and what was missing was the declaration and the case. The docstring, `plan.md` §*Operational impact*, `overview.md` and the ledger rows now state both directions, and `c-8` pins the shape. G3 was the one site the fix pass could not touch: a grounding clause is what judges the build, so rewriting it to match what was built is the failure the framer/smith split exists to prevent, and it came to the orchestrator; Executed, the same four-line document through both readers: `folded_items` answers `set()` at `7db75512` and `{'1700000042-quoted'}` here, and `settle --retire` goes from exit 1 *nothing to retire* to exit 0 `removed seal/specs/1700000042-quoted/`. New at `adb5607d`. The behaviour is HTML-faithful and I do not ask for it back; the two declarations and the missing pin are what the fix owes |
| 2 | 🟡 A code span holding the opener AND the closer is still blanked whole, so its closer is lost and a real section marker inside a parked draft is still lost with it | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed** `281308c7` | fixed at 281308c7 — the predicate blanks the opener occurrences inside the span rather than the span, so a span quoting a complete comment keeps its closer; Executed: with a complete comment quoted in a span inside a parked draft, the marker line begins inside the comment at `7db75512` and here, and outside it with the fix below — which is what the HTML rule says. Not a regression; the residual instance of the class round 1's finding 1 named. Ten such spans exist in the corpus, seven in `seal/ledger.md`, and 48 parked blocks; none coincide today. Fix verified: 233 passed exit 0, corpus unchanged at 761 / 83 |
| 3 | 🟡 The shipped ground *which `tests/test_chain_hooks.py#reader_blanking_passes` refuses by design* is false for a widening of the fence reader; that case reads the calls `readable` makes by name and stays green | `skills/settle/scripts/settle.py#coordinates` | **fixed** `281308c7` | fixed at 281308c7 — all three sites. The behaviour decision stands and only the sentence moved: `reader_blanking_passes` is not what refuses a widened fence reader, and the true refusal is named instead. The census over the repository found eleven citations of that case, three false and eight true; the third false one, in `overview.md`, the reviewer had not named; Executed: the widening mutation leaves `tests/test_chain_hooks.py` green and reddens `test_a_continuation_that_looks_like_an_opener_is_still_joined` in `tests/test_the_record_is_generated.py` instead. `plan.md` §*Alternatives considered* states the same guard correctly for composing a pass into `readable()`; the sentence borrowed it into a place it does not reach. The decision to leave the door is right |
| 🟢 confirmation | Round 1's finding 1 is closed and the corpus invariant survives the narrowing | `skills/verify/scripts/unverified_check.py#live_lines` | **fixed**, verified | Executed at the pristine tip: 233 passed, exit 0 over the four affected modules. Re-derived over `seal/ledger.md`, the top-level `docs/` documents and every ledger fragment: 761 not-live lines, 83 section ids, `1788472135-…`, `1788613827-…` and `1788844127-…` live at lines 767, 992 and 1619, and **0** lines of the corpus answer differently under the narrowed rule than under the rule that blanked every span |
| 🟢 confirmation | Round 1's finding 2 is corrected and the door is right to leave open | `skills/verify/scripts/unverified_check.py#blank_code_spans` | **fixed**, verified | Read: the docstring states both directions with the dated census, and `overview.md` §*Not done* carries the decision. Closing the door needs a second cross-line state keeper in a module whose one such reader four gates depend on. I would decide it the same way |
| 🟢 confirmation | Round 1's finding 4 is answered on grounds that hold | `skills/settle/scripts/settle.py#coordinates` | answered, verified | Read the pin rather than the argument: `test_one_comment_scanner_serves_both_readers` ends on `live_lines(["prose"]) == [("prose", False)]`, and a filter form answers `[]` there — the same answer as a reader that yields nothing. The refusal is behaviour-neutral and costs nothing (NAME NOT IN TREE) |
| 🟢 confirmation | Round 1's finding 5 is corrected, and the measurement behind the correction is right | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Alternatives considered* | answered, verified | Executed: the loose regex reddens exactly two of the five shapes — the double-backtick span and the unmatched-opener shape. The row now says the permission is one the suite refuses, with the date |
| 🟢 confirmation | Round 1's finding 6 is fixed and its count still holds | `skills/settle/scripts/settle.py#coordinates` | **fixed**, verified | Executed: four rows of `seal/ledger.md` quote the opener inside backticks with no closer, at 78, 762, 980 and 1612. The sentence is dated, past tense, and says what the rule rests on |
| 🟢 confirmation | Every unit the `New units` row names is red under a mutation, derived rather than carried | both test modules and `skills/verify/scripts/unverified_check.py` | confirmed | Executed, four mutations each applied alone and restored, tree clean after each. The mapping is in the table above. The indented-example case's non-vacuity proof by mutation is sound for a case that pins an open door |
| 🟢 confirmation | The narrowed rule holds against seven further span shapes | `skills/verify/scripts/unverified_check.py#blank_code_spans` | confirmed | Executed: two openers in one span, a closer whose enclosing comment was opened inside another span, nested backtick runs with the delimiter in the inner run, a line that is a span and nothing else in both delimiters, a stray closer with no comment open, and an opener quoted inside a parked draft. All seven answer as the design intends; only the both-delimiter shape of finding 2 does not |
| ⬜ | `survivors.md` exempts three places and all three grounds hold | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/survivors.md` | confirmed | Read all three. The two comprehension bodies are the pair a case pins, flagged on shared n-grams. The parent's S3 row is a dated append-only re-read chain whose later notes supersede the quoted sentence; Executed as well — `seal/ledger.md` carries 0 fenced blocks, so the superseded sentence is still true on its own terms |
| ⬜ | The stamp line asserting an act of reading is honest | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-1-report.md:191` | confirmed | Read, and the conclusion behind it re-derived: the line states the value it read, says the row has since moved and why the stamp follows it. `skills/settle/scripts/settle.py#coordinates@9b5febe4` and `skills/verify/scripts/unverified_check.py#folded_items@7a8d3c99` are byte-identical across the parent's fragment, this work item's fragment, `spec.md` and the report |
| ❓ out of verified scope | Whether the four changed files pass `ruff check` and whether `evidence_check.py --strict .` is clean at this SHA | the repository | not run | §2 gives the broad gate to the sealer and my definition hands me none of the three. The orchestrator reports both as executed at or near this SHA with exit 0; this round did not re-run them and does not certify them. The caller answers it |

## Paste-ready fixes

```
the failure direction, which for the OPENER half is *reads fewer lines as
live* — a marker that stops counting is a fold record unread, a directory
kept and a deletion reported — and for the CLOSER half is the other way:
leaving a closer-only span alone can only end a comment sooner, so liveness
is monotonically non-decreasing and a marker the old rule parked is now read.
Measured 2026-09-22: a `docs/` draft quoting the closing delimiter in prose
above a marker took `settle --retire` from exit 1 to exit 0 with the
directory removed. Faithful to the HTML rule and deliberate, pinned by
`test_every_comment_shape_a_policy_document_can_carry`'s `c-8`, and the
reason the fold reader may not be given this pass without the case beside it
```
```
- **The hygiene workflow's unverified-record step reads the changed
  `folded_items`.** Failure direction, both halves. The single-line span
  limit fails toward fewer lines live: a marker the rule stops reading is a
  fold reported as a deletion, the noisy and cheaper direction. The
  opener-only predicate fails the other way: a span holding no opener is left
  alone, the only delimiter that can survive is a closing one, and a closing
  one can only end a comment sooner — so a marker the pre-fix rule parked is
  now read and the directory is retired at exit 0. Measured 2026-09-22 at
  `7db75512` against the fix tip: `nothing to retire` at exit 1 became
  `removed seal/specs/<id>/` at exit 0. The behaviour is what the HTML rule
  says and `c-8` pins it. Prompt budget: zero.
```
```
    The direction this buys is worth stating, because it is not the one the
    limit above fails in. A span the predicate leaves alone cannot hold an
    opener, so the only delimiter it can restore is a closing one, and a
    closing one can only end a comment sooner: liveness is monotonically
    non-decreasing, and a marker the unnarrowed pass parked is now read.
    `folded_items` then has a fold record where it had none, and
    `settle --retire` removes that directory at exit 0. Measured 2026-09-22:
    a draft quoting the closing delimiter in prose above a marker took the
    command from exit 1 to exit 0. That is the HTML rule and it is deliberate;
    `c-8` of `test_every_comment_shape_a_policy_document_can_carry` is what
    keeps a later edit from taking it back in silence.
```
```python
        # And its mirror. A CLOSER quoted inside a span is left alone, because
        # inside a comment nothing is markdown and the quotation really does
        # end the draft. So the marker below it is live and this IS a fold
        # record — the one shape where the narrowing reads MORE than the pass
        # that blanked every span, and `settle --retire` removes the directory
        # at exit 0. Deliberate, and pinned here so it is not taken back.
        ("<!-- parked\nprose with `-->` in it\n<!-- specs/c-8 -->\n-->\n", {"c-8"}),
```
```python
            span = line[start : runs[closer][1]]
            if holding is None:
                chars[start : runs[closer][1]] = " " * len(span)
            else:
                # The DELIMITER, not the span. A span quoting a complete
                # comment holds the opener, so blanking it whole took the
                # quoted CLOSER with it and a draft the quotation really ends
                # stayed open — a real section marker below it lost, which is
                # this predicate's own finding one shape over.
                for m in re.finditer(re.escape(holding), span):
                    chars[start + m.start() : start + m.end()] = " " * len(holding)
            i = closer + 1
```
```
    blanked. What is blanked inside such a span is the opener itself and not
    the span around it: a span quoting a complete comment holds an opener and
    a closer, and taking the closer with it left a draft open that the
    quotation really does end.
```
```python
def test_a_quoted_whole_comment_still_closes_the_draft_it_sits_in(tree):
    """The other half of the shape above. A span quoting a complete comment
    holds the OPENER, so the predicate blanked it whole and the quoted closing
    delimiter went with it — the draft stayed open, the next real section
    marker began inside it and opened nothing, and the row below went to
    whichever section was open. Inside a comment nothing is markdown, so what
    the pass owes the comment scan is the opener blanked and the closer left
    where it stands."""
    ledger = tree / "seal" / "ledger.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + "\n<!-- a draft, parked\n"  # the whole comment quoted below ends it: -->
        + "the draft ends with `<!-- a note -->` quoted whole\n"
        + "<!-- specs/1700000002-beta -->\n"
        + "| after | `hooks/after.py#thing@88888888` | read | 2026-01-01 | |\n",
        encoding="utf-8",
    )
    rows = settle.coordinates(str(tree))
    assert "hooks/after.py" in rows["1700000002-beta"], dict(rows)
    assert "hooks/after.py" not in rows["1700000003-gamma"], dict(rows)
```
```
    Widening the fence reader would move `readable`, `check_text`,
    `round_record.py` and the review-history guard at once — measured
    2026-09-22, one such widening reddens
    `tests/test_the_record_is_generated.py#test_a_continuation_that_looks_like_an_opener_is_still_joined`,
    a record reader with no stake in this rule. `reader_blanking_passes` is
    NOT that refusal and does not fire here: it reads the calls `readable`
    makes by name, which a widened `blank_fences` leaves unchanged. It
    refuses a pass ADDED to `readable`, which is a different alternative and
    the row `plan.md` states it against.
```
```python
    """The third quotation, pinned as read rather than as fixed. `blank_fences`
    knows the two fenced forms and markdown's indented code block is neither,
    so a fragment showing its example row indented has that example counted as
    its own coordinate. Widening the fence reader would move `readable`,
    `check_text`, `round_record.py` and the review-history guard at once —
    measured, it reddens a record reader's continuation case with no stake in
    this rule. `tests/test_chain_hooks.py#reader_blanking_passes` is not that
    refusal: it reads the calls `readable` makes by name and a widened
    `blank_fences` leaves them unchanged. The case exists so a session that
    widens it one day is told what this one decided, and why it decided it in
    the docstring instead of in the code."""
```

## Executed probes

| What was run | Result |
|---|---|
| the four affected modules at the pristine tip, in the clone | 233 passed, exit 0 |
| the corpus under four liveness rules — fence-only, naive, blank-every-span, shipped | shipped and blank-every-span agree on every line; 761 not live, 83 section ids, against 787 / 80 naive |
| the three named markers, by id, through the shipped rule | live at `seal/ledger.md` lines 767, 992 and 1619 |
| eight adversarial span shapes, shipped rule against the pre-fix rule against the HTML rule | seven agree with the design; the both-delimiter shape inside a parked draft loses a real marker |
| `folded_items` and `settle --retire` over a parked draft quoting the closing delimiter, at `7db75512` and at this SHA | `set()` / exit 1 *nothing to retire* against `{'1700000042-quoted'}` / exit 0 `removed seal/specs/1700000042-quoted/` |
| the finding-2 fix applied in the clone: the four modules, then the corpus, then the eight shapes | 233 passed exit 0; 761 / 83 unchanged; only the both-delimiter shape changes answer |
| four mutations, each alone and restored, against three to five modules | the mapping in §*The three new units*; tree clean after each |
| the fence-reader widening mutation against five modules | `tests/test_chain_hooks.py` green; one red in `tests/test_the_record_is_generated.py`, one in `tests/test_settle_reads_before_it_removes.py` |
| round 3's loose regex against the five parametrised span shapes | 2 of 5 red, as the corrected `plan.md` row states |
| the ledger rows quoting an unclosed opener inside backticks | 4, at lines 78, 762, 980 and 1612 — the dated docstring count |
| code spans quoting a complete comment, across `seal/ledger.md`, `docs/` and the fragments | 10, seven of them in `seal/ledger.md`; 48 parked blocks in that file; none coincide |
| fenced blocks in `seal/ledger.md` | 0 — `survivors.md`'s third row's superseded sentence is still true |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it, and what blocks that spawn is the three 🟡 above and nothing else |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/unverified_check.py#live_lines` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/unverified_check.py#blank_code_spans` | round 1's 2 — fixed |
| round-1 | `skills/settle/scripts/settle.py#coordinates` | round 1's 3 — answered |
| round-1 | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md` §*Alternatives considered* | round 1's ⬜ 5 — answered |
| round-1 | `skills/verify/scripts/unverified_check.py` | round 1's 🟢 confirmation — confirmed |
| round-1 | `skills/settle/scripts/settle.py#main` | round 1's 🟢 confirmation — confirmed |
| round-1 | both test modules | round 1's 🟢 confirmation — confirmed |
| round-1 | `tests/test_a_row_points_by_content.py:763` | round 1's ⬜ — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py`'s own readers are the same class one module over | already deferred in round 1 to `seal/follow-up.md`, two rows, and before that by `spec.md` §*Scope*, Out | the answerers those rows already name |
| `.github/scripts/fold_ledger.py#demote`'s fence tracking | already deferred in `spec.md` §*Scope*, Out — not shipped, and its own rider says what it misreads | the same, unchanged by this round |
| Markdown's indented code block as a third quotation | already deferred in round 1, finding 3, to `skills/settle/scripts/settle.py#coordinates`'s docstring and `test_an_indented_example_row_is_counted_and_the_reader_says_so` | the decision stands; only the sentence about the guard needs the edit, which is 🟡 3 |
| A comment delimiter inside a code span that crosses a line break | already deferred in round 1, finding 2, to `overview.md` §*Not done* and the docstring's dated census | the same, and this round agrees with the decision |
