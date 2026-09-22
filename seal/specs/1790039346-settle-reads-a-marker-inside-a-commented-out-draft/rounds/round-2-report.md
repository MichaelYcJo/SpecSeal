# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — review round 2 report

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

Target SHA `7f2d6f1c5ccd890b15948c9aa0c0f8488f169c25`, HEAD, which had not
moved. Base `origin/release/v0.13.0` at `3cdfd8ad`. The verifying round: the
fix range `7db75512..6d8ebaae`, three commits, plus the two record commits
after it. Reviewed in a `git clone --no-local` at that SHA, made in the
session scratchpad; the clone, its virtual environment and every probe are
deleted.

## What this round found, in causal order

Round 1's three fixes all do what they claim, and I closed each by execution
rather than by reading the record. The corpus invariant survives the
narrowing exactly: 761 not-live lines, 83 section ids, the three named
markers live, and **0 lines in the whole corpus answer differently under the
narrowed rule than under the rule that blanked every span**.

The three findings below all sit on the one thing round 1's finding 1 changed
— that `blank_code_spans` now takes a predicate — and they fall in causal (NAME NOT IN TREE)
order.

1. Leaving a closer-only span alone can only ever end a comment earlier, so
   the narrowing makes **more** lines live, never fewer. For `folded_items`
   that is the direction that removes a work item directory. Measured: a shape
   the pre-fix reader parked now retires at exit 0. Two documents declare this
   gate's failure direction and both now say the opposite.
2. The rule the fix states and the rule it implements part company for one
   span shape: a span holding the opener **and** the closer. That span is
   still blanked whole, so its closer still vanishes, so a real section marker
   below it is still lost. Same class as round 1's finding 1, one shape over.
3. The ground finding 3 was answered with names a guard that does not guard.
   Widening the fence reader leaves `tests/test_chain_hooks.py` green, and
   that sentence is now in shipped code.

None of the three is reachable in the tree as it stands, which I measured
rather than assumed.

---

## 🟡 1 · The narrowing moves the fold gate toward removing a directory, and both declarations of its failure direction say the opposite

`skills/verify/scripts/unverified_check.py#blank_code_spans` (the behaviour),
`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`
§*Grounding* G3 and `plan.md` §*Operational impact* (the declarations).

A span the narrowed rule leaves alone cannot hold the comment opener — the
predicate is what decides that. So the only delimiter the narrowing can
restore to the text is a closing one, and a closing one can only end a comment
sooner. Liveness is therefore monotonically non-decreasing: every line the
pre-fix rule called live the new rule still calls live, and some lines it
parked are now live.

For `coordinates` that direction is the repair round 1 asked for. For
`folded_items` it is the other thing: a marker that was parked and is now live
is a fold record, and `settle --retire` acts on it.

**Executed**, the same four-line document through the pre-fix reader at
`7db75512` and through this SHA's, driving `settle --retire` against a
throwaway repository whose work item directory nothing had absorbed:

| | `folded_items` | `settle --retire` |
|---|---|---|
| pre-fix `7db75512` | `set()` | exit 1, *nothing to retire* |
| this SHA | `{'1700000042-quoted'}` | **exit 0, `removed seal/specs/1700000042-quoted/`** |

The document is a commented-out draft whose prose quotes the closing delimiter
inside backticks, with a real marker on the next line and the draft's own
closer after it.

**The behaviour is right and the disclosure is missing.** Inside an HTML
comment nothing is markdown, so the quoted closer really does end the draft
and the marker really is outside it — which is the reasoning the fix rests on,
and I agree with it. What follows from it is a direction change on a gate, and
`CONTRIBUTING.md` §*What a change to a gate must carry* asks for that direction
in writing. Two places write it, and both write the old one:

- `spec.md` G3 — *the failure direction, which is reads fewer lines as live …
  a directory kept and a deletion reported rather than a directory removed
  with nothing absorbing it, the cheaper mistake.*
- `plan.md` §*Operational impact* — *Failure direction: fewer lines live, so a
  marker the new rule stops reading is a fold reported as a deletion — the
  noisy direction, and the cheaper one.*

Both sentences were true of the change round 1 reviewed. The fix pass reversed
them and re-ran its census against round 1's finding 2 — the pre-existing
multi-line door — rather than against the change it had just made. That is why
the census reached `plan.md` §*What breaks in six months*, `phases/phase-3.md`,
`questions.md` Q2 and `overview.md` and stopped: those four talk about the
multi-line limit, and these two talk about the gate.

**And nothing pins it.** §14 asks a fix that changes what a person sees to
document it and pin it. What a person sees moved from `nothing to retire` at
exit 1 to `removed seal/specs/<id>/` at exit 0, and no case holds that in
place. `test_every_comment_shape_a_policy_document_can_carry` already
parametrises seven comment shapes and `c-7` is this one's mirror — an opener
quoted in a span. The closer quoted in a span is the missing eighth.

## 🟡 2 · A span holding both delimiters still swallows its closer, so a real marker is still lost

`skills/verify/scripts/unverified_check.py#blank_code_spans`.

The predicate asks whether the span holds the opener and blanks the whole span
when it does. A span that quotes a complete comment — opener, text, closer —
holds the opener, so it is blanked whole and its **closer** goes with it. Sat
inside a parked draft, that span no longer ends the draft, the next real
section marker begins inside it and opens nothing, and the row below is filed
under whichever section was open.

**Executed**, four lines: a parked draft, a sentence quoting a complete comment
inside backticks, a real section marker, a row.

| | the marker line begins outside a comment? |
|---|---|
| what the HTML rule says | **yes** — the quoted closer ends the draft |
| pre-fix `7db75512` | no |
| this SHA | no |
| with the fix below | **yes** |

So this is not a regression — the pre-fix rule answered the same. It is the
residual instance of the class round 1's finding 1 opened, and §12 is why it
belongs in this round rather than in a later one: the finding named a shape,
the fix closed that shape, and the cause produces two.

**The root cause is that the pass blanks a span where it means to blank a
delimiter.** The purpose of the pass is that a quoted opener must not open a
comment. Blanking the span achieves that and takes the span's closer as
collateral. Blanking the opener occurrences inside the span achieves it and
takes nothing — and outside a comment a surviving closer is inert, because
`comment_scan` looks for one only while it is inside.

**Verified, with the fix below applied in the clone**: 233 passed at exit 0
across the four affected modules; the corpus still answers 761 not-live lines
and 83 section ids with the three named markers live; and of the eight shapes
I probed, only this one changes answer.

**Reachable, and the corpus carries both halves.** Ten code spans in
`seal/ledger.md`, `docs/` and the ledger fragments quote a complete comment —
seven of them in `seal/ledger.md` itself, at lines 15, 80, 300, 336, 362 and
1891. `seal/ledger.md` also carries 48 parked comment blocks. None of the ten
sits inside one of the 48 today, which is the whole of why nothing is lost
now.

## 🟡 3 · The ground finding 3 was answered with names a guard that does not guard, and it is in shipped code

`skills/settle/scripts/settle.py#coordinates`, the third-quotation paragraph,
and `tests/test_settle_reads_before_it_removes.py:767`.

Both say widening the fence reader *would move `readable`, `check_text`,
`round_record.py` and the review-history guard at once, which
`tests/test_chain_hooks.py#reader_blanking_passes` refuses by design.*

The first half holds. The second does not. `reader_blanking_passes` reads
`readable`'s own source and returns the functions it calls **by name**; the
case asserts that set against `HIDDEN_CLOSING_WORD`'s keys. Widening
`blank_fences` changes what that function does and not which functions
`readable` calls, so the set is unchanged and the guard stays green.

**Executed**, one mutation that teaches `blank_fences` markdown's indented code
block, applied alone against five modules:

```
tests/test_chain_hooks.py                          green
tests/test_the_record_is_generated.py              1 red -
    test_a_continuation_that_looks_like_an_opener_is_still_joined
tests/test_settle_reads_before_it_removes.py       1 red -
    test_an_indented_example_row_is_counted_and_the_reader_says_so
```

So something does refuse the widening, and it is not the case named. The one
that goes red is `round_record.py`'s continuation joiner, which is the third
of the four readers the sentence lists — evidence for the first half and
against the second.

**Why it matters more than a wrong citation.** `plan.md` §*Alternatives
considered* states the same guard correctly, for a different alternative:
composing the span pass **into `readable()`** does redden it, because that adds
a pass to `readable`. The indented-block paragraph borrowed the guard from that
row into a place it does not reach. A session that widens the fence reader one
day will read the shipped docstring, believe a named case is holding the door,
and find it green.

**The decision itself is right.** Leaving the indented-block door open is the
cheaper choice and I would make it again — the widening moves four readers and
reddens a record case that has nothing to do with this work item. What needs
the edit is the sentence, in the two places it is shipped.

---

## Round 1's six verdicts, re-derived

**Finding 1 — fixed, and closed.** Executed at the pristine tip: 233 passed,
exit 0 across `tests/test_unverified_rows_close.py`,
`tests/test_settle_reads_before_it_removes.py`, `tests/test_chain_hooks.py`
and `tests/test_a_script_says_which_interpreter_it_needs.py`. The corpus
invariant holds unchanged — 761 not-live lines, 83 section ids, the markers
`1788472135-…` at line 767, `1788613827-…` at 992 and `1788844127-…` at 1619
all live — and the narrowed rule differs from the blank-every-span rule on
**0** lines of the whole corpus. Findings 1 and 2 above are what the narrowing
still leaves.

**Finding 2 — the sentence is corrected, and leaving the door is right.** The
docstring now states both directions and carries the census that says why the
shape is harmless here. I judge the decision correct: closing a multi-line span
needs state carried across lines, `blank_fences` is the only reader in this
module that keeps such state, and adding a second one is the change the four
readers refuse. `overview.md` §*Not done* names it with the grounds and the
door's pre-existence, which the pre-fix reader answering the same set
establishes. Nothing here is a finding.

**Finding 3 — the decision is right, the second ground is false.** See 🟡 3
above. The case pinning it is sound and non-vacuous, which I proved rather
than accepted: it cannot be shown red first, because it pins behaviour that
already existed, so the honest substitute is a mutation that closes the door.
Applied, that mutation reddens
`test_an_indented_example_row_is_counted_and_the_reader_says_so` **alone** among
the three modules it runs with. That is the right shape of proof for a case
that pins an open door, and it is what the pass claimed.

**Finding 4 — answered, and the grounds hold.** I opened the pin rather than
the argument about it. `test_one_comment_scanner_serves_both_readers` ends on (NAME NOT IN TREE)
`assert list(uc.live_lines(["prose"])) == [("prose", False)]`, with the reason
beside it: one plain line really does begin outside a comment, so `False` can
only have come off the stub. A generator yielding the live lines alone answers
`[]` there, which is what a `live_lines` reading nothing also answers. The
proposed simplification would make that assertion unable to tell the two apart.
Behaviour-neutral either way, so the refusal costs nothing. Confirmed.

**Finding 5 — answered, and re-derived.** Executed: applying round 3's loose
regex to the five shapes `test_a_code_span_closes_at_a_backtick_string_of_equal_length`
parametrises reddens exactly two —
the double-backtick span, which the loose rule closes at the single backtick
inside it, and the unmatched-opener shape, where scanning is meant to go on
after the literal. The `plan.md` row now says the permission is one the suite
refuses, with the date. Confirmed.

**Finding 6 — fixed, and the count is still true.** Executed: four rows of
`seal/ledger.md` quote the opener inside backticks with no closer on the line,
at 78, 762, 980 and 1612. The docstring now dates the reading, puts it in the
past tense, and says what the rule actually rests on. Confirmed.

## The three new units, each against the mutation that reddens it

Derived rather than taken from the pass. Each mutation applied alone and
restored from the original source, the tree checked clean after each.

| Unit | Mutation | What went red |
|---|---|---|
| `OPENER` | spelt as the closing delimiter instead | 4 cases, including `test_a_closer_quoted_in_prose_still_closes_a_parked_draft`, `test_an_opener_quoted_inside_a_code_span_parks_nothing` and `test_the_rule_over_this_repositorys_ledger_loses_no_section` |
| `test_a_closer_quoted_in_prose_still_closes_a_parked_draft` | the blanking made unconditional again, which is the pre-fix code | that case alone |
| the same | `live_lines` drops the predicate argument | that case alone |
| `test_an_indented_example_row_is_counted_and_the_reader_says_so` | `blank_fences` widened to markdown's indented code block | that case alone |

The second row is §15 satisfied in the only form available after the fact: the
case is red against the code the fix replaced. The fourth is the non-vacuity
proof for a case that pins an open door, and it is sound — a case that is green
by construction cannot be shown red first, and a mutation that closes the door
it pins is what stands in for that.

## The corrections handed over, answered

**1 · The stamp line is honest.** `rounds/round-1-report.md:191` asserts an act
of reading, which nothing can check — but it does not assert the act it did not
perform. It states the value the line carries now, then says in the next clause
that the row read `@a1c78799` when the round read it and why the stamp follows
the row. The conclusion behind the stamp is re-derivable and I re-derived it:
`skills/settle/scripts/settle.py#coordinates@9b5febe4` and
`skills/verify/scripts/unverified_check.py#folded_items@7a8d3c99` appear in four
places — the parent's fragment, this work item's fragment, `spec.md` and the
report — byte-identical in all four. A record of a past state that the records
arm reads as a live claim has exactly two honest shapes, and this is one of
them.

**2 · `survivors.md`, all three rows judged and all three sound.** The two
comprehension bodies in `unverified_check.py` are the pair
`test_one_comment_scanner_serves_both_readers` exists to pin, flagged because (NAME NOT IN TREE)
this branch reworded a docstring sharing their n-grams — an n-gram sweep cannot
tell a kept implementation from a removed sentence, and the grounds say so.

The third is the interesting one and it is right too. The parent's S3 evidence
cell is an append-only chain of dated re-reads; the sentence the sweep found
carries **Re-read 2026-09-22 in round 2's fix pass** in front of it and two
later dated notes after it, the last of which re-asserts the figure for this
build. Rewriting it would delete what was true at the parent's round 2, which
is the one thing such a chain exists to keep. I also checked the superseded
sentence for truth rather than only for supersession: `seal/ledger.md` carries
0 fenced blocks today, so it is still true as well as still dated.

**3 · Finding 2's door is right to leave** — see above.

**4 · The census did not reach everything** — see 🟡 1. Two sites remain, and
both are the gate's declared failure direction.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The narrowing makes liveness monotonically non-decreasing, so `folded_items` gains markers and `settle --retire` removes a directory where the pre-fix reader refused; `spec.md` G3 and `plan.md` §*Operational impact* both declare the opposite direction, and no case pins the change | `skills/verify/scripts/unverified_check.py#blank_code_spans` | open | Executed, the same four-line document through both readers: `folded_items` answers `set()` at `7db75512` and `{'1700000042-quoted'}` here, and `settle --retire` goes from exit 1 *nothing to retire* to exit 0 `removed seal/specs/1700000042-quoted/`. New at `adb5607d`. The behaviour is HTML-faithful and I do not ask for it back; the two declarations and the missing pin are what the fix owes |
| 2 | 🟡 A code span holding the opener AND the closer is still blanked whole, so its closer is lost and a real section marker inside a parked draft is still lost with it | `skills/verify/scripts/unverified_check.py#blank_code_spans` | open | Executed: with a complete comment quoted in a span inside a parked draft, the marker line begins inside the comment at `7db75512` and here, and outside it with the fix below — which is what the HTML rule says. Not a regression; the residual instance of the class round 1's finding 1 named. Ten such spans exist in the corpus, seven in `seal/ledger.md`, and 48 parked blocks; none coincide today. Fix verified: 233 passed exit 0, corpus unchanged at 761 / 83 |
| 3 | 🟡 The shipped ground *which `tests/test_chain_hooks.py#reader_blanking_passes` refuses by design* is false for a widening of the fence reader; that case reads the calls `readable` makes by name and stays green | `skills/settle/scripts/settle.py#coordinates` | open | Executed: the widening mutation leaves `tests/test_chain_hooks.py` green and reddens `test_a_continuation_that_looks_like_an_opener_is_still_joined` in `tests/test_the_record_is_generated.py` instead. `plan.md` §*Alternatives considered* states the same guard correctly for composing a pass into `readable()`; the sentence borrowed it into a place it does not reach. The decision to leave the door is right |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py`'s own readers are the same class one module over | already deferred in round 1 to `seal/follow-up.md`, two rows, and before that by `spec.md` §*Scope*, Out | the answerers those rows already name |
| `.github/scripts/fold_ledger.py#demote`'s fence tracking | already deferred in `spec.md` §*Scope*, Out — not shipped, and its own rider says what it misreads | the same, unchanged by this round |
| Markdown's indented code block as a third quotation | already deferred in round 1, finding 3, to `skills/settle/scripts/settle.py#coordinates`'s docstring and `test_an_indented_example_row_is_counted_and_the_reader_says_so` | the decision stands; only the sentence about the guard needs the edit, which is 🟡 3 |
| A comment delimiter inside a code span that crosses a line break | already deferred in round 1, finding 2, to `overview.md` §*Not done* and the docstring's dated census | the same, and this round agrees with the decision |

## Paste-ready fixes

Finding 1 — the two declarations, and the case that pins the eighth shape.

`spec.md` §*Grounding*, the G3 row's second item:

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

`plan.md` §*Operational impact*, replacing the `folded_items` bullet:

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

`blank_code_spans`, appended to the `holding` paragraph: (NAME NOT IN TREE)

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

and the eighth shape, in `tests/test_unverified_rows_close.py`, in the
parametrisation beside `c-7`:

```python
        # And its mirror. A CLOSER quoted inside a span is left alone, because
        # inside a comment nothing is markdown and the quotation really does
        # end the draft. So the marker below it is live and this IS a fold
        # record — the one shape where the narrowing reads MORE than the pass
        # that blanked every span, and `settle --retire` removes the directory
        # at exit 0. Deliberate, and pinned here so it is not taken back.
        ("<!-- parked\nprose with `-->` in it\n<!-- specs/c-8 -->\n-->\n", {"c-8"}),
```

Finding 2 — `blank_code_spans`, blanking the delimiter rather than the span. (NAME NOT IN TREE)
Verified in the clone: 233 passed at exit 0 across the four modules, the corpus
unchanged at 761 not-live lines and 83 section ids, and of the eight probed
shapes only the both-delimiter one changes answer.

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

and the `holding` paragraph's last sentence, which states the rule the code
now keeps:

```
    blanked. What is blanked inside such a span is the opener itself and not
    the span around it: a span quoting a complete comment holds an opener and
    a closer, and taking the closer with it left a draft open that the
    quotation really does end.
```

with the case, in `tests/test_settle_reads_before_it_removes.py` beside
`test_a_closer_quoted_in_prose_still_closes_a_parked_draft`. Red against this
SHA on the first assertion, which reports the row under the previous section:

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

Finding 3 — the two shipped sentences. In
`skills/settle/scripts/settle.py#coordinates`, replacing the clause from
*Widening the fence reader* to *refuses by design*:

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

and in `tests/test_settle_reads_before_it_removes.py`, the same correction
inside `test_an_indented_example_row_is_counted_and_the_reader_says_so`'s
docstring:

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

Needs a fix: yes — finding 1, an undeclared direction change on a gate that
retires a directory at exit 0, and finding 2, a real section marker still lost
through the span shape the predicate does not reach; finding 3 is a false
ground in shipped code and needs the sentence rather than the behaviour
Loses a record or crashes: yes — finding 1, a work item directory removed at
exit 0 with nothing having absorbed it, new at `adb5607d` and absent at
`7db75512`

## Proof block

Opened: `skills/verify/scripts/unverified_check.py`,
`skills/settle/scripts/settle.py`, `tests/test_unverified_rows_close.py`,
`tests/test_settle_reads_before_it_removes.py`, `tests/test_chain_hooks.py`
(the `reader_blanking_passes` derivation and the case that asserts it),
`tests/test_the_record_is_generated.py` (by mutation result only),
`seal/ledger.md`, the top-level `docs/*.md`, every `seal/ledger/*.md`
fragment, the parent's fragment
`seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`
(the S3 evidence cell in full), this work item's `spec.md`, `plan.md`,
`questions.md`, `overview.md`, `changelog.md`, `survivors.md`,
`phases/phase-3.md`, `rounds/round-1.md` and `rounds/round-1-report.md`, and
its ledger fragment. `CLAUDE.md` and `CONTRIBUTING.md` for the gate rule.

Not opened, and named because a verdict here would have needed them: the
parent work item's `rounds/round-1.md`, `round-2.md`, `round-3.md` and their
reports. Round 1 of this work item did not open them either, for the same
reason — their coordinates reach this round through the ticket, the spec and
the plan, and no verdict above rests on a conclusion carried from them.

Carried rather than re-derived: the coordinates round 1 recorded, and nothing
else. Every verdict above is this round's own, re-derived against the tree as
it stands.
